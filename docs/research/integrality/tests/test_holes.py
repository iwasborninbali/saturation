"""test_holes.py — the eight holes as a SET: are they independent, do they cover P1-P5, what has no hole at all."""
import os, sys, unittest, dataclasses, random, re
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)                       # tests/gaps.py
sys.path.insert(0, os.path.dirname(_HERE))      # phenomenon.py, holes.py
from gaps import gap
import phenomenon as P
import holes as H

# ───────────────────────────── helpers ──────────────────────────────────────────────

_DOCS = os.path.abspath(os.path.join(os.path.dirname(_HERE), "..", ".."))   # docs/


def hole_text(h) -> str:
    """All prose of one Hole, lower-cased, as one string."""
    return " ".join((h.key, h.missing_interaction, h.where_it_breaks,
                     h.testable_now, h.filled_elsewhere, h.payoff)).lower()


ALL_TEXT = " ".join(hole_text(h) for h in H.HOLES)
KEYS = [h.key.split()[0] for h in H.HOLES]
BY_KEY = {k: h for k, h in zip(KEYS, H.HOLES)}


def _read_notes(relpath: str) -> str:
    """Whitespace-normalised text of a project note; '' if unavailable (corroboration only)."""
    try:
        with open(os.path.join(_DOCS, relpath), encoding="utf-8") as f:
            return re.sub(r"\s+", " ", f.read())
    except OSError:
        return ""


NOTES = _read_notes("research/pair_bound_notes.md")
REPORT = _read_notes("REPORT.md")
MODEL_THM = _read_notes("research/model_theorem_conditional.md")
BRIEF = _read_notes("research/integrality/deep_research_brief_8_integrality.md")


def holes_matching(tokens) -> list:
    """Keys of holes whose prose contains any of the tokens."""
    return [k for k in KEYS if any(t in hole_text(BY_KEY[k]) for t in tokens)]


# Vocabulary that a hole would have to use to be ABOUT the mechanism of each principle.
# P1's mechanism is named by P1 itself: "τ велико ⇔ тройки распределены … расширение"; the
# other four lists are the names the holes themselves use, so the mapping below is auditable
# (test_state_of_coverage_is_four_out_of_five pins what each list actually matches today).
PRINCIPLE_VOCABULARY = {
    "P1 packing↔transversal": ("τ", "tau", "трансверс", "transversal", "контейнер",
                               "container", "samotij", "saxton", "thomason",
                               "энтроп", "entropy", "расширен", "expand"),
    "P2 fractional blindness": ("lp", "sdp", "sos", "lasserre", "релаксац", "delsarte"),
    "P3 supersaturation": ("насыщен", "supersat", "removal", "varnavides", "roth"),
    "P4 rigidity of extremals": ("устойчив", "stabil", "экстремал", "vosper", "freiman", "segre", "сегре"),
    "P5 global certificates": ("спектр", "фурье", "полином", "флаг", "flag", "slice rank"),
}


# ───────────────────────── 0. invariants that hold (green) ───────────────────────────

class HoleSetShape(unittest.TestCase):
    """The bookkeeping that IS in order — the baseline against which the gaps are measured."""

    def test_eight_holes_H1_to_H8_all_fields_filled(self):
        self.assertEqual(len(H.HOLES), 8)
        self.assertEqual(KEYS, [f"H{i}" for i in range(1, 9)])
        self.assertEqual(len(set(KEYS)), 8)
        for h in H.HOLES:
            for f in dataclasses.fields(H.Hole):
                v = getattr(h, f.name)
                self.assertIsInstance(v, str)
                self.assertGreater(len(v), 10, f"{h.key}.{f.name} is not a real entry")

    def test_hole_is_six_prose_strings_with_no_structured_payload(self):
        """Every field is prose; nothing in the record is a number, a status or a link."""
        names = [f.name for f in dataclasses.fields(H.Hole)]
        self.assertEqual(names, ["key", "missing_interaction", "where_it_breaks",
                                 "testable_now", "filled_elsewhere", "payoff"])
        for f in dataclasses.fields(H.Hole):
            # holes.py has `from __future__ import annotations`, so f.type is the STRING "str":
            self.assertEqual(f.type, "str", f"{f.name} is annotated {f.type!r}, not str")
            self.assertIs(f.default, dataclasses.MISSING)
            self.assertEqual(f.metadata, {})
        # `field` is imported from dataclasses and never called: no defaults, no metadata anywhere.
        self.assertIs(H.field, dataclasses.field)
        src = open(os.path.join(os.path.dirname(_HERE), "holes.py"), encoding="utf-8").read()
        self.assertEqual(src.count("field("), 0, "holes.py imports dataclasses.field but never calls it")


# ───────────────────── 1. the label 'H4' means two different things ──────────────────

class LabelCollision(unittest.TestCase):
    """holes.py's own H7 says '(H4 в записях)'. Inside a module where H4 is a different object."""

    def test_H4_denotes_holes_H7_in_the_project_notes(self):
        h4, h7 = BY_KEY["H4"], BY_KEY["H7"]
        # holes.py's H7 is the notes' H4 — stated inside holes.py itself:
        self.assertIn("H4 в записях", h7.missing_interaction)
        # and holes.py's H4 is a different statement (exchange, not supersaturation):
        self.assertIn("обмен", h4.missing_interaction)
        self.assertNotIn("насыщен", h4.missing_interaction)
        self.assertIn("насыщен", h7.missing_interaction)
        # the notes really do use H4 for the supersaturation statement of holes.py's H7:
        if NOTES:
            self.assertIn("H4 (precise).", NOTES)
            self.assertIn("T(S) := #{collinear triples in S} ≥", NOTES)
        # consequence: 'H4' is ambiguous across the project's own vocabulary, and the
        # deep-research brief ships both labels to external readers.
        if BRIEF:
            self.assertIn("H4 no exchange/matching lemma", BRIEF)
            self.assertIn("H7 no supersaturation lemma", BRIEF)


# ─────────────── 2. H4 and H7 are the target, not tools (independence) ───────────────

def _brute_force_alpha_and_T(n, triples):
    """α = max independent-set size; returns also T(S) for every subset, indexed by bitmask."""
    alpha = 0
    data = []
    for s in range(1 << n):
        T = sum(1 for t in triples if t & s == t)
        size = bin(s).count("1")
        data.append((size, T))
        if T == 0 and size > alpha:
            alpha = size
    return alpha, data


def _alpha_bound_the_hole_states(key, p, C):
    """The bound on α(P₋₁) that a hole's OWN inequality yields, read off holes.py's text.

    None when the hole states no inequality bounding |S| for the PAIR.  Keyed to the exact
    formula in the module, so if the specification replaces the O(1) statement by a genuinely
    weaker one (B.12 offers exactly such a variant) this returns None and GAP-H-01 goes green
    — which is what the xfail marker is for.
    """
    t = BY_KEY[key].missing_interaction
    if "|S₂| ≤ (3(p−1) − |S₁|) + O(1)" in t:
        # |S| = |S₁| + |S₂| ≤ |S₁| + (3(p−1) − |S₁|) + C = 3(p−1) + C, at EVERY split:
        # the exchange lemma loses nothing, so its conclusion is the goal with the same constant.
        return max(s1 + (3 * (p - 1) - s1) + C for s1 in range(3 * (p - 1) + 1))
    if "T(S) ≥ c·(|S| − 3(p−1) − C)" in t:
        # lawful ⇒ T(S) = 0 ⇒ 0 ≥ c(|S| − 3(p−1) − C) ⇒ |S| ≤ 3(p−1) + C, for EVERY c > 0.
        return max(s for s in range(8 * (p - 1) + 1) if 0 >= 1.0 * (s - 3 * (p - 1) - C))
    return None


class TargetInDisguise(unittest.TestCase):

    def test_supersaturation_with_c_equal_1_is_free_on_every_hypergraph(self):
        """B.12: 'conversely T1(O(1)) ⇒ H4 with c = 1 (delete one point per triple)'.

        Executable form: on ANY 3-uniform hypergraph, T(S) ≥ |S| − α for every S.  So H7's
        'мягкая форма' is not softer than the bound — c = 1 comes for free from the bound.
        """
        for seed in (0, 1, 2):
            rnd = random.Random(seed)
            n, m = 13, 25
            triples = set()
            while len(triples) < m:
                a, b, c = rnd.sample(range(n), 3)
                triples.add((1 << a) | (1 << b) | (1 << c))
            triples = list(triples)
            alpha, data = _brute_force_alpha_and_T(n, triples)
            for size, T in data:
                self.assertGreaterEqual(T, size - alpha,
                                        f"seed={seed}: deletion argument broken")
        # and c = 1 is attained, so H7 with c = 1 says exactly what the bound says:
        # four disjoint triples on 12 points — α = 8, and the full set has T = 4 = 12 − 8.
        disjoint = [(1 << (3 * i)) | (1 << (3 * i + 1)) | (1 << (3 * i + 2)) for i in range(4)]
        alpha, data = _brute_force_alpha_and_T(12, disjoint)
        self.assertEqual(alpha, 8)
        self.assertEqual(data[(1 << 12) - 1], (12, 4))

    def test_notes_state_the_equivalence_explicitly(self):
        if not NOTES:
            self.skipTest("pair_bound_notes.md unavailable")
        self.assertIn("H4 is not an intermediate hypothesis but the target itself", NOTES)
        self.assertIn("conversely T1(O(1)) ⇒ H4 with c = 1", NOTES)
        self.assertIn("T1 (O(1) form) ⇔", NOTES)          # B.13: the exchange statement IS T1
        self.assertIn("any proof of it is a proof of T1", NOTES)

    def test_the_weaker_variant_B12_offers_lands_far_above_the_goal(self):
        """B.12 offers an honestly weaker H4(ε) that holes.py did NOT take — this is what a
        real intermediate tool looks like: its conclusion is Ω(p) above the goal, not equal to it."""
        if NOTES:
            self.assertIn("Weaker, still meaningful: H4(ε): T(S) ≥ c·|S| whenever |S| ≥ (3+ε)(p−1)", NOTES)
            self.assertIn("this gives T2 (α ≤ (3+ε)(p−1))", NOTES)
        for p in (101, 1009):
            goal = 3 * (p - 1) + 5                                  # the O(1) statement's conclusion
            eps_variant = max(s for s in range(8 * (p - 1) + 1) if s < 3.5 * (p - 1))
            self.assertGreater(eps_variant - goal, (p - 1) / 4)     # Ω(p) short of the goal

    @gap("GAP-H-01",
         module="holes.py",
         title="H4 and H7 are not holes: each states the target itself, with no loss in the constant",
         expected="Each Hole is 'какого взаимодействия с системой не хватает' — a MISSING TOOL — and 'payoff: что даст "
                  "закрытие' is what closing it buys.  Eight holes should therefore be eight independent missing "
                  "interactions whose conclusions are steps towards the goal α(P₋₁) ≤ 3(p−1)+O(1) stated in the module "
                  "docstring, not that goal itself.  B.12 shows what such a step looks like: H4(ε) 'T(S) ≥ c·|S| whenever "
                  "|S| ≥ (3+ε)(p−1)' concludes (3+ε)(p−1) — Ω(p) above the goal.",
         actual="Two of the eight state an inequality whose conclusion, computed here from the formula printed in the "
                "module, is exactly 3(p−1)+C with the SAME constant: H4 '|S₂| ≤ (3(p−1) − |S₁|) + O(1)' sums to "
                "3(p−1)+C at every split, and H7 'T(S) ≥ c·(|S| − 3(p−1) − C)' with T = 0 gives 3(p−1)+C for every "
                "c > 0.  Their payoffs say so out loud ('прямой путь к 3(p−1)+O(1)', 'из неё α ≤ 3(p−1)+O(1) удалением').  "
                "pair_bound_notes confirms both directions: B.12 'H4 is not an intermediate hypothesis but the target "
                "itself in supersaturation form' with the converse free at c = 1 (brute-forced here on every 3-uniform "
                "hypergraph), B.13 'T1 (O(1) form) ⇔ f(t) ≤ t + C … any proof of it is a proof of T1'.  So H4 ⇔ H7 ⇔ target.",
         consequence="The count 'eight holes' overstates the missing tools by two, and the two entries an outside reader "
                     "is most likely to attack (they read as concrete, self-contained lemmas) are the whole problem in "
                     "disguise.  deep_research_brief_8 §1 ships H4 and H7 as fillable holes each with a 'testable now' "
                     "experiment and §3 asks for 'a ranked list of the three most promising transfers' — any answer to "
                     "H4 or H7 is a complete solution of the open problem, so the brief's difficulty calibration and its "
                     "ranking are wrong.  The same collision infects the vocabulary: holes.py's H7 says '(H4 в записях)', "
                     "so the label H4 denotes two different statements inside one project.")
    def test_no_hole_states_a_bound_that_is_the_target_itself(self):
        p, C = 19, 5
        goal = 3 * (p - 1) + C          # α(P₋₁) ≤ 3(p−1)+O(1) — the module docstring's goal
        restated = [k for k in KEYS if _alpha_bound_the_hole_states(k, p, C) == goal]
        self.assertEqual(restated, [],
                         f"{restated}: the conclusion of the stated inequality IS 3(p−1)+O(1), "
                         f"so these are the target restated, not missing interactions")


# ────────────────── 3. coverage: which principle has no hole at all ──────────────────

class PrincipleCoverage(unittest.TestCase):

    def _covered(self):
        return {name: holes_matching(toks) for name, toks in PRINCIPLE_VOCABULARY.items()}

    def test_state_of_coverage_is_four_out_of_five(self):
        """Pins exactly which principles are backed by a hole today — and audits the vocabulary."""
        cov = self._covered()
        self.assertEqual(cov["P1 packing↔transversal"], [])
        self.assertEqual(cov["P2 fractional blindness"], ["H1", "H2", "H8"])
        self.assertEqual(cov["P3 supersaturation"], ["H7"])
        self.assertEqual(cov["P4 rigidity of extremals"], ["H2", "H3", "H4", "H6", "H7"])
        self.assertEqual(cov["P5 global certificates"], ["H1", "H2", "H5", "H6", "H7", "H8"])

    def test_the_only_Balogh_in_holes_is_the_wrong_one(self):
        """'Balogh' occurs — as Balogh–Lidický (flag algebras), not Balogh–Morris–Samotij (containers)."""
        self.assertIn("balogh", ALL_TEXT)
        self.assertIn("balogh–lidický", ALL_TEXT)
        for token in ("samotij", "saxton", "thomason", "container", "контейнер", "энтроп"):
            self.assertNotIn(token, ALL_TEXT)

    def test_S3_is_measured_by_the_signature_and_consumed_by_no_hole(self):
        """OUR_SIGNATURE measures exactly the quantities P1's mechanism names; no hole uses them."""
        self.assertIn("S3. Малые костепени", P.__doc__)
        self.assertIn("малые степени/костепени, «расширение»", P.__doc__)     # P1's own mechanism
        self.assertEqual(P.OUR_SIGNATURE.max_codegree, 6)                     # measured…
        self.assertEqual(P.OUR_SIGNATURE.mean_degree, 25.0)
        for tok in ("костепен", "codegree", "расшир"):                        # …and never used
            self.assertNotIn(tok, ALL_TEXT)

    @gap("GAP-H-02",
         module="holes.py",
         title="P1 — the principle that defines the phenomenon — has no hole: nothing about τ, expansion or containers",
         expected="phenomenon.py P1 says max|S| = |V| − τ(H₃) and 'слабые ограничения сильны вместе ⇔ τ велико ⇔ тройки "
                  "распределены (малые степени/костепени, расширение)'; the ESSENCE paragraph repeats it ('тройки "
                  "образуют расширяющийся, малокостепенный гиперграф').  Proving α ≤ 3(p−1)+O(1) IS proving "
                  "τ ≥ 5(p−1)−O(1).  Some hole among H1–H8 must therefore be about lower-bounding τ / the spread of H₃ — "
                  "the tool family for 'ALL independent sets of a spread hypergraph with small codegrees' being hypergraph "
                  "containers (Balogh–Morris–Samotij, Saxton–Thomason) and entropy/counting.  Whether that family "
                  "eventually delivers is not the point; a hole is where the missing interaction is NAMED.",
         actual="No hole mentions τ, transversals, expansion, containers, Samotij/Saxton/Thomason or entropy — nor even "
                "the words 'степень/костепень' whose values OUR_SIGNATURE records.  The single occurrence of 'Balogh' is "
                "Balogh–Lidický (flag algebras, in H2) — the wrong Balogh.  Mapping principles to holes by their own "
                "vocabulary gives P2→H1/H2/H8, P3→H7, P4→H2/H3/H4/H6/H7, P5→H1/H2/H5/H6/H7/H8, and P1→nothing.",
         consequence="Signature S3 ('малые костепени: пара точек лежит в O(1) тройках') is measured in OUR_SIGNATURE "
                     "(max_codegree = 6) precisely because it is the codegree hypothesis a container/counting argument "
                     "consumes — and no hole consumes it.  deep_research_brief_8's questions Q1–Q7 are generated one per "
                     "hole (Q1 [H1,H2], Q2 [H3,H4], Q3 [H5], Q4 [H6], Q5 [H7], Q6 [H8]), and the brief contains zero "
                     "occurrences of 'container', 'Samotij', 'Saxton', 'Thomason' or 'entropy': the route cannot come back "
                     "from the deep research at all.  The one principle the whole specification rests on is the one the "
                     "research programme cannot ask about.")
    def test_every_principle_has_at_least_one_hole(self):
        uncovered = [name for name, ks in self._covered().items() if not ks]
        self.assertEqual(uncovered, [], "principles of phenomenon.py with no hole in holes.py")


# ─────────── 4. missing holes the project's own notes prove are needed ───────────────

class MissingHoles(unittest.TestCase):

    def test_notes_name_the_upper_bound_on_spanned_directions_as_the_missing_input(self):
        if not NOTES:
            self.skipTest("pair_bound_notes.md unavailable")
        self.assertIn("A global geometric argument would need an UPPER bound on the number of "
                      "distinct lines spanned by S", NOTES)
        self.assertIn("give lower bounds on spanned lines, not upper ones", NOTES)
        self.assertIn("nothing in the literature we know bounds the directions spanned by a dense "
                      "subset of a lifted hyperbola pair from above", NOTES)

    def test_H8_is_about_a_different_object(self):
        """The one hole that mentions directions wants a regular sub-family for counting THROUGH a
        point (Bose); it asks for no bound, from above or below, on how many directions S spans."""
        h8 = BY_KEY["H8"]
        self.assertIn("регулярное подсемейство направлений/прямых", h8.missing_interaction)
        self.assertIn("прямые через точку «разбивают» остальные кандидаты", h8.missing_interaction)
        for tok in ("сверху", "upper bound", "натянут", "spanned", "beck"):
            self.assertNotIn(tok, hole_text(h8))

    @gap("GAP-H-03",
         module="holes.py",
         title="No hole for B.12(iv): nothing bounds the number of directions/lines spanned by a dense subset FROM ABOVE",
         expected="phenomenon.py P5 says the certificates that see the phenomenon are the GLOBAL ones, and lists "
                  "'структурные' among them; pair_bound_notes B.12(iv) states what the global GEOMETRIC argument needs: "
                  "'A global geometric argument would need an UPPER bound on the number of distinct lines spanned by S "
                  "(lawful ⇔ S spans C(|S|,2) lines); Beck/Szemerédi–Trotter give lower bounds on spanned lines, not upper "
                  "ones; nothing in the literature we know bounds the directions spanned by a dense subset of a lifted "
                  "hyperbola pair from above.'  That is, verbatim, a missing interaction with the system, i.e. a hole.",
         actual="No hole among H1–H8 mentions the lines/directions spanned by a candidate set, nor Beck, nor an upper "
                "bound on their number (checked with a ±40-character window around every 'сверху'/'upper bound' "
                "occurrence in the module).  The only «сверху» in the whole module is H6's payoff «покрытие явления "
                "сверху» — an upper bound on α, not on the spanned directions.  H8 is the only hole that mentions "
                "directions at all, and it asks for a regular sub-family for counting through a point — a different object.",
         consequence="Lawfulness is *equivalent* to 'S spans C(|S|,2) lines', so this is not one route among many — it is "
                     "the direct geometric translation of the hypothesis, and the notes single it out as the input a "
                     "global argument needs.  With no hole and hence no 'filled_elsewhere' entry, it is absent from the "
                     "deep-research brief (zero occurrences of 'spanned' or 'Beck' there); Q1–Q7 ask for relaxations, "
                     "flags, stability, exchange, short sums, polynomials, supersaturation and regularity, and cannot "
                     "return the one thing B.12 says is missing.")
    def test_some_hole_is_about_the_number_of_spanned_directions(self):
        hits = []
        for k in KEYS:
            t = hole_text(BY_KEY[k])
            if any(tok in t for tok in ("натянут", "spanned", "beck", "порождённых прямых")):
                hits.append(k)
            for m in re.finditer(r"сверху|upper bound", t):
                w = t[max(0, m.start() - 40): m.end() + 40]
                if re.search(r"направлен|прямых|прямые|lines|direction", w):
                    hits.append(k)
        self.assertNotEqual(hits, [], "no hole is about bounding the spanned directions from above")

    # ── the deepest one: every hole is on the upper side ──

    def test_gain_over_the_construction_for_the_frame_the_modules_declare(self):
        """holes.py's own exact maxima are k = −1 — the pair xy ≡ ±1 both modules declare.

        They give gains 2, 4, 6, 5 at p = 11, 13, 17, 19 — the sequence phenomenon.py's S4
        would judge, and it fails S4's own criterion.  OUR_SIGNATURE instead carries
        (5, 5, 6, 5), which is max-over-ALL-k (pair_bound_notes §7: p=11: 32–35, 13: 38–41,
        17: 49–54), i.e. not the declared frame.
        """
        exact = {int(a): int(b) for a, b in re.findall(r"(\d+):\s*(\d+)", BY_KEY["H1"].testable_now)}
        self.assertEqual(exact, {11: 32, 13: 40, 17: 54, 19: 59})
        if NOTES:                                        # these ARE the k = −1 values (§18)
            self.assertIn("below α (32, 40, 54, 59, 70–74)", NOTES)
            self.assertIn("p=11: 32–35; p=13: 38–41; p=17: 49–54", NOTES)   # §7: max over ALL k
        gains = [exact[p] - 3 * (p - 1) for p in (11, 13, 17, 19)]
        self.assertEqual(gains, [2, 4, 6, 5])
        # phenomenon.py's S4 criterion, applied to the frame's own numbers:
        self.assertGreater(max(gains) - min(gains), 3, "S4 would pass on k=−1 data")
        # what OUR_SIGNATURE actually carries is a different k:
        self.assertEqual(list(P.OUR_SIGNATURE.gain_over_construction), [5, 5, 6, 5])
        self.assertLessEqual(max(P.OUR_SIGNATURE.gain_over_construction)
                             - min(P.OUR_SIGNATURE.gain_over_construction), 3)
        # both modules declare k = −1 (xy ≡ ±1) as the system:
        self.assertIn("xy ≡ ±1", P.OUR_FRAME.ground_set)
        self.assertIn("xy ≡ ±1", H.__doc__)

    def test_notes_leave_the_lower_side_open_and_name_it_a_next_step(self):
        if not NOTES:
            self.skipTest("pair_bound_notes.md unavailable")
        self.assertIn("(T4) construction with gain ω(1)", NOTES)             # §6, open candidate
        self.assertIn("| 23 | −1 | 70–74 | 66 |", NOTES)                     # p=23 bracketed: gain 4…8
        # B.11's own recommendation puts the lower-bound construction first among the next steps:
        self.assertIn("the next real step is either the LOWER-bound construction", NOTES)
        if BRIEF:                                        # the brief ships the premise as a conjecture
            self.assertIn("gain ≤ +6 for p ≤ 19; conjecture: ≤ +6 for all p", BRIEF)

    @gap("GAP-H-04",
         module="holes.py",
         title="All eight holes are on the upper side; nothing guards the premise that the gain over 3(p−1) is O(1)",
         expected="holes.py's docstring fixes the goal 'α(P₋₁) ≤ 3(p−1) + O(1)' and every hole is a missing tool for "
                  "proving it.  That goal is a conjecture: pair_bound_notes §6 lists '(T4) construction with gain ω(1)' as "
                  "an open candidate statement alongside T1–T3, and B.11 closes with 'the next real step is either the "
                  "LOWER-bound construction (3(p−1)+c for all p) or a genuinely global argument'.  A set of holes "
                  "describing 'чего не хватает, чтобы материализовать явление' must contain the hole on the other side: "
                  "we cannot prove the gain stays O(1), and no construction is excluded.",
         actual="No hole mentions constructions, lower bounds, the growth of the gain, ω(1) or T4 — the single occurrence "
                "of 'gain' in the module is inside H5's English literature list.  Every missing_interaction is a "
                "certificate, a stability theorem, an exchange lemma or an analytic input, i.e. an upper-bound tool.",
         consequence="The evidence for the premise is four exact values at p ≤ 19.  For the frame both modules actually "
                     "declare (xy ≡ ±1, i.e. k = −1) holes.py's own exact maxima 32/40/54/59 give gains 2, 4, 6, 5 — "
                     "monotone through p = 17 and failing phenomenon.py's own S4 criterion (spread ≤ 3), which "
                     "OUR_SIGNATURE passes only because it carries (5,5,6,5), the max over ALL k (§7: p=11: 32–35, "
                     "13: 38–41, 17: 49–54), not the declared pair.  p = 23 is still only bracketed 70–74, i.e. gain 4…8.  "
                     "If α = 3(p−1) + ω(1), then H3 (distance O(t)), H4 (exchange up to O(1)) and H7 (additive constant C) "
                     "are FALSE as stated and the other five aim at a bound that does not exist — eight holes in a wall "
                     "around the wrong building, with no hole able to detect it.")
    def test_some_hole_is_about_the_lower_side(self):
        toks = ("конструкц", "нижн", "снизу", "lower bound", "прибавк", "ω(1)", "omega(1)", "t4")
        self.assertNotEqual(holes_matching(toks), [],
                            "no hole asks whether the gain over 3(p−1) is really O(1)")


# ─────────── 5. calibration: what each hole is worth against the state of the art ────

class Calibration(unittest.TestCase):

    def test_H5s_payoff_is_worth_less_than_what_is_already_proved(self):
        """holes.py's docstring records «доказано 11/3 → 115/32».  H5 buys the unconditional MODEL
        theorem, and the project's own evaluation of that theorem is below 115/32 — for the model only."""
        self.assertIn("доказано 11/3 → 115/32", H.__doc__)
        self.assertIn("безусловная теорема модели", BY_KEY["H5"].payoff)
        proved = 115 / 32                                    # 3.594(p−1), unconditional, real system
        # B.12's own arithmetic for what the model theorem yields: 4 − c₁/Δ with its measured constants
        self.assertAlmostEqual(4 - 2.4 / 7, 3.657, places=3)
        self.assertGreater(4 - 2.4 / 7, proved, "H5's payoff would beat what is already proved")
        if NOTES:
            self.assertIn("with c₁ ≈ 2.4, Δ ≈ 7 this is ≈ 3.66(p−1), i.e. nothing beyond the block theorem", NOTES)
        if MODEL_THM:                                        # and it is not even about the real system
            self.assertIn("It does not give T1 (singles/mixed pairs are outside the model)", MODEL_THM)
            self.assertIn("the deletion bound T/Δ is weak", MODEL_THM)
        # nothing in H5's payoff says any of this — it names no bound at all:
        for tok in ("115/32", "11/3", "3.4", "3.6", "(p−1)"):
            self.assertNotIn(tok, BY_KEY["H5"].payoff)

    @gap("GAP-H-06",
         module="holes.py",
         title="Payoffs are not priced against the state of the art holes.py itself records: H5 buys less than 115/32",
         expected="holes.py's docstring fixes the only scale on which 'что даст закрытие' can be read — 'доказано "
                  "11/3 → 115/32; локальный потолок LP(1) ≈ 3.45; цель α(P₋₁) ≤ 3(p−1)+O(1)' — and "
                  "deep_research_brief_8 §3 asks for 'a ranked list of the three most promising transfers'.  Ranking "
                  "requires every payoff on that scale, so each payoff must name the bound its hole delivers.",
         actual="Five payoffs are priced (H1 and H2 against 3.45, H3/H4/H7 against 3(p−1)+O(1)); H5, H6 and H8 name no "
                "bound at all.  For the one of those three the notes do price, the number is worse than what is already "
                "proved: H5 buys 'безусловная теорема модели (T(r) ≥ cp ∀r)', and B.12 computes what that yields with "
                "its own measured constants — 4 − c₁/Δ ≈ 3.66(p−1) with c₁ ≈ 2.4, Δ ≈ 7, 'i.e. nothing beyond the block "
                "theorem' — against the 115/32 = 3.594 recorded in holes.py's own docstring.  "
                "model_theorem_conditional.md is blunter still: 'It does not give T1 (singles/mixed pairs are outside the "
                "model), and the deletion bound T/Δ is weak (Δ ~ log p?)', i.e. 4(p−1) − o(p), for the MODEL and not the "
                "system.  H5's record says none of this.",
         consequence="One of the eight holes buys strictly less than what the project has already proved, and the "
                     "specification cannot show it: the reader of the brief sees eight equal-looking holes.  Q3 [H5] is "
                     "the analytically hardest question in the brief — 2-D character sums below the Burgess range, which "
                     "REPORT §16 calls not doable by known unconditional means — and the module gives no way to see that "
                     "its payoff is below the state of the art.  Any ranking of 'the three most promising transfers' "
                     "produced from this file is therefore uncalibrated in exactly the place where the cost is highest.")
    def test_every_payoff_is_priced_on_the_modules_own_scale(self):
        unpriced = [k for k in KEYS if not re.search(r"3[.,]45|\(p−1\)|\d+/\d+", BY_KEY[k].payoff)]
        self.assertEqual(unpriced, [], "payoffs naming no bound: what closing them buys cannot be "
                                       "compared with «доказано 11/3 → 115/32» in holes.py's own docstring")


# ─────────── 6. the experiments the module calls cheap-and-now ──────────────────────

class Experiments(unittest.TestCase):

    def test_interfaces_I1_I6_are_docstring_prose_only(self):
        for i in range(1, 7):
            self.assertIn(f"I{i}", H.__doc__)
            self.assertFalse(hasattr(H, f"I{i}"), f"I{i} exists as an object")
        self.assertFalse(hasattr(H, "INTERFACES"))
        referencing = [k for k in KEYS if re.search(r"\bI[1-6]\b", hole_text(BY_KEY[k]).upper())]
        self.assertEqual(referencing, ["H2"])            # only H2 names an interface, and only I1
        if BRIEF:                                        # while the brief demands the round-trip
            self.assertIn("which of our interfaces I1–I6 (in `holes.py`) it would plug into", BRIEF)

    def test_H1_sizes_a_level_2_relaxation_with_a_level_1_moment_matrix(self):
        """testable_now prescribes Lasserre/SoS LEVEL 2 and gives its moment matrix as (8(p−1)+1)²,
        which is the LEVEL-1 size; REPORT §16 records that what was launched is level 1."""
        t = BY_KEY["H1"].testable_now
        self.assertIn("Lasserre/SoS уровня 2", t)
        self.assertIn("(8(p−1)+1)²", t)
        for p, level1, level2 in ((11, 81, 3241), (31, 241, 28921)):
            n = 8 * (p - 1)                                   # binary variables = candidates
            self.assertEqual(n + 1, level1)                   # monomials of degree ≤ 1 — level 1
            self.assertEqual(1 + n + n * (n - 1) // 2, level2)  # monomials of degree ≤ 2 — level 2
        self.assertGreater(28921 / 241, 100)                  # p = 31: 120× the prescribed dimension
        if REPORT:
            self.assertIn("Запущены эксперименты H1 (SDP уровня 1 с локализующими ограничениями, p ≤ 23) "
                          "и H4 (лемма обмена, p ≤ 31)", REPORT)

    def test_H1s_experiment_cannot_be_scored_over_two_thirds_of_its_own_range(self):
        """testable_now: run to p = 11…31 and compare with the exact max — which does not exist past 19."""
        t = BY_KEY["H1"].testable_now
        self.assertIn("p = 11…31", t)
        known = sorted({int(a) for a, _ in re.findall(r"(\d+):\s*(\d+)", t)})
        self.assertEqual(known, [11, 13, 17, 19])
        prescribed = [11, 13, 17, 19, 23, 29, 31]                     # the primes in 11…31
        self.assertEqual([p for p in prescribed if p not in known], [23, 29, 31])
        # holes.py's I6 nevertheless advertises exact solvers from p ≈ 23 upward:
        self.assertIn("точные решатели до p ≈ 23–61", H.__doc__)
        if NOTES:                                                     # …while p = 23 is a range
            self.assertIn("| 23 | −1 | 70–74 |", NOTES)
            self.assertIn("DATA needed: α for p = 23 (70–74), 29, 31", NOTES)

    def test_H4s_key_experiment_has_already_returned_a_negative(self):
        """testable_now points at B.13 as «ключевой эксперимент»; B.13's verdict is NEGATIVE, and
        nothing in holes.py says so — H4's payoff is still «прямой путь к 3(p−1)+O(1)»."""
        self.assertIn("B.13", BY_KEY["H4"].testable_now)
        self.assertIn("ключевой эксперимент", BY_KEY["H4"].testable_now)
        self.assertIn("прямой путь к 3(p−1)+O(1)", BY_KEY["H4"].payoff)
        if NOTES:
            self.assertIn("Verdict: T2.9 negative", NOTES)
            self.assertIn("this charging gives |S₂| ≲ 4–5·|R|: it certifies slope ≈ 4–5, not 1", NOTES)
        for h in H.HOLES:                                 # nowhere to record any of this
            self.assertNotIn("запущен", hole_text(h))
            self.assertNotIn("negative", hole_text(h))


# ─────────── 7. the chaining that is left over (pinned, not filed as a gap) ──────────

class Chaining(unittest.TestCase):

    def test_H1s_payoff_is_H2s_subject(self):
        """Closing H1 buys, by its own payoff, the thing H2 says is missing — the holes are chained."""
        self.assertIn("SDP над локальными плотностями", BY_KEY["H1"].payoff)
        self.assertIn("локальный предел", BY_KEY["H1"].payoff)
        self.assertIn("local-limit", BY_KEY["H2"].key)
        self.assertIn("ПЛОТНОСТЕЙ локальных конфигураций", BY_KEY["H2"].missing_interaction)

    def test_H3s_payoff_routes_through_H4(self):
        """H3 buys the target only 'через жёсткость + обмен' — i.e. only together with H4, which is
        why H3 is NOT counted as the target restated in GAP-H-01."""
        self.assertIn("через жёсткость + обмен", BY_KEY["H3"].payoff)
        self.assertIn("3(p−1)+O(1)", BY_KEY["H3"].payoff)
        self.assertIn("обмен", BY_KEY["H4"].missing_interaction)
        # and H3's own statement constrains ONE hyperbola, so it bounds nothing for the pair:
        self.assertIn("S₁ ⊂ лифты H(1)", BY_KEY["H3"].missing_interaction)
        self.assertIsNone(_alpha_bound_the_hole_states("H3", 19, 5))


if __name__ == "__main__":
    unittest.main(verbosity=2)
