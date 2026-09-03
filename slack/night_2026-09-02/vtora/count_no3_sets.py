#!/usr/bin/env python3
"""count_no3_sets.py — второй счёт для need-004 коллеги: число подмножеств решётки n×n без трёх точек на одной прямой (независимые
множества 3-однородного гиперграфа коллинеарных троек, включая пустое) и число максимальных по включению таких множеств.
Свой код: DFS по клеткам в фиксированном порядке с битовыми масками; клетка запрещена, если лежит на прямой через две выбранные точки;
множество максимально ⟺ все невыбранные клетки запрещены. usage: python3 count_no3_sets.py n_max"""
import sys, math, time
def run(n):
    N = n * n; cells = [(i // n, i % n) for i in range(N)]
    line = [[0] * N for _ in range(N)]          # line[i][j] = маска клеток на прямой через i и j, кроме самих i, j
    for i in range(N):
        for j in range(i + 1, N):
            (x1, y1), (x2, y2) = cells[i], cells[j]; dx, dy = x2 - x1, y2 - y1; g = math.gcd(abs(dx), abs(dy)); dx //= g; dy //= g
            m = 0
            for k in range(N):
                x, y = cells[k]
                if k != i and k != j and (x - x1) * dy == (y - y1) * dx: m |= 1 << k
            line[i][j] = line[j][i] = m
    FULL = (1 << N) - 1
    total = [0]; maximal = [0]
    def dfs(start, S, chosen, F):
        total[0] += 1
        if (S | F) == FULL: maximal[0] += 1
        for c in range(start, N):
            b = 1 << c
            if F & b: continue
            Fn = F
            for s in chosen: Fn |= line[s][c]
            dfs(c + 1, S | b, chosen + [c], Fn)
    dfs(0, 0, [], 0)
    return total[0], maximal[0]
if __name__ == "__main__":
    for n in range(1, int(sys.argv[1]) + 1):
        t = time.time(); tot, mx = run(n)
        print(f"n={n}: множеств без трёх на прямой (с пустым) {tot}, максимальных {mx}   [{time.time()-t:.1f} с]", flush=True)
