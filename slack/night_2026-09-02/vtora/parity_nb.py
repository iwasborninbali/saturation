#!/usr/bin/env python3
"""parity_nb.py — второй порядок для наклона чётности: перерассеяние T при фиксированном k.
Пуассоновский наклон P(T=0|k) ≈ exp(−E[T|k]) недобирает ≈ 12 % показателя (противник №2). Если T|k перерассеян
(Var/E ≈ 2.3), естественная поправка — отрицательно-биномиальная: P(T=0|k) = (1 + μ_k/r_k)^{−r_k}, r_k = μ_k²/(σ_k² − μ_k).
Считаем оба наклона по одним и тем же выборкам нуля (несколько сидов), сравниваем предсказанные дисперсию k и P(k=n/2) с решениями.
usage: python3 parity_nb.py n samples seed [seed …]
"""
import sys, math, collections
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from parity_mech import null_sample, solutions

def tilt_stats(rows, n, kind):
    W = sum(w for w, *_ in rows)
    acc = collections.defaultdict(lambda: [0.0, 0.0, 0.0])
    for w, T, k, _ in rows: acc[k][0] += w; acc[k][1] += w * T; acc[k][2] += w * T * T
    ks = sorted(k for k in acc if acc[k][0] / W > 0.003)
    logp = {}
    for k in ks:
        Pk = acc[k][0] / W; mu = acc[k][1] / acc[k][0]; var = acc[k][2] / acc[k][0] - mu * mu
        if kind == "poisson": lp = -mu
        else:
            if var <= mu: lp = -mu
            else:
                r = mu * mu / (var - mu); lp = -r * math.log(1 + mu / r)
        logp[k] = math.log(Pk) + lp
    m = max(logp.values()); Z = sum(math.exp(v - m) for v in logp.values())
    P = {k: math.exp(logp[k] - m) / Z for k in ks}
    mean = sum(k * P[k] for k in ks); var = sum((k - mean) ** 2 * P[k] for k in ks)
    return var, P.get(n // 2, 0.0), {k: (acc[k][1] / acc[k][0], acc[k][2] / acc[k][0] - (acc[k][1] / acc[k][0]) ** 2) for k in ks}

if __name__ == "__main__":
    n, S = int(sys.argv[1]), int(sys.argv[2]); seeds = [int(x) for x in sys.argv[3:]]
    sol = solutions(n); m = len(sol); ks = [k for k, _ in sol]; mk = sum(ks) / m
    vs = sum((k - mk) ** 2 for k in ks) / m; p0 = sum(1 for k in ks if k == n // 2) / m
    res = {"poisson": [], "nb": []}
    for seed in seeds:
        rows = null_sample(n, S, seed)
        for kind in res:
            v, p, mv = tilt_stats(rows, n, kind); res[kind].append((v, p))
        print(f"seed {seed}: E[T|k], Var[T|k]: " + " ".join(f"{k}:{mu:.1f}/{va:.0f}" for k, (mu, va) in sorted(mv.items()) if abs(k - n // 2) <= 3))
    print(f"\nn={n}, решений {m}: дисперсия k {vs:.4f}, P(k={n//2}) {p0:.4f}")
    for kind in res:
        vsd = [v for v, _ in res[kind]]; psd = [p for _, p in res[kind]]
        mv, sv = sum(vsd) / len(vsd), (sum((x - sum(vsd) / len(vsd)) ** 2 for x in vsd) / max(len(vsd) - 1, 1)) ** .5
        mp, sp = sum(psd) / len(psd), (sum((x - sum(psd) / len(psd)) ** 2 for x in psd) / max(len(psd) - 1, 1)) ** .5
        print(f"  наклон {kind:>7}: дисперсия {mv:.4f} ± {sv:.4f} ({(mv/vs-1)*100:+.1f} %), P(k={n//2}) {mp:.4f} ± {sp:.4f} ({(mp/p0-1)*100:+.1f} %)")
