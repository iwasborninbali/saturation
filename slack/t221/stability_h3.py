"""stability_h3.py -- numerical test of Hole H3 ("stability of one hyperbola",
docs/research/integrality/holes.py) using the definitions and theorems of paper/hjsw_window.tex
(Theorem thm:main, Corollary cor:slopes, Theorem thm:window).

Question (H3): is a near-maximum lawful subset of ONE hyperbola's lift H(1,p) close (within O(t)) to one of
the 9^s exact maximum sets, when it is short by t points?  This is the missing "almost-extremal" analogue of
the exact classification (thm:main(iii)): 9^s maxima are known, almost-maxima are not.

Setup (matches the task spec / abstract of hjsw_window.tex):
  p odd prime, h = (p-1)//2, box G(p) = [-h, 3h+1] x [0, 2p-1].
  For a in F_p^* the class kappa_a = (a, 1/a): base copy (x_a, y_a), x_a in [-h,h] the centred representative
  of a, y_a in [1,p-1] the representative of 1/a.  Four lifts kappa_a(r,s) = (x_a+r*p, y_a+s*p), r,s in {0,1}.
  H = union over a of the 4 lifts, |H| = 4(p-1), H subset G(p) exactly (HJSW window, c=1).
  S subset H is LAWFUL if no line of the plane meets S in >= 3 points.  Corollary cor:slopes: a rich line
  (>=3 points of H) always has slope 0, infinity, +1 or -1 (rows/columns in fact carry <=2 points of H, so
  are never rich); consequently "lawful" <=> <=2 points of S per row/column/diagonal(+1)/antidiagonal(-1).
  We do NOT take this as given: we verify it (Part 0) by an *independent*, slope-agnostic O(n^2) collinearity
  scan, and we build the ILP/CP-SAT models on the slope-agnostic line list throughout, so correctness never
  depends on the restricted characterization.

  Theorem thm:main: max |S| = 3(p-1); the number of maximum sets is exactly 9^s, s = #{c,-c that are QR}
  in {0,1,2}; for c=1 (always a QR) s = 1 + [-1 is a QR] = 1 + [p = 1 mod 4].  All 9^s maxima agree with the
  HJSW set outside the s "exceptional" V-orbits {kappa_a, kappa_{p-a}} with a^2 = +-1 (mod p); each exceptional
  orbit contributes 2 rich (3-point) lines and a free 3-choose-2 choice on each, i.e. 9 local choices.

Five parts, mirroring the task:
  1. MAX = ALL maximum lawful subsets of H (size 3(p-1)), by exhaustive enumeration with no-good cuts
     (CP-SAT).  Verify |MAX| = 9^s.
  2. D(t) = max over lawful S, |S| = 3(p-1)-t, of  min over M in MAX of |S \\ M|  ("distance to nearest
     maximum"), computed EXACTLY as a single MILP (MAX is finite and small, so max-min collapses to an
     ordinary MILP with one linear constraint per M in MAX and an auxiliary variable z = min_M |S\\M|).
     A randomized local-search lower bound is also computed and reported as a cross-check / fallback.
  3. D(t) vs t, p; the ratio D(t)/t (stability constant) and D(t)/(p-1) (checks "linear in p already at
     t=1", which would refute an O(t) stability theorem).
  4. Structure of the extremal S at t=1,2: per-class point-count histogram (how many classes contribute
     4,3,2,1,0 points of S); distance to every M in MAX (not just the nearest); whether S embeds in some M
     of a different "kind" (exceptional-orbit choice pattern) or is far from all; whether the deviation from
     the nearest M is localized to the exceptional orbit(s) or reaches into the generic (locked) classes.
  5. Bonus: same distance-to-exact-maxima question for H(1) u H(-1) at p=11,13 (exact maxima found by CP-SAT,
     since no closed classification is available for the union; Theorem thm:two only gives an upper bound).

Usage:
  /Users/iwasborninbali/venvs/sat/bin/python3 slack/t221/stability_h3.py             # full run, default primes
  /Users/iwasborninbali/venvs/sat/bin/python3 slack/t221/stability_h3.py 11 13 17    # custom prime list
  /Users/iwasborninbali/venvs/sat/bin/python3 slack/t221/stability_h3.py --no-bonus  # skip part 5
Results are written to slack/t221/stability_h3_results.json.
"""
from __future__ import annotations

import json
import os
import random
import sys
import time
from collections import Counter, defaultdict
from math import gcd

from ortools.sat.python import cp_model

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS_PATH = os.path.join(HERE, "stability_h3_results.json")

DEFAULT_PRIMES = [11, 13, 17, 19, 23, 29, 31]
T_LIST = [1, 2, 3, 4]
BONUS_PRIMES = [11, 13]

# ---------------------------------------------------------------------------
# Part 0: geometry -- the point set H(c,p), and two independent line-builders
# ---------------------------------------------------------------------------


def h_points(p: int, c: int = 1) -> list[tuple[int, int, int, int, int]]:
    """Lifts of xy == c (mod p) in G(p) = [-h,3h+1] x [0,2p-1], as (x,y,a,r,s): a is the class label
    (x_a in [-h,h] the centred representative of a), r,s in {0,1} the lift bits, x = x_a+r*p, y = y_a+s*p,
    y_a = c*a^{-1} mod p in [1,p-1].  |output| = 4(p-1)."""
    h = (p - 1) // 2
    cc = c % p
    pts = []
    for a in range(1, p):
        xa = a if a <= h else a - p
        ya = (cc * pow(a, p - 2, p)) % p
        assert 1 <= ya <= p - 1
        for r in (0, 1):
            for s in (0, 1):
                pts.append((xa + r * p, ya + s * p, a, r, s))
    return pts


def class_type(xa: int, ya: int, h: int) -> str:
    if xa > 0 and ya > h:
        return "A"
    if xa < 0 and ya > h:
        return "B"
    if xa > 0 and ya <= h:
        return "C"
    if xa < 0 and ya <= h:
        return "D"
    raise ValueError((xa, ya, h))


def build_lines_general(coords: list[tuple[int, int]]) -> dict[tuple[int, int, int], frozenset]:
    """ALL maximal collinear subsets (>=3 members) of coords, of ANY slope: O(n^2) pairs, canonical
    (reduced direction, offset) key.  This is the slope-agnostic ground truth for 'lawful'."""
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
    return {k: frozenset(v) for k, v in seen.items() if len(v) >= 3}


def build_lines_restricted(coords: list[tuple[int, int]]) -> dict:
    """Rows, columns, diagonals (slope +1), antidiagonals (slope -1) ONLY -- the characterization the task
    asks us to verify (Corollary cor:slopes)."""
    rows, cols, diag, adiag = (defaultdict(set) for _ in range(4))
    for i, (x, y) in enumerate(coords):
        rows[y].add(i)
        cols[x].add(i)
        diag[x - y].add(i)
        adiag[x + y].add(i)
    groups = list(rows.values()) + list(cols.values()) + list(diag.values()) + list(adiag.values())
    return {i: frozenset(g) for i, g in enumerate(groups) if len(g) >= 3}


def verify_slopes(p: int, c: int = 1) -> dict:
    """Independent check of Corollary cor:slopes: every rich (>=3 point) line of H(c,p) in G(p) has slope
    0, infinity, +1 or -1, AND the family of rich lines found by the fully general O(n^2) scan coincides
    exactly (as a set of point-sets) with the family found by grouping rows/columns/diagonals/antidiagonals."""
    pts = h_points(p, c)
    coords = [(x, y) for x, y, a, r, s in pts]
    assert len(set(coords)) == len(coords), "lifts must be pairwise distinct"
    general = build_lines_general(coords)
    restricted = build_lines_restricted(coords)
    gen_sets = set(general.values())
    res_sets = set(restricted.values())
    slopes_seen = sorted(set((dx, dy) for dx, dy, c0 in general.keys()))
    slopes_ok = all(dx == 0 or dy == 0 or dx == dy or dx == -dy for dx, dy in slopes_seen)
    return dict(p=p, c=c, n=len(coords), n_general_rich=len(general), n_restricted_rich=len(restricted),
                slopes_ok=slopes_ok, same_family=(gen_sets == res_sets), slopes_seen=slopes_seen)


# ---------------------------------------------------------------------------
# quadratic residues, s, exceptional V-orbits
# ---------------------------------------------------------------------------


def is_qr(a: int, p: int) -> bool:
    a %= p
    if a == 0:
        return False
    return pow(a, (p - 1) // 2, p) == 1


def s_value(p: int, c: int) -> int:
    return int(is_qr(c, p)) + int(is_qr((-c) % p, p))


def find_sqrt(val: int, p: int) -> int | None:
    val %= p
    for a in range(1, p):
        if (a * a) % p == val:
            return a
    return None


def exceptional_orbits(p: int, c: int = 1) -> list[tuple[str, frozenset]]:
    """[(name, {a0, p-a0})] for each exceptional V-orbit: 'tau' (a0^2=c, always present for c=1 since 1 is
    always a QR) and 'sigma' (a0^2=-c, present iff -c is a QR)."""
    out = []
    a0 = find_sqrt(c % p, p)
    if a0 is not None:
        out.append(("tau", frozenset({a0, (p - a0) % p})))
    a1 = find_sqrt((-c) % p, p)
    if a1 is not None:
        out.append(("sigma", frozenset({a1, (p - a1) % p})))
    return out


# ---------------------------------------------------------------------------
# Part 1: CP-SAT models -- max value, exhaustive enumeration by no-good cuts, D(t)
# ---------------------------------------------------------------------------


def make_model(n: int, line_groups, size_eq: int | None = None):
    model = cp_model.CpModel()
    x = [model.NewBoolVar(f"x{i}") for i in range(n)]
    for mem in line_groups:
        model.Add(sum(x[i] for i in mem) <= 2)
    if size_eq is not None:
        model.Add(sum(x) == size_eq)
    return model, x


def solve_max_value(n: int, line_groups, time_limit: float = 20.0) -> dict:
    model, x = make_model(n, line_groups)
    model.Maximize(sum(x))
    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = 8
    solver.parameters.max_time_in_seconds = time_limit
    status = solver.Solve(model)
    return dict(status=solver.StatusName(status), value=int(round(solver.ObjectiveValue())),
                bound=solver.BestObjectiveBound(), wall=solver.WallTime())


def add_nogood(model: cp_model.CpModel, x, sol: frozenset, n: int) -> None:
    terms = [(x[i].Not() if i in sol else x[i]) for i in range(n)]
    model.Add(sum(terms) >= 1)


def enumerate_all_max_nogood(n: int, line_groups, target: int, cap: int = 300,
                              time_limit_each: float = 20.0) -> tuple[list[frozenset], bool]:
    """Exhaustive enumeration of ALL lawful subsets of size `target` by CP-SAT + explicit no-good cuts:
    solve, record the optimum, forbid the exact same 0/1 assignment, resolve, until INFEASIBLE (exhausted)
    or `cap` reached."""
    model, x = make_model(n, line_groups, size_eq=target)
    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = 8
    solver.parameters.max_time_in_seconds = time_limit_each
    solutions: list[frozenset] = []
    exhausted = False
    while len(solutions) < cap:
        status = solver.Solve(model)
        if status == cp_model.INFEASIBLE:
            exhausted = True
            break
        if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            break
        sol = frozenset(i for i in range(n) if solver.Value(x[i]) == 1)
        solutions.append(sol)
        add_nogood(model, x, sol, n)
    return solutions, exhausted


class _Collector(cp_model.CpSolverSolutionCallback):
    def __init__(self, x, cap):
        super().__init__()
        self.x = x
        self.cap = cap
        self.sols: list[frozenset] = []

    def on_solution_callback(self):
        self.sols.append(frozenset(i for i, v in enumerate(self.x) if self.Value(v) == 1))
        if len(self.sols) >= self.cap:
            self.StopSearch()


def enumerate_all_max_builtin(n: int, line_groups, target: int, cap: int = 300,
                               time_limit: float = 60.0) -> tuple[list[frozenset], bool]:
    """Cross-check: CP-SAT's built-in exhaustive-search mode (enumerate_all_solutions), independent code
    path from the no-good-cut loop above."""
    model, x = make_model(n, line_groups, size_eq=target)
    solver = cp_model.CpSolver()
    solver.parameters.enumerate_all_solutions = True
    solver.parameters.num_search_workers = 1
    solver.parameters.max_time_in_seconds = time_limit
    cb = _Collector(x, cap)
    status = solver.Solve(model, cb)
    exhausted = status == cp_model.OPTIMAL and len(cb.sols) < cap
    return cb.sols, exhausted


def solve_D(n: int, line_groups, Ms: list[frozenset], target: int, time_limit: float = 60.0) -> dict:
    """D = max over lawful S, |S|=target, of min_{M in Ms} |S \\ M|, as ONE MILP: z <= target - sum_{i in M}
    x_i for every M in Ms (this equals |S\\M| given sum(x)=target), maximize z."""
    model, x = make_model(n, line_groups, size_eq=target)
    z = model.NewIntVar(0, target, "z")
    for M in Ms:
        model.Add(z <= target - sum(x[i] for i in M))
    model.Maximize(z)
    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = 8
    solver.parameters.max_time_in_seconds = time_limit
    status = solver.Solve(model)
    ok = status in (cp_model.OPTIMAL, cp_model.FEASIBLE)
    witness = frozenset(i for i in range(n) if solver.Value(x[i]) == 1) if ok else None
    return dict(status=solver.StatusName(status), optimal=(status == cp_model.OPTIMAL),
                D=(int(round(solver.ObjectiveValue())) if ok else None),
                bound=solver.BestObjectiveBound(), witness=(sorted(witness) if witness else None),
                wall=solver.WallTime())


# ---------------------------------------------------------------------------
# Part 2 (fallback): randomized local search for a LOWER bound on D(t)
# ---------------------------------------------------------------------------


def local_search_D(n: int, line_groups, Ms: list[frozenset], target: int, restarts: int = 40,
                    moves: int = 400, seed: int = 0) -> dict:
    """Multi-start hill-climbing lower bound for D(t).  Each restart begins from a random M in Ms with
    (|M|-target) random points deleted (guaranteed lawful, guaranteed the right size); then repeatedly
    tries random single-point swaps that keep the set lawful, accepting the best of a sample of candidate
    swaps if it does not decrease the objective min_M |S\\M| (occasionally accepting a strictly worse move,
    simulated-annealing style, to escape plateaus)."""
    rng = random.Random(seed)
    lines = list(line_groups)
    at = [[] for _ in range(n)]
    for li, mem in enumerate(lines):
        for i in mem:
            at[i].append(li)
    Ms_list = list(Ms)

    def objective(S: set) -> int:
        return min(len(S - M) for M in Ms_list)

    def can_add(S: set, cur: list, j: int) -> bool:
        return all(cur[li] < 2 for li in at[j])

    best_val = -1
    best_S: set | None = None
    for r in range(restarts):
        M0 = rng.choice(Ms_list)
        S = set(M0)
        drop = len(M0) - target
        if drop > 0:
            S -= set(rng.sample(sorted(M0), drop))
        elif drop < 0:
            continue  # shouldn't happen (all M have the same size)
        cur = [0] * len(lines)
        for i in S:
            for li in at[i]:
                cur[li] += 1
        val = objective(S)
        T0 = 2.0
        for step in range(moves):
            T = T0 * (1 - step / moves)
            i = rng.choice(sorted(S))
            S.discard(i)  # tentatively remove i -- MUST stay in sync with cur, or candidate checks / the
            # objective become inconsistent (this was a real bug: i used to stay in S while cur pretended
            # it was gone, letting "swaps" silently grow |S| past target and violate lawfulness)
            for li in at[i]:
                cur[li] -= 1
            candidates = [j for j in rng.sample(range(n), min(n, 40)) if j not in S and j != i and can_add(S, cur, j)]
            if not candidates:
                S.add(i)
                for li in at[i]:
                    cur[li] += 1
                continue
            best_j, best_j_val = None, -1
            for j in candidates:
                S.add(j)
                v = objective(S)
                S.discard(j)
                if v > best_j_val:
                    best_j_val, best_j = v, j
            accept = best_j_val >= val or rng.random() < 0.05 * T
            if accept:
                S.add(best_j)
                for li in at[best_j]:
                    cur[li] += 1
                val = best_j_val
            else:
                S.add(i)
                for li in at[i]:
                    cur[li] += 1
        if val > best_val:
            best_val, best_S = val, set(S)
    return dict(D_lower=best_val, witness=sorted(best_S) if best_S else None)


# ---------------------------------------------------------------------------
# Part 4: structure of the extremal S
# ---------------------------------------------------------------------------


def class_counts(pts, S) -> tuple[dict, Counter]:
    counts: dict[int, int] = defaultdict(int)
    for i in S:
        counts[pts[i][2]] += 1
    all_a = sorted(set(p2[2] for p2 in pts))
    full = {a: counts.get(a, 0) for a in all_a}
    hist = Counter(full.values())
    return full, hist


def describe(pts, idxs) -> list[tuple[int, int, int]]:
    return sorted((pts[i][2], pts[i][3], pts[i][4]) for i in idxs)


def structure_report(pts, S: frozenset, Ms: list[frozenset], exc_orbit_idx, target: int) -> dict:
    full, hist = class_counts(pts, S)
    dists = [len(S - M) for M in Ms]
    dmin = min(dists)
    nearest_idxs = [k for k, d in enumerate(dists) if d == dmin]
    Mstar = Ms[nearest_idxs[0]]
    holes = sorted(Mstar - S)
    extra = sorted(S - Mstar)
    exc_all = frozenset().union(*[idx for _, idx in exc_orbit_idx]) if exc_orbit_idx else frozenset()
    holes_in_exc = [i for i in holes if i in exc_all]
    holes_generic = [i for i in holes if i not in exc_all]
    extra_in_exc = [i for i in extra if i in exc_all]
    extra_generic = [i for i in extra if i not in exc_all]
    n_embeds = sum(1 for d in dists if d == 0)
    return dict(
        target=target, n_classes_by_count={str(k): v for k, v in sorted(hist.items())},
        dist_to_all_M=dists, dmin=dmin, n_M_at_dmin=len(nearest_idxs), n_M_embedding_S_exactly=n_embeds,
        holes_vs_nearest=describe(pts, holes), extra_vs_nearest=describe(pts, extra),
        holes_in_exceptional=len(holes_in_exc), holes_in_generic=len(holes_generic),
        extra_in_exceptional=len(extra_in_exc), extra_in_generic=len(extra_generic),
        sym_diff_to_nearest=len(holes) + len(extra),
    )


def max_signature(pts, M: frozenset, exc_orbit_idx) -> tuple:
    return tuple(frozenset(M & idx) for _, idx in exc_orbit_idx)


# ---------------------------------------------------------------------------
# driver
# ---------------------------------------------------------------------------


def analyze_prime(p: int, c: int = 1, log=print) -> dict:
    t0 = time.time()
    out: dict = dict(p=p, c=c)
    pts = h_points(p, c)
    coords = [(x, y) for x, y, a, r, s in pts]
    n = len(pts)
    h = (p - 1) // 2
    # pts is laid out a=1..p-1 outer, (r,s) in (0,0),(0,1),(1,0),(1,1) inner, so index 4*(a-1) is the
    # (r=0,s=0) lift, i.e. the base copy (x_a, y_a) itself.
    types = [class_type(pts[i][0], pts[i][1], h) for i in range(0, n, 4)]
    tcount = Counter(types)
    log(f"p={p}: |H|={n}  type counts A/B/C/D = {tcount['A']}/{tcount['B']}/{tcount['C']}/{tcount['D']} "
        f"(n_A=n_D? {tcount['A'] == tcount['D']}, n_B=n_C? {tcount['B'] == tcount['C']})", flush=True)

    # Part 0: slope verification (independent of everything below; the ILP always uses build_lines_general)
    sv = verify_slopes(p, c)
    out["slope_check"] = sv
    log(f"p={p}: slope check -- rich lines general={sv['n_general_rich']} restricted={sv['n_restricted_rich']} "
        f"slopes_seen={sv['slopes_seen']} all in {{0,inf,+1,-1}}? {sv['slopes_ok']}  "
        f"general-family == restricted-family? {sv['same_family']}", flush=True)

    line_groups = list(build_lines_general(coords).values())
    target0 = 3 * (p - 1)
    s = s_value(p, c)
    out["s"] = s
    out["theory_9s"] = 9 ** s

    mx = solve_max_value(n, line_groups, time_limit=30.0)
    out["max_value"] = mx
    log(f"p={p}: exact max lawful subset = {mx['value']} (theorem 3(p-1)={target0}) status={mx['status']} "
        f"{'OK' if mx['value'] == target0 else 'MISMATCH!!'}", flush=True)

    # Part 1: enumerate ALL maxima
    Ms, exhausted = enumerate_all_max_nogood(n, line_groups, target0, cap=300, time_limit_each=30.0)
    out["MAX_count"] = len(Ms)
    out["MAX_exhausted"] = exhausted
    log(f"p={p}: |MAX| (no-good-cut enumeration) = {len(Ms)}  exhausted={exhausted}  "
        f"9^s = {9 ** s}  match? {len(Ms) == 9 ** s}", flush=True)

    if p <= 19:  # cross-check with CP-SAT's builtin exhaustive mode for the smaller, cheaper primes
        Ms2, exhausted2 = enumerate_all_max_builtin(n, line_groups, target0, cap=300, time_limit=60.0)
        same = set(Ms) == set(Ms2)
        out["MAX_crosscheck"] = dict(count=len(Ms2), exhausted=exhausted2, identical_set=same)
        log(f"p={p}: cross-check (builtin enumerate_all_solutions) count={len(Ms2)} exhausted={exhausted2} "
            f"identical solution SET to no-good-cut run? {same}", flush=True)

    # exceptional orbits / "kind" signatures, and the "agrees outside exceptional orbits" check
    orbits = exceptional_orbits(p, c)
    exc_orbit_idx = [(name, frozenset(i for i in range(n) if pts[i][2] in labels)) for name, labels in orbits]
    exc_all = frozenset().union(*[idx for _, idx in exc_orbit_idx]) if exc_orbit_idx else frozenset()
    generic_agree = len({frozenset(M - exc_all) for M in Ms}) == 1 if Ms else None
    sigs = {max_signature(pts, M, exc_orbit_idx) for M in Ms}
    out["orbits"] = [(name, sorted(idx)) for name, idx in exc_orbit_idx]
    out["generic_part_agrees_across_all_M"] = generic_agree
    out["n_distinct_signatures"] = len(sigs)
    log(f"p={p}: exceptional orbits={[name for name,_ in orbits]}  all M agree outside them? {generic_agree}  "
        f"distinct exceptional-orbit signatures = {len(sigs)} (should equal |MAX|={len(Ms)})", flush=True)

    # Part 2-3: D(t)
    out["D"] = {}
    for t in T_LIST:
        target = target0 - t
        r = solve_D(n, line_groups, Ms, target, time_limit=60.0)
        ls = None
        if not r["optimal"]:
            ls = local_search_D(n, line_groups, Ms, target, restarts=40, moves=400, seed=p * 100 + t)
            log(f"p={p} t={t}: MILP NOT proven optimal (status={r['status']}, D<={r['D']}, "
                f"bound<={r['bound']}); local-search LOWER BOUND D>={ls['D_lower']}", flush=True)
        else:
            log(f"p={p} t={t}: D(t)={r['D']} (exact, proven optimal)  D(t)/t={r['D']/t:.3f}  "
                f"D(t)/(p-1)={r['D']/(p-1):.4f}  wall={r['wall']:.2f}s", flush=True)
        out["D"][str(t)] = dict(milp=r, local_search=ls)

        # Part 4: structure, for t=1,2
        if t in (1, 2) and r["witness"] is not None:
            S = frozenset(r["witness"])
            st = structure_report(pts, S, Ms, exc_orbit_idx, target)
            out["D"][str(t)]["structure"] = st
            log(f"p={p} t={t}: class-count histogram (#classes with k points of S) = {st['n_classes_by_count']}  "
                f"dmin={st['dmin']} achieved by {st['n_M_at_dmin']}/{len(Ms)} maxima; "
                f"S subset of some M exactly? {'yes,'+str(st['n_M_embedding_S_exactly'])+' of them' if st['n_M_embedding_S_exactly'] else 'no'}  "
                f"holes(vs nearest M): {st['holes_in_exceptional']} in exceptional orbit(s), "
                f"{st['holes_in_generic']} in generic classes; "
                f"extra(vs nearest M): {st['extra_in_exceptional']} exceptional, {st['extra_in_generic']} generic",
                flush=True)

    out["wall_seconds"] = time.time() - t0
    log(f"p={p}: done in {out['wall_seconds']:.1f}s", flush=True)
    return out


# ---------------------------------------------------------------------------
# Bonus (Part 5): H(1) u H(-1)
# ---------------------------------------------------------------------------


def analyze_union(p: int, log=print) -> dict:
    t0 = time.time()
    pts1 = h_points(p, 1)
    pts2 = h_points(p, -1)
    pts = pts1 + [(x, y, a, r, s) for x, y, a, r, s in pts2]  # keep as-is; disjoint from pts1 (see below)
    coords = [(x, y) for x, y, a, r, s in pts]
    assert len(set(coords)) == len(coords), "H(1) and H(-1) lifts must be pairwise distinct"
    n = len(pts)
    n1 = len(pts1)
    line_groups = list(build_lines_general(coords).values())
    log(f"p={p} UNION: |H1|=|H2|={n1}  n={n}  rich lines={len(line_groups)}", flush=True)

    mx = solve_max_value(n, line_groups, time_limit=60.0)
    log(f"p={p} UNION: exact alpha = {mx['value']} status={mx['status']} bound<={mx['bound']}", flush=True)

    Ms, exhausted = enumerate_all_max_nogood(n, line_groups, mx["value"], cap=400, time_limit_each=30.0)
    log(f"p={p} UNION: |MAX_union| = {len(Ms)}  exhausted={exhausted} (cap=400)", flush=True)

    out = dict(p=p, n=n, n1=n1, alpha=mx, MAX_count=len(Ms), MAX_exhausted=exhausted, D={})
    for t in (1, 2):
        target = mx["value"] - t
        r = solve_D(n, line_groups, Ms, target, time_limit=90.0)
        if r["optimal"]:
            log(f"p={p} UNION t={t}: D(t)={r['D']} (exact)  D(t)/t={r['D']/t:.3f}", flush=True)
        else:
            log(f"p={p} UNION t={t}: MILP status={r['status']} D<={r['D']} bound<={r['bound']}", flush=True)
        out["D"][str(t)] = r
    out["wall_seconds"] = time.time() - t0
    return out


# ---------------------------------------------------------------------------


def main(argv: list[str]) -> None:
    args = [a for a in argv if not a.startswith("--")]
    no_bonus = "--no-bonus" in argv
    primes = [int(a) for a in args] if args else DEFAULT_PRIMES

    results: dict = dict(primes=primes, main={}, bonus={})
    for p in primes:
        print(f"\n=== p={p} ===", flush=True)
        results["main"][str(p)] = analyze_prime(p, c=1, log=print)
        with open(RESULTS_PATH, "w") as fh:
            json.dump(results, fh, indent=1, default=str)

    if not no_bonus:
        for p in BONUS_PRIMES:
            print(f"\n=== UNION p={p} ===", flush=True)
            results["bonus"][str(p)] = analyze_union(p, log=print)
            with open(RESULTS_PATH, "w") as fh:
                json.dump(results, fh, indent=1, default=str)

    with open(RESULTS_PATH, "w") as fh:
        json.dump(results, fh, indent=1, default=str)
    print(f"\nAll done. Results written to {RESULTS_PATH}")


if __name__ == "__main__":
    main(sys.argv[1:])
