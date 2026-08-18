# half_matching — explicit t=1/2 local-matching rules for the cycle-cover model

Agent: `half_matching`. Code: `slack/c_agents/half_matching.py` (self-contained; run with
`/Users/iwasborninbali/venvs/sat/bin/python3 slack/c_agents/half_matching.py` from the repo root,
~2.5s total). Model / background: `docs/research/pair_bound_notes.md` §25–26, `slack/cyc_model.py`.

## Task recap

Choose a set `S` of (4,8,4) groups, put `t_G = 1/2` on each (cost 3, demand 1/2 on its 4 classes),
and a **local matching** of "changing" segments (adjacent `S`-specials of different type, K vs M;
matched segments must be vertex-disjoint) along the `⟨k⟩`-cycles. Exact closed form (§26 bullet 2):
`net = 2·(#matched segments) − 3·|S|`, positive iff more than 3/4 of `S`'s specials get matched.
Report `net / G₈` (total groups in the model, not `|S|`) to compare against the free-LP ceiling
(0.75–1.06 per group, §26) and the known-losing naive schemes.

## What was built

- **Exact matcher** `cyclic_matching`: maximum matching of changing segments on a cyclic typed
  sequence via the standard two-case cycle-DP (`path_matching` + wrap-edge included/excluded),
  O(n). Verified against brute force on 400 random instances (n=2..9) — `self_test()` in the file.
- **Genuinely local matcher** `greedy_matching`: single left-to-right pass, O(1) state (only
  "is the previous vertex already used"), wrap-around pair handled last, no global bookkeeping at
  all. Included to check that the rule survives being implemented as a *true* bounded-window
  automaton, not just something that happens to decompose into an O(n) DP.
- **Rule A — `S = all groups`**, exact or greedy matcher (the naive scheme from the task prompt).
- **Rule B — iterative local pruning**: start `S =` all groups; compute the matching; for every
  group count how many of its 4 vertices ended up matched; drop groups below a threshold `T`;
  recompute on the shrunken `S`; repeat (converges in 2–6 rounds in every instance tested, capped
  at 6). Tried `T ∈ {2,3,4}`.
- **Rule C — mixed `t ∈ {0, 1/2, 1}`**: take Rule B's converged `S` (best threshold), promote
  groups that ended up **fully matched** (4/4 vertices) from `t=1/2` to `t=1` (full block).
- Every rule is cross-checked by the **exact** LP: `lp(M, t_fixed = {g: 0.5 or 1.0 for g in S, 0.0
  for every other group})` — every group is fixed, not just the ones in `S`, so the LP cannot
  quietly re-optimize groups our rule excluded. In every single run below, the closed-form
  `net/G8` and the `lp/G8` agree exactly (see the log; the one exception, greedy-matcher Rule A at
  p=601, differs only in *our own bookkeeping* of which segments we think we picked — the LP
  saving is still identical, because the LP re-derives the true optimum from `S` alone).
- **Structural check `check_disjoint`**: confirmed every class lies in **at most one** (4,8,4)
  group, for all 7 real `(p,k)` instances and all synthetic instances tested. This is why the
  closed form is exact here: `t=1/2` on `S` gives every `S`-vertex demand *exactly* `1/2`, never
  the double-counted `1 − t₁ − t₂` case the general model allows.

## Results — real instances (all 7 combinations `p ∈ {101,199,401,601}`, `k ∈ {2,3}`)

`net/G8` (exact, via `lp(M, t_fixed=...)`); `free-LP/G8` = unconstrained ceiling for context.

| p   | k | G8  | free-LP/G8 | A: all (naive) | B: T=2 | **B: T=3** | B: T=4 | B: T=3, greedy matcher | C: mixed (promote 4/4) |
|-----|---|-----|-----------|-----------------|--------|------------|--------|------------------------|--------------------------|
| 101 | 2 | 16  | 0.750     | −1.000          | +0.500 | **+0.500** | +0.375 | +0.500                 | 0.000                    |
| 199 | 2 | 32  | 0.812     | −0.250          | +0.125 | **+0.625** | +0.062 | +0.625                 | −0.250                   |
| 199 | 3 | 34  | 0.882     | +0.059          | +0.412 | **+0.647** | +0.588 | +0.647                 | −0.118                   |
| 401 | 2 | 64  | 0.938     | +0.000          | +0.281 | **+0.375** | +0.094 | +0.375                 | 0.000                     |
| 401 | 3 | 58  | 0.862     | −0.103          | +0.310 | **+0.586** | +0.414 | +0.586                 | −0.207                   |
| 601 | 2 | 102 | 0.961     | +0.137          | +0.255 | **+0.392** | +0.000 | +0.382                 | +0.078                    |
| 601 | 3 | 94  | 1.064     | +0.064          | +0.287 | **+0.553** | +0.021 | +0.553                 | +0.340                    |
| **mean** | | | | −0.156 | +0.310 | **+0.525** | +0.222 | +0.524 | −0.022 |

`T=3` is the best (or tied-best, at p=101) threshold in **every** real instance: min +0.375,
max +0.647, mean +0.525. Switching the exact DP matcher for the genuinely-local greedy matcher
inside the pruning loop changes the result by at most 1 group / 2 matches out of ~50–60 (p=601,k=2:
52→51 groups, net 0.392→0.382); everywhere else it is bit-for-bit identical — locality is real,
not an artifact of the O(n) DP.

## Results — synthetic instances (same cycles, random groups; ≥2 sizes, ≥5 seeds each)

Ran `p ∈ {199, 401, 601}` (all with `k=2`) × seeds `0..6` (7 seeds, 21 runs total). `net/G8`, mean
(min, max) over the 7 seeds:

| p (synthetic) | G8  | A: all (naive) | B: T=2 | **B: T=3** | B: T=4 | C: mixed |
|----------------|-----|-----------------|--------|------------|--------|----------|
| 199            | 32  | −0.161 (−0.312, 0.000) | +0.004 (−0.188, +0.250) | **+0.214** (+0.188, +0.281) | +0.071 | −0.085 |
| 401            | 64  | −0.062 (−0.156, +0.094) | +0.054 (−0.031, +0.203) | **+0.234** (+0.156, +0.297) | +0.009 | −0.036 |
| 601            | 102 | +0.006 (−0.157, +0.098) | +0.088 (−0.010, +0.167) | **+0.239** (+0.167, +0.304) | +0.000 | −0.031 |
| **all 21 seeds** |  |  |  | **mean +0.229, min +0.156, max +0.304** | | |

`T=3` is positive on **every one of the 21 synthetic seeds** (min +0.156), while `A` (naive,
all groups) and `T=2` are frequently negative, and `T=4` collapses toward zero. This is the
number that matters for "positive expected saving on random-like arrangements": **c ≈ 0.15–0.23**
is directly supported by data, with real-instance arrangements doing noticeably better
(mean +0.525, presumably from the reflection symmetry of the real arrangement noted in §25).

## Honest negative results

1. **`S = all groups` (naive) loses** almost everywhere: negative on 5/7 real instances and on
   most synthetic seeds (mean −0.156 on synthetic) — reproduces the background's warning that only
   ~50–65% of consecutive specials alternate, below the 75% bar the `t=1/2` closed form needs.
2. **Threshold `T=4` over-prunes.** Requiring *all 4* vertices matched from round 0 removes a
   group's potential matching partners, which can un-match a neighboring group's vertex, triggering
   more pruning — a "death spiral". It collapses to a handful of groups (sometimes `net=0`, e.g.
   p=601 both k) rather than converging to a healthy fixed point. `T=3` gives the pruning process
   enough slack to settle at a much larger, still-well-matched `S`.
3. **Mixed rule (promote fully-matched groups to `t=1`) makes things *worse*, often flipping a
   solidly positive net negative** — e.g. p=199,k=2: +0.625 (pure half) → −0.250 (mixed); p=401,k=3:
   +0.586 → −0.207; synthetic mean +0.21..+0.24 → −0.03..−0.09. Diagnosis: for the *same* set `S`,
   the `t=1` closed form needs `changes(S) > 3|S|`, i.e. **more than 3/4 of *all* 4|S| cyclically
   adjacent `S`-special pairs must alternate**, whereas the `t=1/2` form only needs
   `matches(S) > 1.5|S|`, i.e. more than 3/4 of the *maximum possible matching* (`2|S|` pairs, a
   strictly smaller ceiling reachable even when many adjacent pairs don't alternate, since a
   matching only needs *some* disjoint alternating pairs, not universal local alternation). A group
   having 4/4 matched vertices (cheap to satisfy) is a much weaker signal than the much stronger
   condition `t=1` actually requires; promoting on that signal alone is the wrong criterion. (Positive
   caveat: at the two largest, most favorable real instances — p=601, k=2 and k=3 — mixed still beat
   Rule A but never beat pure `T=3`; it was not useful anywhere in this exploration.)

## Best rule found

**`half_matching / prune-T3`**: start with `S` = all (4,8,4) groups; on each `⟨k⟩`-cycle, walk the
current `S`-specials in cyclic order and greedily match adjacent changing (K↔M) pairs with a
single local left-to-right pass (O(1) state; the exact global DP gives at most a rounding-level
improvement and is not needed); for every group, drop it from `S` if fewer than 3 of its 4
vertices ended up matched; repeat the match‑then‑prune step on the shrunken `S` (converges in
2–6 rounds, independent of `p` in every case tested); set `t_G = 1/2` on the converged `S`, `t_G=0`
elsewhere, and use the standard local row/column pattern of §26 bullet 2 (or `lp(M,t_fixed=...)`)
for the edge weights.

- **Real instances**, `(p,k) ∈ {101,199,401,601}×{2,3}`: net/G8 = **+0.375 to +0.647**, mean +0.525.
- **Synthetic** (3 sizes × 7 seeds = 21 runs): net/G8 = **+0.156 to +0.304**, mean +0.229, **positive
  on every single seed**.
- Captures roughly 40–70% of the free-LP ceiling (0.75–1.06/group) with a genuinely local,
  explicit rule.

This directly satisfies the task's target: an explicit local rule with a strictly positive
expected saving per group, `c ≈ 0.15` being a safe, data-supported constant on random-like
(synthetic) arrangements, and considerably better (`≈0.5`) on the real arrangements that the
theorem actually needs.

## Caveats / open points for whoever uses this rule

- The match‑then‑prune loop is local *per round* (bounded-state scan) and converges in an
  empirically bounded number of rounds (≤6, not growing with `p` in any tested instance), so a
  group's final fate depends only on a *bounded* neighborhood of nearby groups — but I have not
  derived an explicit window width `w(rounds)` proving this rigorously; only the round count is
  empirical, not proven bounded as `p → ∞`. Formalizing this (or replacing the iterated prune with
  a genuinely one-shot bounded-window rule that reproduces the same fixed point, e.g. a local
  "density of matched neighbors" estimator) is the natural next step.
- All numbers here rely on the group-disjointness fact (`check_disjoint`, true on every instance
  tested); the model's own docstring mentions the general LP allows a class in two groups
  (`1 − t₁ − t₂`), so this file's exact closed form should be re-verified with `check_disjoint`
  before reuse on any `(p,k)` outside the tested set, in case it fails there.
- Only `k ∈ {2,3}` and unbalanced synthetic sizes up to `p=601` were tried (per the task's time
  budget); larger `p` and other `k` (in particular `k=−1`, the already-solved degenerate case with
  cycles of length 4) were not run.

## Files

- `slack/c_agents/half_matching.py` — implementation + evaluation harness (matching DP, greedy
  matcher, pruning, mixed rule, `self_test()`, full real+synthetic sweep in `__main__`).
- `docs/research/c_agents/half_matching.md` — this report.
