"""orbit_union.py — the LOCAL question behind H4': for a V-orbit O of H(1) (16 points, max lawful 12) and its R-image R(O) subset H(-1),
what is the maximum lawful subset of O ∪ R(O) (32 points)?  If it is 12 + c with small c, summing over the (p-1)/4 orbits gives
alpha(P_{-1}) <= 3(p-1) + c(p-1)/4 — so c decides whether a local route to 3(p-1)+O(1) exists at all.
NOTE: O ∪ R(O) is closed under rows (kappa ∪ R kappa) but NOT under columns/±1 lines, so this is only a heuristic decomposition;
we compute it with ALL lines inside the union.  usage: orbit_union.py p [p ...]"""
import sys
from collections import defaultdict
from itertools import combinations
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
sys.path.insert(0, 'slack')
from lp_curve import lines as alllines

def run(p):
    h = (p - 1) // 2; x0, y0 = -h, 0
    orb = {}
    for a in range(1, p):
        ia = pow(a, -1, p); orb[a] = frozenset({a, ia, (p - a) % p, (p - ia) % p})
    seen = set(); res = []
    for a in range(1, p):
        O = orb[a]
        if O in seen: continue
        seen.add(O)
        pts1 = []
        for b in O:
            ib = pow(b, -1, p)
            bx = x0 + ((b - x0) % p); by = y0 + ((ib - y0) % p)
            pts1 += [(bx + r * p, by + s * p) for r in (0, 1) for s in (0, 1)]
        pts1 = sorted(set(pts1))
        ptsm = sorted({(p - x, y) for (x, y) in pts1})
        def maxlawful(U):
            U = sorted(set(U)); idx = {q: i for i, q in enumerate(U)}
            L = alllines(U, 'all')
            if not L: return len(U)
            A = np.zeros((len(L), len(U)))
            for i, m in enumerate(L):
                for j in m: A[i, j] = 1
            r = milp(c=-np.ones(len(U)), constraints=LinearConstraint(A, -np.inf, 2), bounds=Bounds(0, 1), integrality=np.ones(len(U)))
            return round(-r.fun)
        m1 = maxlawful(pts1); mu = maxlawful(pts1 + ptsm)
        res.append((len(O), len(pts1), m1, len(pts1) + len(ptsm), mu))
    from collections import Counter
    c = Counter((r[1], r[2], r[4]) for r in res)
    tot = sum(r[4] for r in res); tot1 = sum(r[2] for r in res)
    print(f"p={p}: orbits {len(res)}; (|O| pts, max in O, max in O∪R(O)) -> count: {dict(c)}; "
          f"sum over orbits: H(1) alone {tot1} (=3(p-1)={3*(p-1)}), unions {tot} = {tot/(p-1):.3f}(p-1)", flush=True)

for p in map(int, sys.argv[1:]): run(p)
