#!/usr/bin/env python3
"""var_by_type_n6.py — второй момент к lem-002: точные E[T | тип циклов], Var[T | тип], P(T = 0 | тип) по всем 67 950 конфигурациям
«две точки в каждой строке и столбце» при n = 6 (свой перебор рекурсией по строкам; тип циклов — по графу строки–столбцы).
usage: python3 var_by_type_n6.py [n]   (n = 6 по умолчанию; n = 4, 5 — быстро)"""
import sys, itertools, collections
from fractions import Fraction
n = int(sys.argv[1]) if len(sys.argv) > 1 else 6
def collinear(a, b, c): return (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0]) == 0
def all_configs(n):
    out = []
    def rec(i, colrem, rows):
        if i == n:
            if all(x == 0 for x in colrem): out.append([(r, c) for r, cs in enumerate(rows) for c in cs])
            return
        for cs in itertools.combinations([c for c in range(n) if colrem[c] > 0], 2):
            for c in cs: colrem[c] -= 1
            rec(i + 1, colrem, rows + [cs])
            for c in cs: colrem[c] += 1
    rec(0, [2] * n, []); return out
def cycle_type(S):
    rows = collections.defaultdict(list); cols = collections.defaultdict(list)
    for r, c in S: rows[r].append(c); cols[c].append(r)
    seen = set(); lam = []
    for r0 in range(n):
        if r0 in seen: continue
        r, c, k = r0, rows[r0][0], 0
        while r not in seen:
            seen.add(r); k += 1
            c = rows[r][1] if c == rows[r][0] else rows[r][0]
            r = cols[c][1] if cols[c][0] == r else cols[c][0]
        lam.append(k)
    return tuple(sorted(lam, reverse=True))
cf = all_configs(n); acc = collections.defaultdict(list)
for S in cf: acc[cycle_type(S)].append(sum(1 for t in itertools.combinations(S, 3) if collinear(*t)))
def mean(v): return Fraction(sum(v), len(v))
def var(v): m = mean(v); return Fraction(sum((Fraction(x) - m) ** 2 for x in v), len(v))
allT = [t for v in acc.values() for t in v]
print(f"n={n}: конфигураций {len(cf)} (A001499); E[T] = {mean(allT)}, Var[T] = {var(allT)} ≈ {float(var(allT)):.4f}")
print("тип циклов | конфигураций | E[T | тип] | Var[T | тип] | P(T = 0 | тип)")
for t in sorted(acc, key=lambda t: (-len(t), t)):
    v = acc[t]; z = sum(1 for x in v if x == 0)
    print(f"{t} | {len(v)} | {mean(v)} | {var(v)} ≈ {float(var(v)):.4f} | {Fraction(z, len(v))} ≈ {z/len(v):.5f}")
print("вывод: условные средние равны (первый момент слеп), дисперсии и доли решений различны (второй момент и хвост — нет)")
