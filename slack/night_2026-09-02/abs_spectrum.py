#!/usr/bin/env python3
"""Абсолютный спектр направлений: c_v = (среднее число пар направления v на решение)/n по n — константы?
usage: abs_spectrum.py all_known_solutions"""
import sys, collections
import numpy as np
ALPHA = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz#$%&@?!()[]<>{}=*+|-/~^_:;,."
lut = np.zeros(256, dtype=np.int64)
for i, c in enumerate(ALPHA): lut[ord(c)] = i
by_n = collections.defaultdict(list)
for l in open(sys.argv[1]):
    l = l.strip()
    if l: by_n[(len(l) - 1) // 2].append(l)
DIRS = {"(1,1)": [(1, 1), (1, -1)], "(1,2)": [(1, 2), (1, -2), (2, 1), (2, -1)], "(1,3)": [(1, 3), (1, -3), (3, 1), (3, -1)],
        "(2,3)": [(2, 3), (2, -3), (3, 2), (3, -2)], "(1,4)": [(1, 4), (1, -4), (4, 1), (4, -1)]}
print(f"{'n':>3} {'решений':>8} " + " ".join(f"{k:>7}" for k in DIRS) + "   (c_v = пар на решение / n, усреднено по знакам/осям)")
for n in sorted(by_n):
    L = by_n[n]
    if len(L) < 100 or n < 12: continue
    if len(L) > 20000: L = L[::len(L) // 20000]
    S = len(L)
    cols = lut[np.frombuffer(''.join(l[1:] for l in L).encode(), dtype=np.uint8).reshape(S, 2 * n)]
    rows = np.tile(np.repeat(np.arange(n, dtype=np.int64), 2), (S, 1))
    iu = np.triu_indices(2 * n, 1); W = 2 * n + 1; off = n
    hist = np.zeros(W * W, dtype=np.int64)
    for s in range(0, S, 1000):
        x, y = cols[s:s + 1000], rows[s:s + 1000]
        dx = (x[:, :, None] - x[:, None, :])[:, iu[0], iu[1]]; dy = (y[:, :, None] - y[:, None, :])[:, iu[0], iu[1]]
        g = np.gcd(np.abs(dx), np.abs(dy)); ax, ay = dx // g, dy // g
        flip = (ax < 0) | ((ax == 0) & (ay < 0)); ax = np.where(flip, -ax, ax); ay = np.where(flip, -ay, ay)
        hist += np.bincount(((ax + off) * W + (ay + off)).ravel(), minlength=W * W)
    def pairs(d): return hist[(d[0] + off) * W + (d[1] + off)] / S
    vals = [sum(pairs(d) for d in ds) / len(ds) / n for ds in DIRS.values()]
    print(f"{n:>3} {S:>8} " + " ".join(f"{v:7.4f}" for v in vals))
