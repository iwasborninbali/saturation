#!/usr/bin/env python3
"""soft_T.py — мягкая T-модель: P(S) ∝ exp(−β·T(S)), T — число коллинеарных троек, на конфигурациях 2/строку+2/столбец (MCMC
обменами рёбер). При β → ∞ — равномерное распределение на решениях. Вопрос цикла 4: появляется ли κ = 0.731 (доля диагоналей x−y
ровно с двумя точками), которого мягкая ПАРНАЯ цена не даёт, когда штрафуются сами тройки; и что при этом с остальным семейством
(прямоугольники, чётность, гамильтоновых, ρ(k)).  T ведётся через массив κ(c) — число пар точек, коллинеарных с клеткой c
(T = Σ_{s∈S} κ(s)/3); обновление при удалении/добавлении точки — по прямым через неё и каждую другую точку.
usage: python3 soft_T.py n beta moves burnin thin seed
"""
import sys, math, random, collections
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from maxent_pairs import random_config, observe

def build_lines(n):
    """lines[i][j] — кортеж индексов клеток на прямой через клетки i≠j, кроме самих i, j."""
    N = n * n; lines = [[() for _ in range(N)] for _ in range(N)]
    for i in range(N):
        x1, y1 = divmod(i, n)
        for j in range(i + 1, N):
            x2, y2 = divmod(j, n); dx, dy = x2 - x1, y2 - y1
            g = math.gcd(abs(dx), abs(dy)); dx //= g; dy //= g
            cells = []
            for sgn in (1, -1):
                k = 1
                while True:
                    x, y = x1 + sgn * k * dx, y1 + sgn * k * dy
                    if not (0 <= x < n and 0 <= y < n): break
                    c = x * n + y
                    if c != j: cells.append(c)
                    k += 1
            lines[i][j] = lines[j][i] = tuple(cells)
    return lines

def run(n, beta, moves, burnin, thin, seed):
    rnd = random.Random(seed); lines = build_lines(n); N = n * n
    rows = random_config(n, rnd)
    occ = set(r * n + c for r in range(n) for c in rows[r])
    kap = [0] * N
    S = sorted(occ)
    for a in range(len(S)):
        for b in range(a + 1, len(S)):
            for c in lines[S[a]][S[b]]: kap[c] += 1
    def T_of(): return sum(kap[s] for s in occ) // 3
    T = T_of(); assert T * 3 == sum(kap[s] for s in occ)
    def remove(p):
        occ.remove(p)
        for s in occ:
            for c in lines[p][s]: kap[c] -= 1
    def add(q):
        for s in occ:
            for c in lines[q][s]: kap[c] += 1
        occ.add(q)
    acc = 0; samples = []
    for step in range(moves):
        r1 = rnd.randrange(n); r2 = rnd.randrange(n)
        if r1 == r2: continue
        c1 = rows[r1][rnd.randrange(2)]; c2 = rows[r2][rnd.randrange(2)]
        if c1 == c2: continue
        p1, p2 = r1 * n + c1, r2 * n + c2; q1, q2 = r1 * n + c2, r2 * n + c1
        if q1 in occ or q2 in occ: continue
        remove(p1); remove(p2); add(q1); add(q2)
        Tn = sum(kap[s] for s in occ) // 3; dT = Tn - T
        if dT <= 0 or rnd.random() < math.exp(-beta * dT):
            rows[r1][rows[r1].index(c1)] = c2; rows[r2][rows[r2].index(c2)] = c1; T = Tn; acc += 1
        else:
            remove(q1); remove(q2); add(p1); add(p2)
        if step >= burnin and (step - burnin) % thin == 0:
            samples.append(observe(rows, n) + (T,))
    return samples, acc / moves

if __name__ == "__main__":
    n, beta, moves, burnin, thin, seed = int(sys.argv[1]), float(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6])
    samples, accr = run(n, beta, moves, burnin, thin, seed); S = len(samples)
    kap1 = sum(s[6] for s in samples) / S; m2 = sum(s[1] for s in samples) / S
    kees = [s[3] for s in samples]; mk = sum(kees) / S; vk = sum((k - mk) ** 2 for k in kees) / S
    ham = sum(1 for s in samples if s[4]) / S; d11 = sum(s[5] for s in samples) / S; Tm = sum(s[-1] for s in samples) / S
    P0 = sum(1 for s in samples if s[-1] == 0) / S
    dist = collections.Counter()
    for s in samples: dist.update(s[2])
    tot = sum(dist.values()); q0 = {k: 2 * (n - k) / (n * (n - 1)) for k in range(1, n)}
    rho = {k: dist[k] / tot / q0[k] for k in range(1, n)}
    print(f"n={n} β={beta} ходов {moves} → {S} выборок, принято {accr:.3f}, ⟨T⟩ = {Tm:.2f}, доля T=0: {P0:.3f}")
    print(f"  κ (x−y) = {kap1:.4f}  [нуль-A 0.33, решения 0.731];  прямоугольников = {m2:.4f} [0.263 / 0.340];  дисперсия k = {vk:.3f} [2.47 / 0.422], P(k={n//2}) = {sum(1 for k in kees if k == n//2)/S:.3f} [0.25 / 0.61]")
    print(f"  гамильтоновых = {ham:.3f} [0.333 / 0.307];  пар (1,±1) = {d11:.2f} [50.7 / ≈30]")
    obs = {1: 1.07, 2: 1.35, 3: 1.36, 4: 1.30, 5: 0.96, 6: 1.22, 7: 0.59, 8: 0.83, 9: 0.66, 10: 0.88, 11: 0.44, 12: 1.18, 13: 0.43, 14: 0.71, 15: 1.26, 16: 0.91, 17: 0.69, 18: 1.30, 19: 1.02}
    if n == 20:
        ks = [k for k in range(1, n) if rho[k] > 0]; xs = [math.log(rho[k]) for k in ks]; ys = [math.log(obs[k]) for k in ks]
        mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
        slope = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((y - my) ** 2 for y in ys)
        def ranks(v): s = sorted(v); return [s.index(t) for t in v]
        rx, ry = ranks(xs), ranks(ys); a, b = sum(rx) / len(rx), sum(ry) / len(ry)
        sp = sum((u - a) * (w - b) for u, w in zip(rx, ry)) / math.sqrt(sum((u - a) ** 2 for u in rx) * sum((w - b) ** 2 for w in ry))
        print(f"  ρ(k): наклон {slope:.3f}, Спирмен {sp:.3f};  ρ: " + " ".join(f"{k}:{rho[k]:.2f}" for k in range(1, n)))
