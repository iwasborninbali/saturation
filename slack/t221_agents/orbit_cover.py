"""orbit_cover.py — T2.21 agent task A: the (7,5,3,1) orbit-cover lemma for k=-1.

Setting (matches slack/lp1_anatomy.py / slack/lp1_types.py): p odd prime, h=(p-1)//2,
P = {(x,y) in [-h,3h+1] x [0,2p-1] : x*y mod p in {1,p-1}}.  Lines: rows ('r',y), columns
('c',x), slope+1 diagonals ('d',x-y) [exact integer key, not reduced mod p], slope-1
antidiagonals ('a',x+y).  A slope+1 RESIDUE GROUP G_d (d in Z/p) is the union of all
diagonals with x-y ≡ d (mod p); its TYPE is the sorted-descending tuple of sizes of its
(>=1 point) integer diagonals.  Slope-1 residue groups G'_d are, by the convention of
lp1_anatomy.py's img_line/dres_of map, the union of antidiagonals x+y ≡ -d (mod p) (this
is exactly R(G_{-d}) for R:(x,y)->(p-x,y), since R sends the diagonal x-y=c to the
antidiagonal x+y=p-c, i.e. G_d -> G'_{-d}).

ORBIT Omega_d := G_d ∪ G_{-d} ∪ G'_d ∪ G'_{-d}
             = { q in P : (x-y)%p in {d,(-d)%p} }  ∪  { q in P : (x+y)%p in {d,(-d)%p} }.
(Both unions use the SAME 2-element residue set {d,-d mod p}; this is the closed form used
below — see docs/research/pair_bound_notes.md B.19 addendum (a).)  Since type(G_d) always
equals type(G_{-d}) (checked below; forced by the RR' symmetry noted in B.19(a)), the
(7,5,3,1) +1-groups pair up into d <-> -d and each unordered pair {d,-d} gives ONE orbit;
we test each such orbit once (m7 = count of +1-groups i.e. residues d, matching the B_t
convention of lp1_types.py; #orbits = m7/2).

For each orbit we check:
 (i)   |Omega|==64, and Omega is closed under rows and columns of the FULL point set P
       (every row/column of P meeting Omega lies entirely inside Omega).
 (ii)  LP(Omega): maximise sum_{q in Omega} x_q s.t. capacity-2 constraints on every row,
       column, slope+1 and slope-1 line of P *restricted to Omega* that keeps >=3 points,
       0<=x<=1.  (This uses ALL lines of P restricted to Omega, not just the 12 "own"
       lines below — so it also tests whether any other line acquires an accidental >=3
       point intersection with Omega.)
 (iii) The integral cover certificate: the 12 lines of sizes 7,5,3 belonging to the four
       groups G_d, G_{-d}, G'_d, G'_{-d}, plus the 4 points of their four 1-point lines as
       singletons.  Check: covers Omega; the 12 lines are pairwise disjoint (equivalently,
       partition the 60 non-singleton points, since 4*(7+5+3)=60); the 4 uncovered points
       of Omega are exactly the 4 singleton points; whether the 7-line of G_d shares a
       point with any line of G'_d or G'_{-d} (checked directly, not just inferred).
 (iv)  Any failure of the above is logged as an exception.
 (v)   Per p: m7 = #{d in Z/p : type(G_d) == (7,5,3,1)}; m8 = #{d : type==(8,4,4)};
       m6groups = #{d : type==(6,6,2,2)}  (all counting +1-groups one per residue d, i.e.
       BOTH members of each {d,-d} pair — matches lp1_types.py's B_t column).

Usage: python3 slack/t221_agents/orbit_cover.py pmin pmax [--all-above N | --sample-step S]
  Default: all primes in [pmin,pmax].
Writes: slack/t221_agents/orbit_cover_output.txt (summary table + exceptions) and
        slack/t221_agents/orbit_cover_detail.json (machine-readable per-p, per-orbit facts
        used to write the report).
"""
import sys, json, time
from collections import defaultdict, Counter
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix


def primes_between(a, b):
    out = []
    for n in range(max(2, a), b + 1):
        if n < 2:
            continue
        is_p = True
        i = 2
        while i * i <= n:
            if n % i == 0:
                is_p = False
                break
            i += 1
        if is_p:
            out.append(n)
    return out


def build_P(p):
    h = (p - 1) // 2
    pts = [(x, y) for x in range(-h, 3 * h + 2) for y in range(0, 2 * p) if (x * y) % p in (1, p - 1)]
    idx = {q: i for i, q in enumerate(pts)}
    return pts, idx, h


def build_lines(pts, idx):
    """Full line dictionaries over ALL of P, keyed by exact (non-modular) line id."""
    lines = defaultdict(list)
    for (x, y) in pts:
        i = idx[(x, y)]
        lines[('r', y)].append(i)
        lines[('c', x)].append(i)
        lines[('d', x - y)].append(i)
        lines[('a', x + y)].append(i)
    return lines


def group_types(pts, p, lines):
    """+1 residue groups G_d (d=0..p-1 that occur), each with its type = sorted-desc
    profile of sizes of its (>=1 pt) integer diagonals, and the actual (key,size) list of
    those diagonals (needed later to pick out the 7/5/3/1 lines by exact integer c)."""
    grp = defaultdict(list)  # d -> list of point idx
    for i, (x, y) in enumerate(pts):
        grp[(x - y) % p].append(i)
    gtype = {}
    gdiags = {}  # d -> list of (c, size) sorted by size desc, c exact integer with c%p==d
    for d, mem in grp.items():
        cs = Counter(pts[i][0] - pts[i][1] for i in mem)
        prof = tuple(sorted(cs.values(), reverse=True))
        gtype[d] = prof
        gdiags[d] = sorted(cs.items(), key=lambda kv: -kv[1])
    return grp, gtype, gdiags


def antidiag_lines_for_negd(pts, p, lines, d):
    """The slope-1 group G'_d = R(G_{-d}) = { q in P : (x+y)%p == (-d)%p }; return its
    integer antidiagonals (c,size) sorted by size desc (c exact, c%p == (-d)%p)."""
    target = (-d) % p
    cs = Counter()
    for (x, y) in pts:
        if (x + y) % p == target:
            cs[x + y] += 1
    return sorted(cs.items(), key=lambda kv: -kv[1])


def lp_on_omega(omega_idx_set, pts, lines):
    """LP(Omega): maximise sum x over Omega s.t. every P-line restricted to Omega with
    >=3 points inside Omega gets a <=2 capacity constraint."""
    omega = sorted(omega_idx_set)
    local = {g: i for i, g in enumerate(omega)}
    m = len(omega)
    rows, cols, data = [], [], []
    r = 0
    n_constraints_by_fam = Counter()
    for key, mem in lines.items():
        sub = [local[j] for j in mem if j in local]
        if len(sub) >= 3:
            for j in sub:
                rows.append(r)
                cols.append(j)
                data.append(1.0)
            n_constraints_by_fam[key[0]] += 1
            r += 1
    A = csr_matrix((data, (rows, cols)), shape=(r, m))
    res = linprog(-np.ones(m), A_ub=A, b_ub=2 * np.ones(r), bounds=[(0, 1)] * m, method='highs')
    val = -res.fun
    return val, dict(n_constraints_by_fam), r


def check_orbit(p, pts, idx, lines, gtype, gdiags, d):
    """Full check (i)-(iv) for the orbit of +1-group residue d (type must be (7,5,3,1))."""
    nd = (-d) % p
    facts = {'d': d, 'neg_d': nd}
    # Omega as a set of point-indices
    omega = set()
    for i, (x, y) in enumerate(pts):
        r = (x - y) % p
        a = (x + y) % p
        if r == d or r == nd or a == d or a == nd:
            omega.add(i)
    facts['size'] = len(omega)
    facts['size_ok'] = (len(omega) == 64)

    # (i) closure under rows/columns of the FULL P
    rows_full = defaultdict(list)
    cols_full = defaultdict(list)
    for i, (x, y) in enumerate(pts):
        rows_full[y].append(i)
        cols_full[x].append(i)
    closed = True
    bad_rows, bad_cols = [], []
    ys_touched = {pts[i][1] for i in omega}
    xs_touched = {pts[i][0] for i in omega}
    for y in ys_touched:
        mem = rows_full[y]
        if not all(i in omega for i in mem):
            closed = False
            bad_rows.append(y)
    for x in xs_touched:
        mem = cols_full[x]
        if not all(i in omega for i in mem):
            closed = False
            bad_cols.append(x)
    facts['closed'] = closed
    facts['bad_rows'] = bad_rows
    facts['bad_cols'] = bad_cols

    # (ii) LP(Omega) over ALL lines of P restricted to Omega (>=3 pts)
    lp_val, fam_counts, n_constr = lp_on_omega(omega, pts, lines)
    facts['LP'] = lp_val
    facts['LP_constraint_families'] = fam_counts
    facts['LP_n_constraints'] = n_constr
    facts['LP_eq_28'] = abs(lp_val - 28.0) < 1e-6

    # (iii) integral cover: 12 lines (7,5,3) of the four groups + 4 singleton points
    diag_d = gdiags[d]      # [(c,size),...] desc, size profile should be (7,5,3,1)
    diag_nd = gdiags[nd]
    anti_d = antidiag_lines_for_negd(pts, p, lines, d)     # G'_d
    anti_nd = antidiag_lines_for_negd(pts, p, lines, nd)   # G'_{-d}
    four_groups = {'G_d': diag_d, 'G_-d': diag_nd, "G'_d": anti_d, "G'_-d": anti_nd}
    profiles_ok = all(tuple(sz for _, sz in v) == (7, 5, 3, 1) for v in four_groups.values())
    facts['four_groups_profile_ok'] = profiles_ok
    facts['four_groups_profiles'] = {k: [sz for _, sz in v] for k, v in four_groups.items()}

    twelve_lines = {}   # label -> list of point idx, for the 7,5,3 lines only
    singles = {}         # label -> point idx, for the 1-point lines
    kind_of = {'G_d': 'd', 'G_-d': 'd', "G'_d": 'a', "G'_-d": 'a'}
    for gname, diaglist in four_groups.items():
        fam = kind_of[gname]
        for c, sz in diaglist:
            mem = [i for i in lines[(fam, c)]]
            label = f"{gname}:{fam}{c:+d}(sz{sz})"
            if sz == 1:
                singles[f"{gname}:{fam}{c:+d}"] = mem[0]
            else:
                twelve_lines[label] = mem

    union12 = set()
    overlap_points = Counter()
    for lab, mem in twelve_lines.items():
        for i in mem:
            overlap_points[i] += 1
            union12.add(i)
    facts['n_12lines'] = len(twelve_lines)
    facts['union12_size'] = len(union12)
    facts['sum_sizes_12'] = sum(len(v) for v in twelve_lines.values())
    facts['twelve_disjoint'] = (facts['union12_size'] == facts['sum_sizes_12'] == 60)
    dup = [i for i, c in overlap_points.items() if c > 1]
    facts['dup_points_in_12lines'] = len(dup)

    single_pts = set(singles.values())
    facts['n_singletons'] = len(single_pts)
    facts['singletons_distinct'] = (len(single_pts) == 4)

    covered = union12 | single_pts
    facts['covers_omega'] = (covered == omega)
    facts['omega_minus_covered'] = sorted(omega - covered)
    facts['covered_minus_omega'] = sorted(covered - omega)

    uncovered_by_12 = omega - union12
    facts['uncovered_by_12_equals_singletons'] = (uncovered_by_12 == single_pts)
    facts['uncovered_by_12_size'] = len(uncovered_by_12)

    # does the 7-line of G_d meet any line of G'_d or G'_{-d} (or the 5-,3-lines similarly)?
    def line_pts(gname, sz):
        for c, s in four_groups[gname]:
            if s == sz:
                return set(lines[(kind_of[gname], c)])
        return set()
    cross_hits = []
    for sz_d in (7, 5, 3):
        Ld = line_pts('G_d', sz_d)
        for gname_a in ("G'_d", "G'_-d"):
            for sz_a in (7, 5, 3):
                La = line_pts(gname_a, sz_a)
                inter = Ld & La
                if inter:
                    cross_hits.append((f"G_d:{sz_d}", f"{gname_a}:{sz_a}", sorted(inter)))
    facts['cross_hits_Gd_vs_Gprime'] = cross_hits

    facts['exception'] = not (facts['size_ok'] and facts['closed'] and facts['LP_eq_28']
                               and facts['twelve_disjoint'] and facts['covers_omega']
                               and facts['uncovered_by_12_equals_singletons']
                               and profiles_ok)
    return facts


def run_p(p, verbose=True):
    t0 = time.time()
    pts, idx, h = build_P(p)
    lines = build_lines(pts, idx)
    grp, gtype, gdiags = group_types(pts, p, lines)
    m7_ds = sorted(d for d, t in gtype.items() if t == (7, 5, 3, 1))
    m8 = sum(1 for t in gtype.values() if t == (8, 4, 4))
    m6groups = sum(1 for t in gtype.values() if t == (6, 6, 2, 2))
    m7 = len(m7_ds)

    # pair up d <-> -d ; verify pairing structure while doing so
    seen = set()
    pair_issues = []
    orbit_pairs = []
    for d in m7_ds:
        if d in seen:
            continue
        nd = (-d) % p
        seen.add(d)
        if nd == d:
            pair_issues.append(('self-paired d==-d', d))
            continue
        if nd not in gtype or gtype[nd] != (7, 5, 3, 1):
            pair_issues.append(('partner -d not type (7,5,3,1)', d, nd, gtype.get(nd)))
            continue
        seen.add(nd)
        orbit_pairs.append((d, nd))

    orbit_results = []
    for d, nd in orbit_pairs:
        facts = check_orbit(p, pts, idx, lines, gtype, gdiags, d)
        orbit_results.append(facts)

    n_LP28 = sum(1 for f in orbit_results if f['LP_eq_28'])
    n_exceptions = sum(1 for f in orbit_results if f['exception']) + len(pair_issues)

    summary = {
        'p': p, 'n_pts': len(pts), 'h': h,
        'm8': m8, 'm7': m7, 'm6groups': m6groups,
        'n_orbits_checked': len(orbit_results),
        'n_LP_eq_28': n_LP28,
        'n_exceptions': n_exceptions,
        'pair_issues': pair_issues,
        'elapsed': time.time() - t0,
    }
    if verbose:
        print(f"p={p:4d}  n_pts={len(pts):5d}  m8={m8:3d} m7={m7:3d} m6groups={m6groups:3d}  "
              f"orbits={len(orbit_results):3d} LP=28:{n_LP28:3d} exc={n_exceptions:2d}  "
              f"({summary['elapsed']:.2f}s)", flush=True)
    return summary, orbit_results


if __name__ == "__main__":
    pmin = int(sys.argv[1]) if len(sys.argv) > 1 else 11
    pmax = int(sys.argv[2]) if len(sys.argv) > 2 else 500
    ps = primes_between(pmin, pmax)
    print(f"# primes in [{pmin},{pmax}]: {len(ps)}", flush=True)
    all_summary = []
    all_detail = {}
    exceptions_log = []
    t_start = time.time()
    for p in ps:
        summary, orbit_results = run_p(p)
        all_summary.append(summary)
        # keep only compact per-orbit facts for JSON (drop giant point lists)
        compact = []
        for f in orbit_results:
            c = {k: v for k, v in f.items() if k not in (
                'omega_minus_covered', 'covered_minus_omega')}
            compact.append(c)
        all_detail[p] = compact
        for f in orbit_results:
            if f['exception']:
                exceptions_log.append((p, f))
        if summary['pair_issues']:
            exceptions_log.append((p, {'pair_issues': summary['pair_issues']}))
    total_elapsed = time.time() - t_start
    print(f"# total elapsed {total_elapsed:.1f}s", flush=True)

    with open('slack/t221_agents/orbit_cover_output.txt', 'w') as f:
        f.write("orbit_cover.py output — T2.21 task A ((7,5,3,1) orbit-cover lemma), k=-1\n")
        f.write(f"primes checked: {pmin} <= p <= {pmax}, all primes, count={len(ps)}; total runtime {total_elapsed:.1f}s\n")
        f.write("columns: p, n_pts=|P|, m8=#(8,4,4)-groups, m7=#(7,5,3,1)-groups, m6groups=#(6,6,2,2)-groups,\n")
        f.write("         orbits=#distinct {d,-d} orbits checked (=m7/2 unless a pairing issue), LP28=#orbits with LP(Omega)=28,\n")
        f.write("         exceptions=#orbits (or pairings) failing any check\n")
        f.write(f"{'p':>5} {'n_pts':>7} {'m8':>4} {'m7':>4} {'m6grp':>6} {'orbits':>7} {'LP28':>5} {'exc':>4}\n")
        for s in all_summary:
            f.write(f"{s['p']:5d} {s['n_pts']:7d} {s['m8']:4d} {s['m7']:4d} {s['m6groups']:6d} "
                     f"{s['n_orbits_checked']:7d} {s['n_LP_eq_28']:5d} {s['n_exceptions']:4d}\n")
        f.write("\n")
        n_p_with_exc = sum(1 for s in all_summary if s['n_exceptions'] > 0)
        tot_orbits = sum(s['n_orbits_checked'] for s in all_summary)
        tot_LP28 = sum(s['n_LP_eq_28'] for s in all_summary)
        tot_exc = sum(s['n_exceptions'] for s in all_summary)
        f.write(f"TOTALS: primes={len(ps)}, orbits_checked={tot_orbits}, LP=28 count={tot_LP28}, "
                f"exceptions={tot_exc}, primes with >=1 exception={n_p_with_exc}\n\n")
        if exceptions_log:
            f.write("EXCEPTIONS (full detail):\n")
            for p, e in exceptions_log:
                f.write(f"  p={p}: {e}\n")
        else:
            f.write("EXCEPTIONS: none.\n")

    with open('slack/t221_agents/orbit_cover_detail.json', 'w') as f:
        json.dump({'params': {'pmin': pmin, 'pmax': pmax}, 'summary': all_summary, 'detail': all_detail}, f, indent=1)

    print("wrote slack/t221_agents/orbit_cover_output.txt and orbit_cover_detail.json")
