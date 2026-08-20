"""hybrid_second.py — СЦЕПКА двух приёмов: плоскость задаёт начало, столбцы добирают вглубь.

ЗАЧЕМ. Тип куска определяет приём, и это измерено:
  * задано 3 точки в плоскости x=0 (94% перебора) — закрывается плоскостным ходом за ~1 с;
  * задано 0, 1 или 2 (6%) — плоскостной ход не берёт за 600 с.
Для упрямых проверены и отвергнуты ДВА хода:
  * дробление по одному столбцу с длинным бюджетом: 0 закрытий за 180 с, 6 детей в бюджет;
  * добавление ТОЧНОГО профиля слоёв (при одной точке в плоскости профиль определён
    полностью — (1,3,3,3,3,3,3), потому что запас ёмкости всего 2): бюджет 300 с исчерпан.
Второе особенно поучительно: точные мощности по всем семи слоям не помогли даже вместе
с 49 фиксированными позициями. Это третье подтверждение, что решателю нужна ОПРЕДЕЛЁННОСТЬ
позиций, а не ограничения на количества.

Остаётся приём, который у нас РАБОТАЕТ и закрыл 235 тысяч узлов: короткий бюджет плюс
НЕМЕДЛЕННОЕ дробление уцелевших. Прежняя проба провалилась не потому, что столбцы плохи,
а потому, что я дал один уровень с длинным бюджетом — то есть ровно то «ждать вместо дробить»,
против чего у нас есть измерение (отношение закрытий к дроблениям 37:1 и 60:1).

Столбцы 0..6 уже определены содержимым плоскости x=0, поэтому рекурсия начинается со столбца 7.
"""
import sys, os, subprocess, time
from itertools import combinations

n = 7
BASE  = os.environ.get("HY_BASE",  "/tmp/wq/base.cnf")
OUT   = os.environ.get("HY_OUT",   "/dev/shm/hy")
FACTS = os.environ.get("HY_FACTS", "/tmp/facts_hybrid.txt")
BUD   = int(os.environ.get("HY_BUD", "120"))
MAXC  = int(os.environ.get("HY_MAXC", str(n*n)))
shard, nsh = int(sys.argv[1]), int(sys.argv[2])
parents = [l.strip() for l in open(sys.argv[3]) if l.strip().startswith("plx0_")]

os.makedirs(OUT, exist_ok=True)
raw = open(BASE, "rb").read()
i = raw.index(b"p cnf"); nl = raw.index(b"\n", i)
H = raw[i:nl].split(); BODY = raw[nl+1:]
NV, NCL = H[2], int(H[3])
cells = [(0, y, z) for y in range(n) for z in range(n)]
vid = lambda c: (c[0]*n*n + c[1]*n + c[2]) + 1
SUBS = [s for k in range(4) for s in combinations(range(n), k)]

def units(name):
    """Имя: plx0_<клетки>[_c<столбец>s<подмножество>]... Единичные дизъюнкты собираются
    из ОБЕИХ частей — плоскости и всех зафиксированных столбцов."""
    head, *cols = name.split("_c")
    idx = set() if head.endswith("пусто") else {int(t) for t in head[5:].split("-")}
    u = [vid(cells[j]) if j in idx else -vid(cells[j]) for j in range(49)]
    for part in cols:
        col, sub = part.split("s")
        col = int(col); s = SUBS[int(sub)]
        x, y = col // n, col % n
        u += [((x*n+y)*n+z)+1 if z in s else -(((x*n+y)*n+z)+1) for z in range(n)]
    return u

# РАСПИСАНИЕ СТОЛБЦОВ: ДОЕДАТЬ СЛОЙ, А НЕ БРАТЬ СВЕЖИЙ.
# Измерено ранее: дробление по столбцу ВНУТРИ слоя закрывает 57-60 детей из 64 даром,
# а по столбцу СВЕЖЕГО слоя — ровно 1 из 64. Механизм: слой есть богатая плоскость и несёт
# не более 3 точек, поэтому фиксация нескольких его столбцов делает большинство подмножеств
# немедленно противоречивыми; столбец свежего слоя не сталкивается ни с чем.
#
# Плоскость x=0 занимает столбцы 0..6. Первая моя редакция шла дальше по 7, 8, 9 — то есть
# по слою x=1, СВЕЖЕМУ, ровно худший случай. Верное продолжение — доедать слой y=0, чьи
# столбцы суть (x,0) = 0, 7, 14, 21, 28, 35, 42, и чей столбец 0 уже определён плоскостью.
# Потом слой y=1 и так далее.
SCHED = [7*x + y for y in range(n) for x in range(1, n)]
assert len(SCHED) == 42 and len(set(SCHED)) == 42, "расписание неполно или с повторами"
assert not set(SCHED) & set(range(7)), "расписание залезает в уже зафиксированную плоскость"

stats = {"закрыто": 0, "дроблений": 0, "выполнимых": 0, "предел": 0, "оснастка": 0}
fh = open(FACTS, "a", buffering=1)

def solve(name, step):
    """Возвращает True, если поддерево закрыто целиком. step — ИНДЕКС В РАСПИСАНИИ,
    а не номер столбца: порядок задаётся расписанием, а не арифметикой."""
    if step >= len(SCHED):
        stats["предел"] += 1
        print(f"ПРЕДЕЛ {name} (расписание исчерпано на шаге {step})", flush=True)
        return False
    u = units(name)
    f = f"{OUT}/{shard}.cnf"
    head = b"p cnf %s %d\n" % (NV, NCL + len(u))
    tail = b"".join(b"%d 0\n" % v for v in u)
    with open(f, "wb") as g: g.write(head + BODY + tail)
    if os.path.getsize(f) != len(head)+len(BODY)+len(tail):
        stats["оснастка"] += 1; print(f"ОТКАЗ {name}: файл оборван", flush=True); return False
    r = subprocess.run(["timeout", str(BUD), "kissat", "-q", f], capture_output=True)
    if r.returncode == 20:
        stats["закрыто"] += 1; fh.write(name + "\n"); return True
    if r.returncode == 10:
        stats["выполнимых"] += 1; fh.write("SAT " + name + "\n")
        print(f"ВЫПОЛНИМ {name} — УТВЕРЖДЕНИЕ a(7)<=18 РУШИТСЯ", flush=True); return False
    if r.returncode != 124:
        stats["оснастка"] += 1
        print(f"ОТКАЗ ОСНАСТКИ {name}: rc={r.returncode} — это НЕ трудность куска", flush=True)
        return False
    # уцелел — ДРОБИМ НЕМЕДЛЕННО, а не ждём дольше
    stats["дроблений"] += 1
    ok = True
    col = SCHED[step]
    for j in range(64):
        if not solve(f"{name}_c{col}s{j:03d}", step + 1): ok = False
    return ok

mine = [p for k, p in enumerate(parents) if k % nsh == shard]
t0 = time.time()
for p in mine:
    if solve(p, 0):
        print(f"РОДИТЕЛЬ ЗАКРЫТ ЦЕЛИКОМ: {p} ({time.time()-t0:.0f}с)", flush=True)
    else:
        print(f"родитель {p} НЕ закрыт", flush=True)
    print(f"  доля {shard}: {stats}, {time.time()-t0:.0f}с", flush=True)
print(f"ДОЛЯ {shard} ГОТОВА: родителей {len(mine)}, {stats}, {time.time()-t0:.0f}с", flush=True)
