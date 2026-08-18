"""cpsat_max.py — exact maximum lawful subset of a candidate set with CP-SAT (OR-tools), witnesses through the law.
Third independent exact engine (after kissat/CaDiCaL cardinality encodings and HiGHS MIP).
usage: cpsat_max.py M p N k1,k2,...  [workers] [seconds]      union of hyperbolas xy≡k_i (mod p), HJSW x-shift, window N×N
       cpsat_max.py R p N k1,k2,...  [workers] [seconds]      same, RESTRICTED: no class uses both copies of a diagonal
                                                            or antidiagonal pair (only vertical/horizontal pairs and singles)
       cpsat_max.py U p q N        [workers] [seconds]      xy≡1 mod p ∪ xy≡1 mod q (each with its own HJSW x-shift), N×N
       cpsat_max.py PH p k N       [workers] [seconds]      parabola y=x²+k ∪ hyperbola xy≡1 (mod p)
       cpsat_max.py file cands.txt [workers] [seconds]
Prints the optimum (or best/bound at timeout) and the witness (grid coordinates), verified with saturation.the_law."""
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import saturation as S
from maxlawful_pysat import cands_M, cands_U, cands_PH, lines
from ortools.sat.python import cp_model


def class_pairs(cands, p, h):
    """for the M-type candidate sets: group the four copies of each residue class; return list of (diag_pair, antidiag_pair)
    index pairs: ((i00,i11),(i01,i10)) — the copies (0,0)&(1,1) lie on a slope +1 line, (0,1)&(1,0) on a slope -1 line."""
    idx = {c: i for i, c in enumerate(cands)}
    byclass = {}
    for (a, b) in cands:
        X, Y = a - h, b
        byclass.setdefault((X % p, Y % p), []).append((X, Y))
    out = []
    for key, pts in byclass.items():
        if len(pts) != 4: continue
        X0 = min(X for X, Y in pts); Y0 = min(Y for X, Y in pts)
        cp = {((X - X0) // p, (Y - Y0) // p): idx[(X + h, Y)] for X, Y in pts}
        if set(cp) == {(0, 0), (0, 1), (1, 0), (1, 1)}:
            out.append(((cp[(0, 0)], cp[(1, 1)]), (cp[(0, 1)], cp[(1, 0)])))
    return out


def solve(cands, N, workers=8, secs=3600.0, lb=None, log=False, restrict=None):
    L = lines(cands); n = len(cands)
    m = cp_model.CpModel()
    x = [m.NewBoolVar(f"x{i}") for i in range(n)]
    for mem in L:
        m.Add(sum(x[i] for i in mem) <= 2)
    if restrict:                      # restricted model: no diagonal / antidiagonal copy pairs within a class
        for (d, e) in restrict:
            m.Add(x[d[0]] + x[d[1]] <= 1); m.Add(x[e[0]] + x[e[1]] <= 1)
    if lb is not None: m.Add(sum(x) >= lb)
    m.Maximize(sum(x))
    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = workers
    solver.parameters.max_time_in_seconds = secs
    solver.parameters.log_search_progress = log
    t = time.time(); st = solver.Solve(m); dt = time.time() - t
    status = solver.StatusName(st)
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        pts = sorted(cands[i] for i in range(n) if solver.Value(x[i]))
        S.the_law(frozenset(a * N + b for (a, b) in pts), N)          # verified by the law
        return status, len(pts), solver.BestObjectiveBound(), dt, pts
    return status, None, solver.BestObjectiveBound(), dt, None


if __name__ == "__main__":
    a = sys.argv[1:]
    restrict = None
    if a[0] in ("M", "R"):
        p, N = int(a[1]), int(a[2]); ks = {int(k) % p for k in a[3].split(",")}; cands = cands_M(p, ks, N); rest = a[4:]
        tag = f"{a[0]} p={p} ks={sorted(ks)} N={N}"
        if a[0] == "R": restrict = class_pairs(cands, p, (p - 1) // 2); tag += f" restricted(classes={len(restrict)})"
    elif a[0] == "U":
        p, q, N = int(a[1]), int(a[2]), int(a[3]); cands = cands_U(p, q, N); rest = a[4:]; tag = f"U p={p} q={q} N={N}"
    elif a[0] == "PH":
        p, k, N = int(a[1]), int(a[2]), int(a[3]); cands = cands_PH(p, k, N); rest = a[4:]; tag = f"PH p={p} k={k} N={N}"
    else:
        cands = [tuple(map(int, l.split()[:2])) for l in open(a[1]) if l.strip()]; N = max(max(c) for c in cands) + 1
        rest = a[2:]; tag = f"file {a[1]} N={N}"
    workers = int(rest[0]) if rest else 8; secs = float(rest[1]) if len(rest) > 1 else 3600.0
    print(f"{tag}: candidates={len(cands)} lines>=3={len(lines(cands))} workers={workers} limit={secs}s", flush=True)
    status, val, bound, dt, pts = solve(cands, N, workers, secs, restrict=restrict)
    print(f"RESULT {tag}: status={status} value={val} bound={bound:.0f} time={dt:.1f}s ratio={(val or 0)/N:.3f}", flush=True)
    if pts: print("witness (lawful):", " ".join(f"{x},{y}" for x, y in pts), flush=True)
