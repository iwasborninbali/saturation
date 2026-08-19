"""classify_orbits.py — разложение помеченных конфигураций на классы под 48 симметриями куба.
Своя реализация группы и канонизации; сверяется контрольная сумма sum(48/|стабилизатор|) = число помеченных.
    python3 classify_orbits.py n dumpfile
"""
import sys
from collections import Counter
from itertools import permutations, product

n = int(sys.argv[1]); m = n - 1
G = []
for perm in permutations(range(3)):
    for sg in product((0, 1), repeat=3):
        G.append((perm, sg))


def apply(g, p):
    perm, sg = g
    return tuple((m - p[perm[k]]) if sg[k] else p[perm[k]] for k in range(3))


def canon(S):
    return min(tuple(sorted(apply(g, p) for p in S)) for g in G)


classes = {}
tot = 0
for ln in open(sys.argv[2]):
    t = ln.split()
    if len(t) < 3: continue
    S = [tuple(int(t[3*i+k]) for k in range(3)) for i in range(len(t)//3)]
    tot += 1
    classes.setdefault(canon(S), []).append(1)
stab = Counter()
for key in classes:
    imgs = len({tuple(sorted(apply(g, p) for p in key)) for g in G})
    stab[48 // imgs] += 1
check = sum(cnt * (48 // s) for s, cnt in stab.items())
print(f"n={n}: помеченных {tot}, классов {len(classes)}")
print(f"  стабилизаторы: {dict(sorted(stab.items()))}, контроль sum(48/|стаб|) = {check}"
      f" -> {'сходится' if check == tot else 'НЕ СХОДИТСЯ'}")
