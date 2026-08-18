"""cyc_model.py — abstract cycle model for vector C (second hyperbola H(k), any k): classes, <k>-cycles, (4,8,4) groups, and the class-level cover LP.
Definitions (see docs/research/pair_bound_notes.md §25–26):
  classes: ('K',a) = kappa_a = (a,1/a) in H(1); ('M',b) = mu_b = (b,k/b) in H(k), a,b in F_p^*.
  edges: row-edge kappa_a — mu_{ka} (the two rows y = Y(1/a), Y(1/a)+p), column-edge mu_b — kappa_b (the two columns x = X(b), X(b)+p).
  cycles: kappa_x -> mu_{kx} -> kappa_{kx} -> ... (one cycle per coset of <k>), even length 2*ord(k).
  8-groups: residue groups (slope ±1) with line sizes (4,8,4); each has 4 classes (2 kappa + 2 mu); weight t on its 3 lines costs 6t and gives its
  classes demand 1 - t (a class in two groups: 1 - sum of t).
  cover LP: min sum_e 4 w_e + sum_G 6 t_G  s.t.  w_{e-(v)} + w_{e+(v)} + sum_{G ∋ v} t_G >= 1 for every class v; w, t >= 0 (t <= 1).
  Baseline w = 1/2 gives 4(p-1) (=2 per edge, 2(p-1) edges).  Saving := 4(p-1) - optimum.
API: M = build(p,k) -> dict with cycles (list of lists of classes), edges, groups (list of frozensets of classes with tag), pos (class -> (cycle, index)).
     lp(M, groups_subset=None, t_fixed=None) -> (saving, w dict, t dict).   synthetic(M, seed) -> a model with the same cycles but random groups.
     changes(M, S) -> number of type changes among the specials of S along the cycles.   usage: python3 slack/cyc_model.py p k  (self-test vs points)"""
import sys, random
import numpy as np
from collections import defaultdict
from scipy.optimize import linprog
from scipy.sparse import csr_matrix

def build(p, k):
    k %= p; h = (p - 1) // 2
    pts = [(x, y) for x in range(-h, 3 * h + 2) for y in range(0, 2 * p) if (x * y) % p in (1, k)]
    def cls(q):
        x, y = q; return ('K', x % p) if (x * y) % p == 1 else ('M', x % p)
    lines = defaultdict(list)
    for q in pts:
        x, y = q; lines[('d', x - y)].append(q); lines[('a', x + y)].append(q)
    grp = defaultdict(list)
    for key, mem in lines.items(): grp[(key[0], key[1] % p)].append(key)
    groups = []
    for g, keys in grp.items():
        if sorted((len(lines[key]) for key in keys), reverse=True) == [8, 4, 4]:
            cl = frozenset(cls(q) for key in keys for q in lines[key])
            assert len(cl) == 4, (g, cl)
            groups.append((g, cl))
    # cycles
    seen = set(); cycles = []; pos = {}
    for a in range(1, p):
        if ('K', a) in seen: continue
        x = a; seq = []
        while ('K', x) not in seen:
            seen.add(('K', x)); seq.append(('K', x)); seq.append(('M', k * x % p)); x = k * x % p
        for i, c in enumerate(seq): pos[c] = (len(cycles), i)
        cycles.append(seq)
    return dict(p=p, k=k, cycles=cycles, groups=groups, pos=pos)

def edges_of(M):
    """edge index: (cycle c, i) = edge between cycles[c][i] and cycles[c][i+1 mod L]"""
    return [(c, i) for c, seq in enumerate(M['cycles']) for i in range(len(seq))]

def lp(M, groups_subset=None, t_fixed=None, integral_t=None):
    cycles = M['cycles']; groups = M['groups'] if groups_subset is None else groups_subset
    E = edges_of(M); eidx = {e: j for j, e in enumerate(E)}; nE = len(E); nG = len(groups)
    classes = [c for seq in cycles for c in seq]; cidx = {c: i for i, c in enumerate(classes)}
    rows = []; cols = []; vals = []
    for c, seq in enumerate(cycles):
        L = len(seq)
        for i, v in enumerate(seq):
            r = cidx[v]
            rows += [r, r]; cols += [eidx[(c, (i - 1) % L)], eidx[(c, i)]]; vals += [1.0, 1.0]
    for j, (g, cl) in enumerate(groups):
        for v in cl:
            rows.append(cidx[v]); cols.append(nE + j); vals.append(1.0)
    A = csr_matrix((vals, (rows, cols)), shape=(len(classes), nE + nG))
    cost = np.concatenate([4 * np.ones(nE), 6 * np.ones(nG)])
    bounds = [(0, None)] * nE + [(0, 1)] * nG
    if t_fixed is not None:
        for j, (g, cl) in enumerate(groups):
            if g in t_fixed: bounds[nE + j] = (t_fixed[g], t_fixed[g])
    res = linprog(cost, A_ub=-A, b_ub=-np.ones(len(classes)), bounds=bounds, method='highs')
    saving = 4 * (M['p'] - 1) - res.fun
    w = {E[j]: res.x[j] for j in range(nE)}; t = {groups[j][0]: res.x[nE + j] for j in range(nG)}
    return saving, w, t

def synthetic(M, seed=0):
    """same cycles, same number of groups, each group = 2 random kappa + 2 random mu classes (distinct across groups)"""
    rnd = random.Random(seed)
    K = [c for seq in M['cycles'] for c in seq if c[0] == 'K']; Mu = [c for seq in M['cycles'] for c in seq if c[0] == 'M']
    rnd.shuffle(K); rnd.shuffle(Mu); groups = []
    for j in range(len(M['groups'])):
        groups.append((('syn', j), frozenset([K[2 * j], K[2 * j + 1], Mu[2 * j], Mu[2 * j + 1]])))
    return dict(p=M['p'], k=M['k'], cycles=M['cycles'], groups=groups, pos=M['pos'])

def changes(M, S):
    special = set(); 
    for g, cl in S: special |= cl
    ch = 0
    for seq in M['cycles']:
        sp = [c for c in seq if c in special]
        for i in range(len(sp)):
            if sp[i][0] != sp[(i + 1) % len(sp)][0]: ch += 1
    return ch

if __name__ == "__main__":
    p, k = int(sys.argv[1]), int(sys.argv[2]); M = build(p, k)
    s, w, t = lp(M)
    from collections import Counter
    print(f"p={p} k={k}: G8={len(M['groups'])} cycles={len(M['cycles'])} (len {len(M['cycles'][0])}); class-level LP saving={s:.2f} (net/group {s/len(M['groups']):.3f}); t-values {Counter(round(v,2) for v in t.values())}")
    s1, _, _ = lp(M, t_fixed={g: 1.0 for g, cl in M['groups']}); s2, _, _ = lp(M, t_fixed={g: 0.5 for g, cl in M['groups']})
    print(f"   all t=1: saving {s1:.2f} (formula 2*changes-6*G8 = {2*changes(M,M['groups'])-6*len(M['groups'])}); all t=1/2: saving {s2:.2f}")
    for seed in (0, 1):
        Ms = synthetic(M, seed); ss, _, _ = lp(Ms); print(f"   synthetic seed {seed}: LP saving {ss:.2f} (net/group {ss/len(Ms['groups']):.3f})")
