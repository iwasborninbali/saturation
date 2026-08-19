"""verify_encoding.py — доказательство СЕМАНТИКИ кодировки, а не её работоспособности.

Вопрос: действительно ли «в каждой плоскости с >= 4 узлами не более трёх точек» запрещает РОВНО те же
четвёрки, что прямой критерий компланарности определителем? Если да — SAT-кодировке можно верить,
и все три наши реализации решают одну задачу, а не три похожие.

Метод: построить оба множества четвёрок целиком и сравнить как множества. Никаких выборок.
usage: python3 verify_encoding.py n
"""
import sys
from itertools import combinations
sys.path.insert(0, __file__.rsplit('/',1)[0])
from plane4_cnf import planes

def det3(a,b,c,d):
    u=[b[i]-a[i] for i in range(3)];v=[c[i]-a[i] for i in range(3)];w=[d[i]-a[i] for i in range(3)]
    return u[0]*(v[1]*w[2]-v[2]*w[1])-u[1]*(v[0]*w[2]-v[2]*w[0])+u[2]*(v[0]*w[1]-v[1]*w[0])

def main(n):
    nc, pl = planes(n)
    cells=[(x,y,z) for x in range(n) for y in range(n) for z in range(n)]
    by_planes=set()
    for m in pl:
        for q in combinations(sorted(m),4): by_planes.add(q)
    by_det=set()
    for q in combinations(range(nc),4):
        if det3(*[cells[i] for i in q])==0: by_det.add(q)
    only_p=by_planes-by_det; only_d=by_det-by_planes
    print(f"n={n}: всего четвёрок {nc*(nc-1)*(nc-2)*(nc-3)//24}")
    print(f"  запрещено плоскостями: {len(by_planes)}")
    print(f"  компланарно по определителю: {len(by_det)}")
    print(f"  только плоскостями (лишние запреты): {len(only_p)}" + (f"  пример {sorted(only_p)[0]}" if only_p else ""))
    print(f"  только определителем (ПРОПУЩЕННЫЕ запреты): {len(only_d)}" + (f"  пример {sorted(only_d)[0]}" if only_d else ""))
    ok = not only_p and not only_d
    print("  ВЕРДИКТ: множества " + ("СОВПАДАЮТ — семантика кодировки доказана" if ok else "РАЗЛИЧАЮТСЯ — кодировка неверна"))
    return 0 if ok else 1

if __name__=="__main__": sys.exit(main(int(sys.argv[1])))
