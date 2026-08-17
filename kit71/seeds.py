"""seeds.py — one opening, offered not imposed. Better principles are your end.

The opening below is algebra, not search: at prime resolution p, the book
{ i*p + (i*i mod p) : 0 <= i < p } is lawful — an affine relation among three
of its tokens would force two indices equal modulo p, and a degree-2 schedule
cannot serve three. TARGET = 71 is prime, so the opening lands natively:
size 71, shortfall 71, for zero cycles. The family generator widens the idea;
which parameters climb past size 71 is unwritten. Hunt there.
"""

from __future__ import annotations

from saturation import (TARGET, Book, Degenerate, Foothold, exact,
                        in_space_only, motions, the_law)


def quadratic_opening(p: int = TARGET) -> Book:
    return frozenset(i * p + (i * i) % p for i in range(p))
# lawful by algebra; re-proven below by running the law — gifts arrive certified.


def residue_family(n: int, a: int, b: int, c: int, q: int) -> Book:
    # degree-2 schedule over modulus q, kept only where it lands inside the space
    return frozenset(i * n + (a * i * i + b * i + c) % q
                     for i in range(n) if (a * i * i + b * i + c) % q < n)


def closure(reps: Book, chosen: tuple, n: int) -> Book:
    # produce a fixed book from a wedge: close representatives under chosen motions
    book = set(reps)
    while True:
        grown = book | {g(t) for g in chosen for t in book}
        if grown == book:
            return frozenset(book)
        book = grown


if __name__ == "__main__":
    opening = the_law(in_space_only(exact(quadratic_opening()), TARGET), TARGET)
    print(Foothold(n=TARGET, book=opening), "— the opening, certified by this run")

    fam = residue_family(TARGET, 1, 3, 5, 73)
    try:
        the_law(in_space_only(exact(fam), TARGET), TARGET)
        print(f"family(1,3,5,73): lawful, size {len(fam)}")
    except Degenerate as no:
        print(f"family(1,3,5,73): size {len(fam)}, refused with witness {no.args[0]}")

    swap = (motions(6)[4],)
    print("closure of {0, 1} under swap at n=6:", sorted(closure(frozenset({0, 1}), swap, 6)))
