#!/bin/bash
# dispatch.sh — запуск работы с параллелизмом, который определяют ВОРОТА, а не вызывающий.
#
# Существует потому, что ворота, которые только сообщают, не работают: я вызвал preflight.sh,
# получил «можно до 5 задач» и через минуту запустил 10. Дисциплина, которую можно нарушить, —
# не дисциплина. Здесь число параллельных задач берётся из ворот и подставляется в xargs
# автоматически; задать его вручную нельзя.
#
#   usage: dispatch.sh <local|машина> <файл-со-списком-задач> <файл-результатов> [лимит_сек] [нужно_ГБ]
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
T=$1; TASKS=$2; OUT=$3; LIM=${4:-3600}; NEEDGB=${5:-3}

[ -s "$TASKS" ] || { echo "ОТКАЗ: список задач $TASKS пуст или отсутствует"; exit 1; }
N=$(grep -c . "$TASKS")

# ворота: они же и решают, сколько можно
INFO=$("$HERE/preflight.sh" "$T" "$NEEDGB" 1) || { echo "$INFO"; echo "ОТКАЗ: ворота не пропустили запуск"; exit 1; }
echo "$INFO"
P=$(echo "$INFO" | sed -n 's/.*можно запускать до \([0-9]*\) .*/\1/p')
[ -z "$P" ] && { echo "ОТКАЗ: не удалось получить допустимый параллелизм из ворот"; exit 1; }
[ "$P" -lt 1 ] && { echo "ОТКАЗ: допустимый параллелизм $P"; exit 1; }

echo "== задач $N, параллелизм задан воротами: $P (вручную не переопределяется)"
if [ "$T" = local ]; then
  ( LIM=$LIM xargs -P "$P" -I{} "$HERE/../../slack/gates/runcase.sh" {} "$OUT" < "$TASKS"; echo ALLDONE >> "$OUT" ) &
  echo "запущено в фоне, результаты в $OUT"
else
  case "$T" in
    saturation-solver-2) Z=us-central1-b; PR=loyobondar-prod ;;
    saturation-solver-3) Z=us-west1-b;    PR=eg-multi-domain ;;
    *) echo "ОТКАЗ: неизвестная машина $T"; exit 1 ;;
  esac
  gcloud compute ssh "$T" --zone="$Z" --project="$PR" --command="setsid nohup bash -c 'LIM=$LIM xargs -P $P -I{} ~/sat/runcase.sh {} $OUT < $TASKS; echo ALLDONE >> $OUT' >/dev/null 2>&1 </dev/null &" 2>/dev/null
  echo "запущено на $T в фоне, результаты в $OUT"
fi
