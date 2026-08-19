"""no3_3d.py — exact maximum subset of [n]^3 with no three collinear points (3D analogue of the no-three-in-line problem).
C1 (decisive computation): exact values for n = 2..7(8) with certificates.  C4: a witness is verified by brute force over all triples.
C2: the timing curve of the exact solve is the cost estimate for the next n.
usage: no3_3d.py n [seconds]"""
import sys, time, itertools
from collections import defaultdict
from math import gcd
from ortools.sat.python import cp_model

def lines(n):
    pts = [(x, y, z) for x in range(n) for y in range(n) for z in range(n)]
    idx = {p: i for i, p in enumerate(pts)}
    L = defaultdict(set)
    for a in range(len(pts)):
        for b in range(a + 1, len(pts)):
            p, q = pts[a], pts[b]
            d = (q[0]-p[0], q[1]-p[1], q[2]-p[2])
            g = gcd(gcd(abs(d[0]), abs(d[1])), abs(d[2]))
            d = (d[0]//g, d[1]//g, d[2]//g)
            if d < (0,0,0) if False else (d[0] < 0 or (d[0] == 0 and (d[1] < 0 or (d[1] == 0 and d[2] < 0)))):
                d = (-d[0], -d[1], -d[2])
            # canonical base: walk back along -d while inside the box
            base = p
            while True:
                nb = (base[0]-d[0], base[1]-d[1], base[2]-d[2])
                if all(0 <= c < n for c in nb): base = nb
                else: break
            L[(base, d)] |= {a, b}
    return pts, idx, [sorted(s) for s in L.values() if len(s) >= 3]

def certify(pts_sel):
    """brute force: no three of the selected points collinear (exact integer cross product)"""
    m = len(pts_sel)
    for i in range(m):
        for j in range(i+1, m):
            for k in range(j+1, m):
                a, b, c = pts_sel[i], pts_sel[j], pts_sel[k]
                u = (b[0]-a[0], b[1]-a[1], b[2]-a[2]); v = (c[0]-a[0], c[1]-a[1], c[2]-a[2])
                cr = (u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0])
                if cr == (0,0,0): return (a,b,c)
    return None

if __name__ == '__main__':
    n = int(sys.argv[1]); T = float(sys.argv[2]) if len(sys.argv) > 2 else 300
    t0 = time.time(); pts, idx, L = lines(n); tbuild = time.time() - t0
    m = cp_model.CpModel(); x = [m.NewBoolVar(f'x{i}') for i in range(len(pts))]
    for s in L: m.Add(sum(x[i] for i in s) <= 2)
    m.Maximize(sum(x))
    sol = cp_model.CpSolver(); sol.parameters.max_time_in_seconds = T; sol.parameters.num_search_workers = 6
    t1 = time.time(); st = sol.Solve(m); tsolve = time.time() - t1
    sel = [pts[i] for i in range(len(pts)) if sol.Value(x[i])]
    bad = certify(sel)
    print(f"n={n}: points={len(pts)} lines(>=3)={len(L)} [build {tbuild:.1f}s] status={sol.StatusName(st)} "
          f"alpha={len(sel)} bound={sol.BestObjectiveBound():.0f} [solve {tsolve:.1f}s] certified={'OK' if bad is None else 'FAIL '+str(bad)}"
          f"  alpha/n^2={len(sel)/n**2:.3f}", flush=True)
