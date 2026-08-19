"""Executable contracts for the exact/at-least rot2 census.

This module follows the repository owner's ``principles.py`` convention:

* semantic MUSTs are dataclasses and assertions;
* forbidden inferences raise named breaches;
* evidence is carried by the claim that uses it;
* unresolved architecture choices remain honest JUDGMENTs.

It is deliberately solver-independent.  A completeness checker must not import
the searcher's pruning, symmetry breaking, or orbit-conflict implementation.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum, auto
from math import log10
from pathlib import Path
from typing import Iterable, Mapping, Sequence


# --- FORBIDDEN: the exception ontology comes first -----------------------------------------


class ContractBreach(Exception):
    """A published computational claim crossed a semantic boundary."""


class MissingProblemSemantics(ContractBreach):
    pass


class CountUniverseMismatch(ContractBreach):
    pass


class SearchUsedAsEnumeration(ContractBreach):
    pass


class TimeoutUsedAsExhaustion(ContractBreach):
    pass


class IncompleteTaskSet(ContractBreach):
    pass


class ConflictingTerminalAttempts(ContractBreach):
    pass


class OrbitEncodingIncomplete(ContractBreach):
    pass


class WeightedCardinalityLost(ContractBreach):
    pass


class NonHereditaryCanonicalPrune(ContractBreach):
    pass


class ProjectedModelOverlap(ContractBreach):
    pass


class InvalidBlockingClause(ContractBreach):
    pass


class IncomparableNodeMetrics(ContractBreach):
    pass


class ImplementationToAlgorithmClassLeap(ContractBreach):
    pass


class OrderOfMagnitudeMisstatement(ContractBreach):
    pass


class MissingEvidence(ContractBreach):
    pass


# --- MUST: no result is allowed to say merely "rot2" ---------------------------------------


class Universe(Enum):
    """The four non-interchangeable meanings found behind the label rot2."""

    H_FIXED_LABELLED = auto()
    EXACT_H_LABELLED = auto()
    H_CONTAINING_D4_CLASSES = auto()
    EXACT_H_D4_CLASSES = auto()


class RunMode(Enum):
    FIND_ONE = auto()
    ENUMERATE_ALL = auto()
    COUNT_ALL = auto()
    PROVE_EMPTY = auto()


class AttemptStatus(Enum):
    EXHAUSTED = auto()
    FOUND_ONE = auto()
    TIMEOUT = auto()
    CRASHED = auto()
    KILLED = auto()
    PROOF_FAILED = auto()


@dataclass(frozen=True)
class ProblemSpec:
    n: int
    universe: Universe
    mode: RunMode

    def __post_init__(self) -> None:
        if self.n < 2:
            raise MissingProblemSemantics("n must be at least 2")


@dataclass(frozen=True)
class CensusCount:
    spec: ProblemSpec
    value: int

    def __post_init__(self) -> None:
        if self.value < 0:
            raise ValueError("a census count cannot be negative")


@dataclass(frozen=True)
class Evidence:
    says: str
    artifacts: tuple[str, ...]
    verifier: str

    def __post_init__(self) -> None:
        if not self.says or not self.artifacts or not self.verifier:
            raise MissingEvidence(self.says or "claim without a statement")


@dataclass(frozen=True)
class Attempt:
    task_id: str
    status: AttemptStatus
    result_digest: str | None = None


@dataclass(frozen=True)
class NodeMetric:
    name: str
    increments_on: str

    def __post_init__(self) -> None:
        if not self.name or not self.increments_on:
            raise IncomparableNodeMetrics("node metrics require an increment rule")


@dataclass(frozen=True)
class CompletenessClaim:
    spec: ProblemSpec
    expected_tasks: frozenset[str]
    evidence: Evidence


def compare_counts(left: CensusCount, right: CensusCount) -> int:
    """Compare only counts from the exact same mathematical universe."""

    if left.spec != right.spec:
        raise CountUniverseMismatch(f"{left.spec!r} != {right.spec!r}")
    return left.value - right.value


def compare_node_metrics(left: NodeMetric, right: NodeMetric) -> None:
    """Reject a cases/nodes comparison until both counters mean the same event."""

    if left.increments_on != right.increments_on:
        raise IncomparableNodeMetrics(
            f"{left.name} increments on {left.increments_on!r}; "
            f"{right.name} increments on {right.increments_on!r}"
        )


def require_exhaustive_mode(spec: ProblemSpec) -> None:
    if spec.mode is RunMode.FIND_ONE:
        raise SearchUsedAsEnumeration("FIND_ONE cannot support a completeness claim")


def require_complete_tasks(expected: Iterable[str], attempts: Iterable[Attempt]) -> None:
    """Every expected immutable task needs a successful exhausted attempt.

    A timeout followed by a successful rerun is allowed.  Two exhausted attempts
    for one task are allowed only when they publish the same result digest.
    """

    expected_set = frozenset(expected)
    by_task: dict[str, list[Attempt]] = {}
    for attempt in attempts:
        by_task.setdefault(attempt.task_id, []).append(attempt)

    unexpected = frozenset(by_task) - expected_set
    if unexpected:
        raise IncompleteTaskSet(f"unexpected tasks: {sorted(unexpected)!r}")

    missing = []
    for task_id in sorted(expected_set):
        exhausted = [a for a in by_task.get(task_id, ()) if a.status is AttemptStatus.EXHAUSTED]
        if not exhausted:
            prior = by_task.get(task_id, ())
            if any(a.status is AttemptStatus.TIMEOUT for a in prior):
                raise TimeoutUsedAsExhaustion(f"task {task_id} has only a timeout")
            missing.append(task_id)
            continue
        digests = {a.result_digest for a in exhausted}
        if len(digests) > 1:
            raise ConflictingTerminalAttempts(
                f"task {task_id} has conflicting exhausted digests: {sorted(digests)!r}"
            )
    if missing:
        raise IncompleteTaskSet(f"missing exhausted tasks: {missing!r}")


def make_completeness_claim(
    spec: ProblemSpec,
    expected: Iterable[str],
    attempts: Iterable[Attempt],
    evidence: Evidence,
) -> CompletenessClaim:
    require_exhaustive_mode(spec)
    expected_set = frozenset(expected)
    require_complete_tasks(expected_set, attempts)
    return CompletenessClaim(spec, expected_set, evidence)


# --- exact geometry: a reference language independent of production masks ------------------


Point = tuple[int, int]


def rot2(point: Point, n: int) -> Point:
    x, y = point
    return n - 1 - x, n - 1 - y


def orbit_id(point: Point, n: int) -> Point:
    return min(point, rot2(point, n))


def orbit(point: Point, n: int) -> frozenset[Point]:
    return frozenset((point, rot2(point, n)))


def collinear(a: Point, b: Point, c: Point) -> bool:
    return (b[0] - a[0]) * (c[1] - a[1]) == (b[1] - a[1]) * (c[0] - a[0])


def clause_of_triple(triple: Sequence[Point], n: int) -> frozenset[Point]:
    if len(triple) != 3 or not collinear(*triple):
        raise ValueError("a forbidden clause must come from three collinear points")
    clause = frozenset(orbit_id(point, n) for point in triple)
    if len(clause) not in (1, 2, 3):
        raise OrbitEncodingIncomplete(f"unexpected orbit-clause arity {len(clause)}")
    return clause


def row_weight(oid: Point, row: int, n: int) -> int:
    """Coefficient of an orbit variable in one exact row constraint."""

    return sum(x == row for x, _ in orbit(oid, n))


def d4_images(point: Point, n: int) -> tuple[Point, ...]:
    x, y = point
    m = n - 1
    return (
        (x, y),
        (y, m - x),
        (m - x, m - y),
        (m - y, x),
        (m - x, y),
        (x, m - y),
        (y, x),
        (m - y, m - x),
    )


def stabilizer_size(points: Iterable[Point], n: int) -> int:
    book = frozenset(points)
    return sum(
        frozenset(d4_images(point, n)[motion] for point in book) == book
        for motion in range(8)
    )


def is_h_fixed(points: Iterable[Point], n: int) -> bool:
    book = frozenset(points)
    return frozenset(rot2(point, n) for point in book) == book


def is_exact_h(points: Iterable[Point], n: int) -> bool:
    return is_h_fixed(points, n) and stabilizer_size(points, n) == 2


# --- certificates and projected enumeration -------------------------------------------------


def projected_blocking_clause(model: Mapping[str, bool], projected: Iterable[str]) -> tuple[str, ...]:
    keys = tuple(projected)
    if not set(keys).issubset(model) or len(set(keys)) != len(keys):
        raise InvalidBlockingClause("the model must assign every projected variable exactly once")
    return tuple(("~" if model[key] else "") + key for key in keys)


def assert_projected_disjoint(
    leaf_models: Iterable[Iterable[Mapping[str, bool]]], projected: Iterable[str]
) -> None:
    keys = tuple(projected)
    seen: set[tuple[bool, ...]] = set()
    for leaf in leaf_models:
        for model in leaf:
            projection = tuple(model[key] for key in keys)
            if projection in seen:
                raise ProjectedModelOverlap(f"duplicate projected model: {projection!r}")
            seen.add(projection)


def require_hereditary_canonical_proof(proof: str | None) -> None:
    if not proof:
        raise NonHereditaryCanonicalPrune(
            "partial canonical pruning with dynamic branching requires a heredity proof"
        )


# --- forecasts: evidence, never lower bounds ------------------------------------------------


def extrapolated_nodes(last_nodes: int, factor: int | float, steps: int) -> int:
    return round(last_nodes * factor**steps)


def budget_gap(nodes: int, nodes_per_second: float, budget_core_hours: float) -> float:
    return nodes / (nodes_per_second * 3600 * budget_core_hours)


def decimal_orders(gap: float) -> float:
    if gap <= 0:
        raise ValueError("a multiplicative gap must be positive")
    return log10(gap)


def assert_reported_orders(gap: float, reported: float, tolerance: float = 0.01) -> None:
    actual = decimal_orders(gap)
    if abs(actual - reported) > tolerance:
        raise OrderOfMagnitudeMisstatement(f"reported {reported}, but log10(gap) is {actual:.6f}")


def algorithm_class_lower_bound_from_calibration(*_measurements: object) -> None:
    raise ImplementationToAlgorithmClassLeap(
        "an implementation calibration is not a lower bound for DFS/B&B as an algorithm class"
    )


def choose_production_architecture(_evidence: Sequence[Evidence]) -> None:
    """JUDGMENT: this remains open until the specified ablations and pilots are measured."""

    raise NotImplementedError("DFS, SAT, MITM and ZDD must be selected from measured pilots")


# --- legacy-log adapter: quarantined evidence, not the target report format -----------------


_TWOLOOP = re.compile(r"^x=(\d+) y=(\d+) :: (all|dead|timeout-all)\b")


def parse_twoloop_attempts(path: str | Path) -> list[Attempt]:
    attempts = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        match = _TWOLOOP.match(line)
        if not match:
            continue
        x, y, word = match.groups()
        status = AttemptStatus.TIMEOUT if word == "timeout-all" else AttemptStatus.EXHAUSTED
        attempts.append(Attempt(f"{x},{y}", status))
    return attempts


def expected_twoloop_tasks(half: int) -> frozenset[str]:
    return frozenset(f"{x},{y}" for x in range(half) for y in range(x + 1, half))


# --- import-time PROOFS: small, exact, and cheap --------------------------------------------


N32_IF_X19 = 5_699_047_773_074_403_673
assert extrapolated_nodes(17_661_187, 19, 9) == N32_IF_X19
assert clause_of_triple(((0, 0), (1, 1), (2, 2)), 4) == frozenset(((0, 0), (1, 1)))
assert row_weight((1, 0), 1, 3) == 2
assert is_h_fixed(((0, 0), (0, 1), (1, 0), (1, 1)), 2)
assert not is_exact_h(((0, 0), (0, 1), (1, 0), (1, 1)), 2)


if __name__ == "__main__":
    # Breach tests are executable prose: every forbidden inference must actually fail.
    try:
        algorithm_class_lower_bound_from_calibration((14, 17_661_187))
    except ImplementationToAlgorithmClassLeap:
        pass
    else:  # pragma: no cover - it is the breach itself
        raise AssertionError("implementation calibration escaped as an algorithm-class lower bound")

    gap = budget_gap(N32_IF_X19, 795_000, 10_000)
    assert 199_000 < gap < 200_000
    assert 5.29 < decimal_orders(gap) < 5.31
    print("rot2 census contracts: PROOFS and breach tests pass")
