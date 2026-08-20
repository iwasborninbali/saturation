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

# Тело базового куска читается ОДИН РАЗ на базу и держится как байты. Раньше каждый из 64
# подкусков заново читал 54 МБ, разбирал их в список из 2.8 млн строк и склеивал обратно:
# замерено 0.65 с против 0.04 с, то есть 41 с против 2 с на базовый кусок, при 15 работниках
# на машине с 11 ГБ памяти. Замер показал и другое: экономия всего полчаса ядрового времени на
# все 45 кусков, то есть УЗКОЕ МЕСТО НЕ ЗДЕСЬ — оно в самих тяжёлых подкусках. Правка взята
# потому, что она бесплатна и снимает давление на память, а не потому, что она решает задачу.
_BODY: dict = {}

def _body_of(base: str):
    if base not in _BODY:
        raw = open(base, "rb").read()
        nl = raw.index(b"\n", raw.index(b"p cnf"))
        hdr = raw[raw.index(b"p cnf"):nl].split()
        _BODY.clear()                      # держим ровно одну базу: 54 МБ на работника, не больше
        _BODY[base] = (hdr[2], int(hdr[3]), raw[nl+1:])
    return _BODY[base]

def work(job):
    base, col, n, sub, idx, workdir = job
    nv, ncl, body = _body_of(base)
    x, y = col // n, col % n
    units = [((x*n + y)*n + z) + 1 if z in sub else -(((x*n + y)*n + z) + 1) for z in range(n)]
    # ИМЯ ФАЙЛА ОБЯЗАНО НЕСТИ БАЗУ. Раньше путь зависел ТОЛЬКО от idx, а рабочий каталог
    # один на весь прогон: подкусок №idx базы A и подкусок №idx базы B писались в ОДИН файл.
    # open(path,"wb") усекает тот же inode, поэтому решатель, уже читающий его, получал чужое
    # или обрезанное содержимое. Отсюда наши rc=1 (обрыв при чтении) — и, что хуже, возможность
    # записать UNSAT ЧУЖОЙ формулы под именем своей. Это ошибка состоятельности, а не потеря работы.
    path = os.path.join(workdir, f"{os.path.basename(base)[:-4]}__s{idx}.cnf")
    with open(path, "wb") as f:
        f.write(b"p cnf %s %d\n" % (nv, ncl + len(units)))
        f.write(body)
        f.write(b"".join(b"%d 0\n" % u for u in units))
    # ЦЕЛОСТНОСТЬ ПЕРЕД РЕШЕНИЕМ. Обрыв записи (кончился диск) даёт файл правильного ИМЕНИ и
    # неправильного содержимого: решатель вернёт rc=1 за ноль секунд, и в журнале эта строка
    # неотличима от результата. Так у нас 162 узла остались нерешёнными и незамеченными.
    # Проверка стоит доли секунды против часов счёта.
    hdr_n = body.count(b"\n") + len(units) + (0 if body.endswith(b"\n") else 1)
    got = os.path.getsize(path)
    want = len(body) + len(b"p cnf %s %d\n" % (nv, ncl + len(units))) + \
           sum(len(b"%d 0\n" % u) for u in units)
    if got != want:
        return os.path.basename(base), idx, f"ОБОРВАН({got}!={want})", 0
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
    # ИНДЕКС НЕ ЗАВИСИТ ОТ ПОРЯДКА. Раньше разворот применялся к самому списку, а индекс брался
    # уже из развёрнутого: тогда `s0` в прогоне с флагом и без него — РАЗНЫЕ подмножества.
    # Дети одного узла, пришедшие из разных прогонов, дали бы удвоение одних подмножеств и
    # пропажу других, а счёт всё равно дошёл бы до 64 — то есть ложное закрытие, невидимое
    # ни по именам, ни по числу. Меняем ПОРЯДОК ОБХОДА, сохраняя канонический номер.
    order = list(range(len(subs)))
    if "--hardest-last" in sys.argv:
        # ПОРЯДОК ВАЖЕН. Подмножества перебираются с пустого, а пустое — наименее ограниченное,
        # то есть самое тяжёлое: лексикографическое отсечение сгоняет решения именно туда.
        # Идя по порядку, машина утыкается в тяжёлый подкусок КАЖДОГО базового куска первым и
        # закрывает по одному подкуску за сорок минут. Развернув порядок, получаем 63 быстрых
        # закрытия на каждый базовый и один тяжёлый в конце — тот же объём работы, но виден
        # прогресс и тяжёлые собираются в одно место, где их удобно дробить дальше.
        order = list(reversed(order))
    print(f"базовых кусков {len(bases)}, подкусков на каждый {len(subs)}, всего {len(bases)*len(subs)}, "
          f"параллелизм {P}, столбец {col}", flush=True)
    workdir = tempfile.mkdtemp(prefix="ssub_", dir="/tmp")
    jobs = [(b, col, n, subs[i], i, workdir) for b in bases for i in order]
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
