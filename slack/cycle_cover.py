"""cycle_cover.py — TASK 2 (exact cycle cover LP/DP), second solver's C1 picture (pair_bound_notes.md
sections 11, 12, 24, 25, 26): the class graph of P_k = H(1) union H(k) in the HJSW box is a disjoint union
of even cycles kappa_a -row- mu_{k a} -col- kappa_{k a} -row- mu_{k^2 a} -col- ... , one per coset of <k> in
F_p^* (a single cycle of length 2(p-1) when k is a primitive root).  Every (4,8,4) residue group g (an
8-point slope +-1 line, together with its two flanking 4-point lines) contributes 4 classes (two kappa, two
mu); giving weight u_g in {0, 1/2, 1} to g's three lines lowers the row/column "demand" of those 4 classes
from 1 to 1 - u_g, because all 4 copies of each of those classes already lie on one of the group's 3 lines
(pair_bound_notes.md sec. 11/24: "the 16 points of the group's 4 classes are exactly the points on its three
lines").  What is left is a 1-dimensional covering LP on the cycle(s): choose edge weights w_e >= 0 (one per
row-relation and one per column-relation) so every class vertex's (<=2) incident edges sum to >= its demand;
minimise the cost.  This file computes that cover exactly, two ways, and the free joint LP over u_g too.

Cost bookkeeping (calibrated against slack/chain_walk.py, which works at the level of actual box rows/columns
-- 2p-2 of each, nonzero -- rather than the p-1 + p-1 class-edges used here; each class-edge is realised by
TWO box lines that get equal weight at the optimum, by the row/column K_{2,2} symmetry of a class, so the
box-level cost 2*(box-line weight) doubles to 4*w_e per class-edge here):
    line_cost(g)      = 2 * 3 * u_g               (a line of weight u contributes 2u to the |S|-bound; 3 lines)
    rowcol_cost(edge)  = 4 * w_e
    total  = sum_g line_cost(g) + sum_e rowcol_cost(e)
    saving = 4(p-1) - total ;  net/group = saving / G8
Checked exactly (see __main__) against slack/chain_walk.py p=101 k=2, forced u=1/2 on all groups:
rows/cols LP 368.00 = 4(p-1) - 32.00, total cover 416.00 = 4(p-1) - (-16.00), net -1.000/group -- matches to
the last decimal.  (The module docstring in pair_bound_notes.md sec. 25 writes the row/col cost as "2 w_e";
that is the box-line-level statement, e.g. 2*(1/2) per box line -- see sec. 1's "4(p-1), rows and columns:
2p-2 each" -- collapsed here to one variable per class-edge, hence the factor of 4 rather than 2.)

Two independent solvers for the row/col part (cross-checked in __main__, and inside cover_value via
method='both'):
  (a) _rowcol_cost_lp  -- the literal LP, scipy.optimize.linprog, HiGHS.
  (b) _rowcol_cost_dp  -- linear-time DP around each cycle.  The cycles are bipartite (kappa/mu classes
      alternate), so the vertex-edge incidence matrix is totally unimodular; u_g in {0,1/2,1} makes every
      demand a multiple of 1/2, so a half-integer optimum exists and w_e can be searched over {0, 1/2, 1}
      only.  This is verified numerically against (a) below (random u patterns, several (p,k)) before
      cover_value relies on it by default.

cover_value_free(p, k): the joint LP over u_g in [0,1] (continuous, one scalar per group applied to all 3 of
its lines) and w_e >= 0 together -- section 25/26's "free LP".  Nets +0.75/group at p=101,k=2, +0.8125 (note:
"+0.81") at p=199,k=2, +0.8824 (note: "+0.88") at p=199,k=3 -- matches sec. 25/26 to the precision quoted there.

usage:
    python3 slack/cycle_cover.py            # run the validation block (prints the checks above)
    python3 slack/cycle_cover.py p k        # cover_value at u=1/2 everywhere, + the free LP, for one (p,k)
"""
import sys
import time

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix

sys.path.insert(0, 'slack')
try:
    from cycle_stats import specials as _specials_reference  # cross-check only (see __main__)
except ImportError:
    _specials_reference = None


# ---------------------------------------------------------------------------------------------------------
# Group and cycle construction (residue-group definitions of slack/g8_general.py, kept as full membership
# instead of just a count; class-graph cycles of slack/chain_walk.py, generalised to non-primitive k).
# ---------------------------------------------------------------------------------------------------------

def build_groups(p, k):
    """The (4,8,4) 'special' residue groups of P_k = H(1) union H(k), both slopes.

    A class is ('K', a) for kappa_a = (a, 1/a) in H(1), or ('M', b) for mu_b = (b, k/b) in H(k).  For slope
    +1, the H(1) pair at residue d is {a, -1/a} with a - 1/a = d, and the H(k) pair is {b, -k/b} with
    b - k/b = d; the pair is "shared" iff its two members' least residues X(.) have opposite signs.  For
    slope -1, the pairs are {a, 1/a} (a + 1/a = d) and {b, k/b} (b + k/b = d), shared iff same signs.  A
    residue d is a good (4,8,4) group iff both pairs exist (non-degenerate, a two-element pair) and are
    shared (pair_bound_notes.md sec. 24, "F2" lemma: both shared => the group's 3 lines have sizes (4,8,4)).

    Returns (groups, class_to_groups):
      groups           -- dict group_id -> frozenset of the group's 4 classes; group_id = (slope, d).
      class_to_groups  -- dict class -> list of group_ids it belongs to.  Empirically (checked in __main__
                           to p=997 across several k) this list always has length <= 1 -- a class is special
                           for at most one slope -- but cover_value sums u_g over the whole list, so a class
                           that did belong to two groups would still be handled correctly (demand
                           max(0, 1 - sum of its groups' u_g)).
    """
    h = (p - 1) // 2
    k %= p
    X = lambda u: (u % p) if (u % p) <= h else (u % p) - p
    inv = [0] * p
    for a in range(1, p):
        inv[a] = pow(a, -1, p)
    groups = {}
    for slope in (+1, -1):
        H1 = {}
        Hk = {}
        for a in range(1, p):
            for c, D in ((1, H1), (k, Hk)):
                ca = c * inv[a] % p
                key = (a - ca) % p if slope > 0 else (a + ca) % p
                D.setdefault(key, set()).add(frozenset({a, (-ca) % p if slope > 0 else ca}))
        for key in set(H1) & set(Hk):
            if len(H1[key]) != 1 or len(Hk[key]) != 1:
                continue  # more than one pair at this residue: not the generic (F2) case
            pr1 = next(iter(H1[key]))
            prk = next(iter(Hk[key]))
            if len(pr1) != 2 or len(prk) != 2:
                continue  # degenerate (sigma- or tau-fixed) class
            a = min(pr1)
            b = min(prk)
            s1 = (X(a) > 0) != (X(inv[a]) > 0)
            sk = (X(b) > 0) != (X(k * inv[b] % p) > 0)
            if slope < 0:
                s1 = not s1
                sk = not sk
            if s1 and sk:
                gid = (slope, key)
                classes = frozenset({('K', x) for x in pr1} | {('M', y) for y in prk})
                groups[gid] = classes
    class_to_groups = {}
    for gid, classes in groups.items():
        for c in classes:
            class_to_groups.setdefault(c, []).append(gid)
    return groups, class_to_groups


def build_cycles(p, k):
    """The class-graph cycles: kappa_a -row- mu_{k a} -col- kappa_{k a} -row- ... , one per coset of <k> in
    F_p^*.  Returns a list of cycles; each cycle is a list of classes in cyclic order, i.e. edge i of a cycle
    of length L is (seq[i], seq[(i+1) % L]), alternating row-edge (kappa->mu) and column-edge (mu->kappa)."""
    k %= p
    seen = set()
    cycles = []
    for a in range(1, p):
        if ('K', a) in seen:
            continue
        x = a
        seq = []
        while ('K', x) not in seen:
            seen.add(('K', x))
            seq.append(('K', x))
            seq.append(('M', k * x % p))
            x = k * x % p
        cycles.append(seq)
    return cycles


def _demand(v, class_to_groups, u):
    """demand(c) = max(0, 1 - sum of u_g over c's groups); u_g defaults to 0 for a group missing from u."""
    tot_u = sum(u.get(g, 0.0) for g in class_to_groups.get(v, ()))
    return max(0.0, 1.0 - tot_u)


def _cycle_edges(cycles):
    """Flatten cycles into (verts, edges): verts[i] is a class, edges is a list of (i1, i2) vertex-index pairs."""
    verts = []
    edges = []
    for seq in cycles:
        base = len(verts)
        verts.extend(seq)
        L = len(seq)
        for i in range(L):
            edges.append((base + i, base + (i + 1) % L))
    return verts, edges


# ---------------------------------------------------------------------------------------------------------
# Method (a): the exact LP.
# ---------------------------------------------------------------------------------------------------------

def _rowcol_cost_lp(cycles, class_to_groups, u):
    """Row/column cover cost via scipy.optimize.linprog (HiGHS), literal edge-weight LP."""
    verts, edges = _cycle_edges(cycles)
    n = len(verts)
    m = len(edges)
    if m == 0:
        return 0.0
    rows = []
    cols = []
    data = []
    for j, (i1, i2) in enumerate(edges):
        rows.append(i1); cols.append(j); data.append(1.0)
        rows.append(i2); cols.append(j); data.append(1.0)
    A = csr_matrix((data, (rows, cols)), shape=(n, m))
    b = np.array([_demand(v, class_to_groups, u) for v in verts])
    c = 4.0 * np.ones(m)
    res = linprog(c, A_ub=-A, b_ub=-b, bounds=[(0, None)] * m, method='highs')
    if not res.success:
        raise RuntimeError(f"rowcol LP failed: {res.message}")
    return float(res.fun)


# ---------------------------------------------------------------------------------------------------------
# Method (b): the O(#classes) DP.  Edge weights restricted to {0, 1/2, 1} -- exact whenever every demand is a
# multiple of 1/2 (true here: u_g in {0,1/2,1} => demand = max(0, 1 - sum u_g) is a multiple of 1/2), because
# the cycle graph is bipartite (its vertex-edge incidence matrix is totally unimodular) so a half-integer RHS
# LP has a half-integer optimum.  Verified against (a) in __main__ before cover_value relies on it.
# ---------------------------------------------------------------------------------------------------------

_STATES = (0.0, 0.5, 1.0)


def _dp_one_cycle(seq, class_to_groups, u):
    """Minimum sum of edge weights w_e in {0,1/2,1} around one cycle `seq`, s.t. for every vertex v = seq[i]
    the two incident edges w_{i-1} + w_i >= demand(v) (indices mod L).  Fixes w_0 = s0 (3 candidates), does a
    forward DP for w_1..w_{L-1}, then closes the cycle against w_0."""
    L = len(seq)
    d = [_demand(v, class_to_groups, u) for v in seq]
    best = None
    for s0 in _STATES:
        dp = {s0: s0}  # dp[w_i] = min cost of w_0..w_i consistent with w_0 = s0 and constraints at v_1..v_i
        for i in range(1, L):
            ndp = {}
            di = d[i]
            for s_prev, cost_prev in dp.items():
                for s in _STATES:
                    if s_prev + s + 1e-9 >= di:
                        nc = cost_prev + s
                        if s not in ndp or nc < ndp[s] - 1e-12:
                            ndp[s] = nc
            dp = ndp
        d0 = d[0]
        for s_last, cost_last in dp.items():
            if s_last + s0 + 1e-9 >= d0:
                if best is None or cost_last < best - 1e-12:
                    best = cost_last
    if best is None:
        raise RuntimeError("infeasible cycle DP (should not happen: demand <= 1 always)")
    return best


def _rowcol_cost_dp(cycles, class_to_groups, u):
    """Row/column cover cost via the per-cycle DP; sums sum(w_e) over all cycles and scales by 4 (see module
    docstring for the factor)."""
    return 4.0 * sum(_dp_one_cycle(seq, class_to_groups, u) for seq in cycles if len(seq) > 0)


# ---------------------------------------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------------------------------------

def cover_value(p, k, u, method='dp', check=False):
    """Exact minimum total cost of the class-cycle cover of P_k = H(1) union H(k), given per-group line
    weights u (dict group_id -> weight in {0, 0.5, 1}; a group absent from u defaults to u_g = 0).

    method: 'dp' (default, fast; see _rowcol_cost_dp), 'lp' (scipy HiGHS; see _rowcol_cost_lp), or 'both'
            (compute both and assert they agree to 1e-6, for validation).
    check:  if True, always compute both methods and assert agreement, regardless of `method` (the value used
            for the returned numbers is still the one named by `method`; 'both' implies check=True).

    Returns a dict: p, k, G8, groups, class_to_groups, u, line_cost, rowcol_cost, total, saving, net,
    and (if check) rowcol_cost_lp, rowcol_cost_dp.
    """
    groups, class_to_groups = build_groups(p, k)
    cycles = build_cycles(p, k)
    G8 = len(groups)
    line_cost = 6.0 * sum(u.get(g, 0.0) for g in groups)

    want_both = check or method == 'both'
    rc_dp = rc_lp = None
    if method in ('dp', 'both') or want_both:
        rc_dp = _rowcol_cost_dp(cycles, class_to_groups, u)
    if method in ('lp', 'both') or want_both:
        rc_lp = _rowcol_cost_lp(cycles, class_to_groups, u)
    if want_both:
        if abs(rc_dp - rc_lp) > 1e-6:
            raise AssertionError(f"DP/LP mismatch at p={p},k={k}: dp={rc_dp!r} lp={rc_lp!r}")

    rowcol_cost = rc_lp if method == 'lp' else rc_dp
    total = line_cost + rowcol_cost
    saving = 4 * (p - 1) - total
    net = saving / G8 if G8 else float('nan')

    out = dict(p=p, k=k, G8=G8, groups=groups, class_to_groups=class_to_groups, u=dict(u),
               line_cost=line_cost, rowcol_cost=rowcol_cost, total=total, saving=saving, net=net,
               method=method)
    if want_both:
        out['rowcol_cost_dp'] = rc_dp
        out['rowcol_cost_lp'] = rc_lp
    return out


def cover_value_free(p, k):
    """The joint LP: choose u_g in [0,1] for every group g and w_e >= 0 on every class-edge together, to
    minimise total cost = sum_g 6 u_g + sum_e 4 w_e, subject to every class's demand (1 - sum of its groups'
    u_g, or 1 if unspecial) being met by its (<=2) incident edges.  This is section 25/26's "free LP".

    Returns a dict: p, k, G8, total, saving, net, u_star (dict group_id -> optimal weight), runtime (seconds).
    """
    t0 = time.perf_counter()
    groups, class_to_groups = build_groups(p, k)
    cycles = build_cycles(p, k)
    verts, edges = _cycle_edges(cycles)
    n = len(verts)
    m = len(edges)
    gids = list(groups.keys())
    G8 = len(gids)
    gidx = {g: i for i, g in enumerate(gids)}

    rows = []
    cols = []
    data = []
    for j, (i1, i2) in enumerate(edges):
        rows.append(i1); cols.append(j); data.append(1.0)
        rows.append(i2); cols.append(j); data.append(1.0)
    for vi, v in enumerate(verts):
        for g in class_to_groups.get(v, ()):
            rows.append(vi); cols.append(m + gidx[g]); data.append(1.0)
    A = csr_matrix((data, (rows, cols)), shape=(n, m + G8))
    b = np.ones(n)
    c = np.concatenate([4.0 * np.ones(m), 6.0 * np.ones(G8)])
    bounds = [(0, None)] * m + [(0, 1)] * G8
    res = linprog(c, A_ub=-A, b_ub=-b, bounds=bounds, method='highs')
    if not res.success:
        raise RuntimeError(f"free LP failed: {res.message}")

    total = float(res.fun)
    saving = 4 * (p - 1) - total
    net = saving / G8 if G8 else float('nan')
    u_star = {g: float(res.x[m + gidx[g]]) for g in gids}
    runtime = time.perf_counter() - t0
    return dict(p=p, k=k, G8=G8, total=total, saving=saving, net=net, u_star=u_star, runtime=runtime)


# ---------------------------------------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------------------------------------

def _run_validation():
    import random
    random.seed(0)
    ok = True

    print("=== cycle_cover.py validation ===")

    # --- 1. forced u=1/2 on every group, p=101 k=2, vs. slack/chain_walk.py's printed numbers ---
    p, k = 101, 2
    t0 = time.perf_counter()
    groups, class_to_groups = build_groups(p, k)
    u = {g: 0.5 for g in groups}
    r = cover_value(p, k, u, method='both')
    dt = time.perf_counter() - t0
    print(f"\n[1] p={p} k={k}, u_g=1/2 on all G8={r['G8']} groups (chain_walk.py ground truth: "
          f"rows/cols LP 368, total 416, net -1.000/group):")
    print(f"    rows/cols cost = {r['rowcol_cost']:.2f}  (DP {r['rowcol_cost_dp']:.2f} == LP {r['rowcol_cost_lp']:.2f})")
    print(f"    line cost      = {r['line_cost']:.2f}")
    print(f"    total cover    = {r['total']:.2f}  = 4(p-1) - ({r['saving']:.2f})")
    print(f"    saving = {r['saving']:.2f}, net/group = {r['net']:.4f}")
    print(f"    [{dt*1000:.1f} ms]")
    exp_rc, exp_total, exp_net = 368.0, 416.0, -1.0
    c1 = abs(r['rowcol_cost'] - exp_rc) < 1e-6
    c2 = abs(r['total'] - exp_total) < 1e-6
    c3 = abs(r['net'] - exp_net) < 1e-6
    print(f"    check: rows/cols==368 {c1}, total==416 {c2}, net==-1.000 {c3}")
    ok &= c1 and c2 and c3

    # --- 2. baseline (u=0 everywhere, or no groups given) reproduces the trivial bound 4(p-1) ---
    r0 = cover_value(p, k, {}, method='both')
    c0 = abs(r0['total'] - 4 * (p - 1)) < 1e-6
    print(f"\n[2] p={p} k={k}, u={{}} (baseline): total = {r0['total']:.2f} == 4(p-1) = {4*(p-1)}: {c0}")
    ok &= c0

    # --- 3. cross-check the group construction against slack/cycle_stats.py's specials() ---
    if _specials_reference is not None:
        S_ref = _specials_reference(p, k)
        S_mine = set(class_to_groups.keys())
        c4 = (S_ref == S_mine)
        print(f"\n[3] classes marked special: build_groups={len(S_mine)} vs cycle_stats.specials()="
              f"{len(S_ref)}: identical set = {c4}")
        ok &= c4
    else:
        print("\n[3] slack/cycle_stats.py not importable -- skipped the specials() cross-check")

    # --- 4. DP vs LP agreement on random u patterns, several (p,k) (verifying the {0,1/2,1} claim) ---
    print("\n[4] DP vs LP on random u_g patterns (method='both', asserts agreement internally):")
    all_match = True
    for (pp, kk) in [(29, 2), (29, 3), (53, 2), (101, 2), (101, 3), (199, 2), (199, 3)]:
        gg, _ = build_groups(pp, kk)
        gids = list(gg.keys())
        for trial in range(3):
            uu = {g: random.choice([0.0, 0.5, 1.0]) for g in gids}
            try:
                rr = cover_value(pp, kk, uu, method='both')
                match = True
            except AssertionError as e:
                match = False
                print(f"    MISMATCH {pp},{kk},trial{trial}: {e}")
            all_match &= match
        print(f"    p={pp:4d} k={kk}: G8={len(gids):3d}  3 random trials matched: {all_match}")
    print(f"    all DP==LP: {all_match}")
    ok &= all_match

    # --- 5. overlap check (does a class ever belong to >1 group?) ---
    print("\n[5] class_to_groups overlap check (class special for >1 group):")
    for (pp, kk) in [(101, 2), (199, 2), (199, 3), (401, 2), (401, 3), (997, 2)]:
        gg, ctg = build_groups(pp, kk)
        overl = sum(1 for lst in ctg.values() if len(lst) > 1)
        print(f"    p={pp:4d} k={kk}: G8={len(gg):4d}  classes_marked={len(ctg):5d} (4*G8={4*len(gg):5d})  "
              f"overlapping_classes={overl}")

    # --- 6. free LP: net per group vs. sec. 25/26's numbers ---
    print("\n[6] cover_value_free (joint LP over u_g in [0,1] and w_e >= 0):")
    targets = {(101, 2): 0.75, (199, 2): 0.81, (199, 3): 0.88}
    free_results = {}
    for (pp, kk), tgt in targets.items():
        rf = cover_value_free(pp, kk)
        free_results[(pp, kk)] = rf
        c5 = abs(rf['net'] - tgt) < 0.01
        print(f"    p={pp:4d} k={kk}: G8={rf['G8']:3d}  total={rf['total']:.3f}  saving={rf['saving']:.3f}  "
              f"net={rf['net']:.4f}  (notes: +{tgt})  match(<=0.01): {c5}  [{rf['runtime']*1000:.1f} ms]")
        ok &= c5

    print(f"\n=== overall: {'PASS' if ok else 'FAIL'} ===")

    # --- 7. runtime for p=199 (both k=2 and k=3), reported separately as requested ---
    print("\n[7] runtime at p=199 (fresh timings, method='both' for cover_value so both solvers run):")
    for kk in (2, 3):
        t0 = time.perf_counter()
        gg, _ = build_groups(199, kk)
        u = {g: 0.5 for g in gg}
        r = cover_value(199, kk, u, method='both')
        dt_cover = time.perf_counter() - t0
        t0 = time.perf_counter()
        rf = cover_value_free(199, kk)
        dt_free = t0  # placeholder, overwritten below
        dt_free = time.perf_counter() - t0
        print(f"    p=199 k={kk}: cover_value(u=1/2,both)  {dt_cover*1000:6.1f} ms   "
              f"cover_value_free  {dt_free*1000:6.1f} ms   (rf.runtime={rf['runtime']*1000:.1f} ms)")

    return ok


if __name__ == "__main__":
    if len(sys.argv) >= 3:
        p = int(sys.argv[1])
        k = int(sys.argv[2])
        groups, _ = build_groups(p, k)
        u = {g: 0.5 for g in groups}
        r = cover_value(p, k, u, method='both')
        print(f"p={p} k={k}: G8={r['G8']}  u=1/2 on all groups:")
        print(f"  rows/cols cost = {r['rowcol_cost']:.3f} (DP {r['rowcol_cost_dp']:.3f}, LP {r['rowcol_cost_lp']:.3f})")
        print(f"  line cost      = {r['line_cost']:.3f}")
        print(f"  total cover    = {r['total']:.3f} = 4(p-1) - {r['saving']:.3f}")
        print(f"  net/group      = {r['net']:.4f}")
        rf = cover_value_free(p, k)
        print(f"free LP: total={rf['total']:.3f} saving={rf['saving']:.3f} net/group={rf['net']:.4f} "
              f"[{rf['runtime']*1000:.1f} ms]")
    else:
        success = _run_validation()
        sys.exit(0 if success else 1)
