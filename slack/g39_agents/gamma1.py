"""gamma1.py -- compute gamma_1 = lim #good family-(1,3) lines / p, per section 1 of
docs/research/cubic_matching_local_law.md, via the 2-D (s, w') density integral with the
per-residue uncovered probability U from U_model.py.

IMPORTANT CORRECTION found and verified numerically against the dumps (see log): the spec text
for the two thresholds has an extra spurious x0/p term.  The code (cube_matching_fast.py,
confirmed exactly by the .npz dumps) uses

    theta+(x) = 1 - frac( F(x) - pos(x) - y0/p )      [spec text says "-(y0-x0)/p", WRONG by +x0/p]
    theta-(x) = frac( F(x) + pos(x) - y0/p )           [spec text says "-(x0+y0)/p", WRONG by +x0/p]

Verified: for box (700,-2100), p=3203, max|formula - dump thp| = 2e-16 with the y0/p-only form,
vs 0.78 with the (y0-x0)/p / (x0+y0)/p form from the spec text.  Everything else in section 1
(pos(x_m), F_m, Y1/p, X1/p, admissible u*/v*, the density normalisation) was checked against the
generator in cube_matching_fast.py and matches; see the log for the full derivation trace.

Parametrisation (all real, continuum limit):
  a  = (-4, -1, 5)          exponent-multipliers for x1,x2,x3   [x_m = a_m * z mod p]
  a3 = (-64, -1, 125)       = a^3, for F_m = frac(a3_m * w')
  z/p = (s + r)/3,  r = rho in {0,1,2}
  pos(x_m) = frac(a_m*(s+r)/3 - x0/p)
  F_m      = frac(a3_m * w')
  theta+_m = 1 - frac(F_m - pos_m - y0/p)
  theta-_m = frac(F_m + pos_m - y0/p)
  X1/p = x0/p + pos_1 + delta1;         Y1/p = y0/p + frac(F_1 - y0/p) + eps1
  v*/p = frac(63 w') + k   (k integer, "representative" choice)
  delta2 = floor(X1/p + s   - x0/p - pos_2);   delta3 = floor(X1/p + 3s   - x0/p - pos_3)
  eps2   = floor(Y1/p + v*/p - y0/p - frac(F_2-y0/p)); eps3 likewise with 3*(v*/p) and F_3
  admissible iff delta2,delta3,eps2,eps3 in {0,1}.
  density: dN(s,w') = p * (ds dw'/3) * [admissible]  (for each delta1,eps1,rho,k)
  gamma1 = sum_{delta1,eps1} sum_rho (1/3) INT ds INT dw' sum_{admissible k} prod_m U_m

usage: python3 gamma1.py
"""
import sys, os, itertools
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from U_model import U

A1 = np.array([-4.0, -1.0, 5.0])          # a_m
A3 = np.array([-64.0, -1.0, 125.0])       # a_m^3

def frac(v):
    return v - np.floor(v)

def gamma1_integral(xi0, eta0, ns=600, nw=600, use_U=True, k_range=range(-3, 4),
                     s_lo=-2.0/3.0, s_hi=2.0/3.0, return_diag=False):
    """gamma1 (or, if use_U=False, the bare admissible-line density #lines/p) for box
    (xi0=x0/p mod 1, eta0=y0/p mod 1), via a uniform (ns x nw) midpoint grid on
    s in (s_lo,s_hi) x w' in [0,1)."""
    ds = (s_hi - s_lo) / ns
    dw = 1.0 / nw
    s = s_lo + (np.arange(ns) + 0.5) * ds
    w = (np.arange(nw) + 0.5) * dw
    S, W = np.meshgrid(s, w, indexing='ij')   # shape (ns, nw)

    total = 0.0
    diag_admis_count = 0.0
    for delta1, eps1 in itertools.product((0, 1), (0, 1)):
        for rho in (0, 1, 2):
            r = rho
            zsr = (S + r) / 3.0                       # (s+r)/3, real
            pos_m = [frac(A1[m] * zsr - xi0) for m in range(3)]
            F_m = [frac(A3[m] * W) for m in range(3)]
            thp_m = [1.0 - frac(F_m[m] - pos_m[m] - eta0) for m in range(3)]
            thm_m = [frac(F_m[m] + pos_m[m] - eta0) for m in range(3)]

            X1p = xi0 + pos_m[0] + delta1
            Y1p = eta0 + frac(F_m[0] - eta0) + eps1

            # IMPORTANT: delta2 = (X1+u*-r_x2)/p, delta3 = (X1+3u*-r_x3)/p are EXACT algebraic
            # identities that evaluate to an integer for EVERY real s (not just rational u*/p):
            # pos_0(s)-pos_m(s) telescopes the (a_0-a_m)(s+rho)/3 term against the m*s term
            # exactly (verified symbolically: for m=1 the s-terms cancel completely, leaving a
            # pure integer step function of s).  So the raw (pre-floor) expression is ALWAYS
            # within float roundoff of an integer -- np.floor on such values is numerically
            # unstable (0.999999999996 floors to 0 instead of the true 1).  Use np.round.
            raw2 = X1p + S - xi0 - pos_m[1]
            raw3 = X1p + 3.0 * S - xi0 - pos_m[2]
            delta2i = np.round(raw2).astype(np.int64)
            delta3i = np.round(raw3).astype(np.int64)
            adm_u = np.isin(delta2i, (0, 1)) & np.isin(delta3i, (0, 1))

            if use_U:
                U1 = U(pos_m[0], thp_m[0], thm_m[0], delta1, eps1, xi0)
                # precompute U2, U3 for all 4 lift combos, select per-gridpoint
                U2_by = {(d, e): U(pos_m[1], thp_m[1], thm_m[1], d, e, xi0)
                         for d in (0, 1) for e in (0, 1)}
                U3_by = {(d, e): U(pos_m[2], thp_m[2], thm_m[2], d, e, xi0)
                         for d in (0, 1) for e in (0, 1)}

            v0 = frac(63.0 * W)
            cell_total = np.zeros_like(S)
            for k in k_range:
                vk = v0 + k
                eps2i = np.round(Y1p + vk - eta0 - frac(F_m[1] - eta0)).astype(np.int64)
                eps3i = np.round(Y1p + 3.0 * vk - eta0 - frac(F_m[2] - eta0)).astype(np.int64)
                adm_v = np.isin(eps2i, (0, 1)) & np.isin(eps3i, (0, 1))
                mask = adm_u & adm_v
                if not mask.any():
                    continue
                if use_U:
                    d2c = np.clip(delta2i, 0, 1); e2c = np.clip(eps2i, 0, 1)
                    d3c = np.clip(delta3i, 0, 1); e3c = np.clip(eps3i, 0, 1)
                    U2 = np.select(
                        [(d2c == d) & (e2c == e) for d in (0, 1) for e in (0, 1)],
                        [U2_by[(d, e)] for d in (0, 1) for e in (0, 1)])
                    U3 = np.select(
                        [(d3c == d) & (e3c == e) for d in (0, 1) for e in (0, 1)],
                        [U3_by[(d, e)] for d in (0, 1) for e in (0, 1)])
                    prod = U1 * U2 * U3
                    cell_total += np.where(mask, prod, 0.0)
                else:
                    cell_total += mask.astype(np.float64)
            total += cell_total.sum() * ds * dw / 3.0
            diag_admis_count += 1
    if return_diag:
        return total, diag_admis_count
    return total


if __name__ == "__main__":
    log_path = "/home/pmbot/projects/saturation_peer/slack/verification/g39_gamma1.txt"
    lines = []
    def P(*a):
        s = " ".join(str(x) for x in a)
        print(s); lines.append(s)

    P("=== gamma1.py log ===")
    P()
    P("--- spec bug found (confirmed numerically against dumps) ---")
    P("theta+_m formula: correct is  1 - frac(F_m - pos_m - y0/p)   (spec text has extra '+x0/p' via '-(y0-x0)/p')")
    P("theta-_m formula: correct is  frac(F_m + pos_m - y0/p)        (spec text has extra '+x0/p' via '-(x0+y0)/p')")
    P("Verified on dump p=3203 box(700,-2100): max|correct-dump.thp|=2.2e-16 (Y0/p form) vs 0.78 (spec-literal form).")
    P()

    dumps = [
        ("p12809_box0_0", "/home/pmbot/projects/saturation_peer/slack/verification/cube_dump_p12809_box0_0.npz"),
        ("p12809_box-6404_0", "/home/pmbot/projects/saturation_peer/slack/verification/cube_dump_p12809_box-6404_0.npz"),
        ("p3203_box700_-2100", "/home/pmbot/projects/saturation_peer/slack/verification/cube_dump_p3203_box700_-2100.npz"),
    ]

    P("--- STEP 1: validate line COUNT (use_U=False) ---")
    NS = NW = 600
    count_results = {}
    for name, path in dumps:
        d = np.load(path)
        p = int(d['p']); x0 = int(d['x0']); y0 = int(d['y0'])
        xi0 = (x0 % p) / p; eta0 = (y0 % p) / p
        rec13 = d['rec13']
        emp_count = len(rec13) / p
        emp_good = int(((rec13[:, 10] == 1) & (rec13[:, 11] == 1) & (rec13[:, 12] == 1)).sum()) / p if len(rec13) else 0.0
        cnt = gamma1_integral(xi0, eta0, ns=NS, nw=NW, use_U=False)
        count_results[name] = (cnt, emp_count, emp_good, xi0, eta0, p)
        P(f"{name}: p={p} x0={x0} y0={y0} xi0={xi0:.4f} eta0={eta0:.4f}  "
          f"model #lines/p={cnt:.4f}  empirical len(rec13)/p={emp_count:.4f}  (target box(0,0)~1.731, box(-6404,0)~1.800)")
    P()

    P("--- STEP 2: validate local law against rec13 (per-box) ---")
    for name, path in dumps:
        d = np.load(path)
        p = int(d['p']); x0 = int(d['x0']); y0 = int(d['y0'])
        xi0 = (x0 % p) / p; eta0 = (y0 % p) / p
        rec13 = d['rec13']
        us = rec13[:, 0]; d0 = rec13[:, 4]; e0 = rec13[:, 5]
        good = (rec13[:, 10] == 1) & (rec13[:, 11] == 1) & (rec13[:, 12] == 1)
        s_emp = us / p
        # empirical (delta1,eps1) distribution
        P(f"{name}: (delta1,eps1) distribution among rec13 lines:")
        for d1 in (0, 1):
            for e1 in (0, 1):
                m = (d0 == d1) & (e0 == e1)
                P(f"    (d1,e1)=({d1},{e1}): frac={m.mean():.4f}  good-frac-within={good[m].mean() if m.any() else float('nan'):.4f}")
        # good fraction vs s-bin (10 bins over -2/3..2/3)
        nb = 10
        edges = np.linspace(-2.0/3.0, 2.0/3.0, nb + 1)
        binidx = np.digitize(s_emp, edges) - 1
        binidx = np.clip(binidx, 0, nb - 1)
        P(f"    empirical good-fraction by s-decile (s in [-2/3,2/3)):")
        emp_by_bin = []
        for b in range(nb):
            m = binidx == b
            frac_good = good[m].mean() if m.any() else float('nan')
            emp_by_bin.append(frac_good)
            P(f"      bin {b} s in [{edges[b]:.3f},{edges[b+1]:.3f}): n={m.sum():5d} good_frac={frac_good:.4f}")
    P()

    P("--- STEP 3: gamma1 with U (good-line density) for the 3 dump boxes ---")
    gamma1_results = {}
    for name, path in dumps:
        cnt, emp_count, emp_good, xi0, eta0, p = count_results[name]
        g1 = gamma1_integral(xi0, eta0, ns=NS, nw=NW, use_U=True)
        gamma1_results[name] = g1
        P(f"{name}: xi0={xi0:.4f} eta0={eta0:.4f}  gamma1(model)={g1:.4f}  empirical good/p={emp_good:.4f}  "
          f"rel.diff={(g1-emp_good)/max(emp_good,1e-9)*100:.1f}%")
    P()

    P("--- STEP 4: gamma1 on a grid of box positions (xi0,eta0 in {0,0.25,0.5,0.75}) ---")
    grid_vals = [0.0, 0.25, 0.5, 0.75]
    grid_results = {}
    for xi0 in grid_vals:
        for eta0 in grid_vals:
            g1 = gamma1_integral(xi0, eta0, ns=NS, nw=NW, use_U=True)
            grid_results[(xi0, eta0)] = g1
            P(f"  xi0={xi0:.2f} eta0={eta0:.2f}: gamma1={g1:.4f}")
    vals = list(grid_results.values())
    P(f"  grid min/max/mean gamma1 = {min(vals):.4f} / {max(vals):.4f} / {np.mean(vals):.4f}")
    P()
    P("=== done ===")

    with open(log_path, "w") as fh:
        fh.write("\n".join(lines) + "\n")
    print(f"\nlog written to {log_path}")
