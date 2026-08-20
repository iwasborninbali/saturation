"""verdict_classes.py — ЕДИНСТВЕННЫЙ источник ответа об исчерпывающем подсчёте по орбитам профилей.

Написано по правилу, к которому мы пришли за день: не «проверяй результат», а сделай так, чтобы
непроверенный результат было негде взять. Поэтому здесь нет режима «покажи, сколько уже есть»:
скрипт либо выдаёт вердикт, либо отказывает и объясняет, чего не хватает. Частичное число из него
получить нельзя — именно затем, что частичное число выглядит как ответ.

Проверяется:
  1) присутствуют ВСЕ представители орбит, ни одного оборванного;
  2) взвешенная сумма (число конфигураций у представителя × размер орбиты) — это полное число
     помеченных конфигураций;
  3) классы под 48 симметриями куба считаются по объединению выводов представителей. Это законно:
     если у конфигурации пара профилей лежит в орбите представителя, то симметрия переносит саму
     конфигурацию в кусок представителя, а канонизация под полной группой возвращает её в тот же
     класс. Поэтому представители дают ВСЕ классы, а не часть;
  4) контрольная сумма sum(48/|стабилизатор|) обязана совпасть со взвешенной суммой — иначе где-то
     потеря или двойной счёт.

    python3 verdict_classes.py n M orbits.txt repdir
"""
import os, sys
from itertools import permutations, product

n, M, orbfile, repdir = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3], sys.argv[4]
m = n - 1
G = [(p, s) for p in permutations(range(3)) for s in product((0, 1), repeat=3)]


def ap(g, q):
    p, s = g
    return tuple((m - q[p[k]]) if s[k] else q[p[k]] for k in range(3))


def canon(S):
    return min(tuple(sorted(ap(g, q) for q in S)) for g in G)


orbs = [ln.split() for ln in open(orbfile) if ln.strip()]
missing, aborted, weighted, configs = [], [], 0, []
for i, (a, b, w) in enumerate(orbs, start=1):
    path = os.path.join(repdir, f"rep{i}.txt")
    if not os.path.exists(path):
        missing.append(i); continue
    lines = open(path).read().splitlines()
    tail = [l for l in lines if l.startswith(f"n={n} M={M}")]
    if not tail:
        aborted.append(i); continue
    cnt = int(tail[-1].split("конфигураций ")[1].split()[0])
    weighted += cnt * int(w)
    for l in lines:
        if l.startswith("НАЙДЕНО:"):
            pts = [tuple(int(v) for v in t.split(",")) for t in l.split("НАЙДЕНО:")[1].split()]
            configs.append(pts)

print(f"n={n} M={M}: орбит {len(orbs)}, представителей на месте {len(orbs)-len(missing)}")
if missing or aborted:
    print(f"  ОТКАЗ: не хватает представителей {missing[:6]}, оборвано {aborted[:6]}")
    print("  Вердикта нет. Частичное число не выдаётся намеренно: оно неотличимо от ответа.")
    sys.exit(1)

cls = {}
for S in configs:
    cls.setdefault(canon(S), 0)
    cls[canon(S)] += 1
check = 0
for key in cls:
    imgs = len({tuple(sorted(ap(g, q) for q in key)) for g in G})
    check += imgs
print(f"  помеченных конфигураций (взвешенная сумма): {weighted}")
print(f"  найдено представителями напрямую: {len(configs)}")
print(f"  КЛАССОВ под 48 симметриями: {len(cls)}")
print(f"  контроль sum(48/|стаб|) = {check} против взвешенной суммы {weighted}: "
      f"{'СХОДИТСЯ' if check == weighted else 'НЕ СХОДИТСЯ — где-то потеря или двойной счёт'}")
sys.exit(0 if check == weighted else 2)
