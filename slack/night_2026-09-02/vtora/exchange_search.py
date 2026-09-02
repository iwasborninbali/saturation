#!/usr/bin/env python3
"""exchange_search.py — исчерпывающий j-обмен на свидетеле A399138 (куб, нет трёх коллинеарных) с κ-отсечением.

Лемма (цикл 2): удаление точки уменьшает κ(q) не больше чем на 1, поэтому после удаления множества R живыми становятся ровно
те пустые клетки q, у которых КАЖДАЯ убивающая пара пересекает R; в частности κ(q) ≤ |R|. Кандидаты — клетки с κ ≤ j, их мало.
Для каждого j-подмножества R точек: alive(R) → ищем j+1 попарно совместимых клеток (прямая через две новые не несёт третьей точки
S∖R и третьей новой). Найденная конфигурация проверяется полным перебором троек. Свидетель улучшаем j-обменом ⟺ найдено.
usage: python3 exchange_search.py J ФАЙЛ [ФАЙЛ …]     (формат файлов как в rigidity_kappa.py)
"""
import sys, math, itertools, collections, time
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from rigidity_kappa import read_cube_files, line_cells, all_cells

def cross_zero(a, b, c):
    u = [b[i] - a[i] for i in range(3)]; v = [c[i] - a[i] for i in range(3)]
    return u[1] * v[2] - u[2] * v[1] == 0 and u[2] * v[0] - u[0] * v[2] == 0 and u[0] * v[1] - u[1] * v[0] == 0

def killers(S, n):
    """для каждой пустой клетки — список убивающих пар (индексы точек)."""
    K = collections.defaultdict(list); Sset = set(S)
    for i in range(len(S)):
        for j in range(i + 1, len(S)):
            for c in line_cells(S[i], S[j], n, 3):
                if c not in Sset: K[c].append((i, j))
    return K

def search(name, S, n, J):
    t0 = time.time(); m = len(S); K = killers(S, n)
    empties = [c for c in all_cells(n, 3) if c not in set(S)]
    assert all(K[c] for c in empties), "не максимальна: есть живая клетка"
    kap = {c: len(K[c]) for c in empties}
    hist = collections.Counter(kap.values())
    print(f"{name}: n={n} m={m}, κ-гистограмма пустых {dict(sorted(hist.items())[:6])}")
    for j in range(1, J + 1):
        cand = [c for c in empties if kap[c] <= j]
        # для каждой клетки-кандидата — множество точек, участвующих в её убийцах; R должно пересекать каждую пару
        subsets = 0; rich = 0; improved = None; best_alive = 0
        for R in itertools.combinations(range(m), j):
            Rs = set(R); subsets += 1
            alive = [c for c in cand if all(a in Rs or b in Rs for a, b in K[c])]
            if len(alive) > best_alive: best_alive = len(alive)
            if len(alive) < j + 1: continue
            rich += 1
            rest = [S[i] for i in range(m) if i not in Rs]
            # попарная совместимость новых клеток между собой и с остатком
            def compatible(A):
                for x, y in itertools.combinations(A, 2):
                    for z in rest:
                        if cross_zero(x, y, z): return False
                for x, y, z in itertools.combinations(A, 3):
                    if cross_zero(x, y, z): return False
                return True
            for A in itertools.combinations(alive, j + 1):
                if compatible(A):
                    new = rest + list(A)
                    # полная проверка троек
                    bad = any(cross_zero(*t) for t in itertools.combinations(new, 3))
                    if not bad: improved = new; break
            if improved: break
        print(f"  j={j}: подмножеств {subsets}, кандидатов клеток (κ≤{j}) {len(cand)}, с живыми ≥ {j+1}: {rich} ({rich/subsets:.4%}), максимум живых {best_alive}; "
              + (f"УЛУЧШЕНИЕ до {len(improved)} точек!" if improved else "улучшения нет") + f"  [{time.time()-t0:.1f} с]")
        if improved:
            print("  НОВЫЙ СВИДЕТЕЛЬ:"); print("\n".join(f"{x} {y} {z}" for x, y, z in sorted(improved)))
            return improved
    return None

if __name__ == "__main__":
    J = int(sys.argv[1])
    for name, pts in read_cube_files(sys.argv[2:]):
        n = max(max(p) for p in pts) + 1
        if len(pts) < 60: continue
        search(name, pts, n, J)
