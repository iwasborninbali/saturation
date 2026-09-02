#!/usr/bin/env python3
"""rho_k_mech.py — первомоментный ли эффект ρ(k) (обогащение расстояния k между двумя точками столбца)?
Нуль тот же, что в parity_mech.py (равномерная конфигурация, веса 2^−c). Для каждой конфигурации и каждого столбца с расстоянием k
накапливаем (w, w·T): ΔE(k) = E[T | есть столбец с расстоянием k] − E[T]; предсказание наклона ρ_pred(k) ∝ exp(−ΔE(k)),
нормировано так, чтобы Σ_k P_null(k)·ρ_pred(k) = 1; сравнение с наблюдаемым ρ_col(k) из базы (считается здесь же).
usage: python3 rho_k_mech.py n samples seed
"""
import sys, math, random, collections
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from cycle_null import collinear_triples
from parity_mech import cycles_of_pair, IDX, DB

def main(n, S, seed):
    rnd = random.Random(seed)
    acc = collections.defaultdict(lambda: [0.0, 0.0, 0.0]); W = 0.0; WT = 0.0
    for _ in range(S):
        while True:
            a = list(range(n)); rnd.shuffle(a); b = list(range(n)); rnd.shuffle(b)
            if all(x != y for x, y in zip(a, b)): break
        w = 2.0 ** (-cycles_of_pair(a, b, n))
        pts = sorted(set((r, a[r]) for r in range(n)) | set((r, b[r]) for r in range(n)))
        T = collinear_triples(pts); W += w; WT += w * T
        cols = collections.defaultdict(list)
        for r, c in pts: cols[c].append(r)
        for c, rs in cols.items():
            k = abs(rs[0] - rs[1]); acc[k][0] += w; acc[k][1] += w * T; acc[k][2] += w * T * T
    ET = WT / W
    # наблюдаемое ρ
    cnt = collections.Counter(); sols = 0
    for l in open(DB):
        l = l.strip()
        if not l or (len(l) - 1) // 2 != n or l[0] != '.': continue
        body = l[1:]; sols += 1; cols = collections.defaultdict(list)
        for r in range(n):
            cols[IDX[body[2 * r]]].append(r); cols[IDX[body[2 * r + 1]]].append(r)
        for rs in cols.values(): cnt[abs(rs[0] - rs[1])] += 1
    q0 = {k: 2 * (n - k) / (n * (n - 1)) for k in range(1, n)}
    rho_obs = {k: cnt[k] / (sols * n) / q0[k] for k in range(1, n)}
    dE = {k: acc[k][1] / acc[k][0] - ET for k in range(1, n)}
    se = {k: math.sqrt(max(acc[k][2] / acc[k][0] - (acc[k][1] / acc[k][0]) ** 2, 0) / (acc[k][0] / W * S * n / 2)) for k in range(1, n)}
    raw = {k: math.exp(-dE[k]) for k in range(1, n)}
    Z = sum(q0[k] * raw[k] for k in range(1, n)); rho_pred = {k: raw[k] / Z for k in range(1, n)}
    print(f"n={n}, {S} выборок нуля, E[T] = {ET:.3f}; k — расстояние между двумя точками столбца")
    print(f"{'k':>3} {'P_null(k)':>9} {'ΔE(k)':>7} {'±SE':>5} {'ρ_pred':>7} {'ρ_obs':>6}")
    for k in range(1, n):
        print(f"{k:>3} {acc[k][0]/W/n*1:9.4f} {dE[k]:7.3f} {se[k]:5.3f} {rho_pred[k]:7.3f} {rho_obs[k]:6.3f}")
    def ranks(v): s = sorted(v); return [s.index(x) for x in v]
    xs = [math.log(rho_pred[k]) for k in range(1, n)]; ys = [math.log(rho_obs[k]) for k in range(1, n)]
    rx, ry = ranks(xs), ranks(ys); mx, my = sum(rx) / len(rx), sum(ry) / len(ry)
    sp = sum((a - mx) * (b - my) for a, b in zip(rx, ry)) / math.sqrt(sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry))
    print(f"Спирмен(log ρ_pred, log ρ_obs) = {sp:.3f};  ρ_pred(7)/ρ_pred(6) = {rho_pred[7]/rho_pred[6]:.3f} (наблюдаемое {rho_obs[7]/rho_obs[6]:.3f})")

if __name__ == "__main__":
    main(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
