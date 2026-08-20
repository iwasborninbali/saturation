"""profile_orbits3.py — орбиты ТРОЕК профилей (по всем трём осям) под полной группой куба.

Тройку (профиль по x, по y, по z) группа куба переводит в тройку: перестановка осей переставляет
профили, отражение вдоль оси обращает свой профиль. Всего 48 образов. Конфигурации у троек одной
орбиты состоят в биекции, поэтому считать надо один представитель на орбиту.

Фиксировать все три профиля выгоднее, чем два: кусков больше, но каждый несравнимо жёстче, а
орбитальное сокращение съедает рост числа. При n=6, M=17: 216 троек, 10 орбит.

    python3 profile_orbits3.py n M            -> представители и веса
    python3 profile_orbits3.py n M --check f  -> сверка по файлу результатов (все тройки)
"""
import sys
from itertools import permutations, product


def profiles(n, M, cap=3):
    return [p for p in product(range(cap + 1), repeat=n) if sum(p) == M]


def images(t):
    out = set()
    for perm in permutations(range(3)):
        for sg in product((0, 1), repeat=3):
            out.add(tuple(t[perm[k]][::-1] if sg[k] else t[perm[k]] for k in range(3)))
    return out


n, M = int(sys.argv[1]), int(sys.argv[2])
P = set(profiles(n, M))
seen, orbs = set(), []
for t in product(sorted(P), repeat=3):
    if t in seen: continue
    o = sorted(x for x in images(t) if all(u in P for u in x))
    seen |= set(o); orbs.append(o)

if "--check" in sys.argv:
    res = {}
    for ln in open(sys.argv[sys.argv.index("--check") + 1]):
        if "конфигураций" not in ln: continue
        head = ln.split(":")[0]
        t = tuple(tuple(int(v) for v in head.split(f"P{i}=")[1].split()[0].split(",")) for i in range(3))
        res[t] = int(ln.split("конфигураций ")[1].split()[0])
    bad, tot = [], 0
    for o in orbs:
        vals = {res[x] for x in o if x in res}
        if len(vals) > 1: bad.append((o[0], sorted(vals)))
        if vals: tot += next(iter(vals)) * len(o)
    print(f"n={n} M={M}: троек {len(seen)}, орбит {len(orbs)}, сокращение в {len(seen)/len(orbs):.1f} раз")
    print(f"  орбит с РАЗНЫМИ числами внутри: {len(bad)}  {bad[:2]}")
    print(f"  взвешенная сумма: {tot}")
else:
    print(f"# n={n} M={M}: троек {len(seen)}, орбит {len(orbs)}", file=sys.stderr)
    for o in orbs:
        a, b, c = o[0]
        print(",".join(map(str, a)), ",".join(map(str, b)), ",".join(map(str, c)), len(o))
