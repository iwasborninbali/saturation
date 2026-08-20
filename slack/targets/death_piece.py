"""death_piece.py — закрыть УПРЯМЫЙ кусок плоскостного перебора методом смерти.

ЗАЧЕМ. Опорный замер: 16.67% кусков не закрываются решателем за 600 с, и впереди их около
2800. Это не «дорого», а «не берётся»: маршрут оставляет хвост, которого сам не закрывает.
У такого куска УЖЕ зафиксированы все 49 переменных плоскости x=0 — значит поиску остаётся
мало, а отсечение по живым клеткам работает тем точнее, чем ближе к границе (измерено:
жёсткость держится на расстоянии <=1 от максимума и рассыпается на расстоянии двух).

ЧТО ДЕЛАЕТ. Берёт имя куска plx0_<индексы клеток>, кладёт эти клетки как уже рождённые,
вычёркивает остальные клетки плоскости x=0 (кусок говорит «в плоскости РОВНО эти»),
и ищет, можно ли дорастить до M. UNSAT здесь значит ровно то же, что UNSAT решателя.

ОТЛИЧИЕ ОТ РЕШАТЕЛЯ, из-за которого стоит пробовать: отсечение k + живых < M — это счётный
просмотр вперёд ПО ТЕКУЩЕМУ СОСТОЯНИЮ, а не постоянная клауза. Мы четырежды измерили, что
постоянные клаузы здесь не дают ничего.

usage: death_piece.py <имя-куска> [M] [предел-узлов]
"""
import sys
import time
from itertools import combinations

n = 7


def run(name, M=19, node_cap=None):
    N = n * n * n
    pts = [(x, y, z) for x in range(n) for y in range(n) for z in range(n)]
    index = {p: i for i, p in enumerate(pts)}
    cells0 = [(0, y, z) for y in range(n) for z in range(n)]

    if name.endswith("пусто"):
        fixed_idx = set()
    else:
        fixed_idx = {int(t) for t in name[5:].split("-")}
    fixed = [index[cells0[j]] for j in sorted(fixed_idx)]
    dead_plane = [index[cells0[j]] for j in range(49) if j not in fixed_idx]

    kill_pair = [[0] * N for _ in range(N)]
    for i in range(N):
        a = pts[i]
        for j in range(i + 1, N):
            b = pts[j]
            u = (b[0] - a[0], b[1] - a[1], b[2] - a[2])
            m = 0
            for k in range(N):
                if k == i or k == j:
                    continue
                c = pts[k]
                v = (c[0] - a[0], c[1] - a[1], c[2] - a[2])
                if (u[1] * v[2] - u[2] * v[1],
                        u[2] * v[0] - u[0] * v[2],
                        u[0] * v[1] - u[1] * v[0]) == (0, 0, 0):
                    m |= 1 << k
            kill_pair[i][j] = m
            kill_pair[j][i] = m

    cache = {}

    def kill_triple(i, j, k):
        key = (i, j, k) if i < j < k else tuple(sorted((i, j, k)))
        got = cache.get(key)
        if got is not None:
            return got
        a, b, c = pts[key[0]], pts[key[1]], pts[key[2]]
        u = (b[0] - a[0], b[1] - a[1], b[2] - a[2])
        v = (c[0] - a[0], c[1] - a[1], c[2] - a[2])
        nx = u[1] * v[2] - u[2] * v[1]
        ny = u[2] * v[0] - u[0] * v[2]
        nz = u[0] * v[1] - u[1] * v[0]
        d = nx * a[0] + ny * a[1] + nz * a[2]
        m = 0
        for t in range(N):
            p = pts[t]
            if nx * p[0] + ny * p[1] + nz * p[2] == d:
                m |= 1 << t
        m &= ~((1 << key[0]) | (1 << key[1]) | (1 << key[2]))
        cache[key] = m
        return m

    alive = (1 << N) - 1
    for i in dead_plane:
        alive &= ~(1 << i)
    chosen = []
    for i in fixed:
        # проверяем допустимость самого куска: он мог быть невыполним уже внутри плоскости
        for j in chosen:
            if not (alive >> i) & 1:
                return ("КУСОК НЕВЕРЕН", 0, 0.0)
        alive &= ~(1 << i)
        for j in chosen:
            alive &= ~kill_pair[i][j]
        for a, b in combinations(chosen, 2):
            alive &= ~kill_triple(a, b, i)
        chosen.append(i)

    state = {"nodes": 0}

    def rec(alive, start):
        state["nodes"] += 1
        if node_cap and state["nodes"] > node_cap:
            raise TimeoutError
        k = len(chosen)
        if k >= M:
            return True
        if k + bin(alive).count("1") < M:
            return False
        cnt = [[0] * n for _ in range(3)]
        for j in chosen:
            p = pts[j]
            for ax in range(3):
                cnt[ax][p[ax]] += 1
        room = [[0] * n for _ in range(3)]
        m2, i2 = alive, 0
        while m2:
            if m2 & 1:
                p = pts[i2]
                for ax in range(3):
                    room[ax][p[ax]] += 1
            m2 >>= 1
            i2 += 1
        bound = min(sum(min(3 - cnt[ax][t], room[ax][t]) for t in range(n)) for ax in range(3))
        if k + bound < M:
            return False
        m, i = alive >> start, start
        while m:
            if m & 1:
                na = alive & ~((1 << (i + 1)) - 1)
                for j in chosen:
                    na &= ~kill_pair[i][j]
                for a, b in combinations(chosen, 2):
                    na &= ~kill_triple(a, b, i)
                chosen.append(i)
                if rec(na, i + 1):
                    return True
                chosen.pop()
            m >>= 1
            i += 1
        return False

    t0 = time.time()
    try:
        found = rec(alive, 49)      # клетки плоскости уже разобраны
    except TimeoutError:
        return ("ПРЕРВАНО", state["nodes"], time.time() - t0)
    return ("SAT — УТВЕРЖДЕНИЕ РУШИТСЯ" if found else "UNSAT",
            state["nodes"], time.time() - t0)


if __name__ == "__main__":
    nm = sys.argv[1]
    M = int(sys.argv[2]) if len(sys.argv) > 2 else 19
    cap = int(sys.argv[3]) if len(sys.argv) > 3 else None
    r, nodes, el = run(nm, M, cap)
    rate = nodes / el if el > 0 else 0
    print(f"{nm}: {r}, узлов {nodes}, {el:.1f}с ({rate:.0f} узлов/с)")
