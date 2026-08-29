"""Breach tests for the exact-19 sparse-layer cover."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import optimization_contracts as C


class SparseLayerCoverTests(unittest.TestCase):
    def test_exact_profiles_have_only_the_two_claimed_shapes(self):
        self.assertEqual(len(C.exact_profiles()), 28)
        self.assertEqual(
            C.profile_shapes(),
            {
                (3, 3, 3, 3, 3, 3, 1),
                (3, 3, 3, 3, 3, 2, 2),
            },
        )

    def test_7399_cover_is_complete_but_may_overlap(self):
        self.assertEqual(C.sparse_cube_count(), 7399)
        self.assertEqual(C.old_plane_cube_count(), 19650)
        self.assertEqual(C.uncovered_profiles(), ())
        multiplicities = {len(C.covering_branches(p)) for p in C.exact_profiles()}
        self.assertEqual(multiplicities, {1, 2})

    def test_six_pair_layer_positions_are_necessary(self):
        minimum_covers = C.minimum_pair_layer_positions()
        self.assertEqual(len(minimum_covers[0]), 6)
        self.assertEqual(len(minimum_covers), 7)

    def test_deleting_a_singleton_class_creates_a_gap(self):
        branches = set(C.sparse_branch_sizes())
        branches.remove((6, 1))
        self.assertIn((3, 3, 3, 3, 3, 3, 1), C.uncovered_profiles(branches))

    def test_deleting_a_required_pair_class_creates_a_gap(self):
        branches = set(C.sparse_branch_sizes())
        branches.remove((5, 2))
        self.assertTrue(C.uncovered_profiles(branches))

    def test_fixed_x0_sparse_split_is_not_complete(self):
        self.assertTrue(C.uncovered_profiles({(0, 1), (0, 2)}))

    def test_cover_requires_exact_19_bridge(self):
        self.assertEqual(C.covering_branches((3, 3, 3, 3, 3, 3, 3)), ())


if __name__ == "__main__":
    unittest.main()
