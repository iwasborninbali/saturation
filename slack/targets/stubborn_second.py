"""stubborn_second.py — второй приём для УПРЯМЫХ кусков плоскостного перебора.

НАБЛЮДЕНИЕ, СДЕЛАННОЕ ОБОИМИ НЕЗАВИСИМО. Трудность идёт от малого размера к большому
В ОБРАТНУЮ СТОРОНУ: куски, где в плоскости x=0 задано 3 точки (94% перебора), закрываются
за секунду и не дают упрямых вовсе; упрямы те, где задано 0, 1 или 2. У меня из 55 упрямых
пять размера 1 и пятьдесят размера 2, размера 3 — НИ ОДНОГО. У первого решателя из 762
закрытий та же картина.

ПОЧЕМУ. Три зафиксированные точки плюс запрет на четвёртую в плоскости почти не оставляют
свободы; две точки оставляют её много. Это количественное подтверждение того, что решателю
нужна ОПРЕДЕЛЁННОСТЬ, а не ограничения.

ОТСЮДА ВЫВОД, КОТОРЫЙ Я ЧУТЬ НЕ ПРОПУСТИЛ. Я собирался объявить столбцовое дерево тупиковым
целиком. Оно не тупиковое — у него ДРУГАЯ ОБЛАСТЬ ПРИМЕНИМОСТИ. Два приёма дополняют друг
друга ровно по размеру куска: плоскость берёт 94%, столбец добирает упрямые 6%, где мало
задано и добавить определённость есть чем. Третий раз за сутки правило оказывается верным
не вообще, а в диапазоне.

Здесь упрямый кусок дробится по столбцу 7 — первому столбцу СЛЕДУЮЩЕЙ плоскости, поскольку
столбцы 0..6 уже зафиксированы содержимым плоскости x=0. Детей 64.
"""
import sys, os, subprocess, time
from itertools import combinations

n = 7
BASE  = os.environ.get("ST_BASE",  "/tmp/wq/base.cnf")
OUT   = os.environ.get("ST_OUT",   "/dev/shm/st")
FACTS = os.environ.get("ST_FACTS", "/tmp/facts_stubborn.txt")
BUD   = int(os.environ.get("ST_BUD", "600"))
shard, nsh = int(sys.argv[1]), int(sys.argv[2])
names = [l.strip() for l in open(sys.argv[3]) if l.strip().startswith("plx0_")]

os.makedirs(OUT, exist_ok=True)
raw = open(BASE, "rb").read()
i = raw.index(b"p cnf"); nl = raw.index(b"\n", i)
H = raw[i:nl].split(); BODY = raw[nl+1:]
NV, NCL = H[2], int(H[3])
cells = [(0, y, z) for y in range(n) for z in range(n)]
vid = lambda c: (c[0]*n*n + c[1]*n + c[2]) + 1
SUBS = [s for k in range(4) for s in combinations(range(n), k)]

def units_plane(name):
    idx = set() if name.endswith("пусто") else {int(t) for t in name[5:].split("-")}
    return [vid(cells[j]) if j in idx else -vid(cells[j]) for j in range(49)]

def units_col(col, sub):
    x, y = col // n, col % n
    return [((x*n+y)*n+z)+1 if z in sub else -(((x*n+y)*n+z)+1) for z in range(n)]

mine = [nm for k, nm in enumerate(names) if k % nsh == shard]
fh = open(FACTS, "a", buffering=1)
t0 = time.time()
closed_children = 0; open_children = 0; broken = 0; done_parents = 0
for parent in mine:
    up = units_plane(parent)
    bad = 0
    for j in range(64):
        child = f"{parent}_c07s{j:03d}"
        u = up + units_col(7, SUBS[j])
        f = f"{OUT}/{shard}_{j}.cnf"
        head = b"p cnf %s %d\n" % (NV, NCL + len(u))
        tail = b"".join(b"%d 0\n" % v for v in u)
        with open(f, "wb") as g: g.write(head + BODY + tail)
        if os.path.getsize(f) != len(head)+len(BODY)+len(tail):
            print(f"ОТКАЗ {child}: файл оборван", flush=True); os.remove(f); bad = 1; continue
        r = subprocess.run(["timeout", str(BUD), "kissat", "-q", f], capture_output=True)
        os.remove(f)
        if r.returncode == 20:
            closed_children += 1; fh.write(child + "\n")
        elif r.returncode == 10:
            print(f"ВЫПОЛНИМ {child} — УТВЕРЖДЕНИЕ a(7)<=18 РУШИТСЯ", flush=True)
            fh.write("SAT " + child + "\n"); bad = 1
        elif r.returncode == 124:
            open_children += 1; bad = 1
            print(f"НЕ РЕШЁН {child} за {BUD}с — БЮДЖЕТ (это измерение трудности)", flush=True)
        else:
            broken += 1; bad = 1
            print(f"ОТКАЗ ОСНАСТКИ {child}: rc={r.returncode} — это НЕ трудность куска", flush=True)
            if broken >= 5 and closed_children == 0:
                print("ОСТАНОВ: пять отказов оснастки без единого закрытия", flush=True); sys.exit(4)
    if bad == 0:
        done_parents += 1
        print(f"РОДИТЕЛЬ ЗАКРЫТ через 64 детей: {parent}", flush=True)
    else:
        print(f"родитель {parent} НЕ закрыт — остались открытые дети", flush=True)
print(f"ДОЛЯ {shard} ГОТОВА: родителей {len(mine)}, закрыто целиком {done_parents}, "
      f"детей закрыто {closed_children}, детей открыто {open_children}, "
      f"отказов оснастки {broken}, {time.time()-t0:.0f}с", flush=True)
