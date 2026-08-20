#!/bin/bash
# sos_named.sh — рекурсия ПО ИМЕНАМ, без материализации дробления.
#
# ЗАЧЕМ. Прежний ход дробил узел, записывая 64 файла по 54 МБ — 3.5 ГБ на КАЖДЫЙ разбитый
# узел. Замер на живой машине при 24 работниках: ожидание диска 37-45%, полезный счёт 27%,
# 19 процессов в состоянии D, запись 230 МБ/с непрерывно. То есть половина машины ждала диск,
# и добавление ядер добавило бы только ждущих. Просить у Google ядра в таком состоянии
# бессмысленно: узкое место не там.
#
# ПОЧЕМУ ФАЙЛЫ НЕ НУЖНЫ. Любой узел восстанавливается из ИМЕНИ: case_XXXXX_sA_sB_... это
# столбец 0 с подмножеством XXXXX, столбец 1 с A, столбец 2 с B. Значит ребёнок — это базовая
# формула плюс единичные дизъюнкты, и хранить его незачем: достаточно передать имя.
# Восстановление сверено побайтово (cmp) с файлом, сохранённым прошлым прогоном, ДО того как
# на него положились. Без этой сверки факты пошли бы под чужими именами.
#
# Пик на работника: 54 МБ вместо 3.5 ГБ. Это влезает в оперативную память, поэтому файлы
# кладутся на tmpfs и диска не касаются вовсе.
#
#   sos_named.sh <имя-узла> [лимит-с]
set -u
NAME="$1"; LIM="${2:-${SN_LIM:-120}}"
BASE="${SN_BASE:-/tmp/wq/base.cnf}"; RUN="${SN_RUN:-/dev/shm/wq}"
FACTS="${SN_FACTS:-/tmp/facts_vm.txt}"; NN="${SN_N:-7}"
NSUB=64                      # sum_{k<=3} C(7,k)
mkdir -p "$RUN"

ci=$(( $(echo "$NAME" | grep -o '_s' | wc -l) + 1 ))
if [ "$ci" -ge $((NN*NN)) ]; then echo "ПРЕДЕЛ $NAME (расписание исчерпано на шаге $ci)"; exit 1; fi

# ПЛОТНОСТЬ. Порог берётся из ворот (передан в окружении), ВЕРХНЯЯ ГРАНИЦА обязательна:
# у цепочки пустых подмножеств d = 19/(49-k) РАСТЁТ с глубиной, и без потолка предсказатель
# объявляет её трудной на каждом шаге и дробит до дна вместо мгновенного закрытия.
# Выше 3/7 кусок невыполним по чистому счёту — замерено: 0.33 с, rc=20, поиск не начинается.
DENS=$(python3 - "$NAME" "$NN" <<'PYD'
import sys
from itertools import combinations
name,n=sys.argv[1],int(sys.argv[2])
S=[x for k in range(4) for x in combinations(range(n),k)]
toks=[int(name.split("_")[1])]+[int(t) for t in name.split("_s")[1:]]
p=sum(len(S[i]) for i in toks); k=len(toks)
rc=n*n-k
print(f"{(19-p)/rc:.4f}" if rc>0 else "0")
PYD
)
rc=""
if [ -n "${SOS_DENS:-}" ] && [ "${SOS_DENS:-НЕТ}" != "НЕТ" ]; then
  if python3 -c "import sys; d=float('$DENS'); sys.exit(0 if d>=float('$SOS_DENS') and d<=float('${CEIL:-0.4286}') else 1)" 2>/dev/null; then
    rc=99
  fi
fi

f="$RUN/$NAME.cnf"
if [ -z "$rc" ]; then
  python3 - "$BASE" "$NAME" "$f" "$NN" <<'PY'
import sys, os
from itertools import combinations
base,name,dst,n=sys.argv[1],sys.argv[2],sys.argv[3],int(sys.argv[4])
SUBS=[s for k in range(4) for s in combinations(range(n),k)]
toks=[int(name.split("_")[1])]+[int(t) for t in name.split("_s")[1:]]
raw=open(base,"rb").read(); i=raw.index(b"p cnf"); nl=raw.index(b"\n",i)
h=raw[i:nl].split(); body=raw[nl+1:]
units=[]
for col,ti in enumerate(toks):
    x,y=col//n,col%n; sub=SUBS[ti]
    units+=[((x*n+y)*n+z)+1 if z in sub else -(((x*n+y)*n+z)+1) for z in range(n)]
head=b"p cnf %s %d\n"%(h[2],int(h[3])+len(units))
tail=b"".join(b"%d 0\n"%v for v in units)
open(dst,"wb").write(head+body+tail)
# ОБОРВАННЫЙ ФАЙЛ РЕШАТЕЛЬ ВОЗВРАЩАЕТ КАК rc=1, и в журнале это неотличимо от результата.
assert os.path.getsize(dst)==len(head)+len(body)+len(tail), f"ОБОРВАН {dst}"
PY
  if [ ! -s "$f" ]; then echo "ОТКАЗ $NAME: формулу собрать не удалось"; exit 2; fi
  timeout "$LIM" kissat -q "$f" >/dev/null 2>&1; rc=$?
  rm -f "$f"
fi

case $rc in
  20) echo "$NAME" >> "$FACTS"; echo "ЗАКРЫТ $NAME"; exit 0 ;;
  10) echo "ВЫПОЛНИМ $NAME — УТВЕРЖДЕНИЕ РУШИТСЯ"; echo "$NAME" >> "${FACTS}.SAT"; exit 9 ;;
  1)  echo "ОТКАЗ $NAME: решатель не разобрал файл (rc=1) — кусок НЕ решён"; exit 2 ;;
esac

# Уцелел (или пропущен по плотности) — дробим ИМЕНАМИ. Ни одного файла не создаётся.
bad=0
for ((j=0;j<NSUB;j++)); do
  printf -v ch "%s_s%03d" "$NAME" "$j"
  "$0" "$ch" "$LIM" || bad=1
done
# ФАКТ — ТОЛЬКО СОБСТВЕННЫЙ UNSAT. Узел, закрытый через детей, сюда НЕ пишется: файл фактов
# документирован как атомарный, а вердикт выводит закрытие родителя из детей сам. Смешать
# измеренное с выведенным значит потерять возможность их различить — и лишиться права
# пересчитать вердикт заново, если разбиение окажется неполным.
[ "$bad" -eq 0 ] && { echo "ЗАКРЫТ ЧЕРЕЗ ДЕТЕЙ $NAME"; exit 0; }
exit 1
