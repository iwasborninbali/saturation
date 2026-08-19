"""orbit_pairs.py — PAIRWISE certificate: for two V-orbits O_i, O_j of H(1) let U_i = O_i ∪ R(O_i) (32 points, locally max 16).
If for every pair max lawful in U_i ∪ U_j <= c, then averaging over all pairs gives alpha(P_{-1}) <= (m/2)c with m = #orbit unions,
i.e. alpha <= c(p-1)/8 for generic orbits.  c = 32 is trivial (4(p-1)); c = 24 would give exactly 3(p-1).
usage: orbit_pairs.py p [p ...]"""
import sys
from itertools import combinations
from collections import defaultdict
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
sys.path.insert(0, 'slack')
from lp_curve import lines as alllines

def unions(p):
    h = (p - 1) // 2; x0, y0 = -h, 0
    orb = {}
    for a in range(1, p):
        ia = pow(a, -1, p); orb[a] = frozenset({a, ia, (p - a) % p, (p - ia) % p})
    seen = set(); out = []
    for a in range(1, p):
        O = orb[a]
        if O in seen: continue
        seen.add(O)
        pts = []
        for b in O:
            ib = pow(b, -1, p); bx = x0 + ((b - x0) % p); by = y0 + ((ib - y0) % p)
            pts += [(bx + r * p, by + s * p) for r in (0, 1) for s in (0, 1)]
        pts = sorted(set(pts))
        U = sorted(set(pts) | {(p - x, y) for (x, y) in pts})
        out.append((len(O), U))
    return out

def maxlawful(U):
    U = sorted(set(U)); idx = {q: i for i, q in enumerate(U)}
    L = alllines(U, 'all')
    if not L: return len(U)
    A = np.zeros((len(L), len(U)))
    for i, m in enumerate(L):
        for j in m: A[i, j] = 1
    r = milp(c=-np.ones(len(U)), constraints=LinearConstraint(A, -np.inf, 2), bounds=Bounds(0, 1), integrality=np.ones(len(U)))
    return round(-r.fun)

for p in map(int, sys.argv[1:]):
    Us = unions(p)
    singles = [maxlawful(U) for _, U in Us]
    pair = {}
    for (i, j) in combinations(range(len(Us)), 2):
        v = maxlawful(Us[i][1] + Us[j][1]); pair[(i, j)] = v - (singles[i] + singles[j])
    worst = max(pair.values()); best = min(pair.values())
    m = len(Us)
    # averaging bound: sum_i |S_i| <= (1/(m-1)) sum_{pairs} (|S_i|+|S_j|) <= (1/(m-1)) * C(m,2) * max_pair
    maxpair = max(maxlawful(Us[i][1] + Us[j][1]) for (i, j) in combinations(range(m), 2)) if m > 1 else 0
    bound = m * maxpair / 2
    print(f"p={p}: orbit unions {m} (sizes {sorted(len(U) for _, U in Us)}), singles {sorted(singles)}; "
          f"max over pairs of (max lawful in U_i ∪ U_j) = {maxpair} (sum of singles would be {max(singles[i]+singles[j] for i,j in combinations(range(m),2))}); "
          f"pair defect: min {best}, max {worst}; averaging bound: alpha <= {bound:.1f} = {bound/(p-1):.3f}(p-1)", flush=True)
