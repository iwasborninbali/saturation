"""test_falsifiability.py — можно ли эту теорию опровергнуть: чем меряются признаки, бестиарий без чисел,
нулевая гипотеза, и что на самом деле показывают игрушечные модели.

Линза: phenomenon.py + holes.py читаются как НАУЧНОЕ УТВЕРЖДЕНИЕ.  Вопрос не «работает ли код», а
«какое вычисление, доступное проекту (точные решатели до p ≈ 61, LP до p = 199, статистика до p ~ 10⁵),
могло бы опровергнуть каждое утверждение — и записан ли этот критерий хоть где-нибудь».

Сорта тестов — по tests/gaps.py: обычные (зелёные) фиксируют факт/поломку, @gap фиксирует ДЫРУ
спецификации (xfail: пока дыра открыта — прогон зелёный).
"""
from __future__ import annotations

import dataclasses
import inspect
import math
import os
import random
import re
import subprocess
import sys
import unittest

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)                       # tests/gaps.py
sys.path.insert(0, os.path.dirname(_HERE))      # phenomenon.py, holes.py

from gaps import gap
import phenomenon as P
import holes as H

_MOD = os.path.dirname(_HERE)                                   # …/research/integrality
_DOCS = os.path.dirname(os.path.dirname(_MOD))                  # …/docs
_NOTES = os.path.join(_DOCS, "research", "pair_bound_notes.md")
_REPORT = os.path.join(_DOCS, "REPORT.md")
_BRIEF = os.path.join(_MOD, "deep_research_brief_8_integrality.md")
_SRC = os.path.join(_MOD, "phenomenon.py")

# ── общие помощники ──────────────────────────────────────────────────────────────────────

#: повелительные формы, которыми в holes.py описан ПРОВОДИМЫЙ ОПЫТ (поле testable_now)
_VERB = re.compile("посчитать|измерить|проверить|перечислить|семплировать|оценить|выписать|"
                   "вычислить|сравнить|искать|определить|найти")


def _fields_text(obj) -> str:
    return " ".join(str(getattr(obj, f.name)) for f in dataclasses.fields(obj))


def _read(path: str) -> str:
    if not os.path.exists(path):                      # переносимость: без ground truth — пропуск
        raise unittest.SkipTest(f"нет файла {path}")
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def _signature_texts() -> dict:
    """S1…S6 из докстринга phenomenon.py (объектов для них не существует — только проза)."""
    out, cur = {}, None
    for line in (P.__doc__ or "").splitlines():
        m = re.match(r"\s*(S[1-6])\.\s*(.*)", line)
        if m:
            cur = m.group(1); out[cur] = m.group(2)
        elif line.strip().startswith("─") or re.match(r"\s*\d\.\s", line):
            cur = None
        elif cur and line.strip():
            out[cur] += " " + line.strip()
    return out


def _verdict_thresholds() -> list:
    """числа, которыми verdict() решает судьбу системы (порядок как в исходнике, без повторов)."""
    src = inspect.getsource(P.Signature.verdict)
    return list(dict.fromkeys(re.findall(r"[<>]=?\s*([0-9]+(?:\.[0-9]+)?)", src)))


def _mentions_number(haystack: str, num: str) -> bool:
    """число названо как самостоятельная величина (а не кусок «2/3», «3.45», «1999»)."""
    return bool(re.search(r"(?<![\d.,/])" + re.escape(num) + r"(?![\d.,/])", haystack))


def _essence_text() -> str:
    return (P.__doc__ or "").split("4. СУТЬ")[1].split("\n", 2)[2].strip()


def _principle(prefix: str):
    return next(pr for pr in P.PRINCIPLES if pr.key.startswith(prefix))


def _hole(prefix: str):
    return next(h for h in H.HOLES if h.key.startswith(prefix))


def _exact_maxima_from_H1() -> dict:
    """точные max для k = −1, записанные в holes.H1.testable_now: {p: α}."""
    return {int(p): int(a) for p, a in re.findall(r"(\d+):\s*(\d+)", _hole("H1").testable_now)}


def _b2_rows_km1() -> list:
    """таблица B.2 из pair_bound_notes.md, строки с k = −1: (p, α, LP(1), LP(∞))."""
    rows = re.findall(r"^\|\s*(\d+),(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)"
                      r"\s*\|\s*([\d.]+)/([\d.]+)/([\d.]+)\s*\|", _read(_NOTES), re.M)
    out = []
    for p, k, _i1, _i2, _i3, a, l1, _l2, li in rows:
        if int(k) == int(p) - 1:                      # k ≡ −1 (mod p) — рамка OUR_FRAME
            out.append((int(p), int(a), float(l1), float(li)))
    return sorted(out)


def _toy_instance(n: int, m: int, seed: int) -> list:
    """тот же генератор троек, что внутри lp_blind_toy (модуль не трогаем, повторяем код)."""
    rnd = random.Random(seed)
    triples = set()
    while len(triples) < m:
        triples.add(frozenset(rnd.sample(range(n), 3)))
    return sorted(triples, key=lambda t: sorted(t))


# ── 1. Чем меряются признаки: числа вердикта против текста признаков ──────────────────────

class TestOperationalCriteria(unittest.TestCase):
    """Формат «что посчитать, чтобы утверждение упало» в проекте есть (holes.testable_now, 8/8)."""

    def test_every_hole_names_an_experiment(self):
        """holes.Hole.testable_now: критерий опровержения записан у всех восьми дыр."""
        self.assertIn("testable_now", [f.name for f in dataclasses.fields(H.Hole)])
        without = [h.key for h in H.HOLES if not _VERB.search(h.testable_now)]
        self.assertEqual(without, [], "дыра без проводимого опыта")

    def test_no_assertion_of_the_phenomenon_names_a_computation(self):
        """Тот же счёт по phenomenon.py: 0 из 19 (P1–P5 + 8 систем бестиария + S1–S6)."""
        inventory = [(p.key, _fields_text(p)) for p in P.PRINCIPLES]
        inventory += [(a.name, _fields_text(a)) for a in P.BESTIARY]
        inventory += sorted(_signature_texts().items())
        self.assertEqual(len(inventory), 19)
        self.assertEqual([k for k, t in inventory if _VERB.search(t)], [])

    @gap("GAP-F-01", module="phenomenon.py (S1–S6 ↔ Signature.verdict)",
         title="Числа, которыми выносится вердикт, не названы ни в одном признаке",
         expected="раздел 3 назван «ПРИЗНАКИ — как узнать явление в данной системе», и verdict() "
                  "формализует его четырьмя порогами: n_weak ≥ n_ground, LP(все)/LP(сильные) > 0.97, "
                  "костепень ≤ 8, разброс прибавок ≤ 3. Признак, который можно проверить, обязан "
                  "называть свой порог: иначе нельзя сказать, какое измерение его опровергает",
         actual="S1–S6 — качественная проза («много», «малые», «≈», «не растёт»); ни 0.97, ни 8, ни 3 "
                "в них не встречаются. Пороги живут только в коде и ни на что не ссылаются: нигде не "
                "записано, на каких данных они получены и при каком p. Обратное тоже верно — S5 и S6 "
                "не имеют в Signature ни одного поля, а объявленное поле mean_degree (S1: «степени ~ "
                "log |V|») вердиктом не читается",
         consequence="два порога из четырёх УЖЕ противоречат собственным данным проекта, и в "
                     "спецификации это никак не отражается: 0.97 расположен между тремя единственными "
                     "посчитанными отношениями LP(∞)/LP(1) при k = −1 (0.933 / 0.971 / 0.994, B.2), а "
                     "разброс ≤ 3 нарушен четырьмя точными прибавками той же рамки (2,4,6,5). "
                     "Признак без названного порога нельзя опровергнуть — его можно только подогнать")
    def test_the_verdict_thresholds_are_stated_in_the_signatures_they_formalize(self):
        texts = " ".join(_signature_texts().values())
        thresholds = _verdict_thresholds()
        self.assertEqual(thresholds, ["0.97", "8", "3"])            # что именно решает вердикт
        missing = [t for t in thresholds if not _mentions_number(texts, t)]
        self.assertEqual(missing, [], f"порогов вердикта нет в тексте S1–S6: {missing}")

    def test_which_signature_fields_are_computable_at_the_declared_p(self):
        """OUR_SIGNATURE объявлена при p = 1999 — вне диапазонов, в которых проект умеет считать."""
        exact_hi = int(re.search(r"точные решатели до p ≈ \d+[–-](\d+)", H.__doc__).group(1))
        stats_hi = 10 ** 5 if "10⁵" in H.__doc__ else None
        lp_hi = int(re.search(r"LP\(1\).{0,40}for all p ≤ (\d+)", _read(_NOTES)).group(1))
        self.assertEqual((exact_hi, stats_hi, lp_hi), (61, 10 ** 5, 199))
        self.assertGreater(P.p, lp_hi, "p=1999 внутри диапазона LP — тогда 0.985 можно проверить")
        self.assertGreater(P.p, exact_hi)
        self.assertLessEqual(P.p, stats_hi)
        # итог: 4 поля из 6 — счётная статистика (в диапазоне), 2 требуют LP/точного решения (вне)
        computable = ["n_weak", "n_ground", "mean_degree", "max_codegree"]
        not_computable = ["lp_all_over_lp_strong", "gain_over_construction"]
        self.assertEqual(sorted(computable + not_computable),
                         sorted(f.name for f in dataclasses.fields(P.Signature)))


# ── 2. «Локальное не работает»: универсальное отрицание против теоремы самого проекта ─────

class TestTheImpossibilityClaim(unittest.TestCase):

    def test_recorded_scope_of_the_no_local_certificate_claim(self):
        """Фактический объём проверки «локальное не работает»: D ≤ 2 и p ≤ 59 (B.11), не «никакая»."""
        notes = _read(_NOTES)
        self.assertIn("provably insufficient (data up to p=59, D ≤ 2)", notes)
        self.assertIn("при p ≤ 59", P.__doc__)          # тот же объём, но только в комментарии
        self.assertNotIn("59", _fields_text(_principle("P2")), "объём проверки не попал в объект P2")

    def test_the_proved_bound_is_a_local_certificate_and_is_missing_from_the_module(self):
        """P5: «сертификат должен оперировать распределением конфигураций, А НЕ ВЕСАМИ НА ПРЯМЫХ».
        Единственная безусловная теорема проекта — покрытие прямыми: α(P₋₁) ≤ (115/32+o(1))(p−1)
        = 3.594(p−1) < 4(p−1) (REPORT §16).  holes.py её записывает, phenomenon.py — нет."""
        self.assertIn("а не весами на прямых", _principle("P5").consequence)
        self.assertIn("(115/32+o(1))(p−1) = 3.594(p−1)", _read(_REPORT))
        self.assertIn("доказано 11/3 → 115/32", H.__doc__)          # сестринский модуль её знает
        for token in ("115/32", "11/3", "3.594", "3.59"):
            self.assertNotIn(token, P.__doc__, f"докстринг всё же называет {token}")
        # и именно этот текст уходит наружу: модуль — приложение к брифу, бриф повторяет признак
        brief = _read(_BRIEF)
        self.assertIn("Приложения: `phenomenon.py` — спецификация явления", brief)
        self.assertIn("local certificates plateau far above the truth", brief)

    def test_the_headline_LP_number_is_the_strong_only_LP(self):
        """§0: «LP (со всеми ограничениями)… У нас: LP ≈ 3.45(p−1)».  По B.7 заметок 3.45 — это
        LP(1) = «rows, columns and slope-±1 lines only», т.е. в точности СИЛЬНЫЙ список самого
        модуля.  LP со всеми прямыми (LP(∞)) при k = −1 посчитан на трёх простых: 3.53–3.76 (p−1)."""
        notes = _read(_NOTES)
        self.assertIn("LP(1) = LP with rows, columns and slope-±1 lines only", notes)
        self.assertIn("LP(1) ≈ 3.45 (p−1) for all p ≤ 199", notes)
        self.assertIn("3.45(p−1)", P.__doc__)                       # приписано «LP со всеми»
        self.assertIn("строки, столбцы, прямые наклона ±1", P.__doc__)   # он же список СИЛЬНЫХ
        lp_inf = [(q, li / (q - 1)) for q, _a, _l1, li in _b2_rows_km1()]
        self.assertEqual([q for q, _ in lp_inf], [13, 17, 19])
        for q, ratio in lp_inf:
            self.assertGreater(ratio, 3.5, f"p={q}: LP(∞)/(p−1) = {ratio:.2f}, а не 3.45")

    @gap("GAP-F-02", module="phenomenon.py §4 (СУТЬ) + P5",
         title="Универсальное отрицание «никакая взвешенная сумма локальных ограничений» не называет, "
               "до чего локальное не доходит",
         expected="§4: «никакая взвешенная сумма локальных ограничений этого не выражает»; P5: "
                  "«сертификат должен оперировать распределением конфигураций, а не весами на "
                  "прямых». Отрицание проверяемо только если названа величина, которой локальное "
                  "не достигает: у проекта это 3(p−1)+O(1)",
         actual="ни §4, ни объект P5 не называют 3(p−1). Без порога отрицание читается двояко, и "
                "сильное чтение («веса на прямых не дают линейной экономии») ЛОЖНО дважды: LP(1) "
                "ранга 1 на строках/столбцах/±1 даёт 3.45(p−1) < 4(p−1) при всех 19 ≤ p ≤ 199 (B.7, "
                "сертифицировано дуалом, при p = 29 дуал ЦЕЛЫЙ — это буквально покрытие прямыми), а "
                "единственная безусловная теорема проекта — то же покрытие: 115/32 = 3.594(p−1) "
                "(REPORT §16). Слабое чтение («не дают 3(p−1)») — сводка данных объёма D ≤ 2, p ≤ 59 "
                "(B.11), и этот объём в §4 не указан",
         consequence="phenomenon.py уходит внешним исследователям приложением к дип-ресёрч-брифу "
                     "(«Приложения: phenomenon.py — спецификация явления»), а §0 брифа повторяет тот "
                     "же признак («local certificates plateau far above the truth»). Читатель "
                     "получает невозможность там, где у проекта есть работающий результат ровно "
                     "этого типа, и не может понять, что закрыт не класс сертификатов, а участок "
                     "[3(p−1), 3.45(p−1)] — единственный, ради которого H1/H2 и заказаны")
    def test_the_no_local_certificate_claim_names_its_target(self):
        text = _essence_text() + " " + _fields_text(_principle("P5"))
        self.assertRegex(text, r"3\s*\(\s*p\s*[−–-]\s*1\s*\)",
                         "ни §4, ни P5 не называют порог 3(p−1), которого локальные сертификаты не "
                         "достигают; при этом доказанное покрытие уже даёт 3.594(p−1) < 4(p−1)")

    def test_the_projects_own_supersaturation_lemma_pins_the_threshold(self):
        """Та же лемма насыщения в holes.H7 и в B.12 записана с ПРИВЯЗАННЫМ порогом 3(p−1);
        в объекте P3 порог назван свободной буквой α, которая в модуле нигде не определена."""
        self.assertIn("T(S) ≥ c·(|S| − 3(p−1) − C)", _hole("H7").missing_interaction)
        self.assertIn("c·(|S| − 3(p−1) − C₀)", _read(_NOTES))       # B.12, «absolute constants»
        p3 = _fields_text(_principle("P3"))
        self.assertEqual(p3.count("α"), 3)                          # α в посылке, в выводе и в следствии
        self.assertNotIn("3(p−1)", p3)
        self.assertEqual(re.findall(r"α\s*(?:=|:=)", P.__doc__), [])    # и нигде не определена

    @gap("GAP-F-08", module="phenomenon.py (P3)",
         title="Порог насыщения α не определён, поэтому P3 нельзя ни выполнить, ни нарушить осмысленно",
         expected="P3 — «мягкая форма явления, обычно доступная раньше точной», и именно её заказывает "
                  "дыра H7. У H7 и у B.12 заметок та же лемма записана с привязанным порогом: "
                  "T(S) ≥ c·(|S| − 3(p−1) − C₀), c и C₀ абсолютные. P3 обязан назвать ту же величину",
         actual="P3 = «|S| > α + C ⇒ T(S) ≥ c(|S| − α − C)», где α, c, C свободны, а α не определена "
                "ни в §0, ни в §1, ни в объекте. Следствие P3 («из неё α + O(1) удалением») выводит "
                "оценку α из посылки, сформулированной через α: при чтении «α = истинный максимум» "
                "вывод круговой, при чтении «α = размер конструкции 3(p−1)» — это H7. Модуль не "
                "говорит, какое чтение имеется в виду",
         consequence="P3 уходит наружу как заказ на теорему. Насыщение над порогом 3.45(p−1) "
                     "формально удовлетворяет P3 и не даёт проекту ничего: 3.45(p−1) уже получено "
                     "локальным LP (B.7), а цель — 3(p−1)+O(1). Ни спецификация, ни verdict() не "
                     "способны отличить исполненный заказ от бесполезного")
    def test_P3_names_the_threshold_it_is_about(self):
        self.assertRegex(_fields_text(_principle("P3")), r"3\s*\(\s*p\s*[−–-]\s*1\s*\)|конструкц",
                         "P3 не связывает α ни с конструкцией, ни с 3(p−1) — а H7 и B.12 связывают")


# ── 3. Бестиарий и признаки — две несоединённые половины ──────────────────────────────────

class TestBestiaryVersusSignatures(unittest.TestCase):
    """«Как узнать явление в данной системе» — при том, что ни одна система, кроме нашей, не измерена."""

    def test_analog_system_is_all_prose(self):
        types = {f.name: f.type for f in dataclasses.fields(P.AnalogSystem)}
        self.assertEqual(set(types.values()), {"str"}, "в AnalogSystem нет ни одного числового поля")
        self.assertEqual(len(P.BESTIARY), 8)

    @gap("GAP-F-03", module="phenomenon.py (BESTIARY ↔ Signature)",
         title="Ни одна система бестиария не может быть прогнана через признаки S1–S6",
         expected="раздел 3 обещает «как узнать явление в данной системе», раздел 2 перечисляет восемь "
                  "систем; значит для каждой должен существовать путь AnalogSystem → Signature → "
                  "verdict() (хотя бы одно числовое поле или адаптер)",
         actual="AnalogSystem — шесть строк прозы, ноль числовых полей; в модуле нет ни одной функции, "
                "принимающей AnalogSystem; экземпляр Signature ровно один — OUR_SIGNATURE, набранный "
                "руками. Утверждение «no-three-in-line — то же явление в чистом виде» не проверяется "
                "ничем и не может быть опровергнуто",
         consequence="перенос механизмов из чужих систем (поле filled_elsewhere у восьми дыр, все семь "
                     "вопросов Q1–Q7 брифа) опирается на непроверяемое «там то же самое». Проверить "
                     "это не праздно: собственный пример модуля — дуги в PG(2,q) — по его же вердикту "
                     "получает 3/4 «ЯВЛЕНИЕ», хотя слабых ограничений там нет вовсе (см. "
                     "TestNullHypothesis). Приоритеты дип-ресёрча расставлены прозой")
    def test_every_bestiary_system_can_be_scored(self):
        numeric = [f for f in dataclasses.fields(P.AnalogSystem)
                   if f.type not in ("str", "Sequence[str]")]
        adapters = [n for n, o in vars(P).items()
                    if callable(o) and "AnalogSystem" in str(getattr(o, "__annotations__", {}))]
        self.assertTrue(numeric or adapters,
                        f"числовых полей: {len(numeric)}, адаптеров AnalogSystem→Signature: "
                        f"{len(adapters)}; систем в бестиарии: {len(P.BESTIARY)}")

    def test_exactly_one_system_is_ever_evaluated(self):
        sigs = [n for n, o in vars(P).items() if isinstance(o, P.Signature)]
        self.assertEqual((len(P.BESTIARY) + 1, sigs), (9, ["OUR_SIGNATURE"]),
                         "названных систем 9, измеренная 1")


# ── 4. Свидетельство под признаками: числа OUR_SIGNATURE против данных проекта ────────────

class TestSignatureEvidence(unittest.TestCase):

    def test_mean_degree_is_declared_but_never_read(self):
        """S1 требует «степени ~ log|V|»; поле есть, но verdict() его не читает."""
        self.assertNotIn("mean_degree", inspect.getsource(P.Signature.verdict))
        self.assertEqual(_read(_SRC).count("mean_degree"), 2)   # объявление + присваивание, ноль чтений

    def test_S5_and_S6_have_no_field_at_all(self):
        """Признаков объявлено шесть, в verdict() входят четыре; S5/S6 нечем измерить."""
        self.assertEqual(len(_signature_texts()), 6)
        src = inspect.getsource(P.Signature.verdict)
        self.assertEqual(sorted(re.findall(r"# (S\d)", src)), ["S1", "S2", "S3", "S4"])
        names = " ".join(f.name for f in dataclasses.fields(P.Signature))
        for absent in ("supersat", "spectr", "lambda", "plateau", "плато"):
            self.assertNotIn(absent, names)

    def test_signature_has_no_identity_and_mixes_scales(self):
        """У Signature нет поля «какая система/какое p» — OUR_SIGNATURE склеена из двух масштабов."""
        names = {f.name for f in dataclasses.fields(P.Signature)}
        self.assertFalse(names & {"p", "system", "name", "source", "as_of"})
        self.assertEqual(P.OUR_SIGNATURE.n_ground, 8 * (P.p - 1))          # счётные поля при p = 1999
        self.assertIn("p=11,13,17,19", _read(_SRC))                        # прибавки при p ≤ 19

    def test_declared_gains_are_the_maximum_over_k_not_the_declared_frame(self):
        """(5,5,6,5) — это max по k (B.6c); для рамки OUR_FRAME (k = −1) прибавки другие."""
        notes = _read(_NOTES)
        self.assertIn("+5,+5,+6,+5", notes)                                 # источник кортежа
        alpha = _exact_maxima_from_H1()                                     # k = −1, из holes.H1
        self.assertEqual(alpha, {11: 32, 13: 40, 17: 54, 19: 59})
        real = tuple(alpha[q] - 3 * (q - 1) for q in sorted(alpha))
        self.assertEqual(real, (2, 4, 6, 5))
        self.assertNotEqual(tuple(P.OUR_SIGNATURE.gain_over_construction), real)
        # то же из таблицы B.2 заметок (p = 13,17,19; строки k = p−1) — уже без p = 11
        self.assertEqual([a - 3 * (q - 1) for q, a, _, _ in _b2_rows_km1()], [4, 6, 5])
        # и сама «32» при p = 11 — догадка «32?» из §4 заметок, а не посчитанное значение
        self.assertIn("32?", notes)
        self.assertNotIn(11, [q for q, *_ in _b2_rows_km1()])

    @gap("GAP-F-04", module="phenomenon.py (S4 / OUR_SIGNATURE)",
         title="S4 ложен на собственных точных данных проекта для объявленной рамки",
         expected="§0 утверждает «правда (по всем точным данным) 3(p−1)+O(1)», S4 — «численно прибавка "
                  "над конструкцией не растёт», а verdict() формализует это как разброс ≤ 3; OUR_FRAME "
                  "объявляет систему xy ≡ ±1, т.е. k = −1, значит вердикт обязан быть 4/4 на прибавках "
                  "именно этой рамки",
         actual="кортеж (5,5,6,5) взят из B.6(c) заметок, где это максимум по ВСЕМ k (p=11 → k=3, "
                "p=13 → k=2) — другая система, чем объявленная рамка. Прибавки объявленной рамки "
                "проект записал сам, в holes.H1.testable_now как эталон сравнения для опыта H1: "
                "11:32, 13:40, 17:54, 19:59, т.е. (2,4,6,5) — разброс 4, вердикт падает до 3/4. "
                "Значение 32 при p = 11 держится на догадке «32?» из §4 заметок (в таблице точных "
                "значений B.2 строки (11,−1) нет); без него прибавки (4,6,5) укладываются в порог — "
                "то есть S4 проверен ровно на трёх точках, и одна непосчитанная его опровергает",
         consequence="S4 — единственный признак, кодирующий главную гипотезу проекта (α(P₋₁) = "
                     "3(p−1)+O(1), цель в докстринге holes.py). Свидетельство под ним взято из другой "
                     "системы; на данных объявленной рамки он не выполняется, а вердикт этого не "
                     "замечает — порога «3 из 4» хватает. Заявление «по всем точным данным» держится "
                     "на четырёх числах, из которых одно — знак вопроса")
    def test_S4_holds_on_the_declared_frames_own_exact_data(self):
        alpha = _exact_maxima_from_H1()
        real = tuple(alpha[q] - 3 * (q - 1) for q in sorted(alpha))
        sig = dataclasses.replace(P.OUR_SIGNATURE, gain_over_construction=real)
        # порог берём из самого вердикта, а не из теста: дыру можно закрыть и данными, и спецификацией
        self.assertIn("4/4", sig.verdict(), f"прибавки при k=−1: {real} ⇒ {sig.verdict()}")

    def test_four_points_extrapolate_to_a_gain_of_thirty_at_the_declared_p(self):
        """S4 закодирован как «разброс ≤ 3» на четырёх точках p ≤ 19, а объявлена система p = 1999.
        Те же четыре точки, подогнанные моделью a + b·ln p, предсказывают там прибавку ≈ 34."""
        alpha = _exact_maxima_from_H1()
        ps = sorted(alpha)
        y = [alpha[q] - 3 * (q - 1) for q in ps]
        x = [math.log(q) for q in ps]
        mx, my = sum(x) / len(x), sum(y) / len(y)
        b = sum((xi - mx) * (yi - my) for xi, yi in zip(x, y)) / sum((xi - mx) ** 2 for xi in x)
        a = my - b * mx
        sse_log = sum((yi - (a + b * xi)) ** 2 for xi, yi in zip(x, y))
        sse_const = sum((yi - my) ** 2 for yi in y)
        self.assertGreater(b, 0, "наклон по log p положителен")
        self.assertLess(sse_log, sse_const / 2,
                        f"растущая модель точнее постоянной: {sse_log:.2f} против {sse_const:.2f}")
        at_declared = a + b * math.log(P.p)
        self.assertGreater(at_declared, 30,
                           f"при p={P.p} растущая модель даёт прибавку {at_declared:.0f}, "
                           f"а признак S4 обещает O(1) с разбросом ≤ 3")

    def test_S2_threshold_straddled_by_the_only_computed_ratios(self):
        """lp_all_over_lp_strong = 0.985 не посчитан ни при одном p; три реальных значения — по обе
        стороны порога 0.97 (B.2 заметок, k = −1: LP(∞)/LP(1))."""
        ratios = {q: li / l1 for q, _a, l1, li in _b2_rows_km1()}
        self.assertEqual(sorted(ratios), [13, 17, 19])
        self.assertLess(ratios[13], 0.97)                       # 0.9333 — признак S2 ЛОЖЕН при p=13
        self.assertGreater(ratios[17], 0.97)                    # 0.9710 — проходит на 0.001
        self.assertNotIn(round(P.OUR_SIGNATURE.lp_all_over_lp_strong, 4),
                         [round(v, 4) for v in ratios.values()])

    def test_verdict_survives_the_failure_of_any_single_signature(self):
        """Порог «≥ 3 из 4» ⇒ ни один признак по отдельности не может изменить вердикт."""
        broken = {
            "S1": dict(n_weak=0),
            "S2": dict(lp_all_over_lp_strong=0.5),
            "S3": dict(max_codegree=99),
            "S4": dict(gain_over_construction=(0, 100)),
        }
        for label, kw in broken.items():
            with self.subTest(признак=label):
                v = dataclasses.replace(P.OUR_SIGNATURE, **kw).verdict()
                self.assertIn("3/4", v)
                self.assertIn("ЯВЛЕНИЕ", v)


# ── 5. Нулевая гипотеза: чем сказать, что явления НЕТ ────────────────────────────────────

class TestNullHypothesis(unittest.TestCase):

    def test_empty_system_scores_four_of_four(self):
        """Система без кандидатов и без ограничений — «ЯВЛЕНИЕ», 4/4."""
        empty = P.Signature(n_weak=0, n_ground=0, mean_degree=0.0, max_codegree=0,
                            lp_all_over_lp_strong=1.0, gain_over_construction=(0,))
        self.assertEqual(empty.verdict(), "4/4 признаков явления: ЯВЛЕНИЕ")

    def test_system_without_weak_constraints_is_called_the_phenomenon(self):
        """Дуги в PG(2,q) — собственный пример модуля, где всё закрыто счётом «через точку»:
        все прямые полные (q+1 ≥ 5 точек) ⇒ слабых ограничений нет вовсе, костепень 0,
        LP(все) = LP(сильные) тождественно, прибавка над коникой 0 при каждом q."""
        q = 101
        arcs = P.Signature(n_weak=0, n_ground=q * q + q + 1, mean_degree=0.0, max_codegree=0,
                           lp_all_over_lp_strong=1.0, gain_over_construction=(0, 0, 0, 0))
        self.assertEqual(arcs.verdict(), "3/4 признаков явления: ЯВЛЕНИЕ")
        # три из четырёх условий выполнены ПУСТО — именно потому, что слабых ограничений нет
        self.assertEqual([a.name for a in P.BESTIARY][1], "дуги в PG(2,q)")
        self.assertIn("точно", P.BESTIARY[1].truth)             # там ответ известен ТОЧНО

    def test_verdict_crashes_on_an_unmeasured_system(self):
        """«Прибавки ещё не мерили» выражается только пустым кортежем — и это ValueError."""
        blank = dataclasses.replace(P.OUR_SIGNATURE, gain_over_construction=())
        with self.assertRaises(ValueError):
            blank.verdict()

    @gap("GAP-F-05", module="phenomenon.py (Strength / Signature.verdict / игрушки)",
         title="У теории нет нулевой гипотезы: сказать «явления здесь НЕТ» нечем",
         expected="диагностическая схема (раздел 3 «как узнать явление») обязана уметь давать "
                  "отрицательный и неопределённый ответ: значение Strength для «это не ограничение», "
                  "исход verdict() для «данных не хватает», и хотя бы одна игрушка-контроль, где "
                  "слабые ограничения СОВМЕСТНО слабы",
         actual="Strength имеет ровно два значения (и strength() возвращает STRONG для любого size ≠ "
                "cap+1, включая size ≤ cap); verdict() имеет два исхода и падает с ValueError на "
                "непомеренной системе; все три игрушки построены так, чтобы разрыв был — контроля нет. "
                "Итог: пустая система получает 4/4 «ЯВЛЕНИЕ», а дуги в PG(2,q) (собственный пример "
                "модуля, где счёт «через точку» даёт ТОЧНЫЙ ответ q+1) — 3/4 «ЯВЛЕНИЕ», причём три "
                "условия из четырёх выполнены ПУСТО, ровно потому что слабых ограничений там нет",
         consequence="признаки S2/S3/S4 не обладают специфичностью: «LP(все) ≈ LP(сильные)», «малые "
                     "костепени», «прибавка не растёт» одинаково истинны и там, где явление есть, и "
                     "там, где слабых ограничений нет вовсе. Диагноз «ЯВЛЕНИЕ» нельзя опровергнуть "
                     "никакими данными, значит вывод «наша задача — экземпляр явления», на котором "
                     "стоит весь перенос механизмов, не несёт информации")
    def test_module_can_express_absence(self):
        ways = []
        if len({m.name for m in P.Strength} - {"STRONG", "WEAK"}):
            ways.append("Strength")
        outcomes = set()
        for n_weak in (0, 10 ** 6):
            for lp in (0.5, 0.99):
                for cod in (0, 99):
                    for g in ((0, 0), (0, 100)):
                        outcomes.add(P.Signature(n_weak, 10, 0.0, cod, lp, g).verdict().split(": ")[1])
        if len(outcomes) > 2:
            ways.append("verdict")
        toys = [P.lp_blind_toy, P.supersaturation_toy, P.transversal_vs_fractional_toy]
        if any(re.search("контрол|нет разрыва|отсутств", t.__doc__ or "") for t in toys):
            ways.append("контрольная игрушка")
        empty = P.Signature(0, 0, 0.0, 0, 1.0, (0,)).verdict()
        arcs = P.Signature(0, 101 ** 2 + 102, 0.0, 0, 1.0, (0, 0, 0, 0)).verdict()
        self.assertTrue(ways, f"исходы verdict(): {sorted(outcomes)}; "
                              f"значения Strength: {[m.name for m in P.Strength]}; "
                              f"пустая система: {empty!r}; дуги PG(2,101): {arcs!r}")


# ── 6. Что на самом деле показывают игрушечные модели ────────────────────────────────────

class TestToyEvidence(unittest.TestCase):

    def test_lp_blind_toy_can_report_a_negative_gap(self):
        """Величина, названная разрывом целочисленности, принимает отрицательные значения."""
        self.assertEqual(P.lp_blind_toy(n=30, m=0)["gap"], -10.0)

    @gap("GAP-F-06", module="phenomenon.py (lp_blind_toy)",
         title="Единственная исполняемая опора принципа P2 не считает ни одного оптимума",
         expected="докстринг: «дробная упаковка x ≡ 2/3 против жадной целочисленной независимости… "
                  "Показывает P2 в чистом виде», а P2 — про разрыв τ ≫ τ*, т.е. про ОПТИМУМЫ обеих "
                  "задач; значит целочисленная сторона обязана быть максимумом",
         actual="целочисленная сторона — одна жадная прогонка: при n=30, m=200, seed=0 она даёт 11, "
                "тогда как независимое множество размера 13 предъявляется рестартами за 0.05 c, "
                "а точный максимум (ветвями с отсечением, 0.8 c) равен 14. Дробная сторона (2n/3 = 20) "
                "— не значение LP, а лишь допустимая точка, т.е. тоже нижняя оценка. Публикуемый "
                "«gap» = разность двух НИЖНИХ оценок: он не ограничивает разрыв ни сверху, ни снизу "
                "и при m = 0 отрицателен",
         consequence="P2 («LP слепо») — основание всей программы: из него следует, что путь покрытий "
                     "закрыт и нужен глобальный сертификат. Его единственная исполняемая демонстрация "
                     "меряет неудачу жадного алгоритма и завышает разрыв в полтора раза (9.0 вместо "
                     "честных 6.0) на игрушке, по которой читатель судит о явлении")
    def test_lp_blind_toy_integer_side_is_the_optimum(self):
        toy = P.lp_blind_toy()                                   # n=30, m=200, seed=0
        triples = _toy_instance(30, 200, 0)
        rnd, best, witness = random.Random(20260819), 0, set()
        for _ in range(150):
            order = list(range(30)); rnd.shuffle(order)
            S = set()
            for v in order:
                if all(not (t - {v}) <= S for t in triples if v in t):
                    S.add(v)
            if len(S) > best:
                best, witness = len(S), set(S)
        self.assertTrue(all(not t <= witness for t in triples), "свидетель независим")
        self.assertGreaterEqual(toy["greedy_integer"], best,
                                f"жадный ответ {toy['greedy_integer']} против свидетеля {best}")

    def test_supersaturation_toy_reproduces_a_structure_free_constant(self):
        """Выход игрушки — оценка m·C(k,3)/C(n,3), т.е. функция только (n, m, k):
        она одинакова для ЛЮБОГО 3-однородного гиперграфа и потому не различает системы."""
        n, m = 40, 400
        for k, observed in P.supersaturation_toy():
            expected = m * math.comb(k, 3) / math.comb(n, 3)
            self.assertLessEqual(abs(observed - expected), 0.1 * expected + 0.5,
                                 f"k={k}: {observed} против структурно-независимых {expected:.3f}")

    def test_supersaturation_toy_has_no_threshold(self):
        """P3 — рост ЛИНЕЙНЫЙ сверх порога α; у игрушки порога нет, а рост кубический."""
        data = dict(P.supersaturation_toy())
        self.assertGreater(data[5], 0, "троек больше нуля уже при наименьшем k ⇒ порог α = 0")
        slope_low = (data[10] - data[5]) / 5
        slope_high = (data[30] - data[25]) / 5
        self.assertGreater(slope_high / slope_low, 5,
                           "линейный рост дал бы отношение наклонов ≈ 1")

    def test_the_only_exact_demonstration_does_not_scale(self):
        """τ считается полным перебором C(n,k): единственная точная игрушка не доживает до размеров,
        на которых видно заявленное асимптотическое поведение («разрыв линеен по размеру системы»)."""
        env = dict(os.environ, PYTHONPATH=_MOD, PYTHONWARNINGS="ignore")
        cmd = [sys.executable, "-c",
               "import phenomenon as P; print(P.transversal_vs_fractional_toy(n=36, m=200, seed=3))"]
        with self.assertRaises(subprocess.TimeoutExpired):
            subprocess.run(cmd, env=env, timeout=6, capture_output=True)
        small = P.transversal_vs_fractional_toy()                 # n=24: τ=10 против n/3=8
        self.assertEqual(small["tau_exact"], 10)
        self.assertEqual(small["n/3 (tau* upper bound)"], 8.0)


# ── 7. Утверждения, обойдённые событиями ─────────────────────────────────────────────────

class TestOvertakenByEvents(unittest.TestCase):

    def test_report_records_the_experiment_holes_calls_never_run(self):
        """REPORT §16 (тот же день, тот же абзац, что вводит holes.py): эксперименты H1 и H4
        запущены.  holes.py в это время утверждает «НИ РАЗУ не вычислялось»."""
        report = _read(_REPORT)
        self.assertIn("Запущены эксперименты H1 (SDP уровня 1 с локализующими ограничениями, p ≤ 23) "
                      "и H4 (лемма обмена, p ≤ 31)", report)
        self.assertIn("`holes.py` (дыры H1–H8)", report)        # тот же абзац вводит модуль
        h1 = _hole("H1")
        self.assertIn("НИ РАЗУ не вычислялось", h1.where_it_breaks)
        self.assertIn("уровня 2", h1.testable_now)      # предписан уровень 2, запущен уровень 1
        self.assertIn("p = 11…31", h1.testable_now)     # предписано p ≤ 31, запущено p ≤ 23

    @gap("GAP-F-07", module="holes.py",
         title="Дыра умеет записать опыт, но не его результат: статус нечем обновить",
         expected="Hole несёт testable_now («что проверить сейчас») — значит опыт предполагается "
                  "проведённым; чтобы утверждение «НИ РАЗУ не вычислялось» оставалось проверяемым, "
                  "нужен слот статуса/даты/результата (у объекта или у модуля)",
         actual="поля Hole: key, missing_interaction, where_it_breaks, testable_now, filled_elsewhere, "
                "payoff — ни статуса, ни даты, ни результата; у модуля нет __version__/__updated__. "
                "REPORT §16 уже фиксирует запуск экспериментов H1 и H4 (в том же абзаце, которым "
                "holes.py вводится), причём не тех, что предписаны: SDP уровня 1 при p ≤ 23 вместо "
                "SoS уровня 2 при p = 11…31",
         consequence="holes.py — приложение к дип-ресёрч-брифу, уходящее наружу: внешний исследователь "
                     "получает утверждение «никогда не считалось» о вычислении, запущенном до "
                     "отправки, и не может отличить открытую дыру от закрытой, а частичный результат "
                     "(уровень 1 вместо 2) — от предписанного. Список дыр устаревает молча — ровно "
                     "то, чего реестр gaps.py требует избегать")
    def test_holes_can_record_a_result(self):
        names = {f.name for f in dataclasses.fields(H.Hole)}
        self.assertTrue(names & {"status", "as_of", "date", "result", "last_checked", "refuted_by"},
                        f"поля Hole: {sorted(names)}; атрибуты модуля: "
                        f"{sorted(n for n in vars(H) if n.startswith('__'))}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
