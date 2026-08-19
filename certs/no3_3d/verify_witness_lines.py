"""verify_witness_lines.py — независимая проверка свидетеля для трёхмерного no-three-in-line:
перебор ВСЕХ троек целочисленными векторными произведениями. Никакой связи с кодировкой и с
перечислителем: вход — только координаты.
usage: python3 verify_witness_lines.py n "(x,y,z) (x,y,z) ..."   |   --file f.txt"""
import re, sys
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
if __name__=="__main__":
    if sys.argv[1]=="--file":
        txt=open(sys.argv[2]).read(); n=int(sys.argv[3]) if len(sys.argv)>3 else None
    else:
        n=int(sys.argv[1]); txt=sys.argv[2]
    pts=[tuple(map(int,m)) for m in re.findall(r'\((\d+),(\d+),(\d+)\)',txt)]
    if n is None: n=max(c for p in pts for c in p)+1
    exp=int(sys.argv[3]) if len(sys.argv)>3 and sys.argv[3].isdigit() else None
    sys.exit(0 if check(n,pts,exp) else 1)
