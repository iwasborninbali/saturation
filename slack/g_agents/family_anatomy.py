"""family_anatomy.py — G3 STRONG form (task family_anatomy): for the permutation cubic y = x^3 (p prime, p ≡ 2 mod 3, box [0,2p)^2,
N = 2p), classify every 3-point line with 3 distinct residues via the family formula (docs/research/curves_conjecture.md §7, a = 0):
direction (u,v) primitive (u > 0 canonical), integer steps 0 < i < j (base = leftmost of the 3 points), base residue
x0 ≡ -(i+j)*u*inv3 (mod p), v ≡ c1*u^3 (mod p) with c1 = (i^2-ij+j^2)*inv3 (mod p); scale J = max(i,j,j-i) = j.
Reports: counts of 3-point lines by J; the LP (rows/cols -> point-weight fallback, ±1 lines with >=3 points, 3-point lines) and its
value/N; LP mass by (type,size) and by J-bucket; restricted LPs using only 3-point lines with J <= J0 (J0 in {4,8,16,all}) to
quantify how much of the LP saving over the ±1-only baseline comes from small J; degree distribution of the 4p points in the
3-point-line hypergraph restricted to J <= J0 (mean, std, min, fraction <= mean/2, coefficient of variation) for the same J0's.

Line-finding: full O(n^2) pairwise scan keyed by the reduced (dx,dy,c) line equation (NOT per-point direction bucketing, which
undercounts >=4-point lines by splitting them into overlapping partial tuples) -- cross-checked against slack/verification/lp_curve.txt
at p=197 (pm1: 167 lines sizes {3:70,4:31,5:31,6:35} LP=534.00=1.355N; all: 3539 lines LP=436.28=1.107N): matches exactly.

usage: python3 slack/g_agents/family_anatomy.py p [p2 p3 ...]
"""
import sys, time, math
from collections import Counter, defaultdict
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix

J0_LIST = [4, 8, 16]          # plus "all" handled separately
JBUCKET_EDGES = [2, 4, 8, 16, 32, 64, 128, 256]   # cumulative report points for "mass by J"


def build_points(p):
    N = 2 * p
    pts = []
    for X in range(N):
        y0 = pow(X, 3, p)
        pts.append((X, y0))
        pts.append((X, y0 + p))
    return pts  # already sorted by (X,Y) since X increases, and for fixed X, y0 < y0+p


def find_rich_lines(pts):
    """All lines with >=3 points, via full pairwise scan keyed by (dx,dy,c). Returns list of (dx,dy,members_sorted)."""
    n = len(pts)
    L = {}
    for a in range(n):
        x1, y1 = pts[a]
        for b in range(a + 1, n):
            x2, y2 = pts[b]
            dx, dy = x2 - x1, y2 - y1
            g = math.gcd(abs(dx), abs(dy))
            dx //= g; dy //= g
            if dx < 0 or (dx == 0 and dy < 0):
                dx, dy = -dx, -dy
            c = dy * x1 - dx * y1
            key = (dx, dy, c)
            s = L.get(key)
            if s is None:
                L[key] = s = {a}
            s.add(b)
    out = []
    for (dx, dy, c), s in L.items():
        if len(s) >= 3:
            out.append((dx, dy, tuple(sorted(s))))
    return out


def classify(p, pts, rich):
    """Split rich lines into pm1 (dx==dy or dx==-dy) and generic (must be exactly 3 points); attach (i,j,J) + formula check to generic."""
    inv3 = pow(3, -1, p)
    pm1 = []      # (size, members)
    generic = []  # dict-like record per line
    rowcol_bug = 0
    bad_formula = 0
    for dx, dy, mem in rich:
        if dx == 0 or dy == 0:
            rowcol_bug += 1
            continue
        if dx == dy or dx == -dy:
            pm1.append((len(mem), mem))
            continue
        assert len(mem) == 3, f"generic line with {len(mem)} points (Bezout violation?) dx={dx} dy={dy}"
        m0, m1, m2 = mem  # already sorted by point index == sorted by X (all X distinct here)
        X0, Y0 = pts[m0]; X1, Y1 = pts[m1]; X2, Y2 = pts[m2]
        u, v = dx, dy
        i = (X1 - X0) // u
        j = (X2 - X0) // u
        J = max(abs(i), abs(j), abs(i - j))
        base_exp = (-(i + j) * u * inv3) % p
        base_act = X0 % p
        c1 = (i * i - i * j + j * j) * inv3 % p
        v_exp = (c1 * pow(u, 3, p)) % p
        v_act = v % p
        ok = (base_exp == base_act) and (v_exp == v_act)
        if not ok:
            bad_formula += 1
        generic.append({'mem': mem, 'i': i, 'j': j, 'J': J, 'ok': ok})
    return pm1, generic, rowcol_bug, bad_formula


def solve_lp(n, line_membs):
    """LP: min 2*sum(w_line) + sum(z_P) s.t. for every point, sum_{line containing P} w_line + z_P >= 1, w,z>=0.
    line_membs: list of tuples of point indices (each a line with >=3 points, weight coefficient 1 per point)."""
    m = len(line_membs)
    ri = []; ci = []
    for k, mem in enumerate(line_membs):
        for q in mem:
            ri.append(q); ci.append(k)
    for q in range(n):
        ri.append(q); ci.append(m + q)
    data = np.ones(len(ri))
    A = csr_matrix((data, (ri, ci)), shape=(n, m + n))
    c = np.concatenate([2 * np.ones(m), np.ones(n)])
    res = linprog(c, A_ub=-A, b_ub=-np.ones(n), bounds=(0, None), method='highs')
    return res


def degree_stats(n, generic, Jmax, exclude=None):
    deg = np.zeros(n, dtype=int)
    cnt = 0
    for g in generic:
        if g['J'] <= Jmax:
            cnt += 1
            for q in g['mem']:
                deg[q] += 1
    keep = np.ones(n, dtype=bool)
    if exclude:
        keep[list(exclude)] = False
    d = deg[keep]
    mean = d.mean(); std = d.std()
    return {
        'n_lines': cnt, 'mean': mean, 'std': std, 'min': int(d.min()), 'max': int(d.max()),
        'frac_le_half_mean': float(np.mean(d <= mean / 2)) if mean > 0 else float('nan'),
        'cv': (std / mean) if mean > 0 else float('nan'),
        'frac_deg0': float(np.mean(d == 0)),
        'argmax': int(np.argmax(deg)),
    }


def analyze(p):
    t0 = time.time()
    N = 2 * p
    pts = build_points(p)
    n = len(pts)
    rich = find_rich_lines(pts)
    t1 = time.time()
    pm1, generic, rowcol_bug, bad_formula = classify(p, pts, rich)
    assert rowcol_bug == 0, "rows/cols should never reach size>=3 for a bijection"
    pm1_sizes = Counter(sz for sz, _ in pm1)
    n_generic = len(generic)
    Js = [g['J'] for g in generic]
    Jmax_all = max(Js) if Js else 0

    print(f"p={p} N={N} pts={n}  line-find {t1-t0:.1f}s  pm1 rich lines={len(pm1)} sizes={dict(sorted(pm1_sizes.items()))}"
          f"  generic 3-lines={n_generic}  formula mismatches={bad_formula}/{n_generic}  J range=[{min(Js) if Js else '-'},{Jmax_all}]", flush=True)

    pm1_mem = [mem for _, mem in pm1]

    def generic_mem(Jcap):
        if Jcap is None:
            return [g['mem'] for g in generic]
        return [g['mem'] for g in generic if g['J'] <= Jcap]

    # baseline: pm1 only
    t2 = time.time()
    res_pm1 = solve_lp(n, pm1_mem)
    Vpm1 = res_pm1.fun
    t3 = time.time()
    print(f"  LP(pm1 only)      = {Vpm1:8.2f} = {Vpm1/N:.4f} N   [{t3-t2:.1f}s]", flush=True)

    # full LP (all rich lines)
    res_full = solve_lp(n, pm1_mem + generic_mem(None))
    Vfull = res_full.fun
    t4 = time.time()
    print(f"  LP(pm1+all 3-lines) = {Vfull:8.2f} = {Vfull/N:.4f} N   [{t4-t3:.1f}s]   saving over pm1-only = {(Vpm1-Vfull)/N:.4f} N", flush=True)

    # mass by (type,size) and by J, from the FULL optimal solution
    w = res_full.x[:len(pm1_mem) + len(generic_mem(None))]
    lines_all = pm1_mem + generic_mem(None)
    tags = [('pm1', len(mem)) for mem in pm1_mem] + [('gen3', 3) for _ in generic]
    mass_by_type = Counter()
    mass_by_J = defaultdict(float)
    for k, (tag, sz) in enumerate(tags):
        wk = w[k]
        if wk < 1e-9:
            continue
        mass_by_type[(tag, sz)] += 2 * wk
        if tag == 'gen3':
            mass_by_J[generic[k - len(pm1_mem)]['J']] += 2 * wk
    zmass = res_full.x[len(lines_all):].sum()
    print(f"  mass by (type,size): {[(k, round(v,1)) for k,v in sorted(mass_by_type.items(), key=lambda kv:-kv[1])]}  point-weight mass z={zmass:.1f}", flush=True)

    # cumulative mass / line-count by J bucket (from the full optimum's generic-line weights)
    cum_report = []
    running_mass = 0.0; running_cnt = 0
    edges = sorted(set(JBUCKET_EDGES + [Jmax_all]))
    for edge in edges:
        if edge > Jmax_all and edge != edges[-1]:
            continue
        m_here = sum(v for Jv, v in mass_by_J.items() if Jv <= edge)
        c_here = sum(1 for g in generic if g['J'] <= edge)
        cum_report.append((edge, c_here, round(m_here, 1)))
    print(f"  cumulative (J<=e): (edge, #3-lines, LP-mass-on-them) = {cum_report}", flush=True)

    # restricted LPs at J0 in {4,8,16} (full already computed = 'all')
    restricted = {}
    for J0 in J0_LIST:
        tR0 = time.time()
        res_r = solve_lp(n, pm1_mem + generic_mem(J0))
        VJ0 = res_r.fun
        tR1 = time.time()
        frac = (Vpm1 - VJ0) / (Vpm1 - Vfull) if Vpm1 > Vfull else float('nan')
        restricted[J0] = VJ0
        print(f"  LP(pm1 + 3-lines J<={J0:3d}) = {VJ0:8.2f} = {VJ0/N:.4f} N   n_lines(J<={J0})={len(generic_mem(J0))}"
              f"   fraction of full saving captured = {frac:.3f}   [{tR1-tR0:.1f}s]", flush=True)

    # the box-corner hub: (p,p) is the "far" lift of the curve's unique symmetric fixed point (0,0) (f odd: f(-x)=-f(x)); for every
    # residue x0 in (0,p) and either Y-lift, C = 2*(p,p) - (x0,Y0) is an EXACT integer reflection, automatically on the curve too
    # (proof: Cx=2p-x0 -> -x0 (mod p), Cy=2p-Y0 -> -y0 (mod p), and (-x0)^3 = -x0^3 = -y0 identically) -- giving 2(p-1) collinear
    # triples through (p,p) minus the ones that land on slope +-1 (already counted as pm1): x0 in {1,p-1} always slope+1 (f(1)=1,
    # f(-1)=-1), and the two square roots of -1 mod p (slope -1) when p == 1 (mod 4). Predicted generic degree at (p,p):
    idx_map = {pts[k]: k for k in range(n)}
    hub_idx = idx_map.get((p, p))
    pm1_at_hub = 2 if (p % 4 == 1) else 0
    hub_pred = 2 * (p - 1) - 2 - pm1_at_hub
    print(f"  box-corner hub (p,p): predicted generic degree = 2(p-1) - 2 - {pm1_at_hub} = {hub_pred}  (p%4={p%4})", flush=True)

    # degree stats of the 3-line hypergraph restricted to J<=J0, for J0 in {4,8,16,all}: both raw and with the single
    # max-degree point excluded (to separate the box-corner artifact from the regularity of the bulk)
    print("  3-line hypergraph degree stats (mean, std, min, max, frac<=mean/2, CV=std/mean, frac deg=0):", flush=True)
    deg_report = {}
    for J0 in J0_LIST + ['all']:
        Jcap = Jmax_all if J0 == 'all' else J0
        st = degree_stats(n, generic, Jcap)
        hub_ok = (hub_idx is not None and st['argmax'] == hub_idx)
        st_ex = degree_stats(n, generic, Jcap, exclude={st['argmax']})
        deg_report[J0] = st
        print(f"    J0={str(J0):>4s}: n_lines={st['n_lines']:6d}  mean={st['mean']:6.2f}  std={st['std']:6.2f}  min={st['min']:3d} max={st['max']:5d}"
              f"  frac<=mean/2={st['frac_le_half_mean']:.3f}  CV={st['cv']:.3f}  frac_deg0={st['frac_deg0']:.3f}  argmax_is_hub={hub_ok}", flush=True)
        print(f"              excl. top point: mean={st_ex['mean']:6.2f}  std={st_ex['std']:6.2f}  min={st_ex['min']:3d} max={st_ex['max']:5d}"
              f"  frac<=mean/2={st_ex['frac_le_half_mean']:.3f}  CV={st_ex['cv']:.3f}  frac_deg0={st_ex['frac_deg0']:.3f}", flush=True)
        deg_report[J0]['cv_excl_hub'] = st_ex['cv']
        deg_report[J0]['mean_excl_hub'] = st_ex['mean']

    print(f"  total time for p={p}: {time.time()-t0:.1f}s", flush=True)
    return {
        'p': p, 'N': N, 'n': n, 'Vpm1': Vpm1, 'Vfull': Vfull, 'restricted': restricted,
        'n_generic': n_generic, 'Jmax': Jmax_all, 'bad_formula': bad_formula,
        'mass_by_type': dict(mass_by_type), 'cum_report': cum_report, 'deg_report': deg_report,
        'pm1_sizes': dict(pm1_sizes),
    }


if __name__ == '__main__':
    ps = [int(a) for a in sys.argv[1:]] or [197, 401, 599, 797]
    results = []
    for p in ps:
        assert p % 3 == 2, f"p={p} must be ≡ 2 (mod 3) for x^3 to be a permutation"
        results.append(analyze(p))
        print(flush=True)

    print("=== summary ===")
    for r in results:
        print(f"p={r['p']:4d}: N={r['N']:5d}  LP(pm1)={r['Vpm1']/r['N']:.4f}N  LP(full)={r['Vfull']/r['N']:.4f}N"
              f"  LP(J<=4)={r['restricted'][4]/r['N']:.4f}N  LP(J<=8)={r['restricted'][8]/r['N']:.4f}N  LP(J<=16)={r['restricted'][16]/r['N']:.4f}N"
              f"  #generic3={r['n_generic']}  Jmax={r['Jmax']}  formula-mismatches={r['bad_formula']}")
    print("\nCV(J0) by p (raw, includes the box-corner hub point):")
    for r in results:
        row = {J0: round(r['deg_report'][J0]['cv'], 3) for J0 in J0_LIST + ['all']}
        print(f"  p={r['p']:4d}: {row}")
    print("\nCV(J0) by p (hub point excluded):")
    for r in results:
        row = {J0: round(r['deg_report'][J0]['cv_excl_hub'], 3) for J0 in J0_LIST + ['all']}
        print(f"  p={r['p']:4d}: {row}")
