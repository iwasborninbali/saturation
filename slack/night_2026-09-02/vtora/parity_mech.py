#!/usr/bin/env python3
"""parity_mech.py — баланс по классам чётности (и mod 3) как первомоментный эффект.

Нуль: равномерная конфигурация 2/строку+2/столбец, n×n — выборка пар перестановок (a,b), a≠b поточечно, с весом 2^{−c}
(c — число циклов 2-фактора), что даёт равномерность по конфигурациям. Для каждой: T — число коллинеарных троек,
k — число точек в классе (чётная строка, чётный столбец), D3 — дисперсия Пирсона Σ(k_ij − E_ij)²/E_ij по 3×3 таблице классов mod 3.
Механизм: P(T=0 | профиль) ≈ exp(−E[T | профиль]); тогда профиль у решений ∝ P_null(профиль)·exp(−E[T|профиль]).
Сравнение — с iden-решениями базы (k: дисперсия и P(k=10); D3: среднее).
usage: python3 parity_mech.py n samples seed
"""
import sys, math, random, collections
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from cycle_null import collinear_triples
ALPHA = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz#$%&@?!()[]<>{}=*+|-/~^_:;,."
IDX = {c: i for i, c in enumerate(ALPHA)}
DB = "/Users/iwasborninbali/saturation/web/all_known_solutions"

def cycles_of_pair(a, b, n):
    # π = b⁻¹a на строках
    binv = [0] * n
    for r in range(n): binv[b[r]] = r
    seen = [False] * n; c = 0
    for r0 in range(n):
        if seen[r0]: continue
        c += 1; r = r0
        while not seen[r]: seen[r] = True; r = binv[a[r]]
    return c

def profile(pts, n):
    k = sum(1 for r, c in pts if r % 2 == 0 and c % 2 == 0)
    R = [sum(1 for r in range(n) if r % 3 == i) for i in range(3)]; C = R[:]
    tab = [[0] * 3 for _ in range(3)]
    for r, c in pts: tab[r % 3][c % 3] += 1
    D3 = sum((tab[i][j] - 2 * R[i] * C[j] / n) ** 2 / (2 * R[i] * C[j] / n) for i in range(3) for j in range(3))
    return k, D3

def null_sample(n, S, seed):
    rnd = random.Random(seed); rows = []
    for _ in range(S):
        while True:
            a = list(range(n)); rnd.shuffle(a); b = list(range(n)); rnd.shuffle(b)
            if all(x != y for x, y in zip(a, b)): break
        w = 2.0 ** (-cycles_of_pair(a, b, n))
        pts = sorted(set((r, a[r]) for r in range(n)) | set((r, b[r]) for r in range(n)))
        T = collinear_triples(pts); k, D3 = profile(pts, n)
        rows.append((w, T, k, D3))
    return rows

def solutions(n):
    out = []
    for l in open(DB):
        l = l.strip()
        if not l or (len(l) - 1) // 2 != n or l[0] != '.': continue
        body = l[1:]
        pts = [(r, IDX[body[2 * r + t]]) for r in range(n) for t in range(2)]
        out.append(profile(pts, n))
    return out

if __name__ == "__main__":
    n, S, seed = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    rows = null_sample(n, S, seed)
    W = sum(w for w, *_ in rows)
    # --- mod 2 ---
    byk = collections.defaultdict(lambda: [0.0, 0.0, 0.0])   # w, wT, wT²
    for w, T, k, _ in rows:
        byk[k][0] += w; byk[k][1] += w * T; byk[k][2] += w * T * T
    print(f"n={n}, нуль: {S} выборок (взвешены 2^−c). k = точек в классе (чётн.,чётн.)")
    print(f"{'k':>3} {'P_null':>7} {'E[T|k]':>8} {'±SE':>5} {'наклон e^-(ΔE)':>15} {'P_pred':>7}")
    ks = sorted(byk); Pn = {k: byk[k][0] / W for k in ks}; ET = {k: byk[k][1] / byk[k][0] for k in ks}
    SE = {k: math.sqrt(max(byk[k][2] / byk[k][0] - ET[k] ** 2, 0) / max(byk[k][0] * S / W, 1)) for k in ks}
    Emin = min(ET[k] for k in ks if Pn[k] > 0.01)
    tilt = {k: Pn[k] * math.exp(-(ET[k] - Emin)) for k in ks}; Z = sum(tilt.values()); Pp = {k: tilt[k] / Z for k in ks}
    for k in ks:
        print(f"{k:>3} {Pn[k]:7.4f} {ET[k]:8.3f} {SE[k]:5.2f} {math.exp(-(ET[k]-Emin)):15.4f} {Pp[k]:7.4f}")
    mn = sum(k * Pn[k] for k in ks); vn = sum((k - mn) ** 2 * Pn[k] for k in ks)
    mp = sum(k * Pp[k] for k in ks); vp = sum((k - mp) ** 2 * Pp[k] for k in ks)
    print(f"дисперсия k: нуль {vn:.3f}; предсказание наклона {vp:.3f}; P_pred(k={n//2}) = {Pp.get(n//2, 0):.3f}")
    # --- mod 3 ---
    byD = collections.defaultdict(lambda: [0.0, 0.0])
    for w, T, _, D3 in rows:
        b = round(D3 * 2) / 2; byD[b][0] += w; byD[b][1] += w * T
    Dn = sum(w * D3 for w, _, _, D3 in rows) / W
    bins = sorted(byD); PD = {b: byD[b][0] / W for b in bins}; ETD = {b: byD[b][1] / byD[b][0] for b in bins}
    Emin3 = min(ETD[b] for b in bins if PD[b] > 0.01)
    tilt3 = {b: PD[b] * math.exp(-(ETD[b] - Emin3)) for b in bins}; Z3 = sum(tilt3.values())
    Dp = sum(b * tilt3[b] / Z3 for b in bins)
    print(f"\nmod 3: D3 = Σ(k_ij − E_ij)²/E_ij; нуль: среднее {Dn:.3f}; предсказание наклона {Dp:.3f} (отношение {Dp/Dn:.3f})")
    print("  E[T | D3] по корзинам (D3 округлён до 0.5): " + " ".join(f"{b}:{ETD[b]:.2f}(P={PD[b]:.3f})" for b in bins if PD[b] > 0.005))
    # --- решения ---
    sol = solutions(n)
    if sol:
        ksol = collections.Counter(k for k, _ in sol); m = len(sol)
        ms = sum(k for k, _ in sol) / m; vs = sum((k - ms) ** 2 for k, _ in sol) / m
        Ds = sum(d for _, d in sol) / m
        print(f"\nрешения iden n={n}: {m}; дисперсия k {vs:.3f}, P(k={n//2}) = {ksol[n//2]/m:.3f}; среднее D3 {Ds:.3f} (отношение к нулю {Ds/Dn:.3f})")
        print("  распределение k у решений: " + " ".join(f"{k}:{v/m:.3f}" for k, v in sorted(ksol.items())))
        hist = collections.Counter(round(d * 2) / 2 for _, d in sol)
        print("  распределение D3 у решений: " + " ".join(f"{b}:{v/m:.3f}" for b, v in sorted(hist.items()) if v / m >= 0.005))
