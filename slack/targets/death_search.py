"""death_search.py — поиск, устроенный вокруг СМЕРТИ, а не вокруг точек.

ИДЕЯ (хозяина). У клетки есть время жизни. Три элемента конфигурации убивают плоскость,
два — прямую; клетка жива, пока через неё не прошла ни одна мёртвая плоскость и ни одна
мёртвая прямая. Вопрос «сколько точек влезет» становится вопросом «когда кончается место
для рождения».

ЗАМЕРЕНО на известном свидетеле a(7)>=18 — кривая смерти:
    k= 1: живых 342     k= 7: 162     k=14:  7
    k= 5: живых 301     k=10:  55     k=17:  1
    k= 6: живых 237     k=12:  30     k=18:  0
Место кончается РОВНО на восемнадцатом рождении; на семнадцатом оставалась одна клетка,
она и стала восемнадцатой точкой.

ЧТО ЭТО ДАЁТ, ЧЕГО НЕТ В КОДИРОВКЕ. Отсечение по остатку:
        размещено k, живых a  =>  больше k+a элементов не будет НИКОГДА.
На том же свидетеле оно срабатывает на пятнадцатом шаге (15+3=18<19) — за четыре шага до
конца. Решатель SAT такого не выводит: это счётный просмотр вперёд по ТЕКУЩЕМУ состоянию,
а не постоянная клауза. Мы четырежды измерили, что добавление постоянных клауз здесь не даёт
ничего (парная граница слоёв, «ровно 19», запрет коллинеарных троек); это — другого рода.

ПОЧЕМУ ОТСЕЧЕНИЕ СИЛЬНО ИМЕННО ЗДЕСЬ. M=19 при потолке 3n=21: цель почти упирается в потолок,
поэтому запас k+a-M мал и обнуляется рано. При полном переборе (цель низка) то же отсечение
почти не кусается — этим и объясняется, почему наш прежний перечислитель не тянул n=6.

КАЛИБРОВКА ОБЯЗАТЕЛЬНА: инструмент проверяется на известных ответах ДО того, как на него
полагаются. a(3)=8, a(4)=10, a(5)=13.

usage: death_search.py <n> <M> [предел-узлов]
"""
import sys
import time
from itertools import combinations


def solve(n, M, node_cap=None, report=None):
    N = n * n * n
    pts = [(x, y, z) for x in range(n) for y in range(n) for z in range(n)]
    FULL = (1 << N) - 1

    # kill_pair[i][j] — маска клеток, убиваемых ПАРОЙ: все третьи на прямой через i и j.
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

    _tri_cache = {}

    def kill_triple(i, j, k):
        """Маска клеток на плоскости через i,j,k — она мертва с мгновения их рождения."""
        key = (i, j, k)
        got = _tri_cache.get(key)
        if got is not None:
            return got
        a, b, c = pts[i], pts[j], pts[k]
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
        m &= ~((1 << i) | (1 << j) | (1 << k))
        _tri_cache[key] = m
        return m

    state = {"nodes": 0, "best": 0, "sol": None}

    def rec(chosen, alive, start):
        state["nodes"] += 1
        if node_cap and state["nodes"] > node_cap:
            raise TimeoutError
        k = len(chosen)
        if k > state["best"]:
            state["best"] = k
            if report:
                report(k, bin(alive).count("1"), state["nodes"])
        if k >= M:
            state["sol"] = [pts[i] for i in chosen]
            return True
        # ОТСЕЧЕНИЕ ПО ОСТАТКУ, ОГРАНИЧЕННОМУ ЁМКОСТЬЮ.
        # Грубая оценка k + |живых| почти не кусается: живых много, а взять из них можно мало.
        # Слой (плоскость, перпендикулярная оси) есть богатая плоскость и несёт НЕ БОЛЕЕ ТРЁХ
        # точек. Значит из живых клеток слоя можно взять не больше, чем 3 минус уже стоящие
        # в нём. Складываем по слоям и берём МИНИМУМ по трём осям — три независимые оценки
        # одного и того же остатка, и слабейшая из них всё равно верна.
        if k + bin(alive).count("1") < M:
            return False
        cnt = [[0] * n for _ in range(3)]
        for j in chosen:
            p = pts[j]
            for ax in range(3):
                cnt[ax][p[ax]] += 1
        room = [[0] * n for _ in range(3)]
        m2 = alive
        i2 = 0
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
        m = alive >> start
        i = start
        while m:
            if m & 1:
                na = alive & ~((1 << (i + 1)) - 1)   # лексикографический порядок
                for j in chosen:
                    na &= ~kill_pair[i][j]
                for a, b in combinations(chosen, 2):
                    na &= ~kill_triple(a, b, i)
                chosen.append(i)
                if rec(chosen, na, i + 1):
                    return True
                chosen.pop()
            m >>= 1
            i += 1
        return False

    t0 = time.time()
    try:
        found = rec([], FULL, 0)
    except TimeoutError:
        return ("ПРЕРВАНО", state["nodes"], time.time() - t0, state["best"], None)
    return ("SAT" if found else "UNSAT", state["nodes"], time.time() - t0,
            state["best"], state["sol"])


if __name__ == "__main__":
    n, M = int(sys.argv[1]), int(sys.argv[2])
    cap = int(sys.argv[3]) if len(sys.argv) > 3 else None
    r, nodes, el, best, sol = solve(n, M, node_cap=cap)
    rate = nodes / el if el > 0 else 0
    print(f"n={n} M={M}: {r}, узлов {nodes}, {el:.2f}с ({rate:.0f} узлов/с), лучшее {best}")
    if sol:
        print("  свидетель:", " ".join(f"({x},{y},{z})" for x, y, z in sol))
