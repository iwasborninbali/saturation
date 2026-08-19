"""n6_lower.py — независимый поиск НИЖНЕЙ границы для a(6) (3D no-three-in-line): есть ли конфигурация из M точек?
Решающая форма для CP-SAT: ищем ровно M точек, при успехе свидетель проверяется перебором ВСЕХ троек векторными произведениями.
usage: n6_lower.py n M [seconds] [workers]"""
import sys, time
from itertools import combinations
from ortools.sat.python import cp_model
sys.path.insert(0, 'slack')
from lp_curve import lines as alllines
n = int(sys.argv[1]); M = int(sys.argv[2]); T = float(sys.argv[3]) if len(sys.argv) > 3 else 1800; W = int(sys.argv[4]) if len(sys.argv) > 4 else 10
pts = [(x, y, z) for x in range(n) for y in range(n) for z in range(n)]
from collections import defaultdict
from math import gcd
L = defaultdict(set)
for i in range(len(pts)):
    for j in range(i+1, len(pts)):
        p, q = pts[i], pts[j]; d = tuple(q[k]-p[k] for k in range(3))
        g = gcd(gcd(abs(d[0]), abs(d[1])), abs(d[2])); d = tuple(x//g for x in d)
        if d[0] < 0 or (d[0] == 0 and (d[1] < 0 or (d[1] == 0 and d[2] < 0))): d = tuple(-x for x in d)
        base = p
        while True:
            nb = tuple(base[k]-d[k] for k in range(3))
            if all(0 <= c < n for c in nb): base = nb
            else: break
        L[(base, d)] |= {i, j}
lines = [sorted(s) for s in L.values() if len(s) >= 3]
m = cp_model.CpModel(); x = [m.NewBoolVar(f'x{i}') for i in range(len(pts))]
for s in lines: m.Add(sum(x[i] for i in s) <= 2)
m.Add(sum(x) >= M)
sol = cp_model.CpSolver(); sol.parameters.max_time_in_seconds = T; sol.parameters.num_search_workers = W
t0 = time.time(); st = sol.Solve(m); el = time.time() - t0
if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    S = [pts[i] for i in range(len(pts)) if sol.Value(x[i])]
    bad = None
    for a, b, c in combinations(S, 3):
        u = tuple(b[k]-a[k] for k in range(3)); v = tuple(c[k]-a[k] for k in range(3))
        if (u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0]) == (0,0,0): bad = (a,b,c); break
    print(f"n={n} M={M}: FOUND {len(S)} points in {el:.0f}s, certified={'OK' if bad is None else 'FAIL '+str(bad)}")
    print("witness:", S, flush=True)
else:
    print(f"n={n} M={M}: {sol.StatusName(st)} in {el:.0f}s (no configuration found; NOT a proof of impossibility)", flush=True)
