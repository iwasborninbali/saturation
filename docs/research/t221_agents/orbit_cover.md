# T2.21 task A: the (7,5,3,1) orbit-cover lemma, k = -1 — verified for every prime 11 ≤ p ≤ 500

Setting as in `slack/lp1_anatomy.py` / `slack/lp1_types.py` and `docs/research/pair_bound_notes.md` §24
and B.19 (addendum (a)–(c), lines ~962–1035): p odd prime, h = (p−1)/2,

```
P = { (x,y) ∈ [-h, 3h+1] × [0, 2p-1] : xy mod p ∈ {1, p-1} }
```

(lifts of the two hyperbolae xy ≡ 1 and xy ≡ −1 mod p into the 2p×2p box). Lines: rows (`r`,y), columns
(`c`,x), slope+1 diagonals (`d`, x−y, exact integer, not reduced mod p), slope−1 antidiagonals (`a`, x+y).
A slope-(+1) **residue group** `G_d` (d ∈ Z/pZ) is the union of all diagonals with x−y ≡ d (mod p); its
**type** is the sorted-descending tuple of sizes of its (≥1‑point) integer diagonals. This note checks the
**orbit-cover lemma** for every group of type (7,5,3,1), stated and numerically spot-checked for p =
113,137,199 in B.19 point 2 and its addendum (a)–(b); here it is checked exhaustively for all such groups
at every prime 11 ≤ p ≤ 500.

Code: `slack/t221_agents/orbit_cover.py`. Environment: **`/Users/iwasborninbali/venvs/sat/bin/python3`**
(numpy 2.5.2, scipy 1.18.0, `linprog(..., method='highs')`) — the bare `python3` on this machine has no
numpy/scipy installed, so this exact interpreter path is required to reproduce the run. Full run:

```
/Users/iwasborninbali/venvs/sat/bin/python3 slack/t221_agents/orbit_cover.py 11 500
```

Wall-clock **5.3 s** for all 91 primes (91 = π(500) − π(10), all primes 11..500, no sampling was needed —
the "all primes ≤ 300 plus a sample above" fallback in the task was not required). Outputs:
`slack/t221_agents/orbit_cover_output.txt` (the p,m8,m7,m6groups,orbits,LP28,exceptions table) and
`slack/t221_agents/orbit_cover_detail.json` (per-orbit facts, machine-readable, ~800 KB).

## 1. Result in one line

**837 orbits checked across 91 primes (11 ≤ p ≤ 500, all of them). Zero exceptions.** Every single orbit
satisfies |Ω|=64, closure under rows/columns, LP(Ω) = 28 exactly, and the 12-line+4-point integral cover
is an **exact partition** of Ω (not just a cover) — including the two specific structural questions the
task asked to pin down:

* **Does the 7-line of `G_d` meet a line of `G'_d` or `G'_{-d}`?** Checked exhaustively, itemised pair by
  pair: all 3 sizes {7,5,3} of `G_d` against all 3 sizes {7,5,3} of each of `G'_d`, `G'_{-d}` (3×2×3 = 18
  pairs per orbit, 837×18 = 15,066 pairs total): **never** — zero shared points in every case. (`G_{-d}`'s
  three lines against the primed groups were not itemised the same way, but their disjointness is still
  fully covered — see the union-size argument in §5(c), which certifies all 12 lines pairwise disjoint,
  `G_{-d}` included.)
* **Are the four 1-point-line points exactly the points of Ω not on any of the 12 lines?** **Yes, in all
  837 orbits, exactly** (`Ω \ (12 lines) = {the 4 singleton points}`, both directions verified as a set
  equality, not just a size match).

## 2. Definitions used (closed form for Ω, and the ± pairing)

`lp1_anatomy.py`'s dual-symmetrisation machinery defines the slope-(−1) group "at residue d" as
`G'_d := R(G_{-d})` where `R:(x,y)↦(p-x,y)` (since `R` sends the diagonal x−y=c to the antidiagonal
x+y=p−c, i.e. `R(G_c) = G'_{-c}`; see B.19 addendum (a)). Unwinding this, for the orbit

```
Ω_d := G_d ∪ G_{-d} ∪ G'_d ∪ G'_{-d}
```

both the "own" diagonal and the "own" antidiagonal parts collapse to the **same** residue pair {d, −d mod
p}, giving a closed form used directly by the code (no R/R′ bookkeeping needed):

```
Ω_d = { q ∈ P : (x-y) mod p ∈ {d, -d mod p} }  ∪  { q ∈ P : (x+y) mod p ∈ {d, -d mod p} }
```

**Fact checked first (before building any orbit):** type(G_d) = type(G_{-d}) always, for every d with
type(G_d) = (7,5,3,1), at every one of the 91 primes — i.e. the m7 residues of this type (m7 = the count
used by `lp1_types.py`'s `B_t` column, one per residue d) always pair up d ↔ −d with **no** self-paired
residue (d ≡ −d mod p, i.e. d = 0, never has this type) and **no** mismatched partner. Consequently m7 was
even at all 91 primes and **#orbits = m7/2** exactly, with zero pairing exceptions — this is exactly the
"all four groups share the same type" fact of B.19 addendum (a) (RR′ maps `G_d` onto `G_{-d}`), now
verified as an unconditional census rather than inferred from the symmetry argument alone.

## 3. Per-p counts and orbit checks (full table)

m7, m8, m6groups all count **(+1)-groups one per residue d** (the `B_t` convention of `lp1_types.py`,
i.e. both d and −d of a pair are counted separately — matching the B.19 census columns exactly, see §4).
`orbits` = m7/2 = number of distinct {d,−d} pairs actually tested; `LP28` = number of those orbits with
LP(Ω) = 28.000 to 1e-6; `exc` = number failing any check in §1 of the task (i)–(iv), including pairing
issues. Reproduced verbatim from `slack/t221_agents/orbit_cover_output.txt`:

```
    p   n_pts   m8   m7  m6grp  orbits  LP28  exc
   11      80    2    0      0       0     0    0
   13      96    0    0      1       0     0    0
   17     128    0    0      1       0     0    0
   19     144    2    0      2       0     0    0
   23     176    2    2      0       1     1    0
   29     224    4    2      3       1     1    0
   31     240    2    2      2       1     1    0
   37     288    4    2      3       1     1    0
   41     320    2    0      3       0     0    0
   43     336    6    4      0       2     2    0
   47     368    6    2      2       1     1    0
   53     416    4    2      3       1     1    0
   59     464    4    4      6       2     2    0
   61     480    2    8      7       4     4    0
   67     528    6    6      4       3     3    0
   71     560    8    4      4       2     2    0
   73     576    4    8      5       4     4    0
   79     624    8    2      8       1     1    0
   83     656    6   10      4       5     5    0
   89     704   10    2      5       1     1    0
   97     768    6    4      7       2     2    0
  101     800    8    8      9       4     4    0
  103     816    6   10      8       5     5    0
  107     848   10   14      2       7     7    0
  109     864    8    4     13       2     2    0
  113     896    8   10     11       5     5    0
  127    1008    8   16      6       8     8    0
  131    1040   10    8     14       4     4    0
  137    1088   12   12     13       6     6    0
  139    1104   10   10     14       5     5    0
  149    1184   12    6     15       3     3    0
  151    1200   16   10     10       5     5    0
  157    1248   12    6     15       3     3    0
  163    1296   14   10     16       5     5    0
  167    1328   16   12     12       6     6    0
  173    1376   14   20     15      10    10    0
  179    1424   12   12     20       6     6    0
  181    1440   12   16     21       8     8    0
  191    1520   20    8     18       4     4    0
  193    1536   16   12     21       6     6    0
  197    1568   18   12     19       6     6    0
  199    1584   16   10     22       5     5    0
  211    1680   14   20     18      10    10    0
  223    1776   24   10     20       5     5    0
  227    1808   14   18     24       9     9    0
  229    1824   22    6     21       3     3    0
  233    1856   16   20     13      10    10    0
  239    1904   22   16     20       8     8    0
  241    1920   14   26     25      13    13    0
  251    2000   20   18     24       9     9    0
  257    2048   26   18     17       9     9    0
  263    2096   26   20     18      10    10    0
  269    2144   20   28     25      14    14    0
  271    2160   28   18     20       9     9    0
  277    2208   26   28     19      14    14    0
  281    2240   20   20     25      10    10    0
  283    2256   20   34     16      17    17    0
  293    2336   24   26     31      13    13    0
  307    2448   18   36     22      18    18    0
  311    2480   22   18     36       9     9    0
  313    2496   20   26     23      13    13    0
  317    2528   26   24     23      12    12    0
  331    2640   34   14     34       7     7    0
  337    2688   22   24     31      12    12    0
  347    2768   24   34     28      17    17    0
  349    2784   26   28     35      14    14    0
  353    2816   30   20     27      10    10    0
  359    2864   38   18     32       9     9    0
  367    2928   28   40     22      20    20    0
  373    2976   32   34     23      17    17    0
  379    3024   36   28     30      14    14    0
  383    3056   36   30     28      15    15    0
  389    3104   34   38     33      19    19    0
  397    3168   36   24     29      12    12    0
  401    3200   32   30     35      15    15    0
  409    3264   24   38     39      19    19    0
  419    3344   40   30     34      15    15    0
  421    3360   30   34     33      17    17    0
  431    3440   30   42     34      21    21    0
  433    3456   34   26     37      13    13    0
  439    3504   34   30     44      15    15    0
  443    3536   34   42     34      21    21    0
  449    3584   38   38     37      19    19    0
  457    3648   34   34     33      17    17    0
  461    3680   32   36     37      18    18    0
  463    3696   34   42     38      21    21    0
  467    3728   38   40     38      20    20    0
  479    3824   38   40     40      20    20    0
  487    3888   34   46     40      23    23    0
  491    3920   32   40     50      20    20    0
  499    3984   40   34     50      17    17    0

TOTALS: primes=91, orbits_checked=837, LP=28 count=837, exceptions=0, primes with ≥1 exception=0
```

Five small primes (11,13,17,19,41) have **no** (7,5,3,1) group at all (m7 = 0 — h is too small there for a
7-point diagonal to occur among the realised residues); this is vacuous non-existence, not an exception.
The smallest p with a (7,5,3,1) group is **p = 23** (m7=2, 1 orbit, checked, LP=28).

## 4. Cross-checks against the existing notes (independent confirmation of the pipeline)

* **B.19 point 1 census**, exact match: p=113 → m8=8, m7=10, m6groups=11 (notes: "(8,4,4): 8, (7,5,3,1):
  10, (6,6,2,2): 11"); p=137 → 12,12,13 (notes: "12, 12, 13"); p=199 → 16,10,22 (notes: "16, 10, 22").
* **B.19 addendum (b)**, exact match: "(7,5,3,1)-orbits (64 points): LP(Ω) = 28 ... for ALL ten orbits at
  p=113" — this note's "ten" counts the 10 residues (=m7), i.e. each of the 5 distinct orbits was
  (redundantly) checked once per member of its {d,−d} pair; here each orbit is checked once, and all 5
  give LP=28, in agreement.
* **§24 densities** (primes 200 ≤ p ≤ 500, independently reproduced from this run's own data): m8/p =
  0.0795 (§24: 0.0795), m7/p = 0.0800 (§24: 0.0800), 2·m6groups/p = 0.1670 (§24's "m6" counts *lines*, two
  per (6,6,2,2) group, so it's 2×m6groups here; §24: 0.1677) — matches to within the expected fluctuation
  §24 itself reports.

These three independent matches (exact small-p census, exact LP values, and aggregate density) confirm the
point-set/type-classification/LP pipeline in `orbit_cover.py` reproduces the established machinery
correctly, on top of the 837/837 pass rate.

## 5. The structure of the cover (so a proof can be built on it)

This is the part of the task asking to pin down *which lines cover which points*. All of the following
were checked, without exception, on all 837 orbits (46,872 = 837×56 individual line-capacity constraints
built and solved across the orbits' LPs alone, §6):

**(a) The four constituent groups are pairwise disjoint as point sets.** Each of `G_d`, `G_{-d}`, `G'_d`,
`G'_{-d}` has 7+5+3+1 = 16 points (its own type), and |Ω_d| = 64 = 4×16 exactly in every case — so there is
**no** overlap between the four groups of a single orbit. (This is a different, stronger statement than
B.19 addendum (c), which is about pairs of *different* orbits Ω_d, Ω_e sharing points through a class that
lies in two different +1/−1 groups — that overlap phenomenon is real and unaffected by this note, see §7
below; within one orbit the four groups never overlap.)

**(b) Ω_d is a union of exactly 16 full rows and 16 full columns of P, each of size exactly 4** (16×4 = 64,
both ways). This is strictly stronger than the closure property asked for in (i): not only does every
row/column meeting Ω contain none of its points outside Ω, but every such row/column has **exactly** 4
points, uniformly, in all 837 orbits (13,392 = 837×16 row-checks and 837×16 column-checks, size 4 in every
single one — no row or column of any orbit ever has 3, 5, or 6 points). Rows and columns are therefore two
different exact 16×4 partitions of the same 64 points.

**(c) The twelve size-(7,5,3) lines of the four groups exactly partition 60 of the 64 points.** Checked two
ways: (1) the union of the 12 point-sets has exactly 60 elements = the sum of the 12 sizes (so no pair of
the 12 lines shares a point); (2) direct pairwise intersection of every {7,5,3}-line of `G_d`/`G_{-d}`
against every {7,5,3}-line of `G'_d`/`G'_{-d}` is empty (lines within the same slope family are
automatically disjoint — different exact diagonals/antidiagonals never meet — so the only possible
coincidence is a slope+1 line of `G_d`/`G_{-d}` crossing a slope−1 line of `G'_d`/`G'_{-d}` at a single
lattice point; this was checked explicitly for all 18 such cross-family pairs per orbit and never occurs).
In particular: **the 7-line of `G_d` never meets any line of `G'_d` or `G'_{-d}`** (nor does the 5- or
3-line) — this answers the task's specific question directly.

**(d) The remaining 4 points of Ω are exactly the four 1-point-line points, one per group.** `Ω \ (union of
the 12 lines)` was computed directly (not inferred from the size count 64−60=4) and compared as a *set* to
`{singleton of G_d, singleton of G_{-d}, singleton of G'_d, singleton of G'_{-d}}`: equal in all 837
orbits. So **yes** — the 1-point-line points are, exactly and only, the points of Ω not covered by any of
the 12 lines.

**(e) Consequence: the 12-line+4-point cover is an exact partition, and its dual value matches LP(Ω)
exactly, in every orbit.** Weight 1 on each of the 12 lines and weight 1 on each of the 4 points is
dual-feasible for LP(Ω) with total value 2·12 + 1·4 = 28 (every point of Ω is covered with equality — it
lies on exactly one of the 12 lines XOR is exactly one of the 4 singletons, from (c)+(d), never both,
never neither). Since LP(Ω) itself — computed independently by `linprog` from *all* of P's rows, columns,
and slope-±1 lines restricted to Ω, not just these 16 pieces (12 lines + 4 points) — equals 28.000 in every one of the 837 cases,
this combinatorial dual point is **LP-optimal** by weak duality (dual value = primal optimum ⇒ both are
optimal), in every single orbit, unconditionally over the tested range.

## 6. A note on requirement (ii): LP(Ω) uses more than the 16-piece dual certificate, and still gives exactly 28

Requirement (ii) asks for LP(Ω) with *all* rows, columns, and slope-±1 lines of P restricted to Ω (≥3
points), not just the 12 lines + 4 points of §5. This was implemented literally (every line of P is intersected with
Ω and kept as a constraint iff the intersection has ≥3 points), and it turns out Ω has **more** binding
line-constraints than the 12 "own" diagonal/antidiagonal lines of §5 (plus rows and columns): **56
constraints in total, in every one of the 837
orbits**, an exact and completely uniform signature `{rows:16, cols:16, diagonals:12, antidiagonals:12}`
(never varies). Sixteen rows and 16 columns are accounted for by §5(b). The diagonal/antidiagonal counts
split as 6 "own" (the lines of §5(c)) + **6 "extra"** each:

* the 6 extra diagonal (`d`-family) lines have sizes {4,4,3,3,3,3} (always, every orbit) and are built
  *purely* from re-slicing the 32 points of `G'_d ∪ G'_{-d}` along the slope+1 direction — never from
  `G_d`/`G_{-d}` points (checked: 0 counterexamples in 837 orbits);
* symmetrically, the 6 extra antidiagonal (`a`-family) lines have sizes {4,4,3,3,3,3} and are built purely
  from `G_d ∪ G_{-d}`, never from `G'_d`/`G'_{-d}` points.

**Bonus fact** (not required by the task, but relevant to any future uniqueness/robustness argument):
each of the four 1-point-line singletons lies on exactly one of these extra lines — always one of size 4,
never size 3 — giving a clean 1-1 correspondence between the 4 singleton points and the 4 size-4 extra
lines per orbit (2 diagonal + 2 antidiagonal), confirmed in all 837 orbits with no exception. So although a
singleton point is alone on its *own* line, it is never an isolated point of P: it always sits inside one
extra 4-point line of the *other* slope family, together with 3 points drawn from the two same-handedness
groups.

Of the 56 total constraints, only 12 (the "own" diagonal/antidiagonal lines) carry weight in the
combinatorial dual of §5(e); rows, columns, and the 12 extra lines all get dual weight 0 there and are not
needed for the value-28 certificate. Feeding the other 44 constraints (16 rows + 16 columns + 12 extra
lines) back into the LP as well — i.e. solving the literal, full LP(Ω) — still gives exactly **28** in
every one of the 837 orbits: none of these additional constraints ever forces the optimum below the bound
the 12-line-plus-4-point dual already certifies.

## 7. Exceptions (requirement iv)

**None**, for any of the 837 orbits at any of the 91 primes 11 ≤ p ≤ 500 (all primes in range were used —
the fallback sampling above p=300 permitted by the task was not needed, runtime was 5.3s total). Every
orbit has |Ω|=64, is closed under rows and columns, has LP(Ω)=28.000, has its 12 own lines pairwise
disjoint, and its 4 uncovered points equal to its 4 singletons. The only non-generic cases encountered are
the vacuous ones: 5 primes with m7=0 (§3), where "0 orbits checked, 0 LP=28, 0 exceptions" holds trivially.

For the avoidance of doubt about consistency with B.19 addendum (c) (which reports that *different*
(7,5,3,1) orbits can overlap — "5 of 45 pairs of (7,5,3,1)-orbits at p=113 share points"): that is a
statement about pairs of distinct residues d ≠ e (mod the {±d} pairing) whose orbits Ω_d, Ω_e intersect,
and is unrelated to — and not contradicted by — anything checked here, which is entirely about the
internal structure of one orbit Ω_d in isolation. This note did not re-verify the inter-orbit overlap
census of B.19(c) (out of scope for task A); it only certifies that each orbit *by itself* satisfies the
lemma in §5, which is exactly what a "one forced deletion per slope-group, before accounting for
overlaps" argument (B.19 point 6) needs as its local building block.

## 8. Suggested lemma statement (for a write-up)

> **Lemma (orbit cover for (7,5,3,1) groups, k=−1).** Let p be an odd prime, and let d ∈ Z/pZ be such that
> the slope-(+1) residue group G_d has type (7,5,3,1). Then G_{-d}, and the slope-(−1) groups G'_d :=
> R(G_{-d}), G'_{-d} := R(G_d) (R:(x,y)↦(p−x,y)) all have type (7,5,3,1) as well, and Ω := G_d ∪ G_{-d} ∪
> G'_d ∪ G'_{-d} satisfies:
> 1. the four groups are pairwise disjoint, |Ω| = 64;
> 2. Ω is a union of 16 full rows and 16 full columns of P, each of size exactly 4;
> 3. the four groups' twelve lines of sizes 7,5,3 are pairwise disjoint and partition 60 of the 64 points
>    of Ω; the remaining 4 points are exactly the four groups' four 1-point lines, one point each;
> 4. hence, for every lawful point set S (row/column/slope-±1-line capacity ≤ 2), |S ∩ Ω| ≤ 2·12 + 4 = 28;
> 5. LP(Ω) (the LP relaxation with every row, column and slope-±1 line of P restricted to Ω) equals 28
>    exactly, so the bound in (4) is tight and its combinatorial dual certificate is LP-optimal.
>
> Verified by direct enumeration for **every** group of type (7,5,3,1) at **every** prime 11 ≤ p ≤ 500
> (837 orbits, 91 primes, 0 exceptions). Part 1 (type(G_{-d}) = type(G_d)) is the RR′-symmetry argument of
> B.19 addendum (a); parts 2–5 were not previously proved, only spot-checked at p=113,137,199 (B.19 point
> 2 and addendum (b)); this note extends that check to the full range with no failures and pins down the
> exact combinatorial shape (2)–(3) that a real proof of parts 2–5 would need to establish.

## Files

* `slack/t221_agents/orbit_cover.py` — the checker (self-contained, 366 lines; `run_p(p)` returns a
  summary dict + list of per-orbit fact dicts; `__main__` sweeps a prime range and writes the two output
  files below).
* `slack/t221_agents/orbit_cover_output.txt` — the p/m8/m7/m6groups/orbits/LP28/exceptions table (§3) plus
  the exceptions log (empty).
* `slack/t221_agents/orbit_cover_detail.json` — per-orbit machine-readable facts (all fields computed in
  `check_orbit()`: closure, LP value and constraint-family counts, cover/partition booleans, cross-hit
  list, etc.) for all 837 orbits; ~800 KB.
* This report: `docs/research/t221_agents/orbit_cover.md`.

Reproduce with `/Users/iwasborninbali/venvs/sat/bin/python3 slack/t221_agents/orbit_cover.py 11 500`
(5.3 s). `slack/lp1_types.py 113`/`137`/`199` (same venv) reproduces the B.19 census numbers quoted in §4.
