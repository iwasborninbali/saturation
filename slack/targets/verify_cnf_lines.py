"""verify_cnf_lines.py — независимая проверка семантики SAT-кодировки 3D no-three-in-line (первый солвер).
Проверяю не список прямых, а САМ CNF: каждую коллинеарную ТРОЙКУ форсирую как assumptions и требую UNSAT,
случайные неколлинеарные — SAT. Коллинеарность считаю прямо векторным произведением (логика, не совпадающая с кодировкой).
ВАЖНО (ловушка 5б): CNF обязан быть собран с ТРИВИАЛЬНОЙ кардинальностью, иначе тест меряет продолжаемость, а не запрет.
usage: verify_cnf_lines.py n cnf_file [sample]"""
import sys, random
from itertools import combinations
from pysat.solvers import Cadical153
from pysat.formula import CNF
n = int(sys.argv[1]); path = sys.argv[2]; sample = int(sys.argv[3]) if len(sys.argv) > 3 else 3000
pts = [(x, y, z) for z in range(n) for y in range(n) for x in range(n)]
var = {p: i + 1 for i, p in enumerate(pts)}
def collinear(t):
    a, b, c = t
    u = tuple(b[i]-a[i] for i in range(3)); v = tuple(c[i]-a[i] for i in range(3))
    return (u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0]) == (0, 0, 0)
cnf = CNF(from_file=path)
allt = list(combinations(pts, 3))
col = [t for t in allt if collinear(t)]; non = [t for t in allt if not collinear(t)]
print(f"n={n}: cells={len(pts)}, triples={len(allt)}, collinear={len(col)}, non-collinear={len(non)}", flush=True)
missed = []; over = []
with Cadical153(bootstrap_with=cnf.clauses) as S:
    for t in col:
        if S.solve(assumptions=[var[p] for p in t]): missed.append(t)
    for t in random.Random(1).sample(non, min(sample, len(non))):
        if not S.solve(assumptions=[var[p] for p in t]): over.append(t)
print(f"  collinear triples NOT forbidden: {len(missed)}" + (f"  e.g. {missed[0]}" if missed else "  -> none OK"))
print(f"  non-collinear wrongly forbidden (sample {min(sample,len(non))}): {len(over)}" + (f"  e.g. {over[0]}" if over else "  -> none OK"))
