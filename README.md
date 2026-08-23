# saturation

Working repository of an autonomous AI research pair (two Claude agents: a searcher and an
independent verifier) directed by Aleksei Kudriashov, on the no-three-in-line problem and its
relatives. This is a **live working journal**, not a curated library — the curated entry points
are below, so you do not have to hunt.

## If you came for something specific

**Witness configurations (flat, self-describing text files, re-verified at generation time):**

| file | contents |
|---|---|
| [`witnesses/A399138_no3collinear_cube.txt`](witnesses/A399138_no3collinear_cube.txt) | cube, no three collinear: exact optima n = 1..6, lower-bound witnesses a(7) >= 73, a(8) >= 93 |
| [`witnesses/A280537_no4coplanar_cube.txt`](witnesses/A280537_no4coplanar_cube.txt) | cube, no four coplanar: 19 certified lower-bound configurations, n = 9..29 |
| [`witnesses/A000769_new_halfturn_configurations.txt`](witnesses/A000769_new_halfturn_configurations.txt) | plane, 2n points: the ten new configurations with stabiliser exactly the half-turn (n = 33, 36, 37, 39) |

**The five papers (each DOI is a concept DOI: it always resolves to the latest version; every
Zenodo record carries PDF, TeX and a data package):**

| paper | source | DOI (all versions) |
|---|---|---|
| Extremal no-3-in-line subsets of a modular hyperbola (HJSW window) | `paper/hjsw_window.tex` | [10.5281/zenodo.22063297](https://doi.org/10.5281/zenodo.22063297) |
| Balanced orbit defects, with new 2n-point configurations | `paper/no3inline_defects.tex` | [10.5281/zenodo.22063287](https://doi.org/10.5281/zenodo.22063287) |
| Certified exact values, no-3-in-line in the cube | `paper/no3_3d_note.tex` | [10.5281/zenodo.22019279](https://doi.org/10.5281/zenodo.22019279) |
| The error of the Guy–Kelly heuristic, measured | `paper/guy_kelly_error.tex` | [10.5281/zenodo.22063191](https://doi.org/10.5281/zenodo.22063191) |
| Certified witnesses for A280537, against prior art | `paper/a280537_note.tex` | [10.5281/zenodo.22023079](https://doi.org/10.5281/zenodo.22023079) |

**OEIS:**

| entry | contribution | status |
|---|---|---|
| [A399138](https://oeis.org/A399138) — maximum points in the n X n X n grid, no three collinear | new sequence (1, 8, 16, 28, 40, 64), with attached witness file | approved, Aug 23 2026 |
| [A000755](https://oeis.org/A000755) — plane, total number of 2n-point solutions | a(20) = 941580 into DATA (from Flammenkamp's database, confirmed by orbit sums) | proposed, in review |
| [A280537](https://oeis.org/A280537) — cube, no four coplanar | eight strictly improved lower bounds + transcription of the 2016 contest records up to n = 97, with attached witness file | proposed, in review |

**External:** Achim Flammenkamp's [no-three-in-line database](https://wwwhomes.uni-bielefeld.de/achim/no3in/readme.html)
(changelog, 17 Aug 2026) records nine new rot2 solutions for n = 33, 36, 37, 39 from this project.

**Independent verifiers** (no code shared with the searchers): `certs/a280537/verify_witness.py`
(exact determinants over quadruples), `certs/no3_3d/verify_witness_lines.py` (cross products over
triples), `slack/verify_papers/` (the from-scratch verification batteries behind the papers'
pre-publication checks).

**Journals:** every number in the papers traces to a file under `logs/` — start at
[`logs/README_index.md`](logs/README_index.md). Negative results and retractions are kept, not
erased; the repository's rule is that a number without a journal reference counts as unverified.

---

## Working notes (the original journal preamble)

`saturation.py` states the task in a deliberately blinded vocabulary (tokens,
registers, reading classes, "the law") and *verifies*; everything else here
*searches* and hands its books back through `saturation.certify`.

Plain words: choose 2n cells of an n×n grid with no three collinear
(the no-three-in-line problem, Dudeney 1917).  A 2n-book is *saturated*.
State of the art (Flammenkamp's database, 2026-08-11): saturated books are
known for all n ≤ 70 and for 72, 74, 76; open: 71, 73, 75, ≥ 77.

## Layout

| file | what |
|---|---|
| `saturation.py` | the law + certifier (see git history for provenance) |
| `there.c` | the exact search: bit-parallel DFS with restarts, MRV over both registers, shading of every chosen pair, symmetry orbits, pairwise-orbit clash masks, exhaustive mode with solution counts (validated against A000769 and Flammenkamp's tables), fixed-token completion (`FIX=file`) |
| `there.py` | driver: `find(n)` = saturation.find at this end; parallel seeds per symmetry class; results in `books.json` (each entry certified) |
| `there_sat.py` | CNF encoding + kissat (second engine; loses to the DFS from n≈27 up) |
| `lns.py` | large-neighbourhood search from a known book at n to n+2s (negative result: neighbouring sizes are uncorrelated) |
| `web/decode.py`, `web/fetch.sh` | decode/certify configurations in Flammenkamp's format |
| `bench/` | calibration data: exhaustive tree sizes per class, strategy comparisons |
| `deadends/walk.c` | plain min-conflicts local search — dies at n≈12 for exact 2n |
| `web/stab.py` | exact symmetry class of a book (Flammenkamp's names) + his encoding |
| `docs/HELLO.md`, `docs/REPLY.md`, `docs/THREAD.md` | the two solvers' correspondence (append to THREAD) |
| `docs/SUBMISSION.md` | certified candidates for the database |
| `kit71/` | the first solver's kit (footholds at n=71, algebra, SA/ILS, traces, ledger) |

Symmetry class ids in `there.c` (Flammenkamp's names in brackets):
0 none [iden], 1 half turn [rot2], 2 quarter turns [rot4, even n], 3 swap [dia1],
4 flip [ort1, even n], 5 both flips [ort2], 6 both swaps [dia2], 7 all eight [full],
8 quarter turns off the long axes + one half-turn pair on the main axis [rct4, odd n].

## Build & check
    make && make check

## Use
    ./there n sym [seed] [seconds] [cap0] [order] [value] [growth%] [shave]
    ALL=1 ./there n sym            # exhaustive: count every book in the class
    FIX=cells.txt ./there n sym    # complete a fixed lawful partial book (or prove none)
    python3 there.py 2 46 --secs 900 --seeds 8
    python3 lns.py web/n44_rot4 46 --k 6 --tries 100

`there` handles n ≤ 64 (64-bit masks); `there128` handles n ≤ 128.
