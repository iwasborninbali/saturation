"""maximize_witness.py — поиск наибольшей конфигурации без трёх коллинеарных в [n]^3,
записывающий найденное В МОМЕНТ НАХОДКИ.

Правило, ради которого написано (за сутки нарушено трижды, дважды мной): программа, печатающая
«найдено», обязана в тот же миг положить найденное в файл. Иначе она печатает утверждение, под
которым нечего предъявить, и её вывод неотличим от догадки. Здесь это свойство кода, а не
дисциплины: обратный вызов срабатывает на каждом улучшении, так что даже убитый прогон оставляет
лучшее, до чего дошёл. Убитый прогон, не оставивший следа, — это ровно та ловушка, на которой мы
оба спотыкались, и лечится она не внимательностью, а конструкцией.

Профиль по слоям, если задан, резко сужает поиск и остаётся ЗАКОННЫМ для нижней границы: любая
найденная конфигурация есть конфигурация, каким бы способом её ни искали. (Для ВЕРХНЕЙ границы
профиль, разумеется, ничего не даёт — там он был бы лишним предположением.)

    python3 maximize_witness.py n out.txt [seconds] [--profile a,b,...] [--axes 0,1,2] [--lb M]
"""
import sys, time
from collections import defaultdict
from itertools import combinations
from math import gcd
from ortools.sat.python import cp_model


def arg(flag, default=None):
    return sys.argv[sys.argv.index(flag) + 1] if flag in sys.argv else default


n = int(sys.argv[1]); out = sys.argv[2]
T = float(sys.argv[3]) if len(sys.argv) > 3 and not sys.argv[3].startswith("--") else 3600
prof = [int(v) for v in arg("--profile", "").split(",")] if arg("--profile") else None
axes = [int(v) for v in arg("--axes", "0,1,2").split(",")]
lb = int(arg("--lb", "0"))

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
lines = [sorted(s) for s in L.values() if len(s) >= 3]

m = cp_model.CpModel(); x = [m.NewBoolVar(f"x{i}") for i in range(len(pts))]
for s in lines: m.Add(sum(x[i] for i in s) <= 2)
if prof:
    for a in axes:
        for lay in range(n):
            m.Add(sum(x[idx[p]] for p in pts if p[a] == lay) == prof[lay])
if lb: m.Add(sum(x) >= lb)
m.Maximize(sum(x))

hint = arg("--hint")
if hint:                       # тёплый старт: конфигурация, найденная в симметричном слое
    H = set()
    for _l in open(hint):
        _l = _l.strip()
        if not _l or _l.startswith("#"): continue
        _t = _l.split()
        if len(_t) >= 3: H.add(tuple(int(v) for v in _t[:3]))
    for _i, _p in enumerate(pts): m.AddHint(x[_i], 1 if _p in H else 0)
    print(f"тёплый старт из {hint}: {len(H)} точек", flush=True)


def collinear_count(S):
    bad = 0
    for a, b, c in combinations(S, 3):
        u = tuple(b[k] - a[k] for k in range(3)); v = tuple(c[k] - a[k] for k in range(3))
        if (u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0]) == (0, 0, 0): bad += 1
    return bad


class Saver(cp_model.CpSolverSolutionCallback):
    def __init__(self):
        super().__init__(); self.best = -1; self.t0 = time.time()

    def on_solution_callback(self):
        S = sorted(pts[i] for i in range(len(pts)) if self.Value(x[i]))
        if len(S) <= self.best: return
        self.best = len(S)
        bad = collinear_count(S)                          # проверяем КАЖДУЮ сохраняемую, а не только последнюю
        pr = [[sum(1 for p in S if p[a] == t) for t in range(n)] for a in range(3)]
        with open(out, "w") as f:
            f.write(f"# no-three-in-line 3D, n={n}, points={len(S)}\n")
            f.write(f"# verified in place: C({len(S)},3) triples checked, collinear={bad}"
                    f"{'  <-- НЕЧИСТ, НЕ ИСПОЛЬЗОВАТЬ' if bad else ''}\n")
            f.write(f"# profile per axis x,y,z: {pr}\n")
            f.write(f"# found {time.time()-self.t0:.0f}s into the run"
                    f"{'' if prof is None else f', profile {prof} imposed on axes {axes}'}\n")
            for p in S: f.write(f"{p[0]} {p[1]} {p[2]}\n")
        print(f"  [{time.time()-self.t0:6.0f}s] {len(S)} точек, коллинеарных {bad} -> записано", flush=True)


sol = cp_model.CpSolver()
sol.parameters.max_time_in_seconds = T
sol.parameters.num_search_workers = int(arg("--workers", "3"))
cb = Saver()
st = sol.Solve(m, cb)
print(f"n={n} profile={prof} axes={axes if prof else '-'}: статус {sol.StatusName(st)}, "
      f"лучшее {cb.best}, потолок {sol.BestObjectiveBound():.0f}")
print("ЗАМЕЧАНИЕ: OPTIMAL здесь означает оптимум ПРИ НАВЯЗАННОМ ПРОФИЛЕ, а не a(n)." if prof
      else "ЗАМЕЧАНИЕ: OPTIMAL здесь означало бы точное a(n); всё прочее — только нижняя граница.")
