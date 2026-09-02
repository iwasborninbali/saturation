#!/usr/bin/env python3
"""cycle_null.py — теория для вопроса 3 плана 2.09 («длинные циклы»), считается ДО чтения данных.

2n-решение no-3-in-line: 2 точки в строке и в столбце ⇒ двудольный граф строки–столбцы 2-регулярен ⇒
объединение чётных циклов; цикл с k строками и k столбцами называем k-циклом (k ≥ 2; k=2 — прямоугольник).
Тип λ — разбиение n на части ≥ 2.  Записать конфигурацию как пару перестановок (a, b) строк→столбцов с a(r)≠b(r):
строки ходят по циклам перестановки π = b⁻¹a, и k-цикл графа = k-цикл π.

(1) Два нуля.  Равномерная ПАРА (a,b) (так сделан нуль в cycles.py) — это равномерная перестановка-деранжемент π:
    P_ab(λ) ∝ 1/∏ k^{m_k} m_k!.  Но конфигурация с c циклами представляется 2^c упорядоченными парами (в каждом
    цикле два способа сказать, какое из двух рёбер строки — «a»).  Равномерная КОНФИГУРАЦИЯ — правильный нуль:
    P_conf(λ) ∝ 1/(∏ k^{m_k} m_k! · 2^c);  Σ_λ = [tⁿ] (1−t)^{−1/2} e^{−t/2}   (число конфигураций = (n!)² · этот коэффициент
    — это A001499).  Асимптотика: P_conf(гамильтонов) → e^{1/2}√π /(2√n) ≈ 1.46/√n;  P_conf(без 2-цикла) → e^{−1/4}.

(2) Лемма о первом моменте.  При условии λ распределение конфигурации инвариантно относительно независимых
    перестановок строк и столбцов, поэтому для k клеток в попарно разных строках и столбцах
    P(все заняты | λ) = E[N_k | λ] / (n)_k, где N_k — число систем различных представителей множеств
    S_i = {r_i, π⁻¹(r_i)}.  Для k=3: E[N_3 | λ] = 8 − 12/(n−1) при ЛЮБОМ λ без единичных циклов (вывод в vtora/RESULTS.md),
    значит E[#коллинеарных троек | λ] = N₃ᵒᵇˡ(n) · (8 − 12/(n−1))/(n(n−1)(n−2)) не зависит от типа циклов:
    первый момент слеп к длине циклов.  Здесь это проверяется перебором (E[N_k|λ] точно, по подмножествам строк)
    и выборкой (среднее T по случайным конфигурациям заданного типа).

usage: python3 cycle_null.py nulls [n ...]      — точные нули P_conf / P_ab: гамильтонов, без 2-цикла, распределение числа циклов
       python3 cycle_null.py moments n           — E[N_3], E[N_4], E[N_5] точно для набора типов (перебор подмножеств строк)
       python3 cycle_null.py sample n samples    — выборочное среднее числа коллинеарных троек T по типам против леммы
"""
import sys, math, random, itertools
from fractions import Fraction
from collections import Counter, defaultdict


# ---------- разбиения на части ≥ 2 и веса двух нулей ----------
def partitions_min2(n, maxpart=None):
    if maxpart is None: maxpart = n
    if n == 0: yield (); return
    for k in range(min(n, maxpart), 1, -1):
        if n - k == 1: continue
        for rest in partitions_min2(n - k, k):
            yield (k,) + rest

def weights(n):
    """λ -> (w_ab, w_conf) без нормировки: 1/∏k^m m!  и то же /2^c."""
    out = {}
    for lam in partitions_min2(n):
        m = Counter(lam); w = Fraction(1)
        for k, mk in m.items(): w /= Fraction(k) ** mk * math.factorial(mk)
        out[lam] = (w, w / Fraction(2) ** len(lam))
    return out

def nulls(n):
    W = weights(n); Zab = sum(w for w, _ in W.values()); Zc = sum(w for _, w in W.values())
    ham = (n,)
    p_ab = {lam: w / Zab for lam, (w, _) in W.items()}; p_c = {lam: w / Zc for lam, (_, w) in W.items()}
    def agg(p, f):
        d = defaultdict(Fraction)
        for lam, q in p.items(): d[f(lam)] += q
        return dict(d)
    res = {
        "n": n, "types": len(W),
        "ab_ham": p_ab[ham], "conf_ham": p_c[ham],
        "ab_has2": sum(q for lam, q in p_ab.items() if 2 in lam), "conf_has2": sum(q for lam, q in p_c.items() if 2 in lam),
        "ab_has3": sum(q for lam, q in p_ab.items() if 3 in lam), "conf_has3": sum(q for lam, q in p_c.items() if 3 in lam),
        "ab_cycles": agg(p_ab, len), "conf_cycles": agg(p_c, len),
        "conf_Z": Zc,
    }
    # проверка: Σ_λ w_conf = [tⁿ](1−t)^{−1/2}e^{−t/2}, число конфигураций (n!)²·Zc должно быть целым (A001499)
    res["A001499"] = Zc * math.factorial(n) ** 2
    return res


# ---------- E[N_k | λ] точно: перебор k-подмножеств строк при канонической π типа λ ----------
def perm_of_type(lam, n):
    pi = list(range(n)); i = 0
    for k in lam:
        blk = list(range(i, i + k))
        for j in range(k): pi[blk[j]] = blk[(j + 1) % k]
        i += k
    return pi

def sdr_count(sets):
    """число систем различных представителей (перебор, множества маленькие)."""
    cnt = 0
    for choice in itertools.product(*sets):
        if len(set(choice)) == len(choice): cnt += 1
    return cnt

def moments(n, types, kmax=5):
    rows = []
    for lam in types:
        pi = perm_of_type(lam, n); inv = [0] * n
        for x in range(n): inv[pi[x]] = x
        S = [(r, inv[r]) for r in range(n)]
        ex = []
        for k in range(3, kmax + 1):
            tot = 0; cnt = 0
            for sub in itertools.combinations(range(n), k):
                tot += sdr_count([S[r] for r in sub]); cnt += 1
            ex.append(Fraction(tot, cnt))
        rows.append((lam, ex))
    return rows


# ---------- коллинеарные тройки клеток в косых направлениях и выборочная проверка леммы ----------
def oblique_lines(n):
    """все прямые с ≥3 клетками, не горизонтальные и не вертикальные: список длин."""
    lens = []
    dirs = set()
    for dx in range(1, n):
        for dy in range(-(n - 1), n):
            if dy == 0 or math.gcd(dx, abs(dy)) != 1: continue
            dirs.add((dx, dy))
    for dx, dy in dirs:
        for x in range(n):
            for y in range(n):
                px, py = x - dx, y - dy
                if 0 <= px < n and 0 <= py < n: continue     # не начало прямой
                L = 0; cx, cy = x, y
                while 0 <= cx < n and 0 <= cy < n: L += 1; cx += dx; cy += dy
                if L >= 3: lens.append(L)
    return lens

def N3_oblique(n): return sum(math.comb(L, 3) for L in oblique_lines(n))

def random_config_of_type(lam, n, rnd):
    """равномерная конфигурация данного типа: случайная разметка строк для π типа λ и случайная a."""
    labels = list(range(n)); rnd.shuffle(labels)
    pi0 = perm_of_type(lam, n); pi = [0] * n
    for x in range(n): pi[labels[x]] = labels[pi0[x]]
    a = list(range(n)); rnd.shuffle(a)
    # столбец a(r) соединён со строками r и π(r)  (см. вывод: b = a∘π⁻¹)
    pts = set()
    for r in range(n):
        pts.add((r, a[r])); pts.add((pi[r], a[r]))
    assert len(pts) == 2 * n
    return sorted(pts)

def collinear_triples(pts):
    """число коллинеарных троек среди точек (по прямым через пары; без строк/столбцов их и нет)."""
    lines = defaultdict(set); P = pts; m = len(P)
    for i in range(m):
        x1, y1 = P[i]
        for j in range(i + 1, m):
            x2, y2 = P[j]; dx, dy = x2 - x1, y2 - y1
            g = math.gcd(abs(dx), abs(dy)); dx //= g; dy //= g
            if dx < 0 or (dx == 0 and dy < 0): dx, dy = -dx, -dy
            c = dx * y1 - dy * x1
            lines[(dx, dy, c)].update((i, j))
    return sum(math.comb(len(s), 3) for s in lines.values() if len(s) >= 3)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "nulls"
    if cmd == "nulls":
        ns = [int(x) for x in sys.argv[2:]] or list(range(8, 21))
        print(f"{'n':>3} {'типов':>5} | {'P_ab(гам)':>9} {'P_conf(гам)':>11} {'1.46/√n':>8} | {'P_ab(2цикл)':>11} {'P_conf(2цикл)':>13} | {'P_ab(3цикл)':>11} {'P_conf(3цикл)':>13} | A001499(n)")
        for n in ns:
            r = nulls(n)
            print(f"{n:>3} {r['types']:>5} | {float(r['ab_ham']):>9.4f} {float(r['conf_ham']):>11.4f} {math.e**.5*math.pi**.5/2/n**.5:>8.4f} | "
                  f"{float(r['ab_has2']):>11.4f} {float(r['conf_has2']):>13.4f} | {float(r['ab_has3']):>11.4f} {float(r['conf_has3']):>13.4f} | {r['A001499']}")
        n = ns[-1]; r = nulls(n)
        print(f"\nраспределение числа циклов c при n={n}:  c: P_ab / P_conf")
        for c in sorted(r["conf_cycles"]):
            print(f"  {c}: {float(r['ab_cycles'][c]):.4f} / {float(r['conf_cycles'][c]):.4f}")
    elif cmd == "moments":
        n = int(sys.argv[2])
        types = [(n,), (2, n - 2), (3, n - 3), (n // 2, n - n // 2), (2,) * (n // 2) if n % 2 == 0 else (3,) + (2,) * ((n - 3) // 2),
                 (4,) * (n // 4) + ((n % 4,) if n % 4 >= 2 else ()) if n % 4 != 1 else (5,) + (4,) * ((n - 5) // 4), (2, 2, n - 4), (2, 3, n - 5)]
        types = [t for t in types if sum(t) == n and min(t) >= 2]
        print(f"n={n}: точные E[N_k | λ] (лемма: E[N_3] = 8 − 12/(n−1) = {8 - 12 / (n - 1):.6f} для всех λ)")
        for lam, ex in moments(n, types):
            print(f"  λ={lam}: " + "  ".join(f"E[N_{k}]={float(e):.6f}" for k, e in zip(range(3, 3 + len(ex)), ex)))
    elif cmd == "sample":
        n = int(sys.argv[2]); S = int(sys.argv[3]); rnd = random.Random(20260902)
        N3 = N3_oblique(n); mu = N3 * (8 - 12 / (n - 1)) / (n * (n - 1) * (n - 2))
        print(f"n={n}: косых коллинеарных троек клеток N3={N3}; лемма предсказывает E[T | λ] = {mu:.4f} для всех λ")
        types = [(n,), (2, n - 2), (3, n - 3), (n // 2, n - n // 2), (2,) * (n // 2) if n % 2 == 0 else (3,) + (2,) * ((n - 3) // 2), (4,) * (n // 4) + ((n % 4,) if n % 4 >= 2 else ())]
        types = [t for t in types if sum(t) == n and min(t) >= 2]
        for lam in types:
            xs = [collinear_triples(random_config_of_type(lam, n, rnd)) for _ in range(S)]
            m = sum(xs) / S; sd = (sum((x - m) ** 2 for x in xs) / (S - 1)) ** .5; se = sd / S ** .5
            z = (m - mu) / se
            print(f"  λ={str(lam):<32} среднее T = {m:8.4f} ± {se:.4f}  (z = {z:+.2f})  {'в пределах 2 SE' if abs(z) <= 2 else 'РАСХОЖДЕНИЕ'}")
