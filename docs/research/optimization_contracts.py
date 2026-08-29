"""Executable contracts for the exact-19 sparse-layer cover in deep research 12.

This module proves only finite combinatorial bookkeeping.  It deliberately makes no
runtime or solver-performance claim.
"""

from itertools import combinations, product
from math import comb


N_LAYERS = 7
LAYER_CAP = 3
TARGET = 19
LAYER_CELLS = 49
OMITTED_PAIR_LAYER = 6


def exact_profiles():
    """All layer-size profiles compatible with exact target and the plane cap."""
    return tuple(
        p
        for p in product(range(LAYER_CAP + 1), repeat=N_LAYERS)
        if sum(p) == TARGET
    )


def sparse_branch_sizes():
    """Branch descriptors (layer, cardinality), before choosing actual cells."""
    singleton = tuple((layer, 1) for layer in range(N_LAYERS))
    pairs = tuple(
        (layer, 2)
        for layer in range(N_LAYERS)
        if layer != OMITTED_PAIR_LAYER
    )
    return singleton + pairs


def covering_branches(profile):
    """Sparse branch descriptors whose exact layer cardinality matches profile."""
    return tuple(branch for branch in sparse_branch_sizes() if profile[branch[0]] == branch[1])


def sparse_cube_count():
    return N_LAYERS * comb(LAYER_CELLS, 1) + (N_LAYERS - 1) * comb(LAYER_CELLS, 2)


def old_plane_cube_count():
    return sum(comb(LAYER_CELLS, k) for k in range(LAYER_CAP + 1))


def profile_shapes():
    return {tuple(sorted(p, reverse=True)) for p in exact_profiles()}


def uncovered_profiles(branches=None):
    """Return profiles missed by a candidate set of (layer, cardinality) branches."""
    if branches is None:
        branches = sparse_branch_sizes()
    branches = set(branches)
    return tuple(
        p
        for p in exact_profiles()
        if not any((layer, p[layer]) in branches for layer in range(N_LAYERS))
    )


def minimum_pair_layer_positions():
    """Brute-force the smallest set of layer positions hitting every pair of layers."""
    layers = range(N_LAYERS)
    edges = tuple(combinations(layers, 2))
    for size in range(N_LAYERS + 1):
        winners = []
        for chosen in combinations(layers, size):
            chosen = set(chosen)
            if all(chosen.intersection(edge) for edge in edges):
                winners.append(tuple(sorted(chosen)))
        if winners:
            return tuple(winners)
    raise AssertionError("finite complete graph must have a vertex cover")


def contract_report():
    profiles = exact_profiles()
    cover_multiplicity = tuple(len(covering_branches(p)) for p in profiles)
    return {
        "profiles": len(profiles),
        "shapes": tuple(sorted(profile_shapes())),
        "sparse_cubes": sparse_cube_count(),
        "old_cubes": old_plane_cube_count(),
        "cover_multiplicity_min": min(cover_multiplicity),
        "cover_multiplicity_max": max(cover_multiplicity),
        "minimum_pair_layer_positions": len(minimum_pair_layer_positions()[0]),
    }


if __name__ == "__main__":
    print(contract_report())
