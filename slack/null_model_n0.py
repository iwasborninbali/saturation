"""null_model_n0.py — нулевая модель N0(p) для пары гипербол в окне 2p×2p (deep_research_8 §10.4).

N0(p): случайное множество из 8(p−1) точек бокса [0,2p)×[0,2p) ровно по 4 в каждой строке и каждом
столбце — та же геометрия, что у пары {H(1),H(−1)} с 4-лифтом, без арифметики гипербол.
α(N0) — точный максимум подмножества без трёх коллинеарных (MILP HiGHS через scipy; свидетель
перепроверяется независимым перебором всех троек). Вопрос: ложится ли α(N0)/(p−1) на плато
3.44–3.49, которое сертификаты не пробивают? Если да — плато есть значение нулевой модели.

Выборка: четыре последовательных случайных паросочетания строк со столбцами без повторных клеток
(случайные аугментирующие пути); это НЕ равномерное распределение на 4-регулярных бипартитных
графах — закон выборки назван, чтобы противник мог его оспорить.
usage: null_model_n0.py p samples [seed]
"""
import sys, os, random, time
from math import gcd
from itertools import combinations
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds


def lines(cands):
    """все максимальные коллинеарные подмножества (>=3) кандидатов, как кортежи индексов
    (копия maxlawful_pysat.lines: тот модуль тянет pysat, которого на VM может не быть)."""
    seen = set(); out = []; n = len(cands)
    for i in range(n):
        for j in range(i + 1, n):
            (x1, y1), (x2, y2) = cands[i], cands[j]
            dx, dy = x2 - x1, y2 - y1; g = gcd(abs(dx), abs(dy)); dx //= g; dy //= g
            if dx < 0 or (dx == 0 and dy < 0): dx, dy = -dx, -dy
            c0 = dx * y1 - dy * x1
            key = (dx, dy, c0)
            if key in seen: continue
            seen.add(key)
            mem = [k for k, (x, y) in enumerate(cands) if dx * y - dy * x == c0]
            if len(mem) >= 3: out.append(tuple(mem))
    return out


def random_matching(rows, cols, forbidden, rng):
    """случайное совершенное паросочетание rows со cols, избегая forbidden[r] (случайные аугментирующие пути)."""
    match_col = {c: None for c in cols}
    order = list(rows); rng.shuffle(order)
    def augment(r, seen):
        cs = [c for c in cols if c not in forbidden[r]]; rng.shuffle(cs)
        for c in cs:
            if c in seen: continue
            seen.add(c)
            if match_col[c] is None or augment(match_col[c], seen):
                match_col[c] = r; return True
        return False
    for r in order:
        if not augment(r, set()): return None
    return {r: c for c, r in match_col.items()}


def sample_n0(p, rng):
    """8(p−1) точек: по 4 в каждой из 2(p−1) строк и столбцов; строки и столбцы с индексом ≡ 0 (mod p)
    пусты — как у гиперболы xy ≡ c (mod p) в окне [0,2p)², где x ≡ 0 и y ≡ 0 точек не несут."""
    rows = [r for r in range(2 * p) if r % p != 0]; cols = list(rows)
    while True:
        used = {r: set() for r in rows}; pts = []; ok = True
        for _ in range(4):
            m = random_matching(rows, cols, used, rng)
            if m is None: ok = False; break
            for r, c in m.items(): used[r].add(c); pts.append((c, r))
        if ok:
            assert len(pts) == 8 * (p - 1)
            return sorted(pts)


def alpha_exact(cands):
    L = lines(cands); n = len(cands)
    A = np.zeros((max(1, len(L)), n))
    for k, mem in enumerate(L):
        for i in mem: A[k, i] = 1.0
    res = milp(c=-np.ones(n), constraints=LinearConstraint(A, -np.inf, 2.0),
               integrality=np.ones(n), bounds=Bounds(0, 1))
    assert res.status == 0, f"MILP не оптимален: {res.message}"
    chosen = [cands[i] for i in range(n) if res.x[i] > 0.5]
    for (x1, y1), (x2, y2), (x3, y3) in combinations(chosen, 3):   # независимая проверка закона
        assert (x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1) != 0, "свидетель нарушает закон"
    return len(chosen), chosen


if __name__ == "__main__":
    p, samples = int(sys.argv[1]), int(sys.argv[2]); seed = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    rng = random.Random(seed)
    print(f"N0(p={p}): {8*(p-1)} точек в боксе {2*p}×{2*p}, по 4 в строке и столбце; выборок {samples}, seed {seed}")
    vals = []
    for s in range(samples):
        t0 = time.time(); cands = sample_n0(p, rng)
        rows = {}; cols = {}
        for x, y in cands: rows[y] = rows.get(y, 0) + 1; cols[x] = cols.get(x, 0) + 1
        assert set(rows.values()) == {4} and set(cols.values()) == {4}
        a, _ = alpha_exact(cands); vals.append(a)
        print(f"  образец {s+1}: α = {a}  ({a/(p-1):.3f}(p−1))  за {time.time()-t0:.1f} с", flush=True)
    mean = sum(vals) / len(vals)
    print(f"α: {sorted(vals)}; среднее {mean:.2f} = {mean/(p-1):.3f}(p−1); диапазон [{min(vals)/(p-1):.2f}, {max(vals)/(p-1):.2f}]")
