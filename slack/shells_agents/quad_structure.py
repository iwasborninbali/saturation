"""quad_structure.py -- TASK D: structure of the best lawful subsets of the quadruple
H(1) u H(-1) u H(2) u H(-2) in the HJSW box, at p = 11, 13, 17.

For each p:
  1. recompute a best-known lawful set with CP-SAT (ortools, time-limited) and with the
     null-move annealer (many seeds), keep the larger / union-checked best;
  2. CERTIFY it independently: brute-force over ALL C(n,3) triples of the chosen points,
     checking exact collinearity by cross product (does NOT reuse the 'lines' data
     structure used by the solvers -- an independent check as required);
  3. analyse structure: points per shell, per column, per row, per null line (u=x-y,
     v=x+y), per residue CLASS (a,b) in F_p^* x F_p^* (how many of the <=4 box-copies of
     a class survive), and test invariance under swap/negation/boost symmetries acting on
     classes (the natural level at which the HJSW paper's Klein four-group V acts -- the
     box itself is NOT symmetric under these maps, only the class structure is, matching
     Theorem main / the orbit lemma in hjsw_window.tex).

usage: python3 quad_structure.py [p ...]   (default 11 13 17)
"""
import sys, os, time, itertools
sys.path.insert(0, '/home/pmbot/projects/saturation_peer/slack')
from diffusion_sampler import hyper_points, build_lines
from null_search import anneal
from ortools.sat.python import cp_model

CS_OFFSETS = (1, -1, 2, -2)


def shell_consts(p):
    return [c % p for c in CS_OFFSETS]


def solve_cpsat(pts, lines, time_limit, workers=6):
    n = len(pts)
    m = cp_model.CpModel()
    x = [m.NewBoolVar(f'x{i}') for i in range(n)]
    for s in lines:
        m.Add(sum(x[i] for i in s) <= 2)
    m.Maximize(sum(x))
    sol = cp_model.CpSolver()
    sol.parameters.max_time_in_seconds = time_limit
    sol.parameters.num_search_workers = workers
    st = sol.Solve(m)
    idx = [i for i in range(n) if sol.Value(x[i])]
    return idx, sol.StatusName(st), sol.BestObjectiveBound()


def certify_lawful(points):
    """Independent brute-force certification: no 3 of `points` collinear, ANY slope.
    Does not reuse the solver's line-building code. O(n^3) triple scan with exact
    integer cross-product collinearity test."""
    n = len(points)
    for i, j, k in itertools.combinations(range(n), 3):
        x1, y1 = points[i]; x2, y2 = points[j]; x3, y3 = points[k]
        cross = (x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1)
        if cross == 0:
            return False, (points[i], points[j], points[k])
    return True, None


def class_of(pt, p):
    X, Y = pt
    return (X % p, Y % p)


def analyse(p, S, log):
    h = (p - 1) // 2
    consts = shell_consts(p)
    n = len(S)
    log(f"\n=== p={p}: |S| = {n}  ( = {n/(p-1):.3f}(p-1) = {n/(2*p):.3f}N ; 3(p-1) = {3*(p-1)} ; "
        f"extra over 3(p-1): {n - 3*(p-1)} )")

    # (i) per shell
    shell_count = {c: 0 for c in consts}
    for (X, Y) in S:
        a, b = X % p, Y % p
        c = (a * b) % p
        shell_count[c] += 1
    log(f"(i) points per shell (order 1,-1,2,-2 mod p = {consts}):")
    for c in consts:
        log(f"    c={c:3d} ({'+1' if c==1 else '-1' if c==p-1 else '+2' if c==2 else '-2'}): {shell_count[c]}")

    # (ii) per column / row (box coordinates, cap 2 each -- vertical/horizontal lines)
    from collections import Counter
    col = Counter(X for X, Y in S)
    row = Counter(Y for X, Y in S)
    col_hist = Counter(col.values())
    row_hist = Counter(row.values())
    log(f"(ii) columns used: {len(col)}, occupancy histogram (#cols with k points -> count): {dict(sorted(col_hist.items()))}")
    log(f"     rows used: {len(row)}, occupancy histogram: {dict(sorted(row_hist.items()))}")
    bad_col = [c_ for c_, k in col.items() if k > 2]
    bad_row = [r_ for r_, k in row.items() if k > 2]
    log(f"     columns/rows exceeding cap 2: {bad_col} / {bad_row}  (must be empty for a lawful set)")

    # (iii) per null line u = x-y (const), v = x+y (const)
    u_ = Counter(X - Y for X, Y in S)
    v_ = Counter(X + Y for X, Y in S)
    u_hist = Counter(u_.values()); v_hist = Counter(v_.values())
    log(f"(iii) null lines u=x-y used: {len(u_)}, occupancy histogram: {dict(sorted(u_hist.items()))}")
    log(f"      null lines v=x+y used: {len(v_)}, occupancy histogram: {dict(sorted(v_hist.items()))}")
    bad_u = [k for k, cnt in u_.items() if cnt > 2]
    bad_v = [k for k, cnt in v_.items() if cnt > 2]
    log(f"      u/v lines exceeding cap 2: {bad_u} / {bad_v}")

    # class-level analysis: class = (a,b) in F_p^* x F_p^*, ab = one of the 4 shell consts.
    # Each class has up to 4 box-copies (r,s in {0,1}); how many survive in S?
    cls_count = Counter(class_of(pt, p) for pt in S)
    cls_hist = Counter(cls_count.values())
    n_classes_total = 4 * (p - 1)
    log(f"    classes touched: {len(cls_count)} / {n_classes_total} possible; copies-per-touched-class histogram "
        f"(k copies -> #classes): {dict(sorted(cls_hist.items()))}")
    n_extra_from_2copy = sum(1 for k in cls_count.values() if k >= 2)
    log(f"    classes contributing 2 box-copies: {sum(1 for k in cls_count.values() if k==2)}; "
        f"classes contributing 1: {sum(1 for k in cls_count.values() if k==1)}")

    # (iv) symmetries, tested at the CLASS level (the box itself is not symmetric under
    # these affine maps -- x-range is [-h,-h+2p), y-range is [0,2p) -- so we test whether
    # the SET OF CLASSES used by S (ignoring which of the <=4 box-copies is chosen) is
    # invariant; this is exactly the level at which the Klein four-group V of the HJSW
    # paper acts on H(c).
    classes_used = set(cls_count.keys())

    def test_map(name, f):
        img = {f(a, b) for (a, b) in classes_used}
        ok = (img == classes_used)
        log(f"    {name:28s}: class-set invariant = {ok}"
            + ("" if ok else f"   (|symmetric diff| = {len(img ^ classes_used)})"))
        return ok

    log("(iv) symmetry tests (class-level, i.e. mod p; box itself is asymmetric under these maps):")
    test_map("swap (a,b)->(b,a)", lambda a, b: (b, a))
    test_map("neg  (a,b)->(-a,-b)", lambda a, b: ((-a) % p, (-b) % p))
    test_map("sign-flip (a,b)->(a,-b) [c<->-c]", lambda a, b: (a, (-b) % p))
    test_map("sign-flip (a,b)->(-a,b) [c<->-c]", lambda a, b: ((-a) % p, b))
    # boosts: which l in F_p^* leave the class-set invariant?
    good_ls = []
    for l in range(1, p):
        f = lambda a, b, l=l: ((l * a) % p, (pow(l, -1, p) * b) % p)
        img = {f(a, b) for (a, b) in classes_used}
        if img == classes_used:
            good_ls.append(l)
    log(f"    boost l in F_p^*, (a,b)->(l a, l^-1 b): invariant for l in {good_ls}  "
        f"(trivial l=1 always works; {len(good_ls)}/{p-1} of F_p^* )")

    return dict(shell=shell_count, col=col, row=row, u=u_, v=v_, cls=cls_count, good_ls=good_ls)


def run_p(p, cpsat_time, seeds, seed_secs, log):
    cs = shell_consts(p)
    pts = hyper_points(p, cs)
    lines = build_lines(pts)
    log(f"\n########## p={p}: |points|={len(pts)}  |lines(>=3 pts)|={len(lines)} ##########")

    t0 = time.time()
    idx_cp, status, bound = solve_cpsat(pts, lines, cpsat_time)
    S_cp = [pts[i] for i in idx_cp]
    log(f"CP-SAT: alpha={len(S_cp)}  status={status}  bound={bound:.0f}  time={time.time()-t0:.1f}s")

    t0 = time.time()
    best_ann = 0; S_ann = []
    for s in range(seeds):
        v, idxs = anneal(pts, lines, seconds=seed_secs, seed=1000 * p + s)
        if v > best_ann:
            best_ann = v; S_ann = [pts[i] for i in idxs]
    log(f"null-SA ({seeds} seeds x {seed_secs}s): alpha={best_ann}  time={time.time()-t0:.1f}s")

    S = S_cp if len(S_cp) >= best_ann else S_ann
    src = "CP-SAT" if len(S_cp) >= best_ann else "null-SA"
    log(f"-> using the {src} solution, size {len(S)}, for structure analysis")

    ok, witness = certify_lawful(S)
    log(f"INDEPENDENT CERTIFICATION (brute triple scan, {len(S)} pts, C({len(S)},3)="
        f"{len(S)*(len(S)-1)*(len(S)-2)//6} triples checked by exact cross-product): "
        f"{'PASS -- no 3 collinear' if ok else f'FAIL -- collinear triple {witness}'}")
    if not ok:
        log("!! certification failed -- refusing to report a size for this p")
        return None

    stats = analyse(p, S, log)
    return dict(p=p, size=len(S), points=S, status=status, bound=bound, src=src, stats=stats)


if __name__ == '__main__':
    ps = [int(a) for a in sys.argv[1:]] or [11, 13, 17]
    outpath = '/home/pmbot/projects/saturation_peer/slack/verification/shells_structure.txt'
    lines_out = []

    def log(s):
        print(s, flush=True)
        lines_out.append(s)

    log(f"quad_structure.py -- TASK D structure analysis, shells H(1),H(-1),H(2),H(-2), p in {ps}")
    log(f"generated {time.strftime('%Y-%m-%d %H:%M:%S')}")

    results = []
    time_budget = {11: (60, 6, 15), 13: (90, 6, 20), 17: (150, 6, 25)}
    for p in ps:
        cpsat_time, seeds, seed_secs = time_budget.get(p, (120, 6, 20))
        r = run_p(p, cpsat_time, seeds, seed_secs, log)
        if r: results.append(r)

    log("\n\n===== SUMMARY =====")
    for r in results:
        p = r['p']
        log(f"p={p}: alpha_quad = {r['size']} = {r['size']/(p-1):.3f}(p-1) = {r['size']/(2*p):.3f}N   "
            f"[{r['status']}, CP-SAT bound {r['bound']:.0f}, source={r['src']}]   "
            f"extra over 3(p-1) = {r['size']-3*(p-1)}")

    with open(outpath, 'w') as f:
        f.write('\n'.join(lines_out) + '\n')
    print(f"\nlog written to {outpath}")
