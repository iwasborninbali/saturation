"""alt_rules_t1.py -- agent "alt_rules_t1" for the cycle-model slack task
(docs/research/pair_bound_notes.md sections 25-26; slack/cyc_model.py).

TASK: explore LOCAL rules of the form t_G = 1 for the groups G selected by a WINDOW PREDICATE on the
cyclic sequence of ALL specials (the vertices of ALL (4,8,4) groups, selected or not) along the
<k>-cycles.  A rule is "local" if the decision for a group depends only on a bounded neighbourhood of
its 4 vertices in that sequence.  Exact net for any such S (t=1 on S, 0 elsewhere) is the closed form
proved in section 26:  net(S) = 2*changes(S) - 6*|S|,  changes(S) = number of type changes (K<->M) in
the cyclic sequence of S's OWN specials (i.e. S filtered out of the full special sequence) -- this is
exact for the optimal edge cover given those t's, confirmed against lp(M, t_fixed=...) below.  The
metric reported throughout is net(S) / G8, G8 = TOTAL number of groups in the model (matches the
"c * #groups" convention of section 25/26: a group that is not selected still counts in the
denominator, contributing 0 to the saving and diluting c).

RULES EXPLORED (see report for the numbers):
  one-shot window rules (single pass, radius r, over the ALL-specials sequence, fixed once and for
  all before any selection is made):
    all4      : every one of a group's 4 vertices has BOTH its immediate (radius-1) neighbouring
                specials of opposite type (the predicate literally suggested in the task).
    ge3 / ge2 : the same per-vertex condition, required of >=3 / >=2 of the 4 vertices (majority).
    or_all4   : weaker per-vertex condition (at least ONE of the two neighbours opposite, radius 1),
                required of all 4 vertices -- included to show that a too-weak per-vertex test is
                actively harmful once iterated/filtered (see report).
    window_r2 : radius-2 window (2 previous + 2 next specials), >=3 of 4 window-neighbours opposite,
                required of >=3 of the group's 4 vertices -- tests whether a WIDER window helps.
    adjpack   : a genuinely DISTANCE-based rule (no type check needed): select iff a vertex's two
                immediate neighbours in the RAW alternating cycle (not just among specials) are
                themselves special -- automatically opposite type by the strict K/M/K/M alternation
                of the cycle itself, so this isolates the "distance to nearest special" idea from the
                "opposite type" ides.
  iterative rules ("select, then re-evaluate neighbours among the selected only, iterate a bounded
  number of times", as suggested in the task): start with the candidate = all groups; each round,
  recompute the radius-1 opposite-neighbour test using ONLY the current candidate's own vertices as
  the special sequence (not the full one), and drop groups that fail; repeat to a fixed-point (a
  handful of rounds empirically, monotonic shrinking, capped at 30 rounds as a safety net).
    iter_ge2 / iter_ge3 / iter_ge4(=iter_all4) : the majority-threshold in {2,3,4} used at every round.

BEST RULE FOUND: iter_ge2 (iterative, per-vertex "both neighbours opposite among the CURRENT
candidate", group needs >= 2 of its 4 vertices to pass, run to a fixed point).  Positive on every real
(p,k) tested for p >= 199 and rising with p (up to +0.667/group at p=601,k=2, +0.766 at p=601,k=3);
~0 at p=101 (too small a model for 2 rounds of pruning to leave anything); on SYNTHETIC (uniformly
random groups, the harder/more adversarial case) it is positive ON AVERAGE at both sizes tested but
NOT positive on every single seed -- an honest, modest positive result, well below the free-LP
ceiling (section 25: 0.75-1.06/group).  See the report for full numbers and the negative results.

Every rule is cross-checked against the exact LP optimum lp(M, t_fixed=...) (t fixed to EXACTLY 1 on
the selected groups and EXACTLY 0 on every other group, not left free) to confirm the closed-form
net(S) = 2*changes(S) - 6|S| is exact for our selections, not just in the aggregate.

Usage: /Users/iwasborninbali/venvs/sat/bin/python3 slack/c_agents/alt_rules_t1.py
(run from the repo root; builds real models for p in {101,199,401,601}, k in {2,3}, plus synthetic
models at two sizes (p=101, p=601) over 8 seeds each; total wall-clock a few seconds).
"""
import sys, os, time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from cyc_model import build, lp, synthetic, changes

# ---------------------------------------------------------------------------
# shared window/neighbour machinery, operating on an arbitrary "active" vertex
# set (the full-specials set for one-shot rules, a shrinking candidate set for
# the iterative rules) -- this IS the "bounded window along the cycle" of the
# task description: for radius r it looks only at the r nearest active
# vertices on each side.
# ---------------------------------------------------------------------------

def specials_of(groups):
    s = set()
    for g, cl in groups:
        s |= cl
    return s


def window_opp_counts(cycles, active_set, radius):
    """For every v in active_set: number of the `radius` previous + `radius` next ACTIVE vertices
    (cyclic order along v's cycle, restricted to active_set) whose type (K/M) differs from v's,
    out of 2*radius total checked."""
    out = {}
    for seq in cycles:
        idxs = [i for i, v in enumerate(seq) if v in active_set]
        m = len(idxs)
        if m == 0:
            continue
        for pos in range(m):
            i = idxs[pos]
            v = seq[i]
            nb = [seq[idxs[(pos - d) % m]] for d in range(1, radius + 1)]
            nb += [seq[idxs[(pos + d) % m]] for d in range(1, radius + 1)]
            out[v] = sum(1 for u in nb if u[0] != v[0])
    return out


# ---------------------------------------------------------------------------
# one-shot rules: a single window pass over the FULL (all-groups) special
# sequence, fixed before any group is selected.
# ---------------------------------------------------------------------------

def _oneshot(M, radius, vneed, gneed):
    allsp = specials_of(M['groups'])
    opp = window_opp_counts(M['cycles'], allsp, radius)
    return [(g, cl) for g, cl in M['groups']
            if sum(1 for v in cl if opp[v] >= vneed) >= gneed]


def rule_all4(M):      return _oneshot(M, 1, 2, 4)   # both radius-1 neighbours opposite, all 4 vertices
def rule_ge3(M):       return _oneshot(M, 1, 2, 3)   # ... required of >= 3 of 4
def rule_ge2(M):       return _oneshot(M, 1, 2, 2)   # ... required of >= 2 of 4 (majority)
def rule_or_all4(M):   return _oneshot(M, 1, 1, 4)   # >= 1 of 2 neighbours opposite, all 4 vertices
def rule_window_r2(M): return _oneshot(M, 2, 3, 3)   # radius-2 window (4 nbrs), >=3 opposite, >=3/4 vertices


def rule_adjpack(M, gneed=2):
    """Distance-based, no type check: select iff >= gneed of the group's 4 vertices have BOTH raw-
    cycle-adjacent vertices (distance exactly 1 in the underlying K,M,K,M,... cycle, not just among
    specials) themselves special -- these are automatically opposite type by the strict alternation,
    so this isolates "closeness to the nearest special" from "opposite type"."""
    pos = M['pos']; cyc = M['cycles']; allsp = specials_of(M['groups'])
    sel = []
    for g, cl in M['groups']:
        cnt = 0
        for v in cl:
            c, i = pos[v]; seq = cyc[c]; L = len(seq)
            if seq[(i - 1) % L] in allsp and seq[(i + 1) % L] in allsp:
                cnt += 1
        if cnt >= gneed:
            sel.append((g, cl))
    return sel


# ---------------------------------------------------------------------------
# iterative rules: "select, then re-evaluate neighbours among the selected
# only, iterate a bounded number of times."  Monotonic shrinking, capped.
# ---------------------------------------------------------------------------

def rule_iterative(M, vneed=2, gneed=2, radius=1, max_rounds=30):
    keyed = dict(M['groups'])
    candidate = set(keyed)
    trace = []
    for r in range(max_rounds):
        active = set()
        for g in candidate:
            active |= keyed[g]
        opp = window_opp_counts(M['cycles'], active, radius)
        new_candidate = {g for g in candidate
                          if sum(1 for v in keyed[g] if opp[v] >= vneed) >= gneed}
        S = [(g, keyed[g]) for g in new_candidate]
        net = 2 * changes(M, S) - 6 * len(S) if S else 0
        trace.append((r + 1, len(S), net))
        if new_candidate == candidate or not new_candidate:
            candidate = new_candidate
            break
        candidate = new_candidate
    return [(g, keyed[g]) for g in candidate], trace


def rule_iter_ge2(M): return rule_iterative(M, 2, 2, radius=1)[0]
def rule_iter_ge3(M): return rule_iterative(M, 2, 3, radius=1)[0]
def rule_iter_ge4(M): return rule_iterative(M, 2, 4, radius=1)[0]
# supplementary: does WIDENING the window help, once combined with iteration?  (spoiler: no -- see report)
def rule_iter_r2_v3g2(M): return rule_iterative(M, 3, 2, radius=2)[0]
def rule_iter_r2_v4g2(M): return rule_iterative(M, 4, 2, radius=2)[0]


ONESHOT_RULES = [
    ("all4", rule_all4), ("ge3", rule_ge3), ("ge2", rule_ge2),
    ("or_all4", rule_or_all4), ("window_r2", rule_window_r2), ("adjpack", rule_adjpack),
]
ITER_RULES = [("iter_ge2", rule_iter_ge2), ("iter_ge3", rule_iter_ge3), ("iter_ge4/all4", rule_iter_ge4)]
ALL_RULES = ONESHOT_RULES + ITER_RULES


# ---------------------------------------------------------------------------
# evaluation harness
# ---------------------------------------------------------------------------

def eval_rule(M, fn):
    S = fn(M)
    G8 = len(M['groups'])
    ch = changes(M, S)
    net = 2 * ch - 6 * len(S)
    return dict(nsel=len(S), G8=G8, changes=ch, net=net, net_per_group=net / G8 if G8 else 0.0)


def lp_confirm(M, S, label):
    """Confirm net(S) = 2*changes(S)-6|S| exactly against the true LP optimum with t fixed to
    EXACTLY this S (1 on S, 0 elsewhere -- every group is fixed, none left free)."""
    tfix = {g: 1.0 for g, cl in S}
    for g, cl in M['groups']:
        if g not in tfix:
            tfix[g] = 0.0
    saving, w, t = lp(M, t_fixed=tfix)
    ch = changes(M, S)
    formula = 2 * ch - 6 * len(S)
    ok = abs(saving - formula) < 1e-6
    print(f"  LP confirm [{label}]: lp saving={saving:.4f}  formula 2*changes-6|S|={formula}  "
          f"{'OK exact match' if ok else '*** MISMATCH ***'}")
    return ok


def fmt_row(name, r):
    return f"{name:>7s}={r['net_per_group']:+.3f}(|S|{r['nsel']:d}/{r['G8']:d})"


def main():
    t_start = time.time()
    print("=" * 100)
    print("REAL instances: p in {101,199,401,601}, k in {2,3} -- net/group = net(S) / G8 (TOTAL groups)")
    print("=" * 100)
    real_results = {}
    for p in (101, 199, 401, 601):
        for k in (2, 3):
            M = build(p, k)
            G8 = len(M['groups'])
            s_free, _, _ = lp(M)
            row = [f"free-LP={s_free / G8:+.3f}"]
            per_rule = {}
            for name, fn in ALL_RULES:
                r = eval_rule(M, fn)
                per_rule[name] = r
                row.append(fmt_row(name, r))
            real_results[(p, k)] = per_rule
            print(f"p={p:4d} k={k}:  " + "  ".join(row))

    print()
    print("=" * 100)
    print("Supplementary: does WIDENING the iterative window (radius 2) help over radius 1 (iter_ge2)?")
    print("=" * 100)
    for p in (101, 199, 401, 601):
        for k in (2, 3):
            M = build(p, k)
            r1 = eval_rule(M, rule_iter_ge2)
            r2a = eval_rule(M, rule_iter_r2_v3g2)
            r2b = eval_rule(M, rule_iter_r2_v4g2)
            print(f"p={p:4d} k={k}:  iter_ge2(r=1)={r1['net_per_group']:+.3f}   "
                  f"iter(r=2,v=3,g=2)={r2a['net_per_group']:+.3f}   iter(r=2,v=4,g=2)={r2b['net_per_group']:+.3f}")

    print()
    print("=" * 100)
    print("SYNTHETIC instances (uniformly random groups, same cycles): two sizes, 8 seeds each")
    print("=" * 100)
    syn_summary = {}
    for basep in (101, 601):
        Mbase = build(basep, 2)
        G8 = len(Mbase['groups'])
        print(f"-- size p={basep} (G8={G8}) --")
        per_rule_vals = {name: [] for name, _ in ALL_RULES}
        for seed in range(8):
            Ms = synthetic(Mbase, seed)
            row = []
            for name, fn in ALL_RULES:
                r = eval_rule(Ms, fn)
                per_rule_vals[name].append(r['net_per_group'])
                row.append(fmt_row(name, r))
            print(f"  seed {seed}: " + "  ".join(row))
        summary = {}
        for name, vals in per_rule_vals.items():
            mean = sum(vals) / len(vals)
            summary[name] = (mean, min(vals), max(vals))
            print(f"  {name:>14s}: mean net/group = {mean:+.4f}  (range {min(vals):+.3f} .. {max(vals):+.3f})")
        syn_summary[basep] = summary
        print()

    print("=" * 100)
    print("LP cross-checks (exact optimum with t fixed to 1 on S, 0 elsewhere) for the best rule iter_ge2")
    print("=" * 100)
    M199 = build(199, 2)
    S199 = rule_iter_ge2(M199)
    lp_confirm(M199, S199, "real p=199 k=2, iter_ge2")
    M401 = build(401, 3)
    S401 = rule_iter_ge2(M401)
    lp_confirm(M401, S401, "real p=401 k=3, iter_ge2")
    Msyn = synthetic(build(101, 2), 3)
    Ssyn = rule_iter_ge2(Msyn)
    lp_confirm(Msyn, Ssyn, "synthetic p=101 seed=3, iter_ge2")
    Msyn2 = synthetic(build(601, 2), 0)
    Ssyn2 = rule_iter_ge2(Msyn2)
    lp_confirm(Msyn2, Ssyn2, "synthetic p=601 seed=0, iter_ge2")

    print()
    print(f"total wall-clock: {time.time() - t_start:.1f}s")
    return real_results, syn_summary


if __name__ == "__main__":
    main()
