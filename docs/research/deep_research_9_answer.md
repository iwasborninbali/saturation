# Deep research 9 — what actually makes the rot2 census reach n≈30

Date: 2026-08-20

Status: multi-agent research, independent verification, adversarial review, primary-source reconciliation

Companion executable specification: `docs/research/rot2_census_contracts.py`

Regression suite: `docs/research/test_rot2_census_contracts.py`

## Executive answer

The calibration did its job: the current simple `census_rot2` implementation is not a viable route to
`n=32`.  It does **not**, however, establish that DFS or row search as an algorithmic class is unviable.
The public historical record gives a direct counterexample.  Flammenkamp describes his enumerator as a
recursive total tree search with sophisticated branch and bound, and his published rot2 case counts grow
far more slowly than the new local tree.  The modern Riley enumerator is also DFS: the decisive ingredients
are fixed-point row/column propagation, constrained-row pair branching, vulnerable and semivulnerable
branching, symmetry-compatible partial-state canonicalization, and pair-to-line lookup masks.

The immediate research question is therefore no longer

> Which exotic algorithm must replace DFS?

but

> Which propagation, branching, and canonical-order mechanisms change the local base of growth from
> approximately 18–19 per `+2` to the historical range near 10–12?

MITM, ZDD, SAT/model counting, defect-first generation, and SSMCC remain legitimate measured pilots.  They
are not conclusions forced by the calibration.

## 1. Work performed

The research was split into independent roles before reconciliation:

1. **research / oppose / counter-ideas** — reconstruction of the historical and modern enumeration
   algorithms, plus steelmanning of competing architectures;
2. **independent verification** — fresh geometry oracles, small rot2 censuses, arithmetic, group-action
   semantics, and certificate logic;
3. **adversarial / edge cases** — attempts to falsify completeness, encoding, symmetry, manifest, and
   extrapolation claims;
4. **main-agent review** — source reconciliation and direct audit of the repository/tagged artifacts.

The executable translation follows the owner's `principles.py` method: exception ontology first, minimal
predicates, import-time positive proofs, explicit breach tests, evidence-bearing claims, and an honest
`NotImplementedError` for architecture judgment.

## 2. Calibration: exact arithmetic and corrected interpretation

The measured local sequence is:

| n | local nodes | ratio from n−2 |
|---:|---:|---:|
| 6 | 157 | — |
| 8 | 2,546 | 16.22 |
| 10 | 43,008 | 16.89 |
| 12 | 947,135 | 22.02 |
| 14 | 17,661,187 | 18.65 |

The geometric mean of the four ratios is 18.31.  If one nevertheless imposes exactly `×19` for the next
nine `+2` steps, then

```text
N(32) = 17,661,187 × 19^9
      = 5,699,047,773,074,403,673.
```

At 795,000 local nodes per second this is approximately 227,160 core-years, or 4,056 years on 56 cores.
The 10,000-core-hour budget processes 28.62 trillion such nodes, so the conditional gap is approximately
199,128 times.

Two corrections are essential:

- 199,128 times is **5.30 decimal orders**, not thirteen orders;
- this is a forecast for one measured implementation, not a lower bound on DFS/B&B.

The implementation source named in the brief, `slack/t221/census_rot2.c`, is absent from the available
workspace and from the accessible `/Users/iwasborninbali` tree.  The values `36` and `67` were independently
confirmed, but the precise local node definition and the 795k/s measurement cannot be source-audited here.

## 3. Four distinct meanings hidden by “rot2”

Let `H={id,r²}` be the central half-turn subgroup of `D4`.  Four counts must be distinguished:

1. labelled configurations fixed by H;
2. labelled configurations whose stabilizer is exactly H;
3. D4-classes whose stabilizer contains H;
4. D4-classes whose stabilizer is exactly H.

An independent small enumerator gave:

| n | H-fixed labelled | exact-H labelled | H-containing D4 classes | exact-H D4 classes |
|---:|---:|---:|---:|---:|
| 6 | 18 | 8 | 7 | 2 |
| 8 | 36 | 28 | 11 | 7 |
| 10 | 67 | 52 | 21 | 13 |

Thus the local checks `n=8 → 36` and `n=10 → 67` are correct, but they are not exact-rot2 database counts.

Because H is central, `D4/H` has order four.  It acts freely on configurations with exact stabilizer H, so
an exact-H D4 class has four labelled orientations.  The same constant conversion is false for at-least-H:
higher stabilizers have smaller orbits.  Every result and API must name its universe explicitly.

## 4. The historical counterexample to the “DFS is impossible” inference

Flammenkamp's official project page describes the program as a **recursive total tree search** with
**sophisticated branch and bound** and notes that the proper traversal order depends on the symmetry class:

- <https://wwwhomes.uni-bielefeld.de/achim/no3in/readme.html>

The historical half-turn data publish these case counters:

| n | cases |
|---:|---:|
| 6 | 71 |
| 8 | 351 |
| 10 | 2,467 |
| 12 | 17,870 |
| 14 | 169,138 |
| 16 | 1,665,072 |
| 18 | 16,797,899 |
| 20 | 208,014,023 |
| 22 | 2,415,249,559 |
| 24 | 33,184,295,393 |

Primary data: <https://wwwhomes.uni-bielefeld.de/achim/no3in/data_1997/cases_half.txt>

The raw ratio `local nodes / historical cases` is already 2.21, 7.25, 17.43, 53.00, and 104.42 for
`n=6,8,10,12,14`.  These counters are **not** directly interchangeable: their increment semantics are not
fully documented in a common frame, and the published output counts use different symmetry quotients.  The
ratios therefore are not speedup measurements.  Their fast divergence nevertheless falsifies the claim
that the local `×19` tree represents an unavoidable DFS tree.

The official current table reports the exact-rot2 census complete through `n=31`, with 80,229 D4 classes at
that order, while `n=32` remains open:

- <https://wwwhomes.uni-bielefeld.de/achim/no3in/table.html>

The public download exposes common historical sources such as `iden.c` and `fullnew.c`, but the exact source,
revision, hardware, manifest, and node log for the 2026 `n=31` completion were not located:

- <https://wwwhomes.uni-bielefeld.de/~achim/no3in/download/README>

It is therefore justified to conclude that strong symmetry-aware B&B/DFS has achieved the census.  It is
not justified to attribute a specific unpublished 2026 implementation to Flammenkamp.

## 5. The strongest public modern architecture

Riley's public enumerator is also DFS.  Its important features are:

- ternary on/off/unknown board state;
- exact-two row and column propagation to a fixed point;
- vulnerable and semivulnerable cells;
- selection of the row with the fewest legal options;
- branching over every legal pair for that row, not over one isolated point/orbit;
- unknown-aware comparison of partial orientations;
- precomputed pair-to-complete-line masks;
- CPU/GPU frontier execution after the tree has been strengthened.

Primary descriptions and source:

- <https://mvr.github.io/posts/no-three-in-line.html>
- <https://mvr.github.io/posts/no-three-in-line-quicker.html>
- <https://mvr.github.io/posts/no-three-in-line-dumber.html>
- <https://github.com/mvr/no-three-in-line>

The stronger quarter-turn and reflection classes solved at much larger `n` are not direct cost estimates for
rot2: their symmetry leaves a substantially smaller search.  They do show that enumeration at large `n`
does not require abandoning DFS in principle.

## 6. Correct orbit encoding for n=32

Two independent exact line oracles agreed on the following geometry:

| quantity | value |
|---|---:|
| half-turn cell orbits | 512 |
| maximal lattice lines of length ≥3 | 44,282 |
| point-line incidences | 168,860 |
| collinear cell triples | 837,744 |
| unique orbit clauses before subsumption | 415,040 |
| binary clauses | 328 |
| ternary clauses | 414,712 |
| ternaries subsumed by binaries | 1,168 |
| subsumption-minimal clauses | 413,872 |

The earlier ternary table `F[a][b] → forbidden c` is incomplete on its own.  For example, on `n=4` the two
orbits

```text
A = {(0,0),(3,3)}
B = {(1,1),(2,2)}
```

are already mutually incompatible; selecting them puts four points on the main diagonal.  There is no third
orbit `c` to record.  A correct incremental kernel needs both:

```python
if candidate in forbidden:
    reject()

forbidden |= B[candidate]              # binary orbit incompatibilities
for chosen_orbit in chosen:
    forbidden |= F[candidate][chosen_orbit]
```

The full `F` table is about 16 MiB, or about 8 MiB when stored symmetrically.  `B` is about 32 KiB.  Claims of
a 10–40× runtime improvement remain a benchmark hypothesis; the exact clause counts do not prove it.

For odd boards and other symmetry groups, row/column cardinalities in the orbit quotient are weighted:

```python
sum(points_of_orbit_in_row[o, r] * x[o] for o in orbits) == 2
```

On `n=3`, the orbit `{(1,0),(1,2)}` has weight two in the central row.  An unweighted “choose two orbit
variables per row” encoding is unsound.

## 7. Adversarial failures that must become permanent regressions

### 7.1 Search is not enumeration

The paper correctly documents the minimal witness: plain `sym=2` search at `n=8` returns 8 outputs where the
H-fixed labelled universe contains 36.  A `FIND_ONE` result must be structurally incapable of constructing a
completeness claim.

### 7.2 Timeout is not exhaustion

The tagged/current `logs/sweeps/twoloop_n36_exh.txt` has all 153 expected keys, but only 152 exhausted keys.
The entry `(1,4)` is:

```text
x=1 y=4 :: timeout-all n=36 sym=2: incomplete, solutions_so_far=0 nodes=209846272 secs=3600.14
```

The paper says an unlimited rerun completed in about `4.9·10^7` nodes, but no terminal rerun record is present
in `defects-v1.0`.  Moreover `bench/twoloop_exh.sh` treats the existence of any matching line prefix as a
completed task, so the timeout prevents a retry.  The executable regression suite reads the real release log
and requires it to be rejected as incomplete.

### 7.3 Dynamic MRV plus naive partial canonicalization can lose a full orbit

Canonicalizing only the selected set at every dynamic-MRV prefix is not generally hereditary: a canonical
full object need not have a canonical parent under the dynamically chosen deletion.  Allowed approaches are
a proved hereditary orderly generation, a canonical construction path, or an unknown-aware partial-state
comparison whose compatibility with the branching rule is proved and tested.

### 7.4 Auxiliary cube splits can overlap after projection

If `x` is projected and `y` is auxiliary, cubes `y` and `¬y` both contain the projections `x=0` and `x=1`.
They partition full SAT assignments but not projected configurations.  Enumeration must split on projected
variables or apply a global ownership/deduplication rule.  Each published model must be blocked by the exact
complement over **all** projected variables before a terminal UNSAT proof is checked.

### 7.5 Small-n agreement can still share an incomplete generator

The previous omission of central-class three-cycle defects is the concrete warning.  Agreement between two
solvers that receive the same incomplete subclass list is common-mode failure.  The generator itself needs
an exhaustive small reference and the identity

```text
number of three-cycle defect classes = 4*C(h,3) + C(h,2).
```

The second term is exactly the previously omitted central class.

## 8. Release audit of no3inline_defects_v1.0

The `n=41` three-cycle family evidence is structurally strong: the tagged manifests cover 4,750 subclasses
for each of the two bases, the task-key sets agree with the generated lists, and the data rows contain no
timeouts.  This establishes the stated **three-cycle defect-family** result.  It is not an enumeration of all
rot2 configurations at `n=41`.

The `n=36` two-loop row is not supported by the published manifest because `(1,4)` has no exhausted rerun, as
described above.  The release process must be repaired before that row uses an equality/completeness marker.

The PDF v1.0 reproducibility section points readers to immutable tag `defects-v0.8`, although the completed
`n=41` evidence arrived only in `defects-v1.0`.  The release tag reference must be updated.  Negative family
results remain trusted-program computations unless and until independent proof certificates are published.

## 9. Executable contract design

`rot2_census_contracts.py` encodes the following boundaries:

- `ProblemSpec` requires an order, a count universe, and a run mode;
- `AttemptStatus.EXHAUSTED` is the only state that completes an enumeration task;
- timeout then successful rerun is legal, timeout alone is not;
- conflicting exhausted digests are rejected;
- counts in different universes cannot be compared;
- historical `cases` and local `nodes` cannot be compared without a common increment rule;
- binary orbit conflicts and weighted odd-board row incidences are explicit geometry;
- projected blockers and projected-leaf disjointness are checked separately;
- partial canonical pruning requires a named heredity proof;
- an implementation calibration cannot construct an algorithm-class lower bound;
- architecture choice remains a `NotImplementedError`, not a fabricated score.

The stdlib-only test suite includes the real `n=36` manifest breach and the exact `×19` arithmetic.  It is
intentionally independent of the production searcher.

## 10. Revised experimental programme

### Phase A — comparable reference frame

Before performance work:

1. select one explicit universe, initially `H_FIXED_LABELLED` for compatibility with 36/67;
2. build independent canonical and labelled catalogues through at least `n=16`;
3. define every counter (`recursive entry`, `candidate pair`, `contradiction`, `leaf`);
4. require equal catalog hashes for every ablation;
5. store one structured immutable report per task; never infer status from stdout prefixes.

### Phase B — tree ablation

Measure on `n=12,14,16,18`, adding one feature at a time:

1. current fixed-order one-orbit branching;
2. complete row-pair branching;
3. most-constrained-row selection;
4. alternating row/column fixed-point forcing;
5. vulnerable branching;
6. semivulnerable branching;
7. symmetry-compatible partial-state canonicalization;
8. binary/ternary orbit-mask kernel.

Record candidate attempts, contradictions, recursive states, catalogue hash, wall time, and peak memory.  Do
not begin a GPU port unless the tree itself moves materially toward the historical growth regime.  If the
growth remains near 19 through `n=18`, stop and identify the missing pruning invariant.

### Phase C — falsifiable alternative pilots

**SAT / projected AllSAT / model counting.**  First match deterministic counts at `n=14,16,18`; verify
projection semantics and proof size.  Kill circuit/proof compilation if memory already becomes dominant by
`n=18`.  Ganak is a useful independent counter, not automatically a formal certificate:
<https://github.com/meelgroup/ganak>.

**Defect-first generation.**  Classify the entire known catalogue through `n=31` by minimum C4/V2 defect
size, prove a unique owner between bases, and measure both the number and total search cost of all admissible
defects.  Fixed small defects are easy; coverage of all defect sizes is the unresolved issue.

**MITM.**  Produce a compact signature that is proved sufficient for every cross triple of types 2+1 and
1+2.  Kill the approach if the signature state count has the same exponential base as direct DFS.

**ZDD/frontier.**  Measure `unique_states / visited_prefixes` and peak nodes through `n=18`.  Kill it if
global line constraints prevent stable sharing.

**SSMCC/Dancing Cells.**  Compare against custom DFS at `n=14,16`, including weighted orbit incidences.  Keep
it only if it is competitive or provides a distinct certification advantage.

## 11. Information to request from Flammenkamp

No correspondence was sent.  A useful minimal request would ask for:

1. the exact source revision used for the `n=31` exact-rot2 completion;
2. the definitions of `positions`, `cases`, and any modern node counters;
3. row/column selection and branching order;
4. propagation rules and canonical partial-orientation rule;
5. exact-vs-at-least separation and D4 ownership;
6. node/time/hardware records for `n=26…31`;
7. an immutable source/archive or checksum sufficient to reproduce the census.

## 12. Final decision

The local calibration is retained as valuable evidence and its arithmetic is corrected, not discarded.  It
has ruled out the current simple traversal.  It has not ruled out the algorithmic family that the public
record says already reached `n=31`.

The next production bet is:

> **constraint-propagating row-pair DFS with an orbit-bitset kernel**, validated in one explicit count
> universe and ablated against small exact catalogues.

MITM, ZDD, SAT/model counting, and defect-first enumeration proceed only as measured challengers with stated
kill criteria.  This replaces an unsupported architecture conclusion with a falsifiable programme.
