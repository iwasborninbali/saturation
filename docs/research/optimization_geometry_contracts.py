"""Finite geometry counts used by deep research 12.

The functions validate counts and grouping conventions only.  They do not claim that
the corresponding redundant constraints improve SAT runtime.
"""

from collections import Counter
from itertools import combinations, product
from math import gcd


def primitive_unoriented(vector):
    divisor = 0
    for coordinate in vector:
        divisor = gcd(divisor, abs(coordinate))
    if divisor == 0:
        raise ValueError("zero vector has no direction")
    reduced = tuple(coordinate // divisor for coordinate in vector)
    first = next(coordinate for coordinate in reduced if coordinate)
    return tuple(-coordinate for coordinate in reduced) if first < 0 else reduced


def grid_points(n=7):
    return tuple(product(range(n), repeat=3))


def pair_direction_sizes(n=7):
    counts = Counter()
    for left, right in combinations(grid_points(n), 2):
        delta = tuple(right[i] - left[i] for i in range(3))
        counts[primitive_unoriented(delta)] += 1
    return counts


def direction_lift_counts(n=7):
    sizes = pair_direction_sizes(n)
    pairs = sum(sizes.values())
    sequential_aux = sum(size - 1 for size in sizes.values())
    sequential_clauses = sum(3 * size - 4 for size in sizes.values())
    return {
        "pairs": pairs,
        "directions": len(sizes),
        "min_group": min(sizes.values()),
        "max_group": max(sizes.values()),
        "link_clauses": pairs,
        "sequential_aux": sequential_aux,
        "sequential_clauses": sequential_clauses,
        "added_variables": pairs + sequential_aux,
        "added_clauses": pairs + sequential_clauses,
    }


def collinear_2d(left, middle, right):
    return (middle[0] - left[0]) * (right[1] - left[1]) == (
        middle[1] - left[1]
    ) * (right[0] - left[0])


def layer_collinear_triples(n=7):
    points = tuple(product(range(n), repeat=2))
    return sum(collinear_2d(*triple) for triple in combinations(points, 3))


def central_pencil_directions(n=7):
    if n % 2 == 0:
        raise ValueError("a unique central coordinate line requires odd n")
    centre = n // 2
    offsets = (
        (first - centre, second - centre)
        for first in range(n)
        for second in range(n)
        if (first, second) != (centre, centre)
    )
    return frozenset(primitive_unoriented(offset) for offset in offsets)


def central_line_binary_clause_count(n=7):
    return 3 * (n * (n - 1) // 2)


if __name__ == "__main__":
    print(
        {
            "layer_collinear_triples": layer_collinear_triples(),
            "central_pencil_classes": len(central_pencil_directions()),
            "central_line_binary_clauses": central_line_binary_clause_count(),
            "direction_lift": direction_lift_counts(),
        }
    )
