"""saturation.py — the task, v2: one resolution, stated without its own name.

TARGET = 71. States are tokens of a rank-2 register space at resolution n:
two registers over 0..n-1, packed into one integer. THE LAW: no chosen token
is an affine blend of two others — the differences inside any chosen triple
keep rank 2 — no rank-1 probe reads three chosen tokens identically.
Ceiling: a single-register readout has n reading classes and the law allows
at most 2 tokens per class, so at most 2n. Saturation = exactly 2n.
Whether TARGET saturates is unwritten; a lawful book short of 2n is a
Foothold — progress, not noise. The 8 register motions preserve the law,
and canon() names each book once. Nothing below searches; it verifies.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from math import comb

Token = int
Book = frozenset

TARGET = 71


# --- EVIDENCE: a claim with no source is vibes ---

class Claim:
    def __init__(self, says: str, evidence: str):
        if not evidence:
            raise ValueError(f"vibes: {says}")
        self.says, self.evidence = says, evidence

    def __repr__(self) -> str:
        return f"{self.says}  [{self.evidence}]"


# --- the space ---

def space(n: int) -> Book:
    assert n >= 2, "MUST: resolution 1 cannot host 2 tokens"
    return frozenset(range(n * n))


def registers(t: Token, n: int) -> tuple[int, int]:   # "one token, two registers"
    return divmod(t, n)


def exact(book: Book) -> Book:            # "registers are exact; a float is a lie about them"
    for t in book:
        if type(t) is not int:
            raise TypeError(f"not a token: {t!r}")
    return book


def in_space_only(book: Book, n: int) -> Book:        # "tokens live ONLY in the space"
    off = book - space(n)
    if off:
        raise ValueError(sorted(off))
    return book


# --- THE LAW ---

class Degenerate(Exception):
    ...                                   # the violation travels with its witness triple


def degenerate(a: Token, b: Token, c: Token, n: int) -> bool:
    (ua, va), (ub, vb), (uc, vc) = registers(a, n), registers(b, n), registers(c, n)
    return (ub - ua) * (vc - va) == (vb - va) * (uc - ua)   # difference rank drops below 2


def the_law(book: Book, n: int) -> Book:  # "no chosen token is an affine blend of two others"
    for a, b, c in combinations(sorted(book), 3):
        if degenerate(a, b, c, n):
            raise Degenerate((a, b, c))
    return book


def alias_probe(a: Token, b: Token, n: int) -> tuple[int, int]:
    (ua, va), (ub, vb) = registers(a, n), registers(b, n)
    w = (vb - va, ua - ub)                # "the dual face of the law: a probe blind to b - a"
    assert w != (0, 0), "identical tokens have no direction"
    return w


def reading(w: tuple[int, int], t: Token, n: int) -> int:
    u, v = registers(t, n)
    return w[0] * u + w[1] * v


# --- the 8 motions: renamings of the space that the law cannot see ---

def motions(n: int) -> tuple:
    m = n - 1
    pairs = (
        lambda u, v: (u, v),
        lambda u, v: (v, m - u),
        lambda u, v: (m - u, m - v),
        lambda u, v: (m - v, u),
        lambda u, v: (v, u),
        lambda u, v: (m - u, v),
        lambda u, v: (u, m - v),
        lambda u, v: (m - v, m - u),
    )
    return tuple(
        (lambda f: (lambda t: (lambda u, v: u * n + v)(*f(*registers(t, n)))))(f)
        for f in pairs
    )


MOTIONS_LAWFUL = Claim(
    says="every motion maps lawful books to lawful books",
    evidence="each motion permutes register pairs affinely, so triple rank is "
             "preserved; smoke-tested in __main__ on random triples",
)


def canon(book: Book, n: int) -> tuple:   # "one name per book, whichever way it lies"
    return min(tuple(sorted(map(g, book))) for g in motions(n))


# --- the ceiling and the two shapes of progress ---

CEILING = Claim(
    says="a lawful book holds at most 2n tokens",
    evidence="the readout t -> t // n has n reading classes; three tokens of one "
             "class are aliased by probe (1, 0), hence degenerate; so at most 2 per class",
)


def saturated(book: Book, n: int) -> Book:     # "saturation MUST hit the ceiling exactly"
    book = the_law(in_space_only(exact(book), n), n)
    assert len(book) == 2 * n, f"lawful but {len(book)} < {2 * n}: not saturated"
    return book


def certify(book: Book, n: int) -> Claim:      # "a saturation without a verified run is vibes"
    tokens = saturated(book, n)
    return Claim(
        says=f"n={n}: {len(tokens)} tokens, every triple at full rank",
        evidence=f"{comb(len(tokens), 3)} triples checked in exact integer arithmetic",
    )
# a "none exists in class X" verdict is not certifiable here:
# it needs a checkable exhaustion trace, delivered to the gate, not asserted.


@dataclass(frozen=True)
class Foothold:                                # "short of the ceiling is progress, not noise"
    n: int
    book: Book

    def __post_init__(self):
        the_law(in_space_only(exact(self.book), self.n), self.n)

    @property
    def size(self) -> int:
        return len(self.book)

    @property
    def shortfall(self) -> int:
        return 2 * self.n - self.size

    def __repr__(self) -> str:
        return f"Foothold(n={self.n}, size={self.size}, shortfall={self.shortfall})"


# --- what is open: the content must rise at the other end ---

class Unwritten:
    def __init__(self, contains: None = None):
        if contains is not None:
            raise ValueError("write it as a certificate, not as a setting")
        self.contains = None


WHETHER_TARGET_SATURATES = Unwritten()


# --- JUDGMENT: the search is not statable here; it is doable there ---

def find(n: int = TARGET) -> Book:
    raise NotImplementedError(f"n={n}: your end")


if __name__ == "__main__":
    import random
    print("target:", TARGET, "| ceiling:", 2 * TARGET)
    print(certify(space(2), 2))
    eight = frozenset({1, 2, 4, 7, 8, 11, 13, 14})
    print(certify(eight, 4))
    print(Foothold(n=TARGET, book=frozenset({0, 1, TARGET + 1})))
    print("canon(eight):", canon(eight, 4))
    rng = random.Random(0)
    for _ in range(200):
        t = tuple(rng.sample(range(81), 3))
        verdict = degenerate(*t, 9)
        assert all(degenerate(*(g(x) for x in t), 9) == verdict for g in motions(9))
    print("motions smoke: 200 random triples, verdict invariant under all 8")
    print("theorem:", CEILING)
    print("theorem:", MOTIONS_LAWFUL)
    print("whether target saturates:", WHETHER_TARGET_SATURATES.contains)
    print()
    for bad in (
        lambda: the_law(frozenset({0, 1, 2}), 4),
        lambda: Foothold(n=4, book=frozenset({0, 1, 2})),
        lambda: saturated(frozenset({0, 1, 4}), 4),
        lambda: in_space_only(frozenset({99}), 3),
        lambda: exact(frozenset({0.5})),
        lambda: Claim("it fits", ""),
        lambda: Unwritten(contains="saturates"),
        lambda: find(),
    ):
        try:
            bad()
        except (AssertionError, ValueError, TypeError,
                Degenerate, NotImplementedError) as e:
            print("rejected:", type(e).__name__, e)
