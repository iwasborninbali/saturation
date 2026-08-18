"""lp1_general.py — LP(1) (rows, columns, slope ±1 lines with >=3 points, 'at most 2 per line') for P = P_1 ∪ P_k in the HJSW box:
value, and where the dual weight sits (by line type and size).  usage: lp1_general.py k p1 p2 ...   (output: one line per p)"""
import sys, os
import numpy as np
from scipy.optimize import linprog
from collections import defaultdict, Counter
k0 = int(sys.argv[1])
for p in map(int, sys.argv[2:]):
    h = (p - 1) // 2; k = k0 % p
    pts = [(x, y) for x in range(-h, 3 * h + 2) for y in range(0, 2 * p) if (x * y) % p in (1, k)]
    idx = {q: i for i, q in enumerate(pts)}; n = len(pts)
    lines = defaultdict(list)
    for (x, y) in pts:
        lines[('r', y)].append(idx[(x, y)]); lines[('c', x)].append(idx[(x, y)])
        lines[('d', x - y)].append(idx[(x, y)]); lines[('a', x + y)].append(idx[(x, y)])
    L = [(key, mem) for key, mem in lines.items() if len(mem) >= 3]
    A = np.zeros((len(L), n))
    for i, (key, mem) in enumerate(L):
        for j in mem: A[i, j] = 1
    res = linprog(-np.ones(n), A_ub=A, b_ub=2 * np.ones(len(L)), bounds=[(0, 1)] * n, method='highs')
    val = -res.fun
    y = -res.ineqlin.marginals; z = -res.upper.marginals
    wt = defaultdict(float); cnt = Counter(); rich = Counter()
    for i, (key, mem) in enumerate(L):
        rich[(key[0], len(mem))] += 1
        if y[i] > 1e-7: wt[(key[0], len(mem))] += 2 * y[i]; cnt[(key[0], len(mem))] += 1
    zsum = float(z.sum())
    bytype = defaultdict(float)
    for (t, s), w in wt.items(): bytype[t] += w
    print(f"p={p} k={k}: n={n} LP1={val:.2f} = {val/(p-1):.3f}(p-1)  gain vs 4(p-1) = {4*(p-1)-val:.2f}; dual mass: rows {bytype['r']:.1f} cols {bytype['c']:.1f} diag {bytype['d']:.1f} anti {bytype['a']:.1f} points {zsum:.1f}; "
          f"rich lines by (type,size): {dict(sorted(rich.items()))}; weighted (type,size)->mass: {[(ts, round(w,1)) for ts, w in sorted(wt.items()) if w > 0.5]}", flush=True)
