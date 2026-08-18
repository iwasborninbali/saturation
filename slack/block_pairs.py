"""block_pairs.py — k=-1: locality of the loss.  For every pair (and optionally triple) of orbit blocks (16 points each), compute the exact
maximum lawful subset of their union (CP-SAT, all lines of the union with >= 3 candidates), and report how far below 8 per block it is.
usage: python3 slack/block_pairs.py p [triples]"""
import sys, os, itertools
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from maxlawful_pysat import lines
from ortools.sat.python import cp_model
from collections import Counter
p = int(sys.argv[1]); do_triples = len(sys.argv) > 2 and sys.argv[2] == 'triples'
h = (p - 1) // 2
def X(u): u %= p; return u if u <= h else u - p
pts_all = [(x, y) for x in range(-h, 3 * h + 2) for y in range(0, 2 * p) if (x * y) % p in (1, p - 1)]
blocks = {}
for a in range(1, h + 1):
    ia = pow(a, -1, p)
    cols = {X(a), X(a) + p, X(p - a), X(p - a) + p}; rows = {ia, ia + p, p - ia, 2 * p - ia}
    blocks[a] = [(x, y) for (x, y) in pts_all if x in cols and y in rows]
    assert len(blocks[a]) == 16, (a, len(blocks[a]))
def maxlawful(pts):
    P = sorted(pts); L = lines([(x + h, y) for x, y in P])
    m = cp_model.CpModel(); z = [m.NewBoolVar(f"z{i}") for i in range(len(P))]
    for mem in L: m.Add(sum(z[i] for i in mem) <= 2)
    m.Maximize(sum(z)); s = cp_model.CpSolver(); s.parameters.num_search_workers = 4; s.parameters.max_time_in_seconds = 60
    st = s.Solve(m); return int(s.ObjectiveValue()), s.StatusName(st)
single = {a: maxlawful(blocks[a])[0] for a in blocks}
print(f"p={p}: {len(blocks)} orbit blocks; single-block maxima: {Counter(single.values())}")
res = Counter(); worst = []
for a, b in itertools.combinations(sorted(blocks), 2):
    v, st = maxlawful(blocks[a] + blocks[b]); d = single[a] + single[b] - v
    res[d] += 1
    if d > 0: worst.append((d, a, b))
print(f"  pairs: loss distribution (single_a+single_b - max_pair): {sorted(res.items())}; conflicting pairs: {sorted(worst)[:20]}")
if do_triples:
    res3 = Counter(); ex = []
    for a, b, c in itertools.combinations(sorted(blocks), 3):
        v, st = maxlawful(blocks[a] + blocks[b] + blocks[c]); d = single[a] + single[b] + single[c] - v
        res3[d] += 1
        if d > 0: ex.append((d, a, b, c))
    print(f"  triples: loss distribution: {sorted(res3.items())}; examples: {sorted(ex)[:15]}")
