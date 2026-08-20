#!/bin/bash
# preflight.sh — проверка ПЕРЕД запуском работы. Ничего не советует: отказывает.
#   usage: preflight.sh <local|имя-вм> [нужно_ГБ] [нужно_ядер]
# Печатает, сколько ядер реально свободно, и возвращает 1, если запускать нельзя.
set -u
T=${1:-local}; NEEDGB=${2:-5}; NEEDCPU=${3:-1}
# режим обзора: preflight.sh all — состояние ВСЕХ машин разом, без отказа
if [ "$T" = all ]; then
  rc=0
  for m in local saturation-solver-2 saturation-solver-3; do
    "$0" "$m" "${2:-0}" "${3:-0}" || rc=1
  done
  echo
  echo "СВОДКА: суммарно свободных ядер — сумма строк выше. Прежде чем запускать новое,"
  echo "спроси: что это вытеснит, и не считает ли уже кто-то то же самое."
  exit $rc
fi
# без ассоциативных массивов: bash 3.2 на macOS их не знает
case "$T" in
  saturation-solver-2) ZONE=us-central1-b; PROJ=loyobondar-prod ;;
  saturation-solver-3) ZONE=us-west1-b;   PROJ=eg-multi-domain ;;
  local) ZONE=; PROJ= ;;
  *) echo "ОТКАЗ: неизвестная машина «$T». Известны: local, saturation-solver-2, saturation-solver-3"; exit 1 ;;
esac

# ЗАМЕР ЗАНЯТОСТИ, а не средней нагрузки. Средняя нагрузка врёт в ОБЕ стороны:
#   macOS — вверх: наблюдали 207 при семи реально занятых ядрах из восьми;
#   Linux — вниз:  у первого солвера 10.54 при двенадцати занятых из двенадцати.
# Поэтому берём долю простоя процессора напрямую.
probe () {  # печатает: cpus busy freeGB busy_kissat
  if [ "$T" = local ]; then
    # На macOS load average учитывает и ожидание ввода-вывода и НЕ сопоставим с числом ядер
    # (наблюдали 207 при семи занятых ядрах). Берём долю простоя процессора из top.
    idle=$(top -l 1 -n 0 2>/dev/null | awk -F'[ %]+' '/^CPU usage/{print $(NF-1)}')
    cpus=$(sysctl -n hw.ncpu)
    busy=$(awk -v c="$cpus" -v i="${idle:-100}" 'BEGIN{printf "%.1f", c*(100-i)/100}')
    echo "$cpus $busy $(df -g /tmp 2>/dev/null | tail -1 | awk '{print $4}') $(pgrep -x kissat | wc -l | tr -d ' ')"
  else
    timeout 60 gcloud compute ssh "$T" --zone="$ZONE" --project="$PROJ" \
      --command='echo "$(nproc) $(cut -d" " -f1 /proc/loadavg) $(df -BG /tmp|tail -1|awk "{print \$4}"|tr -d G) $(pgrep -c kissat||echo 0)"' 2>/dev/null
  fi
}
read -r CPUS LOAD FREEGB BUSY <<< "$(probe)"
[ -z "${CPUS:-}" ] && { echo "ОТКАЗ: не удалось снять состояние $T"; exit 1; }
FREECPU=$(awk -v c="$CPUS" -v l="$LOAD" 'BEGIN{printf "%d", c-l}')
echo "== $T: ядер $CPUS, загрузка $LOAD, свободно ядер ~$FREECPU, kissat $BUSY, диск ${FREEGB}ГБ"

rc=0
if [ "${FREEGB%%.*}" -lt "$NEEDGB" ]; then
  echo "  ОТКАЗ: диска ${FREEGB}ГБ < ${NEEDGB}ГБ. Генерация даст НЕПОЛНОЕ разбиение (ловушка 9)"; rc=1
fi
if [ "$FREECPU" -lt "$NEEDCPU" ]; then
  echo "  ОТКАЗ: свободных ядер ~$FREECPU < $NEEDCPU. Запуск только вытеснит уже идущее"; rc=1
fi
if [ "$BUSY" -gt "$CPUS" ]; then
  echo "  ОТКАЗ: решателей $BUSY больше, чем ядер $CPUS — машина уже перегружена"; rc=1
fi
[ $rc = 0 ] && echo "  ворота пройдены: можно запускать до $FREECPU параллельных задач"
exit $rc
