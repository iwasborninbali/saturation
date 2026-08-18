"""local_search_structure.py — c_agents task "local_search_structure" (see docs/research/pair_bound_notes.md
sections 25-26 and slack/cyc_model.py for the model).

Question: in the class-graph cover LP (cyc_model.lp), each (4,8,4) group gets an optimal weight
t_G in {0, 1/2, 1}.  What LOCAL feature of a group's 4 vertices -- computed from the cyclic order of
ALL specials (= union of every group's vertex set, known up front, independent of which groups end up
selected) -- predicts t_G?  We build 5 such features (all from nearest-neighbour distances/parities in
that cyclic order), fit small decision rules (a plain-Python CART, no sklearn in this venv, plus an
exhaustively-searched single-feature threshold rule) on TRAIN = real p=199 (k=2,k=3) + synthetic p=199
(seeds 0,1,2), and evaluate the resulting EXPLICIT rules via cyc_model.lp(M, t_fixed=...) on held-out
real (p,k) in {(101,2),(401,2),(401,3),(601,2)} and synthetic p=401 (seeds 0,1,2).

HEADLINE RESULT (see docs/research/c_agents/local_search_structure.md for the full writeup):
  - The STRICT binary rule the task asks for (t=1 on predicted groups, else 0) does NOT beat "do
    nothing" here: even the best rule found nets <= 0 per group on held-out data (honest negative --
    forcing every group's t to {0,1} throws away the 40-80% of groups whose true optimum is t=1/2,
    and even an ORACLE 0/1-only assignment has a near-zero or negative ceiling at these p).
  - Allowing the SAME kind of local rule to also output t=1/2 (still explicit/local/bounded-window,
    just not literally binary) flips the sign: the single-feature rule "t=1 if n_odd>=8, t=1/2 if
    4<=n_odd<8, else t=0" (n_odd = count, over the group's 4 vertices' 8 sides, of sides whose nearest
    other special is at ODD distance) nets +0.35/group on TRAIN and +0.35-0.41/group on EVERY held-out
    instance (real and synthetic alike) -- about 44% of the free LP's own saving, from one feature.

Run:  /Users/iwasborninbali/venvs/sat/bin/python3 slack/c_agents/local_search_structure.py
"""
import sys, os, time, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import cyc_model as cm

# ---------------------------------------------------------------- feature extraction --------------

def specials_of(M):
    s = set()
    for g, cl in M['groups']:
        s |= cl
    return s

def local_context(M):
    """For every special vertex v (member of some group): the nearest OTHER special before/after it
    along its own cycle, among ALL specials (all groups' vertices, not just a candidate subset S).
    Returns v -> dict(dist_prev, type_prev, dist_next, type_next).  Distances are in #vertices (edges)
    along the cycle; type in {'K','M',None} (None only if v is the sole special on its whole cycle)."""
    specials = specials_of(M)
    ctx = {}
    for seq in M['cycles']:
        L = len(seq)
        sp = [i for i, v in enumerate(seq) if v in specials]
        n = len(sp)
        if n == 0:
            continue
        for r, i in enumerate(sp):
            v = seq[i]
            if n == 1:
                ctx[v] = dict(dist_prev=L, type_prev=None, dist_next=L, type_next=None)
                continue
            i_next = sp[(r + 1) % n]; i_prev = sp[(r - 1) % n]
            ctx[v] = dict(dist_prev=(i - i_prev) % L, type_prev=seq[i_prev][0],
                           dist_next=(i_next - i) % L, type_next=seq[i_next][0])
    return ctx

def check_alternation_fact(M):
    """Sanity check baked into the model: cycles are built K,M,K,M,... strictly, so along ANY cycle the
    type of a vertex is determined by the PARITY of its index (even=K, odd=M); consequently a special's
    'previous/next special' has a DIFFERENT type iff the distance to it is ODD -- always, no exception.
    In particular the immediate cycle-neighbour (row-mate/column-mate, distance 1) of any vertex is
    ALWAYS of the opposite type. We verify this here rather than assume it."""
    ctx = local_context(M)
    for v, c in ctx.items():
        if c['type_prev'] is not None:
            assert (c['type_prev'] != v[0]) == (c['dist_prev'] % 2 == 1)
        if c['type_next'] is not None:
            assert (c['type_next'] != v[0]) == (c['dist_next'] % 2 == 1)
    return True

def group_features(cl, ctx):
    """Aggregate, permutation-symmetric (over the group's 2 K + 2 M vertices) features of a group,
    built only from the local_context of its 4 members -- i.e. from a WINDOW around the group in the
    cyclic order of all specials.  8 'sides' = (dist_prev, dist_next) for each of the 4 vertices."""
    dists = []; per_vertex_min = []; n_adj = 0; n_odd = 0
    for v in cl:
        c = ctx[v]
        dp, dn = c['dist_prev'], c['dist_next']
        dists += [dp, dn]
        n_adj += (dp == 1) + (dn == 1)          # row/col-mate is itself special (always opposite type)
        n_odd += (dp % 2 == 1) + (dn % 2 == 1)   # side would form an ALTERNATING (K<->M) pair if both ends were picked
        per_vertex_min.append(min(dp, dn))
    return {
        'min_dist':   min(dists),                  # closest other special to ANY of the 4 vertices
        'max_of_min': max(per_vertex_min),          # worst-connected of the 4 vertices (isolation)
        'mean_dist':  sum(dists) / len(dists),
        'n_adj':      n_adj,       # in [0,8]: # of sides whose neighbour-in-all-specials is immediately adjacent
        'n_odd':      n_odd,       # in [0,8]: # of sides at odd distance (neighbour-in-all-specials is opposite type)
    }

FEATURE_NAMES = ['min_dist', 'max_of_min', 'mean_dist', 'n_adj', 'n_odd']

def classify_t(t, lo=0.05, hi=0.95):
    if t <= lo: return 0
    if t >= hi: return 1
    return None  # ~1/2, ambiguous -- excluded from the binary fit (see report)

def classify_t3(t):
    """3-way label used only for the bonus (non-binary) rule in the report: 0 / 1/2 / 1."""
    if t <= 0.25: return 0.0
    if t >= 0.75: return 1.0
    return 0.5

# ---------------------------------------------------------------- instance collection --------------

def collect(M, tag):
    """Runs the free LP once on M; returns (rows, saving) where rows has one dict per group with its
    local features and its free-LP-optimal t (and the 0/1 label, or None if t is close to 1/2)."""
    check_alternation_fact(M)
    ctx = local_context(M)
    saving, _, t = cm.lp(M)
    rows = []
    for g, cl in M['groups']:
        rows.append(dict(key=g, tag=tag, feats=group_features(cl, ctx), t=float(t[g]),
                          label=classify_t(t[g]), label3=classify_t3(t[g])))
    return rows, saving

_BUILD_CACHE = {}
def cached_build(p, k):
    if (p, k) not in _BUILD_CACHE:
        _BUILD_CACHE[(p, k)] = cm.build(p, k)
    return _BUILD_CACHE[(p, k)]

def instance_from_spec(item):
    if item[0] == 'real':
        _, p, k, tag = item
        return cached_build(p, k), tag
    else:
        _, p, k, seed, tag = item
        return cm.synthetic(cached_build(p, k), seed), tag

# ---------------------------------------------------------------- tiny CART (no sklearn available) --
# Works for binary (y in {0,1}) or 3-way (y in {0,0.5,1}) labels alike -- gini/majority-vote are generic.

def gini(y):
    n = len(y)
    if n == 0: return 0.0
    from collections import Counter
    cnt = Counter(y)
    return 1 - sum((c / n) ** 2 for c in cnt.values())

def majority(y):
    from collections import Counter
    cnt = Counter(y)
    return max(cnt.items(), key=lambda kv: (kv[1], -kv[0] if kv[0] is not None else 0))[0]

def best_split(X, y, names):
    n = len(y); base = gini(y); best = None
    for name in names:
        vals = sorted(set(row[name] for row in X))
        for a, b in zip(vals, vals[1:]):
            thr = (a + b) / 2.0
            ly = [y[i] for i in range(n) if X[i][name] <= thr]
            ry = [y[i] for i in range(n) if X[i][name] > thr]
            if not ly or not ry: continue
            g = (len(ly) * gini(ly) + len(ry) * gini(ry)) / n
            gain = base - g
            if best is None or gain > best[0] + 1e-12:
                best = (gain, name, thr)
    return best

def build_tree(X, y, names, depth=0, max_depth=3, min_leaf=25):
    n = len(y)
    node = {'n': n, 'pred': majority(y) if n else 0, 'purity': 1 - gini(y)}
    if depth >= max_depth or n < 2 * min_leaf or gini(y) == 0.0:
        return node
    sp = best_split(X, y, names)
    if sp is None or sp[0] <= 1e-9:
        return node
    gain, name, thr = sp
    li = [i for i in range(n) if X[i][name] <= thr]; ri = [i for i in range(n) if X[i][name] > thr]
    if len(li) < min_leaf or len(ri) < min_leaf:
        return node
    node['split'] = (name, thr)
    node['left'] = build_tree([X[i] for i in li], [y[i] for i in li], names, depth + 1, max_depth, min_leaf)
    node['right'] = build_tree([X[i] for i in ri], [y[i] for i in ri], names, depth + 1, max_depth, min_leaf)
    return node

def predict_tree(node, feats):
    if 'split' not in node: return node['pred']
    name, thr = node['split']
    return predict_tree(node['left'] if feats[name] <= thr else node['right'], feats)

def print_tree(node, names, indent=''):
    if 'split' not in node:
        print(f"{indent}-> predict {node['pred']}  (n={node['n']}, purity={node['purity']:.2f})")
        return
    name, thr = node['split']
    print(f"{indent}if {name} <= {thr:g}:")
    print_tree(node['left'], names, indent + '  ')
    print(f"{indent}else ({name} > {thr:g}):")
    print_tree(node['right'], names, indent + '  ')

# ---------------------------------------------------------------- explicit rules --------------------
# Each rule is a function feats -> 0/1 ("t=1 on predicted groups, else 0").  Kept as plain closures so
# they double as the literal "explicit local rule" the task asks for (bounded window: 5 numbers computed
# from the 4 group vertices' nearest neighbours in the full specials order).

def rule_always0(feats): return 0
def rule_always1(feats): return 1
def rule_always_half(feats): return 0.5
def rule_adj1(feats):    return 1 if feats['n_adj'] >= 1 else 0
def rule_adj2(feats):    return 1 if feats['n_adj'] >= 2 else 0
def rule_odd_maj(feats): return 1 if feats['n_odd'] >= 5 else 0     # more odd- than even-distance sides
def rule_isolated(feats):return 1 if feats['max_of_min'] >= 6 else 0  # the OPPOSITE intuition: reward isolation
def rule_crowded(feats): return 1 if feats['min_dist'] <= 2 else 0

def make_tree_rule(tree):
    return lambda feats: predict_tree(tree, feats)

def fit_threshold_rule(spec, feature='n_odd', values=range(0, 9), three_way=True):
    """Fit a 1-2 threshold rule on a SINGLE feature by directly maximising the LP net/group on `spec`
    (an exhaustive grid search over integer thresholds, not a gini proxy -- still an explicit, local,
    bounded-window rule). three_way=True allows a middle t=1/2 band (lo<=v<hi); False fits a plain
    binary t=1-iff-v>=thr rule."""
    best = None
    for hi in values:
        los = values if three_way else [hi]
        for lo in los:
            if lo > hi: continue
            def rule(feats, lo=lo, hi=hi, feature=feature, three_way=three_way):
                v = feats[feature]
                if v >= hi: return 1.0
                if three_way and v >= lo: return 0.5
                return 0.0
            res = eval_rules_on_spec(spec, {'r': rule})['r']
            net = sum(r['saving'] for r in res) / sum(r['n_groups'] for r in res)
            if best is None or net > best[0]:
                best = (net, lo, hi)
    net, lo, hi = best
    def final_rule(feats, lo=lo, hi=hi, feature=feature, three_way=three_way):
        v = feats[feature]
        if v >= hi: return 1.0
        if three_way and v >= lo: return 0.5
        return 0.0
    return final_rule, lo, hi, net

HAND_RULES = {
    'always0': rule_always0, 'always1': rule_always1,
    'adj>=1': rule_adj1, 'adj>=2': rule_adj2,
    'odd>=5': rule_odd_maj, 'isolated(maxmin>=6)': rule_isolated, 'crowded(min<=2)': rule_crowded,
}

# ---------------------------------------------------------------- evaluation on real LP --------------

def eval_rule_on_instance(M, rule, ctx=None):
    if ctx is None: ctx = local_context(M)
    t_fixed = {g: float(rule(group_features(cl, ctx))) for g, cl in M['groups']}
    saving, w, t = cm.lp(M, t_fixed=t_fixed)
    return saving, saving / len(M['groups'])

def eval_rules_on_spec(spec, rules):
    """rules: dict name->fn. Returns {name: [ {tag,p,k,n_groups,saving,net}, ... ]} evaluating ALL rules
    on the same built instances (one build + one local_context per instance, |rules| LPs per instance)."""
    out = {name: [] for name in rules}
    for item in spec:
        M, tag = instance_from_spec(item)
        p, k = M['p'], M['k']
        ctx = local_context(M)
        for name, rule in rules.items():
            saving, net = eval_rule_on_instance(M, rule, ctx)
            out[name].append(dict(tag=tag, p=p, k=k, n_groups=len(M['groups']), saving=saving, net=net))
    return out

# ---------------------------------------------------------------- main pipeline ----------------------
# Two training sets are tried: TRAIN_REAL (the actual arithmetic arrangement, p=199, k=2 and k=3 -- what
# theorem C is ultimately about) and TRAIN_MIXED (adds the 3 synthetic p=199 seeds, as the task's step 1
# literally lists).  Both are evaluated on the SAME held-out set, split into its real and synthetic parts
# because (see report) the two behave very differently for a 0/1-only rule.

TRAIN_REAL_SPEC = [
    ('real', 199, 2, 'real(199,2)'),
    ('real', 199, 3, 'real(199,3)'),
]
TRAIN_SYN_SPEC = [
    ('syn', 199, 2, 0, 'syn(199,2,seed0)'),
    ('syn', 199, 2, 1, 'syn(199,2,seed1)'),
    ('syn', 199, 2, 2, 'syn(199,2,seed2)'),
]
TRAIN_MIXED_SPEC = TRAIN_REAL_SPEC + TRAIN_SYN_SPEC

TEST_REAL_SPEC = [
    ('real', 101, 2, 'real(101,2)'),
    ('real', 401, 2, 'real(401,2)'),
    ('real', 401, 3, 'real(401,3)'),
    ('real', 601, 2, 'real(601,2)'),
]
TEST_SYN_SPEC = [
    ('syn', 401, 2, 0, 'syn(401,2,seed0)'),
    ('syn', 401, 2, 1, 'syn(401,2,seed1)'),
    ('syn', 401, 2, 2, 'syn(401,2,seed2)'),
]
TEST_SPEC = TEST_REAL_SPEC + TEST_SYN_SPEC

ALL_SPEC = TRAIN_MIXED_SPEC + TEST_SPEC   # every instance step (1) asks for, in one place for the report

def oracle_binary_net(M):
    """Ceiling for ANY 0/1-only rule on this exact instance: force t=1 exactly where the free LP already
    chose (close to) 1, t=0 elsewhere.  Not a portable rule (it needs the answer already) -- a diagnostic
    upper bound showing how much of the free LP's saving a perfect 0/1 classifier could ever recover."""
    _, _, t = cm.lp(M)
    t_fixed = {g: (1.0 if t[g] >= 0.95 else 0.0) for g, cl in M['groups']}
    s, _, _ = cm.lp(M, t_fixed=t_fixed)
    return s / len(M['groups'])

def summarize_free_lp(spec, title):
    print(f"\n=== {title}: free LP t per group, label counts, and the 0/1-oracle ceiling ===")
    all_rows = []
    for item in spec:
        M, tag = instance_from_spec(item)
        p, k = M['p'], M['k']
        rows, saving = collect(M, tag)
        n = len(rows); n1 = sum(1 for r in rows if r['label'] == 1); n0 = sum(1 for r in rows if r['label'] == 0)
        nh = n - n1 - n0
        orc = oracle_binary_net(M)
        print(f"  {tag:22s} p={p:4d} k={k}: G8={n:4d}  t=1:{n1:4d}({n1/n:.0%}) t=0:{n0:4d}({n0/n:.0%}) "
              f"t~1/2:{nh:3d}({nh/n:.0%})   free-LP net/grp={saving/n:+.3f}   0/1-oracle net/grp={orc:+.3f}")
        all_rows += rows
    return all_rows

def fit_and_report_tree(train_rows, label_key, label_values_desc, max_depth, min_leaf_frac=1/12):
    fit_rows = [r for r in train_rows if r[label_key] is not None]
    X = [r['feats'] for r in fit_rows]; y = [r[label_key] for r in fit_rows]
    print(f"\n--- fitting CART on {len(fit_rows)} labelled groups, label={label_values_desc} ---")
    tree = build_tree(X, y, FEATURE_NAMES, max_depth=max_depth, min_leaf=max(10, int(len(y) * min_leaf_frac)))
    print_tree(tree, FEATURE_NAMES)
    acc = sum(1 for r in fit_rows if predict_tree(tree, r['feats']) == r[label_key]) / len(fit_rows)
    maj = majority(y); base_rate = sum(1 for v in y if v == maj) / len(y)
    print(f"train accuracy: {acc:.3f}  (majority-class baseline: {base_rate:.3f}, n={len(y)})")
    return tree

def report_feature_means(rows, title):
    print(f"\n=== {title}: feature means by true label (0 / ~1/2 / 1) ===")
    for name in FEATURE_NAMES:
        vals = {lab: [r['feats'][name] for r in rows if r['label3'] == lab] for lab in (0.0, 0.5, 1.0)}
        m = {lab: (sum(v) / len(v) if v else float('nan')) for lab, v in vals.items()}
        print(f"  {name:10s}  t=0: {m[0.0]:6.2f}   t~1/2: {m[0.5]:6.2f}   t=1: {m[1.0]:6.2f}")

def evaluate_and_print(rules, title, best_key='train_net'):
    train_eval = eval_rules_on_spec(TRAIN_MIXED_SPEC, rules)
    test_real_eval = eval_rules_on_spec(TEST_REAL_SPEC, rules)
    test_syn_eval = eval_rules_on_spec(TEST_SYN_SPEC, rules)
    print(f"\n=== {title}: net/group (TRAIN = real 199,2/3 + synthetic 199 seeds 0-2) ===")
    print(f"  {'rule':24s} {'TRAIN':>9s} {'TEST-real':>10s} {'TEST-syn':>9s} {'TEST-all':>9s}")
    results = {}
    for rname in rules:
        tr = train_eval[rname]; ter = test_real_eval[rname]; tes = test_syn_eval[rname]
        tr_net = sum(r['saving'] for r in tr) / sum(r['n_groups'] for r in tr)
        ter_net = sum(r['saving'] for r in ter) / sum(r['n_groups'] for r in ter)
        tes_net = sum(r['saving'] for r in tes) / sum(r['n_groups'] for r in tes)
        all_saving = sum(r['saving'] for r in ter + tes); all_n = sum(r['n_groups'] for r in ter + tes)
        results[rname] = dict(train_net=tr_net, test_real_net=ter_net, test_syn_net=tes_net,
                               test_all_net=all_saving / all_n, test_real_rows=ter, test_syn_rows=tes)
        print(f"  {rname:24s} {tr_net:+9.4f} {ter_net:+10.4f} {tes_net:+9.4f} {all_saving/all_n:+9.4f}")
    best_name = max((n for n in rules if n != 'always0'), key=lambda n: results[n][best_key])
    return results, best_name

def main():
    t_start = time.time()

    all_rows = summarize_free_lp(ALL_SPEC, "ALL instances requested by step (1)")
    train_rows = [r for r in all_rows if r['tag'] in {it[-1] for it in TRAIN_MIXED_SPEC}]

    # ---- feature/label analysis (step 2) ----
    report_feature_means(train_rows, "TRAIN (real 199,2/3 + synthetic 199 x3)")
    tree_bin = fit_and_report_tree(train_rows, 'label', 't=1 vs t=0 (t~1/2 dropped)', max_depth=3)
    tree3 = fit_and_report_tree(train_rows, 'label3', 't in {0, 1/2, 1} (bonus, non-binary rule)', max_depth=3)

    # ---- also fit single-feature threshold rules by DIRECTLY maximising LP net/group on TRAIN (exhaustive
    #      grid over the integer feature n_odd in [0,8]; still explicit/local, just not a gini-split tree) ----
    bin_rule, bin_lo, bin_hi, bin_tr_net = fit_threshold_rule(TRAIN_MIXED_SPEC, 'n_odd', three_way=False)
    thr_rule, thr_lo, thr_hi, thr_tr_net = fit_threshold_rule(TRAIN_MIXED_SPEC, 'n_odd', three_way=True)
    print(f"\n--- best BINARY n_odd-threshold by direct TRAIN-net search: t=1 iff n_odd>={bin_hi}, else 0"
          f"   (TRAIN net/grp={bin_tr_net:+.4f}) ---")
    print(f"--- best 3-WAY n_odd-threshold by direct TRAIN-net search: t=1 if n_odd>={thr_hi}, "
          f"t=1/2 if {thr_lo}<=n_odd<{thr_hi}, else t=0   (TRAIN net/grp={thr_tr_net:+.4f}) ---")

    RULES = dict(HAND_RULES); RULES['tree'] = make_tree_rule(tree_bin); RULES['thr_bin'] = bin_rule
    RULES3 = {'always0': rule_always0, 'always_half': rule_always_half,
              'tree3': make_tree_rule(tree3), 'threshold3': thr_rule}

    # ---- step 3: evaluate the required BINARY rules (t=1 on predicted groups, else 0) ----
    results, best_name = evaluate_and_print(RULES, "STEP 3 (required): binary rules, t in {0,1} only")
    print(f"\nBest binary rule by TRAIN net/group: '{best_name}'")
    for r in results[best_name]['test_real_rows'] + results[best_name]['test_syn_rows']:
        print(f"  TEST  {r['tag']:22s} p={r['p']:4d} k={r['k']}: G8={r['n_groups']:4d}  "
              f"saving={r['saving']:8.2f}  net/group={r['net']:+.4f}")
    print(f"  -> TEST-real net/group = {results[best_name]['test_real_net']:+.4f}   "
          f"TEST-syn net/group = {results[best_name]['test_syn_net']:+.4f}   "
          f"TEST-all net/group = {results[best_name]['test_all_net']:+.4f}   "
          f"(TRAIN = {results[best_name]['train_net']:+.4f})")

    # ---- bonus: allow the rule to output 1/2 too (still an explicit bounded-window local rule; goes
    #      beyond the letter of step 3 but tests whether the 0/1 restriction is really the bottleneck) ----
    results3, best3_name = evaluate_and_print(RULES3, "BONUS: rule may also output t=1/2")
    print(f"\nBest 3-way rule by TRAIN net/group: '{best3_name}'")
    print(f"  -> TEST-real net/group = {results3[best3_name]['test_real_net']:+.4f}   "
          f"TEST-syn net/group = {results3[best3_name]['test_syn_net']:+.4f}   "
          f"TEST-all net/group = {results3[best3_name]['test_all_net']:+.4f}   "
          f"(TRAIN = {results3[best3_name]['train_net']:+.4f})")

    print(f"\nTotal wall time: {time.time()-t_start:.1f}s")
    return dict(tree_bin=tree_bin, tree3=tree3, results=results, best_name=best_name,
                results3=results3, best3_name=best3_name)

if __name__ == "__main__":
    main()
