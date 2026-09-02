#!/usr/bin/env python3
"""Стримлайнер по простым расстояниям на больших n по классам симметрии (rot4/rct4/rot2): ρ(k) строк по k и выживаемость.
usage: streamliner_classes.py all_known_solutions"""
import sys, collections, math
import numpy as np
ALPHA = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz#$%&@?!()[]<>{}=*+|-/~^_:;,."
IDX = {c: i for i, c in enumerate(ALPHA)}
CLS = {'.': 'iden', ':': 'rot2', '/': 'dia1', '-': 'ort1', 'o': 'rot4', 'c': 'rct4', 'x': 'dia2', '+': 'ort2', '*': 'full'}
by = collections.defaultdict(list)
for l in open(sys.argv[1]):
    l = l.strip()
    if l: by[((len(l) - 1) // 2, CLS[l[0]])].append(l)
def primes(lo, hi): return [q for q in range(lo, hi + 1) if all(q % d for d in range(2, int(q ** 0.5) + 1))]
print("ρ_row(k) = доля пар строк на расстоянии k у решений / та же доля у равномерного нуля ((n−k)/C(n,2))")
for key in [(31, 'rot2'), (40, 'rot4'), (44, 'rot4'), (50, 'rot4'), (56, 'rot4'), (45, 'rct4'), (53, 'rct4'), (57, 'rct4')]:
    if key not in by: continue
    n, cls = key; L = by[key]
    cnt = collections.Counter()
    for l in L:
        b = l[1:]
        for i in range(n): cnt[abs(IDX[b[2 * i]] - IDX[b[2 * i + 1]])] += 1
    tot = sum(cnt.values())
    rho = {k: (cnt[k] / tot) / ((n - k) / (n * (n - 1) / 2)) for k in range(1, n)}
    pr = primes(7, n - 1)
    line = " ".join(f"{k}:{rho[k]:.2f}" for k in list(range(2, 13)) + [15, 18])
    prl = " ".join(f"{k}:{rho[k]:.2f}" for k in pr[:12])
    F = set(pr)
    allowed = sum(n - d for d in range(1, n) if d not in F) / (n * (n - 1) / 2)
    surv = np.mean([all(abs(IDX[l[1:][2 * i]] - IDX[l[1:][2 * i + 1]]) not in F for i in range(n)) for l in L])
    Fh = set(p for p in pr if p <= n // 2)
    allowed_h = sum(n - d for d in range(1, n) if d not in Fh) / (n * (n - 1) / 2)
    surv_h = np.mean([all(abs(IDX[l[1:][2 * i]] - IDX[l[1:][2 * i + 1]]) not in Fh for i in range(n)) for l in L])
    print(f"\nn={n} {cls} ({len(L)} решений)\n  ρ(k), k=2..12,15,18: {line}\n  ρ(простые ≥7): {prl}")
    print(f"  F=все простые 7..{n-1}: разрешено {allowed:.3f}/строку, пространство {allowed**n:.1e}, выжило {surv:.3f}, выигрыш ×{surv/allowed**n:.3g}")
    print(f"  F=простые 7..{n//2}:   разрешено {allowed_h:.3f}/строку, пространство {allowed_h**n:.1e}, выжило {surv_h:.3f}, выигрыш ×{surv_h/allowed_h**n:.3g}")
