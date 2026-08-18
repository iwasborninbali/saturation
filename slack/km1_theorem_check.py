"""km1_theorem_check.py — check the fractional cover behind  alpha(P_{-1}) <= 4(p-1) - 4 m8(p):
build the dual explicitly (weight 1 on the three lines of every good residue group of both slopes, weight 1/2 on every row and column
of the remaining classes), verify feasibility (every point covered >= 1) and compute its cost; compare with LP(1) and known alpha.
usage: python3 slack/km1_theorem_check.py p1 p2 ..."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from collections import defaultdict
import numpy as np
from scipy.optimize import linprog
def check(p, lp=True):
    h = (p - 1) // 2
    pts = [(x, y) for x in range(-h, 3 * h + 2) for y in range(0, 2 * p) if (x * y) % p in (1, p - 1)]
    idx = {q: i for i, q in enumerate(pts)}; n = len(pts)
    dia = defaultdict(list); ant = defaultdict(list); rows = defaultdict(list); cols = defaultdict(list)
    for (x, y) in pts:
        i = idx[(x, y)]; dia[x - y].append(i); ant[x + y].append(i); rows[y].append(i); cols[x].append(i)
    cover = np.zeros(n); cost = 0.0; blocks = 0; block_pts = set()
    for fam in (dia, ant):
        for c, mem in fam.items():
            if len(mem) == 8:
                grp = fam.get(c - p, []) + mem + fam.get(c + p, [])
                assert len(grp) == 16, (p, c, len(grp))
                assert not (set(grp) & block_pts), "blocks overlap!"
                block_pts |= set(grp); blocks += 1
                for i in grp: cover[i] += 1
                cost += 6
    m8 = sum(1 for mem in dia.values() if len(mem) == 8); m8b = sum(1 for mem in ant.values() if len(mem) == 8)
    assert m8 == m8b and blocks == 2 * m8, (m8, m8b, blocks)
    # rows/columns of the rest at weight 1/2; check they are entirely rest
    for fam in (rows, cols):
        for c, mem in fam.items():
            inb = [i in block_pts for i in mem]
            assert all(inb) or not any(inb), f"partial row/col at p={p}: {c}"
            if not any(inb):
                for i in mem: cover[i] += 0.5
                cost += 1.0            # 2 * 1/2
    assert (cover >= 1 - 1e-9).all(), "not a cover"
    bound = 4 * (p - 1) - 4 * m8
    assert abs(cost - bound) < 1e-9, (cost, bound)
    out = f"p={p}: m8={m8}, blocks={blocks}, cover cost = {cost:.0f} = 4(p-1) - 4 m8 = {bound}  ({bound/(p-1):.3f}(p-1))"
    if lp:
        lines = [mem for fam in (rows, cols, dia, ant) for mem in fam.values() if len(mem) >= 3]
        A = np.zeros((len(lines), n))
        for i, mem in enumerate(lines):
            for j in mem: A[i, j] = 1
        res = linprog(-np.ones(n), A_ub=A, b_ub=2 * np.ones(len(lines)), bounds=[(0, 1)] * n, method='highs')
        out += f"; LP(1) = {-res.fun:.2f}"
    return out
for a in sys.argv[1:]:
    print(check(int(a)), flush=True)
