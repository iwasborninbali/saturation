#!/usr/bin/env python3
"""Куб [n]^3 без трёх коллинеарных (OEIS A399138): точный максимум ВНУТРИ каждой симметричной страты.
Страта = конфигурации, инвариантные под подгруппой H группы симметрий куба O_h (порядок 48).
Переменные — орбиты клеток под H; ограничение: на каждой решёточной прямой ≤ 2 точек; максимизируем число точек.
CP-SAT (OR-Tools). Каждый найденный свидетель ПЕРЕПРОВЕРЯЕТСЯ полным перебором троек (целые векторные произведения).
usage: cube_strata.py n [--time SEC] [--procs P] [--workers W] [--orders 2,3,4,6,8,12,16,24,48] [--out dir]
"""
import sys, os, json, time, argparse, itertools, collections
from multiprocessing import Pool

# ---------- группа O_h как знаковые перестановочные матрицы 3x3 (кортежи из 9 int) ----------
def all_matrices():
    mats = []
    for perm in itertools.permutations(range(3)):
        for signs in itertools.product((1, -1), repeat=3):
            M = [[0] * 3 for _ in range(3)]
            for i in range(3): M[i][perm[i]] = signs[i]
            mats.append(tuple(M[0] + M[1] + M[2]))
    return mats

def mul(A, B):
    return tuple(sum(A[3 * i + k] * B[3 * k + j] for k in range(3)) for i in range(3) for j in range(3))

def inv(A):  # транспонирование: матрицы ортогональные
    return tuple(A[3 * j + i] for i in range(3) for j in range(3))

IDENT = (1, 0, 0, 0, 1, 0, 0, 0, 1)

def closure(gens):
    S = {IDENT}; frontier = [IDENT]
    while frontier:
        new = []
        for a in frontier:
            for g in gens:
                b = mul(a, g)
                if b not in S: S.add(b); new.append(b)
        frontier = new
    return frozenset(S)

def subgroup_classes(G):
    """все подгруппы, порождённые ≤ 2 элементами, по одной на класс сопряжённости"""
    subs = set()
    Gl = sorted(G)
    for a in Gl:
        subs.add(closure([a]))
    singles = list(subs)
    for i, a in enumerate(Gl):
        for b in Gl[i + 1:]:
            subs.add(closure([a, b]))
    # соединения пар найденных подгрупп (доборка порядков 12–24)
    base = list(subs)
    for i in range(len(base)):
        for j in range(i + 1, len(base)):
            if len(base[i]) * len(base[j]) <= 48 * 4:
                subs.add(closure(list(base[i] | base[j])))
    classes = {}
    for S in subs:
        key = min(tuple(sorted(frozenset(mul(mul(g, h), inv(g)) for h in S))) for g in Gl)
        classes.setdefault(key, S)
    return sorted(classes.values(), key=lambda S: (len(S), sorted(S)))

def describe(S):
    """краткое описание подгруппы: порядок, число вращений, есть ли инверсия"""
    det = lambda M: (M[0] * (M[4] * M[8] - M[5] * M[7]) - M[1] * (M[3] * M[8] - M[5] * M[6]) + M[2] * (M[3] * M[7] - M[4] * M[6]))
    rot = sum(1 for M in S if det(M) == 1)
    invn = (-1, 0, 0, 0, -1, 0, 0, 0, -1) in S
    return f"|H|={len(S)} rot={rot} inv={'y' if invn else 'n'}"

# ---------- клетки, орбиты, прямые ----------
def act(M, cell, n):
    m = n - 1
    c = (2 * cell[0] - m, 2 * cell[1] - m, 2 * cell[2] - m)
    d = tuple(sum(M[3 * i + k] * c[k] for k in range(3)) for i in range(3))
    return tuple((d[i] + m) // 2 for i in range(3))

def orbits(S, n):
    cells = [(x, y, z) for x in range(n) for y in range(n) for z in range(n)]
    idx = {c: i for i, c in enumerate(cells)}
    orb_of = [-1] * len(cells); orbs = []
    for c in cells:
        if orb_of[idx[c]] >= 0: continue
        o = sorted({act(M, c, n) for M in S}); k = len(orbs); orbs.append(o)
        for d in o: orb_of[idx[d]] = k
    return cells, idx, orb_of, orbs

def lines(n, cells, idx):
    """все решёточные прямые с ≥ 3 клетками, каждая один раз (по минимальной клетке)"""
    out = []; seen = set()
    from math import gcd
    dirs = set()
    r = (n - 1) // 2
    for a in range(-r, r + 1):
        for b in range(-r, r + 1):
            for c in range(-r, r + 1):
                if (a, b, c) == (0, 0, 0): continue
                g = gcd(gcd(abs(a), abs(b)), abs(c))
                d = (a // g, b // g, c // g)
                if d < (0, 0, 0) or (d[0] == 0 and (d[1] < 0 or (d[1] == 0 and d[2] < 0))): d = tuple(-t for t in d)
                dirs.add(d)
    for p in cells:
        for d in dirs:
            q = (p[0] - d[0], p[1] - d[1], p[2] - d[2])
            if q in idx: continue                      # p не первая на прямой
            L = []; x = p
            while x in idx: L.append(idx[x]); x = (x[0] + d[0], x[1] + d[1], x[2] + d[2])
            if len(L) >= 3: out.append(L)
    return out

def verify(points):
    pts = sorted(points); m = len(pts)
    for i in range(m):
        xi, yi, zi = pts[i]
        for j in range(i + 1, m):
            ax, ay, az = pts[j][0] - xi, pts[j][1] - yi, pts[j][2] - zi
            for k in range(j + 1, m):
                bx, by, bz = pts[k][0] - xi, pts[k][1] - yi, pts[k][2] - zi
                if ay * bz - az * by == 0 and az * bx - ax * bz == 0 and ax * by - ay * bx == 0:
                    return False
    return True

# ---------- одна страта ----------
def solve_stratum(args):
    n, S, tag, tlimit, workers, outdir = args
    from ortools.sat.python import cp_model
    cells, idx, orb_of, orbs = orbits(S, n)
    L = lines(n, cells, idx)
    model = cp_model.CpModel()
    v = [model.NewBoolVar(f"o{k}") for k in range(len(orbs))]
    cons = set()
    for line in L:
        mult = collections.Counter(orb_of[i] for i in line)
        key = tuple(sorted(mult.items()))
        if key in cons: continue
        cons.add(key)
        if any(c >= 3 for c in mult.values()):
            for k, c in mult.items():
                if c >= 3: model.Add(v[k] == 0)
            rest = [(k, c) for k, c in mult.items() if c < 3]
            if rest: model.Add(sum(c * v[k] for k, c in rest) <= 2)
        else:
            model.Add(sum(c * v[k] for k, c in mult.items()) <= 2)
    model.Maximize(sum(len(orbs[k]) * v[k] for k in range(len(orbs))))
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = tlimit
    solver.parameters.num_search_workers = workers
    t0 = time.time(); st = solver.Solve(model); dt = time.time() - t0
    status = solver.StatusName(st)
    best = int(solver.ObjectiveValue()) if st in (cp_model.OPTIMAL, cp_model.FEASIBLE) else 0
    bound = int(solver.BestObjectiveBound()) if st in (cp_model.OPTIMAL, cp_model.FEASIBLE) else None
    pts = []
    if best:
        pts = [cells[i] for k in range(len(orbs)) if solver.Value(v[k]) for i in [idx[c] for c in orbs[k]]]
        ok = verify(pts) and len(pts) == best
        if not ok: status += "_VERIFY_FAILED"
        with open(os.path.join(outdir, f"n{n}_{tag}_{best}.txt"), "w") as f:
            f.write(f"# A399138 n={n} stratum {tag} ({describe(S)}) points={best} status={status} bound={bound} verified={ok}\n")
            for p in sorted(pts): f.write(f"{p[0]} {p[1]} {p[2]}\n")
    return dict(n=n, tag=tag, group=describe(S), orbits=len(orbs), constraints=len(cons), status=status,
                best=best, bound=bound, secs=round(dt, 1))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("n", type=int); ap.add_argument("--time", type=float, default=600)
    ap.add_argument("--procs", type=int, default=8); ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--orders", default="2,3,4,6,8,12,16,24,48"); ap.add_argument("--out", default="strata")
    ap.add_argument("--trivial", type=float, default=0, help="секунд на страту без симметрии (0 = не запускать)")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    G = all_matrices(); assert len(G) == 48
    classes = subgroup_classes(frozenset(G))
    orders = {int(t) for t in a.orders.split(",")}
    jobs = []
    for i, S in enumerate(classes):
        if len(S) in orders: jobs.append((a.n, S, f"c{i:02d}_ord{len(S)}", a.time, a.workers, a.out))
        if len(S) == 1 and a.trivial > 0: jobs.append((a.n, S, f"c{i:02d}_ord1", a.trivial, a.workers, a.out))
    print(f"n={a.n}: классов подгрупп {len(classes)}, запускаем {len(jobs)} страт; порядки {sorted(collections.Counter(len(j[1]) for j in jobs).items())}", flush=True)
    results = []
    with Pool(a.procs) as pool:
        for r in pool.imap_unordered(solve_stratum, jobs):
            results.append(r)
            print(f"  {r['tag']:>12} {r['group']:>22} orbits={r['orbits']:4d} cons={r['constraints']:6d} -> best={r['best']:3d} bound={r['bound']} {r['status']} {r['secs']}s", flush=True)
            json.dump(sorted(results, key=lambda r: -r['best']), open(os.path.join(a.out, f"n{a.n}_results.json"), "w"), indent=1)
    best = max(results, key=lambda r: r['best'])
    print(f"ИТОГ n={a.n}: лучший свидетель {best['best']} точек в страте {best['tag']} ({best['group']}), статус {best['status']}", flush=True)

if __name__ == "__main__":
    main()
