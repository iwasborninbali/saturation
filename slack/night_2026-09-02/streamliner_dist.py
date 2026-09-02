#!/usr/bin/env python3
"""Стримлайнер по запрещённым расстояниям: доля решений, у которых ни одна строка И ни один столбец не несёт пару
на расстоянии из F; сокращение пространства для DFS по строкам ≈ (доля разрешённых пар на строку)^n.
usage: streamliner_dist.py all_known_solutions"""
import sys, collections
import numpy as np
ALPHA = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz#$%&@?!()[]<>{}=*+|-/~^_:;,."
IDX = {c: i for i, c in enumerate(ALPHA)}
by_n = collections.defaultdict(list)
for l in open(sys.argv[1]):
    l = l.strip()
    if l: by_n[(len(l) - 1) // 2].append(l)
FAM = {"F1={7,11,13,17}": {7, 11, 13, 17}, "F2={7,11,13}": {7, 11, 13}, "F3={5,7,9,11,13,14,17}": {5, 7, 9, 11, 13, 14, 17},
       "F4={7,11}": {7, 11}, "F5=простые>=7": {7, 11, 13, 17, 19, 23, 29, 31}}
print(f"{'n':>3} {'решений':>8} {'семейство':>24} {'разреш. пар/строку':>18} {'пространство':>13} {'выжило (строки)':>16} {'выжило (стр+стб)':>17} {'выигрыш':>9}")
for n in (16, 18, 19, 20, 25, 31):
    if n not in by_n: continue
    L = by_n[n]
    rows_d = []; cols_d = []
    for l in L:
        b = l[1:]; r = [(IDX[b[2 * i]], IDX[b[2 * i + 1]]) for i in range(n)]
        rows_d.append([abs(a - c) for a, c in r])
        colpts = collections.defaultdict(list)
        for i, (a, c) in enumerate(r): colpts[a].append(i); colpts[c].append(i)
        cols_d.append([abs(v[0] - v[1]) for v in colpts.values() if len(v) == 2])
    for name, F in FAM.items():
        allowed = sum(n - d for d in range(1, n) if d not in F) / (n * (n - 1) / 2)
        space = allowed ** n
        surv_r = np.mean([all(d not in F for d in ds) for ds in rows_d])
        surv_rc = np.mean([all(d not in F for d in ds) and all(d not in F for d in cs) for ds, cs in zip(rows_d, cols_d)])
        gain = (surv_r / space) if space > 0 else float('inf')
        print(f"{n:>3} {len(L):>8} {name:>24} {allowed:>18.3f} {space:>13.2e} {surv_r:>16.3f} {surv_rc:>17.3f} {gain:>9.1f}")
