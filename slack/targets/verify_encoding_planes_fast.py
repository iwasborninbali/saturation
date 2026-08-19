"""verify_encoding_planes_fast.py — полнота списка плоскостей при большом n, через ТРОЙКИ.

Прямое сравнение множеств четвёрок при n=7 стоит C(343,4) = 546 млн — неподъёмно. Но полнота
проверяется через тройки за O(C(n^3,3)):

  любая компланарная четвёрка содержит тройку; если тройка НЕ коллинеарна, она задаёт единственную
  плоскость, и четвёрка запрещена тогда и только тогда, когда эта плоскость есть в списке
  (с >= 4 узлами она там обязана быть); если же все четыре точки коллинеарны, то любая плоскость,
  содержащая эту прямую, содержит >= 4 узлов и потому в списке есть.

Поэтому достаточно: для КАЖДОЙ неколлинеарной тройки её плоскость обязана найтись в списке богатых
плоскостей — при условии, что эта плоскость несёт >= 4 узлов решётки.

usage: python3 verify_encoding_planes_fast.py n
"""
import sys
from itertools import combinations
from math import gcd
sys.path.insert(0, __file__.rsplit('/',1)[0])
from plane4_cnf import planes

def main(n):
    nc, pl = planes(n)
    cells=[(x,y,z) for x in range(n) for y in range(n) for z in range(n)]
    # канонические ключи плоскостей из списка
    keys=set()
    for m in pl:
        a,b,c = [cells[i] for i in m[:3]]
        # ищем неколлинеарную тройку внутри плоскости
        found=None
        # ИСКАТЬ ПО ВСЕЙ плоскости: первые её точки могут оказаться коллинеарными
        # (при n=7 такая плоскость есть — на этом упала первая версия проверяльщика)
        for t in combinations(m,3):
            p,q,r=[cells[i] for i in t]
            u=(q[0]-p[0],q[1]-p[1],q[2]-p[2]); v=(r[0]-p[0],r[1]-p[1],r[2]-p[2])
            nx=u[1]*v[2]-u[2]*v[1]; ny=u[2]*v[0]-u[0]*v[2]; nz=u[0]*v[1]-u[1]*v[0]
            if (nx,ny,nz)!=(0,0,0): found=(nx,ny,nz,nx*p[0]+ny*p[1]+nz*p[2]); break
        assert found, "плоскость без неколлинеарной тройки — невозможно"
        nx,ny,nz,d=found
        g=gcd(gcd(abs(nx),abs(ny)),abs(nz)); nx,ny,nz,d=nx//g,ny//g,nz//g,d//g
        if nx<0 or (nx==0 and (ny<0 or (ny==0 and nz<0))): nx,ny,nz,d=-nx,-ny,-nz,-d
        keys.add((nx,ny,nz,d))
    print(f"n={n}: богатых плоскостей {len(pl)}, различных ключей {len(keys)}")
    missing=0; checked=0; collinear=0
    for t in combinations(range(nc),3):
        p,q,r=[cells[i] for i in t]
        u=(q[0]-p[0],q[1]-p[1],q[2]-p[2]); v=(r[0]-p[0],r[1]-p[1],r[2]-p[2])
        nx=u[1]*v[2]-u[2]*v[1]; ny=u[2]*v[0]-u[0]*v[2]; nz=u[0]*v[1]-u[1]*v[0]
        if (nx,ny,nz)==(0,0,0): collinear+=1; continue
        d=nx*p[0]+ny*p[1]+nz*p[2]
        g=gcd(gcd(abs(nx),abs(ny)),abs(nz)); nx,ny,nz,d=nx//g,ny//g,nz//g,d//g
        if nx<0 or (nx==0 and (ny<0 or (ny==0 and nz<0))): nx,ny,nz,d=-nx,-ny,-nz,-d
        checked+=1
        if (nx,ny,nz,d) not in keys:
            # плоскость может нести ровно 3 узла — тогда её отсутствие законно
            cnt=sum(1 for c in cells if nx*c[0]+ny*c[1]+nz*c[2]==d)
            if cnt>=4:
                missing+=1
                if missing<=3: print(f"   ПРОПУЩЕНА плоскость {nx}x+{ny}y+{nz}z={d} с {cnt} узлами")
    print(f"  неколлинеарных троек {checked}, коллинеарных {collinear}")
    print(f"  ПРОПУЩЕННЫХ плоскостей с >=4 узлами: {missing}")
    print("  ВЕРДИКТ: список плоскостей " + ("ПОЛОН" if missing==0 else "НЕПОЛОН — ВСЕ ВЫВОДЫ НЕДЕЙСТВИТЕЛЬНЫ"))
    return 0 if missing==0 else 1

if __name__=="__main__": sys.exit(main(int(sys.argv[1])))
