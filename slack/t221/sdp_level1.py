"""sdp_level1.py — hole H1 (docs/research/integrality/holes.py): level-1 Lasserre / Lovász–Schrijver
SDP relaxation of the "lawful subset" problem for the two-hyperbola point set P (candidate set of
slack/lp1_anatomy.py: xy ≡ ±1 (mod p) lifted into the 2p×2p window; P = {(x,y): x in [-h,3h+1],
y in [0,2p-1], x*y mod p in {1,p-1}}, h=(p-1)/2, |P| = 8(p-1)); compared with the LP relaxation
(all lines) and the exact maxima.  See docs/research/integrality/phenomenon.py for the "weak vs
strong lines" framing this experiment tests: does a level-1 SDP moment lift, localized at every
>=3-point line of every slope, see the joint effect of the ~p log p WEAK (3-point) lines that a
purely linear (rank-1 / weighted-cover) certificate provably cannot (P2 "fractional blindness")?

Lines: every line of the plane through >= 3 points of P, all slopes, found by the standard
pairwise-canonical-key sweep (same convention as slack/maxlawful_pysat.py's lines()): for a pair of
points, reduce (dx,dy)=(x2-x1,y2-y1) by gcd, fix the sign so dx>0 or (dx=0 and dy>0), and key on
(dx,dy, dx*y1-dy*x1).  "Strong" lines = rows, columns, slope ±1 (direction in
{(1,0),(0,1),(1,1),(1,-1)}); everything else is a "weak" line (almost all of them exactly 3 points).

SDP (level 1, symmetric moment matrix M = [[1, y^T],[y, Y]] >= 0, y_i ~ E[x_i], Y_ij ~ E[x_i x_j]):
  diag(Y) = y ; 0 <= Y_ij <= min(y_i,y_j) ; Y_ij >= y_i+y_j-1   (McCormick/RLT box for x_i,x_j in {0,1})
For every line l (>=3 pts) and every point j:
  (a) sum_{i in l} Y_ij <= 2 y_j                    [line-constraint × x_j]
  (b) sum_{i in l} (y_i - Y_ij) <= 2 (1 - y_j)       [line-constraint × (1 - x_j)]
  and plainly sum_{i in l} y_i <= 2 for every line.
Maximize sum_i y_i.  NOTE (task's key question): for a 3-point line {a,b,c}, (a) with j=a reads
Y_ab + Y_ac <= y_a — a genuine "no three" constraint at the level of PAIR moments, something no
linear weighting of lines (the LP) can express.  Does the SDP value actually drop below LP because
of it?  That's what this script measures.

Constraint-count policy (task's option (i), to keep problem size tractable): (a)/(b) are imposed
  - for j in l only, for 3-point lines (the ~p log p weak lines: there are too many to afford "all j"),
  - for ALL j in P, for lines with >= 4 points (rows/columns/slope-±1 — few, and where "all j" is
    affordable; this is also where LP already gets most of its strength, so this is the fair
    like-for-like extension of the LP's own strong lines).
This is POLICY (i) of the task instructions; see the report for the constraint-count comparison
against policy (ii) (all j, always).

Two SDP variants are computed per line set:
  - "local"  = the full construction above (localizing constraints included);
  - "theta"  = SAME moment-matrix/box/RLT constraints, PLAIN line constraints only, NO (a)/(b).
    This is provably == LP(the same line set): for any y feasible in the LP, Y := y y^T is PSD
    (rank 1) and satisfies 0<=Y<=min(y_i,y_j) and Y_ij>=y_i+y_j-1 automatically (since
    y_i+y_j-1-y_i y_j = -(1-y_i)(1-y_j) <= 0 for y in [0,1]^n).  It is included as a solver sanity
    check / the "pure Lovász-theta-like variant without localizing constraints" the task asks for.

Also computed: the same "local" SDP restricted to ONLY rows/columns/±1 lines (drop every weak
3-point line from BOTH the line set and the localizing constraints), to isolate what the localizing
lift buys on the strong lines alone vs. what it buys once the weak lines are added in.

usage: python3 slack/t221/sdp_level1.py p [p ...]
env:   SDP_SOLVERS="SCS"   (default; comma list, first one that returns optimal/optimal_inaccurate wins)
       SDP_VERBOSE=1       (pass verbose=True to the solver)
"""
from __future__ import annotations
import sys, os, time, math, json
from collections import defaultdict
import numpy as np
from scipy.optimize import linprog
import cvxpy as cp

STRONG_DIRS = {(1, 0), (0, 1), (1, 1), (1, -1)}
# SCS (first-order ADMM) is the default: benchmarking showed CLARABEL (interior-point) stalls for
# minutes already at p=13's "local, all lines" problem (~13k linear constraints + a 97x97 PSD cone),
# while SCS solves the same problem in seconds at ~1e-5 accuracy.  CLARABEL is fine for the small
# "theta" (no-localizing) problems but is NOT in the default fallback chain for the heavy ones, to
# avoid an unbounded stall; set SDP_SOLVERS=CLARABEL,SCS explicitly to try it first anyway.
SOLVERS = os.environ.get("SDP_SOLVERS", "SCS").split(",")
VERBOSE = bool(int(os.environ.get("SDP_VERBOSE", "0")))


def points(p):
    h = (p - 1) // 2
    return [(x, y) for x in range(-h, 3 * h + 2) for y in range(0, 2 * p) if (x * y) % p in (1, p - 1)]


def all_lines(pts):
    """dict: canonical line key (dx,dy,c0) -> sorted tuple of point indices, for every line with >=3 points."""
    n = len(pts)
    groups = defaultdict(set)
    for i in range(n):
        x1, y1 = pts[i]
        for j in range(i + 1, n):
            x2, y2 = pts[j]
            dx, dy = x2 - x1, y2 - y1
            g = math.gcd(abs(dx), abs(dy)); dx //= g; dy //= g
            if dx < 0 or (dx == 0 and dy < 0): dx, dy = -dx, -dy
            c0 = dx * y1 - dy * x1
            key = (dx, dy, c0)
            groups[key].add(i); groups[key].add(j)
    return {key: tuple(sorted(s)) for key, s in groups.items() if len(s) >= 3}


def size_hist(lines):
    h = defaultdict(int)
    for mem in lines.values(): h[len(mem)] += 1
    return dict(sorted(h.items()))


def lp_value(n, mem_list):
    L = len(mem_list)
    A = np.zeros((L, n))
    for i, mem in enumerate(mem_list):
        for j in mem: A[i, j] = 1.0
    t0 = time.time()
    res = linprog(-np.ones(n), A_ub=A, b_ub=2 * np.ones(L), bounds=(0, 1), method='highs')
    if not res.success: raise RuntimeError(f"LP failed: {res.message}")
    return -res.fun, time.time() - t0


def build_sdp(n, mem_list, localizing=True):
    y = cp.Variable(n, nonneg=True)
    Y = cp.Variable((n, n), symmetric=True)
    top = cp.hstack([np.array([1.0]), y])
    bot = cp.hstack([cp.reshape(y, (n, 1), order='C'), Y])
    M = cp.vstack([cp.reshape(top, (1, n + 1), order='C'), bot])
    yrow = cp.reshape(y, (1, n), order='C')
    ycol = cp.reshape(y, (n, 1), order='C')
    cons = [cp.diag(Y) == y, Y >= 0, Y <= yrow, Y >= ycol + yrow - 1, y <= 1, M >> 0]

    Afull = np.zeros((len(mem_list), n))
    for i, mem in enumerate(mem_list):
        for j in mem: Afull[i, j] = 1.0
    cons.append(Afull @ y <= 2)                                   # plain, every line

    n_local_pairs = 0
    if localizing:
        big = [mem for mem in mem_list if len(mem) >= 4]
        small = [mem for mem in mem_list if len(mem) == 3]
        if big:
            Ab = np.zeros((len(big), n))
            for i, mem in enumerate(big):
                for j in mem: Ab[i, j] = 1.0
            AbY = Ab @ Y
            cons.append(AbY <= 2 * yrow)                                          # (a), all j
            sums = cp.reshape(Ab @ y, (len(big), 1), order='C')
            cons.append(sums - AbY <= 2 - 2 * yrow)                               # (b), all j
            n_local_pairs += len(big) * n
        for mem in small:
            i0, i1, i2 = mem
            for (j, a, b) in ((i0, i1, i2), (i1, i0, i2), (i2, i0, i1)):
                cons.append(Y[a, j] + Y[b, j] <= y[j])                            # (a), j in l
                cons.append((y[a] - Y[a, j]) + (y[b] - Y[b, j]) <= 2 * (1 - y[j]))  # (b), j in l
            n_local_pairs += 3
    prob = cp.Problem(cp.Maximize(cp.sum(y)), cons)
    return prob, n_local_pairs


TIME_LIMIT = float(os.environ.get("SDP_TIME_LIMIT", "0")) or None  # seconds; SCS only


def solve(prob):
    last_err = None
    for name in SOLVERS:
        name = name.strip()
        try:
            t0 = time.time()
            kwargs = dict(verbose=VERBOSE)
            if name == "SCS" and TIME_LIMIT: kwargs["time_limit_secs"] = TIME_LIMIT
            prob.solve(solver=getattr(cp, name), **kwargs)
            dt = time.time() - t0
            if prob.value is not None and prob.status in ("optimal", "optimal_inaccurate"):
                stats = prob.solver_stats
                bits = []
                if stats and stats.solve_time: bits.append(f"solve_time={stats.solve_time:.2f}s")
                if stats and stats.num_iters: bits.append(f"iters={stats.num_iters}")
                try:
                    info = stats.extra_stats["info"]
                    bits.append(f"res_pri={info['res_pri']:.2e}")
                    bits.append(f"res_dual={info['res_dual']:.2e}")
                    bits.append(f"gap={info['gap']:.2e}")
                except Exception:
                    pass
                return dict(solver=name, status=prob.status, value=prob.value, wall=dt, extra=" ".join(bits))
        except Exception as e:
            last_err = e
            continue
    return dict(solver="/".join(SOLVERS), status=f"FAILED ({last_err})", value=float('nan'), wall=float('nan'), extra="")


EXACT = {11: 32, 13: 40, 17: 54, 19: 59}


def run(p):
    t0 = time.time()
    pts = points(p); n = len(pts)
    assert n == 8 * (p - 1), (n, 8 * (p - 1))
    lines = all_lines(pts)
    mem_all = list(lines.values())
    mem_strong = [mem for key, mem in lines.items() if (key[0], key[1]) in STRONG_DIRS]
    hist = size_hist(lines)
    hist_strong = size_hist({k: v for k, v in lines.items() if (k[0], k[1]) in STRONG_DIRS})
    print(f"\n===== p={p}  h={(p-1)//2}  |P|={n}  lines(all)={len(mem_all)} sizes={hist}  "
          f"lines(strong)={len(mem_strong)} sizes={hist_strong}  [setup {time.time()-t0:.2f}s]", flush=True)

    lp_all, t_lp_all = lp_value(n, mem_all)
    lp_strong, t_lp_strong = lp_value(n, mem_strong)
    print(f"  LP(all lines)      = {lp_all:.4f}  = {lp_all/(p-1):.4f}(p-1)   [{t_lp_all:.2f}s]", flush=True)
    print(f"  LP(strong only)    = {lp_strong:.4f}  = {lp_strong/(p-1):.4f}(p-1)   [{t_lp_strong:.2f}s]", flush=True)

    results = {"p": p, "n": n, "n_lines_all": len(mem_all), "n_lines_strong": len(mem_strong),
               "hist_all": hist, "hist_strong": hist_strong,
               "lp_all": lp_all, "lp_strong": lp_strong, "exact": EXACT.get(p)}

    prob, npairs = build_sdp(n, mem_all, localizing=False)
    r = solve(prob)
    print(f"  SDP theta (all lines, NO localizing)  = {r['value']:.4f}  "
          f"[{r['solver']} {r['status']} {r['wall']:.2f}s {r['extra']}]  (sanity check: should == LP(all))", flush=True)
    results["theta_all"] = r

    prob, npairs = build_sdp(n, mem_strong, localizing=True)
    print(f"  building SDP(local, strong-only): {npairs} localized (line,point) pairs ...", flush=True)
    r = solve(prob)
    print(f"  SDP local (strong-only lines)         = {r['value']:.4f}  "
          f"[{r['solver']} {r['status']} {r['wall']:.2f}s {r['extra']}]", flush=True)
    results["local_strong"] = r

    prob, npairs = build_sdp(n, mem_all, localizing=True)
    print(f"  building SDP(local, all lines): {npairs} localized (line,point) pairs ...", flush=True)
    r = solve(prob)
    print(f"  SDP local (ALL lines)                 = {r['value']:.4f}  "
          f"[{r['solver']} {r['status']} {r['wall']:.2f}s {r['extra']}]", flush=True)
    results["local_all"] = r

    print(f"  exact max = {EXACT.get(p, 'unknown')}", flush=True)
    print(f"  ---> gap LP(all)-exact = {lp_all-EXACT[p]:.3f}" if p in EXACT else "", flush=True)
    if p in EXACT and results["local_all"]["value"] == results["local_all"]["value"]:
        gap_lp = lp_all - EXACT[p]
        gap_sdp = results["local_all"]["value"] - EXACT[p]
        closed = 100 * (1 - gap_sdp / gap_lp) if gap_lp > 1e-9 else float('nan')
        print(f"  ---> SDP closes {closed:.1f}% of the LP-exact gap ({gap_lp:.3f} -> {gap_sdp:.3f})", flush=True)
    return results


if __name__ == "__main__":
    all_results = []
    for a in sys.argv[1:]:
        p = int(a)
        all_results.append(run(p))
    out = os.path.join(os.path.dirname(__file__), "sdp_level1_results.json")
    with open(out, "w") as f:
        json.dump(all_results, f, indent=1, default=str)
    print(f"\nwrote {out}")
