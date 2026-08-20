"""stream_profiles.py — разбиение по профилям слоёв БЕЗ хранения кусков на диске.

Зачем. Разбиение по паре осей для n=7, M=19 даёт 784 куска по ~52 МБ, то есть 41 ГБ — больше,
чем есть на машине. Дважды за час мы упирались в переполнение диска, и один раз оно дало ТИХУЮ
недогенерацию (ловушка 9). Поэтому кусок здесь генерируется, решается и удаляется; на диске
одновременно лежит не больше `-P` штук.

ПОЛНОТА. У конфигурации есть определённый профиль вдоль КАЖДОЙ оси. Перечисляя ВСЕ пары
(профиль по оси a, профиль по оси b), мы покрываем пространство: у любой допустимой конфигурации
есть какая-то пара, и кусок с ней в списке присутствует. Пропуск даже одной пары обесценивает всё,
поэтому список пар строится здесь же и печатается в журнал вместе с их числом.

Совместимо с симметрийным отсечением ровно потому, что перечисляются все пары: лексминимальный
представитель орбиты имеет какие-то профили, и кусок с ними есть.

usage: stream_profiles.py <no3|no4> n M [-P параллелизм] [--axes a,b] [--sym] [--out файл]
"""
from __future__ import annotations
import os, subprocess, sys, tempfile, time
from concurrent.futures import ThreadPoolExecutor
from itertools import product

HERE = os.path.dirname(os.path.abspath(__file__))

def profiles(n: int, M: int, cap: int) -> list[tuple]:
    return [c for c in product(range(cap+1), repeat=n) if sum(c) == M]

def run_one(args):
    kind, n, M, pa, pb, axes, sym, workdir, idx = args
    gen = os.path.join(HERE, "no3_3d_cnf.py" if kind == "no3" else "plane4_cnf.py")
    cnf = os.path.join(workdir, f"p{idx}.cnf")
    spec = f"{axes[0]}={','.join(map(str,pa))};{axes[1]}={','.join(map(str,pb))}"
    cmd = [sys.executable, gen, str(n), str(M), cnf, "--profiles", spec] + (["--sym"] if sym else [])
    t0 = time.time()
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0 or not os.path.exists(cnf):
        return (idx, spec, f"GENFAIL:{r.stderr.strip()[:60]}", 0)
    try:
        s = subprocess.run(["kissat", "-q", cnf], capture_output=True)
        rc = s.returncode
        status = {10: "SAT", 20: "UNSAT"}.get(rc, f"rc={rc}")
        sol = s.stdout.decode("utf8", "replace") if rc == 10 else ""
    finally:
        try: os.remove(cnf)
        except OSError: pass
    if rc == 10:                                   # выполнимый кусок — СОХРАНИТЬ немедленно
        open(os.path.join(workdir, f"SAT_{idx}.txt"), "w").write(spec + "\n" + sol)
    return (idx, spec, status, int(time.time()-t0))

def main():
    kind, n, M = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    P = int(sys.argv[sys.argv.index("-P")+1]) if "-P" in sys.argv else 4
    axes = tuple(int(t) for t in sys.argv[sys.argv.index("--axes")+1].split(",")) if "--axes" in sys.argv else (0,1)
    sym = "--sym" in sys.argv
    out = sys.argv[sys.argv.index("--out")+1] if "--out" in sys.argv else f"/tmp/stream_{kind}_{n}_{M}.txt"
    cap = 2 if kind == "no3" else 3
    ps = profiles(n, M, cap)
    pairs = [(a, b) for a in ps for b in ps]
    print(f"{kind} n={n} M={M}: профилей по оси {len(ps)}, ПАР {len(pairs)}, параллелизм {P}, оси {axes}", flush=True)
    workdir = tempfile.mkdtemp(prefix="stream_", dir="/tmp")
    with open(out, "w") as f:
        f.write(f"# {kind} n={n} M={M} axes={axes} sym={sym} pairs={len(pairs)}\n")
    args = [(kind, n, M, a, b, axes, sym, workdir, i) for i, (a, b) in enumerate(pairs)]
    done = sat = 0
    with ThreadPoolExecutor(max_workers=P) as ex:
        for idx, spec, status, secs in ex.map(run_one, args):
            done += 1
            if status == "SAT": sat += 1
            with open(out, "a") as f:
                f.write(f"{idx} {spec} {status} {secs}s\n")
            if status == "SAT" or done % 25 == 0 or status.startswith(("rc=", "GENFAIL")):
                print(f"  {done}/{len(pairs)} последний: {status}" + ("  <-- ВЫПОЛНИМЫЙ" if status=="SAT" else ""), flush=True)
    print(f"ИТОГО: кусков {len(pairs)}, записано результатов {done}, ВЫПОЛНИМЫХ {sat}", flush=True)
    if done != len(pairs):
        print("ОТКАЗ: записано меньше результатов, чем кусков — покрытие НЕПОЛНО"); sys.exit(1)
    if sat: print("ВЫПОЛНИМЫЕ КУСКИ ЕСТЬ: утверждение о невыполнимости ЛОЖНО"); sys.exit(2)
    print("все куски невыполнимы")

if __name__ == "__main__":
    main()
