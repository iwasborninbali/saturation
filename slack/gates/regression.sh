#!/bin/bash
# regression.sh — сверка СУММОЙ после любого изменения генератора или разбиения.
#
# Приём первого солвера, и он себя оправдал дважды подряд за час: при верной переделке ядра
# подтвердил правильность, при переделке, оказавшейся замедлением, — тоже (ошибки не было, но
# если бы была, поймал бы). Проверка, которую можно прогнать за минуту после каждого изменения,
# стоит дороже любого рассуждения о корректности.
#
# Что проверяется: все конфигурации из 10 точек в [4]^3 без четырёх компланарных должны
# раскладываться по 100 парам профилей БЕЗ потерь и БЕЗ двойного счёта, и их должно быть 10960
# (число независимо опубликовано Эдом Пеггом в 2014 году как 232 класса под 48 симметриями).
set -u
R="$(cd "$(dirname "$0")/../.." && pwd)"
echo "== регрессия: сумма по парам профилей при n=4, M=10 (эталон 10960 помеченных / 232 класса)"
[ -s /tmp/sols_4.txt ] || { echo "  нет /tmp/sols_4.txt — сгенерировать: COUNT=10 PRINTSOL=1 plane4count 4 0"; exit 1; }
python3 - "$R" <<'PY'
import sys
from itertools import product
from collections import Counter
n, M = 4, 10
profs = [c for c in product(range(4), repeat=n) if sum(c) == M]
pairs = {(a, b) for a in profs for b in profs}
sols = [[int(t) for t in l.split()] for l in open('/tmp/sols_4.txt') if l.strip()]
buckets, outside = Counter(), 0
for S in sols:
    px = Counter(i//(n*n) for i in S); py = Counter((i//n) % n for i in S)
    key = (tuple(px.get(t,0) for t in range(n)), tuple(py.get(t,0) for t in range(n)))
    if key in pairs: buckets[key] += 1
    else: outside += 1
ok = (len(sols) == 10960) and outside == 0 and sum(buckets.values()) == len(sols)
print(f"  конфигураций {len(sols)} (эталон 10960); вне пар {outside}; сумма по парам {sum(buckets.values())}")
print("  ВЕРДИКТ: " + ("регрессия пройдена" if ok else "РЕГРЕССИЯ ПРОВАЛЕНА — разбиение или генератор сломаны"))
sys.exit(0 if ok else 1)
PY
