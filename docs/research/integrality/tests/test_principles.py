"""test_principles.py — P1-P5 and S1-S6 read as logical statements: counterexamples, tautologies, blind zones.

The lens is NOT "does phenomenon.py run".  It is: taken as assertions about systems, what do the five
principles and the six signatures actually forbid?  A principle no system can violate forbids nothing; a
signature condition that geometry guarantees is a free vote; a formula that predicts a number worse than
the project's own one-line trivial bound is not a reformulation of the problem.

Everything is built from stdlib and from the module's own descriptions.  The reference system is the one
OUR_FRAME names ("лифты двух гипербол xy ≡ ±1 (mod p) в коробке 2p×2p: 8(p−1) точек"), rebuilt here and
self-validated against the frame's own text (test_frame_realisation_is_faithful).

Convention for the @gap tests: the assertion that FAILS is a function of the specification, so that repairing
the module makes it pass, unittest reports an unexpected success, and the run turns red.  Facts about the
world that no repair of the module could change (a decomposable system's LP/IP ratio, the equivalence of
supersaturation and the exact bound) are asserted as ORDINARY tests and used only as the evidence a gap rests
on — an xfail that would fail against a perfect specification records nothing.
"""
import os
import sys
import unittest
from dataclasses import replace
from fractions import Fraction
from itertools import combinations, product
from math import gcd

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)                       # tests/gaps.py
sys.path.insert(0, os.path.dirname(_HERE))      # phenomenon.py, holes.py
from gaps import gap                            # noqa: E402
import phenomenon as P                          # noqa: E402
import holes as H                               # noqa: E402


# ══════════════════════════════════════════════════════════════════════════════════════════════
# 0. Machinery: packing systems, the frame's own ground set, exact τ / max-independent-set
# ══════════════════════════════════════════════════════════════════════════════════════════════

class System:
    """A frame instance: ground set V, a family of constraints (subsets of V), a capacity.

    weak  = constraints of size exactly cap+1   (Strength.WEAK by the module's own definition)
    rich  = constraints of size >= 2*cap+1      (Strength.STRONG by its own docstring)
    """

    def __init__(self, name, points, constraints, cap=2):
        self.name = name
        self.points = list(points)
        self.index = {q: i for i, q in enumerate(self.points)}
        self.constraints = [frozenset(c) for c in constraints]
        self.cap = cap

    @property
    def n(self):
        return len(self.points)

    def weak(self):
        return [c for c in self.constraints if len(c) == self.cap + 1]

    def rich(self):
        return [c for c in self.constraints if len(c) >= 2 * self.cap + 1]

    def middle(self):
        """cap+1 < |l| < 2*cap+1 — neither WEAK nor STRONG by the docstrings.  For cap=2: |l| = 4."""
        return [c for c in self.constraints if self.cap + 1 < len(c) < 2 * self.cap + 1]

    def lawful(self, S):
        S = set(S)
        return all(len(c & S) <= self.cap for c in self.constraints)

    def h3(self):
        """H₃ exactly as P1 defines it: 'тройки кандидатов ... здесь и далее только 3-точечные прямые'."""
        return [set(c) for c in self.weak()]

    def all_collinear_triples(self):
        """The other reading: every (cap+1)-subset of every constraint, rich lines included."""
        out = set()
        for c in self.constraints:
            for t in combinations(sorted(c, key=lambda q: self.index[q]), self.cap + 1):
                out.add(frozenset(t))
        return [set(t) for t in out]


def max_edge_free(n, edges):
    """max |S| over S ⊆ [n] containing no whole edge (= n − τ, the P1 quantity).  Exact, small n only."""
    for k in range(n, -1, -1):
        for S in combinations(range(n), k):
            Ss = set(S)
            if not any(e <= Ss for e in edges):
                return k
    return 0


def tau_exact(n, edges):
    for k in range(0, n + 1):
        for T in combinations(range(n), k):
            Ts = set(T)
            if all(e & Ts for e in edges):
                return k
    return n


def greedy_edge_free(n, edges, restarts=60):
    """A certified LOWER bound on max_edge_free: returns an actual edge-free set, so |result| <= |V| − τ.

    The insertion orders are the deterministic permutations i ↦ (a·i + b) mod n, so the result does not
    depend on the platform's RNG.
    """
    inc = [[] for _ in range(n)]
    for i, e in enumerate(edges):
        for v in e:
            inc[v].append(i)
    best = set()
    deg = [len(inc[v]) for v in range(n)]
    orders = [sorted(range(n), key=lambda i: (deg[i], i))]
    for a in range(1, n):
        if gcd(a, n) == 1:
            for b in (0, 1, n // 2, n // 3):
                orders.append(sorted(range(n), key=lambda i, a=a, b=b: (a * i + b) % n))
                orders.append(sorted(range(n), key=lambda i, a=a, b=b: (deg[i], (a * i + b) % n)))
        if len(orders) >= restarts:
            break
    for order in orders[:restarts]:
        S = set()
        for v in order:
            if all(not (edges[i] - {v} <= S) for i in inc[v]):
                S.add(v)
        if len(S) > len(best):
            best = S
    assert all(not (e <= best) for e in edges)
    return best


# ── the frame's own ground set ────────────────────────────────────────────────────────────────

def hyperbola_pair(p):
    """Lifts of xy ≡ +1 and xy ≡ −1 (mod p) into the 2p×2p box — OUR_FRAME.ground_set."""
    pts = []
    for a in range(1, p):
        ia = pow(a, -1, p)
        for y0 in (ia, (-ia) % p):
            for dx in (0, p):
                for dy in (0, p):
                    pts.append((a + dx, y0 + dy))
    return sorted(set(pts))


def maximal_lines(pts, min_size=3):
    """Maximal collinear subsets of size >= min_size — OUR_FRAME.constraints ('все прямые плоскости')."""
    seen = {}
    for A, B in combinations(pts, 2):
        dx, dy = B[0] - A[0], B[1] - A[1]
        g = gcd(abs(dx), abs(dy))
        u, v = dx // g, dy // g
        if u < 0 or (u == 0 and v < 0):
            u, v = -u, -v
        seen.setdefault((u, v, u * A[1] - v * A[0]), set()).update((A, B))
    return {k: frozenset(s) for k, s in seen.items() if len(s) >= min_size}


_FRAME_CACHE = {}


def our_system(p):
    if p not in _FRAME_CACHE:
        pts = hyperbola_pair(p)
        lines = maximal_lines(pts)
        _FRAME_CACHE[p] = (System(f"P_-1(p={p})", pts, lines.values(), cap=2), lines)
    return _FRAME_CACHE[p]


# ── exact data the project itself measured (pair_bound_notes.md) ──────────────────────────────
#   §2 table (k = −1): p=17 → α=54, p=19 → α=59.
#   §7 "All k (exact, MIP): p=11: 32–35"; §4 lists k=2→33, k=3→35, k=−1→32.  So α(P₋₁)(11) = 32.
ALPHA_KM1 = {11: 32, 17: 54, 19: 59}
ALPHA_K3_11 = 35            # §2/§4: p=11, k=3
LP_ALL = {17: 60.15, 19: 63.6}    # B.11 point 3: "only IP(∞) shows it (54 vs 60.15 …; 59 vs 63.6 …)"
LP_STRONG = {17: 62, 19: 64}      # B.7: LP(1) = rows + columns + slope ±1 only
#   §7 "All k (exact, MIP): p=11: 32–35; p=13: 38–41; p=17: 49–54" — over the exactly solved instances the
#   gain over 3(p−1) runs from +2 to +6 whichever k attains it; B.6(c) records only the per-p MAXIMUM
#   ("+5,+5,+6,+5 for p=11…19"), which is the sequence phenomenon.py entered.
ALL_K_EXACT = {11: (32, 35), 13: (38, 41), 17: (49, 54)}
B6C_MAX_GAINS = (5, 5, 6, 5)
#   cap sets in F₃ⁿ: exact maxima for n ≤ 6, and the algebraic construction {0,1}ⁿ (a+b+c = 0 inside {0,1}ⁿ
#   forces a = b = c coordinatewise, so it contains no line).
CAPSET_TRUTH = (2, 4, 9, 20, 45, 112)
CAPSET_CONSTRUCTION = tuple(2 ** n for n in range(1, 7))


# ── reading the specification's own prose (the @gap trackers) ─────────────────────────────────

def section_0_definition():
    """The sentence of §0 that DEFINES the phenomenon (its two clauses), without §0's own numbers."""
    doc = P.__doc__
    i = doc.index("ЯВЛЕНИЕ:")
    return doc[i:doc.index("У нас:", i)]


def principle_prose(key):
    """The §1 paragraph behind Principle `key` — the module's full text for P1…P5."""
    doc = P.__doc__
    start = doc.index("\n" + key + ".")
    later = [doc.index("\n" + k + ".") for k in ("P1", "P2", "P3", "P4", "P5")
             if "\n" + k + "." in doc and doc.index("\n" + k + ".") > start]
    return doc[start:min(later) if later else doc.index("─" * 10, start)]


#   Properties a system that falls apart into independent blocks of five would FAIL.  §0's definition names
#   none of them; §4's "essence" paragraph names two.  Used as the tracker of GAP-P-01.
STRUCTURAL_TOKENS = ("расшир", "связн", "распада", "неразложим", "глобальн", "жёстк", "костепен")
#   How the module marks a claim that is measured rather than proved (§0 "(по всем точным данным)",
#   P2 "(проверено: … при p ≤ 59)").  Used as the tracker of GAP-P-08.
STATUS_MARKERS = ("проверено", "численно", "точным данным", "гипотеза", "открыт", "не доказан", "данные")


# ── synthetic systems used as counterexamples ────────────────────────────────────────────────

def rich_line_system(cap, r):
    """V = one line of r > cap+1 points.  No constraint has size cap+1 ⇒ H₃ = ∅ ⇒ τ(H₃) = 0."""
    pts = list(range(r))
    return System(f"one {r}-point line, cap={cap}", pts, [pts], cap=cap)


def blocks_system(m, cap=2, block=5):
    """m disjoint blocks of `block` points; every (cap+1)-subset of a block is a constraint.

    Every constraint has size cap+1 — ALL of them are WEAK by the module's own classification, so §0's
    "истинный оптимум определяется совместным действием СЛАБЫХ ограничений" holds by construction.
    LP = (block/(cap+1))*cap per block, IP = cap per block: a LINEAR gap, §0's second clause.
    And the system falls apart into independent blocks of 5 — no globality whatever.
    """
    pts, cons = [], []
    for b in range(m):
        blk = [(b, i) for i in range(block)]
        pts += blk
        cons += [set(c) for c in combinations(blk, cap + 1)]
    return System(f"{m} blocks of {block}", pts, cons, cap=cap)


def blocks_lp(m, cap=2, block=5):
    """Exact LP value of blocks_system, proved by primal + dual (no solver).

    primal  x ≡ cap/(cap+1) is feasible, value block*cap/(cap+1) per block;
    dual    summing all C(block,cap+1) constraints, each point occurs C(block-1,cap) times, giving
            Σx ≤ cap*C(block,cap+1)/C(block-1,cap) = block*cap/(cap+1).  Equal ⇒ optimal.
    """
    from math import comb
    per_block_primal = Fraction(block * cap, cap + 1)
    per_block_dual = Fraction(cap * comb(block, cap + 1), comb(block - 1, cap))
    assert per_block_primal == per_block_dual
    return m * per_block_primal


def capset(n):
    """Cap sets in F₃ⁿ — the bestiary's own entry.  Every 'line' has exactly 3 points ⇒ all WEAK."""
    pts = list(product(range(3), repeat=n))
    idx = {q: i for i, q in enumerate(pts)}
    lines = set()
    for i, a in enumerate(pts):
        for j, b in enumerate(pts):
            if i < j:
                c = tuple((-a[k] - b[k]) % 3 for k in range(n))
                lines.add(frozenset((i, j, idx[c])))
    return System(f"F_3^{n}", list(range(len(pts))), lines, cap=2)


def grid_system(N):
    """no-three-in-line in [N]² — the bestiary's "то же явление в чистом виде"."""
    pts = [(x, y) for x in range(N) for y in range(N)]
    return System(f"[{N}]^2", pts, maximal_lines(pts).values(), cap=2)


# ══════════════════════════════════════════════════════════════════════════════════════════════
# 1. The realisation of OUR_FRAME is faithful to the frame's own text
# ══════════════════════════════════════════════════════════════════════════════════════════════

class FrameRealisation(unittest.TestCase):

    def test_frame_realisation_is_faithful(self):
        """|V| = 8(p−1); rows/columns carry 4 points; every line with >= 5 candidates has slope ±1."""
        for p in (11, 13, 17, 19):
            sysm, lines = our_system(p)
            self.assertEqual(sysm.n, 8 * (p - 1), f"p={p}")
            cols = {}
            rows = {}
            for (x, y) in sysm.points:
                cols[x] = cols.get(x, 0) + 1
                rows[y] = rows.get(y, 0) + 1
            self.assertEqual(set(cols.values()), {4}, f"p={p}: columns must carry 4 points")
            self.assertEqual(set(rows.values()), {4}, f"p={p}: rows must carry 4 points")
            self.assertEqual(len(cols), 2 * (p - 1))
            big = {(u, v) for (u, v, _c), s in lines.items() if len(s) >= 5}
            self.assertTrue(big <= {(1, 1), (1, -1)},
                            f"p={p}: OUR_FRAME says the rich lines are rows/columns and slopes ±1, got {big}")
            self.assertLessEqual(max(len(s) for s in lines.values()), 8,
                                 f"p={p}: OUR_FRAME says slope-±1 lines carry 'до 8' points")

    def test_frame_strength_leaves_the_project_s_own_lines_unclassified(self):
        """Rows and columns (4 points, cap=2) are neither WEAK (=3) nor STRONG (>= 5) by the docstrings."""
        for p in (11, 13, 17, 19):
            sysm, _ = our_system(p)
            mid = sysm.middle()
            self.assertGreater(len(mid), 0)
            self.assertEqual({len(c) for c in mid}, {4})
            # Frame.strength() nevertheless calls every one of them STRONG.
            self.assertIs(P.OUR_FRAME.strength(4), P.Strength.STRONG)
            self.assertIn("2·cap+1", P.Strength.STRONG.value)


# ══════════════════════════════════════════════════════════════════════════════════════════════
# 2. P1  "max|S| = |V| − τ(H₃)"   with H₃ = the 3-point lines only
# ══════════════════════════════════════════════════════════════════════════════════════════════

class PrincipleP1(unittest.TestCase):
    """P1 states an identity.  Under the module's own restriction of H₃ it is not an identity."""

    def test_p1_is_stated_with_the_three_point_restriction(self):
        self.assertIn("только 3‑точечные прямые", P.__doc__)
        p1 = [x for x in P.PRINCIPLES if x.key.startswith("P1")][0]
        self.assertIn("max|S| = |V| − τ(H₃)", p1.statement)

    def test_p1_gap_is_unbounded_on_a_parametrised_rich_line_family(self):
        """One line of r points, capacity c: τ(H₃) = 0, P1 predicts r, the truth is c.  Gap r − c → ∞."""
        witnessed = []
        for cap in (2, 3, 4):
            for r in range(cap + 2, cap + 8):
                sysm = rich_line_system(cap, r)
                h3 = sysm.h3()
                self.assertEqual(h3, [], "no constraint has size cap+1, so H₃ is empty")
                self.assertEqual(tau_exact(sysm.n, h3), 0)
                p1_prediction = sysm.n - 0
                truth = max_edge_free(sysm.n, [set(c) for c in sysm.all_collinear_triples()])
                self.assertEqual(truth, cap, "the true optimum on one r-point line is cap")
                self.assertEqual(p1_prediction, r)
                witnessed.append(r - cap)
        self.assertEqual(max(witnessed), 7, "the P1 error grows with the line length without bound")

    def test_p1_equivalence_fails_on_the_frame_s_own_ground_set(self):
        """Any 3 points of a row are H₃-independent (a row has 4 points, so no 3-point line lies in it)
        and yet unlawful.  So 'S допустимо ⇔ S независимо в H₃' is false on OUR_FRAME itself."""
        for p in (11, 13, 17, 19):
            sysm, lines = our_system(p)
            row = next(s for (u, v, _c), s in lines.items() if (u, v) == (1, 0) and len(s) == 4)
            S = set(sorted(row)[:3])
            self.assertFalse(any(set(w) <= S for w in sysm.weak()),
                             f"p={p}: S contains no whole 3-point line")
            self.assertFalse(sysm.lawful(S), f"p={p}: yet S has 3 points on a row, so it is unlawful")

    def test_p1_literal_prediction_for_our_frame_is_worse_than_the_trivial_bound(self):
        """|V| − τ(H₃) with H₃ = 3-point lines only, on the frame's own ground set.

        pair_bound_notes §1 proves α ≤ 4(p−1) in three lines from rows and columns alone.  P1 read
        literally discards rows, columns and the ±1 lines, and its prediction lands ABOVE 4(p−1) at
        every p — i.e. above every bound the project has ever proved."""
        report = {}
        for p in (11, 13, 17, 19):
            sysm, _ = our_system(p)
            h3 = [set(sysm.index[q] for q in c) for c in sysm.weak()]
            S = greedy_edge_free(sysm.n, h3)
            lower_bound_on_p1 = len(S)      # |V| − τ(H₃) >= |S| for any H₃-independent S
            trivial = 4 * (p - 1)
            report[p] = (lower_bound_on_p1, trivial, ALPHA_KM1.get(p))
            self.assertGreater(lower_bound_on_p1, trivial,
                               f"p={p}: P1's prediction {lower_bound_on_p1} vs trivial 4(p−1)={trivial}")
            if p in ALPHA_KM1:
                self.assertGreaterEqual(lower_bound_on_p1 - ALPHA_KM1[p], 15,
                                        f"p={p}: P1 over-predicts α={ALPHA_KM1[p]} by {lower_bound_on_p1}")
        self.assertEqual(sorted(report), [11, 13, 17, 19])
        # observed (lower bound on P1's prediction, trivial 4(p−1), α):
        #   p=11: 56 / 40 / 32     p=13: 76 / 48 / —     p=17: 72 / 64 / 54     p=19: 96 / 72 / 59

    def test_the_repaired_reading_of_h3_destroys_the_weak_strong_split(self):
        """Reading H₃ as 'all collinear triples' makes P1 true — and then H₃'s edges are no longer the
        'ограничения размера cap+1' of S1: they include triples cut out of the 8-point ±1 lines, whose
        pair-codegree is 6.  The module cannot have P1 and its own §0 dichotomy at the same time."""
        for p in (11, 19):
            sysm, _ = our_system(p)
            allt = [set(sysm.index[q] for q in t) for t in sysm.all_collinear_triples()]
            weak = [set(sysm.index[q] for q in c) for c in sysm.weak()]
            self.assertGreater(len(allt), len(weak))
            codeg = {}
            for t in allt:
                for pr in combinations(sorted(t), 2):
                    codeg[pr] = codeg.get(pr, 0) + 1
            self.assertEqual(max(codeg.values()), 6,
                             "= 8 − 2: the repaired H₃ is carried by the STRONG 8-point lines")
            eight = [c for c in sysm.constraints if len(c) == 8]
            self.assertTrue(eight, f"p={p}: the frame's 8-point ±1 lines exist")


# ══════════════════════════════════════════════════════════════════════════════════════════════
# 3. P2  "τ* ≤ |V|/3 always; τ ≫ τ*; no rank-1 relaxation closes it"
# ══════════════════════════════════════════════════════════════════════════════════════════════

class PrincipleP2(unittest.TestCase):

    def test_tau_star_le_v_over_3_is_a_tautology_for_3_uniform_hypergraphs(self):
        """x ≡ 1/3 is a feasible fractional transversal of ANY 3-uniform hypergraph and has value |V|/3,
        so 'τ*(H₃) ≤ |V|/3 всегда' holds for every system whatever — including systems where nothing
        resembling the phenomenon happens.  P2 offers it as an observation about 'наших системах'."""
        for sysm in (blocks_system(4), capset(2), our_system(11)[0],
                     System("K_7^(3)", list(range(7)), combinations(range(7), 3), cap=2)):
            h3 = sysm.h3()
            self.assertTrue(h3, sysm.name)
            x = Fraction(1, 3)
            self.assertTrue(all(len(e) * x >= 1 for e in h3), "x ≡ 1/3 covers every 3-edge")
            self.assertEqual(sysm.n * x, Fraction(sysm.n, 3), "its value is |V|/3")

    def test_tau_over_tau_star_can_never_exceed_3(self):
        """Rounding lemma: for ANY feasible fractional cover x, T = {v : x_v >= 1/3} is a cover and
        |T| <= 3·Σx.  Hence τ <= 3τ* for every 3-uniform hypergraph — 'τ ≫ τ*' is bounded by 3."""
        import random
        rnd = random.Random(11)
        worst = Fraction(0)
        for _ in range(300):
            n = rnd.randint(6, 9)
            allE = list(combinations(range(n), 3))
            edges = [set(e) for e in rnd.sample(allE, rnd.randint(1, min(14, len(allE))))]
            x = [Fraction(rnd.randint(0, 6), 12) for _ in range(n)]
            for e in edges:                      # repair into feasibility
                s = sum(x[v] for v in e)
                if s < 1:
                    x[min(e)] += 1 - s
            self.assertTrue(all(sum(x[v] for v in e) >= 1 for e in edges))
            T = {v for v in range(n) if x[v] >= Fraction(1, 3)}
            self.assertTrue(all(e & T for e in edges), "the rounded set is a cover")
            self.assertLessEqual(Fraction(len(T)), 3 * sum(x))
            worst = max(worst, Fraction(len(T), 1) / sum(x))
        self.assertLessEqual(worst, 3)

    def test_the_maximal_tau_over_tau_star_belongs_to_the_complete_hypergraph(self):
        """K_n^(3): τ = n−2 (exact), τ* = n/3 (primal x ≡ 1/3 and dual y ≡ (n/3)/C(n,3) both of value
        n/3), so τ/τ* = 3(n−2)/n → 3, the ceiling.  Its extremal sets are 'any two points': no algebraic
        structure, no expansion, codegree n−2.  The quantity P2 calls 'суть явления' is maximised there."""
        from math import comb
        for n in range(5, 10):
            edges = [set(e) for e in combinations(range(n), 3)]
            self.assertEqual(tau_exact(n, edges), n - 2)
            y = Fraction(n, 3) / comb(n, 3)                     # fractional matching
            self.assertEqual(comb(n - 1, 2) * y, 1, "dual feasible")
            self.assertEqual(comb(n, 3) * y, Fraction(n, 3), "dual value = n/3 = primal value")
            self.assertEqual(Fraction(n - 2) / Fraction(n, 3), Fraction(3 * (n - 2), n))
        self.assertAlmostEqual(3 * (999 - 2) / 999, 2.994, places=3)

    def test_universal_reading_of_no_rank_1_certificate_is_false(self):
        """P2: 'Никакая LP-релаксация ранга 1 … его не закрывает.'  For a disjoint union of triples the
        rank-1 LP is exact: LP = IP = 2n/3.  Only the parenthetical ('проверено … при p ≤ 59') is true,
        and it is a measurement on one system at 11 primes (B.11), not a principle."""
        m = 7
        pts, cons = [], []
        for b in range(m):
            t = [(b, i) for i in range(3)]
            pts += t
            cons.append(set(t))
        sysm = System("disjoint triples", pts, cons, cap=2)
        self.assertEqual(len(sysm.weak()), m, "every constraint is weak")
        lp = Fraction(2 * len(pts), 3)                # x ≡ 2/3 feasible; sum of all constraints is tight
        ip = 2 * m                                    # take 2 of every triple
        self.assertEqual(lp, ip, "rank-1 LP closes the gap completely")
        p2 = [x for x in P.PRINCIPLES if x.key.startswith("P2")][0]
        self.assertIn("IP на тех же прямых = LP − O(1)", p2.statement)

    @gap("GAP-P-01",
         module="phenomenon.py §0 (ЯВЛЕНИЕ) + P2",
         title="the definition of the phenomenon is satisfied, more strongly than by our own system, "
               "by m disjoint blocks of 5 whose optimum is 2 per block",
         expected="§0 defines the phenomenon by two clauses: (a) the true optimum is determined by the "
                  "joint action of the WEAK constraints, not the strong ones; (b) the gap between LP "
                  "(with all constraints) and the integer optimum is linear in the size of the system. "
                  "A system meeting both is supposed to be one where the truth is out of reach — that is "
                  "the premise of deep_research_brief_8, which asks researchers to find systems 'where "
                  "this phenomenon lives' and to transfer the mechanisms that closed it there.",
         actual="BLOCKS(m) = m disjoint blocks of 5 points, all C(5,3)=10 triples of each block being "
                "constraints of capacity 2, meets both clauses maximally: every single constraint has "
                "size cap+1 (so (a) is vacuously perfect — there are no strong constraints at all), and "
                "LP = 10m/3 against IP = 2m, a gap of 4m/3 = (4/15)|V|, linear.  Its LP/IP ratio is 5/3 "
                "≈ 1.667 against 60.15/54 ≈ 1.114 for our own system at p=17, so on §0's own metric it "
                "exhibits the phenomenon MORE strongly than the project's system does.  Yet it splits "
                "into independent blocks of five points, its optimum is 'two per block', and §4's "
                "essence — ГЛОБАЛЬНАЯ ЖЁСТКОСТЬ — is entirely absent.  The defining sentence of §0 "
                "names no property (expansion, connectivity, indecomposability, globality) that such a "
                "system could fail — which is what the test asserts and what fails.",
         consequence="The definition on which the whole deep-research brief rests does not exclude "
                     "systems that are solved by inspection, and ranks them above the project's own "
                     "system.  Any analogue returned by the research (Q1-Q7) that satisfies §0 may be "
                     "decomposable and its 'closing mechanism' worthless here.  Exactly ONE statement "
                     "in either module rejects the blocks system — P2's middle clause 'LP(все прямые) "
                     "≈ LP(сильные)', i.e. signature S2, where the blocks system scores 2/3 — and S2 "
                     "is precisely the vote that Signature.verdict()'s 3-of-4 majority can afford to "
                     "lose (GAP-P-05).  §4's own answer, ГЛОБАЛЬНАЯ ЖЁСТКОСТЬ, appears in the essence "
                     "paragraph and in no definition, no field and no hole.")
    def test_section_0_definition_rejects_a_system_solved_by_inspection(self):
        m = 30
        sysm = blocks_system(m)
        # clause (a), maximally: there is no strong constraint at all, so whatever fixes the optimum is
        # the joint action of the weak ones.
        self.assertEqual(sysm.rich(), [], "clause (a): no strong constraint exists")
        self.assertEqual(len(sysm.weak()), len(sysm.constraints))
        # the optimum is "two per block", read off by inspection (checked exactly on one block).
        one = blocks_system(1)
        self.assertEqual(max_edge_free(one.n, [set(one.index[q] for q in c) for c in one.weak()]), 2)
        ip = 2 * m
        lp = blocks_lp(m)                                  # 10m/3: primal x ≡ 2/3, dual = sum of all triples
        self.assertEqual(lp, Fraction(10 * m, 3))
        # clause (b): the LP-IP gap is linear in the size of the system.
        self.assertEqual(lp - ip, Fraction(4 * m, 3))
        self.assertEqual(lp - ip, Fraction(4, 15) * sysm.n)
        # and on §0's own metric (LP over the integer optimum) it beats the project's own system.
        self.assertGreater(float(lp / ip), LP_ALL[17] / ALPHA_KM1[17])
        self.assertAlmostEqual(float(lp / ip), 5 / 3, places=9)
        # the one module statement that does reject it is P2's LP clause = S2, at 2/3 (no strong
        # constraints ⇒ LP with the strong ones alone is the unconstrained |V| = 5m):
        self.assertEqual(lp / Fraction(5 * m), Fraction(2, 3))
        p2 = [x for x in P.PRINCIPLES if x.key.startswith("P2")][0]
        self.assertIn("LP(все прямые) ≈ LP(сильные)", p2.statement)
        # §0's definition itself, however, states nothing a disjoint union of 5-blocks could fail:
        section0 = section_0_definition()
        self.assertIn("СЛАБЫХ", section0)
        self.assertIn("линейный по", section0)
        self.assertTrue(any(tok in section0 for tok in STRUCTURAL_TOKENS),
                        f"§0's definition names no structural property (expansion, connectivity, "
                        f"indecomposability, globality) that BLOCKS(m) lacks: {section0!r}")


# ══════════════════════════════════════════════════════════════════════════════════════════════
# 4. P3  supersaturation
# ══════════════════════════════════════════════════════════════════════════════════════════════

def p3_holds(n, edges, c, alpha, C):
    """P3 verbatim: |S| > α + C  ⇒  T(S) >= c·(|S| − α − C)."""
    for k in range(n + 1):
        if k <= alpha + C:
            continue
        for S in combinations(range(n), k):
            Ss = set(S)
            T = sum(1 for e in edges if e <= Ss)
            if T < c * (k - alpha - C):
                return False
    return True


class PrincipleP3(unittest.TestCase):

    def test_p3_statement_has_three_unbound_constants(self):
        """The pin for GAP-P-02: nothing in P3 — object or prose — binds c, α or C.  If the module ever
        calls them absolute, or quantifies over systems, this test goes red and GAP-P-02's search
        (which then has a falsifier) must be re-read."""
        p3 = [x for x in P.PRINCIPLES if x.key.startswith("P3")][0]
        self.assertEqual(p3.statement, "|S| > α + C ⇒ T(S) ≥ c(|S| − α − C) троек внутри S")
        text = p3.statement + p3.consequence + principle_prose("P3")
        for tok in ("абсолютн", "не зависящ", "равномерн", "∀", "для всех"):
            self.assertNotIn(tok, text, tok)

    def test_supersaturation_with_c_1_is_equivalent_to_the_exact_bound(self):
        """(max edge-free <= A)  ⟺  (∀S: T(S) >= |S| − A).

        ⇐ trivial (T = 0 on an edge-free S).  ⇒ delete one point per edge inside S.
        Verified exhaustively on 400 random hypergraphs — no separating instance exists.
        This is exactly what pair_bound_notes B.12 records: 'H4 is not an intermediate hypothesis but
        the target itself in supersaturation form'."""
        import random
        rnd = random.Random(11)
        checked = 0
        for _ in range(400):
            n = rnd.randint(5, 8)
            allE = list(combinations(range(n), 3))
            edges = [set(e) for e in rnd.sample(allE, rnd.randint(0, min(12, len(allE))))]
            A = max_edge_free(n, edges)
            for k in range(A + 1, n + 1):
                for S in combinations(range(n), k):
                    Ss = set(S)
                    T = sum(1 for e in edges if e <= Ss)
                    checked += 1
                    self.assertGreaterEqual(T, k - A, (n, edges, S))
        self.assertGreater(checked, 1000)

    def test_b12_states_the_equivalence_for_the_project_s_own_hole(self):
        """holes.py H7 is the supersaturation form; its payoff calls it 'мягкая форма правды'."""
        h7 = [h for h in H.HOLES if h.key.startswith("H7")][0]
        self.assertIn("T(S) ≥ c·(|S| − 3(p−1) − C)", h7.missing_interaction)
        self.assertIn("мягкая форма", h7.payoff)

    @gap("GAP-P-02",
         module="phenomenon.py P3",
         title="P3 is satisfied by every finite system whatsoever, so no measurement can refute it",
         expected="P3 is listed among the PRINCIPLES — 'почему слабые ограничения вместе сильны' — and "
                  "holes.py H7 gives it a 'testable_now' experiment ('измерить min T(S) по S с |S| = "
                  "3(p−1)+t при p ≤ 19: растёт ли линейно по t?').  A principle with an experiment "
                  "attached must be capable of coming out false on some system.",
         actual="c, α and C are free.  Taking α = |V|, C = 0 and any c makes the hypothesis |S| > α + C "
                "empty, so P3 is TRUE for every finite system — including a system with no constraints "
                "at all, and including the blocks system and the complete hypergraph.  A search over "
                "hundreds of random systems finds no falsifier, and none can exist.  Nothing in the "
                "module fixes c, α or C, and nothing says the constants must be absolute (uniform in "
                "the system size), which is the only reading with content.",
         consequence="The experiment H7 proposes measures a DIFFERENT statement (linear growth of "
                     "min T(S) in t at fixed p) from the one P3 states, and whatever it returns, P3 "
                     "survives.  Q5 of deep_research_brief_8 asks external researchers which counting "
                     "theorem 'comes closest' to P3 — with unbound constants there is no target to come "
                     "close to, and any answer can be declared a match.")
    def test_p3_is_falsifiable(self):
        p3 = [x for x in P.PRINCIPLES if x.key.startswith("P3")][0]
        text = p3.statement + p3.consequence + principle_prose("P3")

        # READING B (the only one with content): c and C absolute — uniform in the size of the system —
        # and α the size of the algebraic construction.  Under it the module's own bestiary entry
        # falsifies P3: for cap sets the truth exceeds the construction {0,1}ⁿ by 0,0,1,4,13,48, so a
        # maximum cap set has T(S) = 0 while |S| − α − C > 0 as soon as the gain passes C.
        gains = [t - c for t, c in zip(CAPSET_TRUTH, CAPSET_CONSTRUCTION)]
        self.assertEqual(gains, [0, 0, 1, 4, 13, 48])
        bound_falsifiers = [C for C in range(max(gains)) if any(g > C for g in gains)]
        self.assertEqual(len(bound_falsifiers), 48, "every absolute C < 48 is refuted already at n ≤ 6")

        # READING A (what the text says): c, α, C are free per system.  A falsifier must defeat EVERY
        # admissible choice, and α = |V| empties the hypothesis.
        empty = System("no constraints", list(range(6)), [], cap=2)
        candidates = [empty,
                      System("K_6^(3)", list(range(6)), combinations(range(6), 3), cap=2),
                      blocks_system(2)]
        free_falsifiers = []
        for sysm in candidates:
            edges = [set(sysm.index[q] for q in c) for c in sysm.weak()]
            if not any(p3_holds(sysm.n, edges, c, alpha, C)
                       for c in (Fraction(1), Fraction(1, 2))
                       for alpha in range(sysm.n + 1)
                       for C in range(sysm.n + 1 - alpha)):
                free_falsifiers.append(sysm.name)
        self.assertEqual(free_falsifiers, [], "no system makes P3 false when its constants are free")

        # Which reading is the module's?  Nothing in P3 binds c, α or C, so it is A — and A has no
        # falsifier.  Bind them and the test passes: that is what closing this gap means.
        binds_its_constants = any(tok in text for tok in ("абсолютн", "не зависящ", "равномерн", "∀"))
        falsifiers = bound_falsifiers if binds_its_constants else free_falsifiers
        self.assertTrue(falsifiers,
                        "P3 as written admits α = |V|, C = 0: no finite system can refute it")

    @gap("GAP-P-03",
         module="phenomenon.py P3 (consequence field) + holes.py H7",
         title="the 'soft form usually available earlier than the exact one' is logically equivalent to "
               "the exact one, so H7 is not an easier target",
         expected="P3.consequence says 'мягкая форма; из неё α + O(1) удалением; обычно доступна раньше "
                  "точной', and H7.payoff repeats it ('мягкая форма правды; из неё α ≤ 3(p−1)+O(1) "
                  "удалением').  'Softer' must mean strictly weaker: there has to be a system where the "
                  "supersaturation statement holds and the exact bound fails.",
         actual="For every c ∈ (0,1] the quantified P3 is equivalent to the exact bound with the same α, "
                "C.  (⇐) T(S) = 0 on a lawful S gives |S| ≤ α + C.  (⇒) if max lawful ≤ α+C then picking "
                "one point of each triple inside S and deleting them leaves a lawful set, so "
                "T(S) ≥ |S| − α − C, i.e. P3 with c = 1.  Exhaustive search over 400 random hypergraphs "
                "produces no separating instance.  pair_bound_notes B.12 states the same thing about the "
                "project's own system: 'H4 is not an intermediate hypothesis but the target itself in "
                "\"supersaturation\" form'.",
         consequence="The one route the specification labels 'обычно доступна раньше точной' is the "
                     "target T1 itself.  H7's payoff is mis-stated, and Q5 of deep_research_brief_8 "
                     "sends researchers after a soft version of a problem that has no soft version — "
                     "only the genuinely weaker H4(ε) form of B.12 ('T(S) ≥ c|S| whenever |S| ≥ "
                     "(3+ε)(p−1)', which yields T2, not T1) is strictly easier, and neither P3 nor H7 "
                     "states it.")
    def test_supersaturation_is_strictly_weaker_than_the_exact_bound(self):
        import random
        rnd = random.Random(3)
        separations = []
        for _ in range(400):
            n = rnd.randint(5, 8)
            allE = list(combinations(range(n), 3))
            edges = [set(e) for e in rnd.sample(allE, rnd.randint(0, min(12, len(allE))))]
            A = max_edge_free(n, edges)
            for alpha in range(n + 1):
                for C in range(n + 1 - alpha):
                    if alpha + C >= A:
                        continue
                    # supersaturation holds at (α, C) but the exact bound max <= α+C fails?
                    if p3_holds(n, edges, Fraction(1), alpha, C):
                        separations.append((n, alpha, C, A))
        self.assertEqual(separations, [], "the two statements coincide on every instance searched")
        # The gap closes if the specification states the form that IS strictly weaker — B.12's
        # H4(ε): "T(S) ≥ c·|S| whenever |S| ≥ (3+ε)(p−1)", which yields T2 and not T1.  Neither P3 nor
        # H7 mentions it, so the "soft form" they offer is the target itself.
        p3 = [x for x in P.PRINCIPLES if x.key.startswith("P3")][0]
        h7 = [h for h in H.HOLES if h.key.startswith("H7")][0]
        soft = p3.statement + p3.consequence + principle_prose("P3") + h7.missing_interaction + h7.payoff
        states_the_epsilon_form = any(tok in soft for tok in ("ε", "c·|S|", "c|S|"))
        self.assertTrue(separations or states_the_epsilon_form,
                        "the 'мягкая форма' of P3/H7 is logically equivalent to the exact bound, and the "
                        "one genuinely weaker form (B.12's H4(ε)) is stated in neither")


# ══════════════════════════════════════════════════════════════════════════════════════════════
# 5. P4 / P5 — statements or descriptions?
# ══════════════════════════════════════════════════════════════════════════════════════════════

RELATIONAL = ("⇔", "⇒", "≤", "≥", "≈", "=", "<", ">", "≠", "∈", "⊆")


class PrinciplesP4P5(unittest.TestCase):

    def test_p1_p2_p3_carry_a_relation_and_p4_p5_do_not(self):
        by_key = {x.key.split()[0]: x for x in P.PRINCIPLES}
        for k in ("P1", "P2", "P3"):
            self.assertTrue(any(t in by_key[k].statement for t in RELATIONAL), k)
        for k in ("P4", "P5"):
            self.assertFalse(any(t in by_key[k].statement for t in RELATIONAL),
                             f"{k}.statement = {by_key[k].statement!r} contains no relation")

    def test_the_executable_p5_drops_the_only_falsifiable_clause_of_its_own_prose(self):
        """§1's P5 ends with a claim that can be false of a system: 'Локальные сертификаты (LP на
        прямых) — нет.'  The Principle object that PRINCIPLES exports — the thing __main__ prints and
        the thing a reader of the module gets — keeps only the list of method names and drops it."""
        p5 = [x for x in P.PRINCIPLES if x.key.startswith("P5")][0]
        prose = principle_prose("P5")
        self.assertIn("Локальные сертификаты", prose)
        self.assertIn("— нет.", prose)
        self.assertNotIn("Локальные", p5.statement)
        self.assertNotIn(" не ", p5.statement)       # no negation left, so nothing is excluded
        self.assertNotIn(" нет", p5.statement)
        self.assertFalse(any(t in p5.statement for t in RELATIONAL))

    def test_only_p2_s_lp_clause_separates_the_decomposable_blocks_system_from_our_frame(self):
        """P1 (correctly, since every constraint is weak there), P2's τ*-clause and its rank-1 clause,
        P3 (always), P4 and P5 (no predicate) all hold for m disjoint blocks of five.  The single
        clause of the whole principle set that rejects it is P2's middle one, 'LP(все) ≈ LP(сильные)' —
        which is signature S2, the one vote verdict()'s majority can lose (GAP-P-05)."""
        sysm = blocks_system(3)
        edges = [set(sysm.index[q] for q in c) for c in sysm.weak()]
        # P1 holds verbatim here:
        self.assertEqual(max_edge_free(sysm.n, edges), sysm.n - tau_exact(sysm.n, edges))
        self.assertEqual(max_edge_free(sysm.n, edges), 2 * 3)
        # P2, clause 1:
        self.assertLessEqual(Fraction(1, 3) * sysm.n, Fraction(sysm.n, 3))
        # P2, clause 3: rank-1 LP does not reach the integer optimum
        self.assertGreater(blocks_lp(3), 2 * 3)
        # P3: constants exist
        self.assertTrue(p3_holds(sysm.n, edges, Fraction(1), sysm.n, 0))
        # P4, P5: no relation to evaluate, so nothing to violate
        by_key = {x.key.split()[0]: x for x in P.PRINCIPLES}
        for k in ("P4", "P5"):
            self.assertFalse(any(t in by_key[k].statement for t in RELATIONAL), k)
        # P2, clause 2 — the ONLY clause of the five principles this system fails: with no strong
        # constraint, LP(strong) is the unconstrained |V| = 5m and LP(all)/LP(strong) = 2/3, not ≈ 1.
        self.assertEqual(sysm.rich(), [])
        self.assertEqual(blocks_lp(3) / Fraction(5 * 3), Fraction(2, 3))
        self.assertIn("LP(все прямые) ≈ LP(сильные)", by_key["P2"].statement)

    @gap("GAP-P-08",
         module="phenomenon.py P4  vs  holes.py H3, H4",
         title="P4 asserts as an established principle exactly the two things holes.py records as "
               "missing: the structure of NEAR-extremals (H3) and the O(1) cost of mixing (H4 = the "
               "project's open target)",
         expected="PRINCIPLES answers 'почему слабые ограничения вместе сильны' — it is the part of "
                  "the specification a reader may rely on, and deep_research_brief_8 §2 asks external "
                  "researchers to match our system against others on it.  Where the module states "
                  "something it has only measured, it says so: §0 writes 'правда (по всем точным "
                  "данным)', P2 writes '(проверено: IP(1) = LP(1) − O(1) при p ≤ 59)'.  A principle "
                  "whose content is an open conjecture must carry the same mark, or the specification "
                  "asserts its own goal as its own explanation.",
         actual="P4.statement = 'почти экстремали структурированы алгебраически; смешивание двух "
                "структур даёт O(1)', and its §1 prose repeats it flatly.  Both halves are open. "
                "holes.py H3 is 'stability of one hyperbola', and its where_it_breaks reads: 'есть "
                "точная классификация максимумов (9^s), но не почти‑максимумов' — i.e. exactly P4's "
                "first clause is what we do NOT have.  holes.py H4 is the exchange lemma '|S₂| ≤ "
                "(3(p−1) − |S₁|) + O(1)' with where_it_breaks 'нет механизма…' — i.e. P4's second "
                "clause is what we do NOT have; and holes.py's own header names it as the GOAL: 'цель "
                "— α(P₋₁) ≤ 3(p−1) + O(1); доказано 11/3 → 115/32'.  pair_bound_notes §6 lists it as "
                "'(T1) … open; no route', REPORT §12 as 'T1 — нет'.  Nothing in P4 marks any of this.",
         consequence="The module's fourth principle is the theorem the project is trying to prove, "
                     "written in the mood of an explanation, and S4 turns it into a signature 'vote' "
                     "carried by four exact optima (p ≤ 19) that are themselves the maximum over the "
                     "second hyperbola (GAP-P-07).  A researcher answering Q2 of the brief is asked to "
                     "import a stability/exchange mechanism in order to establish a property that "
                     "phenomenon.py already lists as one of the five reasons the phenomenon happens; "
                     "and any analogue can be 'matched' on P4 by assumption.  Of the five principles, "
                     "P1 is false as written, P3 is unfalsifiable, P5 keeps no falsifiable clause "
                     "(see the tests above) — P4 is the fourth of the five, and it is a conjecture.")
    def test_p4_marks_the_status_of_a_claim_its_own_holes_record_as_missing(self):
        p4 = [x for x in P.PRINCIPLES if x.key.startswith("P4")][0]
        h3 = [h for h in H.HOLES if h.key.startswith("H3")][0]
        h4 = [h for h in H.HOLES if h.key.startswith("H4")][0]
        # P4's two clauses:
        self.assertIn("почти экстремали структурированы алгебраически", p4.statement)
        self.assertIn("смешивание двух структур даёт O(1)", p4.statement)
        # and the same two objects, in holes.py, as things that do not exist:
        self.assertIn("теорема устойчивости", h3.missing_interaction)
        self.assertIn("но не почти", h3.where_it_breaks)          # "…максимумов, но не почти‑максимумов"
        self.assertIn("лемма обмена", h4.missing_interaction)
        self.assertIn("+ O(1)", h4.missing_interaction)
        self.assertIn("нет механизма", h4.where_it_breaks)
        self.assertIn("3(p−1) + O(1)", H.__doc__)                 # holes.py's header: this is the GOAL
        self.assertIn("доказано 11/3 → 115/32", H.__doc__)        # this is what is proved
        # The module does mark status where it has one:
        self.assertIn("точным данным", section_0_definition() + P.__doc__[:P.__doc__.index("1. ПРИНЦИПЫ")])
        self.assertIn("проверено", principle_prose("P2"))
        # P4 carries no such mark, in either the object or the prose:
        p4_text = p4.statement + " " + p4.consequence + " " + principle_prose("P4")
        self.assertTrue(any(m in p4_text for m in STATUS_MARKERS),
                        f"P4 states the project's open target as a principle: {p4_text!r}")


# ══════════════════════════════════════════════════════════════════════════════════════════════
# 6. S1-S6 and Signature.verdict()
# ══════════════════════════════════════════════════════════════════════════════════════════════

def conditions(sig):
    """The four booleans verdict() actually votes on (S1, S2, S3, S4)."""
    return (sig.n_weak >= sig.n_ground,
            sig.lp_all_over_lp_strong > 0.97,
            sig.max_codegree <= 8,
            max(sig.gain_over_construction) - min(sig.gain_over_construction) <= 3)


class Signatures(unittest.TestCase):

    def test_verdict_is_a_plain_majority_of_four_votes(self):
        self.assertEqual(sum(conditions(P.OUR_SIGNATURE)), 4)
        self.assertIn("ЯВЛЕНИЕ", P.OUR_SIGNATURE.verdict())
        # any 3 of the 4 suffice, including the three that are not S2
        s = P.Signature(n_weak=10, n_ground=10, mean_degree=3.0, max_codegree=1,
                        lp_all_over_lp_strong=0.0, gain_over_construction=(1, 1))
        self.assertEqual(conditions(s), (True, False, True, True))
        self.assertIn("ЯВЛЕНИЕ", s.verdict())

    def test_s3_codegree_over_weak_constraints_is_1_by_geometry(self):
        """S3's field is 'макс. число слабых ограничений через пару точек'.  Weak constraints are
        3-point LINES; two distinct points of a plane lie on exactly one line; so the value is <= 1 for
        our system, for [N]², for arcs — for every point-line system in the bestiary.  The condition
        `max_codegree <= 8` is therefore satisfied before anything is measured."""
        for sysm in (our_system(11)[0], our_system(19)[0], grid_system(9), capset(3)):
            codeg = {}
            for c in sysm.weak():
                for pr in combinations(sorted(c, key=lambda q: sysm.index[q]), 2):
                    codeg[pr] = codeg.get(pr, 0) + 1
            self.assertLessEqual(max(codeg.values(), default=0), 1, sysm.name)

    def test_our_signature_max_codegree_6_is_the_codegree_of_the_strong_lines(self):
        """OUR_SIGNATURE.max_codegree = 6 = 8 − 2 is the number of collinear TRIPLES a pair on an
        8-point ±1 line lies in — i.e. it was read off the STRONG constraints, not the weak ones the
        field's comment names."""
        self.assertEqual(P.OUR_SIGNATURE.max_codegree, 8 - 2)
        for p in (11, 19):
            sysm, _ = our_system(p)
            self.assertIn(8, {len(c) for c in sysm.constraints})
            codeg = {}
            for t in sysm.all_collinear_triples():
                for pr in combinations(sorted(t, key=lambda q: sysm.index[q]), 2):
                    codeg[pr] = codeg.get(pr, 0) + 1
            self.assertEqual(max(codeg.values()), 6, f"p={p}")

    def test_s3_flips_with_the_reading_and_rejects_the_module_s_purest_example(self):
        """Under the 'all collinear triples' reading, max_codegree in [N]² is N−2, so S3 fails for
        no-three-in-line — which the bestiary calls 'то же явление в чистом виде'."""
        N = 11
        g = grid_system(N)
        codeg = {}
        for t in g.all_collinear_triples():
            for pr in combinations(sorted(t, key=lambda q: g.index[q]), 2):
                codeg[pr] = codeg.get(pr, 0) + 1
        self.assertEqual(max(codeg.values()), N - 2)
        self.assertGreater(N - 2, 8, "S3's threshold 8 is exceeded by the parent problem")

    def test_two_of_the_six_signatures_and_one_declared_field_are_never_checked(self):
        """verdict() votes on S1-S4 only.  S5 ('мягкие формы численно верны … спектральные оценки
        численно работают') and S6 ('локальные сертификаты выходят на плато') have no field and no
        condition, and the declared field mean_degree — the carrier of S1's 'степени ~ log |V|' — is
        never read."""
        import inspect
        src = inspect.getsource(P.Signature.verdict)
        for used in ("n_weak", "n_ground", "lp_all_over_lp_strong", "max_codegree",
                     "gain_over_construction"):
            self.assertIn(used, src)
        self.assertNotIn("mean_degree", src, "declared, documented, never consulted")
        self.assertEqual(src.count("# S"), 4, "exactly four of the six signatures are encoded")
        self.assertIn("S5.", P.__doc__)
        self.assertIn("S6.", P.__doc__)

    def test_lp_ratio_0985_matches_neither_measurement_and_s2_clears_by_0002(self):
        """OUR_SIGNATURE.lp_all_over_lp_strong = 0.985 appears nowhere in the project's data.  The two
        measured values are LP(∞)/LP(1) = 60.15/62 at p=17 and 63.6/64 at p=19 (B.11 point 3 against
        B.7), i.e. 0.9702 and 0.9938 — and the p=17 value clears S2's threshold 0.97 by 0.00017, so
        S2's vote on our own system is decided in the fourth decimal place of a number that is not the
        one the module entered."""
        self.assertEqual(P.OUR_SIGNATURE.lp_all_over_lp_strong, 0.985)
        measured = {p: LP_ALL[p] / LP_STRONG[p] for p in (17, 19)}
        self.assertAlmostEqual(measured[17], 0.970161, places=5)
        self.assertAlmostEqual(measured[19], 0.993750, places=5)
        for p, r in measured.items():
            self.assertNotAlmostEqual(r, 0.985, places=2, msg=f"p={p}")
        self.assertLess(measured[17] - 0.97, 0.001, "S2 is decided at the fourth decimal place")
        self.assertTrue(measured[17] > 0.97)

    def test_no_signature_field_records_the_size_or_density_of_the_extremal_sets(self):
        names = [f.name for f in P.Signature.__dataclass_fields__.values()]
        self.assertEqual(names, ["n_weak", "n_ground", "mean_degree", "max_codegree",
                                 "lp_all_over_lp_strong", "gain_over_construction"])
        for bad in ("density", "extremal", "alpha", "optimum", "max_set"):
            self.assertFalse(any(bad in nm for nm in names), bad)

    def test_honest_capset_signature_and_the_bestiary_s_own_claim(self):
        """Cap sets: every line has 3 points, so there is no strong constraint; LP(all) = 2|V|/3 (primal
        x ≡ 2/3, dual y ≡ 2/(3^n−1) on every line, both of value 2·3^n/3) while the truth is 2, 4, 9 for
        n = 1,2,3 — an LP/IP ratio of 1.0, 1.5, 2.0 and growing.  The bestiary says LP is blind there."""
        for n, truth in ((1, 2), (2, 4), (3, 9)):
            s = capset(n)
            V = 3 ** n
            self.assertEqual(s.n, V)
            self.assertEqual(len(s.constraints), V * (V - 1) // 6)
            self.assertEqual(s.rich(), [], "no cap-set line has >= 5 points")
            y = Fraction(2, V - 1)                                   # dual: weight y on every line
            self.assertEqual(Fraction(V - 1, 2) * y, 1, "dual feasible: each point is in (V−1)/2 lines")
            self.assertEqual(Fraction(V * (V - 1), 6) * 2 * y, Fraction(2 * V, 3), "LP(all) = 2|V|/3")
            edges = [set(c) for c in s.constraints]
            if n <= 2:
                self.assertEqual(max_edge_free(s.n, edges), truth)
            self.assertGreaterEqual(Fraction(2 * V, 3) / truth, 1, "LP/IP = 1.0, 1.5, 2.0 and growing")
        entry = [b for b in P.BESTIARY if "cap sets" in b.name][0]
        self.assertIn("нет плотных экстремалей", entry.lesson)
        self.assertIn("LP слепо", P.__doc__)
        self.assertIn("нет плотных структурированных экстремалей", P.__doc__)

    @gap("GAP-P-05",
         module="phenomenon.py Signature.verdict() (S2, S3)",
         title="false positive: a system where LP is not blind at all is still declared ЯВЛЕНИЕ, "
               "because S3 is a free vote in a 3-of-4 majority",
         expected="§0 defines the phenomenon by LP's blindness to the weak constraints, and S2 is the "
                  "signature that encodes it ('LP со ВСЕМИ ограничениями ≈ LP только с сильными; x ≡ "
                  "2/3 почти допустимо').  A system whose LP with all constraints is two thirds of its "
                  "LP with the strong ones alone — i.e. where the weak constraints cut the relaxation "
                  "by a third and LP sees them perfectly — must not be certified as exhibiting the "
                  "phenomenon.",
         actual="BLOCKS(m) plus one 5-point strong line has n_weak = 10m >= n_ground = 5m+5 (S1 true), "
                "max_codegree = 3 <= 8 (S3 true — and no point-line system can fail S3: two points lie "
                "on at most one 3-point line, so S3 is satisfied by geometry, never by measurement), "
                "gain over the construction identically 0 (S4 true), and "
                "lp_all_over_lp_strong = (10m/3+2)/(5m+2) → 2/3 (S2 FALSE).  verdict() sums the votes "
                "and returns '3/4 признаков явления: ЯВЛЕНИЕ'.  Because S3 costs nothing, the majority "
                "rule needs only two of the three informative conditions, and the defining one may be "
                "the missing vote.",
         consequence="verdict() cannot be used to screen candidate systems for deep_research_brief_8: "
                     "any point-line packing system with enough three-point lines and a stable gain "
                     "passes with the relaxation wide open.  The phrase 'ЯВЛЕНИЕ' in the module's own "
                     "__main__ output therefore certifies nothing about our system beyond S1 and the "
                     "hand-entered numbers of OUR_SIGNATURE.")
    def test_verdict_requires_s2_the_defining_condition(self):
        m = 100
        n_ground = 5 * m + 5
        n_weak = 10 * m
        lp_all = blocks_lp(m) + 2
        lp_strong = Fraction(5 * m) + 2
        sig = P.Signature(n_weak=n_weak, n_ground=n_ground,
                          mean_degree=3 * n_weak / n_ground, max_codegree=3,
                          lp_all_over_lp_strong=float(lp_all / lp_strong),
                          gain_over_construction=(0, 0, 0, 0))
        self.assertEqual(conditions(sig), (True, False, True, True))
        self.assertLess(sig.lp_all_over_lp_strong, 0.7, "LP is not blind: it sees the weak constraints")
        self.assertIn("не характерно", sig.verdict())

    @gap("GAP-P-06",
         module="phenomenon.py Signature (S2, S4) + BESTIARY['cap sets / 3-АП']",
         title="false negative: cap sets — the module's own paradigm of LP blindness — score "
               "'не характерно', and the difference the bestiary insists on is in no field",
         expected="The bestiary lists cap sets in F₃ⁿ as a system with the same weak constraints "
                  "('арифметические прогрессии длины 3') where 'LP слепо', and §2 names exactly ONE "
                  "difference from us: 'там нет плотных структурированных экстремалей (у нас плотность "
                  "3/4!)'.  So the signature must (i) recognise cap sets as exhibiting the phenomenon, "
                  "and (ii) express the density difference, or it cannot support the claim that our "
                  "system is a different case.",
         actual="Every cap-set line has exactly 3 points, so there is no strong constraint: "
                "lp_all_over_lp_strong is 2/3 under the reading 'LP with the strong constraints only' "
                "(the unconstrained optimum |V|), and is undefined under any other — S2 cannot be "
                "scored precisely in the PUREST instance of the phenomenon, the one where the weak "
                "constraints do all the work.  S4 also fails, since the additive gain between the truth "
                "(2, 4, 9, 20, 45, 112 for n ≤ 6) and the algebraic construction {0,1}ⁿ (2ⁿ) is "
                "0,0,1,4,13,48 — a spread of 48.  So verdict() returns '2/4 признаков явления: не "
                "характерно' for the very system whose LP/IP ratio (1.0, 1.5, 2.0 at n = 1,2,3, growing "
                "like (3/2.756)ⁿ) is the largest in the bestiary.  And no field of Signature is a "
                "function of |S_max|/|V|, so the density difference is not recorded anywhere.",
         consequence="S2 measures LP(all)/LP(strong) while §0 defines the phenomenon by LP(all)/IP; the "
                     "two diverge maximally exactly where all constraints are weak.  A deep-research "
                     "answer that matches our system to cap sets and transports Ellenberg-Gijswijt "
                     "cannot be rejected by the specification: the property the module gives as the "
                     "reason they are different is machine-uncheckable.")
    def test_capset_signature_is_recognised_and_density_is_expressible(self):
        n = 4
        V = 3 ** n
        gains = tuple(t - c for t, c in zip(CAPSET_TRUTH, CAPSET_CONSTRUCTION))
        self.assertEqual(gains, (0, 0, 1, 4, 13, 48), "the gain grows for any base below 2.756")
        sig = P.Signature(n_weak=V * (V - 1) // 6, n_ground=V,
                          mean_degree=3 * (V * (V - 1) // 6) / V, max_codegree=1,
                          lp_all_over_lp_strong=2 / 3,
                          gain_over_construction=gains)
        self.assertEqual(conditions(sig), (True, False, True, False))
        self.assertIn("ЯВЛЕНИЕ", sig.verdict())

    @gap("GAP-P-07",
         module="phenomenon.py OUR_SIGNATURE.gain_over_construction",
         title="S4 holds for our own system only because the entered sequence is the maximum over k, "
               "while OUR_FRAME fixes the pair xy ≡ ±1",
         expected="OUR_FRAME.ground_set is 'лифты двух гипербол xy ≡ ±1', i.e. k = −1, and the field's "
                  "comment reads 'p=11,13,17,19: max − 3(p−1)'.  S4 — the only signature condition "
                  "encoding P4, the rigidity of the extremals — should therefore be evaluated on the "
                  "measured gains of THAT system.",
         actual="The entered sequence (5,5,6,5) is pair_bound_notes B.6(c)'s '+5,+5,+6,+5 for p=11…19', "
                "which is the maximum over the second hyperbola k, not the k = −1 values.  The k = −1 "
                "data are α = 32 at p=11 (§7 'p=11: 32–35' exact over all k; §4 lists k=2→33, k=3→35, "
                "k=−1→32), 54 at p=17 and 59 at p=19 (§2), i.e. gains 2, 6, 5 with a spread of 4 > 3; "
                "the entered first term 5 is exactly the k = 3 value 35 − 30.  §7's own summary — 'for "
                "EVERY second hyperbola the gain over 3(p−1) is between +2 and +6' — gives the same "
                "spread of 4.  With the frame's own numbers S4 is FALSE and OUR_SIGNATURE scores 3/4, "
                "the same as the decomposable blocks system of GAP-P-05.",
         consequence="S4 is the module's only quantitative claim about extremals, and the verdict "
                     "'4/4 … ЯВЛЕНИЕ' printed by phenomenon.py's __main__ depends on it.  With the "
                     "project's own exact data our system scores no better than a system that splits "
                     "into blocks of five, so the module's own numbers do not certify the phenomenon "
                     "in the frame the module was written for.")
    def test_our_signature_gains_are_the_frame_s_own_measurements(self):
        declared = tuple(P.OUR_SIGNATURE.gain_over_construction)
        self.assertEqual(declared, B6C_MAX_GAINS, "= B.6(c)'s '+5,+5,+6,+5 for p=11…19'")
        self.assertEqual(declared[0], ALPHA_K3_11 - 3 * (11 - 1), "the p=11 entry is the k=3 value")
        # The frame is k = −1.  Its exactly known optima (§2 for p=17,19; §4/§7 for p=11):
        honest = tuple(ALPHA_KM1[p] - 3 * (p - 1) for p in (11, 17, 19))
        self.assertEqual(honest, (2, 6, 5))
        self.assertGreater(max(honest) - min(honest), 3, "spread 4: S4's own test fails on them")
        # The same conclusion follows from §7 without identifying any k, so it does not depend on the
        # one datum the notes mark with a question mark (§4's "true α: 33, 35, 32?" for p=11):
        # the exactly solved instances span gains +1 (p=17, α=49) … +6 (p=17, α=54) over 3(p−1) —
        # a spread of 5, larger even than §7's own prose ("between +2 and +6") claims.
        exact_gains = [a - 3 * (p - 1) for p, lohi in ALL_K_EXACT.items() for a in lohi]
        self.assertEqual((min(exact_gains), max(exact_gains)), (1, 6))
        self.assertGreater(max(exact_gains) - min(exact_gains), 3)
        # What must hold if the entered numbers certify the phenomenon in the frame they were entered
        # for: substituting the frame's own measurements must not cost OUR_SIGNATURE a vote.
        self.assertIn("4/4", P.OUR_SIGNATURE.verdict())
        with_frame_data = replace(P.OUR_SIGNATURE, gain_over_construction=honest)
        self.assertIn("4/4", with_frame_data.verdict(),
                      f"with the k = −1 gains {honest} the module's own verdict drops to "
                      f"{with_frame_data.verdict()!r}")


# ══════════════════════════════════════════════════════════════════════════════════════════════
# 7. Book-keeping: which principle has a hole, which hole has a principle
# ══════════════════════════════════════════════════════════════════════════════════════════════

class PrincipleHoleCorrespondence(unittest.TestCase):

    def test_p1_the_only_falsifiable_principle_has_no_hole(self):
        """P1 is the identity the project would actually use (packing ↔ transversal); it is false as
        written (PrincipleP1), and no hole in holes.py records the transversal reformulation, its
        failure, or the distribution criterion ('малые степени/костепени, расширение') P1 makes the
        answer to 'when are weak constraints strong together'."""
        self.assertEqual([x.key.split()[0] for x in P.PRINCIPLES], ["P1", "P2", "P3", "P4", "P5"])
        self.assertEqual([h.key.split()[0] for h in H.HOLES],
                         ["H1", "H2", "H3", "H4", "H5", "H6", "H7", "H8"])
        text = " ".join(h.missing_interaction + h.where_it_breaks + h.testable_now for h in H.HOLES)
        self.assertNotIn("трансверсал", text)
        self.assertNotIn("τ(H", text)
        p1 = [x for x in P.PRINCIPLES if x.key.startswith("P1")][0]
        self.assertIn("расширение", p1.consequence)
        for tok in ("расшир", "костепен", "квазислуч", "псевдослуч"):
            self.assertNotIn(tok, text + " ".join(h.payoff for h in H.HOLES))


if __name__ == "__main__":
    unittest.main(verbosity=2)
