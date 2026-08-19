"""test_toys.py — the three toy models of phenomenon.py: what they actually demonstrate.

Lens: TOYS.  lp_blind_toy / supersaturation_toy / transversal_vs_fractional_toy each claim in
their docstring to exhibit a principle (P2, P3, P1/P2).  This file measures what they compute.

Ordinary tests pin the behaviour that is there (values, raises, hangs, costs, cross-toy
contradictions).  @gap tests state what §0/P1/P2/P3 PROMISE and fail because it is absent.

Two rules kept throughout, checked by a hostile re-read of every assertion:
  * a @gap assertion must PASS against a corrected specification — otherwise the xfail is noise
    (this is why GAP-T-02 no longer asks the supersaturation curve to be *at most* linear: P3 is
    a LOWER bound, so a min-curve growing faster than linearly would not contradict it);
  * every quantity a @gap relies on is either computed by phenomenon.py itself or certified here
    in exact arithmetic (independent sets are re-verified against the toy's own hypergraph).
The @gap tests read the shipped return-key names; if the toys are ever rewritten, the
ToyReplicaFidelity tests below go RED, which forces this file to be revisited.
"""
from __future__ import annotations

import itertools
import math
import os
import random
import subprocess
import sys
import unittest
from fractions import Fraction

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)                       # tests/gaps.py
sys.path.insert(0, os.path.dirname(_HERE))      # phenomenon.py, holes.py

from gaps import gap
import phenomenon as P
import holes as H

_MODDIR = os.path.dirname(_HERE)
_NOTES = os.path.join(os.path.dirname(_MODDIR), "pair_bound_notes.md")

# ─────────────────────────── replicas of the toys' own generators ───────────────────────────
# Verified bit-for-bit against the toys in class ToyReplicaFidelity below; every later claim
# about "the toy's hypergraph" rests on that verification.


def _triples_set(n, m, seed):
    """The generator of lp_blind_toy and supersaturation_toy (set + .add)."""
    rnd = random.Random(seed)
    triples = set()
    while len(triples) < m:
        triples.add(frozenset(rnd.sample(range(n), 3)))
    return triples, rnd


def _triples_list(n, m, seed):
    """The generator of transversal_vs_fractional_toy (list + membership test)."""
    rnd = random.Random(seed)
    triples = []
    while len(triples) < m:
        t = frozenset(rnd.sample(range(n), 3))
        if t not in triples:
            triples.append(t)
    return triples, rnd


def _replay_lp_blind(n, m, seed):
    triples, rnd = _triples_set(n, m, seed)
    S = set()
    for v in rnd.sample(range(n), n):
        if all(not (t - {v} <= S) for t in triples if v in t):
            S.add(v)
    return triples, S


def _replay_supersat(n, m, seed):
    triples, rnd = _triples_set(n, m, seed)
    out = []
    for k in range(5, n + 1, 5):
        tot = 0
        for _ in range(200):
            S = set(rnd.sample(range(n), k))
            tot += sum(1 for t in triples if t <= S)
        out.append((k, tot / 200))
    return triples, out


def _triples_inside(triples, S):
    S = set(S)
    return sum(1 for t in triples if t <= S)


def _codegrees(triples):
    co = {}
    for t in triples:
        for pair in itertools.combinations(sorted(t), 2):
            co[pair] = co.get(pair, 0) + 1
    return co


# Independent-set certificates (found offline by greedy with restarts; each is re-verified
# in-test against the toy's OWN hypergraph, so each gives a rigorous lower bound on alpha).
IND_30_200_0 = [2, 4, 5, 12, 13, 14, 15, 16, 17, 18, 19, 20, 23, 24]                    # |.| = 14
IND_15_12_0 = [0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 13]                                   # |.| = 12
IND_40_400_1 = [0, 2, 3, 4, 9, 11, 12, 15, 18, 20, 21, 23, 26, 28, 29, 39]              # |.| = 16

_TRANS = {}


def _trans(n=24, m=60, seed=2):
    """transversal_vs_fractional_toy memoised — the shipped default alone costs ~6 s."""
    key = (n, m, seed)
    if key not in _TRANS:
        _TRANS[key] = P.transversal_vs_fractional_toy(n, m, seed)
    return _TRANS[key]


def _alpha_via_the_modules_own_P1(n, m, seed):
    """P1, verbatim: 'S допустимо ⇔ V\\S бьёт все тройки; max|S| = |V| − τ(H₃)'.

    The transversal toy computes τ exactly by brute force, so the module itself supplies the
    integer optimum of the very hypergraph lp_blind_toy greedily attacks (the two generators
    are proved identical in ToyReplicaFidelity)."""
    return n - _trans(n, m, seed)["tau_exact"]


def _child(expr, timeout):
    code = "import sys; sys.path.insert(0, %r); import phenomenon as P; print(%s)" % (_MODDIR, expr)
    return subprocess.run([sys.executable, "-W", "ignore", "-c", code],
                          capture_output=True, text=True, timeout=timeout)


# ══════════════════════════════════════════════════════════════════════════════════════════
class ToyReplicaFidelity(unittest.TestCase):
    """The replicas above reproduce the toys exactly (licenses every claim that follows)."""

    def test_lp_blind_replica_is_exact(self):
        for (n, m, s) in [(30, 200, 0), (20, 60, 0), (12, 24, 0)]:
            triples, S = _replay_lp_blind(n, m, s)
            out = P.lp_blind_toy(n, m, s)
            self.assertEqual(len(triples), m)
            self.assertEqual(len(S), out["greedy_integer"], (n, m, s))

    def test_supersaturation_replica_is_exact(self):
        triples, mine = _replay_supersat(40, 400, 1)
        self.assertEqual(mine, P.supersaturation_toy())
        self.assertEqual(len(triples), 400)

    def test_transversal_replica_is_exact(self):
        triples, _ = _triples_list(24, 60, 2)
        deg = {v: sum(1 for t in triples if v in t) for v in range(24)}
        out = _trans()
        self.assertEqual(len(triples), 60)
        self.assertAlmostEqual(out["E/Delta"], 60 / max(deg.values()))

    def test_all_three_toys_build_one_and_the_same_random_object(self):
        """The set-generator and the list-generator agree edge for edge AND leave the RNG in the
        same state, so for a given (n, m, seed) the 'three toy models' are three statistics of a
        single uniformly random 3-uniform hypergraph — the same object, measured three ways."""
        for (n, m, s) in [(30, 200, 0), (24, 60, 2), (15, 25, 0), (15, 12, 0), (40, 400, 1)]:
            A, ra = _triples_set(n, m, s)
            B, rb = _triples_list(n, m, s)
            self.assertEqual(A, set(B), (n, m, s))
            self.assertEqual(ra.getstate(), rb.getstate(), (n, m, s))


# ══════════════════════════════════════════════════════════════════════════════════════════
class LpBlindToy(unittest.TestCase):
    """lp_blind_toy: 'Показывает P2 в чистом виде' — the returned key is literally 'gap'."""

    def test_shipped_default_values(self):
        out = P.lp_blind_toy()
        self.assertEqual(out, {"fractional_2/3": 20.0, "greedy_integer": 11, "gap": 9.0})

    def test_the_integer_side_is_not_the_integer_optimum(self):
        """greedy = 11, but the toy's own hypergraph has an independent set of size 14."""
        triples, S = _replay_lp_blind(30, 200, 0)
        self.assertEqual(_triples_inside(triples, IND_30_200_0), 0)   # certificate re-verified
        self.assertEqual(len(IND_30_200_0), 14)
        self.assertEqual(len(S), 11)
        self.assertEqual(P.lp_blind_toy()["gap"], 9.0)                # >= 3 of the 9 units are greedy failure

    def test_the_module_computes_alpha_exactly_and_its_gap_toy_ignores_it(self):
        """The module's own P1 (max|S| = |V| − τ) applied to its own exact τ solver, on the SAME
        hypergraph: the honest gap is 0.0 where the toy reports +2.0, and −2.0 where it reports +1.0."""
        for (n, m, s, tau, greedy, reported) in [(15, 25, 0, 5, 8, 2.0),
                                                 (15, 25, 1, 6, 8, 2.0),
                                                 (15, 12, 0, 3, 9, 1.0)]:
            self.assertEqual(_trans(n, m, s)["tau_exact"], tau, (n, m, s))
            alpha = _alpha_via_the_modules_own_P1(n, m, s)
            out = P.lp_blind_toy(n, m, s)
            self.assertEqual(out["greedy_integer"], greedy, (n, m, s))
            self.assertLess(out["greedy_integer"], alpha, (n, m, s))   # greedy misses the optimum
            self.assertEqual(out["gap"], reported, (n, m, s))
            self.assertNotEqual(out["gap"], 2 * n / 3 - alpha, (n, m, s))
        # sign of the honest comparison is opposite to the reported one on (15, 12, 0)
        self.assertEqual(2 * 15 / 3 - _alpha_via_the_modules_own_P1(15, 12, 0), -2.0)
        self.assertEqual(P.lp_blind_toy(15, 12, 0)["gap"], 1.0)

    def test_reported_gap_is_negative_without_any_constraints(self):
        """m = 0: no constraint at all, so LP* = alpha = 30 and the honest gap is 0; toy says −10."""
        out = P.lp_blind_toy(30, 0, 0)
        self.assertEqual(out["greedy_integer"], 30)
        self.assertEqual(out["gap"], -10.0)

    def test_reported_gap_swings_with_the_seed_alone(self):
        """Same n, m: the number called 'gap' moves by 4 (44 %) because greedy moves."""
        vals = [P.lp_blind_toy(30, 200, s) for s in range(20)]
        greedy = [v["greedy_integer"] for v in vals]
        self.assertEqual((min(greedy), max(greedy)), (8, 12))
        self.assertEqual({v["fractional_2/3"] for v in vals}, {20.0})  # the other side never moves

    def test_reported_gap_does_not_grow_with_the_size_of_the_system(self):
        """§0's only quantitative claim: 'разрыв ... линейный по размеру системы'.  Along the
        module's own family (shipped m = 200) the ground set grows 5x and the reported gap stays
        flat in [9, 15] — its variation is greedy noise, not growth."""
        vals = {n: P.lp_blind_toy(n)["gap"] for n in (30, 45, 60, 90, 120, 150)}
        self.assertEqual(vals[30], 9.0)
        self.assertEqual(vals[150], 13.0)
        self.assertLessEqual(max(vals.values()) - min(vals.values()), 6.0)
        self.assertLess(vals[150], 2 * vals[30])      # linear growth would demand ~45

    @gap("GAP-T-01",
         module="phenomenon.py",
         title="the integer side of lp_blind_toy's 'gap' is a greedy heuristic, although the module "
               "itself computes the integer optimum exactly (P1 + its own tau solver)",
         expected="§0 defines the phenomenon as the gap between the relaxation and the INTEGER OPTIMUM, "
                  "P2 calls that gap 'суть явления', and lp_blind_toy is offered as its executable "
                  "demonstration ('Показывает P2 в чистом виде') under a key literally named 'gap'. The "
                  "integral side must therefore be alpha. The module even states how to get it — P1: "
                  "'max|S| = |V| − τ(H₃)' — and ships transversal_vs_fractional_toy, which computes τ "
                  "exactly by brute force on the SAME generator (proved identical here), so alpha = n − τ "
                  "is available inside the module for every instance the toy can handle. With no "
                  "constraints at all (m = 0) LP* = alpha = n, so the gap must be exactly 0.",
         actual="The integral side is one run of a greedy heuristic seeded by the same RNG. On the shipped "
                "default (30,200,0) greedy = 11 while a re-verified independent set of size 14 exists, so "
                "at least 3 of the 9 reported units are greedy failure; over seeds 0..19 the number swings "
                "8..12 with the hypergraph size fixed. On (15,25,0) the module's own τ = 5 gives alpha = 10 "
                "and an honest gap of 0.0 where the toy reports +2.0; on (15,12,0) τ = 3 gives alpha = 12 "
                "and an honest gap of −2.0 where the toy reports +1.0; at m = 0 it reports −10.0.",
         consequence="P2 — the principle on which the project bases its central negative conclusion (LP is "
                     "blind: covers plateau at LP(1) ≈ 3.45(p−1) and 11/3 → 115/32, so the covering route "
                     "is closed) — has no executable witness. The one number the module labels 'gap' "
                     "measures the failure of a greedy heuristic: it is positive on instances where the "
                     "module's own exact route gives zero or a negative value, so its sign carries no "
                     "information about integrality, and it does not grow with the size of the system, "
                     "which is the phenomenon's defining scaling claim.")
    def test_the_reported_gap_is_built_from_the_integer_optimum(self):
        # (a) the integral side must be alpha = n − tau, which the module itself can compute
        for (n, m, s) in [(15, 25, 0), (15, 12, 0)]:
            alpha = _alpha_via_the_modules_own_P1(n, m, s)
            self.assertEqual(P.lp_blind_toy(n, m, s)["greedy_integer"], alpha,
                             "the integral side must be the integer optimum n − tau = %d" % alpha)
        # (b) on the shipped default it must at least reach the certified independent set
        triples, _ = _replay_lp_blind(30, 200, 0)
        self.assertEqual(_triples_inside(triples, IND_30_200_0), 0)
        self.assertGreaterEqual(P.lp_blind_toy()["greedy_integer"], len(IND_30_200_0))
        # (c) with no constraints the relaxation and the integer optimum coincide: gap = 0
        self.assertEqual(P.lp_blind_toy(30, 0, 0)["gap"], 0.0)


# ══════════════════════════════════════════════════════════════════════════════════════════
class SupersaturationToy(unittest.TestCase):
    """supersaturation_toy: captioned as P3 ('|S| > alpha + C  =>  T(S) >= c(|S| - alpha - C)')."""

    def test_curve_is_the_hypergeometric_mean_and_ignores_the_hypergraph(self):
        """Every value equals m*C(k,3)/C(n,3) — a closed form in (n, m, k) only."""
        n, m = 40, 400
        for k, v in P.supersaturation_toy():
            closed = m * math.comb(k, 3) / math.comb(n, 3)
            self.assertLess(abs(v - closed), max(0.1, 0.06 * closed), (k, v, closed))

    def test_the_mean_is_provably_blind_to_structure(self):
        """Exact, no sampling: two 3-uniform hypergraphs on the same (n, m) = (5, 4).  One has an
        independent 4-set (min T = 0 at k = 4), the other has none (min T = 1), yet the EXACT mean
        of T over all C(5,4) subsets is 8/5 for both — the statistic the toy reports cannot see the
        difference that P3 is entirely about."""
        n, k, m = 5, 4, 4
        clique = [frozenset(t) for t in itertools.combinations(range(4), 3)]        # all triples in {0,1,2,3}
        star = [frozenset({0, 1, 2}), frozenset({0, 1, 3}), frozenset({0, 2, 3}), frozenset({0, 1, 4})]
        self.assertEqual((len(clique), len(star)), (m, m))
        stats = []
        for Hg in (clique, star):
            counts = [_triples_inside(Hg, S) for S in itertools.combinations(range(n), k)]
            stats.append((Fraction(sum(counts), len(counts)), min(counts)))
        self.assertEqual(stats[0][0], stats[1][0])                                  # identical means
        self.assertEqual(stats[0][0], Fraction(m * math.comb(k, 3), math.comb(n, 3)))
        self.assertEqual((stats[0][1], stats[1][1]), (1, 0))                        # different minima

    def test_growth_follows_the_hypergeometric_cubic(self):
        """Further evidence that the curve is the closed form: log-log slope ≈ 3 between k and 2k.
        (Not a defect by itself — P3 is a lower bound, so a fast-growing MINIMUM would satisfy it;
        the defect is that this is a mean.)"""
        curve = dict(P.supersaturation_toy())
        slope = math.log(curve[20] / curve[10]) / math.log(2.0)
        self.assertGreater(slope, 2.8)
        self.assertLess(slope, 3.4)

    def test_a_zero_triple_set_of_size_16_exists_in_the_toys_own_hypergraph(self):
        """min_{|S|=k} T(S) = 0 up to k = 16, while the toy's curve is 18.8 already at k = 15."""
        triples, curve = _replay_supersat(40, 400, 1)
        self.assertEqual(_triples_inside(triples, IND_40_400_1), 0)
        self.assertEqual(len(IND_40_400_1), 16)
        self.assertGreater(dict(curve)[15], 18.0)

    def test_project_data_say_the_mean_is_not_the_minimum(self):
        """The numbers are read out of pair_bound_notes.md (B.12) so this cannot drift from them:
        mean over orientations vs the true minimum, and B.12(iii)'s verdict on typical-case bounds."""
        if not os.path.exists(_NOTES):
            self.skipTest("pair_bound_notes.md not found at %s" % _NOTES)
        text = open(_NOTES, encoding="utf-8").read()
        self.assertIn("p=11: min_r T(S(r)) = 24 (mean 53.5", text)
        self.assertIn("p=13: 28 (mean 51.5)", text)
        self.assertIn("p=17: 42 (mean 71.5", text)
        self.assertIn("p=19: 48 (mean 118", text)
        self.assertIn('"typical" bounds cannot reach them', text)
        mean = {11: 53.5, 13: 51.5, 17: 71.5, 19: 118.0}
        true_min = {11: 24, 13: 28, 17: 42, 19: 48}
        ratios = [mean[p] / true_min[p] for p in mean]
        self.assertGreater(min(ratios), 1.7)
        self.assertGreater(max(ratios), 2.4)

    @gap("GAP-T-02",
         module="phenomenon.py",
         title="supersaturation_toy reports the MEAN over random subsets — a statistic that is "
               "provably independent of the hypergraph, so it cannot exhibit P3 at all",
         expected="P3 is a universally quantified LOWER bound: for EVERY S with |S| > alpha + C, "
                  "T(S) >= c(|S| − alpha − C); holes.py's H7 asks for exactly that lemma for the pair of "
                  "hyperbolae. The quantity it constrains is min_{|S|=k} T(S). Any executable form of P3 "
                  "— however crude — must therefore be a statistic that is 0 below the threshold and that "
                  "changes when the hypergraph changes.",
         actual="The toy returns the MEAN of T over 200 uniformly random k-subsets. For ANY 3-uniform "
                "hypergraph with m edges that mean is m*C(k,3)/C(n,3) — verified here numerically against "
                "the closed form and exactly on two hypergraphs with equal (n, m) whose minima differ "
                "(0 vs 1) while their exact means are identical. So the curve is positive at every k > 2 "
                "regardless of structure: on the toy's own instance a re-verified 16-element set with ZERO "
                "triples exists, yet the curve already reports 18.8 at k = 15.",
         consequence="The project's own data (pair_bound_notes B.12) give mean 53.5/51.5/71.5/118 against "
                     "true minima 24/28/42/48 — a factor 1.7–2.5 — and B.12(iii) states outright that "
                     "second-moment/'typical' bounds cannot reach the minimising orientations. The module's "
                     "only executable illustration of supersaturation is precisely the statistic the "
                     "project's own research rules out: it would report the same 'supersaturation' for a "
                     "system that has none, so it makes H7 — the declared soft-form fallback route to "
                     "3(p−1)+O(1) — look automatically available.")
    def test_curve_reports_zero_below_the_threshold_and_sees_the_hypergraph(self):
        triples, curve = _replay_supersat(40, 400, 1)
        self.assertEqual(_triples_inside(triples, IND_40_400_1), 0)   # alpha >= 16, certified
        d = dict(curve)
        for k in (5, 10, 15):
            self.assertEqual(d[k], 0.0,
                             "below the certified threshold alpha >= 16 a supersaturation curve must read 0")
        blind = 400 * math.comb(15, 3) / math.comb(40, 3)
        self.assertGreater(abs(d[15] - blind), 1.0,
                           "the reported value must depend on the hypergraph, not only on (n, m, k)")


# ══════════════════════════════════════════════════════════════════════════════════════════
class TransversalToy(unittest.TestCase):
    """transversal_vs_fractional_toy: 'τ (точно, перебором) против τ* ≤ n/3 ... разрыв — признак P1/P2'."""

    def test_shipped_default_values(self):
        out = _trans()
        self.assertEqual(out["tau_exact"], 10)
        self.assertEqual(out["n/3 (tau* upper bound)"], 8.0)
        self.assertAlmostEqual(out["E/Delta"], 60 / 13)

    def test_the_generator_also_produces_instances_with_no_gap_at_all(self):
        """(15,25,seed=0): tau_exact = 5 = n/3, i.e. tau <= the fractional bound — no gap shown,
        and the function reports it in exactly the same shape as seed=1, where tau = 6 > 5."""
        a = _trans(15, 25, 0)
        b = _trans(15, 25, 1)
        self.assertEqual(a["tau_exact"], 5)
        self.assertEqual(a["n/3 (tau* upper bound)"], 5.0)
        self.assertEqual(a["tau_exact"], a["n/3 (tau* upper bound)"])
        self.assertEqual(b["tau_exact"], 6)
        self.assertEqual(b["n/3 (tau* upper bound)"], 5.0)   # identical fractional slot

    def test_the_displayed_ratio_lives_in_a_window_open_to_every_3_uniform_hypergraph(self):
        """P2 says 'в наших системах τ ≫ τ*'.  Rounding a fractional transversal y at 1/3 gives a
        transversal {v : y_v >= 1/3} of size <= 3*sum(y), so tau <= 3*tau* for EVERY 3-uniform
        hypergraph — the ratio can never exceed 3.  The toy displays 10 vs <= 8 (>= 1.25), and the
        same bound applied to §0's claimed truth for our system (|V| = 8(p−1), truth 3(p−1), so
        P1's identity gives tau = 5(p−1) against tau* <= 8(p−1)/3) puts it at >= 1.875: both sit in
        the same bounded window, so the ratio does not separate our system from any other."""
        out = _trans()
        self.assertGreater(out["tau_exact"] / out["n/3 (tau* upper bound)"], 1.25 - 1e-9)
        self.assertLessEqual(out["tau_exact"], 3 * out["n/3 (tau* upper bound)"])
        # our system, straight from OUR_FRAME/OUR_SIGNATURE: |V| = 8(p−1), truth 3(p−1)
        v = P.OUR_SIGNATURE.n_ground                       # 8(p−1) with p = 1999
        tau_ours = v - 3 * (v // 8)                        # |V| − 3(p−1) = 5(p−1)
        self.assertEqual(tau_ours, 5 * 1998)
        self.assertLessEqual(tau_ours / (v / 3), 3.0)
        self.assertGreater(tau_ours / (v / 3), 1.8)

    def test_zero_division_when_there_are_no_constraints(self):
        with self.assertRaises(ZeroDivisionError):
            P.transversal_vs_fractional_toy(24, 0, 2)

    def test_exact_route_is_exponential_and_unguarded(self):
        """Cost = sum_{k<tau} C(n,k) subsets; the module documents no limit and guards nothing."""
        out = _trans()
        tau = out["tau_exact"]
        cost = sum(math.comb(24, k) for k in range(tau))
        self.assertEqual(cost, 2579130)
        # holes.py's own smallest exactly solved instance: p = 11, |V| = 8(p-1) = 80, max = 32
        self.assertIn("11: 32", H.HOLES[0].testable_now)
        self.assertGreater(math.comb(80, 80 - 32), 2 * 10 ** 22)
        # and at the size OUR_SIGNATURE itself uses (p = 1999, |V| = 15984, tau ~ 5(p-1))
        self.assertEqual(P.OUR_SIGNATURE.n_ground, 15984)
        self.assertGreater(math.comb(15984, 15984 - 3 * 1998).bit_length(), 10000)


# ══════════════════════════════════════════════════════════════════════════════════════════
class UnboundedGenerators(unittest.TestCase):
    """m > C(n,3): every toy spins forever; n < 3: every toy raises. No validation anywhere."""

    def _assert_hangs(self, expr):
        with self.assertRaises(subprocess.TimeoutExpired):
            _child(expr, timeout=2.5)

    def test_lp_blind_toy_hangs(self):
        self._assert_hangs("P.lp_blind_toy(6, 21, 0)")          # C(6,3) = 20 < 21

    def test_supersaturation_toy_hangs(self):
        self._assert_hangs("P.supersaturation_toy(6, 21, 1)")

    def test_transversal_toy_hangs(self):
        self._assert_hangs("P.transversal_vs_fractional_toy(6, 21, 2)")

    def test_all_three_raise_below_three_vertices(self):
        for fn, args in ((P.lp_blind_toy, (2, 1, 0)),
                         (P.supersaturation_toy, (2, 1, 1)),
                         (P.transversal_vs_fractional_toy, (2, 1, 2))):
            with self.assertRaises(ValueError):
                fn(*args)


# ══════════════════════════════════════════════════════════════════════════════════════════
class TwoTierSplitIsNeverExercised(unittest.TestCase):
    """§0 defines the phenomenon by the split STRONG (|l| >= 2cap+1) / WEAK (|l| = cap+1)."""

    def test_every_constraint_of_every_toy_is_weak(self):
        inst = [_triples_set(30, 200, 0)[0],
                _triples_set(40, 400, 1)[0],
                set(_triples_list(24, 60, 2)[0])]
        for triples in inst:
            self.assertEqual({len(t) for t in triples}, {3})
            self.assertIs(P.OUR_FRAME.strength(3), P.Strength.WEAK)

    def test_no_toy_takes_a_capacity(self):
        import inspect
        for fn in (P.lp_blind_toy, P.supersaturation_toy, P.transversal_vs_fractional_toy):
            names = set(inspect.signature(fn).parameters)
            self.assertEqual(names, {"n", "m", "seed"})
            self.assertNotIn("cap", names)

    def test_no_toy_ever_consults_the_frame(self):
        """Instrumenting Frame.strength records zero calls across all three toys: cap = 2 survives
        in the executable part only as the hard-coded literals 2/3 and 3."""
        orig = P.Frame.strength
        seen = []

        def counting(frame, size):
            seen.append(size)
            return orig(frame, size)

        P.Frame.strength = counting
        try:
            P.lp_blind_toy(12, 20, 0)
            P.supersaturation_toy(12, 20, 1)
            P.transversal_vs_fractional_toy(12, 20, 2)
        finally:
            P.Frame.strength = orig
        self.assertEqual(seen, [])

    def test_the_random_toy_matches_our_signature_on_every_condition_it_can_supply(self):
        """Of verdict()'s four conditions only two are derivable from a constraint system (S1:
        n_weak >= n_ground, S3: max_codegree <= 8).  Both hold for the toy's uniformly random
        hypergraph, whose max codegree is 6 — the exact value OUR_SIGNATURE declares for our
        system.  The other two inputs are mandatory and no toy can produce them."""
        triples, _ = _triples_set(30, 200, 0)
        max_codeg = max(_codegrees(triples).values())
        self.assertEqual(max_codeg, 6)
        self.assertEqual(P.OUR_SIGNATURE.max_codegree, 6)
        self.assertGreaterEqual(len(triples), 30)                # S1 exactly as verdict() codes it
        self.assertLessEqual(max_codeg, 8)                       # S3 exactly as verdict() codes it
        with self.assertRaises(TypeError):                       # S2 and S4 have no executable source
            P.Signature(n_weak=len(triples), n_ground=30, mean_degree=20.0, max_codegree=max_codeg)

    @gap("GAP-T-03",
         module="phenomenon.py",
         title="no toy contains a STRONG constraint: the two-tier system whose interaction §0 uses "
               "to DEFINE the phenomenon is never instantiated",
         expected="§0 defines the phenomenon as an interaction of two sorts of constraint — STRONG "
                  "(|l| >= 2cap+1: rows, columns, slopes ±1) and WEAK (|l| = cap+1) — and asserts that the "
                  "truth is fixed by the weak ones JOINTLY rather than by the strong ones; S2 states it "
                  "quantitatively as LP(all) ≈ LP(strong). An executable model of that claim must contain "
                  "both sorts of constraint, so that the two regimes can be compared at all.",
         actual="All three toys build one and the same uniformly random 3-uniform hypergraph (proved "
                "identical here): every constraint has size 3 = cap+1, so Frame.strength classifies all of "
                "them WEAK and not a single STRONG constraint exists in any executable line of the module. "
                "Frame, OUR_FRAME, Strength and capacity are never read by any toy (instrumenting "
                "Frame.strength records zero calls); the signatures are (n, m, seed) and cap = 2 survives "
                "only as the literals 2/3 and 3.",
         consequence="Everything the module executes is compatible with 'uniformly random 3-uniform "
                     "hypergraphs have integrality gaps' — true of systems with none of the project's "
                     "structure (no algebraic extremals, no rich lines, no construction to exceed by O(1)). "
                     "S2 and S6, the two signatures that carry the project's decision to abandon covers, "
                     "are never measured, and the two signature conditions that ARE derivable from a "
                     "constraint system are met by the toy's random hypergraph exactly as by ours (max "
                     "codegree 6 in both). Nothing in the module distinguishes our system from a random "
                     "one, and the claim that the weak constraints jointly decide the optimum is nowhere "
                     "exercised by code.")
    def test_a_toy_instantiates_the_strong_weak_split(self):
        sizes = set()
        for triples in (_triples_set(30, 200, 0)[0],
                        _triples_set(40, 400, 1)[0],
                        set(_triples_list(24, 60, 2)[0])):
            sizes |= {len(t) for t in triples}
        strong = {s for s in sizes if P.OUR_FRAME.strength(s) is P.Strength.STRONG}
        self.assertTrue(strong,
                        "no toy ever builds a constraint of size >= 2*cap+1 = 5; sizes built: %r" % sizes)


# ══════════════════════════════════════════════════════════════════════════════════════════
class FractionalSideIsAConstant(unittest.TestCase):
    """Both toys put a universal constant in the slot where an LP value belongs."""

    def test_a_same_size_instance_whose_lp_optimum_is_at_least_26(self):
        """30 vertices, 200 triples, all inside {0..11}: x = 1 outside, 2/3 inside is feasible."""
        triples = [frozenset(t) for t in itertools.combinations(range(12), 3)][:200]
        self.assertEqual(len(triples), 200)
        x = {v: (Fraction(1) if v >= 12 else Fraction(2, 3)) for v in range(30)}
        for t in triples:
            self.assertLessEqual(sum(x[v] for v in t), 2)
        self.assertTrue(all(0 <= x[v] <= 1 for v in x))
        self.assertEqual(sum(x.values()), 26)                       # so LP* >= 26 > 2n/3 = 20
        self.assertEqual(P.lp_blind_toy(30, 200, 0)["fractional_2/3"], 20.0)

    def test_the_fractional_slot_falls_below_the_integer_optimum(self):
        """(15,12,0): the module's own tau = 3 gives alpha = 12 (and the certificate below confirms
        12 independent vertices), while the slot called 'fractional' reports 10.0 — a relaxation
        value strictly under the integer optimum it is supposed to dominate."""
        triples, _ = _replay_lp_blind(15, 12, 0)
        self.assertEqual(_triples_inside(triples, IND_15_12_0), 0)
        self.assertEqual(len(IND_15_12_0), 12)
        self.assertEqual(_alpha_via_the_modules_own_P1(15, 12, 0), 12)
        out = P.lp_blind_toy(15, 12, 0)
        self.assertEqual(out["fractional_2/3"], 10.0)
        self.assertLess(out["fractional_2/3"], 12)

    @gap("GAP-T-04",
         module="phenomenon.py",
         title="no executable line of the module computes a fractional optimum: both 'fractional' "
               "slots are constants in n",
         expected="P2/S2/S6 are statements about LP VALUES (τ*(H₃), LP(all)/LP(strong), the 3.45 plateau). "
                  "The toys are the module's only executable content; lp_blind_toy reports a 'fractional' "
                  "value and transversal_vs_fractional_toy reports 'n/3 (τ* upper bound)'. Whatever "
                  "occupies those slots must be a property of the constraint system — at fixed n the "
                  "packing LP optimum provably varies with the constraints (m = 0 gives exactly n, and any "
                  "one triple already forces LP* <= n − 1) — and it must dominate the integer optimum.",
         actual="Both slots are hard-coded constants, 2n/3 and n/3, depending on n alone. lp_blind_toy(30, "
                "m) returns 20.0 for m = 0, 50 and 200 alike, although with zero constraints the LP optimum "
                "is exactly 30, and a 3-uniform hypergraph with the same (n, m) = (30, 200) has LP optimum "
                ">= 26 (exhibited here, feasibility certified in exact Fraction arithmetic). On (15,12,0) "
                "the slot reads 10.0 while the module's own τ = 3 gives alpha = 12, so the 'relaxation' is "
                "strictly below the integer optimum. transversal_vs_fractional_toy prints 5.0 in the "
                "fractional slot both for the instance with τ = 5 and for the one with τ = 6.",
         consequence="The module asserts LP blindness as the heart of the phenomenon but never evaluates "
                     "an LP, so nothing in it can tell a blind relaxation from a tight one, and S2 "
                     "(LP(all) ≈ LP(strong)) and S6 (local certificates plateau) cannot be measured on any "
                     "system at all. The project's quantitative claims — LP(1) ≈ 3.45(p−1), IP(1) = LP(1) − "
                     "O(1), 11/3 → 115/32 — enter the specification as prose and are carried by no "
                     "computation the specification can run, which is exactly what a reader would take the "
                     "toys to have checked.")
    def test_fractional_slots_track_the_instance(self):
        # At n = 30 the packing LP optimum provably varies with the constraint system:
        # m = 0 gives exactly 30, and one triple already caps it at 29.
        vals = {P.lp_blind_toy(30, m, 0)["fractional_2/3"] for m in (0, 50, 200)}
        self.assertGreater(len(vals), 1,
                           "the fractional value depends on n alone: %r for m = 0, 50, 200" % vals)
        self.assertEqual(P.lp_blind_toy(30, 0, 0)["fractional_2/3"], 30.0,
                         "with no constraints the packing LP optimum is n = 30")
        # and it must dominate the integer optimum the module itself can compute
        self.assertGreaterEqual(P.lp_blind_toy(15, 12, 0)["fractional_2/3"],
                                _alpha_via_the_modules_own_P1(15, 12, 0))


# ══════════════════════════════════════════════════════════════════════════════════════════
class Determinism(unittest.TestCase):
    """Given a seed the toys are reproducible across processes (frozenset-of-int hashing is stable)."""

    def _two_runs(self, expr):
        env_a = dict(os.environ, PYTHONHASHSEED="0")
        env_b = dict(os.environ, PYTHONHASHSEED="12345")
        code = "import sys; sys.path.insert(0, %r); import phenomenon as P; print(%s)" % (_MODDIR, expr)
        outs = []
        for env in (env_a, env_b):
            r = subprocess.run([sys.executable, "-W", "ignore", "-c", code],
                               capture_output=True, text=True, timeout=60, env=env)
            self.assertEqual(r.returncode, 0, r.stderr)
            outs.append(r.stdout)
        return outs

    def test_lp_blind_toy_is_reproducible(self):
        a, b = self._two_runs("P.lp_blind_toy()")
        self.assertEqual(a, b)
        self.assertIn("'greedy_integer': 11", a)

    def test_supersaturation_toy_is_reproducible(self):
        a, b = self._two_runs("P.supersaturation_toy()[:3]")
        self.assertEqual(a, b)

    def test_transversal_toy_is_reproducible(self):
        a, b = self._two_runs("P.transversal_vs_fractional_toy(15, 25, 0)")
        self.assertEqual(a, b)


if __name__ == "__main__":
    unittest.main(verbosity=2)
