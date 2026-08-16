"""saturation.py — a task in a quantized latent, stated without its own name.

States are tokens of a rank-2 register space at resolution n: two registers,
each ranging over 0..n-1, packed into one integer. Choose tokens. THE LAW:
no chosen token is an affine blend of two others — equivalently, the
differences inside any chosen triple never drop to rank 1 — equivalently,
no rank-1 probe reads three chosen tokens identically. Ceiling: any
single-register readout has n reading classes, and the law allows at most 2
tokens per class, so at most 2n. A book that hits 2n is *saturated*.
Which resolutions admit saturation is deliberately not written here.
Nothing below searches; it verifies or refuses to pretend.
"""

from __future__ import annotations

from itertools import combinations
from math import comb

Token = int
Book = frozenset


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


# --- the ceiling and the target ---

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


# --- what is open: the content must rise at the other end ---

class Frontier:
    def __init__(self, contains: None = None):
        if contains is not None:
            raise ValueError("a frontier with content is a submission, not a fact")
        self.contains = None


FRONTIER = Frontier()                     # "which resolutions saturate is not recorded here"


# --- JUDGMENT: the search is not statable here; it is doable there ---

def find(n: int) -> Book:
    raise NotImplementedError(f"n={n}: your end")


# --- the blind checks itself ---

def unleaked() -> bool:
    banned = {w[::-1] for w in (
        "dirg", "draob", "tniop", "enil", "raenilloc", "ecittal", "rtemoeg",
        "epols", "enalp", "lanogaid", "nmuloc", "sodre", "yeneddud", "pmaknemmalf",
    )}
    src = open(__file__, encoding="utf-8").read().lower()
    leak = {w for w in banned if w in src}
    if leak:
        raise ValueError(f"leak: {sorted(leak)}")
    return True


if __name__ == "__main__":
    assert unleaked()
    print(certify(space(2), 2))                            # resolution 2: the whole space saturates
    eight = frozenset({1, 2, 4, 7, 8, 11, 13, 14})
    print(certify(eight, 4))                               # a saturated book at resolution 4
    a, b, c = 0, 1, 2                                      # one reading class at n=4
    w = alias_probe(a, b, 4)
    print(f"dual check: probe {w} reads {[reading(w, t, 4) for t in (a, b, c)]} "
          f"on a degenerate triple")
    print()
    print("theorem:", CEILING)
    print("frontier:", FRONTIER.contains)
    print()
    for bad in (
        lambda: the_law(frozenset({0, 1, 2}), 4),          # one class, three tokens
        lambda: saturated(frozenset({0, 1, 4}), 4),        # lawful != saturated
        lambda: in_space_only(frozenset({99}), 3),         # outside the space
        lambda: exact(frozenset({0.5})),                   # not a token
        lambda: Claim("it fits", ""),                      # vibes
        lambda: Frontier(contains="saturates for all n"),
        lambda: find(101),
    ):
        try:
            bad()
        except (AssertionError, ValueError, TypeError,
                Degenerate, NotImplementedError) as e:
            print("rejected:", type(e).__name__, e)
