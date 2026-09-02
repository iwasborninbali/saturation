#!/usr/bin/env python3
"""rot2_null.py — нуль для класса rot2: равномерная rot2-инвариантная конфигурация 2/строку+2/столбец.
Инвариантность: (r, c) ∈ S ⟺ (n−1−r, n−1−c) ∈ S. MCMC — парный обмен рёбер: обмен (r1,c1),(r2,c2) → (r1,c2),(r2,c1) и его зеркальный
образ применяются вместе; принимается, если результат — конфигурация (в каждой строке и столбце ровно 2, клетки различны).
Симметричное предложение и равномерная цель ⇒ принимать всё допустимое. Калибровка: при малых n полный перебор инвариантных
конфигураций (через перебор пар перестановок) даёт точное распределение типов циклов — сэмплер обязан его воспроизвести.
Наблюдаемые: доля гамильтоновых, доля с 2-циклом, среднее число циклов; сравнение с переписью rot2 из базы.
usage: python3 rot2_null.py calib n | sample n moves seed | census n
"""
import sys, math, random, collections, itertools
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from cycle_census import cycle_type, CLS, IDX, DB

def mirror(n, r, c): return n - 1 - r, n - 1 - c

def invariant(rows, n):
    S = set((r, c) for r in range(n) for c in rows[r])
    return all(mirror(n, r, c) in S for r, c in S)

def random_invariant(n, rnd):
    """стартовая инвариантная конфигурация: перебор случайных пар перестановок до инвариантной (мало n) или построение."""
    while True:
        a = list(range(n)); rnd.shuffle(a); b = list(range(n)); rnd.shuffle(b)
        if any(x == y for x, y in zip(a, b)): continue
        rows = [[a[r], b[r]] for r in range(n)]
        if invariant(rows, n): return rows

def build_invariant(n, rnd):
    """конструктивно: для строк r < n/2 выбираем пары столбцов так, чтобы зеркальные строки замкнули столбцы; отбраковка."""
    for _ in range(100000):
        rows = [None] * n; colcnt = [0] * n; ok = True
        half = list(range(n // 2)); rnd.shuffle(half)
        for r in half:
            free = [c for c in range(n) if colcnt[c] < 2 and colcnt[n - 1 - c] < 2]
            if len(free) < 2: ok = False; break
            # случайная пара столбцов, при которой и зеркальная строка законна
            cand = []
            for c1, c2 in itertools.combinations(free, 2):
                m1, m2 = n - 1 - c1, n - 1 - c2
                cnt = collections.Counter([c1, c2, m1, m2])
                if all(colcnt[c] + cnt[c] <= 2 for c in cnt): cand.append((c1, c2))
            if not cand: ok = False; break
            c1, c2 = rnd.choice(cand); m1, m2 = n - 1 - c1, n - 1 - c2
            rows[r] = [c1, c2]; rows[n - 1 - r] = [m1, m2]
            for c in (c1, c2, m1, m2): colcnt[c] += 1
        if not ok: continue
        if n % 2 == 1:
            r = n // 2; free = [c for c in range(n) if colcnt[c] < 2 and c != r]
            cand = [c for c in free if colcnt[n - 1 - c] < 2 and c < n - 1 - c]
            if not cand: continue
            c = rnd.choice(cand); rows[r] = [c, n - 1 - c]; colcnt[c] += 1; colcnt[n - 1 - c] += 1
        if all(x == 2 for x in colcnt) and invariant(rows, n): return rows
    raise RuntimeError("не построил")

def step(rows, n, rnd):
    r1 = rnd.randrange(n); r2 = rnd.randrange(n)
    if r1 == r2: return False
    c1 = rows[r1][rnd.randrange(2)]; c2 = rows[r2][rnd.randrange(2)]
    if c1 == c2: return False
    rem = {(r1, c1), (r2, c2)}; add = {(r1, c2), (r2, c1)}
    rem |= {mirror(n, r, c) for r, c in list(rem)}; add |= {mirror(n, r, c) for r, c in list(add)}
    S = set((r, c) for r in range(n) for c in rows[r])
    if not rem <= S: return False
    if add & (S - rem): return False
    if rem & add: return False
    T = (S - rem) | add
    rc = collections.Counter(r for r, _ in T); cc = collections.Counter(c for _, c in T)
    if len(T) != 2 * n or any(v != 2 for v in rc.values()) or any(v != 2 for v in cc.values()): return False
    new = [[] for _ in range(n)]
    for r, c in sorted(T): new[r].append(c)
    for r in range(n): rows[r] = new[r]
    return True

def stats(types):
    tot = len(types)
    return sum(1 for t in types if len(t) == 1) / tot, sum(1 for t in types if 2 in t) / tot, sum(len(t) for t in types) / tot

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "calib":
        n = int(sys.argv[2]); exact = collections.Counter(); seen = set()
        for a in itertools.permutations(range(n)):
            for b in itertools.permutations(range(n)):
                if any(x == y for x, y in zip(a, b)): continue
                rows = [sorted((a[r], b[r])) for r in range(n)]
                key = tuple(tuple(x) for x in rows)
                if key in seen: continue
                seen.add(key)
                if invariant([list(x) for x in rows], n): exact[cycle_type([list(x) for x in rows])] += 1
        tot = sum(exact.values()); print(f"n={n}: инвариантных конфигураций {tot}; типы: " + " ".join(f"{k}:{v/tot:.4f}" for k, v in sorted(exact.items())))
        rnd = random.Random(1); rows = build_invariant(n, rnd); cnt = collections.Counter(); acc = 0
        for i in range(200000):
            acc += step(rows, n, rnd)
            if i % 20 == 0: cnt[cycle_type(rows)] += 1
        tot2 = sum(cnt.values()); print(f"   сэмплер (200k ходов, принято {acc/200000:.3f}): " + " ".join(f"{k}:{cnt[k]/tot2:.4f}" for k in sorted(exact)))
        print("   макс. расхождение долей:", max(abs(cnt[k] / tot2 - exact[k] / tot) for k in exact))
    elif cmd == "sample":
        n, moves, seed = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]); rnd = random.Random(seed)
        rows = build_invariant(n, rnd); types = []; acc = 0
        for i in range(moves):
            acc += step(rows, n, rnd)
            if i >= moves // 10 and i % 50 == 0: types.append(cycle_type(rows))
        ham, has2, meanc = stats(types)
        print(f"rot2-нуль n={n}: выборок {len(types)} (принято {acc/moves:.3f}); гамильтоновых {ham:.4f}, с 2-циклом {has2:.4f}, среднее циклов {meanc:.3f}")
    elif cmd == "census":
        n = int(sys.argv[2]); types = []
        for l in open(DB):
            l = l.strip()
            if not l or (len(l) - 1) // 2 != n or CLS[l[0]] != 'rot2': continue
            body = l[1:]; rows = [[IDX[body[2 * r]], IDX[body[2 * r + 1]]] for r in range(n)]
            assert invariant(rows, n), "решение класса rot2 не инвариантно?"
            types.append(cycle_type(rows))
        ham, has2, meanc = stats(types)
        print(f"rot2-решения n={n}: {len(types)}; гамильтоновых {ham:.4f}, с 2-циклом {has2:.4f}, среднее циклов {meanc:.3f}")
