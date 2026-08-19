"""save_witness.py — найти конфигурацию с заданным профилем и СОХРАНИТЬ её как артефакт.

Мотив прямой: в журнале может стоять «FOUND, certified OK», а самой конфигурации нигде нет.
Тогда число живёт только в памяти давно завершившегося процесса, и предъявить его нельзя.
Всё, что заявлено, обязано лежать файлом.

    python3 save_witness.py n prof out.txt [seconds] [axes]
"""
import sys, time
from collections import defaultdict
from itertools import combinations
from math import gcd
from ortools.sat.python import cp_model

n = int(sys.argv[1]); prof = [int(v) for v in sys.argv[2].split(',')]; out = sys.argv[3]
T = float(sys.argv[4]) if len(sys.argv) > 4 else 600
axes = [int(v) for v in sys.argv[5].split(',')] if len(sys.argv) > 5 else [0, 1, 2]
pts = [(x, y, z) for x in range(n) for y in range(n) for z in range(n)]
idx = {p: i for i, p in enumerate(pts)}
L = defaultdict(set)
for i in range(len(pts)):
    for j in range(i + 1, len(pts)):
        p, q = pts[i], pts[j]; d = tuple(q[k] - p[k] for k in range(3))
        g = gcd(gcd(abs(d[0]), abs(d[1])), abs(d[2])); d = tuple(v // g for v in d)
        if d[0] < 0 or (d[0] == 0 and (d[1] < 0 or (d[1] == 0 and d[2] < 0))): d = tuple(-v for v in d)
        b = p
        while all(0 <= b[k] - d[k] < n for k in range(3)): b = tuple(b[k] - d[k] for k in range(3))
        L[(b, d)] |= {i, j}
m = cp_model.CpModel(); x = [m.NewBoolVar(f'x{i}') for i in range(len(pts))]
for s in L.values():
    if len(s) >= 3: m.Add(sum(x[i] for i in sorted(s)) <= 2)
if len(prof) == 1:                      # один аргумент = просто «не меньше M точек», без профиля
    m.Add(sum(x) >= prof[0])
    m.Maximize(sum(x))
else:
    for a in axes:
        for lay in range(n):
            m.Add(sum(x[idx[p]] for p in pts if p[a] == lay) == prof[lay])
sol = cp_model.CpSolver(); sol.parameters.max_time_in_seconds = T; sol.parameters.num_search_workers = 3
t0 = time.time(); st = sol.Solve(m); el = time.time() - t0
if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    print(f"n={n} {prof} axes={axes}: {sol.StatusName(st)} за {el:.0f}с" +
          ("  -> НЕВОЗМОЖНО" if st == cp_model.INFEASIBLE else "  (НЕ доказательство)"))
    sys.exit(0)
S = sorted(pts[i] for i in range(len(pts)) if sol.Value(x[i]))
bad = 0
for a, b, c in combinations(S, 3):
    u = tuple(b[k] - a[k] for k in range(3)); v = tuple(c[k] - a[k] for k in range(3))
    if (u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0]) == (0, 0, 0): bad += 1
prof_check = [[sum(1 for p in S if p[a] == t) for t in range(n)] for a in range(3)]
with open(out, "w") as f:
    f.write(f"# no-three-in-line 3D, n={n}, points={len(S)}, profile requested {prof} on axes {axes}\n")
    f.write(f"# verified: all C({len(S)},3)={len(list(combinations(range(len(S)),3)))} triples, collinear={bad}\n")
    f.write(f"# realised profile per axis x,y,z: {prof_check}\n")
    for p in S: f.write(f"{p[0]} {p[1]} {p[2]}\n")
print(f"n={n} {prof} axes={axes}: НАЙДЕНО {len(S)} точек за {el:.0f}с, коллинеарных троек {bad} "
      f"-> {out}\n  профиль по осям: {prof_check}")
