"""lines_crosscheck.py — independent regeneration of the rich-line sets used by cpsat_max/maxsub: compare maxlawful_pysat.lines(cands)
(primitive-direction keys) with a brute-force determinant enumeration of all triples grouped into lines.  usage: python3 slack/lines_crosscheck.py pmax"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from maxlawful_pysat import cands_M, lines
from itertools import combinations
def rich_by_det(cands):
    n = len(cands); coll = {}
    # for each pair, collect all third points collinear (det = 0); a line = maximal collinear set
    for i, j in combinations(range(n), 2):
        (x1, y1), (x2, y2) = cands[i], cands[j]
        mem = [i, j]
        for k in range(n):
            if k == i or k == j: continue
            x3, y3 = cands[k]
            if (x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1) == 0: mem.append(k)
        if len(mem) >= 3: coll[frozenset(mem)] = 1
    return set(coll)
pmax = int(sys.argv[1]) if len(sys.argv) > 1 else 13
for p in [q for q in range(5, pmax + 1) if all(q % d for d in range(2, int(q ** 0.5) + 1))]:
    for k in (2, 3, p - 1):
        c = cands_M(p, {1, k}, 2 * p)
        A = set(frozenset(m) for m in lines(c)); B = rich_by_det(c)
        print(f"p={p} k={k}: generator {len(A)} lines, determinant {len(B)} lines, equal={A==B}")
        assert A == B
print("OK: rich-line sets agree")
