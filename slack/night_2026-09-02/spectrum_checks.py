#!/usr/bin/env python3
"""Проверки по вердикту противника (spectrum_model): (1) правильный нуль — равномерная 2-регулярная конфигурация:
P(пара в общем положении занята) = (C(2n,2) − 2n) / (число пар клеток в общем положении); (2) внутриуровневые контрасты:
при фиксированном m = max(|a|,|b|) сравнить направления с разным kill; (3) λ(n) по полным переписям n=12…20,
λ подгоняется по диагоналям в правильном нуле; предрегистрация: λ·n ≈ const.
usage: spectrum_checks.py all_known_solutions"""
import sys, math, collections
import numpy as np
ALPHA = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz#$%&@?!()[]<>{}=*+|-/~^_:;,."
lut = np.zeros(256, dtype=np.int64)
for i, c in enumerate(ALPHA): lut[ord(c)] = i
by_n = collections.defaultdict(list)
for l in open(sys.argv[1]):
    l = l.strip()
    if l: by_n[(len(l) - 1) // 2].append(l)

def measured(n):
    L = by_n[n]; S = len(L)
    cols = lut[np.frombuffer(''.join(l[1:] for l in L).encode(), dtype=np.uint8).reshape(S, 2 * n)]
    rows = np.tile(np.repeat(np.arange(n, dtype=np.int64), 2), (S, 1))
    iu = np.triu_indices(2 * n, 1); W = 2 * n + 1; off = n
    hist = np.zeros(W * W, dtype=np.int64)
    for s in range(0, S, 2000):
        x, y = cols[s:s + 2000], rows[s:s + 2000]
        dx = (x[:, :, None] - x[:, None, :])[:, iu[0], iu[1]]; dy = (y[:, :, None] - y[:, None, :])[:, iu[0], iu[1]]
        g = np.gcd(np.abs(dx), np.abs(dy)); ax, ay = dx // g, dy // g
        flip = (ax < 0) | ((ax == 0) & (ay < 0)); ax = np.where(flip, -ax, ax); ay = np.where(flip, -ay, ay)
        hist += np.bincount(((ax + off) * W + (ay + off)).ravel(), minlength=W * W)
    meas = {}
    for k in np.nonzero(hist)[0]:
        a, b = divmod(int(k), W); meas[(a - off, b - off)] = hist[k] / S
    return meas, S

def geometry(n, a, b):
    """tot = число пар клеток направления (a,b); kill = среднее (L−2) по парам"""
    seen = set(); tot = 0; K = 0
    for x0 in range(n):
        for y0 in range(n):
            if 0 <= x0 - a < n and 0 <= y0 - b < n: continue
            L = 0; x, y = x0, y0
            while 0 <= x < n and 0 <= y < n: L += 1; x += a; y += b
            c2 = L * (L - 1) // 2; tot += c2; K += c2 * (L - 2)
    return tot, (K / tot if tot else 0.0)

print("=== (1)+(3): правильный нуль и λ(n) ===")
print(f"{'n':>3} {'решений':>8} {'ratio(1,1)':>11} {'ratio m=2':>10} {'ratio m=3':>10} {'ratio m>=4':>11} {'λ':>7} {'λ·n':>6} {'потолок 2n−n':>13} {'E_null(1,1)':>12}")
for n in range(12, 21):
    meas, S = measured(n)
    dirs = [d for d in meas if d not in ((1, 0), (0, 1))]
    geo = {d: geometry(n, *d) for d in dirs}
    free_pairs = (2 * n) * (2 * n - 1) // 2 - 2 * n
    tot_all = sum(geo[d][0] for d in dirs)
    p_occ = free_pairs / tot_all                       # правильный нуль
    Ep = {d: geo[d][0] * p_occ for d in dirs}
    lv = collections.defaultdict(lambda: [0.0, 0.0])
    for d in dirs:
        m = max(abs(d[0]), abs(d[1])); lv[m][0] += meas[d]; lv[m][1] += Ep[d]
    r1 = lv[1][0] / lv[1][1]; r2 = lv[2][0] / lv[2][1]; r3 = lv[3][0] / lv[3][1]
    hi = sum(lv[m][0] for m in lv if m >= 4) / sum(lv[m][1] for m in lv if m >= 4)
    # λ по диагоналям в правильном нуле с сохранением free_pairs
    def pred(lam):
        w = {d: Ep[d] * math.exp(-lam * geo[d][1]) for d in dirs}; Z = sum(w.values())
        return {d: w[d] / Z * free_pairs for d in dirs}
    target = (meas[(1, 1)] + meas[(1, -1)]) / 2; lo, hi_ = 0.0, 5.0
    for _ in range(60):
        mid = (lo + hi_) / 2; p = pred(mid)
        if (p[(1, 1)] + p[(1, -1)]) / 2 > target: lo = mid
        else: hi_ = mid
    lam = (lo + hi_) / 2
    print(f"{n:>3} {S:>8} {r1:>11.3f} {r2:>10.3f} {r3:>10.3f} {hi:>11.3f} {lam:>7.4f} {lam*n:>6.3f} {n:>13} {Ep[(1,1)]:>8.2f}")

print("\n=== (2): внутриуровневые контрасты при n=20 (правильный нуль): направления одного m, разный kill ===")
n = 20; meas, S = measured(n)
dirs = [d for d in meas if d not in ((1, 0), (0, 1))]
geo = {d: geometry(n, *d) for d in dirs}
free_pairs = (2 * n) * (2 * n - 1) // 2 - 2 * n; p_occ = free_pairs / sum(geo[d][0] for d in dirs)
print(f"{'m':>3} {'направление':>12} {'kill':>6} {'ratio измерено':>15}")
for m in (3, 4, 5, 6, 7):
    rowsm = sorted({(abs(a), abs(b)) for (a, b) in dirs if max(abs(a), abs(b)) == m})
    for (a, b) in rowsm:
        ds = [d for d in dirs if (abs(d[0]), abs(d[1])) == (a, b)]
        r = sum(meas[d] for d in ds) / sum(geo[d][0] * p_occ for d in ds)
        print(f"{m:>3} {str((a,b)):>12} {geo[ds[0]][1]:>6.2f} {r:>15.3f}")
