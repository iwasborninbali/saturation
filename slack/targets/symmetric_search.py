"""symmetric_search.py — поиск больших конфигураций СРЕДИ ИНВАРИАНТНЫХ под заданной подгруппой.

Идея берётся из самого ответа: оптимум при n=6 имеет стабилизатор порядка 24, то есть оптимальная
конфигурация оказалась исключительно симметричной. Если это не совпадение, то искать стоит сразу
в симметричном слое: требование инвариантности склеивает клетки в орбиты, и число переменных
падает примерно в |G| раз. При n=8 это 512 клеток против ~64 орбит — разница между «безнадёжно»
и «секунды».

ЗАКОННОСТЬ. Ограничение сужает поиск, поэтому оно годится ТОЛЬКО для нижних границ: что нашли —
то существует, каким бы способом ни искали. Для верхней границы такое предположение было бы
лишним и результат был бы недействителен. Ненайденное здесь не значит несуществующее — это
«не знаю», и никогда «нет».

    python3 symmetric_search.py n out.txt seconds gen1 [gen2 ...]
где генератор — строка вида "yzx" (перестановка осей) с необязательными минусами: "-x,y,-z"
означает (x,y,z) -> (m-x, y, m-z); "y,z,x" означает (x,y,z) -> (y,z,x).
"""
import sys, time
from collections import defaultdict
from itertools import combinations
from math import gcd
from ortools.sat.python import cp_model

n = int(sys.argv[1]); out = sys.argv[2]; T = float(sys.argv[3])
# генераторы — всё после третьего аргумента, кроме ключей и их значений
_rest = sys.argv[4:]
gens_txt, _skip = [], False
for _a in _rest:
    if _skip: _skip = False; continue
    if _a.startswith("--"): _skip = True; continue
    gens_txt.append(_a)
m1 = n - 1
pts = [(x, y, z) for x in range(n) for y in range(n) for z in range(n)]
idx = {p: i for i, p in enumerate(pts)}


def parse(g):
    """"-x,y,-z" -> функция на точках"""
    parts = [t.strip() for t in g.split(",")]
    assert len(parts) == 3
    sel, neg = [], []
    for t in parts:
        s = t.startswith("-"); t = t.lstrip("-")
        sel.append("xyz".index(t)); neg.append(s)
    return lambda p: tuple((m1 - p[sel[k]]) if neg[k] else p[sel[k]] for k in range(3))


def closure(fs):
    """замыкание порождённой группы как множество перестановок индексов"""
    ident = tuple(range(len(pts)))
    G = {ident}
    frontier = [ident]
    perms = [tuple(idx[f(p)] for p in pts) for f in fs]
    while frontier:
        cur = frontier.pop()
        for q in perms:
            new = tuple(q[cur[i]] for i in range(len(pts)))
            if new not in G:
                G.add(new); frontier.append(new)
    return G


G = closure([parse(g) for g in gens_txt])
# орбиты клеток
parent = list(range(len(pts)))
def find(a):
    while parent[a] != a: parent[a] = parent[parent[a]]; a = parent[a]
    return a
def union(a, b):
    ra, rb = find(a), find(b)
    if ra != rb: parent[ra] = rb
for q in G:
    for i in range(len(pts)): union(i, q[i])
orb = defaultdict(list)
for i in range(len(pts)): orb[find(i)].append(i)
orbits = list(orb.values())

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

mo = cp_model.CpModel()
ov = [mo.NewBoolVar(f"o{k}") for k in range(len(orbits))]
cell = [None] * len(pts)
for k, o in enumerate(orbits):
    for i in o: cell[i] = ov[k]
for s in lines: mo.Add(sum(cell[i] for i in s) <= 2)
mo.Maximize(sum(len(orbits[k]) * ov[k] for k in range(len(orbits))))
print(f"n={n}: |G|={len(G)}, орбит клеток {len(orbits)} (из {len(pts)}), богатых прямых {len(lines)}", flush=True)


def collinear_count(S):
    bad = 0
    for a, b, c in combinations(S, 3):
        u = tuple(b[k]-a[k] for k in range(3)); v = tuple(c[k]-a[k] for k in range(3))
        if (u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0]) == (0, 0, 0): bad += 1
    return bad


class Saver(cp_model.CpSolverSolutionCallback):
    def __init__(self): super().__init__(); self.best = -1; self.t0 = time.time()
    def on_solution_callback(self):
        S = sorted(pts[i] for i in range(len(pts)) if self.Value(cell[i]))
        if len(S) <= self.best: return
        self.best = len(S); bad = collinear_count(S)
        pr = [[sum(1 for p in S if p[a] == t) for t in range(n)] for a in range(3)]
        with open(out, "w") as f:
            f.write(f"# no-three-in-line 3D, n={n}, points={len(S)}, invariant under group of order {len(G)}\n")
            f.write(f"# generators: {gens_txt}\n")
            f.write(f"# verified in place: collinear triples = {bad}{'  <-- НЕЧИСТ' if bad else ''}\n")
            f.write(f"# profile per axis x,y,z: {pr}\n")
            for p in S: f.write(f"{p[0]} {p[1]} {p[2]}\n")
        print(f"  [{time.time()-self.t0:5.0f}s] {len(S)} точек, коллинеарных {bad} -> записано", flush=True)


sol = cp_model.CpSolver(); sol.parameters.max_time_in_seconds = T
sol.parameters.num_search_workers = int(sys.argv[sys.argv.index("--workers")+1]) if "--workers" in sys.argv else 2
st = sol.Solve(mo, Saver())
print(f"n={n} |G|={len(G)}: статус {sol.StatusName(st)}; лучшее среди ИНВАРИАНТНЫХ {Saver.best if False else ''}"
      f" -> см. файл; потолок для инвариантных {sol.BestObjectiveBound():.0f}")
print("ЗАМЕЧАНИЕ: это оптимум В СИММЕТРИЧНОМ СЛОЕ, не a(n). Нижняя граница — законна; верхняя — нет.")
