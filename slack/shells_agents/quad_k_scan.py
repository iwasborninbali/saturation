"""quad_k_scan.py -- TASK A: scan every k in {2,...,(p-1)/2} for the quadruple
H(1) u H(-1) u H(k) u H(-k), p in {11,13,17,19,23,29,31}.

For each (p,k): several simulated-annealing (null_search.anneal) restarts give a
CERTIFIED lower bound on alpha(H(1) u H(-1) u H(k) u H(-k)) (certification = an
independent brute-force triple-collinearity check on the returned point set,
done in this file, NOT reusing the SA's internal line/counter bookkeeping).
For the best k of each p (and only there, budget reasons) we also attempt an
exact CP-SAT solve (ortools) with a generous time limit, reusing the exact
covering-model construction of quad_hyperbolas.py.

We also record whether k is a quadratic residue mod p (Legendre symbol) to test
empirically the conjecture that only the coset of k modulo squares/inverses
matters (stated in the task): since squares*QR=QR and 1/QR=QR (QR is a
subgroup), this reduces to testing whether alpha(k) depends only on the QR/QNR
class of k.

usage: quad_k_scan.py [p1 p2 ...]   (default: 11 13 17 19 23 29 31)
"""
import sys, time, itertools, math
sys.path.insert(0, '/home/pmbot/projects/saturation_peer/slack')
from diffusion_sampler import hyper_points, build_lines
from null_search import anneal

PS = [11, 13, 17, 19, 23, 29, 31]
if len(sys.argv) > 1:
    PS = [int(a) for a in sys.argv[1:]]

SCREEN_SECONDS = 12.0
SCREEN_SEEDS = 2
REFINE_SECONDS = 40.0
REFINE_SEEDS = 3
CPSAT_TIME = 300.0
CPSAT_MAX_P = 19   # only attempt exact CP-SAT for p <= this (time budget reasons)


def legendre(k, p):
    r = pow(k, (p - 1) // 2, p)
    return 'QR' if r == 1 else 'QNR'


def certify_lawful(pts_full, idx):
    """Independent brute-force check: no 3 of the chosen points are collinear
    (any slope). O(m^3) exact cross-product test, m = |idx| (<=~120, fine)."""
    S = [pts_full[i] for i in idx]
    m = len(S)
    assert m == len(set(S)), "duplicate points in claimed lawful set"
    for a in range(m):
        xa, ya = S[a]
        for b in range(a + 1, m):
            xb, yb = S[b]
            dx, dy = xb - xa, yb - ya
            for c in range(b + 1, m):
                xc, yc = S[c]
                # collinear iff cross product of (b-a) and (c-a) is zero
                if dx * (yc - ya) - dy * (xc - xa) == 0:
                    return False, (a, b, c)
    return True, None


def best_anneal(pts, lines, seeds, seconds, seed0=0):
    best = -1; bestS = None
    for s in range(seeds):
        v, S = anneal(pts, lines, seconds=seconds, seed=seed0 + s)
        if v > best:
            best, bestS = v, S
    return best, bestS


def cpsat_exact(pts, T):
    try:
        from ortools.sat.python import cp_model
    except Exception as e:
        return None, f"ortools unavailable: {e}"
    from lp_curve import lines as alllines
    U = sorted(set(pts))
    L = alllines(U, 'all')
    m = cp_model.CpModel()
    x = [m.NewBoolVar(f'x{i}') for i in range(len(U))]
    for s in L:
        m.Add(sum(x[i] for i in s) <= 2)
    m.Maximize(sum(x))
    sol = cp_model.CpSolver()
    sol.parameters.max_time_in_seconds = T
    sol.parameters.num_search_workers = 6
    st = sol.Solve(m)
    status = sol.StatusName(st)
    is_optimal = (st == cp_model.OPTIMAL)
    val = int(sol.ObjectiveValue()) if st in (cp_model.OPTIMAL, cp_model.FEASIBLE) else None
    bound = sol.BestObjectiveBound()
    idx = None
    if val is not None:
        idx = [i for i in range(len(U)) if sol.Value(x[i])]
    return (U, val, bound, status, idx, is_optimal), None


def main():
    log = []
    def out(s):
        print(s, flush=True); log.append(s)

    t_start = time.time()
    out(f"# quad_k_scan.py  PS={PS}  screen={SCREEN_SEEDS}x{SCREEN_SECONDS}s  refine={REFINE_SEEDS}x{REFINE_SECONDS}s  cpsat<={CPSAT_TIME}s")

    rows = []       # (p,k,cls,best_lb, certified, exact?, status)
    per_p_best = {}

    for p in PS:
        N = 2 * p
        ks = list(range(2, (p - 1) // 2 + 1))
        out(f"\n== p={p}  N={N}  (p-1)={p-1}  k-range {ks} ==")
        screen = {}
        for k in ks:
            cs = (1, p - 1, k % p, (p - k) % p)
            pts = hyper_points(p, cs)
            lines = build_lines(pts)
            lb, S = best_anneal(pts, lines, SCREEN_SEEDS, SCREEN_SECONDS)
            ok, bad = certify_lawful(pts, S)
            cls = legendre(k, p)
            screen[k] = (lb, ok, pts, lines)
            status = "CERTIFIED-lawful" if ok else f"FAILED cert at {bad}"
            out(f"  screen p={p} k={k:3d} [{cls}]: lb={lb:3d} = {lb/(p-1):.3f}(p-1) = {lb/N:.3f}N  {status}")
            if not ok:
                raise RuntimeError(f"certification failed for p={p} k={k}: triple {bad} is collinear")

        # refine the top-2 screening k's with a longer anneal budget
        order = sorted(ks, key=lambda k: -screen[k][0])
        top = order[:2]
        out(f"  -- refining top candidates {top} for p={p} with {REFINE_SEEDS}x{REFINE_SECONDS}s --")
        refined = {}
        for k in top:
            _, _, pts, lines = screen[k]
            lb, S = best_anneal(pts, lines, REFINE_SEEDS, REFINE_SECONDS, seed0=100)
            lb = max(lb, screen[k][0])
            if S is None:
                S = []  # keep prior certified bound if refine found nothing better
            ok, bad = certify_lawful(pts, S) if S else (True, None)
            if not ok:
                raise RuntimeError(f"certification failed on refine p={p} k={k}: triple {bad}")
            refined[k] = max(lb, screen[k][0])
            out(f"  refine p={p} k={k:3d} [{legendre(k,p)}]: lb={refined[k]:3d} = {refined[k]/(p-1):.3f}(p-1) = {refined[k]/N:.3f}N  CERTIFIED-lawful")

        best_k = max(refined, key=lambda k: refined[k])
        best_lb = refined[best_k]

        # exact CP-SAT attempt for the single best k of this p (only for small p: time budget)
        cs = (1, p - 1, best_k % p, (p - best_k) % p)
        pts = hyper_points(p, cs)
        exact_val = None; exact_status = "not attempted"
        cpsat_feasible_val = None
        if p > CPSAT_MAX_P:
            out(f"  CP-SAT p={p} k={best_k}: SKIPPED (p > {CPSAT_MAX_P}, time budget) -- using SA lower bound only")
            err = "skipped"
        else:
            res, err = cpsat_exact(pts, CPSAT_TIME)
        if err:
            pass
        else:
            U, val, bound, status, idx, is_optimal = res
            exact_status = f"{status} (bound {bound:.0f})"
            if val is not None:
                ok, bad = certify_lawful(U, idx)
                if not ok:
                    raise RuntimeError(f"CP-SAT solution failed certification p={p} k={best_k}: {bad}")
                cpsat_feasible_val = val
                if is_optimal:
                    exact_val = val
                    out(f"  CP-SAT p={p} k={best_k}: EXACT (OPTIMAL) alpha={val}  [{status}, bound {bound:.0f}]  CERTIFIED-lawful  ({CPSAT_TIME:.0f}s budget)")
                else:
                    out(f"  CP-SAT p={p} k={best_k}: NOT PROVEN OPTIMAL within {CPSAT_TIME:.0f}s -- feasible lawful set of size {val} (LB, not exact)  [{status}, bound {bound:.0f}]  CERTIFIED-lawful")
            else:
                out(f"  CP-SAT p={p} k={best_k}: no feasible solution within {CPSAT_TIME:.0f}s  [{status}, bound {bound:.0f}]")

        final_val = exact_val if exact_val is not None else max(best_lb, cpsat_feasible_val or 0)
        is_exact = exact_val is not None
        per_p_best[p] = (best_k, final_val, is_exact, N)
        for k in ks:
            lb = refined[k] if k in refined else screen[k][0]
            ex = is_exact if k == best_k else False
            val = final_val if (k == best_k) else lb
            rows.append((p, k, legendre(k, p), val, ex))

        out(f"  ==> p={p}: best k={best_k}  alpha {'(EXACT)' if is_exact else '(LB)'} = {final_val} = {final_val/(p-1):.3f}(p-1) = {final_val/N:.3f}N")

    # ---- summary table ----
    out("\n\n===== TABLE: p, k, QR-class(k), best alpha for {H(1),H(-1),H(k),H(-k)}, alpha/N, alpha/(p-1), exact/LB =====")
    for p, k, cls, val, ex in rows:
        N = 2 * p
        out(f"  p={p:3d} k={k:3d} [{cls}] alpha={val:3d}  alpha/N={val/N:.4f}  alpha/(p-1)={val/(p-1):.4f}  {'EXACT' if ex else 'LB'}")

    # ---- QR/QNR correlation check ----
    out("\n===== QR-class correlation (does alpha(k) depend only on QR/QNR of k, at fixed p?) =====")
    for p in PS:
        qr_vals = [val for (pp, k, cls, val, ex) in rows if pp == p and cls == 'QR']
        qnr_vals = [val for (pp, k, cls, val, ex) in rows if pp == p and cls == 'QNR']
        out(f"  p={p}: QR alphas={qr_vals}  QNR alphas={qnr_vals}")

    # ---- trend across p for the best k of each p ----
    out("\n===== TREND: best-k alpha vs p =====")
    xs = []; ys = []
    for p in PS:
        k, val, ex, N = per_p_best[p]
        out(f"  p={p:3d}  best_k={k:3d}  alpha={val:3d} ({'EXACT' if ex else 'LB'})  alpha/N={val/N:.4f}  alpha/(p-1)={val/(p-1):.4f}")
        xs.append(p - 1); ys.append(val)

    # least squares fit alpha ~ c*(p-1) + d
    n = len(xs)
    sx = sum(xs); sy = sum(ys); sxx = sum(x*x for x in xs); sxy = sum(x*y for x, y in zip(xs, ys))
    c = (n * sxy - sx * sy) / (n * sxx - sx * sx)
    d = (sy - c * sx) / n
    out(f"\nLeast-squares fit over best-k points: alpha ~ {c:.4f} * (p-1) + {d:.3f}")
    resid = [y - (c*x+d) for x, y in zip(xs, ys)]
    out(f"  residuals: {[round(r,2) for r in resid]}")

    ratios = [per_p_best[p][1] / (2*p) for p in PS]
    out(f"\nalpha/N sequence over p={PS}: {[round(r,4) for r in ratios]}")
    if len(ratios) >= 2:
        trend = "DECREASING" if ratios[-1] < ratios[0] else ("INCREASING" if ratios[-1] > ratios[0] else "FLAT")
        out(f"Trend from p={PS[0]} to p={PS[-1]}: alpha/N is {trend} (from {ratios[0]:.4f} to {ratios[-1]:.4f}); 1.5 threshold {'crossed downward' if ratios[-1] <= 1.5 <= ratios[0] else 'not crossed'}")

    out(f"\ntotal wall time: {time.time()-t_start:.0f}s")

    with open('/home/pmbot/projects/saturation_peer/slack/verification/shells_quad_k.txt', 'w') as f:
        f.write("\n".join(log) + "\n")


if __name__ == '__main__':
    main()
