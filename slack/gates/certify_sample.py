"""certify_sample.py — выборочная сертификация закрытых кусков DRAT-ом.

Зачем: все наши факты получены kissat. Если утверждение состоится, слабейшим звеном будет
доверие к одному решателю. Второй решатель местами непосилен (измерено: на одном куске Glucose
молотил 754 с и не закрыл, kissat закрыл за 0.47 с — разница в полторы тысячи раз). DRAT даёт
независимость БЕЗ второго решателя: сертификат проверяет чужая программа drat-trim, не доверяя
ни kissat, ни нам.

Цена измерена: проверка стоит около 2.4 времени решения, сертификат пишется со скоростью
0.55 МБ/с. Связывающее ограничение — не время, а ВРЕМЕННОЕ МЕСТО: сертификат проверяется
сразу и удаляется.

ОГРАНИЧЕНИЕ, БЕЗ КОТОРОГО ЭТИМ ПОЛЬЗОВАТЬСЯ НЕЛЬЗЯ. Кусок восстанавливается ПО ИМЕНИ, и при
этом принимается соглашение «глубина k <=> столбец k». Оно верно для прогонов ВТОРОГО солвера.
У первого солвера есть схема имён со столбцом внутри (subsplit_c.py), и к его фактам этот
восстановитель применять НЕЛЬЗЯ: он соберёт другую формулу, её невыполнимость ничего не скажет
о настоящем куске, а вывод «ПОДТВЕРЖДЁН» будет ложным и неотличимым от верного.
Поэтому по умолчанию берётся facts_second_solver.txt. Проверять чужие факты — только после
явной сверки соглашения.

usage: certify_sample.py <файл-фактов> <сколько> [seed]
"""
import os, random, subprocess, sys, time
from itertools import combinations
N, CAP = 7, 3
SUBS = [s for k in range(CAP + 1) for s in combinations(range(N), k)]
W = os.environ.get("CERT_WORK", "/tmp/cert")
os.makedirs(W, exist_ok=True)

def units(col, sub):
    x, y = col // N, col % N
    return [((x * N + y) * N + z) + 1 if z in sub else -(((x * N + y) * N + z) + 1) for z in range(N)]

def build(name, base_body, nv, ncl):
    """Собрать кусок по ИМЕНИ: case_00000_sA_sB_... — столбец k задаётся глубиной."""
    parts = name.split("_s")
    idxs = [int(p) for p in parts[1:]]
    u = units(0, SUBS[int(parts[0].split("_")[1])])
    for depth, k in enumerate(idxs, start=1):
        u += units(depth, SUBS[k])
    head = b"p cnf %s %d\n" % (nv, ncl + len(u))
    tail = b"".join(b"%d 0\n" % v for v in u)
    p = os.path.join(W, name + ".cnf")
    open(p, "wb").write(head + base_body + tail)
    assert os.path.getsize(p) == len(head) + len(base_body) + len(tail), f"ОБОРВАН {p}"
    return p

if __name__ == "__main__":
    facts, k = sys.argv[1], int(sys.argv[2])
    seed = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    names = [l.strip() for l in open(facts) if l.strip() and not l.startswith("#")]
    names = [n for n in names if n.count("_s") >= 3]        # неглубокие слишком дороги
    random.Random(seed).shuffle(names)
    names = names[:k]
    base = os.path.join(W, "base.cnf")
    if not os.path.exists(base):
        t0 = time.time()
        subprocess.run([sys.executable, "slack/targets/plane4_cnf.py", "7", "19", base, "--sym"],
                       capture_output=True, check=True)
        print(f"база за {time.time()-t0:.0f}с", flush=True)
    raw = open(base, "rb").read()
    i = raw.index(b"p cnf"); nl = raw.index(b"\n", i)
    h = raw[i:nl].split(); body = raw[nl+1:]
    nv, ncl = h[2], int(h[3])
    ok = bad = 0
    for nm in names:
        p = build(nm, body, nv, ncl)
        pr = p[:-4] + ".drat"
        t0 = time.time()
        r = subprocess.run(["kissat", "-q", p, pr], capture_output=True)
        solve = time.time() - t0
        if r.returncode != 20:
            print(f"  {nm}: решатель дал rc={r.returncode}, НЕ UNSAT — сертифицировать нечего"); bad += 1
            for f in (p, pr):
                try: os.remove(f)
                except OSError: pass
            continue
        sz = os.path.getsize(pr) / 1e6
        t1 = time.time()
        v = subprocess.run(["drat-trim", p, pr, "-f"], capture_output=True, timeout=7200)
        ver = time.time() - t1
        good = b"s VERIFIED" in v.stdout
        print(f"  {nm}: {'ПОДТВЕРЖДЁН' if good else 'НЕ ПОДТВЕРЖДЁН'} "
              f"(решение {solve:.1f}с, сертификат {sz:.0f}МБ, проверка {ver:.1f}с)", flush=True)
        ok += good; bad += (not good)
        for f in (p, pr):
            try: os.remove(f)
            except OSError: pass
    print(f"\nИТОГ: подтверждено {ok}, НЕ подтверждено {bad}")
    sys.exit(1 if bad else 0)
