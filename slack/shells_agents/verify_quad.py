"""verify_quad.py -- VERIFIER task (1): independently re-derive alpha for the quadruple
H(1) u H(-1) u H(2) u H(-2) at p=11,13 via exact CP-SAT (<=300s), and certify the returned
set by an independent O(n^3) brute-force triple-collinearity scan (exact integer cross
products; does not reuse the CP-SAT solver's own line list construction -- it re-derives
lines with its own code path, and ALSO does the raw O(n^3) triple check for full hygiene).

usage: python3 verify_quad.py [p ...]   (default 11 13)
"""
import sys, itertools, math, time
from ortools.sat.python import cp_model

def hyper_points(p, cs):
    h = (p - 1) // 2; x0, y0 = -h, 0
    P = set()
    for c in cs:
        for x in range(1, p):
            y = c * pow(x, -1, p) % p
            bx = x0 + ((x - x0) % p); by = y0 + ((y - y0) % p)
            for r in (0, 1):
                for s in (0, 1): P.add((bx + r * p, by + s * p))
    return sorted(P)

def build_lines(pts):
    # independent re-implementation (own variable names, own loop structure)
    from collections import defaultdict
    n = len(pts)
    groups = defaultdict(list)
    for i in range(n):
        xi, yi = pts[i]
        for j in range(i + 1, n):
            xj, yj = pts[j]
            ddx, ddy = xj - xi, yj - yi
            g = math.gcd(abs(ddx), abs(ddy))
            ddx //= g; ddy //= g
            if ddx < 0 or (ddx == 0 and ddy < 0):
                ddx, ddy = -ddx, -ddy
            key = (ddx, ddy, ddy * xi - ddx * yi)
            groups[key].append(i); groups[key].append(j)
    out = []
    for key, members in groups.items():
        s = sorted(set(members))
        if len(s) >= 3:
            out.append(s)
    return out

def brute_certify(points):
    """RAW O(n^3) triple scan over ALL C(n,3) triples -- the mandated hygiene check,
    independent of any 'lines' data structure."""
    n = len(points)
    checked = 0
    for i, j, k in itertools.combinations(range(n), 3):
        x1, y1 = points[i]; x2, y2 = points[j]; x3, y3 = points[k]
        cross = (x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1)
        checked += 1
        if cross == 0:
            return False, checked, (points[i], points[j], points[k])
    return True, checked, None

def solve(p, cs, T):
    pts = hyper_points(p, cs)
    lines = build_lines(pts)
    m = cp_model.CpModel()
    x = [m.NewBoolVar(f'x{i}') for i in range(len(pts))]
    for s in lines:
        m.Add(sum(x[i] for i in s) <= 2)
    m.Maximize(sum(x))
    sol = cp_model.CpSolver()
    sol.parameters.max_time_in_seconds = T
    sol.parameters.num_search_workers = 8
    st = sol.Solve(m)
    idx = [i for i in range(len(pts)) if sol.Value(x[i])]
    chosen = [pts[i] for i in idx]
    return chosen, sol.StatusName(st), sol.BestObjectiveBound(), len(pts), len(lines)

if __name__ == '__main__':
    ps = [int(a) for a in sys.argv[1:]] or [11, 13]
    T = 300.0
    LOG = '/home/pmbot/projects/saturation_peer/slack/verification/verify_quad_indep.txt'
    with open(LOG, 'a') as log:
        def out(s):
            print(s, flush=True)
            print(s, file=log, flush=True)
        out(f"\n=== verify_quad.py independent re-derivation, {time.ctime()} ===")
        for p in ps:
            cs = (1 % p, (p - 1) % p, 2 % p, (p - 2) % p)
            t0 = time.time()
            chosen, status, bound, npts, nlines = solve(p, cs, T)
            el = time.time() - t0
            ok, checked, bad = brute_certify(chosen)
            N = 2 * p
            out(f"p={p}: |points|={npts} lines(>=3)={nlines} CP-SAT status={status} "
                f"bound={bound:.0f} time={el:.1f}s -> alpha={len(chosen)} "
                f"= {len(chosen)/(p-1):.4f}(p-1) = {len(chosen)/N:.4f}N")
            out(f"  CERTIFY (raw O(n^3) triple scan, {checked} triples checked, exact int cross-product): "
                f"{'PASS' if ok else 'FAIL'}" + ("" if ok else f"  bad triple={bad}"))
            if status == 'OPTIMAL':
                out(f"  ==> PROVED OPTIMAL: true alpha({p}, quad{{1,-1,2,-2}}) = {len(chosen)}")
