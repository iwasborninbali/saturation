"""verify_cnf_lines7.py — сквозная проверка семантики кодировки, потоковая (годится для n=7,8).

Отличия от verify_cnf_lines.py, обе существенные.

1. НУМЕРАЦИЯ КЛЕТОК ВЗЯТА ТА ЖЕ, ЧТО В ГЕНЕРАТОРЕ: (x*n + y)*n + z. В прежней версии порядок
   перечисления давал отображение (x,y,z) -> (z,y,x). Тест от этого не ломался — переставка осей
   есть симметрия куба, а множество коллинеарных троек под ней замкнуто, так что перебор всех
   троек всё равно накрывал всё. Но держаться на таком совпадении — плохо: в задаче без этой
   симметрии (скажем, с навязанным профилем по одной оси) тот же код молча проверял бы не то.
   Совпадение — не обоснование, поэтому нумерация приведена в точное соответствие.

2. Тройки НЕ материализуются списком: при n=7 их 6.5 млн, при n=8 — 22 млн.

Кардинальность обязана быть тривиальной (M=1): иначе тест меряет продолжаемость, а не запрет.

    python3 verify_cnf_lines7.py n cnf_file [sample]
"""
import random, sys
from itertools import combinations
from pysat.formula import CNF
from pysat.solvers import Cadical153

n = int(sys.argv[1]); path = sys.argv[2]
sample = int(sys.argv[3]) if len(sys.argv) > 3 else 3000
pts = [(x, y, z) for x in range(n) for y in range(n) for z in range(n)]
var = {p: (p[0] * n + p[1]) * n + p[2] + 1 for p in pts}      # ровно как в no3_3d_cnf.py


def collinear(a, b, c):
    u = (b[0]-a[0], b[1]-a[1], b[2]-a[2]); v = (c[0]-a[0], c[1]-a[1], c[2]-a[2])
    return u[1]*v[2] == u[2]*v[1] and u[2]*v[0] == u[0]*v[2] and u[0]*v[1] == u[1]*v[0]


cnf = CNF(from_file=path)
rng = random.Random(7); ntot = 0; col = []; non_kept = []
for t in combinations(pts, 3):
    ntot += 1
    if collinear(*t):
        col.append(t)
    elif len(non_kept) < sample:                     # резервуарная выборка неколлинеарных
        non_kept.append(t)
    else:
        j = rng.randrange(ntot)
        if j < sample:
            non_kept[j] = t
print(f"n={n}: клеток {len(pts)}, троек {ntot}, коллинеарных {len(col)}", flush=True)
missed, over = [], []
with Cadical153(bootstrap_with=cnf.clauses) as S:
    for t in col:
        if S.solve(assumptions=[var[p] for p in t]):
            missed.append(t)
    for t in non_kept:
        if not S.solve(assumptions=[var[p] for p in t]):
            over.append(t)
print(f"  коллинеарных троек НЕ запрещено: {len(missed)}" + (f"  напр. {missed[0]}" if missed else "  — ни одной"))
print(f"  неколлинеарных запрещено зря (выборка {len(non_kept)}): {len(over)}" + (f"  напр. {over[0]}" if over else "  — ни одной"))
print("ВЕРДИКТ:", "семантика кодировки подтверждена при n=%d" % n if not missed and not over
      else "СЕМАНТИКА НЕ ПОДТВЕРЖДЕНА")
