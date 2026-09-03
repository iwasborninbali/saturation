#!/usr/bin/env python3
"""sym_rigid.py — жёсткость случайных СИММЕТРИЧНЫХ максимальных конфигураций A280537 как функция порядка группы (need-006, conj-006f).
Для каждого класса подгрупп H ⊂ O_h (нумерация классов c00…c32 — как у cube_strata.py коллеги; c00 — тривиальная группа) при данном n:
случайный орбитный рост (орбиты H в случайном порядке; орбита добавляется, если нет четырёх компланарных), затем достройка одиночными
точками до максимальности по включению (нарушает симметрию), затем жёсткость (после удаления любой точки допустима только она сама).
usage: python3 sym_rigid.py n runs seed [макс. порядок группы] [мин. порядок]   → строки: класс |H| прогонов средний размер (симм. стадия / итог) доля жёстких
"""
import sys, random, itertools, collections
sys.path.insert(0, __file__.rsplit('/', 1)[0] + '/..')
from cube_strata import all_matrices, subgroup_classes, orbits, IDENT
from kappa_general import coplanar, collinear

def has_coplanar4_with_new(S, new):
    """есть ли компланарная четвёрка в S ∪ new, содержащая хотя бы одну новую точку (S сама чиста)."""
    allp = S + new; ns = len(S)
    for i in range(ns, len(allp)):                 # новая точка с наименьшим индексом в четвёрке — среди новых
        for trip in itertools.combinations(range(len(allp)), 3):
            if trip[0] <= i and i in trip: continue
            if trip[0] > i or i in trip: continue
            if coplanar(allp[i], allp[trip[0]], allp[trip[1]], allp[trip[2]]): return True
    return False

def clean_add(S, new):
    """быстрее: проверяем все четвёрки с ≥1 новой точкой перебором троек из S∪new для каждой новой точки, без повторов."""
    allp = S + new; ns = len(S)
    for i in range(ns, len(allp)):
        others = allp[:i] + allp[i+1:]
        for a, b, c in itertools.combinations(others, 3):
            if coplanar(allp[i], a, b, c): return False
    return True

def grow(n, H, rnd):
    cells, idx, orb_of, orbs = orbits(H, n)
    order = list(range(len(orbs))); rnd.shuffle(order)
    S = []
    for k in order:
        O = orbs[k]
        if any(c in S for c in O): continue
        if clean_add(S, O): S = S + O
    sym_size = len(S)
    # достройка одиночными точками
    free = [c for c in cells if c not in S]; rnd.shuffle(free)
    changed = True
    while changed:
        changed = False
        for c in free:
            if c in S: continue
            if clean_add(S, [c]): S = S + [c]; changed = True
    return S, sym_size

def rigid(S, n):
    Sset = set(S); cells = [c for c in itertools.product(range(n), repeat=3) if c not in Sset]
    triples = list(itertools.combinations(S, 3))
    killers = {q: [t for t in triples if coplanar(q, *t)] for q in cells}
    if any(len(K) == 0 for K in killers.values()): return None      # не максимальна
    for q, K in killers.items():
        cnt = collections.Counter(p for t in K for p in t)
        if any(c == len(K) for c in cnt.values()): return False
    return True

if __name__ == "__main__":
    n, runs, seed = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]); maxord = int(sys.argv[4]) if len(sys.argv) > 4 else 8; minord = int(sys.argv[5]) if len(sys.argv) > 5 else 1
    G = all_matrices(); classes = subgroup_classes(G)
    rnd = random.Random(seed)
    print(f"# n={n}, runs={runs} на класс, seed={seed}; класс |H| прогонов | размер симм. стадии (мин–макс, среднее) | итог (мин–макс, среднее) | доля жёстких | жёстких среди чисто-симметричных (без достройки)")
    for ci, H in enumerate(classes):
        if len(H) > maxord or len(H) < minord: continue
        sizes = []; syms = []; rig = 0; pure = 0; pure_rig = 0; nonmax = 0
        for r in range(runs):
            S, ss = grow(n, H, rnd); v = rigid(S, n)
            if v is None: nonmax += 1; continue
            sizes.append(len(S)); syms.append(ss); rig += v
            if ss == len(S): pure += 1; pure_rig += v
        m = len(sizes)
        print(f"c{ci:02d} |H|={len(H):2d} прогонов {m:3d} | симм {min(syms)}–{max(syms)} ({sum(syms)/m:.1f}) | итог {min(sizes)}–{max(sizes)} ({sum(sizes)/m:.1f}) | жёстких {rig}/{m} = {rig/m:.2f} | чисто-симм {pure}, из них жёстких {pure_rig}" + (f" | немаксимальных {nonmax}" if nonmax else ""), flush=True)
