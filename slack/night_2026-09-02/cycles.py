#!/usr/bin/env python3
"""Циклы 2-фактора: решение = 2 точки в строке и в столбце = 2-регулярный двудольный граф строки-столбцы = объединение циклов.
k-цикл = k строк и k столбцов. «Дефектное семейство» фиксирует короткий цикл; его покрытие = доля решений, содержащих такой цикл.
Считаем по классам и сравниваем со случайными 2-регулярными графами."""
import sys, collections, random
ALPHA = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz#$%&@?!()[]<>{}=*+|-/~^_:;,."
IDX = {c: i for i, c in enumerate(ALPHA)}
CLS = {'.': 'iden', ':': 'rot2', '/': 'dia1', '-': 'ort1', 'o': 'rot4', 'c': 'rct4', 'x': 'dia2', '+': 'ort2', '*': 'full'}

def cycles_of(rows):
    """rows[r] = (c1, c2); возвращает список длин циклов (в строках)"""
    n = len(rows); col_rows = collections.defaultdict(list)
    for r, (a, b) in enumerate(rows):
        col_rows[a].append(r); col_rows[b].append(r)
    seen = [False] * n; out = []
    for r0 in range(n):
        if seen[r0]: continue
        # идём по циклу: строка -> столбец (первый неиспользованный) -> другая строка ...
        length = 0; r = r0; c = rows[r][0]; prev_c = None
        while not seen[r]:
            seen[r] = True; length += 1
            a, b = rows[r]
            c = b if c == a else a           # выйти через другой столбец
            rs = col_rows[c]; r = rs[1] if rs[0] == r else rs[0]
        out.append(length)
    return out

def stats(items):
    n_ = len(items); shortest = collections.Counter(min(c) for c in items)
    has2 = sum(1 for c in items if 2 in c) / n_; has3 = sum(1 for c in items if 3 in c) / n_
    le4 = sum(1 for c in items if min(c) <= 4) / n_; ham = sum(1 for c in items if len(c) == 1) / n_
    return has2, has3, le4, ham, shortest

by = collections.defaultdict(list)
for l in open(sys.argv[1]):
    l = l.strip()
    if not l: continue
    n = (len(l) - 1) // 2; body = l[1:]
    rows = [(IDX[body[2 * r]], IDX[body[2 * r + 1]]) for r in range(n)]
    by[(n, CLS[l[0]])].append(cycles_of(rows))
print(f"{'n':>3} {'класс':>5} {'решений':>8} {'есть 2-цикл':>11} {'есть 3-цикл':>11} {'кратч.<=4':>10} {'один цикл':>10}   кратчайший цикл: распределение")
want = [(20, 'iden'), (20, 'rot2'), (31, 'rot2'), (30, 'dia1'), (31, 'dia1'), (32, 'dia1'), (44, 'rot4'), (56, 'rot4'), (45, 'rct4'), (57, 'rct4'), (31, 'iden'), (29, 'iden')]
for key in want:
    if key not in by: continue
    has2, has3, le4, ham, sh = stats(by[key])
    dist = " ".join(f"{k}:{v/len(by[key]):.2f}" for k, v in sorted(sh.items())[:6])
    print(f"{key[0]:>3} {key[1]:>5} {len(by[key]):>8} {has2:>11.3f} {has3:>11.3f} {le4:>10.3f} {ham:>10.3f}   {dist}")
# нуль: случайные 2-регулярные двудольные графы (объединение двух непересекающихся перестановок)
random.seed(1)
for n in (20, 31, 44):
    items = []
    while len(items) < 20000:
        p1 = list(range(n)); random.shuffle(p1); p2 = list(range(n)); random.shuffle(p2)
        if all(a != b for a, b in zip(p1, p2)): items.append(cycles_of(list(zip(p1, p2))))
    has2, has3, le4, ham, sh = stats(items)
    dist = " ".join(f"{k}:{v/len(items):.2f}" for k, v in sorted(sh.items())[:6])
    print(f"{n:>3} {'НУЛЬ':>5} {len(items):>8} {has2:>11.3f} {has3:>11.3f} {le4:>10.3f} {ham:>10.3f}   {dist}")
