#!/usr/bin/env python3
"""rect_geometry.py — форма прямоугольников (2-циклов) в iden-решениях против равномерной конфигурации.
Прямоугольник: две строки r1<r2, делящие оба столбца c1<c2; форма (Δr, Δc) = (r2−r1, c2−c1).
Нуль: при условии типа циклов строки и столбцы 2-цикла равномерны и независимы, P(Δ = d) = 2(n−d)/(n(n−1));
среднее число прямоугольников на конфигурацию E_conf[m₂] — точно из весов P_conf (cycle_null.weights).
Обогащение класса форм = (прямоугольников класса на решение) / (E_conf[m₂] · P_null(класс)).
usage: python3 rect_geometry.py [n] [класс]      (по умолчанию 20 iden)
"""
import sys, math, collections
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from cycle_null import weights
ALPHA = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz#$%&@?!()[]<>{}=*+|-/~^_:;,."
IDX = {c: i for i, c in enumerate(ALPHA)}
CLS = {'.': 'iden', ':': 'rot2', '/': 'dia1', '-': 'ort1', 'o': 'rot4', 'c': 'rct4', 'x': 'dia2', '+': 'ort2', '*': 'full'}
DB = "/Users/iwasborninbali/saturation/web/all_known_solutions"

n = int(sys.argv[1]) if len(sys.argv) > 1 else 20
cls = sys.argv[2] if len(sys.argv) > 2 else 'iden'
W = weights(n); Zc = sum(w for _, w in W.values())
E_m2 = float(sum(lam.count(2) * w for lam, (_, w) in W.items()) / Zc)
p_delta = {d: 2 * (n - d) / (n * (n - 1)) for d in range(1, n)}

sols = 0; shapes = collections.Counter()
for l in open(DB):
    l = l.strip()
    if not l or (len(l) - 1) // 2 != n or CLS[l[0]] != cls: continue
    body = l[1:]; sols += 1
    rows = [frozenset((IDX[body[2 * r]], IDX[body[2 * r + 1]])) for r in range(n)]
    seen = collections.defaultdict(list)
    for r, cs in enumerate(rows): seen[cs].append(r)
    for cs, rs in seen.items():
        if len(rs) == 2:
            c1, c2 = sorted(cs); shapes[(rs[1] - rs[0], c2 - c1)] += 1
tot = sum(shapes.values())
print(f"n={n} {cls}: решений {sols}, прямоугольников {tot} ({tot/sols:.4f} на решение; нуль E_conf[m₂] = {E_m2:.4f}; общее обогащение {tot/sols/E_m2:.3f})")

def enrich(pred, name):
    obs = sum(v for s, v in shapes.items() if pred(*s)) / sols
    pn = sum(p_delta[a] * p_delta[b] for a in p_delta for b in p_delta if pred(a, b))
    cnt = sum(v for s, v in shapes.items() if pred(*s))
    E = obs / (E_m2 * pn) if pn else float('nan')
    se = E / math.sqrt(cnt) if cnt else float('nan')
    print(f"  {name:<34} прямоугольников {cnt:>6}  P_null(класс)={pn:.4f}  обогащение E = {E:.3f} ± {se:.3f}")

print("по размеру max(Δr, Δc):")
for lo, hi in ((1, 3), (4, 7), (8, n - 1)):
    enrich(lambda a, b, lo=lo, hi=hi: lo <= max(a, b) <= hi, f"max ∈ [{lo},{hi}]")
for m in range(1, n):
    cnt = sum(v for (a, b), v in shapes.items() if max(a, b) == m)
    pn = sum(p_delta[a] * p_delta[b] for a in p_delta for b in p_delta if max(a, b) == m)
    if cnt: print(f"    max={m:>2}: {cnt:>6}  E={cnt/sols/(E_m2*pn):.3f}")
print("квадраты и НОД:")
enrich(lambda a, b: a == b, "Δr = Δc (квадраты)")
enrich(lambda a, b: a != b, "Δr ≠ Δc")
enrich(lambda a, b: math.gcd(a, b) == 1, "gcd = 1")
enrich(lambda a, b: math.gcd(a, b) >= 2, "gcd ≥ 2")
enrich(lambda a, b: math.gcd(a, b) >= 2 and max(a, b) >= 8, "gcd ≥ 2 и max ≥ 8")
enrich(lambda a, b: math.gcd(a, b) == 1 and max(a, b) >= 8, "gcd = 1 и max ≥ 8")
print("по min(Δr, Δc) (тонкие прямоугольники):")
for lo, hi in ((1, 1), (2, 3), (4, 7), (8, n - 1)):
    enrich(lambda a, b, lo=lo, hi=hi: lo <= min(a, b) <= hi, f"min ∈ [{lo},{hi}]")
