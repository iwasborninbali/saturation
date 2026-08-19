"""Regression and breach tests for ``rot2_census_contracts.py``.

Stdlib-only on purpose: this checker is meant to survive independently of the
production solver and its dependencies.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))

import rot2_census_contracts as C  # noqa: E402


class SemanticFrameTests(unittest.TestCase):
    def test_four_rot2_universes_are_not_interchangeable(self):
        fixed = C.CensusCount(
            C.ProblemSpec(10, C.Universe.H_FIXED_LABELLED, C.RunMode.COUNT_ALL), 67
        )
        exact_classes = C.CensusCount(
            C.ProblemSpec(10, C.Universe.EXACT_H_D4_CLASSES, C.RunMode.COUNT_ALL), 13
        )
        with self.assertRaises(C.CountUniverseMismatch):
            C.compare_counts(fixed, exact_classes)

    def test_n2_is_at_least_rot2_but_not_exact_rot2(self):
        board = {(0, 0), (0, 1), (1, 0), (1, 1)}
        self.assertTrue(C.is_h_fixed(board, 2))
        self.assertEqual(C.stabilizer_size(board, 2), 8)
        self.assertFalse(C.is_exact_h(board, 2))

    def test_search_result_cannot_construct_completeness_claim(self):
        spec = C.ProblemSpec(8, C.Universe.H_FIXED_LABELLED, C.RunMode.FIND_ONE)
        evidence = C.Evidence("eight objects found", ("search.log",), "independent geometry")
        attempts = [C.Attempt("root", C.AttemptStatus.EXHAUSTED, "abc")]
        with self.assertRaises(C.SearchUsedAsEnumeration):
            C.make_completeness_claim(spec, {"root"}, attempts, evidence)

    def test_evidence_cannot_be_empty(self):
        with self.assertRaises(C.MissingEvidence):
            C.Evidence("the census is complete", (), "")


class ManifestTests(unittest.TestCase):
    def test_timeout_is_not_exhaustion(self):
        with self.assertRaises(C.TimeoutUsedAsExhaustion):
            C.require_complete_tasks(
                {"1,4"}, [C.Attempt("1,4", C.AttemptStatus.TIMEOUT)]
            )

    def test_timeout_then_successful_rerun_is_allowed(self):
        C.require_complete_tasks(
            {"1,4"},
            [
                C.Attempt("1,4", C.AttemptStatus.TIMEOUT),
                C.Attempt("1,4", C.AttemptStatus.EXHAUSTED, "catalog-a"),
            ],
        )

    def test_conflicting_terminal_attempts_are_rejected(self):
        with self.assertRaises(C.ConflictingTerminalAttempts):
            C.require_complete_tasks(
                {"0,1"},
                [
                    C.Attempt("0,1", C.AttemptStatus.EXHAUSTED, "catalog-a"),
                    C.Attempt("0,1", C.AttemptStatus.EXHAUSTED, "catalog-b"),
                ],
            )

    def test_release_twoloop_n36_is_detected_as_incomplete(self):
        log = ROOT / "logs" / "sweeps" / "twoloop_n36_exh.txt"
        attempts = C.parse_twoloop_attempts(log)
        expected = C.expected_twoloop_tasks(18)
        self.assertEqual(len(expected), 153)
        self.assertEqual({a.task_id for a in attempts}, expected)
        self.assertEqual(
            {a.task_id for a in attempts if a.status is C.AttemptStatus.TIMEOUT}, {"1,4"}
        )
        with self.assertRaisesRegex(C.TimeoutUsedAsExhaustion, "1,4"):
            C.require_complete_tasks(expected, attempts)


class GeometryAndEncodingTests(unittest.TestCase):
    def test_binary_orbit_clause_is_not_lost(self):
        # The two half-turn orbits on the n=4 main diagonal are already incompatible.
        clause = C.clause_of_triple(((0, 0), (1, 1), (2, 2)), 4)
        self.assertEqual(clause, {(0, 0), (1, 1)})
        self.assertEqual(len(clause), 2)

    def test_odd_central_row_constraint_is_weighted(self):
        # Orbit {(1,0),(1,2)} alone contributes both required points to row 1.
        self.assertEqual(C.orbit((1, 0), 3), {(1, 0), (1, 2)})
        self.assertEqual(C.row_weight((1, 0), 1, 3), 2)

    def test_partial_canonical_pruning_requires_heredity_proof(self):
        with self.assertRaises(C.NonHereditaryCanonicalPrune):
            C.require_hereditary_canonical_proof(None)
        C.require_hereditary_canonical_proof("canonical construction path theorem")


class ProjectionCertificateTests(unittest.TestCase):
    def test_blocker_is_the_full_projected_complement(self):
        self.assertEqual(
            C.projected_blocking_clause({"x": True, "z": False}, ("x", "z")),
            ("~x", "z"),
        )
        with self.assertRaises(C.InvalidBlockingClause):
            C.projected_blocking_clause({"x": True}, ("x", "z"))
        with self.assertRaises(C.InvalidBlockingClause):
            C.projected_blocking_clause({"x": True, "aux": False}, ("x", "z"))

    def test_auxiliary_cube_split_is_not_projected_disjoint(self):
        # Leaves y and ~y both contain the same two projections on x.
        leaves = [
            ({"x": False, "y": True}, {"x": True, "y": True}),
            ({"x": False, "y": False}, {"x": True, "y": False}),
        ]
        with self.assertRaises(C.ProjectedModelOverlap):
            C.assert_projected_disjoint(leaves, ("x",))


class ForecastBoundaryTests(unittest.TestCase):
    def test_x19_arithmetic_is_exact(self):
        self.assertEqual(
            C.extrapolated_nodes(17_661_187, 19, 9),
            5_699_047_773_074_403_673,
        )

    def test_budget_gap_is_5_30_orders_not_13(self):
        gap = C.budget_gap(C.N32_IF_X19, 795_000, 10_000)
        self.assertAlmostEqual(gap, 199_128.1541954718)
        self.assertAlmostEqual(C.decimal_orders(gap), 5.299132668100281)
        C.assert_reported_orders(gap, 5.30)
        with self.assertRaises(C.OrderOfMagnitudeMisstatement):
            C.assert_reported_orders(gap, 13)

    def test_node_counters_need_the_same_increment_semantics(self):
        local = C.NodeMetric("local nodes", "every recursive entry")
        historical = C.NodeMetric("Flammenkamp cases", "terminal case")
        with self.assertRaises(C.IncomparableNodeMetrics):
            C.compare_node_metrics(local, historical)

    def test_calibration_cannot_become_algorithm_class_lower_bound(self):
        with self.assertRaises(C.ImplementationToAlgorithmClassLeap):
            C.algorithm_class_lower_bound_from_calibration(
                (6, 157), (8, 2_546), (10, 43_008), (12, 947_135), (14, 17_661_187)
            )

    def test_architecture_choice_remains_judgment(self):
        with self.assertRaises(NotImplementedError):
            C.choose_production_architecture(())


if __name__ == "__main__":
    unittest.main(verbosity=2)
