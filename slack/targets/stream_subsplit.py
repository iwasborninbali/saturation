"""stream_subsplit.py — доразбиение тяжёлых кусков БЕЗ хранения на диске.

Зачем. Осталось 158 тяжёлых кусков, каждый идёт по 40 минут. Дробление на 64 подкуска закрывает
подавляющее большинство за секунды — но 158*64 файлов по 52 МБ это 526 ГБ, и хранить их негде.
Здесь подкусок собирается в памяти, пишется во временный файл, решается и удаляется; на диске
одновременно лежит не больше `-P` штук.

ПОЛНОТА. В z-столбце (фиксированы x,y) четыре точки компланарны (они коллинеарны), поэтому
подмножества размера <= 3 исчерпывают столбец: 1+n+C(n,2)+C(n,3) штук. Кусок закрыт тогда и только
тогда, когда закрыты ВСЕ его подкуски; частичное закрытие не закрывает ничего.

usage: stream_subsplit.py <список_базовых_cnf> <колонка> <n> <cap> <файл-результатов> [-P k]
"""
from __future__ import annotations
import os, subprocess, sys, tempfile, time
from concurrent.futures import ThreadPoolExecutor, as_completed
from itertools import combinations

def subsets(n: int, cap: int):
    return [s for k in range(cap+1) for s in combinations(range(n), k)]

def work(job):
    base, col, n, sub, idx, workdir = job
    lines = open(base).read().splitlines()
    h = next(i for i, l in enumerate(lines) if l.startswith("p cnf"))
    nv, ncl = lines[h].split()[2:4]
    x, y = col // n, col % n
    units = [((x*n + y)*n + z) + 1 if z in sub else -(((x*n + y)*n + z) + 1) for z in range(n)]
    path = os.path.join(workdir, f"s{idx}.cnf")
    with open(path, "w") as f:
        f.write(f"p cnf {nv} {int(ncl)+len(units)}\n")
        f.write("\n".join(lines[h+1:]) + "\n")
        f.write("".join(f"{u} 0\n" for u in units))
    t0 = time.time()
    try:
        r = subprocess.run(["kissat", "-q", path], capture_output=True)
        st = {10: "SAT", 20: "UNSAT"}.get(r.returncode, f"rc={r.returncode}")
        if r.returncode == 10:
            open(os.path.join(workdir, f"SAT_{os.path.basename(base)}_{idx}.txt"), "w").write(
                r.stdout.decode("utf8", "replace"))
    finally:
        try: os.remove(path)
        except OSError: pass
    return os.path.basename(base), idx, st, int(time.time()-t0)

def main():
    lst, col, n, cap, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
    P = int(sys.argv[sys.argv.index("-P")+1]) if "-P" in sys.argv else 4
    bases = [l.strip() for l in open(lst) if l.strip()]
    subs = subsets(n, cap)
    print(f"базовых кусков {len(bases)}, подкусков на каждый {len(subs)}, всего {len(bases)*len(subs)}, "
          f"параллелизм {P}, столбец {col}", flush=True)
    workdir = tempfile.mkdtemp(prefix="ssub_", dir="/tmp")
    jobs = [(b, col, n, s, i, workdir) for b in bases for i, s in enumerate(subs)]
    done = sat = 0
    closed = {}
    with open(out, "w") as f:
        f.write(f"# базовых {len(bases)} подкусков-на-кусок {len(subs)} всего {len(jobs)}\n")
    with ThreadPoolExecutor(max_workers=P) as ex:
        futs = [ex.submit(work, j) for j in jobs]
        for fut in as_completed(futs):
            b, idx, st, secs = fut.result()
            done += 1
            if st == "SAT": sat += 1
            if st == "UNSAT": closed[b] = closed.get(b, 0) + 1
            with open(out, "a") as f:
                f.write(f"{b} s{idx} {st} {secs}s\n")
            if st == "SAT" or done % 200 == 0:
                full = sum(1 for v in closed.values() if v == len(subs))
                print(f"  {done}/{len(jobs)}; базовых закрыто целиком {full}/{len(bases)}"
                      + ("  ВЫПОЛНИМЫЙ!" if st == "SAT" else ""), flush=True)
    full = sum(1 for v in closed.values() if v == len(subs))
    print(f"ИТОГО: подкусков {done}/{len(jobs)}, выполнимых {sat}, "
          f"базовых кусков закрыто ЦЕЛИКОМ {full} из {len(bases)}", flush=True)
    if sat: sys.exit(2)
    if full != len(bases): sys.exit(1)

if __name__ == "__main__":
    main()
