#!/usr/bin/env python3
"""slack/c_agents/milp_ceiling.py — agent "milp_ceiling".
Task: the CEILING of the "selection" approach to the class-graph cover problem of
docs/research/pair_bound_notes.md §25-26 (module slack/cyc_model.py).

The free LP (cyc_model.lp) lets t_G range continuously over [0,1] per group.  A "selection
rule" (t_G in {0, 1/2, 1} only, i.e. "unused / matched(demand 1/2) / full block(demand 0)")
is what any *explicit local rule* can realistically compute (the rule from §26 reads a
bounded window of the cycle and outputs one of 3 choices per group).  This script computes
the EXACT optimum of that restricted problem — a genuine mixed-integer program (continuous
edge weights, t_G in {0,1/2,1}) — via scipy.optimize.milp (HiGHS branch & bound), and asks:

  (1) does restricting t to {0,1/2,1} lose anything relative to the free continuous LP?
      i.e. is the free LP's optimal vertex already half-integral?
  (2) on the MILP-optimal solution, what distinguishes a SELECTED group (t_G > 0) from an
      UNSELECTED one (t_G = 0), in terms of the local ("window") arrangement of the nearest
      other candidate-special vertices around its own 4 vertices?

MILP encoding.  t_G in {0, 1/2, 1} is encoded as a single bounded integer n_G in {0,1,2}
with t_G = n_G / 2 (equivalent to, but simpler than, the two-binary z1,z2 encoding suggested
in the task brief — scipy.optimize.milp/HiGHS handles bounded general integers natively).
Substituting into the model of cyc_model.lp: a class v in group G gets coefficient 0.5 (not
1.0) on n_G in the covering constraint, and the objective coefficient of n_G is 6*0.5 = 3
(so that at n_G=2, i.e. t_G=1, the group costs 6, matching cyc_model exactly).

Usage (run from repo root):
    /Users/iwasborninbali/venvs/sat/bin/python3 slack/c_agents/milp_ceiling.py            # full run
    /Users/iwasborninbali/venvs/sat/bin/python3 slack/c_agents/milp_ceiling.py quick       # smaller/faster smoke test
See docs/research/c_agents/milp_ceiling.md for the write-up and numbers.
"""
import sys, os, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import cyc_model as cm
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import csr_matrix
from collections import defaultdict

TOL = 1e-6

# ---------------------------------------------------------------------- MILP core (§ task)
def milp_solve(M, groups_subset=None, time_limit=120, mip_gap=1e-9):
    """Exact optimum with t_G constrained to {0, 1/2, 1} and continuous edge weights w_e >= 0,
    same cost/feasibility model as cyc_model.lp.  n_G integer in {0,1,2}, t_G := n_G/2.
    Returns (saving, w:{edge:weight}, t:{groupkey:t_value in {0,.5,1}}, res)."""
    cycles = M['cycles']; groups = M['groups'] if groups_subset is None else groups_subset
    E = cm.edges_of(M); eidx = {e: j for j, e in enumerate(E)}; nE = len(E); nG = len(groups)
    classes = [c for seq in cycles for c in seq]; cidx = {c: i for i, c in enumerate(classes)}
    rows = []; cols = []; vals = []
    for c, seq in enumerate(cycles):
        L = len(seq)
        for i, v in enumerate(seq):
            r = cidx[v]
            rows += [r, r]; cols += [eidx[(c, (i - 1) % L)], eidx[(c, i)]]; vals += [1.0, 1.0]
    for j, (g, cl) in enumerate(groups):
        for v in cl:
            rows.append(cidx[v]); cols.append(nE + j); vals.append(0.5)  # t_G = 0.5 * n_G
    A = csr_matrix((vals, (rows, cols)), shape=(len(classes), nE + nG))
    c_obj = np.concatenate([4 * np.ones(nE), 3 * np.ones(nG)])  # 6*t_G = 6*(0.5*n_G) = 3*n_G
    integrality = np.concatenate([np.zeros(nE), np.ones(nG)])
    lb = np.zeros(nE + nG); ub = np.concatenate([np.full(nE, np.inf), np.full(nG, 2.0)])
    con = LinearConstraint(A, lb=np.ones(len(classes)), ub=np.inf)
    res = milp(c_obj, integrality=integrality, bounds=Bounds(lb, ub), constraints=con,
               options=dict(time_limit=time_limit, mip_rel_gap=mip_gap))
    assert res.success, (M['p'], M['k'], res.status, res.message)
    saving = 4 * (M['p'] - 1) - res.fun
    w = {E[j]: res.x[j] for j in range(nE)}
    t = {groups[j][0]: res.x[nE + j] / 2.0 for j in range(nG)}
    return saving, w, t, res

def half_integral_gap(t):
    """max distance of any t-value from the nearest multiple of 1/2 (0 = already half-integral)."""
    if not t: return 0.0
    return max(abs(v - round(v * 2) / 2) for v in t.values())

def status_of(tval):
    if tval > 1 - 0.01: return 'full(t=1)'
    if tval > 0.01: return 'half(t=1/2)'
    return 'unused(t=0)'

# ------------------------------------------------------------------- window statistics
def group_window_features(M, groups):
    """For every group G, and each of its 4 vertices v: distance (# cycle steps) and
    alternation flag (odd distance <=> different K/M type, since a <k>-cycle strictly
    alternates K,M,K,M,... by construction) to the NEAREST OTHER candidate-special vertex
    (candidate pool = union of the vertex sets of ALL groups of the model, "specials" in the
    sense of pair_bound_notes.md §25-26, independent of which groups end up selected) in the
    + and - cyclic directions.  Returns {groupkey: [(d_prev,alt_prev,d_next,alt_next), x4]}."""
    owner = {}
    for g, cl in groups:
        for v in cl: owner[v] = g
    feats = defaultdict(list)
    for c, seq in enumerate(M['cycles']):
        L = len(seq)
        sp = [(i, v) for i, v in enumerate(seq) if v in owner]
        n = len(sp)
        if n <= 1: continue
        for idx, (i, v) in enumerate(sp):
            i_next, v_next = sp[(idx + 1) % n]
            i_prev, v_prev = sp[(idx - 1) % n]
            d_next = (i_next - i) % L; d_prev = (i - i_prev) % L
            assert (d_next % 2 == 1) == (v_next[0] != v[0])   # sanity: parity <=> type change
            assert (d_prev % 2 == 1) == (v_prev[0] != v[0])
            feats[owner[v]].append((d_prev, d_prev % 2 == 1, d_next, d_next % 2 == 1))
    return feats

def window_report(M, groups, t_solution, label, print_fn=print):
    feats = group_window_features(M, groups)
    buckets = defaultdict(list)
    for g, cl in groups:
        st = status_of(t_solution.get(g, 0.0))
        for row in feats.get(g, []):
            buckets[st].append(row)
    print_fn(f"--- window stats: {label} (candidate pool = all {len(groups)} groups' vertices) ---")
    out = {}
    for st in ('full(t=1)', 'half(t=1/2)', 'unused(t=0)'):
        rows = buckets[st]
        if not rows:
            print_fn(f"  {st:12s}: (none)"); continue
        d_all = [r[0] for r in rows] + [r[2] for r in rows]
        alt_all = [r[1] for r in rows] + [r[3] for r in rows]
        min_d = [min(r[0], r[2]) for r in rows]
        either_alt = [r[1] or r[3] for r in rows]
        both_alt = [r[1] and r[3] for r in rows]
        rec = dict(n_vertices=len(rows), avg_gap=float(np.mean(d_all)), avg_min_gap=float(np.mean(min_d)),
                   frac_alt_gap=float(np.mean(alt_all)), frac_either_side_alt=float(np.mean(either_alt)),
                   frac_both_sides_alt=float(np.mean(both_alt)))
        out[st] = rec
        print_fn(f"  {st:12s}: n_vertices={rec['n_vertices']:5d}  avg_gap={rec['avg_gap']:6.2f}  "
                 f"avg_min_gap={rec['avg_min_gap']:6.2f}  frac_alternating_gap={rec['frac_alt_gap']:.3f}  "
                 f"frac(>=1 side alt)={rec['frac_either_side_alt']:.3f}  frac(both sides alt)={rec['frac_both_sides_alt']:.3f}")
    return out

# ----------------------------------------------------------------------------- harness
REAL_INSTANCES = [(101, 2), (199, 2), (199, 3)]
SYN_BASES = [(101, 2), (199, 2), (199, 3)]

def run_real(print_fn=print):
    rows = []
    for p, k in REAL_INSTANCES:
        M = cm.build(p, k)
        t0 = time.time(); s_lp, w_lp, t_lp = cm.lp(M); dt_lp = time.time() - t0
        gap = half_integral_gap(t_lp)
        t0 = time.time(); s_milp, w_milp, t_milp, res = milp_solve(M); dt_milp = time.time() - t0
        ng = len(M['groups'])
        rows.append(dict(p=p, k=k, ngroups=ng, lp=s_lp, lp_per=s_lp / ng, milp=s_milp, milp_per=s_milp / ng,
                          half_int_gap=gap, dt_lp=dt_lp, dt_milp=dt_milp, M=M, t_milp=t_milp))
        print_fn(f"REAL p={p:4d} k={k}: G8={ng:4d}  LP saving={s_lp:8.3f} ({s_lp/ng:.4f}/grp)  "
                 f"MILP saving={s_milp:8.3f} ({s_milp/ng:.4f}/grp)  (LP-MILP)/grp={ (s_lp-s_milp)/ng:.6f}  "
                 f"LP-half-int-gap={gap:.2e}  t(ms): lp={1000*dt_lp:.0f} milp={1000*dt_milp:.0f}")
    return rows

def run_synthetic(seeds=range(8), print_fn=print):
    rows = []
    for p, k in SYN_BASES:
        M = cm.build(p, k)
        for seed in seeds:
            Ms = cm.synthetic(M, seed)
            s_lp, w_lp, t_lp = cm.lp(Ms)
            gap = half_integral_gap(t_lp)
            s_milp, w_milp, t_milp, res = milp_solve(Ms)
            ng = len(Ms['groups'])
            rows.append(dict(p=p, k=k, seed=seed, ngroups=ng, lp=s_lp, lp_per=s_lp / ng,
                              milp=s_milp, milp_per=s_milp / ng, half_int_gap=gap))
            print_fn(f"SYN  p={p:4d} k={k} seed={seed}: G8={ng:4d}  LP {s_lp/ng:.4f}/grp  "
                     f"MILP {s_milp/ng:.4f}/grp  (LP-MILP)/grp={(s_lp-s_milp)/ng:.4f}  LP-half-int-gap={gap:.3f}")
    return rows

def summarize_synthetic(rows, print_fn=print):
    agg = defaultdict(list)
    for r in rows: agg[(r['p'], r['k'])].append(r)
    for (p, k), rs in sorted(agg.items()):
        lp = np.array([r['lp_per'] for r in rs]); mi = np.array([r['milp_per'] for r in rs])
        print_fn(f"  base p={p:4d} k={k}: n_seeds={len(rs)}  LP/grp mean={lp.mean():.4f} "
                 f"[{lp.min():.4f},{lp.max():.4f}]   MILP/grp mean={mi.mean():.4f} [{mi.min():.4f},{mi.max():.4f}]   "
                 f"mean rounding gap (LP-MILP)/grp={ (lp-mi).mean():.4f}")

def main():
    quick = len(sys.argv) > 1 and sys.argv[1] == 'quick'
    seeds = range(3) if quick else range(8)

    print("=" * 100)
    print("PART 1/3 — real instances: MILP (t in {0,1/2,1}) vs free LP relaxation")
    print("=" * 100)
    real_rows = run_real()

    print()
    print("=" * 100)
    print("PART 2/3 — synthetic instances (random groups on same cycles), several seeds, two sizes")
    print("=" * 100)
    syn_rows = run_synthetic(seeds=seeds)
    print()
    print("synthetic summary:")
    summarize_synthetic(syn_rows)

    print()
    print("=" * 100)
    print("PART 3/3 — window statistics: MILP-selected vs unselected groups")
    print("=" * 100)
    for r in real_rows:
        window_report(r['M'], r['M']['groups'], r['t_milp'], f"REAL p={r['p']} k={r['k']}")
    for p, k in SYN_BASES:
        M = cm.build(p, k); Ms = cm.synthetic(M, 0)
        s, w, t, res = milp_solve(Ms)
        window_report(Ms, Ms['groups'], t, f"SYN  p={p} k={k} seed=0 (base cycles)")

if __name__ == "__main__":
    main()
