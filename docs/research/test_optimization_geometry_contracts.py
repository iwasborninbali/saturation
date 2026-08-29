"""Breach tests for the finite geometry counts in deep research 12."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import optimization_geometry_contracts as G


class GeometryContractTests(unittest.TestCase):
    def test_layer_has_824_collinear_triples(self):
        self.assertEqual(G.layer_collinear_triples(), 824)

    def test_central_coordinate_line_has_16_plane_classes(self):
        self.assertEqual(len(G.central_pencil_directions()), 16)
        self.assertEqual(G.central_line_binary_clause_count(), 63)

    def test_direction_lift_counts(self):
        self.assertEqual(
            G.direction_lift_counts(),
            {
                "pairs": 58653,
                "directions": 865,
                "min_group": 2,
                "max_group": 1029,
                "link_clauses": 58653,
                "sequential_aux": 57788,
                "sequential_clauses": 172499,
                "added_variables": 116441,
                "added_clauses": 231152,
            },
        )


if __name__ == "__main__":
    unittest.main()
