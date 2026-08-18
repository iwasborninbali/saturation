"""local_search_structure.py — c_agents task "local_search_structure" (see docs/research/pair_bound_notes.md
sections 25-26 and slack/cyc_model.py for the model).

Question: in the class-graph cover LP (cyc_model.lp), each (4,8,4) group gets an optimal weight
t_G in {0, 1/2, 1}.  What LOCAL feature of a group's 4 vertices -- computed from the cyclic order of
ALL specials (= union of every group's vertex set, known up front, independent of which groups end up
selected) -- predicts t_G = 1 vs t_G = 0?  We build those features, fit a small decision tree (plain
Python / no sklearn in this venv) on real p=199 (k=2,k=3) + synthetic p=199 (seeds 0,1,2), and evaluate
the resulting EXPLICIT rule (t=1 on predicted groups, t=0 else) via cyc_model.lp(M, t_fixed=...) on
held-out real (p,k) in {(101,2),(401,2),(401,3),(601,2)} and synthetic p=401 (seeds 0,1,2).

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

# ---------------------------------------------------------------- instance collection --------------

def collect(M, tag):
    """Runs the free LP once on M; returns (rows, saving) where rows has one dict per group with its
    local features and its free-LP-optimal t (and the 0/1 label, or None if t is close to 1/2)."""
    check_alternation_fact(M)
    ctx = local_context(M)
    saving, _, t = cm.lp(M)
    rows = []
    for g, cl in M['groups']:
        rows.append(dict(key=g, tag=tag, feats=group_features(cl, ctx), t=float(t[g]), label=classify_t(t[g])))
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

def gini(y):
    n = len(y)
    if n == 0: return 0.0
    p1 = sum(y) / n
    return 1 - p1 * p1 - (1 - p1) * (1 - p1)

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
    n = len(y); p1 = sum(y) / n if n else 0.0
    node = {'n': n, 'p1': p1, 'pred': 1 if p1 >= 0.5 else 0}
    if depth >= max_depth or n < 2 * min_leaf or p1 in (0.0, 1.0):
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
        print(f"{indent}-> predict {node['pred']}  (n={node['n']}, p(t=1)={node['p1']:.2f})")
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
def rule_adj1(feats):    return 1 if feats['n_adj'] >= 1 else 0
def rule_adj2(feats):    return 1 if feats['n_adj'] >= 2 else 0
def rule_odd_maj(feats): return 1 if feats['n_odd'] >= 5 else 0     # more odd- than even-distance sides
def rule_isolated(feats):return 1 if feats['max_of_min'] >= 6 else 0  # the OPPOSITE intuition: reward isolation
def rule_crowded(feats): return 1 if feats['min_dist'] <= 2 else 0

def make_tree_rule(tree):
    return lambda feats: predict_tree(tree, feats)

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

TRAIN_SPEC = [
    ('real', 199, 2, 'real(199,2)'),
    ('real', 199, 3, 'real(199,3)'),
    ('syn', 199, 2, 0, 'syn(199,2,seed0)'),
    ('syn', 199, 2, 1, 'syn(199,2,seed1)'),
    ('syn', 199, 2, 2, 'syn(199,2,seed2)'),
]
TEST_SPEC = [
    ('real', 101, 2, 'real(101,2)'),
    ('real', 401, 2, 'real(401,2)'),
    ('real', 401, 3, 'real(401,3)'),
    ('real', 601, 2, 'real(601,2)'),
    ('syn', 401, 2, 0, 'syn(401,2,seed0)'),
    ('syn', 401, 2, 1, 'syn(401,2,seed1)'),
    ('syn', 401, 2, 2, 'syn(401,2,seed2)'),
]

def summarize_free_lp(spec, title):
    print(f"\n=== {title}: free LP t per group, and label counts ===")
    all_rows = []
    for item in spec:
        M, tag = instance_from_spec(item)
        p, k = M['p'], M['k']
        rows, saving = collect(M, tag)
        n = len(rows); n1 = sum(1 for r in rows if r['label'] == 1); n0 = sum(1 for r in rows if r['label'] == 0)
        nh = n - n1 - n0
        print(f"  {tag:22s} p={p:4d} k={k}: G8={n:4d}  t=1: {n1:4d} ({n1/n:.2%})  t=0: {n0:4d} ({n0/n:.2%})  "
              f"t~1/2: {nh:3d} ({nh/n:.2%})   free-LP net/group={saving/n:.3f}")
        all_rows += rows
    return all_rows

def main():
    t_start = time.time()

    train_rows = summarize_free_lp(TRAIN_SPEC, "TRAIN instances")
    test_rows = summarize_free_lp(TEST_SPEC, "HELD-OUT (test) instances")

    # ---- fit CART on TRAIN rows with a clean 0/1 label only (drop the ~1/2 rows from the FIT, not from
    #      evaluation: the final rule still outputs 0/1 for every group when evaluated on real instances).
    fit_rows = [r for r in train_rows if r['label'] is not None]
    X = [r['feats'] for r in fit_rows]; y = [r['label'] for r in fit_rows]
    print(f"\n=== Fitting CART on {len(fit_rows)} labelled TRAIN groups ({sum(y)} positive) ===")
    tree = build_tree(X, y, FEATURE_NAMES, max_depth=3, min_leaf=max(15, len(y)//12))
    print_tree(tree, FEATURE_NAMES)
    train_acc = sum(1 for r in fit_rows if predict_tree(tree, r['feats']) == r['label']) / len(fit_rows)
    print(f"train classification accuracy (t=1 vs t=0 only): {train_acc:.3f}  (base rate predicting majority: "
          f"{max(sum(y), len(y)-sum(y))/len(y):.3f})")

    # ---- feature means conditioned on label (diagnostic, printed once) ----
    print("\n=== TRAIN feature means by label (0 / ~1/2 / 1) ===")
    for name in FEATURE_NAMES:
        m0 = sum(r['feats'][name] for r in train_rows if r['label'] == 0) / max(1, sum(1 for r in train_rows if r['label'] == 0))
        mh = sum(r['feats'][name] for r in train_rows if r['label'] is None) / max(1, sum(1 for r in train_rows if r['label'] is None))
        m1 = sum(r['feats'][name] for r in train_rows if r['label'] == 1) / max(1, sum(1 for r in train_rows if r['label'] == 1))
        print(f"  {name:10s}  t=0: {m0:6.2f}   t~1/2: {mh:6.2f}   t=1: {m1:6.2f}")

    RULES = dict(HAND_RULES); RULES['tree'] = make_tree_rule(tree)

    # ---- evaluate every candidate rule via the REAL LP (t_fixed) on TRAIN then TEST ----
    print("\n=== Rule evaluation via cyc_model.lp(M, t_fixed=rule(...)) ===")
    train_eval = eval_rules_on_spec(TRAIN_SPEC, RULES)
    test_eval = eval_rules_on_spec(TEST_SPEC, RULES)
    results = {}
    for rname in RULES:
        tr, te = train_eval[rname], test_eval[rname]
        tr_net = sum(r['saving'] for r in tr) / sum(r['n_groups'] for r in tr)
        te_net = sum(r['saving'] for r in te) / sum(r['n_groups'] for r in te)
        results[rname] = dict(train_rows=tr, test_rows=te, train_net=tr_net, test_net=te_net)
        print(f"  rule={rname:22s}  TRAIN net/group={tr_net:+.4f}   TEST(held-out) net/group={te_net:+.4f}")

    # ---- pick best rule BY TRAIN performance (no test leakage in model selection); report its TEST number
    best_name = max((n for n in RULES if n != 'always0'), key=lambda n: results[n]['train_net'])
    print(f"\n=== Best rule by TRAIN net/group: '{best_name}' ===")
    for r in results[best_name]['test_rows']:
        print(f"  TEST  {r['tag']:22s} p={r['p']:4d} k={r['k']}: G8={r['n_groups']:4d}  saving={r['saving']:8.2f}  net/group={r['net']:+.4f}")
    print(f"  TEST TOTAL net/group = {results[best_name]['test_net']:+.4f}   "
          f"(TRAIN net/group = {results[best_name]['train_net']:+.4f})")

    # ---- also show the free LP's own net/group on the same TEST set as the upper bound ----
    free_saving_total = 0; free_groups_total = 0
    for item in TEST_SPEC:
        M, _ = instance_from_spec(item)
        s, _, _ = cm.lp(M)
        free_saving_total += s; free_groups_total += len(M['groups'])
    print(f"\nFree LP upper bound on TEST set: net/group = {free_saving_total/free_groups_total:+.4f}")
    print(f"Total wall time: {time.time()-t_start:.1f}s")

    return dict(tree=tree, results=results, best_name=best_name)

if __name__ == "__main__":
    main()
