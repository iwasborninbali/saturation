#!/usr/bin/env python3
"""reduced_lp.py (agent: reduced_lp) -- G3'/reduced_lp task: the reduced LP over +-1-line weights only,
for the box lift of the permutation cubic y = x^3 (mod p), p prime, p == 2 mod 3, using the EXACT
rectangle reduction of rows/columns (THREAD[127]; background docs/research/curves_conjecture.md #8-9,
docs/research/permutation_cubic_note.md).

SETUP.  Residue points (x, y=x^3 mod p), x=0..p-1 (a bijection since p==2 mod 3).  Box lift: 4p points, one
rectangle per residue x: P1=(x,y), P2=(x+p,y), P3=(x+p,y+p), P4=(x,y+p).  (P1,P3) share a slope+1 ("diagonal",
X-Y=const) line; (P2,P4) share a slope-1 ("antidiagonal", X+Y=const) line.  Rows/columns each carry exactly 2
points (one rectangle's own).

REDUCED LP.  Only diagonal/antidiagonal line weights w_l >= 0 are free variables.  With t_P = sum of the (<=2)
+-1-line weights through P, the EXACT optimal rows+columns cost of one rectangle is
    2 * max( (1-t_P1)_+ + (1-t_P3)_+ ,  (1-t_P2)_+ + (1-t_P4)_+ )      ( x_+ := max(0,x) )
(proved by LP duality on the 4-cycle row/col sub-LP: rows/cols are never shared across rectangles, so the
row/col optimum decomposes rectangle-by-rectangle; the sub-LP's dual is the fractional matching polytope of
C4, which is integral, vertices = the two diagonal-pair matchings).  So
    reduced-LP cost = min_{w>=0}  2 sum_l w_l + sum_r 2 max(...)
is a genuine LP once the two maxes and the two hinges (.)_+ are linearised with one aux var m_r >= 0 per
rectangle and 4 aux vars u_{r,1..4} >= 0 (standard epigraph trick; see reduced_lp() below).

TASKS (a)-(d), see docs/research/g_agents/reduced_lp.md for the write-up and numbers:
 (a) reduced_lp() is checked against full_lp() -- the SAME cost with rows, columns, every diagonal and every
     antidiagonal line as INDEPENDENT 0/1-incidence LP variables (cost 2 per unit weight, no extra point
     slack) -- for every p in DEFAULT_PS; they agree to solver precision (see main()).
 (b) reduced_lp()/N is reported for each p.
 (c) classify_lines() buckets every diagonal/antidiagonal line into (shape, own_size) = position-in-group,
     shape in {single(1,2,1), balanced(3,6,3), split(1,4,5,2)/(2,5,4,1) -- the two split orientations are
     mirror images and pooled by own_size}; the optimal reduced_lp() weights are tabulated by (slope, shape,
     own_size).
 (d) a TYPE-BASED RULE: weight depends only on (slope, shape, own_size) -- fit_flat_rule() -- and, refined,
     also on nsmall = the number of a line's member rectangles whose OTHER-slope class is small (shape
     'single') -- fit_interaction_rule() (the cross-slope interaction the task allows for).  Both are found
     by SOLVING a small constrained LP (shared weight per bucket; still a genuine sub-family of reduced_lp's
     feasible region, so its cost is a rigorous, checkable upper bound for ANY weights >= 0 plugged in,
     whether or not they are bucket-optimal) and independently re-evaluated by evaluate_labelled() (pure
     O(p) arithmetic, no LP solve) as a cross-check -- a genuinely separate code path from the fitting
     LPs, which caught a real sign bug during development (see docs/research/g_agents/reduced_lp.md d.3).

usage: python3 slack/g_agents/reduced_lp.py [p1 p2 ...]     (default: 101 197 401 599 797; ~10s total)
Python: /Users/iwasborninbali/venvs/sat/bin/python3 (numpy/scipy, scipy.optimize.linprog method='highs').
Output is printed to stdout and also written verbatim to slack/g_agents/reduced_lp_output.txt.
"""
import sys, time
from collections import defaultdict, Counter
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix

DEFAULT_PS = [101, 197, 401, 599, 797]


def is_prime(n):
    if n < 2: return False
    if n % 2 == 0: return n == 2
    i = 3
    while i * i <= n:
        if n % i == 0: return False
        i += 2
    return True


def build_rects(p):
    """Rectangle r = residue x: (P1,P2,P3,P4) = (x,y),(x+p,y),(x+p,y+p),(x,y+p), y=x^3 mod p."""
    rects = []
    for x in range(p):
        y = pow(x, 3, p)
        rects.append(((x, y), (x + p, y), (x + p, y + p), (x, y + p)))
    return rects


# ------------------------------------------------------------- (a) full LP (rows+cols+diag+antidiag, no z_P)
def full_lp(p, rects):
    pts = [P for R in rects for P in R]
    n = len(pts)
    rows = defaultdict(list); cols = defaultdict(list); diag = defaultdict(list); anti = defaultdict(list)
    for i, (X, Y) in enumerate(pts):
        rows[Y].append(i); cols[X].append(i); diag[X - Y].append(i); anti[X + Y].append(i)
    lines = []
    for d in (rows, cols, diag, anti):
        for mem in d.values():
            lines.append(mem)
    m = len(lines)
    data = []; ri = []; ci = []
    for j, mem in enumerate(lines):
        for i in mem:
            data.append(1.0); ri.append(i); ci.append(j)
    A = csr_matrix((data, (ri, ci)), shape=(n, m))
    c = 2 * np.ones(m)
    res = linprog(c, A_ub=-A, b_ub=-np.ones(n), bounds=(0, None), method='highs')
    assert res.status == 0, res.message
    return res.fun


# ------------------------------------------------------------------------- (a),(b) reduced LP (THREAD[127])
def diag_anti_lists(rects):
    diagvals = set(); antivals = set()
    for (P1, P2, P3, P4) in rects:
        diagvals.update((P1[0]-P1[1], P2[0]-P2[1], P4[0]-P4[1]))   # P3-P1 same diag value (centre)
        antivals.update((P1[0]+P1[1], P2[0]+P2[1], P3[0]+P3[1]))   # P4-P2 same anti value (centre)
    return sorted(diagvals), sorted(antivals)


def reduced_lp(p, rects, diag_list=None, anti_list=None):
    """min 2 sum w_l + sum_r 2*m_r  s.t.  w_diag(P)+w_anti(P)+u_{r,k} >= 1 (k=0..3, P=rect r's k-th corner),
       m_r >= u_{r,0}+u_{r,2} (P1,P3 pair), m_r >= u_{r,1}+u_{r,3} (P2,P4 pair);  all vars >= 0."""
    if diag_list is None: diag_list, anti_list = diag_anti_lists(rects)
    didx = {v: i for i, v in enumerate(diag_list)}; aidx = {v: i for i, v in enumerate(anti_list)}
    nd, na = len(diag_list), len(anti_list); nw = nd + na
    R = len(rects); nu = 4 * R; nvar = nw + nu + R
    def wd(v): return didx[v]
    def wa(v): return nd + aidx[v]
    def uidx(r, k): return nw + 4 * r + k
    def midx(r): return nw + nu + r
    rows_i = []; cols_i = []; data = []; rhs = []; con = 0
    for r, (P1, P2, P3, P4) in enumerate(rects):
        for k, (X, Y) in enumerate((P1, P2, P3, P4)):
            rows_i += [con, con, con]; cols_i += [wd(X - Y), wa(X + Y), uidx(r, k)]; data += [-1.0, -1.0, -1.0]
            rhs.append(-1.0); con += 1
        mv = midx(r)
        rows_i += [con, con, con]; cols_i += [mv, uidx(r, 0), uidx(r, 2)]; data += [-1.0, 1.0, 1.0]
        rhs.append(0.0); con += 1
        rows_i += [con, con, con]; cols_i += [mv, uidx(r, 1), uidx(r, 3)]; data += [-1.0, 1.0, 1.0]
        rhs.append(0.0); con += 1
    A = csr_matrix((data, (rows_i, cols_i)), shape=(con, nvar)); b = np.array(rhs)
    c = np.zeros(nvar); c[:nw] = 2.0; c[nw + nu:] = 2.0
    res = linprog(c, A_ub=A, b_ub=b, bounds=(0, None), method='highs')
    assert res.status == 0, res.message
    w_diag = {v: float(res.x[didx[v]]) for v in diag_list}
    w_anti = {v: float(res.x[nd + aidx[v]]) for v in anti_list}
    return res.fun, w_diag, w_anti


# ------------------------------------------------------------------------------------------- (c) anatomy
def classify_lines(p, rects, slope):
    """slope 'd' (diagonal, X-Y) or 'a' (antidiagonal, X+Y).  -> {line_value: (c0,pos,shape,sizes,own_size)},
       shapecount (Counter of shapes, one count per GROUP not per line), and members {line_value: set(x)}."""
    size = Counter(); members = defaultdict(set)
    for x, (P1, P2, P3, P4) in enumerate(rects):
        if slope == 'd':
            v1 = P1[0]-P1[1]; v2 = P2[0]-P2[1]; v4 = P4[0]-P4[1]
            size[v1] += 2; size[v2] += 1; size[v4] += 1
            members[v1].add(x); members[v2].add(x); members[v4].add(x)
        else:
            v2 = P2[0]+P2[1]; v1 = P1[0]+P1[1]; v3 = P3[0]+P3[1]
            size[v2] += 2; size[v1] += 1; size[v3] += 1
            members[v2].add(x); members[v1].add(x); members[v3].add(x)
    groups = defaultdict(set)
    for v in size: groups[v % p].add(v)
    info = {}; shapecount = Counter()
    for c0, vals in groups.items():
        vs = sorted(vals); sizes = tuple(size[v] for v in vs)
        if len(vs) == 3 and sizes == (1, 2, 1): shape = 'single'
        elif len(vs) == 3 and sizes == (3, 6, 3): shape = 'balanced'
        elif len(vs) == 4 and sizes in ((1, 4, 5, 2), (2, 5, 4, 1)): shape = 'split'
        else: shape = f'other{sizes}'
        shapecount[shape] += 1
        for pos, v in enumerate(vs):
            info[v] = (c0, pos, shape, sizes, size[v])
    return info, shapecount, members


# --------------------------------------------------------------------------------- (d) type-based rule(s)
# A line's TYPE ("position in the group") is fully determined by its own point-count except own_size==2,
# which needs `shape` to disambiguate "single-mid" (the 2-line of a (1,2,1) group) from "split-tip" (the
# 2-line of a split group).  own_size==1 and own_size>=6 are always exactly the group's tip / balanced-mid.
NMEM = {'single_mid': 1, 'balanced_tip': 3, 'split_s2': 2, 'split_s4': 3, 'split_s5': 3}   # for nsmall bucketing


def type_of(shape, own_size):
    if own_size == 1: return 'size1'
    if own_size == 2: return 'single_mid' if shape == 'single' else 'split_s2'
    if own_size == 3: return 'balanced_tip'
    if own_size == 4: return 'split_s4'
    if own_size == 5: return 'split_s5'
    if own_size >= 6: return 'balanced_mid'
    return 'split_s2'  # unreachable for the shapes occurring at the tested p (own_size>=1 always)


def other_slope_shapes(p, rects):
    """x -> (diag-class shape of x, antidiag-class shape of x) -- x's OWN classes, not a line's."""
    info_d, _, _ = classify_lines(p, rects, 'd')
    info_a, _, _ = classify_lines(p, rects, 'a')
    out = {}
    for x, (P1, P2, P3, P4) in enumerate(rects):
        out[x] = (info_d[P1[0]-P1[1]][2], info_a[P2[0]+P2[1]][2])
    return out


def line_labels(p, rects):
    """-> dkeys, akeys : line_value -> ('fixed',const) or ('var', type, nsmall) for every diagonal /
       antidiagonal line.  nsmall = #members whose shape on the OTHER slope is 'single' (the cross-slope
       interaction term)."""
    info_d, _, members_d = classify_lines(p, rects, 'd')
    info_a, _, members_a = classify_lines(p, rects, 'a')
    oshape = other_slope_shapes(p, rects)
    def label(info, members, otheridx):
        out = {}
        for v, (c0, pos, shape, sizes, sz) in info.items():
            t = type_of(shape, sz)
            if t == 'size1': out[v] = ('fixed', 0.0)
            elif t == 'balanced_mid': out[v] = ('fixed', 1.0)
            else:
                mem = members[v]
                nsmall = sum(1 for x in mem if oshape[x][otheridx] == 'single')
                out[v] = ('var', t, nsmall)
        return out
    return label(info_d, members_d, 1), label(info_a, members_a, 0)


def evaluate_labelled(rects, dkeys, akeys, weight_fn):
    """Direct O(p) evaluation: weight_fn(slope,type,nsmall)->float for 'var' labels, constant for 'fixed'.
       This is THE rigorous check -- valid for ANY weight_fn >= 0, independent of how it was derived."""
    def val(slope, k):
        return k[1] if k[0] == 'fixed' else weight_fn(slope, k[1], k[2])
    w_d = {v: val('d', k) for v, k in dkeys.items()}
    w_a = {v: val('a', k) for v, k in akeys.items()}
    line_cost = 2.0 * (sum(w_d.values()) + sum(w_a.values()))
    rect_cost = 0.0
    for (P1, P2, P3, P4) in rects:
        d = [max(0.0, 1.0 - (w_d[X-Y] + w_a[X+Y])) for (X, Y) in (P1, P2, P3, P4)]
        rect_cost += 2.0 * max(d[0] + d[2], d[1] + d[3])
    return line_cost + rect_cost, w_d, w_a


def fit_flat_rule(ps, rects_cache):
    """Constrained LP: ONE shared weight per (slope, type) -- no interaction term -- jointly optimal across
       all p in ps.  7 types x 2 slopes = 14 shared variables + per-(p,rectangle) u,m auxiliaries."""
    VARNAMES = ['size1', 'single_mid', 'split_s2', 'balanced_tip', 'split_s4', 'split_s5', 'balanced_mid']
    nV = len(VARNAMES)
    def type_var(slope_i, t): return slope_i * nV + VARNAMES.index(t)
    line_counts = Counter(); dkeys_c = {}; akeys_c = {}
    for p in ps:
        rects = rects_cache[p]
        info_d, _, _ = classify_lines(p, rects, 'd'); info_a, _, _ = classify_lines(p, rects, 'a')
        dk = {v: type_of(s, sz) for v, (c0, pos, s, sizes, sz) in info_d.items()}
        ak = {v: type_of(s, sz) for v, (c0, pos, s, sizes, sz) in info_a.items()}
        dkeys_c[p] = dk; akeys_c[p] = ak
        for t in dk.values(): line_counts[(p, type_var(0, t))] += 1
        for t in ak.values(): line_counts[(p, type_var(1, t))] += 1
    offset = {}; cur = 2 * nV
    for p in ps: offset[p] = cur; cur += 5 * p
    nvar = cur
    rows_i = []; cols_i = []; data = []; rhs = []; con = 0
    c = np.zeros(nvar)
    for (p, vi), cnt in line_counts.items(): c[vi] += 2.0 * cnt
    for p in ps:
        off = offset[p]; rects = rects_cache[p]; R = len(rects)
        dk = dkeys_c[p]; ak = akeys_c[p]
        for r, (P1, P2, P3, P4) in enumerate(rects):
            for k, (X, Y) in enumerate((P1, P2, P3, P4)):
                dvi = type_var(0, dk[X - Y]); avi = type_var(1, ak[X + Y]); uidx = off + 4 * r + k
                rows_i += [con, con, con]; cols_i += [dvi, avi, uidx]; data += [-1.0, -1.0, -1.0]
                rhs.append(-1.0); con += 1
            mv = off + 4 * R + r
            rows_i += [con, con, con]; cols_i += [mv, off+4*r, off+4*r+2]; data += [-1.0, 1.0, 1.0]
            rhs.append(0.0); con += 1
            rows_i += [con, con, con]; cols_i += [mv, off+4*r+1, off+4*r+3]; data += [-1.0, 1.0, 1.0]
            rhs.append(0.0); con += 1
            c[mv] += 2.0
    A = csr_matrix((data, (rows_i, cols_i)), shape=(con, nvar)); b = np.array(rhs)
    res = linprog(c, A_ub=A, b_ub=b, bounds=(0, None), method='highs')
    assert res.status == 0, res.message
    rule = {(('d' if si == 0 else 'a'), VARNAMES[vi]): float(res.x[si*nV+vi]) for si in (0,1) for vi in range(nV)}
    return rule


def fit_interaction_rule(ps, rects_cache):
    """Constrained LP: ONE shared weight per (slope, type, nsmall) bucket, jointly optimal across all p in
       ps.  A strict superset of fit_flat_rule's family (nsmall adds the cross-slope interaction), so its
       cost is <= fit_flat_rule's, and (being a restriction of the fully unrestricted reduced_lp, where every
       line gets its own free weight) its cost is >= reduced_lp's true optimum.  Both inequalities are
       checked in main()."""
    KEYS = [(si, t, ns) for si in (0, 1) for t, nm in NMEM.items() for ns in range(nm + 1)]
    KIDX = {k: i for i, k in enumerate(KEYS)}; NV = len(KEYS)
    dkeys_c = {}; akeys_c = {}; line_counts = Counter()
    for p in ps:
        rects = rects_cache[p]
        dk, ak = line_labels(p, rects)
        dkeys_c[p] = dk; akeys_c[p] = ak
        for v, k in dk.items():
            if k[0] == 'var': line_counts[(p, KIDX[(0, k[1], k[2])])] += 1
        for v, k in ak.items():
            if k[0] == 'var': line_counts[(p, KIDX[(1, k[1], k[2])])] += 1
    offset = {}; cur = NV
    for p in ps: offset[p] = cur; cur += 5 * p
    nvar = cur
    rows_i = []; cols_i = []; data = []; rhs = []; con = 0
    c = np.zeros(nvar)
    for (p, vi), cnt in line_counts.items(): c[vi] += 2.0 * cnt
    for p in ps:
        off = offset[p]; rects = rects_cache[p]; R = len(rects)
        dk = dkeys_c[p]; ak = akeys_c[p]
        for r, (P1, P2, P3, P4) in enumerate(rects):
            for k, (X, Y) in enumerate((P1, P2, P3, P4)):
                dlab = dk[X - Y]; alab = ak[X + Y]; uidx = off + 4 * r + k
                terms = [(uidx, -1.0)]; fixed_sum = 0.0
                if dlab[0] == 'fixed': fixed_sum += dlab[1]
                else: terms.append((KIDX[(0, dlab[1], dlab[2])], -1.0))
                if alab[0] == 'fixed': fixed_sum += alab[1]
                else: terms.append((KIDX[(1, alab[1], alab[2])], -1.0))
                for (ci, dd) in terms: rows_i.append(con); cols_i.append(ci); data.append(dd)
                rhs.append(-1.0 + fixed_sum); con += 1        # -u -w_var's <= -1 + (fixed contributions)
            mv = off + 4 * R + r
            rows_i += [con, con, con]; cols_i += [mv, off+4*r, off+4*r+2]; data += [-1.0, 1.0, 1.0]
            rhs.append(0.0); con += 1
            rows_i += [con, con, con]; cols_i += [mv, off+4*r+1, off+4*r+3]; data += [-1.0, 1.0, 1.0]
            rhs.append(0.0); con += 1
            c[mv] += 2.0
    A = csr_matrix((data, (rows_i, cols_i)), shape=(con, nvar)); b = np.array(rhs)
    res = linprog(c, A_ub=A, b_ub=b, bounds=(0, None), method='highs')
    assert res.status == 0, res.message
    rule = {KEYS[i]: float(res.x[i]) for i in range(NV)}
    rule_fn_table = {}
    for (si, t, ns), val in rule.items():
        rule_fn_table[(('d' if si == 0 else 'a'), t, ns)] = val
    return rule_fn_table


def main():
    ps = [int(a) for a in sys.argv[1:]] or DEFAULT_PS
    out = []
    def w(s=''): print(s); out.append(s)

    for p in ps: assert is_prime(p) and p % 3 == 2, f"p={p} must be prime, ==2 mod 3"
    rects_cache = {p: build_rects(p) for p in ps}

    w(f"reduced_lp.py -- p in {ps}")
    w("\n=== (a) reduced_lp vs full_lp (rows+cols+diag+antidiag, independent line variables, no z_P) ===")
    lpvals = {}
    for p in ps:
        t0 = time.time(); fv = full_lp(p, rects_cache[p]); t1 = time.time()
        diag_list, anti_list = diag_anti_lists(rects_cache[p])
        rv, w_diag, w_anti = reduced_lp(p, rects_cache[p], diag_list, anti_list); t2 = time.time()
        lpvals[p] = (rv, w_diag, w_anti)
        N = 2 * p
        w(f"p={p:4d}: full_lp={fv:11.4f}   reduced_lp={rv:11.4f}   |diff|={abs(fv-rv):.2e}"
          f"   [{t1-t0:.2f}s + {t2-t1:.2f}s]")

    w("\n=== (b) reduced_lp optimum / N ===")
    for p in ps:
        rv = lpvals[p][0]; N = 2*p
        w(f"p={p:4d}: N={N:5d}  reduced_lp={rv:10.4f}  =  {rv/N:.4f} N  =  {rv/p:.4f} p")

    w("\n=== (c) anatomy: reduced_lp's optimal weight by (slope, shape, own_size=position) ===")
    for p in ps:
        rv, w_diag, w_anti = lpvals[p]
        w(f"-- p={p} --")
        for slope, wdict in (('diag(+1)', w_diag), ('anti(-1)', w_anti)):
            info, shapecount, _ = classify_lines(p, rects_cache[p], 'd' if slope[0] == 'd' else 'a')
            w(f"   {slope}: groups by shape {dict(shapecount)}")
            agg = defaultdict(list)
            for v, (c0, pos, shape, sizes, sz) in info.items(): agg[(shape, sz)].append(wdict[v])
            for key in sorted(agg, key=lambda k: (k[0], -k[1])):
                vals = agg[key]
                w(f"      shape={key[0]:8s} own_size={key[1]:2d}: n={len(vals):4d}  weight mean={np.mean(vals):.4f}"
                  f"  [{min(vals):.4f},{max(vals):.4f}]  std={np.std(vals):.4f}")

    w("\n=== (d.1) flat type-based rule: weight depends only on (slope, shape, own_size) [no interaction] ===")
    t0 = time.time(); flat_rule = fit_flat_rule(ps, rects_cache); w(f"  fit time {time.time()-t0:.2f}s")
    for k in sorted(flat_rule, key=lambda k: (k[0], k[1])): w(f"    {k}: {flat_rule[k]:.4f}")
    w("  cost/N (evaluated independently, direct arithmetic, NOT re-using the fit's own bookkeeping):")
    flat_vals = {}
    for p in ps:
        rects = rects_cache[p]; dk, ak = line_labels(p, rects)
        val, _, _ = evaluate_labelled(rects, dk, ak, lambda slope, t, ns: flat_rule[(slope, t)])
        flat_vals[p] = val
        rv = lpvals[p][0]; N = 2*p
        assert rv <= val + 1e-6, "flat rule beat the unrestricted LP -- impossible, a restriction can't"
        w(f"    p={p:4d}: rule={val:10.4f} = {val/N:.4f} N   |   LP={rv:10.4f} = {rv/N:.4f} N"
          f"   |   gap = {(val-rv)/N:+.4f} N   |   1.5N - rule = {(1.5*N - val)/N:+.4f} N")

    w("\n=== (d.2) interaction rule: weight depends on (slope, shape/position, nsmall) ===")
    w("  nsmall(line) = #{member rectangles x of this line : x's OTHER-slope class has shape 'single'}")
    t0 = time.time(); irule = fit_interaction_rule(ps, rects_cache); w(f"  fit time {time.time()-t0:.2f}s")
    for slope in ('d', 'a'):
        w(f"  -- slope {slope} --")
        for t, nm in NMEM.items():
            row = "  ".join(f"ns={ns}:{irule[(slope,t,ns)]:.4f}" for ns in range(nm+1))
            w(f"    {t:12s} (nmem={nm}): {row}")
    w("  cost/N (evaluated independently, direct arithmetic):")
    ratios = []
    for p in ps:
        rects = rects_cache[p]; dk, ak = line_labels(p, rects)
        val, _, _ = evaluate_labelled(rects, dk, ak, lambda slope, t, ns: irule[(slope, t, ns)])
        rv = lpvals[p][0]; N = 2*p
        ratios.append(val/N)
        # nesting check: unrestricted LP <= interaction rule (a restriction of it) <= flat rule (a further
        # restriction, sharing weights across nsmall too) -- must hold at every p, or a fit has a bug.
        assert rv <= val + 1e-6, "interaction rule beat the unrestricted LP -- impossible"
        assert val <= flat_vals[p] + 1e-6, "interaction rule did worse than flat rule -- impossible (superset family)"
        w(f"    p={p:4d}: rule={val:10.4f} = {val/N:.4f} N   |   LP={rv:10.4f} = {rv/N:.4f} N"
          f"   |   gap = {(val-rv)/N:+.4f} N   |   1.5N - rule = {(1.5*N - val)/N:+.4f} N")
    w(f"  worst (max) rule/N over the tested p: {max(ratios):.4f}  => c >= {1.5-max(ratios):.4f} on this range")
    w("  (nesting check passed at every p: LP <= interaction-rule <= flat-rule)")

    with open('slack/g_agents/reduced_lp_output.txt', 'w') as f:
        f.write('\n'.join(out) + '\n')
    print("\n[wrote slack/g_agents/reduced_lp_output.txt]")


if __name__ == '__main__':
    main()
