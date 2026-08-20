"""plane_sweep_second.py — НЕЗАВИСИМЫЙ ход к a(7) <= 18: перебор по содержимому ПЛОСКОСТИ.

ЗАЧЕМ. Дерево дроблений по СТОЛБЦАМ упёрлось: 91% неразобранной массы лежит в тридцати
узлах, у всех столбцы (0,0) и (0,1) пусты, и это почти пустое сообщение — плоскость x=0
держит <=3 точек на 7 столбцов, значит >=4 её столбца пусты ВСЕГДА. Мы дробили по признаку,
который почти ничего не говорит, и мера продвижения три замера подряд стояла на месте:
закрывались миллионы глубоких кусков, весящих ничто.

ПОСТРОЕНИЕ. У любой конфигурации есть определённое пересечение с плоскостью x=0, и оно
содержит не более 3 точек (плоскость есть богатая плоскость). Значит перебор всех
подмножеств размера <=3 из 49 клеток ИСЧЕРПЫВАЮЩ:
    C(49,0)+C(49,1)+C(49,2)+C(49,3) = 1 + 49 + 1176 + 18424 = 19650.
Кусок фиксирует ВСЕ 49 переменных плоскости, тогда как дробление по столбцу фиксирует 7.

ЗАМЕР: семь пробных кусков закрылись за 1.1 с каждый. 19650 * 1.1 с = 6 ядро-часов.

СОВМЕСТИМОСТЬ С ОТСЕЧЕНИЕМ СИММЕТРИИ. Законно ровно потому, что перечисляются ВСЕ
подмножества: у лексминимального представителя есть какое-то пересечение с плоскостью,
и кусок с ним в списке есть. ПРОПУСК ХОТЯ БЫ ОДНОГО ОБЕСЦЕНИВАЕТ ВСЁ — то же правило,
что для дробления по профилям.

ИМЕНА НЕСУТ ЗАДАЧУ. Куски зовутся plx0_<индексы клеток>, а не case_NNNNN: сегодня чужие
закрытия из задачи n=5 с такими же именами перевернули вердикт первого решателя
с «63 из 64» на «закрыто целиком». Имя обязано различать то, что обязано различаться.
"""
import sys, os, subprocess, time
from itertools import combinations

n = 7
BASE = os.environ.get("PS_BASE", "/tmp/wq/base.cnf")
OUT  = os.environ.get("PS_OUT",  "/dev/shm/ps")
FACTS= os.environ.get("PS_FACTS","/tmp/facts_plane.txt")
BUD  = int(os.environ.get("PS_BUD", "600"))
shard, nsh = int(sys.argv[1]), int(sys.argv[2])

os.makedirs(OUT, exist_ok=True)
raw = open(BASE, "rb").read()          # база читается ОДИН раз и живёт в памяти
i = raw.index(b"p cnf"); nl = raw.index(b"\n", i)
H = raw[i:nl].split(); BODY = raw[nl+1:]
NV, NCL = H[2], int(H[3])
cells = [(0, y, z) for y in range(n) for z in range(n)]
vid = lambda c: (c[0]*n*n + c[1]*n + c[2]) + 1
SUBS = [s for k in range(4) for s in combinations(range(len(cells)), k)]
assert len(SUBS) == 19650, f"кусков {len(SUBS)}, ожидалось 19650 — перебор НЕ исчерпывающ"

mine = [(i, s) for i, s in enumerate(SUBS) if i % nsh == shard]
fh = open(FACTS, "a", buffering=1)
t_start = time.time()
closed = sat = unresolved = 0
for idx, sub in mine:
    name = "plx0_" + ("-".join(f"{c:02d}" for c in sub) if sub else "пусто")
    f = f"{OUT}/{shard}_{idx}.cnf"
    ss = set(sub)
    u = [vid(cells[j]) if j in ss else -vid(cells[j]) for j in range(len(cells))]
    head = b"p cnf %s %d\n" % (NV, NCL + len(u))
    tail = b"".join(b"%d 0\n" % v for v in u)
    with open(f, "wb") as g: g.write(head + BODY + tail)
    if os.path.getsize(f) != len(head)+len(BODY)+len(tail):
        print(f"ОТКАЗ {name}: файл оборван", flush=True); os.remove(f); continue
    r = subprocess.run(["timeout", str(BUD), "kissat", "-q", f], capture_output=True)
    os.remove(f)
    if r.returncode == 20:
        closed += 1; fh.write(name + "\n")
    elif r.returncode == 10:
        sat += 1
        print(f"ВЫПОЛНИМ {name} — УТВЕРЖДЕНИЕ a(7)<=18 РУШИТСЯ", flush=True)
        fh.write("SAT " + name + "\n")
    else:
        unresolved += 1
        print(f"НЕ РЕШЁН {name} за {BUD}с (rc={r.returncode})", flush=True)
    if (closed + sat + unresolved) % 200 == 0:
        el = time.time() - t_start
        print(f"доля {shard}: {closed+sat+unresolved}/{len(mine)}, закрыто {closed}, "
              f"не решено {unresolved}, {el:.0f}с", flush=True)
el = time.time() - t_start
print(f"ДОЛЯ {shard} ГОТОВА: всего {len(mine)}, закрыто {closed}, выполнимых {sat}, "
      f"не решено {unresolved}, {el:.0f}с", flush=True)
