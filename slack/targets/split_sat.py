"""split_sat.py — разбиение SAT-экземпляра на независимые куски для счёта на многих ядрах
(cube-and-conquer в простейшей, но полностью проверяемой форме).

ПОЛНОТА РАЗБИЕНИЯ доказывается тем же аргументом, что и у нашего перебора, и это важно: в z-столбце
(фиксированы x, y) любые три точки коллинеарны, а любые четыре — компланарны. Поэтому

    для no-three-in-line  в каждом столбце не более 2 точек  -> подмножеств размера <= 2;
    для no-four-coplanar  в каждом столбце не более 3 точек  -> подмножеств размера <= 3.

Перебор ВСЕХ таких подмножеств в первых c столбцах исчерпывает пространство. Общий экземпляр
невыполним тогда и только тогда, когда невыполним КАЖДЫЙ кусок — поэтому пропуск даже одного куска
обесценивает всё, и агрегатор обязан это ловить (см. check_split.py).

usage: python3 split_sat.py <no3|no4> n M outdir [--cols 2] [--sym]
"""
import os, subprocess, sys
from itertools import combinations

def main():
    kind, n, M, outdir = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    cols = int(sys.argv[sys.argv.index("--cols")+1]) if "--cols" in sys.argv else 2
    sym  = "--sym" in sys.argv
    cap  = 2 if kind == "no3" else 3
    gen  = "no3_3d_cnf.py" if kind == "no3" else "plane4_cnf.py"
    os.makedirs(outdir, exist_ok=True)
    base = os.path.join(outdir, "base.cnf")
    here = os.path.dirname(os.path.abspath(__file__))
    subprocess.run([sys.executable, os.path.join(here, gen), str(n), str(M), base] + (["--sym"] if sym else []), check=True)
    head = open(base).readline()
    body = open(base).read()
    # индекс клетки: (x*n + y)*n + z; столбец (x,y) — это z = 0..n-1
    subsets = [s for k in range(cap+1) for s in combinations(range(n), k)]
    cases, idx = [], 0
    def rec(ci, units):
        nonlocal idx
        if ci == cols:
            cases.append(list(units)); idx += 1; return
        x, y = ci // n, ci % n
        for s in subsets:
            u = [((x*n + y)*n + z) + 1 if z in s else -(((x*n + y)*n + z) + 1) for z in range(n)]
            rec(ci+1, units + u)
    rec(0, [])
    lines = body.splitlines()
    hdr = [i for i, l in enumerate(lines) if l.startswith("p cnf")][0]
    nv, ncl = lines[hdr].split()[2:4]
    for i, units in enumerate(cases):
        p = os.path.join(outdir, f"case_{i:05d}.cnf")
        with open(p, "w") as f:
            f.write(f"c split case {i} of {len(cases)}: {cols} columns fixed\n")
            f.write(f"p cnf {nv} {int(ncl)+len(units)}\n")
            f.write("\n".join(lines[hdr+1:]) + "\n")
            f.write("".join(f"{u} 0\n" for u in units))
    with open(os.path.join(outdir, "MANIFEST.txt"), "w") as f:
        f.write(f"kind={kind} n={n} M={M} cols={cols} sym={sym} cases={len(cases)}\n")
        for i in range(len(cases)): f.write(f"case_{i:05d}.cnf\n")
    print(f"{kind} n={n} M={M}: {len(cases)} кусков в {outdir} (по {len(subsets)} подмножеств на столбец, ёмкость {cap})")

if __name__ == "__main__": main()
