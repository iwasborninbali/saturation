"""death_2d.py — кривая смерти для ДВУМЕРНОЙ задачи (три точки на прямой), задача Ахима.

Та же алгебра, сжатая на ступень. В трёхмерии четыре точки компланарны, когда три НАПРАВЛЕНИЯ
от одной из них коллинеарны; в двумерии три точки коллинеарны, когда два направления СОВПАДАЮТ.
Значит смерть проще: две точки убивают прямую, и третьей на ней не быть.
После k рождений мертво ровно C(k,2) прямых; клетка жива, пока через неё не прошла ни одна.

ЗАЧЕМ ЭТО ЗДЕСЬ. При цели 2n запас ёмкости РАВЕН НУЛЮ: n строк по две точки дают ровно 2n,
значит каждая строка и каждый столбец держат РОВНО две. Кривая смерти обязана упираться
в ноль в точности на 2n — если конфигурация существует. Гипотеза Гая-Келли утверждает, что
при больших n её нет: 2n недостижимо, а верхняя граница асимптотически около 1.87n.
Это ровно утверждение «место кончается РАНЬШЕ, чем на 2n», то есть высказывание о кривой
смерти, а не о конфигурациях.

Здесь кривая измеряется, а не постулируется: для каждого n ищется максимум и печатается,
на каком рождении место кончилось.

usage: death_2d.py <n_от> <n_до> [предел-узлов]
"""
import sys
import time
from itertools import combinations


def collinear(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0]) == 0


def solve(n, M, node_cap=None):
    """Есть ли M точек в сетке n на n без трёх на прямой. Отсечение: k + оценка остатка."""
    N = n * n
    pts = [(x, y) for x in range(n) for y in range(n)]
    FULL = (1 << N) - 1

    kill = [[0] * N for _ in range(N)]
    for i in range(N):
        for j in range(i + 1, N):
            m = 0
            for k in range(N):
                if k == i or k == j:
                    continue
                if collinear(pts[i], pts[j], pts[k]):
                    m |= 1 << k
            kill[i][j] = m
            kill[j][i] = m

    state = {"nodes": 0, "sol": None}

    def rec(chosen, alive, start):
        state["nodes"] += 1
        if node_cap and state["nodes"] > node_cap:
            raise TimeoutError
        k = len(chosen)
        if k >= M:
            state["sol"] = [pts[i] for i in chosen]
            return True
        if k + bin(alive).count("1") < M:
            return False
        # ЁМКОСТЬ: строка и столбец держат не более ДВУХ точек (три в ряд коллинеарны).
        cnt = [[0] * n for _ in range(2)]
        for j in chosen:
            p = pts[j]
            cnt[0][p[0]] += 1
            cnt[1][p[1]] += 1
        room = [[0] * n for _ in range(2)]
        m2, i2 = alive, 0
        while m2:
            if m2 & 1:
                p = pts[i2]
                room[0][p[0]] += 1
                room[1][p[1]] += 1
            m2 >>= 1
            i2 += 1
        bound = min(sum(min(2 - cnt[ax][t], room[ax][t]) for t in range(n)) for ax in range(2))
        if k + bound < M:
            return False
        m, i = alive >> start, start
        while m:
            if m & 1:
                na = alive & ~((1 << (i + 1)) - 1)
                for j in chosen:
                    na &= ~kill[i][j]
                chosen.append(i)
                if rec(chosen, na, i + 1):
                    return True
                chosen.pop()
            m >>= 1
            i += 1
        return False

    try:
        found = rec([], FULL, 0)
    except TimeoutError:
        return None, state["nodes"]
    return (state["sol"] if found else None), state["nodes"]


def death_curve(n, S):
    """Сколько клеток живо после каждого рождения."""
    grid = [(x, y) for x in range(n) for y in range(n)]
    out = []
    cur = []
    for p in S:
        cur.append(p)
        alive = 0
        for q in grid:
            if q in cur:
                continue
            if not any(collinear(a, b, q) for a, b in combinations(cur, 2)):
                alive += 1
        out.append(alive)
    return out


if __name__ == "__main__":
    lo, hi = int(sys.argv[1]), int(sys.argv[2])
    cap = int(sys.argv[3]) if len(sys.argv) > 3 else None
    print(" n | цель 2n | найдено | узлов | живых на последнем рождении | вся кривая (хвост)")
    for n in range(lo, hi + 1):
        t0 = time.time()
        best, nodes, sol = 0, 0, None
        for M in range(2 * n, 0, -1):
            s, nd = solve(n, M, node_cap=cap)
            nodes += nd
            if s:
                best, sol = M, s
                break
        if sol is None:
            print(f"{n:2d} | {2*n:7d} | не решено за предел узлов")
            continue
        curve = death_curve(n, sol)
        tail = ",".join(str(c) for c in curve[-6:])
        mark = "= 2n" if best == 2 * n else f"< 2n на {2*n-best}"
        print(f"{n:2d} | {2*n:7d} | {best:7d} {mark:>10s} | {nodes:9d} | {curve[-1]:3d} | ...{tail}  ({time.time()-t0:.1f}с)")
