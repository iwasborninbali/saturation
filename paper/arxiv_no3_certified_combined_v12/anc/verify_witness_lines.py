"""verify_witness_lines.py — независимая проверка свидетеля для трёхмерного no-three-in-line:
перебор ВСЕХ троек целочисленными векторными произведениями. Никакой связи с кодировкой и с
перечислителем: вход — только координаты.
usage: python3 verify_witness_lines.py n ПУТЬ | n "(x,y,z) ..." | --file ПУТЬ [n [сколько]] | --selftest"""
import re, sys, os
from itertools import combinations
def cross(a,b,c):
    u=[b[i]-a[i] for i in range(3)]; v=[c[i]-a[i] for i in range(3)]
    return (u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0])
def check(n, pts, expect=None):
    if len(pts) < 3:
        print(f"  ОТКАЗ: свидетель ПУСТОЙ или слишком мал ({len(pts)} точек) — проверять нечего, это НЕ подтверждение")
        return False
    if expect is not None and len(pts) != expect:
        print(f"  ОТКАЗ: точек {len(pts)}, а ожидалось {expect}")
        return False
    if len(set(pts))!=len(pts): print("  точки НЕ различны"); return False
    if not all(0<=c<n for p in pts for c in p): print("  точка вне куба"); return False
    bad=[t for t in combinations(pts,3) if cross(*t)==(0,0,0)]
    import math
    print(f"  n={n}: точек {len(pts)}, проверено троек {math.comb(len(pts),3)}, коллинеарных {len(bad)}"
          + (f"  ПЕРВАЯ {bad[0]} — СВИДЕТЕЛЬ НЕВЕРЕН" if bad else "  — свидетель ЧИСТ"))
    return not bad
# ПРАВИЛО: калибровочный случай берётся из АРТЕФАКТА, а не сочиняется. Сочинённый
# "заведомо чистый" вход уже один раз оказался грязным (слой 4x4x2 содержит три
# коллинеарные точки), и самопроверка ловила собственную ошибку, а не проверяльщика.
import os as _os
_HERE=_os.path.dirname(_os.path.abspath(__file__))
GOOD_N = 6
def GOOD_SAMPLE():
    txt=open(_os.path.join(_HERE,"sat_witness_n6_64.txt")).read()
    cl="\n".join(l for l in txt.splitlines() if not l.strip().startswith("#"))
    pts=[tuple(map(int,m)) for m in re.findall(r'\((\d+),(\d+),(\d+)\)',cl)]
    if not pts:
        pts=[tuple(int(t) for t in l.split()) for l in cl.splitlines()
             if len(l.split())==3 and all(t.lstrip("-").isdigit() for t in l.split())]
    return pts
def PLANT_BAD(pts, rnd):
    # Подсаживаем ЯВНУЮ коллинеарную тройку a, a+d, a+2d внутри куба и убираем
    # столько прочих точек, чтобы тройка точно осталась.
    for _ in range(200):
        a=(rnd.randrange(GOOD_N),rnd.randrange(GOOD_N),rnd.randrange(GOOD_N))
        d=(rnd.randrange(-2,3),rnd.randrange(-2,3),rnd.randrange(-2,3))
        if d==(0,0,0): continue
        t=[tuple(a[i]+k*d[i] for i in range(3)) for k in (0,1,2)]
        if all(0<=c<GOOD_N for q in t for c in q) and len(set(t))==3:
            return list(dict.fromkeys(t+[q for q in pts if q not in t]))
    return None
if __name__=="__main__":
    a=sys.argv[1:]
    if not a:
        print("  ОТКАЗ: нечего проверять"); sys.exit(1)
    if a[0]=="--selftest":
        # Проверяльщик, ни разу не показавший ОТКАЗ, не проверен. Здесь он обязан
        # принять заведомо чистый вход и отвергнуть заведомо грязный.
        import random
        ok = True
        for trial in range(20):
            random.seed(trial)
            good = GOOD_SAMPLE()
            if not check(GOOD_N, good):
                print(f"  СБОЙ САМОПРОВЕРКИ: чистый вход отвергнут (попытка {trial})"); ok=False; break
            bad = PLANT_BAD(list(good), random)
            if bad is None: continue
            if check(GOOD_N, bad):
                print(f"  СБОЙ САМОПРОВЕРКИ: ГРЯЗНЫЙ вход принят (попытка {trial}) — проверяльщик слеп"); ok=False; break
        print("  самопроверка ПРОЙДЕНА: чистое принимается, грязное отвергается" if ok else "  самопроверка ПРОВАЛЕНА")
        sys.exit(0 if ok else 1)
    if a[0]=="--file":
        txt=open(a[1]).read(); nums=a[2:]
    else:
        # argv[2] — либо путь, либо сам текст свидетеля. Различаем по существованию файла.
        # Молчаливый разбор ПУТИ как данных даёт ложную тревогу на ВЕРНОМ свидетеле, а это
        # хуже простого отказа: посторонний аудитор естественно передаёт путь.
        txt=open(a[1]).read() if (len(a)>1 and os.path.exists(a[1])) else (a[1] if len(a)>1 else "")
        nums=[a[0]]+a[2:]
    # Два формата, оба явные; строки-комментарии (#) отбрасываются.
    #   A: "(x,y,z) (x,y,z) ..."           — наш вывод из SAT
    #   B: по одной точке на строку "x y z" — формат первого солвера
    # Расширять разбор дальше НЕ следует: свободный парсер тем и опасен, что находит
    # числа там, где их не имели в виду.
    clean = "\n".join(l for l in txt.splitlines() if not l.strip().startswith("#"))
    pts=[tuple(map(int,m)) for m in re.findall(r'\((\d+),(\d+),(\d+)\)',clean)]
    if not pts:
        pts=[tuple(int(t) for t in l.split()) for l in clean.splitlines()
             if len(l.split())==3 and all(t.lstrip("-").isdigit() for t in l.split())]
    def _num(i): return int(nums[i]) if len(nums)>i and nums[i].lstrip("-").isdigit() else None
    n=_num(0); exp=_num(1)
    if n is None:
        if not pts: print("  ОТКАЗ: свидетель ПУСТОЙ — проверять нечего"); sys.exit(1)
        n=max(c for p in pts for c in p)+1
    sys.exit(0 if check(n,pts,exp) else 1)
