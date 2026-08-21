"""sym_baseline_exact.py — ТОЧНАЯ база симметрии, без выборки.

Множество неподвижно под движением g тогда и только тогда, когда оно есть объединение орбит g.
Значит число неподвижных M-подмножеств считается точно — задачей о суммах по размерам орбит.
Сумма по 47 нетождественным движениям даёт оценку сверху на долю симметричных (объединительная
граница); истинная доля чуть меньше, поэтому обогащение выходит ЗАНИЖЕННЫМ, то есть надёжным.

Выборка тут не годится в принципе: при n=5 доля порядка 10^-6, и 400 000 образцов дают
одно событие. Считать по одному событию нельзя — это тот самый урок про базу, доведённый до конца.
"""
import itertools
from math import comb

def fixed_count(n, M):
    cells = [(x, y, z) for x in range(n) for y in range(n) for z in range(n)]
    idx = {c: i for i, c in enumerate(cells)}
    N = len(cells); m = n - 1
    mots = [(p, s) for p in itertools.permutations(range(3)) for s in itertools.product((0, 1), repeat=3)]
    total = 0
    for p, s in mots:
        if p == (0, 1, 2) and s == (0, 0, 0):
            continue
        seen = [False] * N; sizes = []
        for i, c in enumerate(cells):
            if seen[i]:
                continue
            o = 0; cur = c
            while True:
                j = idx[cur]
                if seen[j]:
                    break
                seen[j] = True; o += 1
                q = [cur[p[0]], cur[p[1]], cur[p[2]]]
                cur = tuple((m - q[k]) if s[k] else q[k] for k in range(3))
            sizes.append(o)
        dp = [0] * (M + 1); dp[0] = 1
        for sz in sizes:
            if sz > M:
                continue
            for t in range(M, sz - 1, -1):
                dp[t] += dp[t - sz]
        total += dp[M]
    return total, comb(N, M)

for n, M, truth, symtrue in [(3, 8, 16, 16), (4, 10, 10960, 160), (5, 13, 1768, 40)]:
    fx, tot = fixed_count(n, M)
    base = 100.0 * fx / tot
    got = 100.0 * symtrue / truth
    print(f"n={n} M={M}: у максимумов {got:6.2f}% ({symtrue}/{truth}),  "
          f"база (точно, сверху) {base:.7f}%  ->  обогащение >= ×{got/base:.0f}")
