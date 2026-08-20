"""profile_test.py — есть ли в [n]^3 конфигурация без трёх коллинеарных с ЗАДАННЫМ профилем слоёв?
Проверяет гипотезу «внешние слои несут планарный максимум 2n, внутренние 2n−2» (формула 2n²−2n+4).
Профиль задаётся по всем трём осям одновременно.  usage: profile_test.py n prof_comma_separated [seconds]"""
import sys, time
from itertools import combinations
from collections import defaultdict
from math import gcd
from ortools.sat.python import cp_model
n = int(sys.argv[1]); prof = [int(v) for v in sys.argv[2].split(',')]; T = float(sys.argv[3]) if len(sys.argv) > 3 else 600
axes = [int(v) for v in sys.argv[4].split(',')] if len(sys.argv) > 4 else [0,1,2]
assert len(prof) == n
pts = [(x, y, z) for x in range(n) for y in range(n) for z in range(n)]
idx = {p: i for i, p in enumerate(pts)}
L = defaultdict(set)
for i in range(len(pts)):
    for j in range(i+1, len(pts)):
        p, q = pts[i], pts[j]; d = tuple(q[k]-p[k] for k in range(3))
        g = gcd(gcd(abs(d[0]), abs(d[1])), abs(d[2])); d = tuple(v//g for v in d)
        if d[0] < 0 or (d[0] == 0 and (d[1] < 0 or (d[1] == 0 and d[2] < 0))): d = tuple(-v for v in d)
        base = p
        while all(0 <= base[k]-d[k] < n for k in range(3)): base = tuple(base[k]-d[k] for k in range(3))
        L[(base, d)] |= {i, j}
lines = [sorted(s) for s in L.values() if len(s) >= 3]
m = cp_model.CpModel(); x = [m.NewBoolVar(f'x{i}') for i in range(len(pts))]
for s in lines: m.Add(sum(x[i] for i in s) <= 2)
for axis in axes:
    for lay in range(n):
        m.Add(sum(x[idx[p]] for p in pts if p[axis] == lay) == prof[lay])
sol = cp_model.CpSolver(); sol.parameters.max_time_in_seconds = T; sol.parameters.num_search_workers = 2
t0 = time.time(); st = sol.Solve(m); el = time.time()-t0
tot = sum(prof)
if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    S = [pts[i] for i in range(len(pts)) if sol.Value(x[i])]
    bad = next((t for t in combinations(S,3) if (lambda u,v: (u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0])==(0,0,0))(
        tuple(t[1][k]-t[0][k] for k in range(3)), tuple(t[2][k]-t[0][k] for k in range(3)))), None)
    print(f"n={n} profile={prof} axes={axes} (total {tot}): FOUND in {el:.0f}s, certified={'OK' if bad is None else 'FAIL'}"); print(sorted(S))
else:
    print(f"n={n} profile={prof} axes={axes} (total {tot}): {sol.StatusName(st)} in {el:.0f}s" + ("  -> PROVED IMPOSSIBLE" if st == cp_model.INFEASIBLE else "  (not a proof)"))
