#!/usr/bin/env python3
"""rect_shapes.py — разведка после проигрыша ставки о форме прямоугольников: полная таблица обогащения E(Δr, Δc),
мультипликативная модель log E ≈ f(Δr) + f(Δc) и остатки по gcd, и распределение точек решений по классам чётности
(r mod 2, c mod 2) против нуля — не является ли обогащение чётных форм следствием расслоения по чётности.
usage: python3 rect_shapes.py [n] [класс]
"""
import sys, math, collections, itertools
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from cycle_null import weights
ALPHA = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz#$%&@?!()[]<>{}=*+|-/~^_:;,."
IDX = {c: i for i, c in enumerate(ALPHA)}
CLS = {'.': 'iden', ':': 'rot2', '/': 'dia1', '-': 'ort1', 'o': 'rot4', 'c': 'rct4', 'x': 'dia2', '+': 'ort2', '*': 'full'}
DB = "/Users/iwasborninbali/saturation/web/all_known_solutions"
n = int(sys.argv[1]) if len(sys.argv) > 1 else 20
cls = sys.argv[2] if len(sys.argv) > 2 else 'iden'
W = weights(n); Zc = sum(w for _, w in W.values())
E_m2 = float(sum(lam.count(2) * w for lam, (_, w) in W.items()) / Zc)
p_delta = {d: 2 * (n - d) / (n * (n - 1)) for d in range(1, n)}

sols = 0; shapes = collections.Counter(); parity = collections.Counter(); par_hist = collections.Counter()
for l in open(DB):
    l = l.strip()
    if not l or (len(l) - 1) // 2 != n or CLS[l[0]] != cls: continue
    body = l[1:]; sols += 1
    rows = [(IDX[body[2 * r]], IDX[body[2 * r + 1]]) for r in range(n)]
    seen = collections.defaultdict(list)
    for r, cs in enumerate(rows): seen[frozenset(cs)].append(r)
    for cs, rs in seen.items():
        if len(rs) == 2:
            c1, c2 = sorted(cs); a, b = rs[1] - rs[0], c2 - c1
            shapes[(a, b)] += 1
    ee = sum(1 for r in range(n) for c in rows[r] if r % 2 == 0 and c % 2 == 0)
    par_hist[ee] += 1
# таблица E(Δr, Δc) (симметризована: класс {(a,b),(b,a)})
E = {}
for a in range(1, n):
    for b in range(1, n):
        obs = shapes[(a, b)] / sols
        E[(a, b)] = obs / (E_m2 * p_delta[a] * p_delta[b])
print(f"n={n} {cls}: решений {sols}; E(Δr,Δc) = наблюдаемое/нуль, строки Δr, столбцы Δc (пусто = < 5 прямоугольников)")
print("     " + " ".join(f"{b:>4}" for b in range(1, n)))
for a in range(1, n):
    print(f"{a:>3}: " + " ".join((f"{E[(a,b)]:4.1f}" if shapes[(a, b)] >= 5 else "   .") for b in range(1, n)))
# мультипликативная модель: log E(a,b) = f(a) + f(b), подгонка МНК по симметризованным классам с весами
import numpy as np
pairs = [(a, b) for a in range(1, n) for b in range(a, n) if shapes[(a, b)] + shapes[(b, a)] >= 10]
y = []; X = []; wts = []
for a, b in pairs:
    cnt = shapes[(a, b)] + shapes[(b, a)]; pn = p_delta[a] * p_delta[b] * (2 if a != b else 1)
    y.append(math.log(cnt / sols / (E_m2 * pn))); row = np.zeros(n - 1); row[a - 1] += 1; row[b - 1] += 1; X.append(row); wts.append(cnt)
X = np.array(X); y = np.array(y); wts = np.sqrt(np.array(wts, float))
f, *_ = np.linalg.lstsq(X * wts[:, None], y * wts, rcond=None)
res = y - X @ f
print("\nмультипликативная модель log E = f(Δr) + f(Δc): f по Δ:")
print("  " + " ".join(f"{d}:{math.exp(f[d-1]):.2f}" for d in range(1, n)))
by_g = collections.defaultdict(list)
for (a, b), r in zip(pairs, res): by_g[math.gcd(a, b)].append(r)
print("  остатки exp(mean) по gcd(Δr,Δc): " + " ".join(f"g={g}:{math.exp(np.mean(v)):.2f}(n={len(v)})" for g, v in sorted(by_g.items())))
by_par = collections.defaultdict(list)
for (a, b), r in zip(pairs, res): by_par[(a % 2, b % 2)].append(r)
print("  остатки по чётности (Δr%2,Δc%2): " + " ".join(f"{k}:{math.exp(np.mean(v)):.2f}(n={len(v)})" for k, v in sorted(by_par.items())))
print(f"  RMS остатков {math.sqrt(np.mean(res**2)):.3f} (в log), размах наблюдаемого log E: {y.min():.2f}…{y.max():.2f}")
# чётность: число точек в чётных строках и чётных столбцах
print("\nчисло точек в клетках (чётная строка, чётный столбец) — гистограмма у решений (нуль: гипергеометрическое около 10 при n=20):")
print("  " + " ".join(f"{k}:{v/sols:.3f}" for k, v in sorted(par_hist.items())))
mean = sum(k * v for k, v in par_hist.items()) / sols; var = sum((k - mean) ** 2 * v for k, v in par_hist.items()) / sols
print(f"  среднее {mean:.3f}, дисперсия {var:.3f}")
