"""test_numbers.py — числа спецификации против самих себя, против измерения и против данных проекта.

Линза: ЧИСЛЕННАЯ СОГЛАСОВАННОСТЬ.  phenomenon.py несёт ровно один количественный экземпляр явления
(OUR_SIGNATURE) и один порог-детектор (Signature.verdict).  Здесь эти шесть чисел проверяются
(а) друг против друга (точное тождество рукопожатия для 3-однородной системы),
(б) против ИЗМЕРЕНИЯ реального множества кандидатов P₋₁ (инструмент ниже; он валидируется против
    опубликованных чисел §11 заметок, прежде чем использоваться как улика),
(в) против чисел, записанных в pair_bound_notes.md (§2, §4, §7, B.2, B.7, B.17), в REPORT §16 и в
    holes.py (H1.testable_now),
(г) против того, чего в числах вердикта НЕТ (раздел H): §3 объявляет ШЕСТЬ признаков S1–S6, verdict()
    печатает знаменатель 4, а поле mean_degree не читается ни одним условием.

Коробка кандидатов — каноническая для проекта (§12: X(u) ∈ [−h,h] — наименьший абсолютный вычет по x,
Y(u) ∈ [1,p−1] — наименьший положительный по y; четыре лифта (X+ip, Y+jp) на класс).  Инструмент
воспроизводит §11 точно: p=29 → по наклону +1 размеры 8:4, 7:2, 6:6, 5:2; p=199 → 164 прямые ≥5 точек
на оба наклона.  Это проверяется тестом ПЕРВЫМ.
"""
import dataclasses
import math
import os
import re
import sys
import unittest
from collections import defaultdict
from math import gcd, isqrt

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)                       # tests/gaps.py
sys.path.insert(0, os.path.dirname(_HERE))      # phenomenon.py, holes.py

from gaps import gap
import phenomenon as P
import holes as H

# ───────────────────────── данные проекта (цитаты, не пересчитываемые здесь) ─────────────────────────
#
# pair_bound_notes.md §B.2, строки k = −1 (в таблице k записано как p−1: 13,12 / 17,16 / 19,18):
#   p : (LP(1) = строки+столбцы+наклоны ±1,  LP(∞) = все богатые прямые,  α = точный максимум)
B2_KM1 = {13: (48.0, 44.8, 40), 17: (62.0, 60.2, 54), 19: (64.0, 63.6, 59)}
# LP(1) — единственная «LP только по сильным» величина, записанная в проекте.  Она БОЛЬШЕ, чем LP по
# сильным ограничениям в смысле самого модуля (|ℓ| ≥ 2·cap+1 = 5 — по измерению ниже это ровно прямые
# наклона ±1, без строк и столбцов): убрав строки и столбцы, LP только вырастет.  Поэтому отношение
# LP(все)/LP(сильные) в смысле докстринга ≤ приведённого здесь, и признак S2 от этой замены может
# только ухудшиться — все выводы ниже устойчивы к выбору чтения.
# pair_bound_notes.md §2: «23 | −1 | 70–74» — точный максимум при p = 23 не определён данными проекта.
ALPHA_23_KM1 = (70, 74)
# pair_bound_notes.md §4: «p=11: … k=−1 → 31 (true α: 33, 35, 32?)» → α(P₋₁)(11) = 32 (со знаком вопроса
# в заметках; в holes.py то же число записано БЕЗ оговорки, как «точный max»).
#
# B.17 (замечание, на которое опирается шаг 4 model_theorem_conditional.md):
#   «N₀ = max #patterns through a pair of classes ≤ 64·6 = 384 (64 point pairs, ≤ 6 patterns per line)»
B17_CODEGREE_OF_A_CLASS_PAIR = 64 * 6

# Точные максимумы α(P_k) по (p, k): §2 (таблица; k = 2,3 при p = 11, k = 2 при p = 13, k = −1 при 17,19),
# §4 («p=11: … k=−1 → 31 (true α: 33, 35, 32?)»), B.2 (строка 13,12 ⇒ α = 40 при k = −1).
NOTES_ALPHA_BY_K = {11: {2: 33, 3: 35, -1: 32}, 13: {2: 41, -1: 40}, 17: {-1: 54}, 19: {-1: 59}}
# §7 («α does not depend much on k»): диапазон по ВСЕМ k, независимая проверка верхних концов.
NOTES_ALPHA_RANGE_OVER_K = {11: (32, 35), 13: (38, 41), 17: (49, 54)}

# B.2, все семь посчитанных строк: (p, k) → (LP(1), LP(∞)); k = −1 записан в таблице как p−1.
B2_LP_ALL_K = {(11, 3): (36.0, 36.0), (11, 2): (38.9, 37.6), (13, 2): (48.0, 47.5), (13, -1): (48.0, 44.8),
               (17, -1): (62.0, 60.2), (17, 2): (63.5, 61.6), (19, -1): (64.0, 63.6)}

# B.7: LP(1) — ЛОКАЛЬНЫЙ сертификат (строки/столбцы/±1) — выходит на плато ≈ 3.45(p−1) на 40 простых p ≤ 199.
# REPORT §16 (ответ хозяину): «3.45 — потолок локальных сертификатов … не путь к правде».
LP1_PLATEAU_B7 = 3.45
# model_theorem_conditional.md §23: λ_min(C)/√m₂ измерено при p = 199…4001 — числовое содержание S5.
LAMBDA_MIN_OVER_SQRT_M2 = {199: -1.94, 499: -1.87, 997: -1.94, 1999: -2.01, 4001: -2.08}

PRIME_OF_OUR_SIGNATURE = 1999          # phenomenon.py: n_ground = 8*(p := 1999) - 8


# ─────────────────────────────── инструмент: измерение системы ───────────────────────────────

def candidates(p, k=-1):
    """8(p−1) лифтов H(1) ∪ H(k) в коробке 2p×2p — каноническая коробка §12 заметок."""
    h = (p - 1) // 2
    pts = []
    for a in range(1, p):
        ai = pow(a, p - 2, p)
        x0 = a - p if a > h else a                     # X(a) ∈ [−h, h]
        for yr in (ai, (k * ai) % p):                  # Y(·) ∈ [1, p−1]
            for i in (0, 1):
                for j in (0, 1):
                    pts.append((x0 + i * p, yr + j * p))
    return sorted(set(pts))


def _line_sizes(pts):
    """{размер прямой: сколько таких прямых} — только счёт пар, без хранения множеств (быстро)."""
    cnt = {}
    get = cnt.get
    n = len(pts)
    B = 4 * max(abs(x) for x, _ in pts) + 8
    for i in range(n):
        x1, y1 = pts[i]
        for j in range(i + 1, n):
            x2, y2 = pts[j]
            dx = x2 - x1
            dy = y2 - y1
            q = gcd(dx, dy) if dx >= 0 else -gcd(dx, dy)
            dx //= q
            dy //= q
            if dx == 0 and dy < 0:
                dy = -dy
            key = ((dx + B) * (2 * B) + (dy + B)) * (4 * B * B) + (dx * y1 - dy * x1)
            cnt[key] = get(key, 0) + 1
    out = defaultdict(int)
    for c in cnt.values():
        m = (1 + isqrt(1 + 8 * c)) // 2
        assert m * (m - 1) // 2 == c, "ключ прямой не соответствует C(m,2) парам"
        out[m] += 1
    return dict(out)


def _lines_with_members(pts):
    """{(dx,dy,c): множество индексов точек} — нужно для костепеней; только для малых p."""
    L = defaultdict(set)
    n = len(pts)
    for i in range(n):
        x1, y1 = pts[i]
        for j in range(i + 1, n):
            x2, y2 = pts[j]
            dx = x2 - x1
            dy = y2 - y1
            g = gcd(abs(dx), abs(dy))
            dx //= g
            dy //= g
            if dx < 0 or (dx == 0 and dy < 0):
                dx, dy = -dx, -dy
            key = (dx, dy, dx * y1 - dy * x1)
            L[key].add(i)
            L[key].add(j)
    return L


_SIZES_CACHE = {}
_MEMBERS_CACHE = {}


def sizes(p):
    if p not in _SIZES_CACHE:
        _SIZES_CACHE[p] = _line_sizes(candidates(p))
    return _SIZES_CACHE[p]


def members(p):
    if p not in _MEMBERS_CACHE:
        _MEMBERS_CACHE[p] = _lines_with_members(candidates(p))
    return _MEMBERS_CACHE[p]


def codegree_over_weak(p):
    """Макс. число СЛАБЫХ ограничений (|ℓ| = cap+1 = 3, определение Frame/Strength) через пару точек."""
    pair = defaultdict(int)
    for S in members(p).values():
        if len(S) == 3:
            a, b, c = sorted(S)
            pair[(a, b)] += 1
            pair[(a, c)] += 1
            pair[(b, c)] += 1
    return max(pair.values())


def codegree_over_all_collinear_triples(p):
    """Макс. число КОЛЛИНЕАРНЫХ ТРОЕК через пару точек (чтение, запрещённое скобкой в P1)."""
    pair = defaultdict(int)
    for S in members(p).values():
        m = len(S)
        if m >= 3:
            Ss = sorted(S)
            for i in range(m):
                for j in range(i + 1, m):
                    pair[(Ss[i], Ss[j])] += m - 2
    return max(pair.values())


def handshake_defect(sig):
    """Точное тождество любой 3-однородной системы: Σ степеней = 3·|E| ⇒ mean_degree·|V| = 3·n_weak."""
    return sig.mean_degree * sig.n_ground - 3 * sig.n_weak


def measured_signature(p, gains):
    """Signature НАШЕЙ системы при данном p: всё, что можно измерить — измерено, LP — из B.2."""
    lp1, lp_inf, _alpha = B2_KM1[p]
    n_weak = sizes(p)[3]
    n_ground = len(candidates(p))
    return P.Signature(
        n_weak=n_weak,
        n_ground=n_ground,
        mean_degree=3 * n_weak / n_ground,
        max_codegree=codegree_over_weak(p),
        lp_all_over_lp_strong=lp_inf / lp1,
        gain_over_construction=gains,
    )


def holes_exact_maxima():
    """Точные максимумы, записанные в holes.py H1.testable_now: «(11: 32; 13: 40; 17: 54; 19: 59)»."""
    h1 = next(h for h in H.HOLES if h.key.startswith("H1"))
    tail = h1.testable_now.split("точным max")[1]
    return {int(a): int(b) for a, b in re.findall(r"(\d+):\s*(\d+)", tail)}


# ───────────────────────────────────── A. инструмент ──────────────────────────────────────

class TestInstrumentAgreesWithTheProject(unittest.TestCase):
    """Прежде чем измерением что-то опровергать, измеритель проверяется против §11 заметок."""

    def test_ground_set_is_8_p_minus_1(self):
        for p in (11, 13, 17, 19, 23, 29, 31):
            self.assertEqual(len(candidates(p)), 8 * (p - 1))

    def test_reproduces_published_pm1_line_spectrum_at_p29(self):
        # §11: «p = 29: 8:4, 7:2, 6:6, 5:2 per slope»
        spec = defaultdict(int)
        for (dx, dy, _c), S in members(29).items():
            if len(S) >= 5 and (dx, dy) == (1, 1):
                spec[len(S)] += 1
        self.assertEqual(dict(spec), {8: 4, 7: 2, 6: 6, 5: 2})

    def test_reproduces_published_count_of_rich_lines_at_p199(self):
        # §11: «p = 199: 164 lines ≥ 5 over both slopes»
        s = sizes(199)
        self.assertEqual(sum(n for m, n in s.items() if m >= 5), 164)

    def test_every_line_with_at_least_five_points_has_slope_pm1(self):
        # подтверждает прозу рамок: «СИЛЬНЫЕ … У нас — строки, столбцы, прямые наклона ±1 (до 8 точек)»
        for p in (17, 19, 23, 29, 31):
            dirs = {(dx, dy) for (dx, dy, _c), S in members(p).items() if len(S) >= 5}
            self.assertEqual(dirs, {(1, 1), (1, -1)}, f"p={p}")
            self.assertLessEqual(max(len(S) for S in members(p).values()), 8, f"p={p}")


# ───────────────────────────── B. тождество рукопожатия ─────────────────────────────

class TestHandshakeIdentity(unittest.TestCase):
    """3·n_weak = mean_degree·n_ground — точный инвариант, а не приближение."""

    def test_invariant_holds_on_a_genuinely_measured_system(self):
        """Сорт A: инвариант, который ДЕРЖИТСЯ, когда числа действительно измерены."""
        for p in (13, 17, 19):
            sig = measured_signature(p, (2, 4, 6, 5))
            self.assertAlmostEqual(handshake_defect(sig), 0.0, places=9, msg=f"p={p}")

    def test_module_builds_exactly_one_signature_and_it_is_the_only_one_checkable(self):
        built = [(n, v) for n, v in vars(P).items() if isinstance(v, P.Signature)]
        self.assertEqual([n for n, _ in built], ["OUR_SIGNATURE"])
        sig = P.OUR_SIGNATURE
        self.assertEqual(sig.mean_degree * sig.n_ground, 399600.0)
        self.assertEqual(3 * sig.n_weak, 300000)
        self.assertAlmostEqual(handshake_defect(sig) / (3 * sig.n_weak), 0.332, places=3)

    def test_n_ground_is_the_only_field_that_survives_arithmetic(self):
        """Сорт A: n_ground = 8(p−1) — единственное число OUR_SIGNATURE, проверяемое в одну строку."""
        self.assertEqual(P.OUR_SIGNATURE.n_ground, 8 * (PRIME_OF_OUR_SIGNATURE - 1))
        self.assertEqual(P.OUR_SIGNATURE.n_ground, 15984)

    def test_which_of_the_two_incompatible_numbers_was_never_measured(self):
        """S1 обещает «степени ~ log |V|».  Измеряем степень при p = 101, 151, 199: она растёт
        БЫСТРЕЕ ln p (отношение md/ln p само растёт 2.92 → 3.44 → 3.59).

        Пара (n_weak = 1e5, n_ground = 15984) означает среднюю степень 18.77 при p = 1999 — МЕНЬШЕ
        измеренной при p = 199 (18.99), т.е. требует ПАДЕНИЯ степени на системе в 10 раз большей.
        Объявленная mean_degree = 25.0 (3.29·ln p) хотя бы лежит внутри измеренной полосы (снизу).
        Значит несовместимую пару разрешает измерение: рвётся n_weak, и рвётся вниз.
        """
        band = {}
        for p in (101, 151, 199):
            md = 3 * sizes(p)[3] / (8 * (p - 1))
            band[p] = md / math.log(p)
        self.assertEqual(sorted(band, key=band.get), [101, 151, 199])   # полоса не плато: она растёт
        self.assertAlmostEqual(3 * sizes(199)[3] / (8 * 198), 18.992, places=3)

        implied = 3 * P.OUR_SIGNATURE.n_weak / P.OUR_SIGNATURE.n_ground
        self.assertAlmostEqual(implied, 18.769, places=3)
        self.assertGreater(3 * sizes(199)[3] / (8 * 198), implied)      # p=199 плотнее, чем «p=1999»

        lnp = math.log(PRIME_OF_OUR_SIGNATURE)
        self.assertLess(implied / lnp, min(band.values()))              # 2.47 < 2.92 — вне полосы
        self.assertGreaterEqual(P.OUR_SIGNATURE.mean_degree / lnp, min(band.values()))
        self.assertLessEqual(P.OUR_SIGNATURE.mean_degree / lnp, max(band.values()))   # 3.29 ∈ [2.92, 3.59]
        # …но полоса растёт, так что даже объявленные 25.0 ниже темпа последней измеренной точки:
        self.assertLess(P.OUR_SIGNATURE.mean_degree, band[199] * lnp)   # 25.0 < 27.3


# ───────────────────────────────── C. костепень «6» ──────────────────────────────────

class TestMaxCodegreeHasNoObject(unittest.TestCase):
    """max_codegree = 6 объявлено как «макс. число слабых ограничений через пару точек»."""

    def test_codegree_over_weak_constraints_is_exactly_one(self):
        """Две различные точки лежат ровно на ОДНОЙ прямой ⇒ костепень по |ℓ|=3 ограничениям ≤ 1."""
        for p in (13, 17, 19, 23, 29, 31):
            self.assertEqual(codegree_over_weak(p), 1, f"p={p}")

    def test_therefore_S3_is_satisfied_by_every_point_line_system(self):
        """Порог «≤ 8» при костепени, тождественно равной 1, не различает ничего:
        любая система «точки/прямые» из бестиария (no-three-in-line, дуги PG(2,q), наша) проходит S3
        по построению, т.е. одно из четырёх условий verdict() информации не несёт."""
        for p in (13, 17, 19):
            sig = measured_signature(p, (2, 4, 6, 5))
            self.assertLessEqual(sig.max_codegree, 8)
            self.assertEqual(sig.max_codegree, 1)
        for p in (23, 29, 31):
            self.assertLessEqual(codegree_over_weak(p), 8)

    def test_six_is_the_codegree_of_the_reading_P1_explicitly_forbids(self):
        """P1: «здесь и далее только 3-точечные прямые».  Если же H₃ — ВСЕ коллинеарные тройки
        (включая подтройки богатых прямых), костепень пары = (макс. размер прямой) − 2 = 8 − 2 = 6.
        Число 6 верно ровно в том чтении, которое спецификация запрещает."""
        for p in (19, 23, 29, 31):
            longest = max(len(S) for S in members(p).values())
            self.assertEqual(longest, 8, f"p={p}")
            self.assertEqual(codegree_over_all_collinear_triples(p), longest - 2, f"p={p}")
            self.assertEqual(codegree_over_all_collinear_triples(p), P.OUR_SIGNATURE.max_codegree, f"p={p}")

    def test_the_codegree_the_project_actually_uses_fails_the_S3_threshold(self):
        """B.17 (шаг 4 model_theorem_conditional.md) ограничивает костепень ПАРЫ КЛАССОВ: N₀ ≤ 64·6 = 384 —
        единственная костепень, которая в проекте что-то доказывает, и она в 48 раз выше порога S3.
        Клетка S3 решается целиком тем, какой объект назвать: 384 → признак теряется, 1 (объект,
        разрешённый скобкой в P1) → признак выполняется тождественно.  Информации о явлении нет ни там, ни там."""
        def with_codegree(c):
            return P.Signature(n_weak=10 ** 5, n_ground=15984, mean_degree=18.77, max_codegree=c,
                               lp_all_over_lp_strong=0.985, gain_over_construction=(5, 5, 6, 5))
        self.assertIn("3/4", with_codegree(B17_CODEGREE_OF_A_CLASS_PAIR).verdict())
        self.assertIn("4/4", with_codegree(codegree_over_weak(19)).verdict())

    @gap("GAP-N-02",
         module="phenomenon.py",
         title="max_codegree = 6 не описывает ни один объект системы; S3 либо тавтология, либо ложь",
         expected="Signature.max_codegree объявлен как «макс. число слабых ограничений через пару точек», "
                  "а слабое ограничение по Frame/Strength — это прямая с |ℓ| = cap+1 = 3; измеренная "
                  "костепень пары точек по таким ограничениям должна равняться объявленным 6",
         actual="она тождественно равна 1 при каждом p (две точки лежат ровно на одной прямой). "
                "6 = 8 − 2 — костепень в чтении «H₃ = все коллинеарные тройки, включая подтройки "
                "богатых прямых», которое скобка в P1 («здесь и далее только 3-точечные прямые») "
                "запрещает; а костепень объекта, который проект действительно ограничивает "
                "(пара КЛАССОВ, B.17), равна 384",
         consequence="S3 «малые костепени» — одно из четырёх условий verdict() — либо выполняется "
                     "тождественно (тогда оно не отличает наше явление ни от какой системы точек и "
                     "прямых, включая все геометрические пункты бестиария), либо нарушено в 48 раз "
                     "тем самым числом 384, на котором держится шаг 4 model_theorem_conditional.md "
                     "(m₂ ≤ K₀·E/(p−1)).  В обоих случаях «4/4 признаков» — это 3/4 плюс пустая клетка")
    def test_declared_codegree_is_the_codegree_of_an_object_of_the_system(self):
        # Какое чтение H₃ разрешено — решает скобка в P1.  Тест закрывается ЛЮБЫМ исправлением
        # спецификации: если число заменят на 1, сойдётся первое чтение; если скобку уберут
        # (H₃ = все коллинеарные тройки) — сойдётся второе.  Сейчас не сходится никакое.
        licences_only_three_point_lines = re.search(r"здесь и далее только 3.точечные прямые", P.__doc__)
        measure = codegree_over_weak if licences_only_three_point_lines else codegree_over_all_collinear_triples
        for p in (19, 23, 29):
            self.assertEqual(measure(p), P.OUR_SIGNATURE.max_codegree, f"p={p}")


# ─────────────────────────── D. вектор прибавок над конструкцией ────────────────────────────

class TestGainOverConstruction(unittest.TestCase):
    """gain_over_construction = (5,5,6,5) — единственная численная опора P4/S4 и гипотезы 3(p−1)+O(1)."""

    def test_holes_py_records_different_maxima_for_the_same_four_primes(self):
        maxima = holes_exact_maxima()
        self.assertEqual(maxima, {11: 32, 13: 40, 17: 54, 19: 59})
        gains_from_holes = tuple(maxima[q] - 3 * (q - 1) for q in (11, 13, 17, 19))
        self.assertEqual(gains_from_holes, (2, 4, 6, 5))
        self.assertEqual(tuple(P.OUR_SIGNATURE.gain_over_construction), (5, 5, 6, 5))
        # обратный пересчёт: какие максимумы утверждает phenomenon.py
        implied = tuple(3 * (q - 1) + g for q, g in zip((11, 13, 17, 19), (5, 5, 6, 5)))
        self.assertEqual(implied, (35, 41, 54, 59))
        self.assertNotEqual(implied, tuple(maxima[q] for q in (11, 13, 17, 19)))

    def test_the_phenomenon_vector_is_a_maximum_over_k_not_our_frames_system(self):
        """OUR_FRAME фиксирует k = −1 («две гиперболы xy ≡ ±1»).  Максимумы, подразумеваемые объявленным
        вектором, — это max ПО k из §2/§7 (35 при k=3, 41 при k=2), а не строка k = −1 (32, 40 по §4/B.2).
        Две из четырёх координат измерены на ДРУГИХ вторых гиперболах."""
        self.assertIn("xy ≡ ±1", P.OUR_FRAME.ground_set)
        implied = tuple(3 * (q - 1) + g
                        for q, g in zip((11, 13, 17, 19), P.OUR_SIGNATURE.gain_over_construction))
        self.assertEqual(implied, tuple(max(NOTES_ALPHA_BY_K[q].values()) for q in (11, 13, 17, 19)))
        for q in (11, 13):                                      # где максимум берётся не на k = −1
            best_k = max(NOTES_ALPHA_BY_K[q], key=NOTES_ALPHA_BY_K[q].get)
            self.assertNotEqual(best_k, -1, f"p={q}")
            self.assertEqual(NOTES_ALPHA_BY_K[q][best_k], NOTES_ALPHA_RANGE_OVER_K[q][1])   # §7, независимо
        self.assertEqual(tuple(NOTES_ALPHA_BY_K[q][-1] for q in (11, 13, 17, 19)),
                         tuple(holes_exact_maxima()[q] for q in (11, 13, 17, 19)))  # holes.py = строка k = −1

    def test_S4_flips_between_the_two_vectors(self):
        def spread(v):
            return max(v) - min(v)
        self.assertEqual(spread((5, 5, 6, 5)), 1)               # проходит порог ≤ 3
        self.assertEqual(spread((2, 4, 6, 5)), 4)               # не проходит

    def test_S4_is_blind_to_the_order_and_passes_a_vector_that_grows_at_every_step(self):
        """Честный вектор РАСТЁТ на 11 → 13 → 17 (2 → 4 → 6) — ровно то, что S4 обязан ловить, — но
        падает он не из-за роста: условие max−min ≤ 3 инвариантно к перестановке, так что растущая
        и убывающая последовательности получают один ответ, а (0,1,2,3) — строгий рост на каждом
        шаге — признак «прибавка не растёт» ПРОХОДИТ."""
        gains = tuple(holes_exact_maxima()[q] - 3 * (q - 1) for q in (11, 13, 17, 19))
        self.assertEqual(gains[:3], (2, 4, 6))
        self.assertLess(gains[0], gains[1])
        self.assertLess(gains[1], gains[2])

        def s4(v):
            return max(v) - min(v) <= 3

        self.assertEqual(s4(gains), s4(tuple(reversed(gains))))
        self.assertTrue(s4((0, 1, 2, 3)))
        self.assertTrue(s4((3, 2, 1, 0)))

    def test_the_next_prime_is_undetermined_in_the_projects_own_data(self):
        """§2: «23 | −1 | 70–74».  Прибавка при p = 23 лежит в [4, 8] и накрывает объявленный
        максимум 6 с обеих сторон: данные проекта не решают, растёт ли прибавка."""
        lo, hi = ALPHA_23_KM1
        self.assertEqual((lo - 3 * 22, hi - 3 * 22), (4, 8))
        self.assertLess(4, max(P.OUR_SIGNATURE.gain_over_construction))
        self.assertGreater(8, max(P.OUR_SIGNATURE.gain_over_construction))

    @gap("GAP-N-03",
         module="phenomenon.py + holes.py",
         title="phenomenon.py и holes.py называют разные точные максимумы для одних и тех же p = 11,13,17,19",
         expected="gain_over_construction = «max − 3(p−1)» при p = 11,13,17,19 для системы OUR_FRAME "
                  "(xy ≡ ±1, т.е. k = −1) должно совпадать с точными максимумами, записанными в "
                  "holes.py H1.testable_now: (11: 32; 13: 40; 17: 54; 19: 59) ⇒ (2, 4, 6, 5)",
         actual="phenomenon.py объявляет (5, 5, 6, 5), т.е. максимумы (35, 41, 54, 59): это максимум ПО k "
                "(35 = α при k = 3, 41 = α при k = 2 — §2 заметок), а не значения системы, которую "
                "описывает OUR_FRAME.  Два приложения одного и того же брифа противоречат друг другу",
         consequence="S4 («прибавка не растёт») — единственный признак, отличающий нас от cap sets, и "
                     "единственная численная опора гипотезы α = 3(p−1)+O(1) — на объявленном векторе "
                     "имеет разброс 1 и проходит, а на векторе из holes.py разброс 4 и не проходит; "
                     "к тому же честный вектор монотонно РАСТЁТ 2 → 4 → 6, а следующая точка данных "
                     "(p = 23: α ∈ [70,74], прибавка ∈ [4,8]) не определена в самих заметках.  "
                     "«Численно прибавка не растёт» держится на выборе, который нигде не задокументирован")
    def test_gain_vector_agrees_with_holes_py(self):
        maxima = holes_exact_maxima()
        self.assertEqual(tuple(P.OUR_SIGNATURE.gain_over_construction),
                         tuple(maxima[q] - 3 * (q - 1) for q in (11, 13, 17, 19)))


# ──────────────────── E. вердикт спецификации на измеренных числах ─────────────────────

class TestVerdictOnMeasuredNumbers(unittest.TestCase):

    def test_declared_verdict_is_four_of_four(self):
        self.assertEqual(P.OUR_SIGNATURE.verdict(), "4/4 признаков явления: ЯВЛЕНИЕ")

    def test_measured_verdict_of_our_own_system_flips_with_p(self):
        """Одна и та же система (k = −1), один и тот же протокол измерения, разные p — разный ответ:
        p = 13 → «не характерно», p = 17, 19 → «ЯВЛЕНИЕ».  Пороги verdict() — абсолютные константы."""
        gains = tuple(holes_exact_maxima()[q] - 3 * (q - 1) for q in (11, 13, 17, 19))
        self.assertEqual(measured_signature(13, gains).verdict(), "2/4 признаков явления: не характерно")
        self.assertEqual(measured_signature(17, gains).verdict(), "3/4 признаков явления: ЯВЛЕНИЕ")
        self.assertEqual(measured_signature(19, gains).verdict(), "3/4 признаков явления: ЯВЛЕНИЕ")

    def test_threshold_0_97_is_below_the_rounding_noise_of_the_projects_lp_table(self):
        """B.2 записывает LP с одним знаком после запятой: при p = 17 LP(∞)/LP(1) = 60.2/62.0 = 0.9710,
        но истинное отношение лежит в [60.15/62.05, 60.25/61.95] = [0.9694, 0.9726] — порог 0.97
        внутри интервала округления.  Исход S2 при p = 17 не определён точностью данных проекта."""
        lo = 60.15 / 62.05
        hi = 60.25 / 61.95
        self.assertLess(lo, 0.97)
        self.assertGreater(hi, 0.97)
        self.assertAlmostEqual(60.2 / 62.0, 0.9710, places=4)
        # а при p = 13 (та же система) отношение 0.933 — порог проваливается с запасом
        self.assertLess(B2_KM1[13][1] / B2_KM1[13][0], 0.97)

    def test_the_0_97_threshold_splits_the_projects_lp_table_by_k_and_not_by_phenomenon(self):
        """Все семь посчитанных строк B.2.  При ОДНОМ И ТОМ ЖЕ p = 13 признак S2 выполняется для
        k = 2 (0.990) и нарушается для k = −1 (0.933) — то есть S2 различает вторые гиперболы, тогда
        как §7 заметок («α does not depend much on k») и вывод B.2 («rank-1 certificates cannot give
        T2 uniformly in k») говорят, что явление от k не зависит.  Два из пяти «прохождений» отделены
        от порога меньше чем на 0.002 — внутри округления таблицы до одного знака."""
        ratio = {pk: lp_inf / lp1 for pk, (lp1, lp_inf) in B2_LP_ALL_K.items()}
        passing = {pk for pk, r in ratio.items() if r > 0.97}
        self.assertEqual(passing, {(11, 3), (13, 2), (17, -1), (17, 2), (19, -1)})
        self.assertGreater(ratio[(13, 2)], 0.97)
        self.assertLess(ratio[(13, -1)], 0.97)                       # то же p, другая вторая гипербола
        self.assertLess(ratio[(17, -1)] - 0.97, 0.002)
        self.assertLess(ratio[(17, 2)] - 0.97, 0.002)

    def test_the_constant_3_45_is_the_plateau_of_LP1_not_of_the_LP_with_all_lines(self):
        """§0: «разрыв между LP (со ВСЕМИ ограничениями) и целочисленным оптимумом … У нас: LP ≈ 3.45(p−1)».
        3.45 — плато LP(1) (строки/столбцы/±1; B.7, 40 простых; REPORT §16: «потолок ЛОКАЛЬНЫХ
        сертификатов»).  LP(∞) посчитан ровно при p = 13, 17, 19 и там равен 3.73, 3.76, 3.53 (p−1) —
        выше 3.45 при КАЖДОМ p, где он вообще известен, и выше нигде не измеренного плато."""
        self.assertEqual(re.findall(r"LP ≈ ([\d.]+)\(p−1\)", P.__doc__), [str(LP1_PLATEAU_B7)])
        lp_inf = {p: B2_KM1[p][1] / (p - 1) for p in (13, 17, 19)}
        lp_1 = {p: B2_KM1[p][0] / (p - 1) for p in (13, 17, 19)}
        for p in (13, 17, 19):
            self.assertGreater(lp_inf[p], LP1_PLATEAU_B7, f"p={p}")
            self.assertGreater(lp_1[p], lp_inf[p], f"p={p}")         # LP(1) ≥ LP(∞): меньше ограничений
        self.assertAlmostEqual(lp_inf[13], 3.733, delta=0.001)
        self.assertAlmostEqual(lp_inf[17], 3.763, delta=0.001)
        self.assertAlmostEqual(lp_inf[19], 3.533, delta=0.001)

    @gap("GAP-N-04",
         module="phenomenon.py",
         title="вердикт спецификации, применённый к измеренным числам своей же системы, отрицает явление",
         expected="OUR_SIGNATURE — это «признаки явления в конкретной системе» для системы OUR_FRAME; "
                  "Signature, собранная измерением той же системы (n_weak, n_ground, mean_degree, "
                  "костепень — посчитаны на кандидатах; LP-отношение — из B.2; прибавки — из holes.py), "
                  "обязана давать тот же вердикт",
         actual="при p = 13 измеренная Signature даёт «2/4 признаков явления: не характерно» "
                "(S2: LP(∞)/LP(1) = 44.8/48.0 = 0.933 < 0.97; S4: разброс 4 > 3), при p = 17 и 19 — "
                "«3/4 … ЯВЛЕНИЕ»; объявленный вердикт — «4/4 … ЯВЛЕНИЕ»",
         consequence="детектор явления, применённый к системе, ради которой он написан, не воспроизводит "
                     "ни одно из своих объявленных значений и меняет ответ вместе с p.  Значит фраза "
                     "«4/4 признаков явления» в __main__ не является измерением: она пересказывает "
                     "введённые вручную числа.  Всё, что бриф 8 просит внешних исследователей делать по "
                     "этим признакам («узнать явление в другой системе»), опирается на детектор, который "
                     "на своей собственной системе даёт три разных ответа")
    def test_measured_verdict_matches_the_declared_one(self):
        gains = tuple(holes_exact_maxima()[q] - 3 * (q - 1) for q in (11, 13, 17, 19))
        for p in (13, 17, 19):
            self.assertEqual(measured_signature(p, gains).verdict(), P.OUR_SIGNATURE.verdict(), f"p={p}")


# ───────────────────── F. пороги как абсолютные константы (масштаб) ──────────────────────

def scaled_copies(sig, t):
    """t непересекающихся копий системы: |V|, число троек и прибавка над конструкцией — аддитивны;
    средняя степень, костепень и отношение LP — инварианты."""
    return P.Signature(
        n_weak=t * sig.n_weak,
        n_ground=t * sig.n_ground,
        mean_degree=sig.mean_degree,
        max_codegree=sig.max_codegree,
        lp_all_over_lp_strong=sig.lp_all_over_lp_strong,
        gain_over_construction=tuple(t * g for g in sig.gain_over_construction),
    )


class TestThresholdsAreNotScaleInvariant(unittest.TestCase):

    def test_S1_S2_S3_are_scale_invariant_but_S4_is_not(self):
        base = P.OUR_SIGNATURE
        for t in (1, 2, 3, 4, 8, 100):
            s = scaled_copies(base, t)
            self.assertTrue(s.n_weak >= s.n_ground)                      # S1 — инвариант
            self.assertEqual(s.lp_all_over_lp_strong, base.lp_all_over_lp_strong)   # S2 — инвариант
            self.assertEqual(s.max_codegree, base.max_codegree)          # S3 — инвариант
        drops = [t for t in range(1, 12)
                 if scaled_copies(base, t).verdict() != base.verdict()]
        self.assertEqual(min(drops), 4)      # при t = 4 разброс 4·1 > 3 и признак S4 теряется
        self.assertEqual(scaled_copies(base, 4).verdict(), "3/4 признаков явления: ЯВЛЕНИЕ")

    def test_a_single_measured_size_always_passes_S4(self):
        """Слепая зона: вектор из одной точки имеет разброс 0, поэтому «прибавка не растёт»
        сертифицируется одним измерением — даже если прибавка равна миллиону."""
        s = P.Signature(n_weak=10 ** 6, n_ground=10 ** 3, mean_degree=3000.0, max_codegree=1,
                        lp_all_over_lp_strong=0.99, gain_over_construction=(10 ** 6,))
        self.assertEqual(s.verdict(), "4/4 признаков явления: ЯВЛЕНИЕ")

    def test_an_empty_gain_vector_crashes_the_verdict(self):
        s = P.Signature(n_weak=1, n_ground=1, mean_degree=3.0, max_codegree=1,
                        lp_all_over_lp_strong=1.0, gain_over_construction=())
        with self.assertRaises(ValueError):
            s.verdict()

    @gap("GAP-N-05",
         module="phenomenon.py",
         title="S4 проверяет не «прибавка не растёт», а абсолютный разброс четырёх чисел",
         expected="S4 сформулирован как «численно прибавка над конструкцией не растёт (O(1))» — "
                  "свойство последовательности, инвариантное относительно замены системы на t её "
                  "непересекающихся копий (|V|, число троек и прибавка умножаются на t, явление то же)",
         actual="условие закодировано как max(gain) − min(gain) ≤ 3 — абсолютная константа; при t = 4 "
                "копиях вектор (5,5,6,5) → (20,20,24,20), разброс 4 > 3, и признак теряется, хотя "
                "прибавка по-прежнему НЕ РАСТЁТ с p (она постоянна = 20 на всех четырёх размерах)",
         consequence="признак, отвергающий систему с доказуемо ограниченной прибавкой, не является тестом "
                     "на ограниченность; порог 3 подогнан под конкретные четыре числа одной системы. "
                     "Поскольку S4 — единственное, чем verdict() отличает нас от cap sets («там нет "
                     "плотных структурированных экстремалей»), классификация систем бестиария по этим "
                     "признакам — а именно её бриф 8 просит распространить на новые системы — не имеет "
                     "определённого смысла вне того единственного масштаба, на котором она откалибрована")
    def test_verdict_is_invariant_under_disjoint_copies(self):
        base = P.OUR_SIGNATURE
        for t in (1, 2, 3, 4, 5, 8):
            self.assertEqual(scaled_copies(base, t).verdict(), base.verdict(), f"t={t}")


# ──────────────────── G. откуда числа берутся: пути измерения нет ─────────────────────

class TestThereIsNoMeasurementPath(unittest.TestCase):

    def test_no_toy_model_produces_a_signature(self):
        """Модуль о себе: «Модуль исполняемый: в конце — маленькие игрушечные модели, ПОКАЗЫВАЮЩИЕ
        ПРИЗНАКИ ЯВЛЕНИЯ на синтетических системах».  Признаки — это S1–S6/Signature (§3).  Но три
        игрушки — единственные исполнимые системы модуля — возвращают dict/list, и ни одно их поле
        не совпадает с полем Signature: ни один признак ни на одной из них не вычисляется."""
        self.assertIn("игрушечные модели, показывающие признаки явления", P.__doc__)
        anns = {name: getattr(fn, "__annotations__", {}).get("return")
                for name, fn in vars(P).items() if callable(fn) and name.endswith("_toy")}
        self.assertEqual(len(anns), 3)
        self.assertNotIn(P.Signature, anns.values())
        out = P.lp_blind_toy(n=12, m=20, seed=0)          # безопасно: 20 ≪ C(12,3) = 220
        self.assertIsInstance(out, dict)
        self.assertEqual(set(out) & set(P.Signature.__dataclass_fields__), set())

    def test_signature_accepts_arithmetically_impossible_numbers(self):
        """Валидации нет: систему с отрицательным числом ограничений и степенью −5 модуль
        объявляет явлением."""
        s = P.Signature(n_weak=-1, n_ground=-10, mean_degree=-5.0, max_codegree=0,
                        lp_all_over_lp_strong=1.5, gain_over_construction=(0, 0))
        self.assertEqual(s.verdict(), "4/4 признаков явления: ЯВЛЕНИЕ")
        self.assertNotEqual(handshake_defect(s), 0)

    def test_measuring_a_signature_is_cheap(self):
        """Отсутствие измерителя — не следствие его дороговизны: measured_signature(19) —
        30 строк stdlib и доли секунды на 144 кандидатах."""
        sig = measured_signature(19, (2, 4, 6, 5))
        self.assertEqual((sig.n_weak, sig.n_ground, sig.max_codegree), (292, 144, 1))
        self.assertAlmostEqual(handshake_defect(sig), 0.0, places=9)

    @gap("GAP-N-01",
         module="phenomenon.py",
         title="ни одна функция модуля не вычисляет Signature: все шесть чисел введены руками и нефальсифицируемы",
         expected="модуль о себе: «Модуль исполняемый: в конце — маленькие игрушечные модели, ПОКАЗЫВАЮЩИЕ "
                  "ПРИЗНАКИ ЯВЛЕНИЯ на синтетических системах»; Signature документирован как «диагностические "
                  "признаки явления в конкретной системе (что измерить)», S1–S6 — «как узнать явление в данной "
                  "системе».  Значит путь система → Signature обязан существовать хотя бы для трёх собственных "
                  "игрушечных моделей — единственных исполнимых систем модуля",
         actual="ни один callable модуля не возвращает Signature; игрушки возвращают dict/list, ни одно "
                "поле которых не является полем Signature; у dataclass нет ни __post_init__, ни какой-либо "
                "проверки, поэтому точное тождество 3·n_weak = mean_degree·n_ground нарушено на 33 % "
                "(399600 против 300000) и нарушить его нечему помешать",
         consequence="признаки S1–S6 не являются проверяемыми утверждениями о нашей системе: verdict() "
                     "возвращает функцию от введённых руками чисел, и «4/4 признаков явления» — не "
                     "измерение, а перепечатка входа.  Ни одна из восьми дыр holes.py этого не покрывает: "
                     "H1–H8 требуют инструментов ДОКАЗАТЕЛЬСТВА (SDP, флаги, устойчивость, обмен, короткие "
                     "суммы, полиномы, насыщение, регулярность), и ни одна не требует измерителя, который "
                     "сделал бы спецификацию опровержимой — а бриф 8 передаёт эти числа внешним "
                     "исследователям как данность")
    def test_some_callable_produces_a_signature(self):
        producers = []
        for name, fn in vars(P).items():
            if callable(fn) and getattr(fn, "__annotations__", {}).get("return") in (P.Signature, "Signature"):
                producers.append(name)
        for fn, kwargs in ((P.lp_blind_toy, dict(n=12, m=20, seed=0)),
                           (P.supersaturation_toy, dict(n=15, m=20, seed=1))):
            if isinstance(fn(**kwargs), P.Signature):
                producers.append(fn.__name__)
        self.assertTrue(producers, "в phenomenon.py нет функции, вычисляющей Signature по системе")


# ────────── H. чего вердикт не считает: S5, S6 и объявленная, но никем не читаемая степень ──────────

class TestTheVerdictIgnoresTwoOfSixSignatures(unittest.TestCase):
    """§3 объявляет ШЕСТЬ признаков S1–S6; verdict() печатает знаменатель 4 и читает пять полей из шести."""

    def test_mean_degree_is_declared_but_never_read(self):
        """Единственное поле Signature, не входящее ни в одно условие verdict(): вердикт не меняется
        ни при −10⁹, ни при +10⁹.  Следствие: нарушение точного тождества 3·n_weak = mean_degree·n_ground
        на 33 % не может проявиться НИГДЕ — ни один признак его не смотрит; и вторая половина S1
        («степени ~ log |V|») не закодирована вообще."""
        for md in (-1e9, 0.0, 1e9):
            self.assertEqual(dataclasses.replace(P.OUR_SIGNATURE, mean_degree=md).verdict(),
                             P.OUR_SIGNATURE.verdict(), f"mean_degree={md}")
        self.assertNotEqual(handshake_defect(P.OUR_SIGNATURE), 0.0)

    def test_signature_has_no_field_for_the_two_best_measured_numbers(self):
        """S6 (плато локальных сертификатов) измерено в B.7 на 40 простых p ≤ 199; S5 (спектр) —
        до p = 4001, включая p = 1999, то самое, при котором объявлена OUR_SIGNATURE.  Ни для того,
        ни для другого в Signature нет поля: два признака из шести невыразимы в объекте, который
        «что измерить» перечисляет."""
        self.assertEqual(set(P.Signature.__dataclass_fields__),
                         {"n_weak", "n_ground", "mean_degree", "max_codegree",
                          "lp_all_over_lp_strong", "gain_over_construction"})
        self.assertIn(PRIME_OF_OUR_SIGNATURE, LAMBDA_MIN_OVER_SQRT_M2)          # p = 1999 измерено (§23)
        base = dict(n_weak=1, n_ground=1, mean_degree=3.0, max_codegree=1,
                    lp_all_over_lp_strong=1.0, gain_over_construction=(0,))
        for extra in ({"local_certificate_plateau": LP1_PLATEAU_B7},
                      {"lambda_min_over_sqrt_m2": LAMBDA_MIN_OVER_SQRT_M2[PRIME_OF_OUR_SIGNATURE]}):
            with self.assertRaises(TypeError):
                P.Signature(**base, **extra)

    def test_one_informative_condition_is_enough_to_print_the_phenomenon(self):
        """S3 в разрешённом P1 чтении выполняется тождественно (костепень 1 ≤ 8), а S1 требует лишь
        «троек не меньше, чем точек».  Значит из двух содержательных условий (S2, S4) достаточно
        ОДНОГО, чтобы напечатать «ЯВЛЕНИЕ», — порог «≥ 3 из 4» на деле есть «≥ 1 из 2»."""
        def sig(lp, gains):
            return P.Signature(n_weak=100, n_ground=100, mean_degree=3.0, max_codegree=1,
                               lp_all_over_lp_strong=lp, gain_over_construction=gains)
        self.assertEqual(sig(0.99, (0, 100)).verdict(), "3/4 признаков явления: ЯВЛЕНИЕ")   # только S2
        self.assertEqual(sig(0.00, (0, 0)).verdict(), "3/4 признаков явления: ЯВЛЕНИЕ")     # только S4
        self.assertEqual(sig(0.00, (0, 100)).verdict(), "2/4 признаков явления: не характерно")

    @gap("GAP-N-06",
         module="phenomenon.py",
         title="verdict() оценивает четыре признака из шести объявленных, и «4/4» читается как полная аттестация",
         expected="§3 «ПРИЗНАКИ (signatures) — как узнать явление в данной системе» перечисляет S1–S6 "
                  "(шесть), а Signature документирован как «что измерить»; знаменатель вердикта обязан "
                  "совпадать с числом объявленных признаков",
         actual="verdict() печатает «N/4»: условий четыре.  S5 (мягкие формы + спектральные оценки) и "
                "S6 (плато локальных сертификатов, «у нас 3.45») не оценены и не могут быть оценены — "
                "для них нет полей в Signature, хотя именно у них самые толстые данные проекта: плато "
                "LP(1) измерено на 40 простых p ≤ 199 (B.7), λ_min/√m₂ — при p = 199…4001 (§23), включая "
                "p = 1999, то самое, при котором объявлена OUR_SIGNATURE.  Шестое поле, mean_degree, "
                "объявлено, но не читается ни одним условием (вердикт не меняется при mean_degree = ±10⁹)",
         consequence="строка «4/4 признаков явления», которую печатает __main__, читается как «все признаки "
                     "налицо», а на деле треть списка не проверялась, S3 при разрешённом P1 чтении "
                     "выполняется тождественно (GAP-N-02), и из двух содержательных условий достаточно "
                     "ОДНОГО для вывода «ЯВЛЕНИЕ».  Аттестация опирается на четыре числа при p ≤ 19 "
                     "(вектор прибавок, противоречащий holes.py) и игнорирует две серии, измеренные до "
                     "p = 199 и 4001; именно этот вердикт бриф 8 предлагает внешним исследователям "
                     "переносить на чужие системы")
    def test_verdict_evaluates_every_declared_signature(self):
        declared = sorted(set(re.findall(r"S([1-6])\.", P.__doc__)))
        self.assertEqual(len(declared), 6, "в §3 объявлено не шесть признаков — тест устарел")
        denominator = int(P.OUR_SIGNATURE.verdict().split("/")[1].split()[0])
        self.assertEqual(denominator, len(declared))


if __name__ == "__main__":
    unittest.main(verbosity=2)
