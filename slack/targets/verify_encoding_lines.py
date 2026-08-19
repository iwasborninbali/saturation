"""verify_encoding_lines.py — доказательство семантики линейной кодировки СРАВНЕНИЕМ МНОЖЕСТВ.

Вопрос: запрещает ли ограничение «в каждой богатой прямой не более двух точек» ровно те же тройки,
что прямой критерий коллинеарности векторным произведением? Строятся оба множества целиком и
сравниваются; никаких выборок.

Проверять обязательно при ТОМ ЖЕ n, для которого делается заявление: кодировка, верная при n=5,
не обязана быть верной при n=6 (например, если перечисление прямых теряет направления, появляющиеся
только в большей решётке).

usage: python3 verify_encoding_lines.py n
"""
import sys
from itertools import combinations
sys.path.insert(0, __file__.rsplit('/',1)[0])
from no3_3d_cnf import lines

def main(n):
    nc, ln = lines(n)
    cells=[(x,y,z) for x in range(n) for y in range(n) for z in range(n)]
    by_lines=set()
    for m in ln:
        for t in combinations(sorted(m),3): by_lines.add(t)
    def cr(a,b,c):
        u=[b[i]-a[i] for i in range(3)];v=[c[i]-a[i] for i in range(3)]
        return (u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0])
    by_cross=set()
    for t in combinations(range(nc),3):
        if cr(*[cells[i] for i in t])==(0,0,0): by_cross.add(t)
    only_l=by_lines-by_cross; only_c=by_cross-by_lines
    print(f"n={n}: всего троек {nc*(nc-1)*(nc-2)//6}, богатых прямых {len(ln)}")
    print(f"  запрещено прямыми: {len(by_lines)}")
    print(f"  коллинеарно по векторному произведению: {len(by_cross)}")
    print(f"  только прямыми (лишние запреты): {len(only_l)}" + (f"  пример {sorted(only_l)[0]}" if only_l else ""))
    print(f"  только произведением (ПРОПУЩЕННЫЕ): {len(only_c)}" + (f"  пример {sorted(only_c)[0]}" if only_c else ""))
    ok = not only_l and not only_c
    print("  ВЕРДИКТ: множества " + ("СОВПАДАЮТ — семантика кодировки доказана" if ok else "РАЗЛИЧАЮТСЯ — КОДИРОВКА НЕВЕРНА"))
    return 0 if ok else 1
if __name__=="__main__": sys.exit(main(int(sys.argv[1])))
