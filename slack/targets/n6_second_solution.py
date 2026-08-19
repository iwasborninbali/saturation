"""n6_second_solution.py — есть ли ДРУГАЯ конфигурация на 64 точки в [6]^3 (кроме найденной)?
Добавляем блокирующее ограничение «не более 63 точек из данного множества» и ищем снова.
UNSAT ⇒ конфигурация единственна (как множество); SAT ⇒ печатаем вторую и сравниваем с первой с точностью до 48 симметрий куба.
usage: n6_second_solution.py witness_file [seconds]"""
import sys, re, time
from itertools import combinations, permutations, product
from collections import defaultdict
from math import gcd
from ortools.sat.python import cp_model
n = 6
W = set(tuple(int(v) for v in m) for m in re.findall(r'\(?\s*(\d+)[,\s]+(\d+)[,\s]+(\d+)\s*\)?', re.sub(r'#.*', '', open(sys.argv[1]).read())))
T = float(sys.argv[2]) if len(sys.argv) > 2 else 900
pts = [(x, y, z) for x in range(n) for y in range(n) for z in range(n)]
idx = {p: i for i, p in enumerate(pts)}
L = defaultdict(set)
for i in range(len(pts)):
    for j in range(i+1, len(pts)):
        p, q = pts[i], pts[j]; d = tuple(q[k]-p[k] for k in range(3))
        g = gcd(gcd(abs(d[0]), abs(d[1])), abs(d[2])); d = tuple(x//g for x in d)
        if d[0] < 0 or (d[0] == 0 and (d[1] < 0 or (d[1] == 0 and d[2] < 0))): d = tuple(-x for x in d)
        base = p
        while all(0 <= base[k]-d[k] < n for k in range(3)): base = tuple(base[k]-d[k] for k in range(3))
        L[(base, d)] |= {i, j}
lines = [sorted(s) for s in L.values() if len(s) >= 3]
m = cp_model.CpModel(); x = [m.NewBoolVar(f'x{i}') for i in range(len(pts))]
for s in lines: m.Add(sum(x[i] for i in s) <= 2)
m.Add(sum(x) >= 64)
m.Add(sum(x[idx[p]] for p in W) <= 63)          # exclude the known witness
sol = cp_model.CpSolver(); sol.parameters.max_time_in_seconds = T; sol.parameters.num_search_workers = 3
t0 = time.time(); st = sol.Solve(m); el = time.time()-t0
if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    S = {pts[i] for i in range(len(pts)) if sol.Value(x[i])}
    def canon(P):
        best = None
        for perm in permutations(range(3)):
            for fl in product([False, True], repeat=3):
                key = tuple(sorted(tuple((n-1-p[perm[i]] if fl[i] else p[perm[i]]) for i in range(3)) for p in P))
                if best is None or key < best: best = key
        return best
    print(f"SECOND configuration FOUND in {el:.0f}s; equivalent to the first up to the 48 cube symmetries: {canon(S)==canon(W)}")
    print("second witness:", sorted(S))
else:
    print(f"{sol.StatusName(st)} in {el:.0f}s -> no other 64-point configuration exists (the witness is unique AS A SET)")
