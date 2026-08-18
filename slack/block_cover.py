"""block_cover.py — k=-1: the 'block' cover bound.  Blocks = residue groups (of slope +1 or -1) containing an 8-point line: their three
lines (sizes 4,8,4) cover the 16 points of the group's four classes at cost 6.  Greedy: all +1 blocks, then -1 blocks disjoint (in points)
from what is covered.  The remaining points are covered by an LP over rows, columns, ±1 lines and single points (min cost, fractional).
Reports: cost = 6*blocks + rest, compared with 4(p-1) and LP(1).   usage: python3 slack/block_cover.py p [p2 ...]"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from scipy.optimize import linprog
from collections import defaultdict
def run(p):
    h = (p - 1) // 2
    pts = [(x, y) for x in range(-h, 3 * h + 2) for y in range(0, 2 * p) if (x * y) % p in (1, p - 1)]
    idx = {q: i for i, q in enumerate(pts)}; n = len(pts)
    dia = defaultdict(list); ant = defaultdict(list); rows = defaultdict(list); cols = defaultdict(list)
    for (x, y) in pts:
        dia[x - y].append(idx[(x, y)]); ant[x + y].append(idx[(x, y)]); rows[y].append(idx[(x, y)]); cols[x].append(idx[(x, y)])
    covered = np.zeros(n, bool); blocks = 0; cost = 0
    for fam in (dia, ant):
        for c, mem in list(fam.items()):
            if len(mem) == 8:
                grp = fam.get(c - p, []) + mem + fam.get(c + p, [])
                if any(covered[i] for i in grp): continue
                for i in grp: covered[i] = True
                blocks += 1; cost += 6
    rest = [i for i in range(n) if not covered[i]]
    if not rest: return dict(p=p, blocks=blocks, cost=cost, restpts=0, restcost=0)
    lines = [mem for fam in (rows, cols, dia, ant) for mem in fam.values() if len(mem) >= 1]
    # LP: minimize sum 2*y_l + sum z_q  s.t. for each rest point: sum_{l∋q} y_l + z_q >= 1
    m = len(lines); A = np.zeros((len(rest), m + len(rest)))
    pos = {q: r for r, q in enumerate(rest)}
    for li, mem in enumerate(lines):
        for q in mem:
            if q in pos: A[pos[q], li] = 1
    for r in range(len(rest)): A[r, m + r] = 1
    cvec = np.concatenate([2 * np.ones(m), np.ones(len(rest))])
    res = linprog(cvec, A_ub=-A, b_ub=-np.ones(len(rest)), bounds=[(0, None)] * (m + len(rest)), method='highs')
    return dict(p=p, blocks=blocks, cost=cost + res.fun, restpts=len(rest), restcost=res.fun)
for a in sys.argv[1:]:
    p = int(a); r = run(p)
    print(f"p={p}: blocks={r['blocks']} (cost {6*r['blocks']}), rest points {r['restpts']} covered at cost {r['restcost']:.2f} "
          f"(= {r['restcost']/max(1,r['restpts']):.3f} per point; 1/2 = no waste); total {r['cost']:.2f} = {r['cost']/(p-1):.3f}(p-1); "
          f"trivial 4(p-1) = {4*(p-1)}", flush=True)
