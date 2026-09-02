#!/usr/bin/env python3
"""2-D таблица отношений по вектору разности (dx,dy) без gcd, n=20, правильный нуль.
Разложение: примитивное направление v × кратность k (d = k·v; промежуточных клеток k−1) × чётность класса.
usage: diff2d.py all_known_solutions [n]"""
import sys, math, collections
import numpy as np
ALPHA = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz#$%&@?!()[]<>{}=*+|-/~^_:;,."
lut = np.zeros(256, dtype=np.int64)
for i, c in enumerate(ALPHA): lut[ord(c)] = i
n = int(sys.argv[2]) if len(sys.argv) > 2 else 20
L = [l.strip() for l in open(sys.argv[1]) if len(l.strip()) == 2 * n + 1]; S = len(L)
cols = lut[np.frombuffer(''.join(l[1:] for l in L).encode(), dtype=np.uint8).reshape(S, 2 * n)]
rows = np.tile(np.repeat(np.arange(n, dtype=np.int64), 2), (S, 1))
iu = np.triu_indices(2 * n, 1); W = 2 * n + 1; off = n
hist = np.zeros(W * W, dtype=np.int64)
for s in range(0, S, 2000):
    x, y = cols[s:s + 2000], rows[s:s + 2000]
    dx = (x[:, :, None] - x[:, None, :])[:, iu[0], iu[1]]; dy = (y[:, :, None] - y[:, None, :])[:, iu[0], iu[1]]
    flip = (dx < 0) | ((dx == 0) & (dy < 0)); dx = np.where(flip, -dx, dx); dy = np.where(flip, -dy, dy)
    hist += np.bincount(((dx + off) * W + (dy + off)).ravel(), minlength=W * W)
meas = {}
for k in np.nonzero(hist)[0]:
    a, b = divmod(int(k), W); meas[(a - off, b - off)] = hist[k] / S
# правильный нуль
free_pairs = (2 * n) * (2 * n - 1) // 2 - 2 * n
tot_general = sum((n - abs(dx)) * (n - abs(dy)) for dx in range(-(n - 1), n) for dy in range(-(n - 1), n) if dx and dy) // 2
p_gen = free_pairs / tot_general
def null(d):
    dx, dy = d
    cells = (n - abs(dx)) * (n - abs(dy))
    if dx == 0 or dy == 0: return cells / (n * (n - 1) / 2)      # одна пара на строку/столбец, равномерно по C(n,2)
    return cells * p_gen
ratio = {d: meas[d] / null(d) for d in meas}
print(f"n={n}, решений {S}; контроль: сумма измеренных пар = {sum(meas.values()):.1f} (C(40,2)=780), сумма нуля = {sum(null(d) for d in meas):.1f}")

print("\n=== кратность при фиксированном направлении (ratio по d = k·v; k−1 промежуточных клеток) ===")
def prim(d):
    g = math.gcd(abs(d[0]), abs(d[1])); return (d[0] // g, d[1] // g), g
byv = collections.defaultdict(dict)
for d in meas:
    v, g = prim(d); byv[v][g] = (meas[d], null(d))
def line(v):
    ks = sorted(byv[v]); return "  ".join(f"k={k}:{byv[v][k][0]/byv[v][k][1]:.2f}" for k in ks[:10])
for v in [(1, 0), (0, 1), (1, 1), (1, -1), (1, 2), (1, -2), (2, 1), (2, -1), (1, 3), (1, -3), (3, 1), (2, 3), (1, 4), (1, 5)]:
    if v in byv: print(f"  v={str(v):>8}: {line(v)}")

print("\n=== по классу чётности разности (dx mod 2, dy mod 2), только общее положение ===")
cls = collections.defaultdict(lambda: [0.0, 0.0])
for d in meas:
    if d[0] and d[1]: cls[(abs(d[0]) % 2, abs(d[1]) % 2)][0] += meas[d]; cls[(abs(d[0]) % 2, abs(d[1]) % 2)][1] += null(d)
for c in sorted(cls): print(f"  чётность {c}: ratio {cls[c][0]/cls[c][1]:.3f}  (измерено {cls[c][0]:.1f}, нуль {cls[c][1]:.1f})")

print("\n=== по gcd разности (общее положение) и по кратности для m ≤ 3 против m ≥ 4 ===")
byg = collections.defaultdict(lambda: [0.0, 0.0]); bykm = collections.defaultdict(lambda: [0.0, 0.0])
for d in meas:
    if not (d[0] and d[1]): continue
    v, g = prim(d); byg[g][0] += meas[d]; byg[g][1] += null(d)
    m = max(abs(v[0]), abs(v[1])); bykm[(min(g, 5), 'm<=3' if m <= 3 else 'm>=4')][0] += meas[d]; bykm[(min(g, 5), 'm<=3' if m <= 3 else 'm>=4')][1] += null(d)
print("  gcd:", "  ".join(f"g={g}:{byg[g][0]/byg[g][1]:.3f}" for g in sorted(byg)[:8]))
for key in sorted(bykm): print(f"  кратность {key[0]}{'+' if key[0]==5 else ''} {key[1]}: ratio {bykm[key][0]/bykm[key][1]:.3f}")

print("\n=== расстояние внутри столбца/строки: ρ(Δ) (dx=0 или dy=0) ===")
print("  Δ:   " + " ".join(f"{k:>5d}" for k in range(1, 20)))
print("  col: " + " ".join(f"{ratio.get((0, k), float('nan')):5.2f}" for k in range(1, 20)))
print("  row: " + " ".join(f"{ratio.get((k, 0), float('nan')):5.2f}" for k in range(1, 20)))
print("\n=== топ обогащённых и обеднённых векторов разности (общее положение, нуль ≥ 1.0 пары) ===")
gen = [d for d in meas if d[0] and d[1] and null(d) >= 1.0]
for d in sorted(gen, key=lambda d: -ratio[d])[:8]: print(f"  {str(d):>9}: ratio {ratio[d]:.2f} (нуль {null(d):.1f}, gcd {math.gcd(abs(d[0]),abs(d[1]))})")
print("  ...")
for d in sorted(gen, key=lambda d: ratio[d])[:8]: print(f"  {str(d):>9}: ratio {ratio[d]:.2f} (нуль {null(d):.1f}, gcd {math.gcd(abs(d[0]),abs(d[1]))})")
