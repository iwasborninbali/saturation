"""gamma2_continuum.py -- the CONTINUUM integral for gamma_2 = lim (#unordered pairs of good
family-(1,3) lines sharing a point)/p, per section 3 of
docs/research/cubic_matching_local_law.md, reusing gamma1.py's line-1 parametrisation
(s=u*/p, w', rho=u* mod 3, admissible representatives, U_model.U) and extending it with the
role/config machinery of section 3 (six configurations (m,m'), fractional-ratio digits).

======================================================================================
DERIVATION (worked out in this file; see the log for the numeric validation)
======================================================================================

Line 1 (exactly gamma1.py's parametrisation): free real grid (s,w') with s=u1*/p in (-2/3,2/3),
w' uniform in [0,1); digit rho=u1* mod 3 (uniform 0,1,2, weight 1/3); lift (delta1,eps1) of the
role-1 point (free, summed over {0,1}^2); z/p=(s+rho)/3; pos_n=frac(a_n*z/p-xi0), F_n=frac(a_n^3
w') for n=1,2,3 (a=(-4,-1,5), a^3=(-64,-1,125)); v1*/p = frac(63 w')+k1 (representative search,
k1 an integer, "k1-loop"); X1p,Y1p and, for n=2,3, delta_n,eps_n via the EXACT-integer-lift trick
(np.round on the algebraically-integer raw expression, per gamma1.py's bug-fix comment); line 1
admissible iff delta_n,eps_n in {0,1} for n=2,3.

A pair is a CONFIGURATION (m,m'), m = role of the shared point on line 1, m' = its role on line
2, m != m' (6 configs, spec sec.3). Given line 1's data above and the shared role m, the shared
point's own (pos,F,thp,thm,delta,eps) are exactly line 1's role-m data (a lattice point's lift is
intrinsic to the point, not to which line refers to it -- so line 2 must reproduce the SAME lift
at role m').

z' = (a_m/a_m') * z =: (P/Q) z in lowest terms (P,Q coprime integers, Q in {1,4,5}):
  Q z' = P z (mod p)  =>  z' = (P z + j p)/Q for a digit j in {0,...,Q-1} (uniform, independent
  of s in the continuum limit -- see the log's "digit-uniformity" note); z'/p = (P*(z/p)+j)/Q.
  (Q=1: j=0 only, weight 1; the four fractional configs have Q=4 or 5, weight 1/Q per j.)

W-digit / w'' (EXACT change of variables, not a Monte-Carlo average -- worked out below):
  a*(z')^3 = (P/Q)^3 * a*z^3 = (P^3/Q^3) W, W = a z^3 mod p, w'=W/p. The physical rule
  (spec sec.3(ii)) is w'' = frac(P^3 * (w'+i)/Q^3) for a fine digit i in {0,...,Q^3-1} (uniform,
  independent of w'). We do NOT loop i explicitly: for any target function G,
     INT_0^1 dw' (1/Q^3) SUM_{i=0}^{Q^3-1} G(w', frac((w'+i)/Q^3))
       = INT_0^1 dw'' G(frac(Q^3 w''), w'')                              (*)
  (proof: substitute v=(w'+i)/Q^3; as i ranges over 0..Q^3-1 the intervals [i/Q^3,(i+1)/Q^3)
  tile [0,1) exactly, and on each piece w'=frac(Q^3 v) exactly; sum over i, then relabel v->w'').
  So we replace the (w', i) pair by a SINGLE grid variable t in [0,1) and set
     w'_line1 := frac(Q^3 * t),         w'' := frac(P^3 * t)
  (Q=1 recovers w'_line1 = t = w' directly, and w'' = frac(P^3 t) = frac(64 w') / frac(-125 w')
  for the two integer-ratio configs (1,2),(3,2) -- matches spec sec.3 exactly, no digit needed
  there). This is an EXACT identity (*), not an approximation, and replaces a 64- or 125-wide
  inner loop by a change of grid variable -- the key efficiency device of this file.

Line 2: anchor role m' with KNOWN lift (delta_shared,eps_shared) = line 1's role-m lift; free
representative searches u2*/p = frac(3 z'/p) + k2, v2*/p = frac(63 w'') + k3 (k2,k3-loops, exactly
analogous to line 1's v1*-loop -- u2*,v2* are DETERMINED residues here, unlike line 1's free s).
pos'_n, F'_n, thp'_n, thm'_n as usual; X'_{m'}p,Y'_{m'}p from the anchor, and for n != m'
(INCLUDING n=1 if m' != 1 -- this is exactly the spec's "X'_1+u'*, X'_1+3u'*" box constraint,
now derived from the m' anchor rather than a free role-1 lift) delta'_n,eps'_n via the same
np.round trick; line 2 admissible iff delta'_n,eps'_n in {0,1} for all n != m'.

P(both good) = U(shared) * PROD_{n!=m} U(line1, n) * PROD_{n!=m'} U(line2, n)   [5 distinct
residues, shared one counted once -- the two lines' "other" residues are pairwise distinct in
|a_n| by construction of family (1,3), matching spec sec.3].

Density and normalisation: dN(s,t) = p*(ds*dt/3)*(1/Q) * [line1 adm] * [line2 adm], summed over
(delta1,eps1) in {0,1}^2, rho in {0,1,2}, j in {0,...,Q-1}, and the representative loops
k1,k2,k3 (each a genuinely distinct actual line/point -- summed, not averaged); integrated over
(s,t) in (-2/3,2/3) x [0,1). UNORDERED PAIRS: config (m,m') and (m',m) are the same physical pair
described from the two lines' sides (verified below to give equal integrals, exactly mirroring
gamma2.py's finite-p symmetry finding) -- we take the THREE configs with m<m' -- {1,2}=(1,2),
{1,3}=(1,3),{2,3}=(2,3) -- and SUM them (no further /2); gamma2 = sum of these three integrals.
We also compute the other three (m,m') with m>m' as a symmetry check (logged).

usage: python3 gamma2_continuum.py
"""
import sys, os, itertools, time
from fractions import Fraction
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from U_model import U

A1 = np.array([-4.0, -1.0, 5.0])          # a_m, m=1,2,3 (index 0,1,2)
A3 = np.array([-64.0, -1.0, 125.0])       # a_m^3
A1_INT = (-4, -1, 5)
SHIFT = np.array([0, 1, 3])               # shift_n (in units of u*), role n=1,2,3

CONFIGS_ALL = [(1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2)]
CONFIGS_HALF = [(1, 2), (1, 3), (2, 3)]   # m<m': counted once per unordered pair


def frac(x):
    return x - np.floor(x)


def PQ(m, mp):
    r = Fraction(A1_INT[m - 1], A1_INT[mp - 1])
    return r.numerator, r.denominator


def compute_line(z_over_p, w_prime, r0, d0, e0, s_val, v_val, xi0, eta0):
    """Generalisation of gamma1.py's per-line block to an arbitrary anchor role r0 (1,2,3)
    with GIVEN lift (d0,e0) (python int or array). Returns pos,Fm,thp,thm (lists of 3 arrays,
    shape = broadcast of z_over_p,w_prime), delta,eps (lists of 3 int arrays, shape = broadcast
    of everything incl. s_val,v_val), admissible (bool array over the roles != r0)."""
    pos = [frac(A1[n] * z_over_p - xi0) for n in range(3)]
    Fm = [frac(A3[n] * w_prime) for n in range(3)]
    thp = [1.0 - frac(Fm[n] - pos[n] - eta0) for n in range(3)]
    thm = [frac(Fm[n] + pos[n] - eta0) for n in range(3)]

    base_shape = np.broadcast(z_over_p, w_prime, s_val, v_val).shape
    Xr0p = xi0 + pos[r0 - 1] + d0
    Yr0p = eta0 + frac(Fm[r0 - 1] - eta0) + e0

    delta = [None, None, None]
    eps = [None, None, None]
    admissible = np.ones(base_shape, dtype=bool)
    for n in range(3):
        if n == r0 - 1:
            delta[n] = np.broadcast_to(np.asarray(d0, dtype=np.int64), base_shape)
            eps[n] = np.broadcast_to(np.asarray(e0, dtype=np.int64), base_shape)
            continue
        shift_diff = float(SHIFT[n] - SHIFT[r0 - 1])
        Xnp = Xr0p + shift_diff * s_val
        dn = np.round(Xnp - xi0 - pos[n]).astype(np.int64)
        Ynp = Yr0p + shift_diff * v_val
        en = np.round(Ynp - eta0 - frac(Fm[n] - eta0)).astype(np.int64)
        delta[n] = dn
        eps[n] = en
        admissible &= np.isin(dn, (0, 1)) & np.isin(en, (0, 1))
    return pos, Fm, thp, thm, delta, eps, admissible


def U_role(pos_n, thp_n, thm_n, delta_n, eps_n, xi0, shape):
    dc = np.clip(np.broadcast_to(delta_n, shape), 0, 1)
    ec = np.clip(np.broadcast_to(eps_n, shape), 0, 1)
    out = np.zeros(shape, dtype=np.float64)
    for dv, ev in itertools.product((0, 1), (0, 1)):
        m = (dc == dv) & (ec == ev)
        if m.any():
            uval = U(pos_n, thp_n, thm_n, dv, ev, xi0)
            uval = np.broadcast_to(uval, shape)
            out = np.where(m, uval, out)
    return out


def gamma2_pair_integral(m, mp, xi0, eta0, ns, nt, s_lo=-2.0 / 3.0, s_hi=2.0 / 3.0,
                          k1_range=range(-1, 2), k2_range=range(-1, 2), k3_range=range(-1, 2),
                          use_U=True):
    """The single-config (m,m') integral (real number, already the 'p' density, i.e. gamma2
    contribution *p is this value * p... no: this returns the dimensionless integral, i.e. the
    contribution to gamma2 directly, comparable to pred_total/p in gamma2.py)."""
    P, Q = PQ(m, mp)
    ds = (s_hi - s_lo) / ns
    dt = 1.0 / nt
    s = s_lo + (np.arange(ns) + 0.5) * ds
    t = (np.arange(nt) + 0.5) * dt
    S, T = np.meshgrid(s, t, indexing='ij')

    total = 0.0
    for delta1, eps1 in itertools.product((0, 1), (0, 1)):
        for rho in (0, 1, 2):
            z_over_p = (S + rho) / 3.0
            w_line1 = frac(float(Q) ** 3 * T)
            # v1* representative loop
            for k1 in k1_range:
                v1p = frac(63.0 * w_line1) + k1
                pos1, F1, thp1, thm1, d1arr, e1arr, adm1 = compute_line(
                    z_over_p, w_line1, 1, delta1, eps1, S, v1p, xi0, eta0)
                if not adm1.any():
                    continue
                shape = adm1.shape
                if use_U:
                    U1 = [U_role(pos1[n], thp1[n], thm1[n], d1arr[n], e1arr[n], xi0, shape)
                          for n in range(3)]
                else:
                    U1 = [np.ones(shape) for _ in range(3)]
                other2_line1 = np.ones(shape)
                for n in range(3):
                    if n != m - 1:
                        other2_line1 = other2_line1 * U1[n]
                sharedU = U1[m - 1]
                shared_delta = d1arr[m - 1]
                shared_eps = e1arr[m - 1]
                pos_shared = pos1[m - 1]

                for j in range(Q):
                    w_line2 = frac(P ** 3 * T)
                    zprime_over_p = (P * z_over_p + j) / Q
                    s2_base = frac(3.0 * zprime_over_p)
                    v2_base = frac(63.0 * w_line2)
                    for k2 in k2_range:
                        s2p = s2_base + k2
                        for k3 in k3_range:
                            v2p = v2_base + k3
                            pos2, F2, thp2, thm2, d2arr, e2arr, adm2 = compute_line(
                                zprime_over_p, w_line2, mp, shared_delta, shared_eps,
                                s2p, v2p, xi0, eta0)
                            mask = adm1 & adm2
                            if not mask.any():
                                continue
                            if use_U:
                                other2_line2 = np.ones(shape)
                                for n in range(3):
                                    if n != mp - 1:
                                        Un = U_role(pos2[n], thp2[n], thm2[n], d2arr[n],
                                                    e2arr[n], xi0, shape)
                                        other2_line2 = other2_line2 * Un
                                prod = sharedU * other2_line1 * other2_line2
                            else:
                                prod = np.ones(shape)
                            total += np.where(mask, prod, 0.0).sum() * ds * dt / 3.0 / Q
    return total


def gamma2_continuum(xi0, eta0, ns=400, nt=400, k1_range=range(-1, 2),
                      k2_range=range(-1, 2), k3_range=range(-1, 2), use_U=True,
                      configs=CONFIGS_HALF, return_by_config=False):
    by_config = {}
    total = 0.0
    for (m, mp) in configs:
        v = gamma2_pair_integral(m, mp, xi0, eta0, ns, nt, k1_range=k1_range,
                                  k2_range=k2_range, k3_range=k3_range, use_U=use_U)
        by_config[(m, mp)] = v
        total += v
    if return_by_config:
        return total, by_config
    return total


if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(__file__))
    from gamma1 import gamma1_integral

    log_path = "/home/pmbot/projects/saturation_peer/slack/verification/g39_gamma2_continuum.txt"
    lines = []

    def P_(*a):
        s = " ".join(str(x) for x in a)
        print(s); lines.append(s)

    P_("=== gamma2_continuum.py log ===")
    P_()
    P_("Method: continuum (s,t) grid for line 1's own (s,w') parametrisation, with t the")
    P_("change-of-variables grid variable for the divide-configs' W-digit (exact identity, see")
    P_("module docstring); k1/k2/k3 = representative-search loops for v1*, u2*, v2*.")
    P_("Convention for the unordered-pair sum: take configs with m<m' -- {1,2}=(1,2), {1,3}=(1,3),")
    P_("{2,3}=(2,3) -- and SUM (no /2); (m,m') and (m',m) verified numerically equal below.")
    P_()

    dumps = [
        ("p12809_box0_0", "/home/pmbot/projects/saturation_peer/slack/verification/cube_dump_p12809_box0_0.npz"),
        ("p12809_box-6404_0", "/home/pmbot/projects/saturation_peer/slack/verification/cube_dump_p12809_box-6404_0.npz"),
        ("p3203_box700_-2100", "/home/pmbot/projects/saturation_peer/slack/verification/cube_dump_p3203_box700_-2100.npz"),
    ]
    dump_boxes = []
    for name, path in dumps:
        d = np.load(path)
        p = int(d['p']); x0 = int(d['x0']); y0 = int(d['y0'])
        xi0 = (x0 % p) / p; eta0 = (y0 % p) / p
        dump_boxes.append((name, xi0, eta0, p))

    t0 = time.time()
    P_("--- STEP 0: symmetry check config(m,m') == config(m',m), small grid ---")
    NS0, NT0 = 100, 100
    for name, xi0, eta0, p in dump_boxes:
        _, byc = gamma2_continuum(xi0, eta0, ns=NS0, nt=NT0, configs=CONFIGS_ALL,
                                   k2_range=range(-2, 3), k3_range=range(-2, 3),
                                   return_by_config=True)
        P_(f"{name}: xi0={xi0:.4f} eta0={eta0:.4f}")
        for (m, mp) in [(1, 2), (1, 3), (2, 3)]:
            a = byc[(m, mp)]; b = byc[(mp, m)]
            P_(f"    config({m},{mp})={a:.5f}  config({mp},{m})={b:.5f}  reldiff={abs(a-b)/max(a,1e-9):.4f}")
    P_(f"  [{time.time()-t0:.1f}s elapsed]")
    P_()

    P_("--- STEP 1: validate against gamma2.py hybrid gamma2 (0.0283, 0.0304, 0.0300) and role-set")
    P_("    good-good counts/p (box0_0: 0.0091/0.0081/0.0103; box-6404_0: 0.0098/0.0101/0.0116;")
    P_("    box700_-2100(p3203): 0.0069/0.0106/0.0078), small-ish grid for speed ---")
    NS1, NT1 = 200, 200
    step1 = {}
    for name, xi0, eta0, p in dump_boxes:
        t1 = time.time()
        total, byc = gamma2_continuum(xi0, eta0, ns=NS1, nt=NT1, configs=CONFIGS_HALF,
                                       return_by_config=True)
        step1[name] = (total, byc)
        P_(f"{name}: xi0={xi0:.4f} eta0={eta0:.4f}  gamma2(continuum)={total:.4f}  "
           f"{{1,2}}={byc[(1,2)]:.4f} {{1,3}}={byc[(1,3)]:.4f} {{2,3}}={byc[(2,3)]:.4f}  "
           f"[{time.time()-t1:.1f}s]")
    P_()

    P_("--- STEP 2: gamma2 (and gamma1, gamma1-gamma2) for xi0 in {0,0.1,...,0.9}, eta0 in {0,0.5} ---")
    NS2, NT2 = 400, 400
    grid_results = {}
    xi_vals = [round(0.1 * i, 1) for i in range(10)]
    for eta0 in (0.0, 0.5):
        for xi0 in xi_vals:
            t2 = time.time()
            g2 = gamma2_continuum(xi0, eta0, ns=NS2, nt=NT2, configs=CONFIGS_HALF)
            g1 = gamma1_integral(xi0, eta0, ns=600, nw=600)
            grid_results[(xi0, eta0)] = (g1, g2, g1 - g2)
            P_(f"  xi0={xi0:.1f} eta0={eta0:.1f}: gamma1={g1:.4f} gamma2={g2:.4f} "
               f"gamma1-gamma2={g1-g2:.4f}  [{time.time()-t2:.1f}s]")
    vals = list(grid_results.values())
    diffs = [v[2] for v in vals]
    P_()
    P_(f"  grid min/max gamma1-gamma2 = {min(diffs):.4f} / {max(diffs):.4f}")
    argmin = min(grid_results, key=lambda k: grid_results[k][2])
    P_(f"  argmin at xi0={argmin[0]}, eta0={argmin[1]}: gamma1-gamma2={grid_results[argmin][2]:.4f}")
    P_(f"  1/12 = {1.0/12:.4f}; margin at argmin = {grid_results[argmin][2]-1.0/12:.4f}")
    P_()
    P_("=== done ===")

    with open(log_path, "w") as fh:
        fh.write("\n".join(lines) + "\n")
    print(f"\nlog written to {log_path}")
