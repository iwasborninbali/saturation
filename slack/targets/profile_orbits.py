"""profile_orbits.py — сокращение разбиения по парам профилей до орбит.

Пары (профиль по x, профиль по y) связаны симметриями куба, сохраняющими ось z и множество {x,y}:
отражение по x, отражение по y, перестановка x и y — группа порядка 8. Симметрия — биекция на
конфигурациях, поэтому число конфигураций у пар одной орбиты ОДИНАКОВО. Значит считать надо один
представитель на орбиту, а не все пары.

Утверждение проверяемо, и проверять его надо числом, а не рассуждением: (1) внутри каждой орбиты
все посчитанные числа обязаны совпасть; (2) сумма «представитель × размер орбиты» обязана дать
общее число. Обе проверки делает режим --check по готовому файлу результатов.

    python3 profile_orbits.py n M            -> печатает представителей и размеры орбит
    python3 profile_orbits.py n M --check f  -> сверяет орбиты по файлу результатов
"""
import sys
from itertools import product


def profiles(n, M, cap=3):
    return [p for p in product(range(cap + 1), repeat=n) if sum(p) == M]


def orbit(a, b):
    ra, rb = a[::-1], b[::-1]
    return frozenset({(a, b), (ra, b), (a, rb), (ra, rb), (b, a), (rb, a), (b, ra), (rb, ra)})


n, M = int(sys.argv[1]), int(sys.argv[2])
P = profiles(n, M)
seen, orbs = set(), []
for a in P:
    for b in P:
        if (a, b) in seen: continue
        o = orbit(a, b)
        o = frozenset(x for x in o if x[0] in P and x[1] in P)
        seen |= set(o)
        orbs.append(sorted(o))

if "--check" in sys.argv:
    res = {}
    for ln in open(sys.argv[sys.argv.index("--check") + 1]):
        if "конфигураций" not in ln: continue
        head, tail = ln.split(":")[0], ln.split("конфигураций ")[1]
        a = tuple(int(v) for v in head.split("P0=")[1].split()[0].split(","))
        b = tuple(int(v) for v in head.split("P1=")[1].split()[0].split(","))
        res[(a, b)] = int(tail.split()[0])
    bad, tot = [], 0
    for o in orbs:
        vals = {res[x] for x in o if x in res}
        if len(vals) > 1: bad.append((o[0], sorted(vals)))
        v = next(iter(vals)) if vals else None
        if v is not None: tot += v * len(o)
    print(f"n={n} M={M}: пар {len(seen)}, орбит {len(orbs)}, сокращение в {len(seen)/len(orbs):.1f} раз")
    print(f"  орбит с РАЗНЫМИ числами внутри: {len(bad)}  {bad[:2]}")
    print(f"  сумма представитель*размер: {tot}")
else:
    print(f"# n={n} M={M}: пар {len(seen)}, орбит {len(orbs)}", file=sys.stderr)
    for o in orbs:
        a, b = o[0]
        print(",".join(map(str, a)), ",".join(map(str, b)), len(o))
