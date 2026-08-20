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
    if os.environ.get("CERT_BY") == "density":
        # ВЫБОРКА ПО ТРУДНОСТИ. Проверять надо там, где решатель ИСКАЛ: плотность остатка
        # d=(M-p)/(49-k) предсказывает трудность до запуска (docs/research/hardness_threshold.md).
        # Идём от самых плотных вниз; те, что не уложились в срок, дают ГРАНИЦУ: до какой
        # трудности наша проверка вообще достаёт. Это измерение, а не неудача.
        from itertools import combinations as _cb
        _S=[x for kk in range(4) for x in _cb(range(7),kk)]
        def _d(nm):
            ix=[int(t) for t in nm.split("_s")[1:]]
            return (19-sum(len(_S[i]) for i in ix))/(49-len(ix)-1)
        names=sorted(names, key=_d, reverse=True)[:k]
        print(f"выборка ПО ПЛОТНОСТИ: от {_d(names[0]):.3f} до {_d(names[-1]):.3f}", flush=True)
    else:
      # ВЫБОРКА ПО СЛОЯМ ГЛУБИНЫ, а не случайная. Случайная почти вся попадает в самую
      # многочисленную группу — глубокие куски (2770 из 3072), — а глубокий значит сильно
      # ограниченный, то есть ЛЁГКИЙ: все двенадцать первых решились за 0.5 с. Сертифицировать
      # там, где решатель не искал, — проверять работу там, где ошибиться было негде.
      # Берём поровну из каждой глубины, начиная с наименьшей: неглубокий = трудный.
      from collections import defaultdict as _dd
      by = _dd(list)
      for n in names: by[n.count("_s")].append(n)
      rnd = random.Random(seed)
      for d in by: rnd.shuffle(by[d])
      depths = sorted(by)
      names, i = [], 0
      while len(names) < k and any(by[d] for d in depths):
          d = depths[i % len(depths)]
          if by[d]: names.append(by[d].pop())
          i += 1
      print(f"выборка по слоям: {[(d, sum(1 for n in names if n.count('_s')==d)) for d in depths]}", flush=True)
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
    import shutil as _sh
    LIM = int(os.environ.get("CERT_LIMIT", "900"))      # потолок на решение, с
    MINGB = float(os.environ.get("CERT_MIN_GB", "3"))   # запас диска перед каждым куском
    skipped = 0
    for nm in names:
        free = _sh.disk_usage(W).free / 1e9
        if free < MINGB:
            print(f"  {nm}: ПРОПУЩЕН — на диске {free:.1f} ГБ при потребности {MINGB}. "
                  f"Это отказ по МЕСТУ, а не по существу."); skipped += 1; continue
        p = build(nm, body, nv, ncl)
        pr = p[:-4] + ".drat"
        t0 = time.time()
        try:
            r = subprocess.run(["kissat", "-q", p, pr], capture_output=True, timeout=LIM)
        except subprocess.TimeoutExpired:
            sz = os.path.getsize(pr)/1e6 if os.path.exists(pr) else 0
            print(f"  {nm}: СЛИШКОМ ДОРОГ — не решён за {LIM}с, сертификат уже {sz:.0f}МБ. "
                  f"Это ИЗМЕРЕНИЕ стоимости, а не отказ проверки."); skipped += 1
            for f in (p, pr):
                try: os.remove(f)
                except OSError: pass
            continue
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
    print(f"\nИТОГ: подтверждено {ok}, НЕ подтверждено {bad}, пропущено по стоимости/месту {skipped}")
    sys.exit(1 if bad else 0)
