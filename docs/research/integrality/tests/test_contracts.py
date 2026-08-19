"""test_contracts.py — Frame/Strength/Signature/AnalogSystem/Principle/Hole as DATA CONTRACTS: what the declared types cannot express."""
import os, re, sys, unittest, itertools, collections, dataclasses
from math import gcd

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)                       # tests/gaps.py
sys.path.insert(0, os.path.dirname(_HERE))      # phenomenon.py, holes.py
from gaps import gap
import phenomenon as P
import holes as H

_INTEGRALITY = os.path.dirname(_HERE)                       # …/docs/research/integrality
_RESEARCH = os.path.dirname(_INTEGRALITY)                   # …/docs/research
_NOTES = os.path.join(_RESEARCH, "pair_bound_notes.md")
_REPORT = os.path.join(os.path.dirname(_RESEARCH), "REPORT.md")
_BRIEF = os.path.join(_INTEGRALITY, "deep_research_brief_8_integrality.md")


def read(path):
    """The project's own text, read live: every quote below is checked against the file."""
    assert os.path.exists(path), path
    with open(path, encoding="utf-8") as fh:
        return fh.read()


# ══════════════════════════════════════════════════════════════════════════════════════
# Ground truth built from OUR_FRAME's own description, so that every claim below is
# measured on the project's real candidate set rather than on the module's prose.
# ══════════════════════════════════════════════════════════════════════════════════════

def our_candidates(p):
    """The 8(p−1) lifts of xy ≡ ±1 (mod p) into the 2p×2p box — OUR_FRAME.ground_set."""
    return [(x, y)
            for x in range(1, 2 * p) if x % p
            for y in range(1, 2 * p) if y % p and (x * y) % p in (1, p - 1)]


def rich_lines(V):
    """Every line of the plane carrying ≥ 3 candidates, as {line-key: frozenset(points)}."""
    acc = collections.defaultdict(set)
    for a, b in itertools.combinations(V, 2):
        dx, dy = b[0] - a[0], b[1] - a[1]
        g = gcd(abs(dx), abs(dy))
        dx, dy = dx // g, dy // g
        if dx < 0 or (dx == 0 and dy < 0):
            dx, dy = -dx, -dy
        acc[(dx, dy, dy * a[0] - dx * a[1])].update((a, b))
    return {k: frozenset(s) for k, s in acc.items() if len(s) >= 3}


_FRAME_CACHE = {}


def our_frame_instance(p):
    if p not in _FRAME_CACHE:
        V = our_candidates(p)
        _FRAME_CACHE[p] = (V, rich_lines(V))
    return _FRAME_CACHE[p]


def weak_codegrees(p):
    """#WEAK (=cap+1-point) constraints through each pair of candidates, at prime p."""
    _, lines = our_frame_instance(p)
    co = collections.Counter()
    for L in lines.values():
        if len(L) == P.OUR_FRAME.capacity + 1:
            for pair in itertools.combinations(sorted(L), 2):
                co[pair] += 1
    return co


def collinear_triple_codegrees(p):
    """#collinear triples through each pair — the hypergraph of ALL triples, weak or not."""
    _, lines = our_frame_instance(p)
    co = collections.Counter()
    for L in lines.values():
        for pair in itertools.combinations(sorted(L), 2):
            co[pair] += len(L) - 2
    return co


def blocks_system(t):
    """cap = 2, t disjoint 5-point blocks + every in-block triple as a WEAK constraint.

    The triples are implied by the blocks, so LP(all) = LP(strong) = IP = 2t: the
    integrality gap is exactly zero and the optimum is read off by inspection.
    """
    n = 5 * t
    strong = [frozenset(range(5 * j, 5 * j + 5)) for j in range(t)]
    weak = [frozenset(c) for b in strong for c in itertools.combinations(sorted(b), 3)]
    return n, strong, weak


def brute_force_optimum(n, constraints, cap):
    masks = [sum(1 << i for i in c) for c in constraints]
    best = 0
    for mask in range(1 << n):
        pc = bin(mask).count("1")
        if pc <= best:
            continue
        if all(bin(mask & m).count("1") <= cap for m in masks):
            best = pc
    return best


def pg2(q):
    """PG(2,q) for prime q: q²+q+1 points, q²+q+1 lines, every line full (q+1 points)."""
    pts = []
    for v in itertools.product(range(q), repeat=3):
        if v == (0, 0, 0):
            continue
        inv = next(pow(c, q - 2, q) for c in v if c)
        nv = tuple((x * inv) % q for x in v)
        if nv not in pts:
            pts.append(nv)
    lines = {frozenset(i for i, pt in enumerate(pts)
                       if sum(a * b for a, b in zip(L, pt)) % q == 0) for L in pts}
    return pts, sorted(lines, key=sorted)


# ── Building Signatures in a way that survives a repair of the specification ──────────
# Every diagnostic below is built with dataclasses.replace on OUR_SIGNATURE, so a field
# that a repaired Signature adds is inherited instead of raising TypeError; the fields
# that would carry the truth are then overwritten with the honest value for that system.
# Without this, closing a gap would leave its test failing (for a new, unrelated reason)
# and the xfail would go quietly stale — exactly what gaps.py exists to prevent.

_TRUTH_TOKENS = ("integer", "integral", "ip", "optimum", "opt", "truth", "exact", "gap")


def truth_fields(T=None):
    """Fields of Signature that could carry the integer optimum or the integrality gap."""
    return [f.name for f in dataclasses.fields(T or P.Signature)
            if any(tok in f.name.lower() for tok in _TRUTH_TOKENS)]


def signature(**measured):
    live = {f.name for f in dataclasses.fields(P.Signature)}
    unknown = set(measured) - live
    assert not unknown, unknown
    return dataclasses.replace(P.OUR_SIGNATURE, **measured)


def zero_gap_signature(t=3):
    """The block system of blocks_system(t), measured honestly: LP = IP = 2t."""
    n, _, weak = blocks_system(t)
    vals = {"n_weak": len(weak), "n_ground": n, "mean_degree": 3 * len(weak) / n,
            "max_codegree": 3, "lp_all_over_lp_strong": 1.0,
            "gain_over_construction": (0, 0, 0, 0)}
    for name in truth_fields():                 # a repaired Signature's own truth field
        vals[name] = 0 if "gap" in name else 2 * t
    return signature(**vals)


def arcs_signature(q=7):
    """Arcs in PG(2,q), measured from the bestiary's own facts: every line is full, so
    there are no weak constraints at all; the truth is q+1, attained by the conic."""
    pts, _ = pg2(q)
    vals = {"n_weak": 0, "n_ground": len(pts), "mean_degree": 0.0, "max_codegree": 0,
            "lp_all_over_lp_strong": 1.0, "gain_over_construction": (0, 0, 0, 0)}
    for name in truth_fields():
        vals[name] = 0 if "gap" in name else q + 1
    return signature(**vals)


def sensitive_fields(base):
    """Field names whose perturbation changes Signature.verdict()."""
    probes = {"n_weak": [0, 10 ** 9], "n_ground": [0, 10 ** 9], "mean_degree": [0.0, 1e9],
              "max_codegree": [0, 10 ** 9], "lp_all_over_lp_strong": [0.0, 1e9],
              "gain_over_construction": [(0,), (0, 10 ** 6)]}
    v0, live = base.verdict(), set()
    for name, values in probes.items():
        if any(dataclasses.replace(base, **{name: v}).verdict() != v0 for v in values):
            live.add(name)
    return live


# ══════════════════════════════════════════════════════════════════════════════════════
# A. Invariants that HOLD — the contract really on offer.
# ══════════════════════════════════════════════════════════════════════════════════════

class TestContractsThatHold(unittest.TestCase):

    def test_registries_are_well_formed(self):
        self.assertEqual([h.key.split()[0] for h in H.HOLES],
                         ["H%d" % i for i in range(1, 9)])
        self.assertEqual([pr.key.split()[0] for pr in P.PRINCIPLES],
                         ["P%d" % i for i in range(1, 6)])
        self.assertEqual(len(P.BESTIARY), 8)
        self.assertEqual(len({a.name for a in P.BESTIARY}), 8)

    def test_exactly_one_spec_type_is_mutable(self):
        """Every declared type is frozen except the one holding the module's conclusion."""
        frozen = {T.__name__: T.__dataclass_params__.frozen
                  for T in (P.Frame, P.Principle, P.AnalogSystem, P.Signature, H.Hole)}
        self.assertEqual({k for k, v in frozen.items() if not v}, {"Signature"})

    def test_ground_set_prose_matches_the_real_candidate_set(self):
        """OUR_FRAME.ground_set says '8(p−1) точек'; the constructed set has exactly that."""
        for p in (5, 7, 11, 13):
            V, _ = our_frame_instance(p)
            self.assertEqual(len(V), 8 * (p - 1))
        self.assertEqual(P.OUR_SIGNATURE.n_ground, 8 * (1999 - 1))

    def test_the_one_size_the_classifier_gets_right(self):
        self.assertEqual(P.OUR_FRAME.capacity, 2)
        self.assertIs(P.OUR_FRAME.strength(P.OUR_FRAME.capacity + 1), P.Strength.WEAK)


# ══════════════════════════════════════════════════════════════════════════════════════
# B. Frame / Strength — the classification and its blind zone.
# ══════════════════════════════════════════════════════════════════════════════════════

class TestFrameClassification(unittest.TestCase):

    def test_blind_zone_for_every_capacity_1_to_6(self):
        """The sizes called STRONG that violate STRONG's own predicate |ℓ| ≥ 2·cap+1,
        among the sizes a real constraint can have (|ℓ| ≥ cap+1)."""
        expected_zone = {1: [], 2: [4], 3: [5, 6], 4: [6, 7, 8],
                         5: [7, 8, 9, 10], 6: [8, 9, 10, 11, 12]}
        for cap, zone in expected_zone.items():
            f = P.Frame("V", "ℓ", cap)
            got = [s for s in range(cap + 1, 3 * cap + 3)
                   if f.strength(s) is P.Strength.STRONG and s < 2 * cap + 1]
            self.assertEqual(got, zone, "cap=%d" % cap)
        self.assertEqual(expected_zone[1], [], "the zone is empty only at cap = 1")

    def test_degenerate_and_negative_sizes_are_called_strong(self):
        f = P.OUR_FRAME
        for s in (-10 ** 6, -1, 0, 1, 2):        # 0,1,2 impose nothing at cap = 2
            self.assertIs(f.strength(s), P.Strength.STRONG, "size %d" % s)

    def test_frame_accepts_capacities_no_frame_can_have(self):
        """No constructor validation: at cap = 0 the classification inverts (|ℓ| = 1, the
        strongest constraint there is, comes back WEAK) and a negative capacity is taken."""
        self.assertIs(P.Frame("V", "ℓ", 0).strength(1), P.Strength.WEAK)
        self.assertIs(P.Frame("V", "ℓ", -2).strength(-1), P.Strength.WEAK)

    def test_strength_reads_capacity_and_nothing_else(self):
        """Three of Frame's four fields are never read; |V| exists only as prose."""
        a = P.Frame("lifts of two hyperbolae", "all lines with ≥3 candidates", 2)
        b = P.Frame("", "", 2, objective="")
        self.assertEqual([a.strength(s) for s in range(10)], [b.strength(s) for s in range(10)])
        numeric = [f.name for f in dataclasses.fields(P.Frame) if f.type in ("int", "float")]
        self.assertEqual(numeric, ["capacity"])

    def test_size_four_lines_dwarf_the_lines_that_certify_anything(self):
        """DATA on the real candidate set: the size-2·cap lines outnumber the lines with
        ≥ 2·cap+1 candidates by ≥ 8×, and x ≡ 1/2 satisfies all of them at exactly 4(p−1)
        — the trivial bound, i.e. they certify nothing (pair_bound_notes §10(d))."""
        counts = {}
        for p in (5, 7, 11, 13):
            V, lines = our_frame_instance(p)
            n4 = sum(1 for L in lines.values() if len(L) == 4)
            n_rich = sum(1 for L in lines.values() if len(L) >= 5)
            counts[p] = (n4, n_rich, len(lines))
            self.assertGreaterEqual(n4, 8 * n_rich, "p=%d" % p)
            small = [L for L in lines.values() if len(L) <= 4]
            self.assertTrue(all(len(L) * 0.5 <= P.OUR_FRAME.capacity for L in small))
            self.assertFalse(any(len(L) * 0.5 <= P.OUR_FRAME.capacity
                                 for L in lines.values() if len(L) >= 5))
            self.assertEqual(len(V) * 0.5, 4 * (p - 1))          # = the trivial bound
            self.assertIs(P.OUR_FRAME.strength(4), P.Strength.STRONG)
        self.assertEqual(counts, {5: (20, 2, 30), 7: (34, 4, 78),
                                  11: (106, 4, 182), 13: (144, 2, 202)})
        self.assertIn("with ≤ 4 candidates (x ≡ 1/2 is LP-feasible), so any strict LP bound "
                      "needs lines with ≥ 5 candidates", read(_NOTES))

    def test_section_0_calls_rows_and_columns_rich_and_they_carry_four_points(self):
        """§0 lists rows/columns as examples of '|ℓ| ≥ 5', OUR_FRAME.constraints says they
        have 4 points, and the data say 4.  The brief ships the §0 version outward."""
        self.assertIn("СИЛЬНЫЕ (rich): |ℓ| ≥ 5 при cap = 2", P.__doc__)
        self.assertIn("У нас — строки, столбцы, прямые наклона ±1 (до 8 точек)", P.__doc__)
        self.assertIn("строки/столбцы (4 точки)", P.OUR_FRAME.constraints)
        for p in (5, 7, 11, 13):
            V, _ = our_frame_instance(p)
            cols = collections.Counter(x for x, _ in V)
            rows = collections.Counter(y for _, y in V)
            self.assertEqual(set(cols.values()) | set(rows.values()), {4}, "p=%d" % p)
            self.assertEqual((len(cols), len(rows)), (2 * (p - 1), 2 * (p - 1)))
        self.assertIn("STRONG ones (lines with ≥ 5 candidates: rows, columns, slopes ±1)",
                      read(_BRIEF))

    @gap("GAP-C-01", module="phenomenon.py",
         title="Strength is a two-member Enum for a three-regime reality: no member for |ℓ| = 2·cap",
         expected="Strength's members carry their own predicates — WEAK: '|ℓ| = cap+1', STRONG: "
                  "'|ℓ| ≥ 2·cap+1'.  Frame.strength(size) must return a member whose documented "
                  "predicate the size satisfies, for every size a real constraint can have "
                  "(|ℓ| ≥ cap+1).",
         actual="for every cap ≥ 2 the sizes cap+2 … 2·cap come back as STRONG while violating "
                "STRONG's own predicate, and no third member exists to receive them: the orphan "
                "zone is [], [4], [5,6], [6,7,8], [7…10], [8…12] for cap = 1…6.  At cap = 2 the "
                "orphan size is exactly 4 — the rows and columns OUR_FRAME.constraints names "
                "first (measured: every row and column carries exactly 4 candidates), and 20/30, "
                "34/78, 106/182, 144/202 of all ≥3-point lines at p = 5,7,11,13, i.e. ≥ 8× as "
                "many as the lines with ≥ 5 candidates.",
         consequence="STRONG's docstring promises 'видно LP, даёт сертификаты-покрытия'.  On "
                     "size-2·cap lines the uniform x ≡ cap/(2cap) = 1/2 is feasible and attains "
                     "EXACTLY the trivial bound (measured here: |V|/2 = 4(p−1)), while it is "
                     "violated by every line with ≥ 5 candidates; pair_bound_notes §10(d) says the "
                     "same for the real system, verbatim: 'the 4(p−1) bound is not strict via "
                     "lines with ≤ 4 candidates (x ≡ 1/2 is LP-feasible), so any strict LP bound "
                     "needs lines with ≥ 5 candidates', and the only proved saving, 4(p−1) − 4·m₈, "
                     "comes from 8-point lines (x ≤ 1/4).  §0's own definition of WEAK — "
                     "'поодиночке каждое такое ограничение почти ничего не стоит' — is exactly "
                     "true of them (§B.19: the 4-point lines 'save nothing alone').  So the "
                     "module's central dichotomy files the largest family of OUR_FRAME under the "
                     "label whose promise is false for it; §0 then lists rows and columns as "
                     "examples of '|ℓ| ≥ 5', and deep_research_brief_8 §0 ships that sentence to "
                     "the external researchers.  Unrepairable inside strength(): the middle regime "
                     "has no member to return, so every downstream construct that inherits the "
                     "split (S1, S2, P2, AnalogSystem.weak_constraints) inherits the error.")
    def test_returned_member_satisfies_its_own_predicate(self):
        # A member this test does not know about — a third regime added by a repaired spec —
        # is NOT counted as an offender, and a classifier that refuses (raises) is not one
        # either: closing the gap must turn this test red rather than leave it xfail.
        predicate = {"WEAK": lambda s, cap: s == cap + 1,
                     "STRONG": lambda s, cap: s >= 2 * cap + 1}
        offenders = []
        for cap in range(1, 7):
            f = P.Frame("V", "ℓ", cap)
            for size in range(cap + 1, 3 * cap + 3):     # sizes a real constraint can have
                try:
                    got = f.strength(size)
                except Exception:
                    continue
                check = predicate.get(getattr(got, "name", None))
                if check is not None and not check(size, cap):
                    offenders.append((cap, size, got.name))
        self.assertEqual(offenders, [],
                         "no member exists for cap+2 ≤ |ℓ| ≤ 2·cap (the x ≡ 1/2 regime)")


# ══════════════════════════════════════════════════════════════════════════════════════
# C. Signature — the fields, the dead field, the crash, the mutable conclusion.
# ══════════════════════════════════════════════════════════════════════════════════════

class TestSignatureFields(unittest.TestCase):

    def test_mean_degree_is_declared_and_never_read(self):
        live = sensitive_fields(P.OUR_SIGNATURE)
        self.assertEqual(live, {"n_weak", "n_ground", "max_codegree",
                                "lp_all_over_lp_strong", "gain_over_construction"})
        self.assertNotIn("mean_degree", live)
        for v in (0.0, -1e9, 1e300):
            self.assertEqual(dataclasses.replace(P.OUR_SIGNATURE, mean_degree=v).verdict(),
                             P.OUR_SIGNATURE.verdict())

    def test_no_measurements_crashes_the_diagnostic(self):
        """Sequence[int] admits (); the honest 'nobody has measured this system' case raises."""
        s = dataclasses.replace(P.OUR_SIGNATURE, gain_over_construction=())
        with self.assertRaises(ValueError):
            s.verdict()

    def test_one_measurement_always_satisfies_S4(self):
        """A single data point has range 0, so 'прибавка не растёт' passes at any size."""
        s = dataclasses.replace(P.OUR_SIGNATURE, gain_over_construction=(10 ** 6,))
        self.assertIn("ЯВЛЕНИЕ", s.verdict())

    def test_the_only_conclusion_of_the_module_is_mutable_global_state(self):
        """Signature alone is unfrozen and unhashable; OUR_SIGNATURE.verdict() is writable."""
        with self.assertRaises(TypeError):
            hash(P.OUR_SIGNATURE)
        keep = (P.OUR_SIGNATURE.n_weak, P.OUR_SIGNATURE.lp_all_over_lp_strong)
        try:
            P.OUR_SIGNATURE.n_weak, P.OUR_SIGNATURE.lp_all_over_lp_strong = 0, 0.0
            self.assertIn("не характерно", P.OUR_SIGNATURE.verdict())
        finally:
            P.OUR_SIGNATURE.n_weak, P.OUR_SIGNATURE.lp_all_over_lp_strong = keep
        self.assertEqual(P.OUR_SIGNATURE.verdict(), "4/4 признаков явления: ЯВЛЕНИЕ")

    def test_no_single_signature_can_overturn_the_conclusion(self):
        """The verdict fires at ≥ 3 of 4, so ANY one признак may fail freely — including S1,
        'много ограничений размера cap+1', without which there is no phenomenon to have."""
        for name, kill in (("n_weak", 0), ("lp_all_over_lp_strong", 0.0),
                           ("max_codegree", 10 ** 6), ("gain_over_construction", (0, 10 ** 6))):
            v = dataclasses.replace(P.OUR_SIGNATURE, **{name: kill}).verdict()
            self.assertEqual(v, "3/4 признаков явления: ЯВЛЕНИЕ", name)

    def test_max_codegree_cannot_mean_what_the_field_says(self):
        """Declared: 'макс. число СЛАБЫХ ограничений через пару точек'.  Two points lie on one
        line, so that number is ≤ 1 in any point-line frame — measured.  OUR_SIGNATURE says 6,
        which is the codegree of the hypergraph of ALL collinear triples (8-point lines)."""
        for p in (5, 7, 11, 13):
            co = weak_codegrees(p)
            self.assertGreater(len(co), 0, "p=%d has weak constraints" % p)
            self.assertEqual(max(co.values()), 1, "p=%d" % p)
        self.assertEqual(P.OUR_SIGNATURE.max_codegree, 6)
        self.assertEqual([max(collinear_triple_codegrees(p).values()) for p in (5, 11, 13)],
                         [6, 6, 6])


# ══════════════════════════════════════════════════════════════════════════════════════
# D. Signature — what the type cannot hold: the integrality gap itself.
# ══════════════════════════════════════════════════════════════════════════════════════

class TestSignatureVsIntegralityGap(unittest.TestCase):

    def test_zero_gap_block_system_scores_the_phenomenon(self):
        n, strong, weak = blocks_system(3)
        self.assertEqual(brute_force_optimum(n, strong + weak, 2), 2 * 3)   # IP = 2t
        # LP = 2t as well: primal x ≡ 2/5 sums to 2t and is feasible; dual = weight 1 per block.
        self.assertTrue(all(len(c) * 0.4 <= 2 for c in strong + weak))
        self.assertAlmostEqual(n * 0.4, 2 * 3)
        self.assertEqual(zero_gap_signature(3).verdict(), "4/4 признаков явления: ЯВЛЕНИЕ")

    @gap("GAP-C-02", module="phenomenon.py",
         title="Signature has no field for the integer optimum — the integrality gap, the definition "
               "of the phenomenon, is not representable",
         expected="§0 defines the phenomenon as 'разрыв между LP (со всеми ограничениями) и "
                  "целочисленным оптимумом — линейный по размеру системы', and §3 declares S1–S6 as "
                  "the way to recognise it.  Signature must therefore carry the integer optimum (or "
                  "LP(all)/IP), and verdict() must refuse a system whose gap is zero.",
         actual="the six fields carry LP(all)/LP(strong) and nothing about the truth.  A disjoint "
                "union of t five-point blocks with cap 2, whose in-block triples are added as "
                "(redundant) weak constraints, has LP = IP = 2t exactly — verified here by brute "
                "force at t = 3 and by an explicit primal (x ≡ 2/5) / dual (weight 1 per block) "
                "pair — and scores '4/4 признаков явления: ЯВЛЕНИЕ'.",
         consequence="the module's own diagnostic certifies the phenomenon in a totally "
                     "decomposable system with zero integrality gap that a rank-1 certificate "
                     "solves exactly.  S2 as encoded measures LP(all)/LP(strong) — the wrong "
                     "ratio: it detects that the weak constraints are redundant, which is true "
                     "both when LP is blind (our case) and when there is nothing to be blind to.  "
                     "Every use of S1–S6 to decide whether an analogous system 'has our "
                     "phenomenon' — the entire input of deep_research_brief_8 — rests on a "
                     "criterion that never looks at the quantity being diagnosed.")
    def test_verdict_separates_us_from_a_zero_gap_system(self):
        self.assertIn("не характерно", zero_gap_signature(3).verdict(),
                      "a system with LP = IP = 2t is certified as the phenomenon")
        self.assertTrue(truth_fields(),
                        "no field can carry the integer optimum or the integrality gap")


# ══════════════════════════════════════════════════════════════════════════════════════
# E. Signature versus the project's own numbers: the one condition that touches the truth.
# ══════════════════════════════════════════════════════════════════════════════════════

class TestSignatureVsOurOwnData(unittest.TestCase):

    SIZES = (11, 13, 17, 19)

    def test_our_signature_gain_is_measured_on_a_different_system(self):
        """gain_over_construction is commented 'p=11,13,17,19: max − 3(p−1)'.  OUR_FRAME is
        xy ≡ ±1, i.e. k = −1, whose exact maxima are holes.py's own (32, 40, 54, 59) →
        (2, 4, 6, 5).  The declared (5, 5, 6, 5) is the maximum over k (k = 3, 2, −1, −1);
        on the frame's own numbers S4 fails and the module's headline 4/4 becomes 3/4."""
        h1 = next(h for h in H.HOLES if h.key.startswith("H1"))
        self.assertIn("(11: 32; 13: 40; 17: 54; 19: 59)", h1.testable_now)
        notes = read(_NOTES)
        self.assertIn("α (32, 40, 54, 59, 70–74)", notes)                     # k = −1 series
        self.assertIn("p=11: 32–35; p=13: 38–41; p=17: 49–54", notes)         # max over k
        honest = tuple(m - 3 * (q - 1) for m, q in zip((32, 40, 54, 59), self.SIZES))
        self.assertEqual(honest, (2, 4, 6, 5))
        self.assertEqual(tuple(P.OUR_SIGNATURE.gain_over_construction), (5, 5, 6, 5))
        self.assertEqual(signature(gain_over_construction=honest).verdict(),
                         "3/4 признаков явления: ЯВЛЕНИЕ")

    @gap("GAP-C-06", module="phenomenon.py",
         title="S4 is the only condition that touches the truth and it carries no scale: a gain "
               "linear in the size of the system passes it",
         expected="§0 defines the phenomenon by a gap 'ЛИНЕЙНЫЙ ПО РАЗМЕРУ СИСТЕМЫ' and S4 asks "
                  "that the прибавка over the algebraic construction 'не растёт (O(1))'; the field "
                  "is documented 'по размерам системы'.  The datum must therefore identify the "
                  "sizes, and the condition must reject a gain that grows with them.",
         actual="gain_over_construction is a bare Sequence[int] with no sizes attached and the "
                "condition is max − min ≤ 3 on the unlabelled numbers.  At the project's own "
                "sizes p = 11,13,17,19 the sequence (p−1)//4 = (2,3,4,4) — a gain equal to "
                "|V|/32, monotone and linear in the size of the system — has range 2 and passes "
                "S4 exactly as OUR_SIGNATURE's (5,5,6,5) does; the two verdicts are identical "
                "strings.  Nothing in the type distinguishes them, and no repair inside verdict() "
                "can, since the sizes are not in the data.",
         consequence="S4 is the only one of the four conditions that looks at the integer truth at "
                     "all (GAP-C-02: no field carries the optimum), and it is the encoding of the "
                     "project's entire target, α(P₋₁) ≤ 3(p−1) + O(1) — the O(1) IS 'the прибавка "
                     "does not grow'.  As written the diagnostic certifies that target from four "
                     "unlabelled integers and would certify it just as loudly for a system whose "
                     "gain is a fixed fraction of |V|, i.e. for a system where the construction is "
                     "NOT extremal and P4 (rigidity of extremals) is false.  Combined with the "
                     "sibling test above — OUR_SIGNATURE's four numbers are the maxima over k, "
                     "four different systems, and OUR_FRAME's own k = −1 numbers fail S4 — the "
                     "module's single asymptotic claim is neither falsifiable by growth nor true "
                     "of the frame it is attached to.")
    def test_S4_can_tell_a_bounded_gain_from_a_linear_one(self):
        linear = tuple((q - 1) // 4 for q in self.SIZES)      # gain = |V|/32 at these sizes
        self.assertEqual(linear, (2, 3, 4, 4))
        self.assertEqual(sorted(linear), list(linear))        # monotone: it grows
        self.assertNotEqual(signature(gain_over_construction=(5, 5, 6, 5)).verdict(),
                            signature(gain_over_construction=linear).verdict())


# ══════════════════════════════════════════════════════════════════════════════════════
# F. AnalogSystem — the bestiary is never diagnosed.
# ══════════════════════════════════════════════════════════════════════════════════════

class TestBestiaryContract(unittest.TestCase):

    def test_pg2q_has_no_weak_constraints_at_all(self):
        for q in (5, 7):
            pts, lines = pg2(q)
            self.assertEqual(len(pts), q * q + q + 1)
            self.assertEqual({len(L) for L in lines}, {q + 1})
            self.assertEqual(sum(1 for L in lines
                                 if P.OUR_FRAME.strength(len(L)) is P.Strength.WEAK), 0)

    def test_arcs_in_pg2q_score_the_phenomenon(self):
        """Facts from the bestiary itself: all lines full ⇒ n_weak = 0, LP(all) = LP(strong);
        truth q+1 = the conic exactly ⇒ gain 0 at every q.  S2 and S3 pass VACUOUSLY."""
        self.assertEqual(arcs_signature(7).verdict(), "3/4 признаков явления: ЯВЛЕНИЕ")
        self.assertIn("работает благодаря РЕГУЛЯРНОСТИ (все прямые полные)", P.__doc__)

    def test_regularity_is_the_bestiary_variable_and_appears_nowhere_else(self):
        """Every bestiary entry explains itself by `regularity`; no principle and no
        signature field mentions it."""
        self.assertEqual(sum(1 for a in P.BESTIARY if a.regularity.strip()), 8)
        blob = " ".join(pr.key + pr.statement + pr.consequence for pr in P.PRINCIPLES).lower()
        for word in ("регуляр", "regular", "симметри", "инвариант"):
            self.assertNotIn(word, blob)
        self.assertEqual([f.name for f in dataclasses.fields(P.Signature)
                          if "regular" in f.name], [])

    @gap("GAP-C-03", module="phenomenon.py",
         title="AnalogSystem carries no measurement: the bestiary is never run through the module's "
               "own criterion, and arcs in PG(2,q) pass it",
         expected="§3 declares S1–S6 as 'как узнать явление в данной системе' and §2 lists eight "
                  "systems as analogues whose lessons transfer to us.  Each AnalogSystem must "
                  "therefore carry the measurement placing it inside or outside the phenomenon, and "
                  "the entries the module itself calls regular/solved must come out 'не характерно'.",
         actual="AnalogSystem has six str fields, no Signature and no numbers; nothing in the module "
                "ever diagnoses a bestiary entry.  Filled from the bestiary's own facts, arcs in "
                "PG(2,q) — every line full (q+1 points, computed here for q = 5,7, so n_weak = 0 "
                "and LP(all) = LP(strong)); truth q+1 = the conic, gain 0 at every q — score "
                "'3/4 признаков явления: ЯВЛЕНИЕ'.",
         consequence="the criterion certifies the phenomenon in the one bestiary system where the "
                     "module says it is absent ('работает благодаря РЕГУЛЯРНОСТИ (все прямые "
                     "полные)', exact answer by a Bose count through a point).  S2 and S3 are "
                     "satisfied VACUOUSLY when n_weak = 0 and S4 by exactness, so the absence of "
                     "the phenomenon scores like its presence — and, by the sibling test, no single "
                     "признак can overturn a verdict that fires at ≥ 3 of 4.  Meanwhile "
                     "`regularity` — the field the bestiary uses to explain every one of its eight "
                     "entries — appears in no principle P1–P5 and in no signature field, so the "
                     "axis that actually separates the solved systems from ours is unrepresentable. "
                     "Q7 of deep_research_brief_8 ('extract the pattern: what distinguishes the "
                     "solved ones') is unanswerable inside this type system, and the mechanisms of "
                     "Q1–Q6 are imported on an analogy the module cannot check.")
    def test_every_bestiary_entry_is_diagnosed(self):
        self.assertIn("не характерно", arcs_signature(7).verdict(),
                      "the module's own regular/solved system scores as the phenomenon")
        measured = [f.name for f in dataclasses.fields(P.AnalogSystem) if f.type != "str"]
        self.assertTrue(measured, "every AnalogSystem field is free text: no entry is measured")


# ══════════════════════════════════════════════════════════════════════════════════════
# G. The declared signatures S1–S6 versus the four conditions of verdict().
# ══════════════════════════════════════════════════════════════════════════════════════

def declared_signatures():
    return sorted(set(re.findall(r"\bS([1-9])\.", P.__doc__)))


def implemented_signatures():
    return int(P.OUR_SIGNATURE.verdict().split("/")[1].split()[0])


class TestSignatureCoverage(unittest.TestCase):

    def test_verdict_implements_four_of_six_declared_signatures(self):
        self.assertEqual(declared_signatures(), ["1", "2", "3", "4", "5", "6"])
        self.assertEqual(implemented_signatures(), 4)
        self.assertTrue(P.OUR_SIGNATURE.verdict().startswith("4/4"))

    def test_S3_threshold_can_never_bind_in_a_point_line_frame(self):
        """The condition is max_codegree ≤ 8; the true weak codegree of a point-line frame is
        ≤ 1, so replacing the declared 6 by the honest 1 leaves the verdict unchanged."""
        for p in (5, 7, 11, 13):
            self.assertLessEqual(max(weak_codegrees(p).values()), 1)
        self.assertEqual(signature(max_codegree=1).verdict(), P.OUR_SIGNATURE.verdict())

    def test_the_two_unimplemented_signatures_hold_the_projects_own_headline(self):
        """S6 is the 3.45 plateau — REPORT §16's answer to the owner about what is known.
        The number appears in the spec's prose and in no field of any Signature."""
        self.assertIn("S5.", P.__doc__)
        self.assertIn("S6.", P.__doc__)
        self.assertIn("плато (у нас 3.45)", P.__doc__)
        self.assertIn("3.45 — потолок локальных сертификатов", read(_REPORT))
        values = [getattr(P.OUR_SIGNATURE, f.name) for f in dataclasses.fields(P.Signature)]
        self.assertNotIn(3.45, values)
        self.assertEqual(sensitive_fields(P.OUR_SIGNATURE),
                         {"n_weak", "n_ground", "max_codegree",
                          "lp_all_over_lp_strong", "gain_over_construction"})

    @gap("GAP-C-04", module="phenomenon.py",
         title="Three of the six declared signatures cannot be tested: S5 and S6 have no field, S3's "
               "threshold is unfalsifiable",
         expected="§3 declares six signatures S1–S6 and verdict() is their implementation; it "
                  "reports 'N/M признаков явления', so M must be 6 and each of the six must be able "
                  "to fail on some admissible Signature.",
         actual="M = 4.  S5 (soft forms / spectral bounds work numerically) and S6 (local "
                "certificates plateau — 'у нас 3.45') have no field in Signature at all: the number "
                "3.45 occurs in the module's prose and in no field value.  S3 is encoded as "
                "max_codegree ≤ 8, but two points lie on one line, so the number of WEAK "
                "(=cap+1-point) constraints through a pair is ≤ 1 in any point-line frame — "
                "measured here on the real 8(p−1) set at p = 5,7,11,13 — and the threshold can "
                "never bind; replacing OUR_SIGNATURE.max_codegree by the honest 1 leaves the "
                "verdict unchanged.  mean_degree, which carries S1's 'степени ~ log |V|' clause, "
                "is read by nothing (verified by perturbation to 0.0, −1e9, 1e300).",
         consequence="'4/4 признаков явления' over-reports: at most three of the four conditions "
                     "carry information, and the two omitted signatures hold exactly the project's "
                     "own measurements — the 3.45 plateau, the reason this whole integrality "
                     "vector exists (REPORT §16, quoted live in the sibling test: '3.45 — потолок "
                     "локальных сертификатов'), and the spectral evidence of §20/§23.  A system "
                     "whose local certificates do NOT plateau, i.e. where LP already delivers the "
                     "truth, is indistinguishable from ours under S1–S4, so the diagnostic cannot "
                     "state the one thing the project actually knows about itself.")
    def test_all_six_declared_signatures_are_implemented(self):
        self.assertEqual(implemented_signatures(), len(declared_signatures()),
                         "verdict() implements %d of the %d signatures §3 declares"
                         % (implemented_signatures(), len(declared_signatures())))


# ══════════════════════════════════════════════════════════════════════════════════════
# H. Hole — six str fields, no logical strength, no closure.
# ══════════════════════════════════════════════════════════════════════════════════════

class TestHoleContract(unittest.TestCase):

    def test_every_hole_field_is_free_text(self):
        self.assertEqual({f.type for f in dataclasses.fields(H.Hole)}, {"str"})
        self.assertEqual([f.name for f in dataclasses.fields(H.Hole)],
                         ["key", "missing_interaction", "where_it_breaks", "testable_now",
                          "filled_elsewhere", "payoff"])

    def test_interfaces_I1_I6_are_docstring_prose_with_no_type(self):
        for i in range(1, 7):
            self.assertIn("I%d " % i, H.__doc__)
        self.assertFalse(any(n.lower().startswith("interface") for n in dir(H)))
        cited = [h.key for h in H.HOLES
                 if any("(I%d" % i in " ".join(dataclasses.astuple(h)) for i in range(1, 7))]
        self.assertEqual(len(cited), 1, "only %r names an interface it consumes" % cited)

    def test_H4_and_H7_are_both_the_target_by_the_projects_own_notes(self):
        """holes.py's H7 is the notes' H4, which B.12 proves equivalent to T1; holes.py's H4
        is the exchange statement, which B.13 proves equivalent to T1 in its O(1) form."""
        h4 = next(h for h in H.HOLES if h.key.startswith("H4"))
        h7 = next(h for h in H.HOLES if h.key.startswith("H7"))
        self.assertIn("H4 в записях", h7.missing_interaction)
        self.assertIn("|S₂| ≤ (3(p−1) − |S₁|) + O(1)", h4.missing_interaction)
        notes = read(_NOTES)
        self.assertIn("conversely T1(O(1)) ⇒ H4 with c = 1", notes)            # B.12
        self.assertIn("not an intermediate\nhypothesis but the target itself", notes)
        self.assertIn("T1 (O(1) form) ⇔  f(t)", notes)                         # B.13
        # P3 calls supersaturation the softer form; in this frame it is the target itself.
        p3 = next(pr for pr in P.PRINCIPLES if pr.key.startswith("P3"))
        self.assertIn("обычно доступна раньше точной", p3.consequence)

    def test_H4s_key_experiment_has_already_been_run(self):
        """H4.testable_now calls B.13 'ключевой эксперимент'; B.13 ran it and closed with a
        verdict, and REPORT §16 logs the H4 experiment as launched.  No field can say so."""
        h4 = next(h for h in H.HOLES if h.key.startswith("H4"))
        self.assertIn("это ключевой эксперимент", h4.testable_now)
        self.assertIn("B.13", h4.testable_now)
        for still_to_do in ("посчитать", "проверить", "измерить"):    # phrased as a to-do
            self.assertIn(still_to_do, h4.testable_now)
        self.assertIn("Verdict: T2.9 negative.", read(_NOTES))        # …already answered
        self.assertIn("H4 (лемма обмена, p ≤ 31)", read(_REPORT))     # …and logged as run

    @gap("GAP-C-05", module="holes.py",
         title="Hole has no field for logical strength: a restatement of the target types "
               "identically to a missing tool, and two of the eight holes ARE the target",
         expected="holes.py declares each Hole as 'чего нам не хватает, чтобы материализовать "
                  "явление' — a tool strictly below the goal α(P₋₁) ≤ 3(p−1)+O(1) — and the eight "
                  "as eight distinct research tasks with distinct payoffs.  Some field must record "
                  "a hole's logical relation to the target (and whether it is closed), and the two "
                  "the project has already proved equivalent to T1 must be marked.",
         actual="all six fields are str: no field for logical strength, none for a result or "
                "status, none naming the interface I1–I6 it consumes (I1–I6 exist only as "
                "docstring prose; exactly one of the eight texts cites one, asserted in-test).  "
                "Two of the eight are the target: holes.py's H7 is the notes' H4 (its own "
                "missing_interaction says '(H4 в записях)') and pair_bound_notes B.12 proves "
                "'H4 ⇒ T1 in the strong O(1) form; conversely T1(O(1)) ⇒ H4 with c = 1 … not an "
                "intermediate hypothesis but the target itself'; holes.py's H4 is the exchange "
                "statement |S₂| ≤ (3(p−1) − |S₁|) + O(1) and cites B.13, which proves "
                "'T1 (O(1) form) ⇔ f(t) ≤ t + C' — that same statement — and closes 'Verdict: T2.9 "
                "negative'.  All four quotes are asserted against the live notes file.",
         consequence="two of eight research tasks are logically equivalent to each other and to the "
                     "theorem they are supposed to help prove, and nothing in the type records it.  "
                     "P3 asserts supersaturation is 'мягкая форма … обычно доступна раньше "
                     "точной'; in this frame it is not softer at all, so H7's payoff ('мягкая "
                     "форма правды; из неё α ≤ 3(p−1)+O(1) удалением') states only half of an "
                     "equivalence and P3 is false as written for OUR_FRAME.  "
                     "deep_research_brief_8 allocates external effort per hole (Q2 ← H3,H4; "
                     "Q5 ← H7) and will buy the same statement twice, priced as two cheap "
                     "sub-goals.  And since no field can record a closure, H4 — whose 'ключевой "
                     "эксперимент' B.13 already ran with a negative answer, and whose experiment "
                     "REPORT §16 logs as launched — is type-indistinguishable from an untouched "
                     "hole, so gaps.py's own design principle (a closed gap must turn the suite "
                     "red) cannot be applied to holes.py at all.")
    def test_holes_are_distinct_tasks_strictly_below_the_target(self):
        relation = [f.name for f in dataclasses.fields(H.Hole) if f.type != "str"]
        self.assertTrue(relation,
                        "every Hole field is free text: nothing records a hole's logical strength "
                        "relative to α(P₋₁) ≤ 3(p−1)+O(1), nor whether it has been closed")
        marked = {h.key.split()[0] for h in H.HOLES
                  if any(getattr(h, name) for name in relation)}
        self.assertLessEqual({"H4", "H7"}, marked,
                             "B.12 and B.13 prove both equivalent to T1; neither is marked")


if __name__ == "__main__":
    unittest.main(verbosity=2)
