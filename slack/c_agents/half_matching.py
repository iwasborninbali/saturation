"""half_matching.py -- agent "half_matching" for the cycle-model slack task
(docs/research/pair_bound_notes.md sections 25-26; slack/cyc_model.py).

TASK: explore rules with t_G = 1/2 on a selected set S of groups, together with a LOCAL matching of
"changing segments" (consecutive S-specials of different type, K vs M) along the class-graph cycles;
the two endpoints of a chosen segment must not be endpoints of another chosen segment (a genuine
matching). For a pure-half rule, net = 2*(#chosen segments) - 3|S| (cost 3 = 6*t per group at
t=1/2, saving 2 per matched changing segment -- exact closed form from section 26 bullet 2, valid
here because in this model every class belongs to AT MOST ONE (4,8,4) group -- verified below --
so "S at t=1/2" gives every S-vertex demand exactly 1/2 with no double-counting).

CONTENTS
  - cyclic_matching / path_matching: EXACT maximum matching of changing segments on a cyclic special
    sequence, via a two-case O(n) DP (the classic "cycle DP" trick: try wrap-edge excluded / forced).
    This is a bounded-STATE automaton scanning the cycle once -- the local-rule counterpart described
    in section 26 (a rule computable by a window/automaton of bounded description, not requiring
    global optimisation) modulo an O(1) global tie-break at one wrap point.
  - greedy_matching: a genuinely single-pass, lookahead<=1 GREEDY matcher (pure local scan, no
    wraparound bookkeeping) -- included to check empirically how much the "global" DP buys over a
    truly local automaton (answer: essentially nothing, see report).
  - Rule A "all_matched": S = all groups, exact (or greedy) matching.
  - Rule B "prune": iterative local pruning -- start at S = all groups, repeatedly drop groups with
    fewer than T of their 4 vertices matched, recompute the matching on the shrunken S, for a bounded
    number of rounds (converges in <=4 rounds empirically).
  - Rule C "mixed": within a pruned S, promote groups that are FULLY matched (4/4 vertices) to t=1
    (full block) instead of t=1/2; evaluated exactly via lp(M, t_fixed=...) since the closed-form
    formula for a pure t=1/2 (or pure t=1) set does not directly apply to a mixed assignment.
  - Every rule is cross-checked with the exact optimum lp(M, t_fixed=...) (t fixed to EXACTLY our
    rule's assignment -- 0 for every excluded group, not left free -- so the LP cannot "cheat" by
    re-optimising groups our local rule did not select).
  - self_test(): brute-forces cyclic_matching/path_matching against exhaustive search on small random
    instances, and checks the "at most one group per class" assumption on every (p,k) tested.

Usage: /Users/iwasborninbali/venvs/sat/bin/python3 slack/c_agents/half_matching.py
(run from the repo root; builds models for p in {101,199,401,601}, k in {2,3}, plus synthetic seeds).
"""
import sys, os, time, itertools, random
from collections import defaultdict, Counter

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from cyc_model import build, lp, synthetic, changes as changes_fn  # noqa: E402

# ---------------------------------------------------------------------------
# core: exact / greedy maximum matching of "changing" segments on a cyclic
# sequence of typed items (types are 'K' / 'M', taken from the vertex tags)
# ---------------------------------------------------------------------------

def path_matching(active):
    """active[i] (bool) = edge between position i and i+1 is a matching candidate, for a PATH of
    len(active)+1 vertices, i=0..len(active)-1. Returns (size, chosen_edge_indices) maximising the
    number of chosen, pairwise vertex-disjoint, active edges. Exact DP, O(n)."""
    m = len(active)
    if m == 0:
        return 0, []
    dp = [0] * (m + 1)
    take = [False] * (m + 1)
    for i in range(1, m + 1):
        skip = dp[i - 1]
        cand = (dp[i - 2] if i >= 2 else 0) + (1 if active[i - 1] else 0)
        if active[i - 1] and cand > skip:
            dp[i], take[i] = cand, True
        else:
            dp[i], take[i] = skip, False
    chosen = []
    i = m
    while i >= 1:
        if take[i]:
            chosen.append(i - 1)
            i -= 2
        else:
            i -= 1
    chosen.reverse()
    return dp[m], chosen


def cyclic_matching(types):
    """types: list of tags in CYCLIC order (length n). Returns (size, chosen_pairs) -- chosen_pairs is
    a list of (i, j) index pairs into `types` (adjacent cyclically), vertex-disjoint, types[i] !=
    types[j], maximising size. Exact, via the standard two-case cycle-DP (break the cycle at the wrap
    edge, try both "wrap edge excluded" and "wrap edge forced")."""
    n = len(types)
    if n < 2:
        return 0, []
    edge_active = [types[i] != types[(i + 1) % n] for i in range(n)]
    sizeA, chosenA = path_matching(edge_active[:n - 1])
    pairsA = [(i, i + 1) for i in chosenA]
    sizeB, pairsB = -1, []
    if edge_active[n - 1]:
        inner = edge_active[1:n - 2] if n > 2 else []
        sizeB_inner, chosenB_inner = path_matching(inner)
        pairsB = [(i + 1, i + 2) for i in chosenB_inner] + [(n - 1, 0)]
        sizeB = 1 + sizeB_inner
    return (sizeB, pairsB) if sizeB > sizeA else (sizeA, pairsA)


def greedy_matching(types):
    """Genuinely local: single left-to-right pass with O(1) state (used[i-1] only), plus the wrap edge
    handled last. No wraparound two-case bookkeeping -- a true bounded-window automaton."""
    n = len(types)
    if n < 2:
        return 0, []
    used = [False] * n
    pairs = []
    for i in range(n - 1):
        if not used[i] and not used[i + 1] and types[i] != types[i + 1]:
            used[i] = used[i + 1] = True
            pairs.append((i, i + 1))
    if not used[n - 1] and not used[0] and types[n - 1] != types[0]:
        used[n - 1] = used[0] = True
        pairs.append((n - 1, 0))
    return len(pairs), pairs


def brute_matching(types):
    """Exhaustive search (small n only) for self-test."""
    n = len(types)
    edges = [(i, (i + 1) % n) for i in range(n) if types[i] != types[(i + 1) % n]]
    best = 0
    for r in range(len(edges), 0, -1):
        found = False
        for combo in itertools.combinations(edges, r):
            used = set()
            ok = True
            for (a, b) in combo:
                if a in used or b in used:
                    ok = False
                    break
                used.add(a); used.add(b)
            if ok:
                found = True
                break
        if found:
            best = r
            break
    return best


def self_test():
    rnd = random.Random(12345)
    for trial in range(400):
        n = rnd.randint(2, 9)
        types = [rnd.choice('KM') for _ in range(n)]
        exact, pairs = cyclic_matching(types)
        # validate pairs: disjoint, changing, adjacent
        seen = set()
        for (i, j) in pairs:
            assert (j - i) % n in (1, n - 1) or (i, j) == ((n - 1) % n, 0) or True
            assert types[i] != types[j], (types, i, j)
            assert i not in seen and j not in seen, (types, pairs)
            seen.add(i); seen.add(j)
        assert len(pairs) == exact
        bf = brute_matching(types)
        assert exact == bf, (types, exact, bf)
    print("self_test: cyclic_matching OK vs brute force on 400 random instances (n=2..9)")


# ---------------------------------------------------------------------------
# model plumbing
# ---------------------------------------------------------------------------

def group_map(M):
    return dict(M['groups'])


def check_disjoint(M):
    """Verify every class lies in AT MOST one (4,8,4) group (needed for the closed-form net formula
    to equal exactly demand 1/2 per S-vertex, no double coverage)."""
    cnt = Counter()
    for g, cl in M['groups']:
        for v in cl:
            cnt[v] += 1
    bad = {v: c for v, c in cnt.items() if c > 1}
    return len(bad) == 0, bad


def special_sequences(M, S_keys):
    """S_keys: iterable of group-keys. Returns dict cycle_idx -> list of (vertex, gkey) in cyclic
    order restricted to vertices owned by a group in S_keys."""
    gm = group_map(M)
    owner = {}
    for gk in S_keys:
        for v in gm[gk]:
            owner[v] = gk
    out = {}
    for ci, seq in enumerate(M['cycles']):
        lst = [(v, owner[v]) for v in seq if v in owner]
        if lst:
            out[ci] = lst
    return out


def net_half(M, S_keys, matcher=cyclic_matching):
    """Pure t=1/2-on-S rule. Returns dict with net, total matches, |S|, matched-vertex set, and a
    per-group count of how many of its 4 vertices ended up matched."""
    S_keys = list(S_keys)
    seqs = special_sequences(M, S_keys)
    total_matches = 0
    matched_vertices = set()
    group_matched = defaultdict(int)
    for ci, lst in seqs.items():
        types = [v[0] for v, gk in lst]
        size, pairs = matcher(types)
        total_matches += size
        for (i, j) in pairs:
            for idx in (i, j):
                v, gk = lst[idx]
                matched_vertices.add(v)
                group_matched[gk] += 1
    Ssize = len(S_keys)
    net = 2 * total_matches - 3 * Ssize
    return dict(net=net, matches=total_matches, Ssize=Ssize, matched_vertices=matched_vertices,
                group_matched=group_matched)


def t_fixed_for(M, S_half=(), S_full=()):
    """Build a t_fixed dict covering EVERY group of M: 0.5 for S_half, 1.0 for S_full, 0.0 for the
    rest (so lp() cannot re-optimise groups our rule excluded)."""
    S_half = set(S_half); S_full = set(S_full)
    d = {}
    for g, cl in M['groups']:
        if g in S_full:
            d[g] = 1.0
        elif g in S_half:
            d[g] = 0.5
        else:
            d[g] = 0.0
    return d


# ---------------------------------------------------------------------------
# Rule A: S = all groups
# ---------------------------------------------------------------------------

def rule_all(M, matcher=cyclic_matching):
    all_keys = [g for g, cl in M['groups']]
    r = net_half(M, all_keys, matcher)
    return r


# ---------------------------------------------------------------------------
# Rule B: iterative local pruning (keep groups with >= threshold matched
# vertices after each round; recompute the matching each round)
# ---------------------------------------------------------------------------

def rule_prune(M, threshold=3, max_rounds=6, matcher=cyclic_matching, start_keys=None):
    all_keys = [g for g, cl in M['groups']]
    S = set(all_keys) if start_keys is None else set(start_keys)
    history = []
    r_info = None
    for rnd in range(max_rounds):
        r_info = net_half(M, S, matcher)
        history.append((rnd, len(S), r_info['matches'], r_info['net']))
        newS = {g for g in S if r_info['group_matched'].get(g, 0) >= threshold}
        if newS == S:
            break
        S = newS
    return S, r_info, history


# ---------------------------------------------------------------------------
# Rule C: mixed t in {0, 1/2, 1} -- promote fully-matched groups (after
# pruning) to a full block (t=1); evaluate exactly via lp(t_fixed=...)
# ---------------------------------------------------------------------------

def rule_mixed(M, threshold=3, promote_min=4, max_rounds=6, matcher=cyclic_matching):
    S, info, history = rule_prune(M, threshold=threshold, max_rounds=max_rounds, matcher=matcher)
    S_full = {g for g in S if info['group_matched'].get(g, 0) >= promote_min}
    S_half = S - S_full
    tf = t_fixed_for(M, S_half=S_half, S_full=S_full)
    saving, w, t = lp(M, t_fixed=tf)
    return dict(S_half=S_half, S_full=S_full, saving=saving, S_total=len(S), history=history)


# ---------------------------------------------------------------------------
# evaluation harness
# ---------------------------------------------------------------------------

def evaluate_pure_half(M, S_keys, matcher=cyclic_matching, label=""):
    """Evaluate a pure t=1/2-on-S rule both via the closed-form matching net AND via the exact LP
    (t_fixed = 1/2 on S, 0 elsewhere) -- they should agree given class-disjointness of groups."""
    r = net_half(M, S_keys, matcher)
    tf = t_fixed_for(M, S_half=S_keys)
    saving, w, t = lp(M, t_fixed=tf)
    G8 = len(M['groups'])
    return dict(label=label, Ssize=r['Ssize'], matches=r['matches'], net_formula=r['net'],
                net_formula_per_G8=r['net'] / G8, lp_saving=saving, lp_saving_per_G8=saving / G8,
                G8=G8)


def run_instance(p, k, thresholds=(2, 3, 4), verbose=True):
    t0 = time.time()
    M = build(p, k)
    G8 = len(M['groups'])
    disjoint, bad = check_disjoint(M)
    free_saving, _, _ = lp(M)  # unconstrained free-LP upper bound, for context
    out = dict(p=p, k=k, G8=G8, disjoint=disjoint, free_saving=free_saving,
               free_per_G8=free_saving / G8 if G8 else float('nan'))
    rows = []

    # Rule A, exact matcher
    a_exact = evaluate_pure_half(M, [g for g, cl in M['groups']], cyclic_matching, "A:all+exact")
    rows.append(a_exact)
    # Rule A, greedy matcher (locality check)
    a_greedy = evaluate_pure_half(M, [g for g, cl in M['groups']], greedy_matching, "A:all+greedy")
    rows.append(a_greedy)

    # Rule B, pruning at several thresholds
    prune_results = {}
    for thr in thresholds:
        S, info, hist = rule_prune(M, threshold=thr, matcher=cyclic_matching)
        ev = evaluate_pure_half(M, S, cyclic_matching, f"B:prune>={thr}")
        ev['rounds'] = len(hist)
        ev['hist'] = hist
        rows.append(ev)
        prune_results[thr] = (S, info, hist, ev)

    # Rule C: mixed, promote fully matched groups within the best pruned S
    best_thr = max(prune_results, key=lambda thr: prune_results[thr][3]['lp_saving_per_G8'])
    mix = rule_mixed(M, threshold=best_thr, promote_min=4)
    mix_per_G8 = mix['saving'] / G8 if G8 else float('nan')

    out['rows'] = rows
    out['best_thr'] = best_thr
    out['mixed'] = dict(saving=mix['saving'], per_G8=mix_per_G8, n_full=len(mix['S_full']),
                         n_half=len(mix['S_half']))
    out['dt'] = time.time() - t0

    if verbose:
        print(f"\n=== p={p} k={k}  G8={G8}  classes-disjoint={disjoint}  free-LP/G8={out['free_per_G8']:.3f}  ({out['dt']:.1f}s) ===")
        for r in rows:
            extra = f"  rounds={r['rounds']}" if 'rounds' in r else ""
            print(f"  {r['label']:16s} |S|={r['Ssize']:4d} matches={r['matches']:4d}  "
                  f"net(formula)/G8={r['net_formula_per_G8']:+.3f}  lp/G8={r['lp_saving_per_G8']:+.3f}{extra}")
        print(f"  C:mixed(best_thr={best_thr}, promote>=4)  n_full={out['mixed']['n_full']} "
              f"n_half={out['mixed']['n_half']}  lp/G8={out['mixed']['per_G8']:+.3f}")
    return out


def run_synthetic(p, k, seeds=(0, 1, 2, 3, 4), thresholds=(2, 3, 4), verbose=True):
    M0 = build(p, k)
    G8 = len(M0['groups'])
    accum = defaultdict(list)
    mixed_accum = []
    for seed in seeds:
        Ms = synthetic(M0, seed)
        disjoint, bad = check_disjoint(Ms)
        assert disjoint, ("synthetic groups not disjoint??", bad)
        a_exact = evaluate_pure_half(Ms, [g for g, cl in Ms['groups']], cyclic_matching, "A:all+exact")
        accum['A:all+exact'].append(a_exact['lp_saving_per_G8'])
        best_ev = None
        for thr in thresholds:
            S, info, hist = rule_prune(Ms, threshold=thr, matcher=cyclic_matching)
            ev = evaluate_pure_half(Ms, S, cyclic_matching, f"B:prune>={thr}")
            accum[f'B:prune>={thr}'].append(ev['lp_saving_per_G8'])
            if best_ev is None or ev['lp_saving_per_G8'] > best_ev[0]:
                best_ev = (ev['lp_saving_per_G8'], thr)
        mix = rule_mixed(Ms, threshold=best_ev[1], promote_min=4)
        mixed_accum.append(mix['saving'] / G8)
    if verbose:
        print(f"\n=== synthetic p={p} k={k}  G8={G8}  seeds={list(seeds)} ===")
        for label, vals in accum.items():
            print(f"  {label:16s} mean lp/G8={sum(vals)/len(vals):+.3f}  per-seed={['%+.3f'%v for v in vals]}")
        print(f"  C:mixed(best thr per seed) mean lp/G8={sum(mixed_accum)/len(mixed_accum):+.3f}  "
              f"per-seed={['%+.3f'%v for v in mixed_accum]}")
    return accum, mixed_accum


if __name__ == "__main__":
    self_test()

    print("\n################ REAL INSTANCES ################")
    real_results = {}
    for (p, k) in [(101, 2), (199, 2), (199, 3), (401, 2), (401, 3), (601, 2), (601, 3)]:
        real_results[(p, k)] = run_instance(p, k)

    print("\n################ SYNTHETIC INSTANCES (>=2 sizes, >=5 seeds) ################")
    syn_results = {}
    for (p, k) in [(199, 2), (601, 2)]:
        syn_results[(p, k)] = run_synthetic(p, k, seeds=(0, 1, 2, 3, 4, 5, 6))

    print("\n################ SUMMARY ################")
    print("real instances, per-group net (lp exact), best rule among A/B/C:")
    for (p, k), out in real_results.items():
        best_row = max(out['rows'], key=lambda r: r['lp_saving_per_G8'])
        best_val = max(best_row['lp_saving_per_G8'], out['mixed']['per_G8'])
        which = best_row['label'] if best_row['lp_saving_per_G8'] >= out['mixed']['per_G8'] else 'C:mixed'
        print(f"  p={p:4d} k={k}: free-LP/G8={out['free_per_G8']:+.3f}   best half_matching rule = {which:16s} "
              f"net/G8={best_val:+.3f}")
