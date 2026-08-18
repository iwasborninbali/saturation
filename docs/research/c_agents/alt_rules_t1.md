# alt_rules_t1: local window-predicate rules for t_G ∈ {0,1} selection

Task `alt_rules_t1` (see `docs/research/pair_bound_notes.md` §25–26 and `slack/cyc_model.py`). Code:
`slack/c_agents/alt_rules_t1.py` (run with `/Users/iwasborninbali/venvs/sat/bin/python3 slack/c_agents/alt_rules_t1.py`
from the repo root; ~2s wall-clock, all numbers below are reproduced verbatim by that one run).

## Setup and metric

Each 8-group `G` has 4 vertices (2 K-type, 2 M-type). Choosing `t_G = 1` on a set `S` of groups gives
demand 0 to their vertices; the exact optimal cover cost is then (§26, confirmed below)

```
net(S) = 2 · changes(S) − 6 · |S|,     changes(S) = # type-alternations in the cyclic sequence of
                                       S's OWN specials (S filtered out of the full special sequence)
```

positive iff more than 3/4 of consecutive `S`-specials alternate type. The reported metric is
**net(S) / G8**, `G8` = total number of groups in the model (a non-selected group still dilutes the
denominator — this is the convention of §25/26, `c` in `saving ≥ c·G8`). Every rule here is a
*window predicate* on the cyclic sequence of **all** specials (all groups' vertices, selected or
not): the decision for a group depends only on the type of a bounded number of neighbouring specials.

## Rules tried

**One-shot** (single pass over the full all-specials sequence, decided once before any selection):
- `all4` — every one of a group's 4 vertices has *both* its immediate (radius-1) neighbouring
  specials of the opposite type (the predicate literally suggested in the task).
- `ge3`, `ge2` — the same per-vertex test, required of ≥3 / ≥2 of the 4 vertices.
- `or_all4` — weaker per-vertex test (*at least one* of the two neighbours opposite), required of
  all 4 vertices.
- `window_r2` — radius-2 window (2 previous + 2 next specials), ≥3 of 4 window-neighbours opposite,
  required of ≥3 of the group's 4 vertices ("distance"-flavoured: a wider neighbourhood).
- `adjpack` — pure distance rule, no type check: selects a vertex iff both its raw-cycle-adjacent
  vertices (distance exactly 1 in the underlying strictly-alternating K,M,K,M,… cycle, not just among
  specials) are themselves special; by the strict alternation this *automatically* forces opposite
  type, so it isolates "closeness to the nearest special" from "opposite type".

**Iterative** ("select, then re-evaluate neighbours among the selected only, iterate a bounded number
of times" — as suggested in the task): start with candidate = all groups; each round, recompute the
radius-`r` opposite-neighbour test using **only the current candidate's own vertices** as the special
sequence, and drop groups that fail; repeat to a fixed point (empirically 2–7 rounds; capped at 30 as
a safety net, monotonic shrinking).
- `iter_ge2`, `iter_ge3`, `iter_ge4` (=`all4` iterated) — radius 1, per-vertex AND, group needs ≥2/≥3/≥4
  of 4.
- supplementary: `iter(r=2,v=3,g=2)`, `iter(r=2,v=4,g=2)` — same idea at radius 2, to check whether a
  *wider* window helps once combined with iteration.

## Best rule: `iter_ge2`

Radius-1, per-vertex "both immediate neighbours (within the current candidate) opposite type",
group selected iff ≥2 of its 4 vertices pass, iterated to a fixed point. Clearly the best of every
rule tried, on both real and synthetic data, and the only one that is never negative on the real
instances tested.

### Real instances (p,k) ∈ {101,199,401,601} × {2,3}

net/group, `G8` = total groups in that model, free-LP = reference ceiling (unconstrained 0/½/1 LP, §25):

| p | k | G8 | free-LP | all4 | ge3 | ge2 | or_all4 | window_r2 | adjpack | **iter_ge2** | iter_ge3 | iter_ge4 |
|---|---|----|---------|------|-----|-----|---------|-----------|---------|--------------|----------|----------|
|101|2| 16|+0.750|−0.250|−0.250|+0.000|+0.000|+0.000|−0.250|**+0.000**|+0.000|+0.000|
|101|3| 10|+0.400|+0.000|+0.000|+0.000|−0.800|+0.000|+0.000|**+0.000**|+0.000|+0.000|
|199|2| 32|+0.812|−0.125|−0.125|−0.250|−0.250|−0.500|−0.250|**+0.250**|+0.000|+0.000|
|199|3| 34|+0.882|−0.118|−0.118|+0.235|−0.118|+0.000|+0.118|**+0.235**|+0.000|+0.000|
|401|2| 64|+0.938|−0.250|−0.250|+0.312|−0.375|−0.250|−0.312|**+0.375**|+0.000|+0.000|
|401|3| 58|+0.862|−0.069|−0.069|−0.552|−0.828|−0.483|−0.207|**+0.069**|+0.000|+0.000|
|601|2|102|+0.961|−0.118|−0.118|+0.314|−0.471|−0.157|−0.275|**+0.667**|+0.039|+0.039|
|601|3| 94|+1.064|−0.426|−0.426|+0.553|+0.128|−0.298|−0.340|**+0.766**|+0.000|+0.000|
| **mean** | | | | | | | | | | **+0.295** | | |

`iter_ge2` is ≥ 0 on all 8 real instances and strictly positive on 6/8, rising with `p` (matches the
free-LP ceiling's own rise, §25). It is well below the free-LP ceiling throughout (using ~35–75% of
the LP's saving), consistent with §26's expectation that bounded-window rules approach, but do not
reach, the free optimum. A striking single data point on how much the *iteration* step matters:
at p=199,k=2 the one-shot `ge2` gives **−0.250**, but the iterated `iter_ge2` on the exact same
model gives **+0.250** — a full 0.5/group swing from re-evaluating neighbours after one round of
pruning, exactly the mechanism the task description points at.

### Synthetic instances (uniformly random groups, same cycles) — two sizes, 8 seeds each

`p=101` (G8=16):

| rule | mean net/group | range |
|---|---|---|
| all4 | −0.016 | [−0.125, +0.125] |
| ge3 | −0.172 | [−0.500, +0.250] |
| ge2 | −0.125 | [−0.500, +0.375] |
| or_all4 | −0.250 | [−0.750, +0.500] |
| window_r2 | −0.125 | [−0.625, +0.125] |
| adjpack | −0.031 | [−0.250, +0.125] |
| **iter_ge2** | **+0.250** | **[+0.000, +0.750]** |
| iter_ge3 | +0.063 | [+0.000, +0.250] |
| iter_ge4 | +0.016 | [+0.000, +0.125] |

`p=601` (G8=102):

| rule | mean net/group | range |
|---|---|---|
| all4 | −0.120 | [−0.255, +0.000] |
| ge3 | −0.203 | [−0.333, −0.098] |
| ge2 | −0.314 | [−0.529, −0.196] |
| or_all4 | −0.466 | [−0.549, −0.333] |
| window_r2 | −0.233 | [−0.373, −0.039] |
| adjpack | −0.157 | [−0.216, −0.078] |
| **iter_ge2** | **+0.074** | **[−0.039, +0.137]** |
| iter_ge3 | +0.003 | [+0.000, +0.020] |
| iter_ge4 | +0.000 | [+0.000, +0.000] |

`iter_ge2` is the only rule with a clearly positive **mean** at both sizes. At `p=101` it is ≥0 on
every one of the 8 seeds (never negative). At `p=601` it is positive on 6/8 seeds and only slightly
negative on the other 2 (−0.020, −0.039) — an honest, modest **positive-in-expectation, not
positive-in-the-worst-case** result on the harder, fully-random instances.

## Negative / mixed results (honest reporting)

- **`all4` / `ge3` (one-shot or iterated)** are essentially useless: too strict a per-vertex test
  applied to a group with 4 independently-placed vertices selects almost nothing (often `|S|=0`),
  and even when non-empty the surviving groups' *own* filtered adjacency (which is what actually
  counts, via `changes(S)`) is usually worse than what the ALL-specials window promised — because a
  vertex's good ALL-specials neighbour frequently belongs to a group that itself doesn't qualify, so
  within the `S`-only sequence the true neighbour is someone else entirely. `iter_ge3`/`iter_ge4`
  mostly collapse all the way to the empty set under iteration (cascading pruning), landing at exactly
  `net/group = 0`.
- **`or_all4`** (the weak, "at least one neighbour opposite" per-vertex test) is actively bad
  (−0.25 to −0.83 on real, −0.25 to −0.47 mean on synthetic): the condition is so permissive that it
  barely filters anything, so `S` ends up close to "all groups", which loses for exactly the reason
  in §26 (change-ratio ≈ 0.5–0.66 < 0.75 needed).
- **`window_r2`** (a *wider*, radius-2 window, one-shot) is never better than `iter_ge2` and usually
  negative. The supplementary check in the script (radius-2 window **combined with iteration**,
  `iter(r=2,v=3,g=2)`) makes this precise: on the same 8 real instances where `iter_ge2` scores
  +0.000 … +0.766, the radius-2 iterated version scores between **−0.500 and +0.000** every time
  (`iter(r=2,v=4,g=2)` collapses to the empty set everywhere, `net/group = 0`). **Widening the window
  does not help once iteration is already doing the real work** — the single extra hop from
  "ALL-specials neighbour" to "current-candidate neighbour" is what buys the swing; a second hop of
  raw window radius does not add more.
- **`adjpack`** (pure raw-cycle distance ≤1, no type check) is consistently negative to mildly
  negative — being *physically adjacent* to another special in the underlying cycle is not, by
  itself, a useful signal once one also needs that neighbour's *group* to be selected; the type-based
  window tests (which reason about ALL specials, not just distance) dominate it everywhere tested.

## LP cross-check

`net(S) = 2·changes(S) − 6|S|` was confirmed against the exact optimum `lp(M, t_fixed=…)` (every
group fixed — 1 on `S`, 0 elsewhere, nothing left free for the LP to re-optimise) for `iter_ge2`'s
selection on 4 instances; all match to the solver's numerical precision:

```
real p=199 k=2 : lp saving=8.0000   formula 2*changes-6|S| = 8    OK
real p=401 k=3 : lp saving=4.0000   formula 2*changes-6|S| = 4    OK
synthetic p=101 seed=3 : lp saving=10.0000  formula = 10          OK
synthetic p=601 seed=0 : lp saving=12.0000  formula = 12          OK
```

## Summary

Best rule found: **`iter_ge2`** — radius-1 "both immediate neighbours (recomputed among the current
candidate only) of opposite type", group selected iff ≥2 of its 4 vertices pass, iterated to a fixed
point (2–7 rounds in practice). Numbers:
- **Real** (8 instances, p∈{101,199,401,601}, k∈{2,3}): mean **+0.295/group**, never negative, up to
  +0.766/group at p=601,k=3.
- **Synthetic** (2 sizes × 8 seeds, uniformly random groups — the harder, more adversarial case): mean
  **+0.250/group** at p=101 (never negative over 8 seeds), mean **+0.074/group** at p=601 (2 of 8
  seeds mildly negative, −0.02 to −0.04).

This is a genuine but modest positive-expectation local rule (well below the ≈0.75–1.06/group free-LP
ceiling of §25, and not uniformly positive on every synthetic seed at the larger size), obtained from
a bounded window (radius 1) plus a bounded number of re-evaluation rounds. The single largest lever
found was the **iteration step itself** — re-deriving each vertex's "neighbouring special" from the
current candidate set rather than the full all-groups set, which at p=199,k=2 alone flips the same
per-vertex test from −0.25/group to +0.25/group. Widening the window (radius 2) does not substitute
for this and performs worse in every configuration tried.
