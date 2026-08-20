#!/bin/bash
# prove_a280537.sh — полная цепочка доказательства для одного значения:
#   кодировка -> решение -> сертификат -> НЕЗАВИСИМАЯ проверка сертификата -> проверка свидетеля
#
# ЦЕПЬ ДОВЕРИЯ, и в ней три разных звена — путать их нельзя:
#   (1) CNF правильно выражает задачу.  drat-trim этого НЕ проверяет и проверить не может.
#       Устанавливается двумя независимыми способами: slack/targets/verify_encoding.py (сравнение
#       множеств четвёрок через список плоскостей) и verify_cnf_semantics.py первого солвера
#       (сквозной прогон через решатель с assumptions).  Оба дали ноль расхождений при n = 4 и 5.
#   (2) CNF невыполним.  Это и проверяет drat-trim — чужой программой, не доверяя ни kissat, ни нам.
#   (3) свидетель на M точек действительно допустим.  Проверяется перебором ВСЕХ четвёрок
#       определителями (certs/a280537/verify_witness.py), независимо от всего остального.
# Только (1) и (2) вместе дают «a(n) <= M-1»; только (1) и (3) дают «a(n) >= M».
#
# usage: prove_a280537.sh n M [--sym]
set -eu
n=$1; M=$2; SYM=${3:-}
R="$(cd "$(dirname "$0")/../.." && pwd)"
W="${TMPDIR:-/tmp}/a280537"; mkdir -p "$W"
CNF="$W/n${n}_M${M}.cnf"; PRF="$W/n${n}_M${M}.drat"; LOG="$R/logs/a280537/proof_n${n}_M${M}.log"
mkdir -p "$(dirname "$LOG")"
{
  echo "== $(TZ=Asia/Makassar date '+%F %H:%M %Z')  n=$n M=$M ${SYM}"
  python3 "$R/slack/targets/plane4_cnf.py" "$n" "$M" "$CNF" $SYM
  t0=$(date +%s); set +e; kissat -q "$CNF" "$PRF" >"$W/sol.txt" 2>&1; rc=$?; set -e; t1=$(date +%s)
  case $rc in
    10) echo "РЕЗУЛЬТАТ: SAT за $((t1-t0))с  => a($n) >= $M"
        python3 - "$n" "$W/sol.txt" <<'PY' > "$W/wit.txt"
import re,sys
n=int(sys.argv[1]); txt=open(sys.argv[2]).read()
v=[int(t) for t in re.findall(r'-?\d+', txt.replace('v',' '))]
pts=[( (i-1)//(n*n), ((i-1)//n)%n, (i-1)%n ) for i in v if 0 < i <= n**3]
print(" ".join(f"({a},{b},{c})" for a,b,c in pts))
PY
        cat "$W/wit.txt"
        python3 "$R/certs/a280537/verify_witness.py" "$n" "$(cat "$W/wit.txt")"
        cp "$W/wit.txt" "$R/certs/a280537/sat_witness_n${n}_M${M}.txt" ;;
    20) echo "РЕЗУЛЬТАТ: UNSAT за $((t1-t0))с  => a($n) <= $((M-1))"
        ls -l "$PRF" | awk '{printf "сертификат: %.1f МБ\n", $5/1048576}'
        t2=$(date +%s); "${DRAT:-/tmp/drat-trim}" "$CNF" "$PRF" | tail -3; t3=$(date +%s)
        echo "проверка сертификата: $((t3-t2))с" ;;
    *)  echo "РЕЗУЛЬТАТ: НЕ РЕШЕНО (rc=$rc) — заявлять ничего нельзя" ;;
  esac
} 2>&1 | tee "$W/run.log"
# ЖУРНАЛ ПИШЕТСЯ ВНЕ РАБОЧЕГО ДЕРЕВА и копируется в репозиторий только по завершении.
# Причина (ловушка 10): git заменяет файл целиком — пишет временный и переименовывает, — поэтому
# дескриптор ЖИВОГО процесса повисает на осиротевшем inode, и вывод обрывается молча. Прогон при
# этом не убит: он идёт и считает верно, а по журналу выглядит застрявшим. Любой коммит во время
# счёта (а они у нас идут постоянно) обрезает журнал.
cp "$W/run.log" "$LOG"
