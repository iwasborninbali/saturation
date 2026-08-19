"""exchange_test.py -- numerical test of the exchange/matching lemma H4 (docs/research/integrality/holes.py)
and of B.13 (docs/research/pair_bound_notes.md, grep "B.13"): the claim that the trade-off between the two
lifted hyperbolae has slope exactly 1 -- "each point of H(-1) costs one point of H(1)".

Setup (mirrors the task spec / pair_bound_notes.md Part A section 1 and Part B section 9):
  p odd prime, h = (p-1)//2, box G(p) = [-h, 3h+1] x [0, 2p-1].
  H1 = lifts of xy == 1 (mod p): for each nonzero residue a (window x_a in [-h,h]), y_a = a^{-1} mod p in
       [1,p-1]; the 4 lifts are (x_a + r*p, y_a + s*p), r,s in {0,1}.  |H1| = 4(p-1).
  H2 = lifts of xy == -1 (mod p): same recipe with y_a = -a^{-1} mod p.  |H2| = 4(p-1).
  A set S subset H1 u H2 is LAWFUL if every line of the plane meets S in at most 2 points.
  Known (theorem, computed exactly below as a check): max lawful subset of H1 alone = 3(p-1).
  Known exact/ranged maxima of H1 u H2 (k=-1): p=11:32, 13:40, 17:54, 19:59, 23: 70-74.

f(t) := max{ |S n H2| : S lawful, |S n H1| >= 3(p-1) - t }         (B.13's trade-off function)

Identity used throughout (elementary, proved in the report): for EVERY t,
    3(p-1) - t + f(t)  <=  alpha(H1 u H2)   ,     and    max_t ( 3(p-1) - t + f(t) ) = alpha(H1 u H2) exactly.
So a full, *exactly solved* f(t)-sweep re-derives alpha independently of the earlier direct MILP runs.

Four parts (see main() / run_prime()):
  1. Build H1, H2 and all lines with >= 3 points of H1 u H2 (rich lines); "lawful" = <= 2 per rich line.
  2. f(t) for t = 0 .. 3(p-1) (coarse grid for large p) via OR-tools CP-SAT (binary var per point, line
     constraints sum <= 2, threshold on |S n H1|, maximize |S n H2|).  Table t, f(t), f(t)-t, and where
     3(p-1)-t+f(t) is maximal.
  3. Enumerate ALL (or up to CAP) maximum lawful subsets M of H1 (size 3(p-1)) via CP-SAT's exhaustive
     solution enumeration (a no-good-cut search under the hood); for each M and each q in H2, count the
     number of pairs {a,b} subset M with a,b,q collinear ("q sees a pair of M").  Distribution over q; in
     particular whether EVERY q sees >= 1 pair for EVERY M (blocking-hypergraph statement of B.13 item (1)).
  4. For t = 1..4: take the optimal witness S from part 2, find its nearest (by symmetric difference) M
     from part 3's catalogue, and describe the "holes" M \\ S1 and the added H2 points S2 structurally
     (same class / same column / common line?).

Usage:
  /Users/iwasborninbali/venvs/sat/bin/python3 slack/t221/exchange_test.py [p1 p2 ...]
  (default primes: 11 13 17 19 23; pass e.g. "29" or "31" separately -- see PRIME_CONFIG for their coarser
  grid/time budget.  Safe to re-run: results are checkpointed to exchange_test_results.json and already
  solved (p,t) pairs are skipped.)
"""
from __future__ import annotations

import json
import os
import sys
import time
from math import comb, gcd

from ortools.sat.python import cp_model

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS_PATH = os.path.join(HERE, "exchange_test_results.json")

KNOWN_ALPHA = {11: (32, 32), 13: (40, 40), 17: (54, 54), 19: (59, 59), 23: (70, 74)}

# ---------------------------------------------------------------------------
# Part 1: geometry -- H1, H2, and the rich-line hypergraph
# ---------------------------------------------------------------------------


def h_points(p: int, k: int) -> list[tuple[int, int, int, int, int]]:
    """Lifts of xy == k (mod p) in G(p) = [-h,3h+1] x [0,2p-1].  Returns (x, y, a, r, s) with a the
    residue-class label (x_a in [-h,h] the representative of a mod p), r,s in {0,1} the lift bits:
    x = x_a + r*p, y = y_a + s*p, y_a = (k * a^{-1} mod p) in [1,p-1].  |output| = 4(p-1)."""
    h = (p - 1) // 2
    kk = k % p
    pts = []
    for a in range(1, p):
        xa = a if a <= h else a - p
        ya = (kk * pow(a, p - 2, p)) % p
        assert 1 <= ya <= p - 1
        for r in (0, 1):
            for s in (0, 1):
                pts.append((xa + r * p, ya + s * p, a, r, s))
    return pts


def build_lines(coords: list[tuple[int, int]]) -> list[tuple[int, ...]]:
    """All maximal collinear subsets (>=3 members) of coords, as sorted index tuples.  O(n^2) pairs,
    canonical (reduced-direction, offset) key per line."""
    n = len(coords)
    seen: dict[tuple[int, int, int], set[int]] = {}
    for i in range(n):
        xi, yi = coords[i]
        for j in range(i + 1, n):
            xj, yj = coords[j]
            dx, dy = xj - xi, yj - yi
            g = gcd(abs(dx), abs(dy))
            dx //= g
            dy //= g
            if dx < 0 or (dx == 0 and dy < 0):
                dx, dy = -dx, -dy
            c0 = dx * yi - dy * xi
            key = (dx, dy, c0)
            s = seen.get(key)
            if s is None:
                seen[key] = s = set()
            s.add(i)
            s.add(j)
    return [tuple(sorted(m)) for m in seen.values() if len(m) >= 3]


def build_system(p: int) -> dict:
    h1 = h_points(p, 1)
    h2 = h_points(p, -1)
    pts = h1 + h2
    coords = [(x, y) for x, y, a, r, s in pts]
    assert len(set(coords)) == len(coords), "H1, H2 lifts must be pairwise distinct points"
    n = len(pts)
    n1 = len(h1)
    in_h1 = [1] * n1 + [0] * len(h2)
    in_h2 = [0] * n1 + [1] * len(h2)
    L = build_lines(coords)
    L1 = build_lines(coords[:n1])  # rich lines restricted to H1 alone
    lines_at = [[] for _ in range(n)]
    for li, mem in enumerate(L):
        for i in mem:
            lines_at[i].append(li)
    return dict(p=p, h1=h1, h2=h2, pts=pts, coords=coords, n=n, n1=n1,
                in_h1=in_h1, in_h2=in_h2, L=L, L1=L1, lines_at=lines_at)


# ---------------------------------------------------------------------------
# Part 2: f(t) by CP-SAT
# ---------------------------------------------------------------------------


def solve_ft(sysd: dict, t: int, time_limit: float, workers: int = 8) -> dict:
    n, L, in_h1, in_h2, p = sysd["n"], sysd["L"], sysd["in_h1"], sysd["in_h2"], sysd["p"]
    model = cp_model.CpModel()
    xs = [model.NewBoolVar(f"x{i}") for i in range(n)]
    for mem in L:
        model.Add(sum(xs[i] for i in mem) <= 2)
    model.Add(sum(xs[i] for i in range(n) if in_h1[i]) >= 3 * (p - 1) - t)
    model.Maximize(sum(xs[i] for i in range(n) if in_h2[i]))
    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = workers
    solver.parameters.max_time_in_seconds = time_limit
    status = solver.Solve(model)
    if status == cp_model.UNKNOWN:  # one retry with more time if not even a feasible point was found
        solver.parameters.max_time_in_seconds = max(time_limit * 3, 10.0)
        status = solver.Solve(model)
    ok = status in (cp_model.OPTIMAL, cp_model.FEASIBLE)
    f_val = int(round(solver.ObjectiveValue())) if ok else None
    chosen = sorted(i for i in range(n) if ok and solver.Value(xs[i])) if ok else None
    return dict(t=t, f=f_val, bound=solver.BestObjectiveBound(), status=solver.StatusName(status),
                optimal=(status == cp_model.OPTIMAL), chosen=chosen, wall=solver.WallTime())


def t_grid(tmax: int, step: int, dense_upto: int = 15) -> list[int]:
    ts = list(range(0, min(dense_upto, tmax) + 1))
    t = ts[-1] + step if ts else 0
    while t <= tmax:
        ts.append(t)
        t += step
    if ts[-1] != tmax:
        ts.append(tmax)
    return sorted(set(ts))


PRIME_CONFIG = {
    11: dict(step=1, time_limit=20.0, wall_budget=300),
    13: dict(step=1, time_limit=20.0, wall_budget=400),
    17: dict(step=1, time_limit=15.0, wall_budget=520),
    19: dict(step=1, time_limit=6.0, wall_budget=220),
    23: dict(step=1, time_limit=4.0, wall_budget=220),
    29: dict(step=2, time_limit=3.0, wall_budget=150),
    31: dict(step=2, time_limit=3.0, wall_budget=150),
}


def default_config(p: int) -> dict:
    return PRIME_CONFIG.get(p, dict(step=(1 if p <= 23 else 2), time_limit=8.0, wall_budget=400))


def sweep_ft(sysd: dict, cache: dict, log=print) -> list[dict]:
    p = sysd["p"]
    cfg = default_config(p)
    tmax = 3 * (p - 1)
    ts = t_grid(tmax, cfg["step"])
    pcache = cache.setdefault(str(p), {})
    out = []
    t0 = time.time()
    remaining_ts = [t for t in ts if str(t) not in pcache]
    for idx, t in enumerate(ts):
        key = str(t)
        if key in pcache:
            out.append(pcache[key])
            continue
        pos = remaining_ts.index(t)
        elapsed = time.time() - t0
        remaining_budget = cfg["wall_budget"] - elapsed
        remaining_n = len(remaining_ts) - pos
        tl = cfg["time_limit"]
        if remaining_n > 0:
            fair = remaining_budget / remaining_n
            if fair < tl:
                tl = max(1.5, fair)
        r = solve_ft(sysd, t, time_limit=tl)
        pcache[key] = r
        save_cache(cache)
        gain = (r["f"] - t) if r["f"] is not None else None
        log(f"p={p} t={t:3d}: f(t)={r['f']!s:>4} bound<={r['bound']:.1f} gain(f-t)={gain!s:>3} "
            f"status={r['status']:<9} tl={tl:5.1f}s wall={r['wall']:.1f}s", flush=True)
        out.append(r)
    return out


# ---------------------------------------------------------------------------
# Part 3: enumerate maximum lawful subsets of H1, and blocking-pair distribution
# ---------------------------------------------------------------------------


class _Collector(cp_model.CpSolverSolutionCallback):
    def __init__(self, xs, cap):
        super().__init__()
        self.xs = xs
        self.cap = cap
        self.solutions: list[frozenset] = []

    def on_solution_callback(self):
        sol = frozenset(i for i, v in enumerate(self.xs) if self.Value(v) == 1)
        self.solutions.append(sol)
        if len(self.solutions) >= self.cap:
            self.StopSearch()


def enumerate_max_h1(sysd: dict, cap: int = 100, time_limit: float = 60.0) -> tuple[list[frozenset], bool]:
    """All maximum lawful subsets of H1 (size 3(p-1)), up to `cap` (task suggests 50; we use 100 because
    p=13,17 have exactly 81 = 9^2 of them and we want the exact 9^s count intact).  Returns (list, exhausted)."""
    n1 = sysd["n1"]
    L1 = sysd["L1"]
    p = sysd["p"]
    model = cp_model.CpModel()
    xs = [model.NewBoolVar(f"x{i}") for i in range(n1)]
    for mem in L1:
        model.Add(sum(xs[i] for i in mem) <= 2)
    model.Add(sum(xs) == 3 * (p - 1))
    solver = cp_model.CpSolver()
    solver.parameters.enumerate_all_solutions = True
    solver.parameters.num_search_workers = 1
    solver.parameters.max_time_in_seconds = time_limit
    cb = _Collector(xs, cap)
    status = solver.Solve(model, cb)
    exhausted = status == cp_model.OPTIMAL and len(cb.solutions) < cap
    return cb.solutions, exhausted


def blocking_pairs(sysd: dict, M: frozenset, q: int) -> int:
    """#{ {a,b} subset M : a,b,q collinear } = sum over rich lines through q of C(|line n M|, 2)."""
    total = 0
    for li in sysd["lines_at"][q]:
        mem = sysd["L"][li]
        m = sum(1 for i in mem if i in M)
        if m >= 2:
            total += comb(m, 2)
    return total


def block_stats(sysd: dict, Ms: list[frozenset]) -> dict:
    n1 = sysd["n1"]
    n = sysd["n"]
    h2_idx = list(range(n1, n))
    per_M = []
    for M in Ms:
        Bs = [blocking_pairs(sysd, M, q) for q in h2_idx]
        per_M.append(dict(min=min(Bs), mean=sum(Bs) / len(Bs), max=max(Bs),
                           n0=sum(1 for b in Bs if b == 0), n1_=sum(1 for b in Bs if b == 1),
                           n2=sum(1 for b in Bs if b == 2)))
    fully_blocked = sum(1 for d in per_M if d["min"] >= 1)
    return dict(per_M=per_M, n_M=len(Ms), fully_blocked=fully_blocked,
                extendable=len(Ms) - fully_blocked,
                min_over_all=min(d["min"] for d in per_M) if per_M else None,
                mean_of_means=sum(d["mean"] for d in per_M) / len(per_M) if per_M else None,
                max_over_all=max(d["max"] for d in per_M) if per_M else None)


# ---------------------------------------------------------------------------
# Part 4: holes of S n H1 relative to a nearest maximum set, for small t
# ---------------------------------------------------------------------------


def trace_unblocking(sysd: dict, M: frozenset, holes: set, q: int) -> list[dict]:
    """For added point q, list every rich line through q with >=2 members of M (a "critical line" that
    HAD to lose a point for q to be addable), and which of its M-members is in `holes` (the point(s) whose
    deletion broke that blocking pair).  This makes the exchange mechanism of B.13 item (1) concrete:
    q in S2 forces holes to contain a transversal of q's blocking-pair matching."""
    pts = sysd["pts"]
    out = []
    for li in sysd["lines_at"][q]:
        mem = sysd["L"][li]
        in_M = [i for i in mem if i in M]
        if len(in_M) >= 2:
            broken = [i for i in in_M if i in holes]
            out.append(dict(line_members_in_M=[pts[i][2:] for i in in_M],
                             broken_by_deletion=[pts[i][2:] for i in broken],
                             fully_covered=len(broken) >= 1))
    return out


def analyze_holes(sysd: dict, Ms: list[frozenset], ft_results: list[dict],
                   ts_to_check=(1, 2, 3, 4)) -> dict:
    n1 = sysd["n1"]
    n = sysd["n"]
    pts = sysd["pts"]
    out = {}
    if not Ms:
        return out
    for r in ft_results:
        if r["t"] not in ts_to_check or r["chosen"] is None:
            continue
        t = r["t"]
        chosen = set(r["chosen"])
        S1 = frozenset(i for i in chosen if i < n1)
        S2 = frozenset(i for i in chosen if i >= n1)
        best_M = min(Ms, key=lambda M: len(M ^ S1))
        holes = set(sorted(best_M - S1))
        extra = sorted(S1 - best_M)
        holes_meta = [pts[i][2:] for i in sorted(holes)]  # (a, r, s)
        extra_meta = [pts[i][2:] for i in extra]
        s2_meta = [pts[i][2:] for i in sorted(S2)]
        hole_classes = {a for a, rr, ss in holes_meta}
        added_classes = {a for a, rr, ss in s2_meta}
        same_class = sorted(hole_classes & added_classes)
        unblocking = {}
        for q in sorted(S2):
            crit = trace_unblocking(sysd, best_M, holes, q)
            unblocking[str(pts[q][2:])] = dict(
                n_critical_lines=len(crit),
                all_covered=all(c["fully_covered"] for c in crit) if crit else True,
                lines=crit)
        out[t] = dict(f=r["f"], sym_diff=len(best_M ^ S1), n_holes=len(holes), n_extra=len(extra),
                      holes=holes_meta, extra_h1=extra_meta, added_h2=s2_meta,
                      hole_classes=sorted(hole_classes), added_classes=sorted(added_classes),
                      classes_in_common=same_class, unblocking=unblocking)
    return out


# ---------------------------------------------------------------------------
# checkpointing + driver
# ---------------------------------------------------------------------------


def load_cache() -> dict:
    if os.path.exists(RESULTS_PATH):
        with open(RESULTS_PATH) as fh:
            return json.load(fh)
    return {}


def save_cache(cache: dict) -> None:
    tmp = RESULTS_PATH + ".tmp"
    with open(tmp, "w") as fh:
        json.dump(cache, fh)
    os.replace(tmp, RESULTS_PATH)


def run_prime(p: int, cache: dict, log=print) -> None:
    log(f"\n=== p={p} ===", flush=True)
    sysd = build_system(p)
    log(f"p={p}: |H1|=|H2|={len(sysd['h1'])}  n={sysd['n']}  rich lines(H1uH2)={len(sysd['L'])} "
        f"rich lines(H1 only)={len(sysd['L1'])}", flush=True)

    # sanity: known theorem, max lawful subset of H1 alone = 3(p-1)
    key = f"h1_alone_max_{p}"
    if key not in cache:
        model = cp_model.CpModel()
        xs = [model.NewBoolVar(f"x{i}") for i in range(sysd["n1"])]
        for mem in sysd["L1"]:
            model.Add(sum(xs[i] for i in mem) <= 2)
        model.Maximize(sum(xs))
        solver = cp_model.CpSolver()
        solver.parameters.num_search_workers = 8
        solver.parameters.max_time_in_seconds = 30
        status = solver.Solve(model)
        val = int(round(solver.ObjectiveValue()))
        cache[key] = val
        save_cache(cache)
    log(f"p={p}: max lawful subset of H1 alone = {cache[key]}  (theorem: {3 * (p - 1)}) "
        f"{'OK' if cache[key] == 3 * (p - 1) else 'MISMATCH!!'}", flush=True)

    # part 2
    ft_results = sweep_ft(sysd, cache, log=log)
    best = max(((3 * (p - 1) - r["t"] + r["f"]), r["t"]) for r in ft_results if r["f"] is not None)
    lo, hi = KNOWN_ALPHA.get(p, (None, None))
    log(f"p={p}: max_t (3(p-1)-t+f(t)) = {best[0]} at t={best[1]}  "
        f"(known alpha = {lo if lo == hi else f'{lo}-{hi}'})", flush=True)

    # part 3
    mkey = f"max_h1_sets_{p}"
    if mkey not in cache:
        Ms, exhausted = enumerate_max_h1(sysd, cap=100, time_limit=90.0)
        cache[mkey] = dict(sets=[sorted(m) for m in Ms], exhausted=exhausted)
        save_cache(cache)
    Ms = [frozenset(m) for m in cache[mkey]["sets"]]
    exhausted = cache[mkey]["exhausted"]
    log(f"p={p}: enumerated {len(Ms)} maximum H1 sets (exhausted={exhausted}, cap=100)", flush=True)

    bkey = f"block_stats_{p}"
    if bkey not in cache:
        cache[bkey] = block_stats(sysd, Ms)
        save_cache(cache)
    bs = cache[bkey]
    log(f"p={p}: of {bs['n_M']} maximum H1 sets, {bs['fully_blocked']} are fully-blocked (every q in H2 "
        f"sees >=1 pair) and {bs['extendable']} admit >=1 free q (B(q)=0); "
        f"B(q) pooled: min={bs['min_over_all']} mean-of-means={bs['mean_of_means']:.2f} "
        f"max={bs['max_over_all']}", flush=True)

    # part 4
    hkey = f"holes_{p}"
    holes = analyze_holes(sysd, Ms, ft_results, ts_to_check=(1, 2, 3, 4))
    cache[hkey] = {str(k): v for k, v in holes.items()}
    save_cache(cache)
    for t in sorted(holes):
        d = holes[t]
        log(f"p={p} t={t}: |M\\S1|={d['n_holes']} |S1\\M|={d['n_extra']} sym_diff={d['sym_diff']} "
            f"hole classes(a)={d['hole_classes']} added-H2 classes(a)={d['added_classes']} "
            f"common classes={d['classes_in_common']}", flush=True)


def main(argv: list[str]) -> None:
    primes = [int(a) for a in argv] if argv else [11, 13, 17, 19, 23]
    cache = load_cache()
    for p in primes:
        run_prime(p, cache, log=print)
    print(f"\nAll done. Results cached in {RESULTS_PATH}")


if __name__ == "__main__":
    main(sys.argv[1:])
