"""progress_measure.py — МЕРА ПРОДВИЖЕНИЯ, а не активности.

Число закрытий растёт всегда, пока машина включена, и потому ничего не говорит о том,
приближаемся ли мы. Нужна величина, которая МОЖЕТ не улучшаться.

Узел с k зафиксированными столбцами занимает долю 64^-k пространства поиска (64 = число
подмножеств размера <=3 из 7). Отсюда:
  * ДРОБЛЕНИЕ СОХРАНЯЕТ меру: кусок веса w даёт 64 ребёнка по w/64, сумма та же;
  * ЗАКРЫТИЕ строго уменьшает: вес закрытого узла уходит навсегда.
Значит сумма весов открытого фронта монотонно НЕ РАСТЁТ и обязана дойти до нуля.
Это честная мера: она не поощряет суету и не может быть улучшена дроблением.

ЧЕГО ОНА НЕ ЗНАЕТ. Она считает все поддеревья одинаково трудными, а они не одинаковы:
оставшийся кусок может стоить больше, чем весь пройденный путь. Поэтому линейная
экстраполяция срока — оценка снизу по трудности, а не обещание. Говорить «осталось X часов»
на её основании нельзя; говорить «разобрано столько-то пространства» — можно.

usage: progress_measure.py <файлы-фактов...>
"""
import sys
from collections import defaultdict

NSUB = 64
closed = set()
children = defaultdict(set)
for fp in sys.argv[1:]:
    try: fh = open(fp, encoding="utf-8")
    except OSError:
        print(f"  ВНИМАНИЕ: {fp} не открылся — мера будет ЗАВЫШЕНА (открытого покажется больше)")
        continue
    for l in fh:
        l = l.strip()
        if not l.startswith("case_"): continue
        closed.add(l)
        if "_s" in l:
            par, idx = l.rsplit("_s", 1)
            children[par].add(int(idx))

def depth(nm):        # число зафиксированных столбцов
    return nm.count("_s") + 1

# Открытый фронт: ребёнок разбитого узла без собственного закрытия и без своих детей,
# плюс верхнеуровневые куски, за которые вообще не брались.
open_nodes = []
for i in range(NSUB):
    nm = f"case_{i:05d}"
    if nm in closed: continue
    if nm not in children or not children[nm]:
        open_nodes.append(nm)
for p, got in children.items():
    if p in closed or not got: continue
    for j in range(NSUB):
        if j in got: continue
        ch = f"{p}_s{j:03d}"
        if ch in closed: continue
        if ch in children and children[ch]: continue
        open_nodes.append(ch)

mera = sum(NSUB ** (-depth(nm)) for nm in open_nodes)
by_depth = defaultdict(float)
for nm in open_nodes: by_depth[depth(nm)] += NSUB ** (-depth(nm))

print(f"открытых узлов: {len(open_nodes)}")
print(f"ДОЛЯ ПРОСТРАНСТВА, ЕЩЁ НЕ РАЗОБРАННАЯ: {mera:.12f}")
print(f"РАЗОБРАНО: {(1-mera)*100:.9f}%")
print("вклад по глубинам (только весомые):")
for d in sorted(by_depth):
    if by_depth[d] >= mera * 0.01:
        print(f"  глубина {d:2d}: {by_depth[d]:.12f}  ({by_depth[d]/mera*100:5.1f}% остатка)")
