"""lp1_pieces.py — k=-1, LP(1) integral cover at p (29, 37): print the pieces (rows/columns/±1 lines with weight 1 and singleton points),
in class language: for each point (x,y): hyperbola (1 or -1), class a = x mod p (as base rep), copy (r,s), type A/B/C/D of the H(1) class.
usage: python3 slack/lp1_pieces.py p"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from scipy.optimize import linprog
from collections import defaultdict, Counter
p = int(sys.argv[1]); h = (p - 1) // 2
def X(u): u %= p; return u if u <= h else u - p
def Y(u): u %= p; return u if u else p       # in [1,p]... careful: Y in [1,p-1] for u != 0
pts = [(x, y) for x in range(-h, 3 * h + 2) for y in range(0, 2 * p) if (x * y) % p in (1, p - 1)]
idx = {q: i for i, q in enumerate(pts)}; n = len(pts)
def describe(q):
    x, y = q; a = x % p; hyp = 1 if (x * y) % p == 1 else -1
    Xa = X(a); Yb = Y(y)                       # base copy of the H(1)/H(-1) class (a, y mod p): (X(a), Y(y))
    r = (x - Xa) // p; s = (y - Yb) // p
    # type of the class w.r.t. its own base copy: A: X>0,Y>h ; B: X<0,Y>h ; C: X>0,Y<=h ; D: X<0,Y<=h
    typ = 'A' if Xa > 0 and Yb > h else 'B' if Xa < 0 and Yb > h else 'C' if Xa > 0 else 'D'
    return f"H{'+' if hyp==1 else '-'}({Xa:3d},{Yb:2d}){typ}({r},{s})"
lines = defaultdict(list)
for (x, y) in pts:
    lines[('row', y)].append(idx[(x, y)]); lines[('col', x)].append(idx[(x, y)])
    lines[('dia', x - y)].append(idx[(x, y)]); lines[('ant', x + y)].append(idx[(x, y)])
L = [(key, mem) for key, mem in lines.items() if len(mem) >= 3]
A = np.zeros((len(L), n))
for i, (key, mem) in enumerate(L):
    for j in mem: A[i, j] = 1
res = linprog(-np.ones(n), A_ub=A, b_ub=2 * np.ones(len(L)), bounds=[(0, 1)] * n, method='highs')
y = -res.ineqlin.marginals; z = -res.upper.marginals
print(f"p={p}: LP(1) = {-res.fun:.2f}")
cover = Counter()
for i, (key, mem) in enumerate(L):
    if y[i] > 1e-7:
        for j in mem: cover[j] += y[i]
        print(f"{key[0]} {key[1]:4d} w={y[i]:.2f} size {len(mem)}: ", "  ".join(describe(pts[j]) for j in mem))
for j in range(n):
    if z[j] > 1e-7: print(f"point w={z[j]:.2f}: {describe(pts[j])}"); cover[j] += z[j]
print("coverage multiplicities:", Counter(round(v, 2) for v in cover.values()), " uncovered:", n - len(cover))
