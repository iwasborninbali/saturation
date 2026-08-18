"""lp1_dual.py — k=-1: LP with rows, columns and slope ±1 lines (>= 3 points) of P = P_1 u P_{-1} in the HJSW box; prints the primal
value and the dual solution (weights on lines and points).   usage: python3 slack/lp1_dual.py p [k]"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from scipy.optimize import linprog
from collections import defaultdict
p = int(sys.argv[1]); h = (p - 1) // 2; k = int(sys.argv[2]) % p if len(sys.argv) > 2 else p - 1
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
print(f"p={p} k={k}: points {n}, lines {len(L)} (rows {sum(1 for k,_ in L if k[0]=='r')}, cols {sum(1 for k,_ in L if k[0]=='c')}, diag {sum(1 for k,_ in L if k[0]=='d')}, anti {sum(1 for k,_ in L if k[0]=='a')}); LP(1) = {val:.3f} = {val/(p-1):.3f}(p-1)")
# duals: ineqlin.marginals (<=0 for max problem written as min -c) ; upper bounds duals in res.upper.marginals
y = -res.ineqlin.marginals; z = -res.upper.marginals
used = [(L[i][0], len(L[i][1]), round(float(y[i]), 3)) for i in range(len(L)) if y[i] > 1e-7]
from collections import Counter
print("dual line weights by (type, size, weight):", sorted(Counter((k[0], sz, w) for k, sz, w in used).items()))
print("points with dual weight:", sum(1 for v in z if v > 1e-7), " total dual value:", round(float(2 * y.sum() + z.sum()), 3))
print("integral dual?", all(abs(w - round(w)) < 1e-6 for _, _, w in used) and all(abs(v-round(v))<1e-6 for v in z))
