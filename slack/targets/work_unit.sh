#!/bin/bash
# work_unit.sh — один кусок фронта, восстановленный ИЗ ИМЕНИ.
#
# Существует потому, что рекурсия в sos_second.sh строго последовательна: цикл по 64 детям
# вызывает себя и ЖДЁТ. Одна цепочка занимает ровно одно ядро, сколько бы их ни было. На
# 32-ядерной машине шли три цепочки — 87 процессов в списке, из них решают два, load 3.9.
# Восемьдесят четыре процесса были предками, ждущими своих детей.
#
# Чинить веер параллельным запуском 64 детей нельзя: каждый ребёнок дробится снова, и число
# процессов растёт как 64^глубина. Вместо этого работа выпрямляется в ОЧЕРЕДЬ независимых
# кусков, а параллелизмом управляет xargs -P снаружи. Внутри куска рекурсия остаётся
# последовательной — она уже проверена, и трогать её незачем.
#
# Кусок восстанавливается из имени: case_XXXXX_sA_sB_... — это столбец 0 с подмножеством
# XXXXX, столбец 1 с подмножеством A, столбец 2 с B и так далее. Значит любой узел дерева
# получается из базовой формулы дописыванием единичных дизъюнктов, и хранить промежуточные
# файлы не нужно вовсе.
set -u
NAME="$1"; BASE="${WU_BASE:-/tmp/wq/base.cnf}"; OUT="${WU_OUT:-/tmp/wq/run}"
FACTS="${WU_FACTS:-/tmp/facts_vm.txt}"; NN="${WU_N:-7}"; LIM="${WU_LIM:-120}"
mkdir -p "$OUT"
f="$OUT/$NAME.cnf"
python3 - "$BASE" "$NAME" "$f" "$NN" <<'PY'
import sys, os
from itertools import combinations
base, name, dst, n = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
SUBS=[s for k in range(4) for s in combinations(range(n),k)]
toks=[int(name.split("_")[1])]+[int(t) for t in name.split("_s")[1:]]
raw=open(base,"rb").read(); i=raw.index(b"p cnf"); nl=raw.index(b"\n",i)
h=raw[i:nl].split(); body=raw[nl+1:]
units=[]
for col,ti in enumerate(toks):
    x,y=col//n,col%n
    sub=SUBS[ti]
    units += [((x*n+y)*n+z)+1 if z in sub else -(((x*n+y)*n+z)+1) for z in range(n)]
head=b"p cnf %s %d\n"%(h[2],int(h[3])+len(units))
tail=b"".join(b"%d 0\n"%v for v in units)
open(dst,"wb").write(head+body+tail)
# ЦЕЛОСТНОСТЬ ПРОВЕРЯЕТСЯ СРАЗУ. Оборванный файл решатель возвращает как rc=1, и в журнале
# эта строка неотличима от результата — именно так были потеряны 280 фактов.
assert os.path.getsize(dst)==len(head)+len(body)+len(tail), f"ОБОРВАН {dst}"
PY
if [ ! -s "$f" ]; then echo "ОТКАЗ $NAME: формулу собрать не удалось"; exit 2; fi
ci=$(python3 -c "print('$NAME'.count('_s')+1)")
"${WU_REPO:-$HOME/sat}/sos_second.sh" "$f" "$ci" "$LIM" $((NN*NN)) "$FACTS" "$NN"
rc=$?
rm -f "$f"
exit $rc
