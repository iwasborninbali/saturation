"""principles_no3.py — what we learned about saturation, written as executable prose.

Method (principles.py of the owner): a sentence of prose becomes a construct by its Kind — a MUST is an
assert, a FORBIDDEN raises, an EVIDENCE is a Claim that must carry its proof, a JUDGMENT is an honest
NotImplementedError, a SYMBOL is a None that must stay None.  Module level proves the laws that held
(PROOFS); __main__ proves the breaches and runs the edge tests.  The tests use the law itself
(saturation.py, v1) and a compact pure-Python search that embodies the search principles; where a
test needs the C searcher (there.c) it is skipped when the binary is absent.

Everything here is measured, not believed.  Where we do not know, the file says "your end".
"""

from __future__ import annotations

import os
import random
import subprocess
import sys
from dataclasses import dataclass, field
from enum import Enum
from itertools import combinations
from math import gcd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import saturation as S  # the law; nothing else is imported from the project on purpose


# --- kinds and the translator (both directions) ---------------------------------------------

class Kind(str, Enum):
    MUST = "must"
    FORBIDDEN = "forbidden"
    ONLY = "only"
    EVIDENCE = "evidence"
    JUDGMENT = "judgment"
    SYMBOL = "symbol"
    DEFAULT = "default"


TO_CONSTRUCT = {
    Kind.MUST:      "assert <phi>, '<says>'",
    Kind.FORBIDDEN: "if <act>: raise Violation('<says>')",
    Kind.ONLY:      "assert actual - allowed == set()   # <says>",
    Kind.EVIDENCE:  "Claim(says='<says>', evidence='<how it was checked>')",
    Kind.JUDGMENT:  "def <name>(...): raise NotImplementedError('your end')   # <says>",
    Kind.SYMBOL:    "<name>: None = None   # <says>; set it -> raise",
    Kind.DEFAULT:   "def f(x='<the prior>')   # <says>",
}
TO_PROSE = {                                     # the reverse move: construct -> sentence template
    "assert": Kind.MUST, "raise Violation": Kind.FORBIDDEN, "- allowed == set()": Kind.ONLY,
    "Claim(": Kind.EVIDENCE, "NotImplementedError": Kind.JUDGMENT, ": None = None": Kind.SYMBOL,
    "def f(x=": Kind.DEFAULT,
}
PROSE_TEMPLATE = {
    Kind.MUST: "It must hold that {says}.",
    Kind.FORBIDDEN: "It is forbidden to {says}.",
    Kind.ONLY: "Only {says} are allowed.",
    Kind.EVIDENCE: "We claim that {says}; the evidence is: {evidence}.",
    Kind.JUDGMENT: "Whether {says} is not decided here; it is decided at the other end.",
    Kind.SYMBOL: "{says} — this stays open, on purpose.",
    Kind.DEFAULT: "Unless said otherwise, {says}.",
}


def to_python(kind: Kind, says: str) -> str:
    return TO_CONSTRUCT[kind].replace("<says>", says)


def to_prose(construct: str, says: str, evidence: str = "") -> str:
    for marker, kind in TO_PROSE.items():
        if marker in construct:
            return PROSE_TEMPLATE[kind].format(says=says, evidence=evidence or "—")
    raise ValueError(f"no kind recognised in construct: {construct!r}")


# --- evidence carries its proof; a hole is honest ---------------------------------------------

@dataclass(frozen=True)
class Claim:
    says: str
    evidence: str

    def __post_init__(self) -> None:
        if not self.evidence:
            raise ValueError(f"vibes: {self.says}")


class Hole:
    """a named gap: what we do not know, and what would close it (a JUDGMENT with a door)"""

    def __init__(self, name: str, question: str, would_close: str) -> None:
        if not would_close:
            raise ValueError("a hole without a door is despair, not a question")
        self.name, self.question, self.would_close = name, question, would_close

    def answer(self):
        raise NotImplementedError(f"{self.name}: your end — {self.question}")

    def __repr__(self) -> str:
        return f"Hole({self.name}: {self.question} | closes with: {self.would_close})"


# --- the small pure-Python search that embodies the search principles -------------------------

def line_cells(p, q, n):
    """all cells of the space on the line through p and q (registers)"""
    (u1, v1), (u2, v2) = p, q
    du, dv = u2 - u1, v2 - v1
    g = gcd(abs(du), abs(dv)); du //= g; dv //= g
    out = []
    u, v = u1, v1
    while 0 <= u < n and 0 <= v < n:
        out.append((u, v)); u -= du; v -= dv
    u, v = u1 + du, v1 + dv
    while 0 <= u < n and 0 <= v < n:
        out.append((u, v)); u += du; v += dv
    return out


def enumerate_books(n, fixed=(), forbid=(), limit=None):
    """Complete search for saturated books (2 per row and column, no degenerate triple), pure Python.
    Principles embodied: shading (every chosen pair kills its line), fail-first (most constrained class),
    sibling exclusion (a tried candidate is dead for its siblings, so the search is complete)."""
    dead = [[0] * n for _ in range(n)]
    for (u, v) in forbid: dead[u][v] += 1
    rowc, colc = [0] * n, [0] * n
    chosen = []
    found = []

    def take(p):
        u, v = p
        for q in chosen:
            for (a, b) in line_cells(p, q, n): dead[a][b] += 1
        dead[u][v] += 1; rowc[u] += 1; colc[v] += 1; chosen.append(p)

    def untake():
        p = chosen.pop(); u, v = p
        rowc[u] -= 1; colc[v] -= 1; dead[u][v] -= 1
        for q in chosen:
            for (a, b) in line_cells(p, q, n): dead[a][b] -= 1

    def alive(u, v):
        return dead[u][v] == 0 and rowc[u] < 2 and colc[v] < 2

    for p in fixed: take(p)

    def rec():
        if limit is not None and len(found) >= limit: return
        if len(chosen) == 2 * n:
            found.append(frozenset(u * n + v for (u, v) in chosen)); return
        best, bestcnt = None, 10 ** 9
        for u in range(n):
            need = 2 - rowc[u]
            if need <= 0: continue
            cnt = sum(1 for v in range(n) if alive(u, v))
            if cnt < need: return
            if cnt < bestcnt: best, bestcnt = ("row", u), cnt
        for v in range(n):
            need = 2 - colc[v]
            if need <= 0: continue
            cnt = sum(1 for u in range(n) if alive(u, v))
            if cnt < need: return
            if cnt < bestcnt: best, bestcnt = ("col", v), cnt
        if best is None: return
        kind, i = best
        cands = [(i, v) for v in range(n) if alive(i, v)] if kind == "row" else [(u, i) for u in range(n) if alive(u, i)]
        marks = []
        for c in cands:
            if alive(*c):
                take(c); rec(); untake()
            dead[c[0]][c[1]] += 1; marks.append(c)          # sibling exclusion: c is settled
        for (a, b) in marks: dead[a][b] -= 1

    rec()
    return found


def canonical(book, n):
    m = n - 1
    fs = [lambda u, v: (u, v), lambda u, v: (v, m - u), lambda u, v: (m - u, m - v), lambda u, v: (m - v, u),
          lambda u, v: (m - u, v), lambda u, v: (u, m - v), lambda u, v: (v, u), lambda u, v: (m - v, m - u)]
    return min(tuple(sorted(f(t // n, t % n)[0] * n + f(t // n, t % n)[1] for t in book)) for f in fs)


# --- the principles ---------------------------------------------------------------------------

A000769 = {2: 1, 3: 1, 4: 4, 5: 5, 6: 11, 7: 22, 8: 57}       # books up to the eight motions


def p_search_is_complete() -> Claim:
    """EVIDENCE: shading + fail-first + sibling exclusion enumerate every book (checked against A000769)."""
    for n, known in A000769.items():
        books = enumerate_books(n)
        for b in books: S.saturated(b, n)                    # every book passes the law
        classes = {canonical(b, n) for b in books}
        assert len(classes) == known, (n, len(classes), known)
    return Claim("the search principles are complete for n <= 8",
                 "pure-Python enumeration matches A000769 for n=2..8 and every book passes the law")


def p_modular_arcs_are_lawful() -> Claim:
    """EVIDENCE: the parabola over F_p is a lawful book of size p (Erdős); it uses no integer slack."""
    for p in (5, 7, 11, 13):
        book = frozenset(x * p + (x * x % p) for x in range(p))
        S.the_law(book, p)
    return Claim("{(x, x^2 mod p)} is lawful for primes p (size p, half of the ceiling)",
                 "checked with the law for p=5,7,11,13")


def p_segre_wall() -> Claim:
    """EVIDENCE: modulo p no three-free set beats p+1 points (arcs of AG(2,p)); so mod-p algebra caps near n."""
    def collinear_mod(a, b, c, p):
        return ((b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])) % p == 0
    for p in (3, 5):
        pts = [(u, v) for u in range(p) for v in range(p)]
        best = 0
        # exhaustive: largest subset with no three collinear mod p (small p only)
        def rec(start, chosen):
            nonlocal best
            best = max(best, len(chosen))
            for i in range(start, len(pts)):
                c = pts[i]
                if all(not collinear_mod(a, b, c, p) for a, b in combinations(chosen, 2)):
                    rec(i + 1, chosen + [c])
        rec(0, [])
        assert best == p + 1, (p, best)
    return Claim("a set with no three collinear modulo p has at most p+1 points (Segre); mod-p constructions cap near n",
                 "exhaustive maximum arc size p+1 for p=3,5 in AG(2,p); Segre's theorem for the general statement")


def p_books_use_integer_slack() -> Claim:
    """EVIDENCE: saturated books contain triples that ARE collinear modulo small primes — they live in the slack."""
    n = 8
    books = enumerate_books(n, limit=5)
    for b in books:
        pts = [divmod(t, n) for t in b]
        for p in (2, 3, 5, 7):
            bad = sum(1 for a, c, d in combinations(pts, 3)
                      if ((c[0] - a[0]) * (d[1] - a[1]) - (c[1] - a[1]) * (d[0] - a[0])) % p == 0)
            assert bad > 0, (p,)
    return Claim("every saturated book (n=8, first five found) has triples collinear mod 2,3,5,7 — it is not an arc mod any small prime",
                 "counted the triples with determinant ≡ 0 mod p")


def p_balance_lemma() -> Claim:
    """EVIDENCE: relative to a group with a column->row motion, defect pairs form an Eulerian digraph; a lone pair is diagonal.
    Uses the C searcher (rot4 orbits + one fixed half-turn pair, exhaustive); skipped honestly if it is absent."""
    binary = os.path.join(HERE, "there")
    if not os.path.exists(binary):
        return Claim("a rot4-symmetric-except-one-pair book must have that pair on a long diagonal (rct4)",
                     "proof only (searcher absent here): each rot4 orbit puts equally many points in row a and column a, "
                     "so a lone pair adds 1 to row a and 0 to column a unless it lies on a diagonal")
    n, m = 17, 16
    def count(a, b):
        out = subprocess.run([binary, str(n), "2", "1", "60"], capture_output=True, text=True,
                             env=dict(os.environ, ALL="1", PAIRS=f"{a},{b}")).stdout
        return int(out.rsplit("solutions=", 1)[1].split()[0])
    off = sum(count(a, b) for (a, b) in ((1, 4), (2, 7), (3, 5), (0, 9), (5, 11)))
    on = sum(count(i, i) for i in range(m // 2))
    assert off == 0, "an off-axis lone pair admitted a book — the lemma would be false"
    assert on == 2, on                                     # Flammenkamp: one rct4 class at n=17 (two labelled books)
    return Claim("a rot4-symmetric-except-one-pair book must have that pair on a long diagonal (rct4)",
                 "n=17: five off-axis pair positions -> 0 books; all diagonal positions -> 2 labelled books (= the one "
                 "rct4 class of the table); proof: each rot4 orbit puts equally many points in row a and column a")


def p_locally_rigid() -> Claim:
    """EVIDENCE: dropping k points of a book and re-completing exactly returns only the book itself (n=8, k<=6)."""
    n = 8
    b = enumerate_books(n, limit=1)[0]
    pts = sorted(divmod(t, n) for t in b)
    rng = random.Random(3)
    for k in (2, 4, 6):
        for _ in range(4):
            drop = set(rng.sample(pts, k))
            keep = [p for p in pts if p not in drop]
            comp = enumerate_books(n, fixed=keep)
            assert comp == [b] or set(comp) == {b}, (k, len(comp))
    return Claim("a saturated book is locally rigid: no other completion after dropping up to 6 of 16 points (n=8)",
                 "exact re-completion with the fixed remainder, 12 random drops")


def p_no_lift_between_sizes() -> Claim:
    """EVIDENCE: a book of size n shifted into n+2 has no completion — neighbouring sizes do not correlate."""
    n = 6
    for b in enumerate_books(n)[:10]:
        shifted = [(u + 1, v + 1) for (u, v) in (divmod(t, n) for t in b)]
        comp = enumerate_books(n + 2, fixed=shifted)
        assert comp == [], comp
    return Claim("no book of size 8 contains a shifted book of size 6 (first ten checked)",
                 "exact completion search with the shifted book fixed")



def p_free_pairs_are_eulerian() -> Claim:
    """EVIDENCE (partner): in every half-turn-symmetric book, the pairs {p, rot2 p} that belong neither to a quarter-turn
    orbit nor to a swap (dia2) orbit nor to a long diagonal — in any DISJOINT decomposition into such pieces — form an
    Eulerian digraph on the row classes {i, m-i} (arc x->y for the pair {(x,y),(m-x,m-y)}): in-degree = out-degree.  This is the balance lemma applied
    with the quarter-turn group, minus the (balanced) swap orbits and loops.  Checked on every rot2 book at n=9 and 11 with
    the C searcher; skipped honestly if it is absent."""
    binary = os.path.join(HERE, "there")
    if not os.path.exists(binary):
        return Claim("free pairs of a half-turn-symmetric book form an Eulerian digraph on the row classes",
                     "proof only (searcher absent here): quarter-turn orbits, swap orbits and diagonal pairs are each balanced "
                     "between row a and column a; every row and column holds exactly two points; hence the remaining pairs are balanced")
    checked = 0
    for n in (9, 11):
        m = n - 1
        out = subprocess.run([binary, str(n), "1", "1", "120"], capture_output=True, text=True,
                             env=dict(os.environ, ALL="1", PRINTALL="1")).stdout
        for line in out.splitlines():
            if not line.startswith("sol"): continue
            pts = {divmod(int(t), n) for t in line.split()[1:]}
            S.saturated(frozenset(u * n + v for (u, v) in pts), n)
            pairs = {frozenset({(u, v), (m - u, m - v)}) for (u, v) in pts}
            used = set(); indeg, outdeg = {}, {}
            for pr in sorted(pairs, key=min):                                        # a DISJOINT decomposition
                if pr in used: continue
                (u, v) = min(pr)
                if u == v or u + v == m: used.add(pr); continue                     # loop: balanced
                rp = frozenset({(v, m - u), (m - v, u)}); dp = frozenset({(v, u), (m - v, m - u)})
                if rp in pairs and rp not in used: used |= {pr, rp}; continue       # quarter-turn orbit: balanced
                if dp in pairs and dp not in used: used |= {pr, dp}; continue       # swap orbit: balanced
                used.add(pr)                                                        # free pair: an arc
                x, y = min(u, m - u), min(v, m - v)
                outdeg[x] = outdeg.get(x, 0) + 1; indeg[y] = indeg.get(y, 0) + 1
            for c in set(indeg) | set(outdeg):
                assert indeg.get(c, 0) == outdeg.get(c, 0), (n, c, indeg, outdeg)
            checked += 1
    assert checked == 28 + 120, checked                                            # all rot2 books at n=9 and 11
    return Claim("free pairs of a half-turn-symmetric book form an Eulerian digraph on the row classes",
                 f"all {checked} rot2 books at n=9, 11 (labelled): in-degree = out-degree at every row class; "
                 "proof: quarter-turn orbits, swap orbits and diagonal pairs are balanced between row a and column a")

PRINCIPLES = (p_search_is_complete, p_modular_arcs_are_lawful, p_segre_wall,
              p_books_use_integer_slack, p_balance_lemma, p_locally_rigid, p_no_lift_between_sizes,
              p_free_pairs_are_eulerian)

MEASURED = (
    Claim("the cost of one saturated book grows ×8–10 per +4 in n (rot4/rct4) and ×6 per +2 (rot2)",
          "bench/: rot4 n=36: 10–60 s, 40: 70 s; rct4 41: 806 s, 43: 6.7 core-h; rot2 24: 10 s, 27: 137 s (8 seeds)"),
    Claim("plain local search on exactly 2n points dies from n≈12–28; large partial books are easy (134 at n=71)",
          "deadends/walk.c, kit71/fast/sa.c and mc.c; kit71/results/ledger.json"),
    Claim("the mixed families (C4 orbits + at least one V2 quadruple, + a loop for odd n) are empty for n<=23 and no book was found up to 33",
          "kit71 exhaustive lists n<=23; there.c sym 11 with NV2>=1, 8 seeds up to 500 s at n=21..33"),
    Claim("the 3-cycle defect family has books at n=13,17,33,37,39 and none at 15,19,21,23,25; the two-loop family has 2/1/1 books at n=24/26/28 and none for 14..22",
          "kit71/bench/cycle3_summary.txt, family sweeps; bench/twoloop_*; paper tables"),
)

FORBIDDEN = frozenset({
    "report a book that has not passed saturation.certify",
    "call a configuration 'first known' without the table check (state, date) written down",
    "spend cluster money on 71/78 with the present tools (10^5–10^7 core-hours by our own curve)",
})


class Violation(Exception): ...


def deliver(act: str):
    if act in FORBIDDEN:
        raise Violation(act)
    return act


HOLES = (
    Hole("mixed-empty", "why are the mixed C4/V2 defect families empty (n<=23 exhaustively)?",
         "a counting or geometric argument like the balance lemma — or a book that shows they are not"),
    Hole("beyond-3/2", "a construction with more than 3n/2 - o(n) points for infinitely many n",
         "a family of sets living in the integer slack (collinear mod every prime, not in Z^2) with a proof; the "
         "candidate must fail p_segre_wall's premise: it must NOT be an arc modulo any prime for large n"),
    Hole("why-symmetric-dense", "why do rot4/rct4 books exist far beyond the probabilistic heuristic's range?",
         "known half-answer (Flammenkamp): in rotational classes a pair blocks only ~C log n cells against ~n in axis "
         "classes; still missing: a second-moment/orbit-level count that reproduces the measured class counts"),
    Hole("davies-619", "how were 619 iden/rot2 books for n=21..57 'constructed' in July 2026 (database entry)?",
         "the method is undocumented anywhere (deep research 2026-08-18); perturbation of known books is refuted by "
         "p_locally_rigid at n=41 (relax.py, relax0.py); door: ask Flammenkamp"),
    Hole("integer-slack", "a set beating 3n/2 that lives in the integer slack (Green's question, arXiv 2607.05255 rem. 1.2)",
         "greedy lawful subsets of the hyperbola xy=c mod p in a 3p x 3p grid reach only 1.0-1.26 n (this file's sibling "
         "experiment); door: an exact maximum-lawful-subset search on structured sets, or a CRT gluing of arcs"),
)

# --- what stays open ---------------------------------------------------------------------------

class Frontier:
    def __init__(self, contains: None = None):
        if contains is not None:
            raise ValueError("a frontier with content is a submission, not a fact")
        self.contains = None


WHICH_N_SATURATE = Frontier()                    # known: all n<=70, 72, 74, 76; open: 71, 73, 75, >=77 — recorded elsewhere, not here


# --- module level: the laws that held (import fails otherwise) ------------------------------------

PROOFS = tuple(p() for p in PRINCIPLES)


if __name__ == "__main__":
    for c in PROOFS: print("held:", c.says)
    for c in MEASURED: print("measured:", c.says)
    print()
    print("translator:", to_python(Kind.MUST, "every triple keeps full rank"))
    print("translator:", to_prose("assert phi", "every triple keeps full rank"))
    print()
    for h in HOLES:
        try:
            h.answer()
        except NotImplementedError as e:
            print("hole:", e)
    print()
    for bad in (
        lambda: Claim("it works", ""),
        lambda: deliver("report a book that has not passed saturation.certify"),
        lambda: Frontier(contains="all n"),
        lambda: Hole("x", "why?", ""),
    ):
        try:
            bad()
        except (ValueError, Violation) as e:
            print("rejected:", type(e).__name__, e)
