"""verify_cnf_semantics.py — НЕЗАВИСИМАЯ проверка семантики SAT-кодировки A280537 (первый солвер).
Логика проверки не повторяет кодировку: я строю множество ВСЕХ компланарных четвёрок ПРЯМО (целочисленный определитель),
а затем для каждой из них форсирую соответствующие переменные в CNF и требую UNSAT; и наоборот, для случайных
НЕкомпланарных четвёрок требую SAT. Если совпадает на всех четвёрках — кодировка запрещает ровно то, что нужно.
usage: verify_cnf_semantics.py n cnf_file [sample_ok]"""
import sys, random
from itertools import combinations
from pysat.solvers import Cadical153
from pysat.formula import CNF
n = int(sys.argv[1]); path = sys.argv[2]; sample = int(sys.argv[3]) if len(sys.argv) > 3 else 2000
pts = [(x, y, z) for z in range(n) for y in range(n) for x in range(n)]
var = {p: i + 1 for i, p in enumerate(pts)}          # cell (x,y,z) -> variable; must match the encoder's order
def det3(u, v, w): return u[0]*(v[1]*w[2]-v[2]*w[1]) - u[1]*(v[0]*w[2]-v[2]*w[0]) + u[2]*(v[0]*w[1]-v[1]*w[0])
def coplanar(q):
    a, b, c, d = q
    return det3(tuple(b[i]-a[i] for i in range(3)), tuple(c[i]-a[i] for i in range(3)), tuple(d[i]-a[i] for i in range(3))) == 0
cnf = CNF(from_file=path)
allq = list(combinations(pts, 4))
cop = [q for q in allq if coplanar(q)]
non = [q for q in allq if not coplanar(q)]
print(f"n={n}: cells={len(pts)}, quadruples={len(allq)}, coplanar={len(cop)}, non-coplanar={len(non)}", flush=True)
bad_missed = []; bad_over = []
with Cadical153(bootstrap_with=cnf.clauses) as S:
    for q in cop:
        if S.solve(assumptions=[var[p] for p in q]): bad_missed.append(q)
    for q in random.Random(1).sample(non, min(sample, len(non))):
        if not S.solve(assumptions=[var[p] for p in q]): bad_over.append(q)
print(f"  coplanar quadruples NOT forbidden by the encoding: {len(bad_missed)}" + (f"  e.g. {bad_missed[0]}" if bad_missed else "  -> none ✓"))
print(f"  non-coplanar quadruples wrongly forbidden (sample {min(sample,len(non))}): {len(bad_over)}" + (f"  e.g. {bad_over[0]}" if bad_over else "  -> none ✓"))
