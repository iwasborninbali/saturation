"""validate_U.py -- Task A validation: compare U_model.U against the ground-truth dumps.

For each dump: for each residue x and each lift (delta,eps), compare cov[x,delta,eps]
(True=covered) with the predicted uncovered probability U(pos[x], thp[x], thm[x], delta, eps, x0/p).
Bin residues by (pi, thp, thm) into 8x8x8 cells (per lift), report empirical uncovered
frequency vs mean predicted U in each populated cell (max/mean abs deviation), and the
overall totals sum(1-cov) vs sum(U).

Also validates intermediate steps directly against kp,km,ap,bm,npl,nmi:
  - P(k+=3) empirical vs 1/2, P(k-=3) vs 1/2
  - distribution of n (npl,nmi) given class and thresholds, vs the model's n=1+#matches law
    (checked via the K0-rotation formula for partner positions).
"""
import numpy as np
import sys
sys.path.insert(0, '/home/pmbot/projects/saturation_peer/slack/g39_agents')
from U_model import U

DUMPS = [
    '/home/pmbot/projects/saturation_peer/slack/verification/cube_dump_p12809_box0_0.npz',
    '/home/pmbot/projects/saturation_peer/slack/verification/cube_dump_p12809_box-6404_0.npz',
    '/home/pmbot/projects/saturation_peer/slack/verification/cube_dump_p3203_box700_-2100.npz',
]

log = []
def P(*a):
    s = ' '.join(str(x) for x in a)
    print(s); log.append(s)

for path in DUMPS:
    d = np.load(path)
    p = int(d['p']); x0 = int(d['x0']); y0 = int(d['y0'])
    pos = d['pos']; thp = d['thp']; thm = d['thm']
    kp = d['kp']; ap = d['ap']; npl = d['npl']
    km = d['km']; bm = d['bm']; nmi = d['nmi']
    cov = d['cov']
    x0p = (x0 % p) / p

    P("="*100)
    P(f"dump {path}")
    P(f"p={p} x0={x0} y0={y0} x0p={x0p:.6f}")

    # ---- intermediate-step checks ----
    P(f"  P(kp=3) empirical = {np.mean(kp==3):.5f}  (model: 1/2);  P(kp=1)={np.mean(kp==1):.5f}  P(kp=2,other)={np.mean((kp!=1)&(kp!=3)):.5f} [count={(np.sum((kp!=1)&(kp!=3)))}]")
    P(f"  P(km=3) empirical = {np.mean(km==3):.5f}  (model: 1/2);  P(km=1)={np.mean(km==1):.5f}  P(km=2,other)={np.mean((km!=1)&(km!=3)):.5f} [count={(np.sum((km!=1)&(km!=3)))}]")
    # given kp=3, distribution of npl in {1,2,3} (only meaningful when kp==3 exactly)
    m3 = (kp == 3)
    vals, cnts = np.unique(npl[m3], return_counts=True)
    P(f"  kp=3: npl distribution {dict(zip(vals.tolist(), (cnts/cnts.sum()).round(4).tolist()))}  (model expects mass on 1,2,3 depending on pi,thp -- not a fixed law, see cell test below)")

    # ---- full U validation, binned ----
    total_unc_emp = 0
    total_U = 0
    nb = 8
    pib = np.clip((pos*nb).astype(int), 0, nb-1)
    thpb = np.clip((thp*nb).astype(int), 0, nb-1)
    thmb = np.clip((thm*nb).astype(int), 0, nb-1)
    for delta in (0, 1):
        for eps in (0, 1):
            Uval = U(pos, thp, thm, delta, eps, x0p)
            unc_emp = (~cov[:, delta, eps]).astype(np.float64)
            total_unc_emp += unc_emp.sum()
            total_U += Uval.sum()
            # bin
            cellkey = (pib*nb + thpb)*nb + thmb
            order = np.argsort(cellkey)
            ck_sorted = cellkey[order]
            uemp_sorted = unc_emp[order]
            Uval_sorted = Uval[order]
            boundaries = np.flatnonzero(np.diff(ck_sorted)) + 1
            starts = np.concatenate(([0], boundaries))
            ends = np.concatenate((boundaries, [len(ck_sorted)]))
            max_abs_dev = 0.0; sum_abs_dev = 0.0; n_cells = 0; wsum=0
            for s_, e_ in zip(starts, ends):
                n = e_ - s_
                emp_freq = uemp_sorted[s_:e_].mean()
                pred_mean = Uval_sorted[s_:e_].mean()
                dev = abs(emp_freq - pred_mean)
                max_abs_dev = max(max_abs_dev, dev)
                sum_abs_dev += dev*n; wsum += n; n_cells += 1
            P(f"  lift ({delta},{eps}): populated cells={n_cells:4d}  max|emp-pred| over cells={max_abs_dev:.4f}  "
              f"pop-weighted mean|emp-pred|={sum_abs_dev/wsum:.5f}  Sigma(1-cov)={unc_emp.sum():.0f}  Sigma(U)={Uval.sum():.2f}")

    P(f"  OVERALL: Sigma_{{x,d,e}}(1-cov) = {total_unc_emp:.0f}   (|S0|, target ~1.75p = {1.75*p:.1f}, ratio to p = {total_unc_emp/p:.4f})")
    P(f"  OVERALL: Sigma_{{x,d,e}}(U)     = {total_U:.2f}  (ratio to p = {total_U/p:.4f})")
    P(f"  OVERALL relative diff (Sigma U - Sigma(1-cov)) / p = {(total_U-total_unc_emp)/p:.5f}")


# ---------------------------------------------------------------------------
# supplementary check: is the 8x8x8-cell scatter consistent with pure sampling
# noise (n residues/cell, Bernoulli(pred)), or is there a systematic bias?
# Also: U-decile calibration (pools far more residues per bin than the 8x8x8
# grid, so less noise) -- the real test of whether U is correctly calibrated.
# ---------------------------------------------------------------------------
P("\n" + "#"*100)
P("# supplementary: z-score check (8x8x8 grid) + U-decile calibration (pooled, low-noise)")
P("#"*100)
for path in DUMPS:
    d = np.load(path)
    p = int(d['p']); x0 = int(d['x0'])
    pos = d['pos']; thp = d['thp']; thm = d['thm']; cov = d['cov']
    x0p = (x0 % p) / p
    P(f"\n--- {path} (p={p}) ---")
    nb = 8
    pib = np.clip((pos*nb).astype(int), 0, nb-1)
    thpb = np.clip((thp*nb).astype(int), 0, nb-1)
    thmb = np.clip((thm*nb).astype(int), 0, nb-1)
    for delta in (0, 1):
        for eps in (0, 1):
            Uval = U(pos, thp, thm, delta, eps, x0p)
            unc_emp = (~cov[:, delta, eps]).astype(np.float64)
            cellkey = (pib*nb + thpb)*nb + thmb
            order = np.argsort(cellkey); ck = cellkey[order]; ue = unc_emp[order]; uv = Uval[order]
            b_ = np.flatnonzero(np.diff(ck)) + 1
            starts = np.concatenate(([0], b_)); ends = np.concatenate((b_, [len(ck)]))
            zs = []
            for s_, e_ in zip(starts, ends):
                n = e_ - s_
                if n < 5: continue
                pr = uv[s_:e_].mean()
                emp = ue[s_:e_].mean()
                var = pr*(1-pr)/n
                if var <= 0: continue
                zs.append((emp-pr)/np.sqrt(var))
            zs = np.array(zs)
            P(f"  lift ({delta},{eps}): cells(n>=5)={len(zs):3d}  mean z={zs.mean():+.3f}  std z={zs.std():.3f}  "
              f"frac|z|>2={np.mean(np.abs(zs)>2):.3f}  frac|z|>3={np.mean(np.abs(zs)>3):.3f}  (pure noise expects mean~0,std~1,frac>2~0.05,frac>3~0.003)")
            # decile calibration
            ndec = 20 if p > 5000 else 10
            order2 = np.argsort(Uval)
            edges = np.linspace(0, len(order2), ndec+1).astype(int)
            rows = []
            for i in range(ndec):
                idx = order2[edges[i]:edges[i+1]]
                if len(idx) == 0: continue
                rows.append((Uval[idx].mean(), unc_emp[idx].mean(), len(idx)))
            maxdev = max(abs(a-b) for a,b,n in rows)
            P(f"    U-decile calib ({ndec} bins, ~{len(order2)//ndec} residues/bin): max|pred-emp|={maxdev:.4f}  "
              f"table(pred,emp,n)=" + ",".join(f"({a:.3f},{b:.3f},{n})" for a,b,n in rows))

with open('/home/pmbot/projects/saturation_peer/slack/verification/g39_U_validation.txt', 'w') as f:
    f.write('\n'.join(log) + '\n')
print("\nWROTE /home/pmbot/projects/saturation_peer/slack/verification/g39_U_validation.txt")
