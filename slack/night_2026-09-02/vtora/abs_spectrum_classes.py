#!/usr/bin/env python3
"""abs_spectrum_classes.py — абсолютный спектр направлений по базе Фламменкампа: c_v = число пар точек решения, разность которых —
положительное кратное примитивного вектора v, делённое на n; среднее по ориентациям класса {(a,b),(b,a),(a,−b),(b,−a)} (для (a,a) — две),
затем среднее по всем решениям с n_min ≤ n ≤ n_max (каждое решение — вес 1). Векторизовано numpy по группам одного n.
usage: python3 abs_spectrum_classes.py n_min n_max a,b [a,b …]"""
import sys, collections, numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from cycle_census import DB, IDX
n_min, n_max = int(sys.argv[1]), int(sys.argv[2]); classes = [tuple(int(t) for t in s.split(',')) for s in sys.argv[3:]]
grids = collections.defaultdict(list)
for l in open(DB):
    l = l.strip()
    if not l: continue
    n = (len(l) - 1) // 2
    if n < n_min or n > n_max: continue
    body = l[1:]; G = np.zeros((n, n), dtype=bool)
    for r in range(n): G[r, IDX[body[2*r]]] = True; G[r, IDX[body[2*r+1]]] = True
    grids[n].append(G)
def count_dir(A, a, b):
    """пары с разностью (ka, kb), k ≥ 1, во всех решениях массива A (N, n, n); a > 0 или (a == 0, b > 0)."""
    N, n, _ = A.shape; tot = np.zeros(N, dtype=np.int64); k = 1
    while k * abs(a) < n and k * abs(b) < n:
        da, db = k * a, k * b
        if db >= 0: tot += np.sum(A[:, :n-da, :n-db] & A[:, da:, db:], axis=(1, 2))
        else: tot += np.sum(A[:, :n-da, -db:] & A[:, da:, :n+db], axis=(1, 2))
        k += 1
    return tot
def orientations(a, b):
    return [(a, b), (a, -b)] if a == b else [(a, b), (b, a), (a, -b), (b, -a)]
res = {}
for cl in classes:
    vals = []
    for n, lst in sorted(grids.items()):
        A = np.stack(lst); ori = orientations(*cl)
        per = sum(count_dir(A, a, b) for a, b in ori) / (len(ori) * n)
        vals.append(per)
    allv = np.concatenate(vals); res[cl] = (allv.mean(), len(allv))
print(f"# база Фламменкампа, n = {n_min}…{n_max}, решений {sum(len(v) for v in grids.values())}; c_v — пар направления v на решение / n, среднее по ориентациям класса, среднее по решениям")
for cl, (m, N) in res.items(): print(f"c_{cl} (среднее по ориентациям) = {m:.4f}")
