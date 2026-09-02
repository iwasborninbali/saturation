#!/usr/bin/env python3
"""cycle_census.py — перепись циклов 2-фактора строки–столбцы по базе Фламменкампа (web/all_known_solutions),
своим парсером (cycles.py дня не читается как код: второй счёт), против ДВУХ нулей из cycle_null.py:
P_ab — равномерная пара перестановок (нуль дня), P_conf — равномерная конфигурация (правильный).
Цикл ищется обходом двудольного графа: строка → столбец → другая строка того же столбца → другой столбец той же строки …
usage: python3 cycle_census.py [n_min n_max] [класс …]     (по умолчанию 8 20 и все классы; iden сравнивается с нулями)
"""
import sys, math, collections
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from cycle_null import nulls, weights
ALPHA = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz#$%&@?!()[]<>{}=*+|-/~^_:;,."
IDX = {c: i for i, c in enumerate(ALPHA)}
CLS = {'.': 'iden', ':': 'rot2', '/': 'dia1', '-': 'ort1', 'o': 'rot4', 'c': 'rct4', 'x': 'dia2', '+': 'ort2', '*': 'full'}
DB = "/Users/iwasborninbali/saturation/web/all_known_solutions"

def cycle_type(rows):
    """rows[r] = [c1, c2]; возвращает отсортированный кортеж длин циклов (в строках)."""
    n = len(rows); col_rows = collections.defaultdict(list)
    for r, cs in enumerate(rows):
        for c in cs: col_rows[c].append(r)
    assert all(len(v) == 2 for v in col_rows.values()), "не 2 в столбце"
    seen = [False] * n; lam = []
    for r0 in range(n):
        if seen[r0]: continue
        r, c, k = r0, rows[r0][0], 0
        while not seen[r]:
            seen[r] = True; k += 1
            c = rows[r][1] if c == rows[r][0] else rows[r][0]       # выйти через другой столбец
            rr = col_rows[c]; r = rr[1] if rr[0] == r else rr[0]     # и в другую строку этого столбца
        lam.append(k)
    assert sum(lam) == n and min(lam) >= 2
    return tuple(sorted(lam, reverse=True))

def main():
    a = sys.argv[1:]
    n_min, n_max = (int(a[0]), int(a[1])) if len(a) >= 2 and a[0].isdigit() else (8, 20)
    classes = [x for x in a if not x.isdigit()] or list(CLS.values())
    by = collections.defaultdict(collections.Counter)
    for l in open(DB):
        l = l.strip()
        if not l: continue
        n = (len(l) - 1) // 2
        if n < n_min or n > n_max: continue
        cls = CLS[l[0]]
        if cls not in classes: continue
        body = l[1:]
        rows = [[IDX[body[2 * r]], IDX[body[2 * r + 1]]] for r in range(n)]
        by[(n, cls)][cycle_type(rows)] += 1
    print(f"{'n':>3} {'класс':>5} {'решений':>8} | {'гам':>6} {'P_conf':>6} {'P_ab':>6} | {'2цикл':>6} {'P_conf':>6} {'P_ab':>6} | {'3цикл':>6} {'P_conf':>6} | {'ср.c':>5} {'нуль':>5}  распределение c у решений")
    nl = {}
    for (n, cls), cnt in sorted(by.items()):
        tot = sum(cnt.values())
        if n not in nl: nl[n] = nulls(n)
        r = nl[n]
        ham = cnt[(n,)] / tot
        has2 = sum(v for lam, v in cnt.items() if 2 in lam) / tot
        has3 = sum(v for lam, v in cnt.items() if 3 in lam) / tot
        meanc = sum(len(lam) * v for lam, v in cnt.items()) / tot
        nullc = sum(float(c) * float(p) for c, p in r["conf_cycles"].items())
        cd = collections.Counter()
        for lam, v in cnt.items(): cd[len(lam)] += v
        dist = " ".join(f"{c}:{cd[c]/tot:.3f}" for c in sorted(cd))
        print(f"{n:>3} {cls:>5} {tot:>8} | {ham:6.3f} {float(r['conf_ham']):6.3f} {float(r['ab_ham']):6.3f} | {has2:6.3f} {float(r['conf_has2']):6.3f} {float(r['ab_has2']):6.3f} | {has3:6.3f} {float(r['conf_has3']):6.3f} | {meanc:5.2f} {nullc:5.2f}  {dist}")
    # обогащение по типам с двумя циклами при максимальном n класса iden: (k, n−k), k=2..n/2
    key = (n_max, 'iden')
    if key in by:
        cnt = by[key]; tot = sum(cnt.values()); W = weights(n_max); Zc = sum(w for _, w in W.values())
        print(f"\nобогащение E(λ) = P(λ | решение)/P_conf(λ), iden, n={n_max}, типы с двумя циклами (k, n−k):")
        for k in range(2, n_max // 2 + 1):
            lam = (n_max - k, k); p_sol = cnt[lam] / tot; p_null = float(W[lam][1] / Zc)
            se = math.sqrt(max(cnt[lam], 1)) / tot
            print(f"  λ=({n_max - k},{k}): решений {cnt[lam]:>6}  P_sol={p_sol:.4f}±{se:.4f}  P_conf={p_null:.4f}  E={p_sol / p_null:.3f}")
        print(f"  гамильтонов ({n_max}): решений {cnt[(n_max,)]:>6}  P_sol={cnt[(n_max,)]/tot:.4f}  P_conf={float(W[(n_max,)][1]/Zc):.4f}  E={cnt[(n_max,)]/tot/float(W[(n_max,)][1]/Zc):.3f}")
        print(f"  типы с тремя циклами, содержащие 2-цикл, против без него:")
        c3 = [(lam, v) for lam, v in cnt.items() if len(lam) == 3]
        for has in (True, False):
            ps = sum(v for lam, v in c3 if (2 in lam) == has) / tot
            pn = float(sum(W[lam][1] for lam in W if len(lam) == 3 and (2 in lam) == has) / Zc)
            print(f"    {'с 2-циклом' if has else 'без 2-цикла'}: P_sol={ps:.4f}  P_conf={pn:.4f}  E={ps/pn if pn else float('nan'):.3f}")

if __name__ == "__main__":
    main()
