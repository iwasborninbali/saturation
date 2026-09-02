#!/usr/bin/env python3
"""maxent_pairs.py — max-entropy модель «пара стоит затенённых клеток» на конфигурациях 2/строку+2/столбец.

P(S) ∝ exp(−λ·E(S)),  E(S) = Σ_{пары точек} kill(P,Q),  kill = число клеток сетки на прямой через P и Q, кроме самих P и Q
(строчные и столбцовые пары дают константу n(n−2)·2 — включены, на веса не влияют).  Жёсткое ограничение — ровно 2 точки в
каждой строке и каждом столбце; MCMC — обмены рёбер (r1,c1),(r2,c2) → (r1,c2),(r2,c1), Метрополис.  λ = 0 — точный нуль
(равномерная конфигурация): калибровка на известном (κ_null = 0.639 при n=20, прямоугольников 0.263, ρ ≡ 1, дисперсия чётности 2.47,
гамильтоновых 0.333).  Наблюдаемые: κ (доля диагоналей x−y=const ровно с двумя точками), прямоугольники на конфигурацию,
ρ(k) по расстояниям в столбцах, дисперсия числа точек в классе (чётн.,чётн.), доля гамильтоновых, доля пар в направлениях (1,±1).
usage: python3 maxent_pairs.py n lambda moves burnin thin seed
"""
import sys, math, random, collections

def build_kill(n):
    N = n * n; kill = [[0] * N for _ in range(N)]
    for i in range(N):
        x1, y1 = divmod(i, n)
        for j in range(i + 1, N):
            x2, y2 = divmod(j, n); dx, dy = x2 - x1, y2 - y1
            g = math.gcd(abs(dx), abs(dy)); dx //= g; dy //= g
            cnt = 0
            for sgn in (1, -1):
                k = 1
                while True:
                    x, y = x1 + sgn * k * dx, y1 + sgn * k * dy
                    if not (0 <= x < n and 0 <= y < n): break
                    cnt += 1; k += 1
            # cnt = все клетки прямой кроме P; минус Q
            kill[i][j] = kill[j][i] = cnt - 1
    return kill

def energy(pts, kill):
    return sum(kill[pts[i]][pts[j]] for i in range(len(pts)) for j in range(i + 1, len(pts)))

def random_config(n, rnd):
    while True:
        a = list(range(n)); rnd.shuffle(a); b = list(range(n)); rnd.shuffle(b)
        if all(x != y for x, y in zip(a, b)): break
    rows = [[a[r], b[r]] for r in range(n)]
    return rows

def observe(rows, n):
    pts = [(r, c) for r in range(n) for c in rows[r]]
    # κ по диагоналям x−y
    diag = collections.Counter(r - c for r, c in pts); kap1 = sum(1 for v in diag.values() if v == 2) / n
    anti = collections.Counter(r + c for r, c in pts); kap = (kap1 * n + sum(1 for v in anti.values() if v == 2)) / (2 * n)   # обе диагонали, среднее на направление
    # прямоугольники
    seen = collections.Counter(frozenset(cs) for cs in rows); m2 = sum(1 for v in seen.values() if v == 2)
    # расстояния в столбцах
    cols = collections.defaultdict(list)
    for r, c in pts: cols[c].append(r)
    dists = [abs(v[0] - v[1]) for v in cols.values()]
    # чётность
    kee = sum(1 for r, c in pts if r % 2 == 0 and c % 2 == 0)
    # гамильтонов?
    seenr = [False] * n; cyc = 0
    for r0 in range(n):
        if seenr[r0]: continue
        cyc += 1; r, c = r0, rows[r0][0]
        while not seenr[r]:
            seenr[r] = True; c = rows[r][1] if c == rows[r][0] else rows[r][0]
            rr = cols[c]; r = rr[1] if rr[0] == r else rr[0]
    # пары в направлениях (1,±1)
    d11 = 0
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            if abs(pts[i][0] - pts[j][0]) == abs(pts[i][1] - pts[j][1]): d11 += 1
    return kap, m2, dists, kee, cyc == 1, d11, kap1

def run(n, lam, moves, burnin, thin, seed):
    rnd = random.Random(seed); kill = build_kill(n)
    rows = random_config(n, rnd)
    occ = set(r * n + c for r in range(n) for c in rows[r])
    pts_idx = sorted(occ)
    E = energy(pts_idx, kill)
    acc = 0; samples = []
    for step in range(moves):
        r1 = rnd.randrange(n); r2 = rnd.randrange(n)
        if r1 == r2: continue
        c1 = rows[r1][rnd.randrange(2)]; c2 = rows[r2][rnd.randrange(2)]
        if c1 == c2: continue
        p1, p2 = r1 * n + c1, r2 * n + c2; q1, q2 = r1 * n + c2, r2 * n + c1
        if q1 in occ or q2 in occ: continue
        dE = kill[q1][q2] - kill[p1][p2]
        for s in occ:
            if s == p1 or s == p2: continue
            dE += kill[q1][s] + kill[q2][s] - kill[p1][s] - kill[p2][s]
        if dE <= 0 or rnd.random() < math.exp(-lam * dE):
            occ.remove(p1); occ.remove(p2); occ.add(q1); occ.add(q2)
            rows[r1][rows[r1].index(c1)] = c2; rows[r2][rows[r2].index(c2)] = c1
            E += dE; acc += 1
        if step >= burnin and (step - burnin) % thin == 0:
            samples.append(observe(rows, n) + (E,))
    return samples, acc / moves

if __name__ == "__main__":
    n, lam, moves, burnin, thin, seed = int(sys.argv[1]), float(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6])
    samples, accr = run(n, lam, moves, burnin, thin, seed)
    S = len(samples)
    kap = sum(s[0] for s in samples) / S; m2 = sum(s[1] for s in samples) / S
    kees = [s[3] for s in samples]; mk = sum(kees) / S; vk = sum((k - mk) ** 2 for k in kees) / S
    ham = sum(1 for s in samples if s[4]) / S; d11 = sum(s[5] for s in samples) / S; Em = sum(s[-1] for s in samples) / S
    dist = collections.Counter()
    for s in samples: dist.update(s[2])
    tot = sum(dist.values()); q0 = {k: 2 * (n - k) / (n * (n - 1)) for k in range(1, n)}
    rho = {k: dist[k] / tot / q0[k] for k in range(1, n)}
    # блочные ошибки (10 блоков) для κ и m2
    B = 10; bl = S // B
    def bse(f):
        ms = [sum(f(s) for s in samples[i * bl:(i + 1) * bl]) / bl for i in range(B)]; m = sum(ms) / B
        return math.sqrt(sum((x - m) ** 2 for x in ms) / (B - 1) / B)
    print(f"n={n} λ={lam} ходов {moves} (прогрев {burnin}, шаг {thin}) → {S} выборок, принято {accr:.3f}, ⟨E⟩ = {Em:.1f}")
    kap1 = sum(s[6] for s in samples) / S
    print(f"  κ (диагонали ровно с 2, среднее по двум направлениям) = {kap:.4f} ± {bse(lambda s: s[0]):.4f}; только x−y: {kap1:.4f}   [нуль-A дня (2/строку+2/столбец) 0.33, решения 0.731; κ дня — по одному направлению x−y]")
    print(f"  прямоугольников на конфигурацию = {m2:.4f} ± {bse(lambda s: s[1]):.4f}   [нуль 0.263, решения 0.3396]")
    print(f"  дисперсия k(чётн.,чётн.) = {vk:.3f}   [нуль 2.47, решения 0.422];  P(k={n//2}) = {sum(1 for k in kees if k == n//2)/S:.3f} [0.252 / 0.609]")
    print(f"  гамильтоновых = {ham:.3f}   [нуль 0.333, решения 0.307];  пар в направлениях (1,±1) = {d11:.2f} на конфигурацию")
    obs = {1: 1.07, 2: 1.35, 3: 1.36, 4: 1.30, 5: 0.96, 6: 1.22, 7: 0.59, 8: 0.83, 9: 0.66, 10: 0.88, 11: 0.44, 12: 1.18, 13: 0.43, 14: 0.71, 15: 1.26, 16: 0.91, 17: 0.69, 18: 1.30, 19: 1.02}
    print("  ρ(k) модель / решения: " + " ".join(f"{k}:{rho[k]:.2f}/{obs[k]:.2f}" for k in range(1, n)))
    if n == 20:
        xs = [math.log(rho[k]) for k in range(1, n) if rho[k] > 0]; ys = [math.log(obs[k]) for k in range(1, n) if rho[k] > 0]
        mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
        slope = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((y - my) ** 2 for y in ys)   # наклон log ρ_model по log ρ_obs
        def ranks(v): s = sorted(v); return [s.index(t) for t in v]
        rx, ry = ranks(xs), ranks(ys); a, b = sum(rx) / len(rx), sum(ry) / len(ry)
        sp = sum((u - a) * (w - b) for u, w in zip(rx, ry)) / math.sqrt(sum((u - a) ** 2 for u in rx) * sum((w - b) ** 2 for w in ry))
        print(f"  ρ(k): наклон log ρ_model по log ρ_obs = {slope:.3f} (1 = полная амплитуда), Спирмен = {sp:.3f}")
