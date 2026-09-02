#!/usr/bin/env python3
"""Независимая реализация max-entropy модели «пара стоит затенённых клеток» (MCMC обменами рёбер на конфигурациях
2/строку+2/столбец, P ∝ exp(−λ Σ_пар kill)), с вычислением СПЕКТРА НАПРАВЛЕНИЙ по уровням m против правильного нуля
и сравнением с измеренным на решениях n=20 (0.577 / 0.748 / 0.917 / 1.077 …). Заодно κ и прямоугольники как контроль.
usage: maxent_spectrum.py n lambda samples [burnin] [thin] [seed]"""
import sys, math, random, collections
n = int(sys.argv[1]); lam = float(sys.argv[2]); S = int(sys.argv[3])
burn = int(sys.argv[4]) if len(sys.argv) > 4 else 200000; thin = int(sys.argv[5]) if len(sys.argv) > 5 else 200
random.seed(int(sys.argv[6]) if len(sys.argv) > 6 else 1)
N = n * n
def cell(r, c): return r * n + c
# kill[i][j]: клетки прямой через i, j, кроме i и j
kill = [[0] * N for _ in range(N)]
for i in range(N):
    r1, c1 = divmod(i, n)
    for j in range(i + 1, N):
        r2, c2 = divmod(j, n); dr, dc = r2 - r1, c2 - c1
        g = math.gcd(abs(dr), abs(dc)); dr //= g; dc //= g
        cnt = 0
        for sgn in (1, -1):
            k = 1
            while 0 <= r1 + sgn * k * dr < n and 0 <= c1 + sgn * k * dc < n: cnt += 1; k += 1
        kill[i][j] = kill[j][i] = cnt - 1
# начальная конфигурация: две перестановки без совпадений
while True:
    p1 = list(range(n)); random.shuffle(p1); p2 = list(range(n)); random.shuffle(p2)
    if all(a != b for a, b in zip(p1, p2)): break
rows = [[p1[r], p2[r]] for r in range(n)]
pts = [cell(r, c) for r in range(n) for c in rows[r]]
def energy(pts):
    return sum(kill[pts[i]][pts[j]] for i in range(len(pts)) for j in range(i + 1, len(pts)))
E = energy(pts)
def delta(A, B, A2, B2, pts):
    """снять A,B, поставить A2,B2"""
    d = kill[A2][B2] - kill[A][B]
    for X in pts:
        if X == A or X == B: continue
        d += kill[A2][X] + kill[B2][X] - kill[A][X] - kill[B][X]
    return d
acc = 0; tries = 0; samples = []
total = burn + S * thin
for t in range(total):
    r1, r2 = random.sample(range(n), 2)
    c1 = random.choice(rows[r1]); c2 = random.choice(rows[r2])
    if c1 == c2 or c2 in rows[r1] or c1 in rows[r2]: continue
    A, B, A2, B2 = cell(r1, c1), cell(r2, c2), cell(r1, c2), cell(r2, c1)
    dE = delta(A, B, A2, B2, pts); tries += 1
    if dE <= 0 or random.random() < math.exp(-lam * dE):
        rows[r1][rows[r1].index(c1)] = c2; rows[r2][rows[r2].index(c2)] = c1
        pts[pts.index(A)] = A2; pts[pts.index(B)] = B2; E += dE; acc += 1
    if t >= burn and (t - burn) % thin == 0: samples.append([tuple(divmod(p, n)) for p in pts])
# ---- статистики ----
W = 2 * n + 1; off = n
hist = collections.Counter(); kap = []; rect = []
for smp in samples:
    diag = collections.Counter(c - r for r, c in smp); kap.append(sum(1 for v in diag.values() if v == 2) / n)
    bycol = collections.defaultdict(list)
    for r, c in smp: bycol[c].append(r)
    pairs_c = collections.Counter(tuple(sorted(v)) for v in bycol.values()); rect.append(sum(v * (v - 1) // 2 for v in pairs_c.values()))
    for i in range(len(smp)):
        for j in range(i + 1, len(smp)):
            dc, dr = smp[j][1] - smp[i][1], smp[j][0] - smp[i][0]
            g = math.gcd(abs(dc), abs(dr)); a, b = dc // g, dr // g
            if a < 0 or (a == 0 and b < 0): a, b = -a, -b
            hist[(a, b)] += 1
meas = {d: v / len(samples) for d, v in hist.items()}
dirs = [d for d in meas if d not in ((1, 0), (0, 1))]
def tot_pairs(a, b):
    t = 0
    for x0 in range(n):
        for y0 in range(n):
            if 0 <= x0 - a < n and 0 <= y0 - b < n: continue
            L = 0; x, y = x0, y0
            while 0 <= x < n and 0 <= y < n: L += 1; x += a; y += b
            t += L * (L - 1) // 2
    return t
free_pairs = (2 * n) * (2 * n - 1) // 2 - 2 * n
tot = {d: tot_pairs(*d) for d in dirs}; p_occ = free_pairs / sum(tot.values())
lv = collections.defaultdict(lambda: [0.0, 0.0])
for d in dirs:
    m = max(abs(d[0]), abs(d[1])); lv[m][0] += meas[d]; lv[m][1] += tot[d] * p_occ
obs20 = {1: 0.577, 2: 0.748, 3: 0.917, 4: 1.085 * 1.0486 / 1.0486, 5: 1.161, 6: 1.161, 7: 1.175, 8: 1.137, 9: 1.128, 10: 1.096, 11: 1.130, 12: 1.091}
# измеренные при n=20 в правильном нуле: m=1..3 из spectrum_checks; m>=4 — из dirratio, пересчитанные на правильный нуль (×1/1.0486)
obs = {1: 0.577, 2: 0.748, 3: 0.917}
for m in range(4, 13): obs[m] = {4: 1.085, 5: 1.161, 6: 1.161, 7: 1.175, 8: 1.137, 9: 1.128, 10: 1.096, 11: 1.130, 12: 1.091}[m] / 1.0486
print(f"n={n} λ={lam} выборок {len(samples)} принято {acc/max(tries,1):.3f} ⟨E⟩≈{E}; κ = {sum(kap)/len(kap):.4f}; прямоугольников {sum(rect)/len(rect):.3f}")
print(f"{'m':>3} {'модель':>8} {'решения':>8} {'разница':>8}")
err = []
for m in sorted(lv):
    if m > 12: break
    r = lv[m][0] / lv[m][1]; err.append(((r - obs[m]) ** 2, lv[m][1]))
    print(f"{m:>3} {r:>8.3f} {obs[m]:>8.3f} {r-obs[m]:>+8.3f}")
rms = math.sqrt(sum(e * w for e, w in err) / sum(w for _, w in err))
print(f"взвешенный RMS по уровням m=1..12: {rms:.3f}")
