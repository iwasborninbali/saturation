#!/usr/bin/env python3
"""A280537 — куб [n]^3 без ЧЕТЫРЁХ компланарных точек: максимум внутри каждой страты симметрии (подгруппы O_h).
Модель CP-SAT по орбитам клеток; ограничения: ≤ 2 на прямой (три коллинеарные + любая четвёртая компланарны), ≤ 3 на каждой
решёточной плоскости с ≥ 4 клетками. Плоскости добавляются ЛЕНИВО: сначала все с малой нормалью (|a|,|b|,|c| ≤ K), затем —
найденные точным перебором четвёрок в решении (определители); цикл до чистого решения или до лимита. Лучший ЧИСТЫЙ свидетель
записывается в файл и перепроверяется полным перебором четвёрок.
usage: cube_strata_planes.py n [--time SEC] [--procs P] [--workers W] [--orders 2,3,4,6,8,12,16,24,48] [--out dir] [--K 3] [--trivial SEC]"""
import sys, os, json, time, argparse, itertools, collections
from math import gcd
from multiprocessing import Pool

def all_matrices():
    mats = []
    for perm in itertools.permutations(range(3)):
        for signs in itertools.product((1, -1), repeat=3):
            M = [[0] * 3 for _ in range(3)]
            for i in range(3): M[i][perm[i]] = signs[i]
            mats.append(tuple(M[0] + M[1] + M[2]))
    return mats
def mul(A, B): return tuple(sum(A[3*i+k]*B[3*k+j] for k in range(3)) for i in range(3) for j in range(3))
def inv(A): return tuple(A[3*j+i] for i in range(3) for j in range(3))
IDENT = (1,0,0,0,1,0,0,0,1)
def closure(gens):
    S = {IDENT}; fr = [IDENT]
    while fr:
        new = []
        for a in fr:
            for g in gens:
                b = mul(a, g)
                if b not in S: S.add(b); new.append(b)
        fr = new
    return frozenset(S)
def subgroup_classes(G):
    subs = set(); Gl = sorted(G)
    for a in Gl: subs.add(closure([a]))
    for i, a in enumerate(Gl):
        for b in Gl[i+1:]: subs.add(closure([a, b]))
    base = list(subs)
    for i in range(len(base)):
        for j in range(i+1, len(base)):
            if len(base[i]) * len(base[j]) <= 192: subs.add(closure(list(base[i] | base[j])))
    classes = {}
    for S in subs:
        key = min(tuple(sorted(frozenset(mul(mul(g, h), inv(g)) for h in S))) for g in Gl)
        classes.setdefault(key, S)
    return sorted(classes.values(), key=lambda S: (len(S), sorted(S)))
def describe(S):
    det = lambda M: (M[0]*(M[4]*M[8]-M[5]*M[7]) - M[1]*(M[3]*M[8]-M[5]*M[6]) + M[2]*(M[3]*M[7]-M[4]*M[6]))
    return f"|H|={len(S)} rot={sum(1 for M in S if det(M)==1)} inv={'y' if (-1,0,0,0,-1,0,0,0,-1) in S else 'n'}"
def act(M, cell, n):
    m = n - 1; c = (2*cell[0]-m, 2*cell[1]-m, 2*cell[2]-m)
    d = tuple(sum(M[3*i+k]*c[k] for k in range(3)) for i in range(3))
    return tuple((d[i]+m)//2 for i in range(3))
def orbits(S, n):
    cells = [(x,y,z) for x in range(n) for y in range(n) for z in range(n)]
    idx = {c: i for i, c in enumerate(cells)}; orb_of = [-1]*len(cells); orbs = []
    for c in cells:
        if orb_of[idx[c]] >= 0: continue
        o = sorted({act(M, c, n) for M in S}); k = len(orbs); orbs.append(o)
        for d in o: orb_of[idx[d]] = k
    return cells, idx, orb_of, orbs

def lines(n, cells, idx):
    out = []; dirs = set(); r = (n-1)//2
    for a in range(-r, r+1):
        for b in range(-r, r+1):
            for c in range(-r, r+1):
                if (a,b,c) == (0,0,0): continue
                g = gcd(gcd(abs(a),abs(b)),abs(c)); d = (a//g, b//g, c//g)
                if d < (0,0,0) or (d[0]==0 and (d[1]<0 or (d[1]==0 and d[2]<0))): d = tuple(-t for t in d)
                dirs.add(d)
    for p in cells:
        for d in dirs:
            if (p[0]-d[0], p[1]-d[1], p[2]-d[2]) in idx: continue
            L = []; x = p
            while x in idx: L.append(idx[x]); x = (x[0]+d[0], x[1]+d[1], x[2]+d[2])
            if len(L) >= 3: out.append(L)
    return out

def plane_cells(normal, d, n, idx):
    a, b, c = normal; out = []
    if c != 0:
        for x in range(n):
            for y in range(n):
                num = d - a*x - b*y
                if num % c == 0:
                    z = num // c
                    if 0 <= z < n: out.append(idx[(x, y, z)])
    elif b != 0:
        for x in range(n):
            num = d - a*x
            if num % b == 0:
                y = num // b
                if 0 <= y < n:
                    for z in range(n): out.append(idx[(x, y, z)])
    elif a != 0:
        if d % a == 0 and 0 <= d // a < n:
            x = d // a
            for y in range(n):
                for z in range(n): out.append(idx[(x, y, z)])
    return out

def canon_normal(a, b, c):
    g = gcd(gcd(abs(a), abs(b)), abs(c))
    if g == 0: return None
    a, b, c = a//g, b//g, c//g
    if (a, b, c) < (0, 0, 0) or (a == 0 and ((b, c) < (0, 0) or (b == 0 and c < 0))): a, b, c = -a, -b, -c
    return (a, b, c)

def small_planes(n, cells, idx, K):
    planes = {}
    for a in range(-K, K+1):
        for b in range(-K, K+1):
            for c in range(-K, K+1):
                nm = canon_normal(a, b, c)
                if nm is None or nm != (a, b, c): continue
                for d in range(-K*(n-1)*2, K*(n-1)*2 + 1):
                    L = plane_cells(nm, d, n, idx)
                    if len(L) >= 4: planes[(nm, d)] = L
    return planes

def det3(p, q, r, s):
    u = [q[i]-p[i] for i in range(3)]; v = [r[i]-p[i] for i in range(3)]; w = [s[i]-p[i] for i in range(3)]
    return u[0]*(v[1]*w[2]-v[2]*w[1]) - u[1]*(v[0]*w[2]-v[2]*w[0]) + u[2]*(v[0]*w[1]-v[1]*w[0])

def coplanar_quads(pts):
    return [q for q in itertools.combinations(pts, 4) if det3(*q) == 0]

def plane_of(p, q, r):
    u = [q[i]-p[i] for i in range(3)]; v = [r[i]-p[i] for i in range(3)]
    nm = (u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0])
    nm = canon_normal(*nm)
    if nm is None: return None
    return nm, nm[0]*p[0] + nm[1]*p[1] + nm[2]*p[2]

def solve_stratum(args):
    n, S, tag, tlimit, workers, outdir, K, pfile = args
    from ortools.sat.python import cp_model
    t0 = time.time()
    cells, idx, orb_of, orbs = orbits(S, n)
    L = lines(n, cells, idx)
    if pfile:
        planes = {}
        for a_, b_, c_, d_ in json.load(open(pfile)):
            L2 = plane_cells((a_, b_, c_), d_, n, idx)
            if len(L2) >= 4: planes[((a_, b_, c_), d_)] = L2
    else:
        planes = small_planes(n, cells, idx, K)
    cons = set(); added_planes = set(planes.keys())
    def build():
        model = cp_model.CpModel(); v = [model.NewBoolVar(f"o{k}") for k in range(len(orbs))]
        def add_cap(cellset, cap):
            mult = collections.Counter(orb_of[i] for i in cellset); key = (tuple(sorted(mult.items())), cap)
            if key in cons: return
            cons.add(key)
            bad = [k for k, c in mult.items() if c > cap]
            for k in bad: model.Add(v[k] == 0)
            rest = [(k, c) for k, c in mult.items() if c <= cap]
            if rest: model.Add(sum(c*v[k] for k, c in rest) <= cap)
        for line in L: add_cap(line, 2)
        for L2 in planes.values(): add_cap(L2, 3)
        model.Maximize(sum(len(orbs[k])*v[k] for k in range(len(orbs))))
        return model, v
    best_clean = 0; best_pts = []; status = "NONE"; rounds = 0; bound = None
    while time.time() - t0 < tlimit:
        cons.clear(); model, v = build()
        if best_pts:
            chosen = {orb_of[idx[p]] for p in best_pts}
            for k in range(len(orbs)): model.AddHint(v[k], 1 if k in chosen else 0)
        solver = cp_model.CpSolver(); solver.parameters.max_time_in_seconds = max(5, tlimit - (time.time()-t0)); solver.parameters.num_search_workers = workers
        st = solver.Solve(model); rounds += 1
        if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE): status = solver.StatusName(st); break
        bound = int(solver.BestObjectiveBound())
        pts = [cells[i] for k in range(len(orbs)) if solver.Value(v[k]) for i in [idx[c] for c in orbs[k]]]
        quads = coplanar_quads(pts)
        if not quads:
            if len(pts) > best_clean: best_clean, best_pts = len(pts), pts
            status = solver.StatusName(st); break
        newp = 0
        for q in quads:
            pl = plane_of(q[0], q[1], q[2])
            if pl is None or pl in added_planes: continue
            added_planes.add(pl); planes[pl] = plane_cells(pl[0], pl[1], n, idx); newp += 1
        if newp == 0: status = "STUCK"; break
        status = f"cut{rounds}"
    if best_pts:
        ok = not coplanar_quads(best_pts) and len(set(best_pts)) == best_clean
        with open(os.path.join(outdir, f"n{n}_{tag}_{best_clean}.txt"), "w") as f:
            f.write(f"# A280537 n={n} stratum {tag} ({describe(S)}) points={best_clean} status={status} bound={bound} rounds={rounds} planes={len(planes)} verified={ok}\n")
            for p in sorted(best_pts): f.write(f"{p[0]} {p[1]} {p[2]}\n")
    return dict(n=n, tag=tag, group=describe(S), orbits=len(orbs), planes=len(planes), best=best_clean, bound=bound, status=status, rounds=rounds, secs=round(time.time()-t0, 1))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("n", type=int); ap.add_argument("--time", type=float, default=600); ap.add_argument("--procs", type=int, default=8)
    ap.add_argument("--workers", type=int, default=2); ap.add_argument("--orders", default="2,3,4,6,8,12,16,24,48"); ap.add_argument("--out", default="strata_p")
    ap.add_argument("--K", type=int, default=3); ap.add_argument("--trivial", type=float, default=0)
    ap.add_argument("--only", default="", help="считать только эти классы, напр. c03,c06")
    ap.add_argument("--skip", default="", help="классы, которые не считать, напр. c01,c07 (для A280537 — все с инверсией: lem-003)")
    ap.add_argument("--planes", default=None, help="JSON [[a,b,c,d],...] точного множества плоскостей (planes_exact.py); тогда ленивые раунды — только контроль")
    a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
    classes = subgroup_classes(frozenset(all_matrices())); orders = {int(t) for t in a.orders.split(",")}
    jobs = []
    skip = set(t for t in a.skip.split(",") if t); only = set(t for t in a.only.split(",") if t)
    for i, S in enumerate(classes):
        if f"c{i:02d}" in skip or (only and f"c{i:02d}" not in only): continue
        if len(S) in orders: jobs.append((a.n, S, f"c{i:02d}_ord{len(S)}", a.time, a.workers, a.out, a.K, a.planes))
        if len(S) == 1 and a.trivial > 0: jobs.append((a.n, S, f"c{i:02d}_ord1", a.trivial, a.workers, a.out, a.K, a.planes))
    print(f"n={a.n}: страт {len(jobs)}, K={a.K}, planes={a.planes}", flush=True)
    results = []
    with Pool(a.procs) as pool:
        for r in pool.imap_unordered(solve_stratum, jobs):
            results.append(r)
            print(f"  {r['tag']:>12} {r['group']:>22} orbits={r['orbits']:4d} planes={r['planes']:6d} -> best={r['best']:3d} bound={r['bound']} {r['status']} rounds={r['rounds']} {r['secs']}s", flush=True)
            json.dump(sorted(results, key=lambda r: -r['best']), open(os.path.join(a.out, f"n{a.n}_results.json"), "w"), indent=1)
    best = max(results, key=lambda r: r['best'])
    print(f"ИТОГ n={a.n}: лучший чистый свидетель {best['best']} точек в страте {best['tag']} ({best['group']})", flush=True)

if __name__ == "__main__":
    main()
