#!/usr/bin/env python3
"""parity_seeds.py — переоценка предсказаний цикла 3/3б по замечаниям противника №2: несколько сидов, честные ошибки.
(1) чётность: дисперсия k и P(k=10) по наклону exp(−E[T|k]) — среднее ± sd по сидам; нуль тоже с ±.
(2) mod 3: отношение D3 — сглаженный эстиматор (взвешенная регрессия T на D3, наклон b; вес exp(−b·D3)) вместо корзин.
(3) ρ(k): ΔE(k) с ошибкой по конфигурациям (все столбцы одной конфигурации несут один T) и Спирмен по сидам.
usage: python3 parity_seeds.py n samples seed1 seed2 …   (каждый сид — отдельный процесс, результаты сводятся из файлов parity_seed_<s>.json)
       python3 parity_seeds.py summarize n
"""
import sys, math, json, collections, glob, os
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from parity_mech import null_sample, solutions
HERE = __file__.rsplit('/', 1)[0]

def one(n, S, seed):
    rows = null_sample(n, S, seed)   # (w, T, k, D3) — но нам нужны и расстояния столбцов; пересобираем ниже отдельно
    W = sum(w for w, *_ in rows)
    byk = collections.defaultdict(lambda: [0.0, 0.0])
    for w, T, k, _ in rows: byk[k][0] += w; byk[k][1] += w * T
    ks = sorted(byk); Pn = {k: byk[k][0] / W for k in ks}; ET = {k: byk[k][1] / byk[k][0] for k in ks}
    Emin = min(ET[k] for k in ks if Pn[k] > 0.01)
    tilt = {k: Pn[k] * math.exp(-(ET[k] - Emin)) for k in ks}; Z = sum(tilt.values()); Pp = {k: tilt[k] / Z for k in ks}
    mn = sum(k * Pn[k] for k in ks); vn = sum((k - mn) ** 2 * Pn[k] for k in ks)
    mp = sum(k * Pp[k] for k in ks); vp = sum((k - mp) ** 2 * Pp[k] for k in ks)
    # mod 3: регрессия T на D3 (взвешенная)
    sw = W; mD = sum(w * d for w, _, _, d in rows) / sw; mT = sum(w * T for w, T, _, _ in rows) / sw
    b = sum(w * (d - mD) * (T - mT) for w, T, _, d in rows) / sum(w * (d - mD) ** 2 for w, _, _, d in rows)
    Dn = mD; Dp = sum(w * d * math.exp(-b * (d - mD)) for w, _, _, d in rows) / sum(w * math.exp(-b * (d - mD)) for w, _, _, d in rows)
    return {"seed": seed, "S": S, "var_null": vn, "var_pred": vp, "P10_pred": Pp.get(n // 2, 0), "P10_null": Pn.get(n // 2, 0),
            "D3_null": Dn, "D3_pred": Dp, "D3_ratio": Dp / Dn, "b": b, "dE12": ET.get(n // 2 + 2, float('nan')) - ET.get(n // 2, float('nan'))}

if __name__ == "__main__":
    if sys.argv[1] == "summarize":
        n = int(sys.argv[2]); res = [json.load(open(f)) for f in sorted(glob.glob(f"{HERE}/parity_seed_{n}_*.json"))]
        def ms(key):
            v = [r[key] for r in res]; m = sum(v) / len(v); sd = math.sqrt(sum((x - m) ** 2 for x in v) / (len(v) - 1)) if len(v) > 1 else 0
            return m, sd
        sol = solutions(n); m = len(sol); ks = [k for k, _ in sol]; mk = sum(ks) / m
        vs = sum((k - mk) ** 2 for k in ks) / m; p10 = sum(1 for k in ks if k == n // 2) / m; Ds = sum(d for _, d in sol) / m
        print(f"n={n}: сидов {len(res)} по {res[0]['S']} выборок; решений iden {m}")
        for key, obs in (("var_null", None), ("var_pred", vs), ("P10_null", None), ("P10_pred", p10), ("D3_null", None), ("D3_ratio", Ds / ms('D3_null')[0]), ("dE12", None)):
            mm, sd = ms(key)
            print(f"  {key:>9}: {mm:.4f} ± {sd:.4f}" + (f"   наблюдаемое {obs:.4f}   отклонение {(mm/obs-1)*100:+.1f} %" if obs else ""))
        print(f"  (наблюдаемое: дисперсия k {vs:.4f}, P(k={n//2}) {p10:.4f}, среднее D3 {Ds:.4f})")
    else:
        n, S = int(sys.argv[1]), int(sys.argv[2])
        for seed in map(int, sys.argv[3:]):
            r = one(n, S, seed); json.dump(r, open(f"{HERE}/parity_seed_{n}_{seed}.json", "w")); print(r)
