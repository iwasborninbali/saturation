"""lp_curve.py — fractional line-cover LP for the box lift of a plane curve mod p (Conjecture G numerics).
Points: {(x,y) in [x0,x0+2p) x [y0,y0+2p): (x mod p, y mod p) on the curve}.  LP: min Σ_ℓ 2 w_ℓ + Σ_P z_P  s.t. Σ_{ℓ∋P} w_ℓ + z_P ≥ 1
(a lawful set meets each line in ≤ 2 points, so |S| ≤ value).  Modes: 'all' = all lines with ≥ 3 points; 'pm1' = only slopes 0, ∞, ±1.
usage: lp_curve.py p curve [x0 y0]   curve ∈ {hyp, cube, poly:a3,a2,a1,a0, pow:k}"""
import sys, math
from fractions import Fraction
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import lil_matrix

def curve_points(p, curve, x0, y0):
    pts = []
    def lifts(u, lo):
        v = lo + ((u - lo) % p)          # smallest lift >= lo
        return [v, v + p]                # exactly two lifts in [lo, lo+2p)
    for x in range(p):
        ys = []
        if curve == 'hyp':
            if x == 0: continue
            ys = [pow(x, -1, p)]
        elif curve == 'cube': ys = [x * x * x % p]
        elif curve.startswith('pow:'): ys = [pow(x, int(curve[4:]), p)]
        elif curve.startswith('poly:'):
            c = [int(t) for t in curve[5:].split(',')]
            v = 0
            for a in c: v = (v * x + a) % p
            ys = [v]
        for y in ys:
            for X in lifts(x, x0):
                for Y in lifts(y, y0):
                    pts.append((X, Y))
    return sorted(set(pts))

def lines(pts, mode):
    idx = {P: i for i, P in enumerate(pts)}; n = len(pts)
    L = {}
    for i in range(n):
        x1, y1 = pts[i]
        for j in range(i + 1, n):
            x2, y2 = pts[j]
            dx, dy = x2 - x1, y2 - y1
            if mode == 'pm1' and not (dx == 0 or dy == 0 or abs(dx) == abs(dy)): continue
            g = math.gcd(abs(dx), abs(dy)); dx //= g; dy //= g
            if dx < 0 or (dx == 0 and dy < 0): dx, dy = -dx, -dy
            c = dy * x1 - dx * y1
            L.setdefault((dx, dy, c), set()).update((i, j))
    return [sorted(s) for s in L.values() if len(s) >= 3]

def solve(pts, ls):
    n = len(pts); m = len(ls)
    A = lil_matrix((n, m + n))
    for k, s in enumerate(ls):
        for i in s: A[i, k] = 1
    for i in range(n): A[i, m + i] = 1
    c = np.concatenate([2 * np.ones(m), np.ones(n)])
    res = linprog(c, A_ub=-A.tocsr(), b_ub=-np.ones(n), bounds=(0, None), method='highs')
    return res.fun

if __name__ == '__main__':
    p = int(sys.argv[1]); curve = sys.argv[2]
    x0 = int(sys.argv[3]) if len(sys.argv) > 3 else 0; y0 = int(sys.argv[4]) if len(sys.argv) > 4 else 0
    pts = curve_points(p, curve, x0, y0)
    out = [f"p={p} {curve} box=({x0},{y0}) N=2p={2*p} pts={len(pts)}"]
    for mode in ('pm1', 'all'):
        ls = lines(pts, mode)
        sizes = {}
        for s in ls: sizes[len(s)] = sizes.get(len(s), 0) + 1
        v = solve(pts, ls)
        out.append(f"  {mode}: lines>=3: {len(ls)} sizes={dict(sorted(sizes.items()))} LP={v:.2f} = {v/(2*p):.3f} N = {v/p:.3f} p")
    print("\n".join(out), flush=True)
