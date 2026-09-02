#!/usr/bin/env python3
"""Механизм спектра направлений: модель «пара стоит затенённых клеток».
Предсказание: pairs(v) = E(v)·exp(−λ·kill(v)) / Z, где E(v) — ожидание для случайного 2n-множества,
kill(v) — среднее число клеток, которые убивает пара направления v (длина её прямой минус 2),
Z — нормировка, сохраняющая общее число пар (C(2n,2) минус строки/столбцы, которые заданы точно).
λ подгоняется по ОДНОМУ направлению (1,±1); всё остальное — предсказание."""
import sys, math, collections
import numpy as np
ALPHA = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz#$%&@?!()[]<>{}=*+|-/~^_:;,."
lut = np.zeros(256, dtype=np.int64)
for i, c in enumerate(ALPHA): lut[ord(c)] = i
n = int(sys.argv[2]) if len(sys.argv) > 2 else 20
lines_ = [l.strip() for l in open(sys.argv[1]) if len(l.strip()) == 2 * n + 1]
S = len(lines_)
cols = lut[np.frombuffer(''.join(l[1:] for l in lines_).encode(), dtype=np.uint8).reshape(S, 2 * n)]
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

def line_stats(a, b):
    """ожидаемые пары E и среднее убийство на пару для направления (a,b): по всем прямым этого направления"""
    seen = set(); E = 0.0; K = 0.0; N = n * n
    for x0 in range(n):
        for y0 in range(n):
            if (x0 - a, y0 - b) in seen or (0 <= x0 - a < n and 0 <= y0 - b < n): continue
            L = 0; x, y = x0, y0
            while 0 <= x < n and 0 <= y < n: L += 1; x += a; y += b
            if L >= 2:
                c2 = L * (L - 1) / 2; E += c2; K += c2 * (L - 2)
    E *= (2 * n) * (2 * n - 1) / (N * (N - 1))
    return E, (K / (E / ((2 * n) * (2 * n - 1) / (N * (N - 1)))) if E else 0.0)

dirs = [d for d in meas if d not in ((1, 0), (0, 1))]
E = {d: line_stats(*d)[0] for d in dirs}; kill = {d: line_stats(*d)[1] for d in dirs}
total = sum(meas[d] for d in dirs)          # пары вне строк/столбцов (должно быть 780 − 40 = 740)
def predict(lam):
    w = {d: E[d] * math.exp(-lam * kill[d]) for d in dirs}; Z = sum(w.values())
    return {d: w[d] / Z * total for d in dirs}
# λ по одному направлению (1,1)+(1,-1)
target = (meas[(1, 1)] + meas[(1, -1)]) / 2
lo, hi = 0.0, 5.0
for _ in range(60):
    mid = (lo + hi) / 2; p = predict(mid)
    if (p[(1, 1)] + p[(1, -1)]) / 2 > target: lo = mid
    else: hi = mid
lam = (lo + hi) / 2; P = predict(lam)
print(f"n={n}, решений {S}; пар вне строк/столбцов: измерено {total:.1f}; λ (по диагоналям) = {lam:.4f}; kill(1,1)={kill[(1,1)]:.2f}, kill(1,2)={kill[(1,2)]:.2f}, kill(3,4)={kill[(3,4)]:.2f}")
print(f"{'направление':>12} {'измерено':>9} {'ожид.':>7} {'kill':>6} {'ratio изм.':>10} {'ratio модель':>12}")
for d in sorted(dirs, key=lambda d: -meas[d])[:14]:
    print(f"{str(d):>12} {meas[d]:9.3f} {E[d]:7.3f} {kill[d]:6.2f} {meas[d]/E[d]:10.3f} {P[d]/E[d]:12.3f}")
print("\nпо уровню m = max(|a|,|b|):")
lv = collections.defaultdict(lambda: [0.0, 0.0, 0.0])
for d in dirs:
    m = max(abs(d[0]), abs(d[1])); lv[m][0] += meas[d]; lv[m][1] += E[d]; lv[m][2] += P[d]
err = []
for m in sorted(lv)[:12]:
    a, e, p = lv[m]; err.append((a / e - p / e, e))
    print(f"   m={m:2d}: ratio измерено {a/e:.3f}  модель {p/e:.3f}  разница {a/e-p/e:+.3f}")
rms = math.sqrt(sum(x * x * w for x, w in err) / sum(w for _, w in err))
print(f"\nвзвешенный RMS ошибки отношения по уровням m=1..12: {rms:.3f};  предсказание модели для m=5..7: {[round(lv[m][2]/lv[m][1],3) for m in (5,6,7)]}")
