"""m_shells.py -- Task B: how does alpha grow with the NUMBER of shells m?

For p in {11,13,17,19,23} and m in {1,2,3,4,6,8,12}, three families of shell constants:
  (i)   signed sequence  {1,-1,2,-2,3,-3,...}          (first m terms, m <= p-1)
  (ii)  multiplicative subgroup of F_p^* of order m     {g^(j*(p-1)/m) : j=0..m-1}   (only when m | p-1)
  (iii) m random distinct nonzero constants, 3 independent samples per (p,m)

For each set of constants cs, build the point set  H(c1) u ... u H(cm)  in the HJSW box
(via diffusion_sampler.hyper_points / build_lines -- SAME lines routine used everywhere else
in this repo for this problem, so lower/upper bounds are computed on an identical line set).

Lower bound: null_search.anneal (several seeds; the light-cone SA that reaches the exact
pair optimum 40 at p=13 in seconds).
Upper bound: lp_curve.solve -- the fractional line-cover LP over ALL lines with >=3 points
(this is a valid upper bound on the true max lawful subset since a lawful set meets every
line in <=2 points).

HYGIENE: every reported lower-bound subset is independently certified lawful (no 3 collinear)
by certify_lawful() below, a direct O(k^2) group-by-line scan over the RAW POINT COORDINATES
of the returned subset (not reusing the SA's internal bookkeeping / cnt arrays).

usage: m_shells.py [anneal_seconds] [anneal_seeds] [p_list] [m_list]
  e.g. m_shells.py 2 2                      -- default budget, all p, all m
       m_shells.py 3 3 11,13 1,2,4          -- restrict p and m (for quick tests)
"""
import sys, time, random, math
sys.path.insert(0, '/home/pmbot/projects/saturation_peer/slack')
from diffusion_sampler import hyper_points, build_lines
from null_search import anneal
from lp_curve import lines as lp_lines, solve as lp_solve


def primitive_root(p):
    if p == 2:
        return 1
    phi = p - 1
    n = phi
    fac = set()
    d = 2
    while d * d <= n:
        while n % d == 0:
            fac.add(d)
            n //= d
        d += 1
    if n > 1:
        fac.add(n)
    for g in range(2, p):
        if all(pow(g, phi // f, p) != 1 for f in fac):
            return g
    return None


def family_signed(p, m):
    cs = []
    j = 1
    while len(cs) < m and j < p:
        cs.append(j % p)
        if len(cs) < m:
            cs.append((-j) % p)
        j += 1
    return cs[:m] if len(cs) == m else None


def family_subgroup(p, m):
    if (p - 1) % m != 0:
        return None
    g = primitive_root(p)
    step = (p - 1) // m
    S = sorted({pow(g, j * step, p) for j in range(m)})
    return S if len(S) == m else None


def family_random(p, m, seed):
    if m > p - 1:
        return None
    rng = random.Random(seed)
    pool = list(range(1, p))
    rng.shuffle(pool)
    return sorted(pool[:m])


def certify_lawful(points):
    """Independent brute-force check: group by (reduced direction, offset), no group > 2 points.
    Operates directly on raw (x,y) coordinates -- does not touch the SA's line/membership arrays."""
    n = len(points)
    groups = {}
    for i in range(n):
        x1, y1 = points[i]
        for j in range(i + 1, n):
            x2, y2 = points[j]
            dx, dy = x2 - x1, y2 - y1
            g = math.gcd(abs(dx), abs(dy))
            ddx, ddy = dx // g, dy // g
            if ddx < 0 or (ddx == 0 and ddy < 0):
                ddx, ddy = -ddx, -ddy
            c = ddy * x1 - ddx * y1
            key = (ddx, ddy, c)
            s = groups.setdefault(key, set())
            s.add(i); s.add(j)
            if len(s) > 2:
                return False
    return True


def eval_set(p, cs, anneal_seconds, anneal_seeds):
    pts = hyper_points(p, cs)
    lines = build_lines(pts)
    best = 0
    best_pts = []
    for s in range(anneal_seeds):
        v, idx = anneal(pts, lines, seconds=anneal_seconds, seed=s)
        if v > best:
            best = v
            best_pts = [pts[i] for i in idx]
    lp = lp_solve(pts, lines)
    ok = certify_lawful(best_pts) if best_pts else True
    return len(pts), len(lines), best, lp, ok


def main():
    A_SEC = float(sys.argv[1]) if len(sys.argv) > 1 else 2.0
    A_SEEDS = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    P_LIST = [int(x) for x in sys.argv[3].split(',')] if len(sys.argv) > 3 else [11, 13, 17, 19, 23]
    M_LIST = [int(x) for x in sys.argv[4].split(',')] if len(sys.argv) > 4 else [1, 2, 3, 4, 6, 8, 12]

    t_start = time.time()
    rows = []  # (p, m, family, points, lines, alpha_lb, LP_ub, alpha/N, LP/N, certified)
    for p in P_LIST:
        N = 2 * p
        trivial = 2 * N
        print(f"\n=== p={p}  N=2p={N}  trivial bound 2N={trivial} ===", flush=True)
        for m in M_LIST:
            if m > p - 1:
                print(f"  m={m}: skipped (m > p-1={p-1}, not enough distinct nonzero constants)", flush=True)
                continue
            fams = []
            cs = family_signed(p, m)
            if cs is not None:
                fams.append(('signed', cs))
            cs = family_subgroup(p, m)
            if cs is not None:
                fams.append(('subgroup', cs))
            else:
                print(f"  m={m} family=subgroup: skipped (m does not divide p-1={p-1})", flush=True)
            for si in range(3):
                cs = family_random(p, m, seed=1000 * p + 10 * m + si)
                if cs is not None:
                    fams.append((f'random#{si}', cs))

            for fname, cs in fams:
                npts, nlines, lb, ub, ok = eval_set(p, cs, A_SEC, A_SEEDS)
                lb_N = lb / N
                ub_N = ub / N
                cert = "CERTIFIED" if ok else "FAILED-CERT"
                print(f"  m={m:2d} {fname:10s} cs={cs} pts={npts:4d} lines={nlines:5d} "
                      f"alpha_lb={lb:4d} ({lb_N:.3f}N)  LP_ub={ub:7.2f} ({ub_N:.3f}N)  [{cert}]", flush=True)
                rows.append((p, m, fname, npts, nlines, lb, ub, lb_N, ub_N, ok))

    print(f"\n[total wall time {time.time()-t_start:.0f}s]", flush=True)

    # summary: per p, the m that maximizes alpha_lb/N (over the best family at that m)
    print("\n=== SUMMARY: best alpha/N per (p, m) [max over families], and argmax_m ===", flush=True)
    from collections import defaultdict
    best_by_pm = {}
    for (p, m, fname, npts, nlines, lb, ub, lb_N, ub_N, ok) in rows:
        if not ok:
            continue
        key = (p, m)
        if key not in best_by_pm or lb > best_by_pm[key][0]:
            best_by_pm[key] = (lb, lb_N, ub, ub_N, fname)
    for p in P_LIST:
        N = 2 * p
        line = f"p={p:2d}:"
        best_m = None; best_val = -1
        for m in M_LIST:
            key = (p, m)
            if key in best_by_pm:
                lb, lb_N, ub, ub_N, fname = best_by_pm[key]
                line += f"  m={m}:{lb_N:.3f}N({fname})"
                if lb_N > best_val:
                    best_val = lb_N; best_m = m
        line += f"   -> argmax_m = {best_m} at {best_val:.3f}N"
        print(line, flush=True)


if __name__ == '__main__':
    main()
