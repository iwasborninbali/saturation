#!/bin/bash
# preflight_linux.sh — версия проверки для линуксовой машины первого солвера.
# Ничего не советует: отказывает. usage: preflight_linux.sh [нужно_ГБ] [нужно_ядер] [каталог_журналов]
#
# ПОЧЕМУ НЕ load average. На Linux он честнее, чем на macOS, но всё равно считает и процессы,
# ждущие диска (состояние D), и усредняет за минуту — то есть отстаёт и завышает. Занятость
# берём из /proc/stat разностью за секунду: это доля времени, реально проведённого не в простое.
# Разница у нас наблюдалась вдвое, и запуск «по load average» дважды приводил к тому, что
# двенадцать решателей делили восемь ядер.
set -u
NEEDGB=${1:-5}; NEEDCPU=${2:-1}; LOGDIR=${3:-}
cpus=$(nproc)
read_idle () { awk '/^cpu /{idle=$5+$6; tot=0; for(i=2;i<=NF;i++) tot+=$i; print idle, tot}' /proc/stat; }
read -r i1 t1 <<< "$(read_idle)"; sleep 1; read -r i2 t2 <<< "$(read_idle)"
busy=$(awk -v i1="$i1" -v t1="$t1" -v i2="$i2" -v t2="$t2" -v c="$cpus" \
  'BEGIN{d=t2-t1; if(d<=0){print c; exit} printf "%.1f", c*(1-(i2-i1)/d)}')
freecpu=$(awk -v c="$cpus" -v b="$busy" 'BEGIN{printf "%d", c-b}')
load1=$(cut -d' ' -f1 /proc/loadavg)
freegb=$(df -BG /tmp | tail -1 | awk '{gsub("G","",$4); print $4}')
echo "== local: ядер $cpus, занято ~$busy (load1 $load1), свободно ~$freecpu, диск ${freegb}ГБ"

rc=0
[ "${freegb%%.*}" -lt "$NEEDGB" ] && { echo "  ОТКАЗ: диска ${freegb}ГБ < ${NEEDGB}ГБ — генерация даст НЕПОЛНОЕ разбиение (ловушка 9)"; rc=1; }
[ "$freecpu" -lt "$NEEDCPU" ] && { echo "  ОТКАЗ: свободно ~$freecpu ядер < $NEEDCPU — запуск лишь вытеснит идущее"; rc=1; }
# ловушка 10: журнал живого прогона не должен лежать в рабочем дереве git
if [ -n "$LOGDIR" ]; then
  if git -C "$LOGDIR" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    echo "  ОТКАЗ: каталог журналов «$LOGDIR» внутри рабочего дерева git — любой checkout/rebase/stash"
    echo "         осиротит дескриптор живого процесса, и его вывод исчезнет молча (ловушка 10)"; rc=1
  fi
fi
# сколько уже идёт нашего счёта — чтобы не удваивать вслепую
mine=$(pgrep -c -f 'symmetric_search|maximize_witness|no4_search|no4_count|cross_solver' 2>/dev/null || echo 0)
echo "  уже идёт наших процессов: $mine"
[ $rc -eq 0 ] && echo "  ПРОПУСК: запускать можно"
exit $rc
