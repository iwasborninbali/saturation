"""brief.py — the solver's campaign, v2. One target, two verbs, one currency.

You receive saturation.py and this file; nothing else exists for you: no
outside channels, no other modules, no guessing what the task is called —
a right guess changes nothing that certify would not settle. TARGET = 71.
Grow a lawful book toward 2 * TARGET = 142 tokens. Two verbs are yours:
seed (open a book from a principle — schedules, residues, recurrences,
whatever the structure itself suggests) and climb (one lawful move: add,
swap, drop). Cycles are for hypotheses, not wandering: every run should
answer a question you can state before it starts. Footholds are currency —
the ledger keeps your best size and its canon key, and several solvers can
share one ledger later. Your no is an answer, not a malfunction.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from itertools import combinations

from saturation import (TARGET, Claim, Degenerate, Foothold, canon, certify,
                        degenerate, exact, in_space_only, space, the_law)

ROLE = "solver"


# --- ONLY: the solver's ontology is one module ---

DEPS = frozenset({"saturation"})

def deps_only(imports: frozenset) -> frozenset:
    out = imports - DEPS
    if out:
        raise ValueError(sorted(out))
    return imports


# --- FORBIDDEN: channels that bypass certify ---

FORBIDDEN_DELIVERY = frozenset(
    {"prose", "unverified_claim", "identity_guess", "outside_lookup"})

def deliver(kind: str, payload):
    if kind in FORBIDDEN_DELIVERY:
        raise PermissionError(kind)
    return payload


# --- MUST: a submission certifies itself on construction ---

@dataclass(frozen=True)
class Submission:
    n: int
    book: frozenset
    certificate: Claim = field(init=False)

    def __post_init__(self):
        object.__setattr__(self, "certificate", certify(self.book, self.n))


# --- the toolkit: lawful moves are cheap to test ---

def admits(book: frozenset, t: int, n: int) -> bool:   # "may t join without breaking the law"
    if t in book:
        return False
    for a, b in combinations(book, 2):
        if degenerate(a, b, t, n):
            return False
    return True
# quadratic on purpose; making it cheaper is your end.


# --- EVIDENCE: the ledger remembers, dedups by canon, and never inflates ---

@dataclass
class Ledger:
    best: Foothold | None = None
    keys: set = field(default_factory=set)

    def log(self, f: Foothold) -> Claim:
        key = canon(f.book, f.n)
        fresh = key not in self.keys
        self.keys.add(key)
        if self.best is None or f.size > self.best.size:
            self.best = f
        return Claim(
            says=f"{f!r} fresh={fresh}",
            evidence="law re-verified on construction; canon key stored",
        )


# --- honest failure: a refusal carries its best evidence ---

class Exhausted(Exception):
    def __init__(self, best: Foothold, runs: int):
        self.best, self.runs = best, runs
        super().__init__(f"{best!r} after {runs} runs")


# --- JUDGMENT slots: the loop below is codable; these two are your end ---

def seed(n: int, rng: random.Random) -> frozenset:
    raise NotImplementedError("your end")

def climb(book: frozenset, n: int, rng: random.Random) -> frozenset:
    raise NotImplementedError("your end")


# --- the loop: every move re-enters through the law ---

def campaign(n: int, seed, climb, runs: int, patience: int,
             ledger: Ledger, rng_seed: int = 0) -> Submission:
    assert isinstance(runs, int) and runs > 0, "MUST: a finite budget"
    assert isinstance(patience, int) and patience > 0, "MUST: finite patience"
    rng = random.Random(rng_seed)
    for _ in range(runs):
        book = the_law(in_space_only(exact(seed(n, rng)), n), n)
        best, still = book, 0
        while still < patience:
            book = the_law(climb(book, n, rng), n)   # an unlawful move crashes: use admits
            if len(book) > len(best):
                best, still = book, 0
            else:
                still += 1
            if len(best) == 2 * n:
                ledger.log(Foothold(n=n, book=best))
                return Submission(n=n, book=best)
        ledger.log(Foothold(n=n, book=best))
    raise Exhausted(ledger.best, runs)


if __name__ == "__main__":
    # a deliberately dumb brain — proves the mechanics precede the intelligence
    def naive_seed(n, rng):
        return frozenset({rng.randrange(n * n)})

    def naive_climb(book, n, rng):
        pool = rng.sample(sorted(space(n)), min(6 * n, n * n))
        for t in pool:
            if admits(book, t, n):
                return book | {t}
        if len(book) > 2:
            return book - {rng.choice(sorted(book))}
        return book

    ledger = Ledger()
    sub = campaign(5, naive_seed, naive_climb, runs=40, patience=60,
                   ledger=ledger, rng_seed=2)
    print("campaign n=5:", sub.certificate)

    ledger12 = Ledger()
    try:
        campaign(12, naive_seed, naive_climb, runs=2, patience=25,
                 ledger=ledger12, rng_seed=1)
    except Exhausted as e:
        print("campaign n=12 refused with evidence:", e)

    print()
    for bad in (
        lambda: Submission(n=4, book=frozenset({0, 1, 2, 3, 4, 5, 6, 7})),
        lambda: deliver("outside_lookup", "let me just check one thing"),
        lambda: deps_only(frozenset({"saturation", "requests"})),
        lambda: campaign(3, naive_seed, naive_climb, 0, 1, Ledger()),
        lambda: seed(3, random.Random(0)),
        lambda: Foothold(n=4, book=frozenset({0, 1, 2})),
    ):
        try:
            bad()
        except (AssertionError, ValueError, PermissionError,
                Degenerate, NotImplementedError) as e:
            print("rejected:", type(e).__name__, e)
