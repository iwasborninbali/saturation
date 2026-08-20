#!/bin/bash
# after_sweep_second.sh — что делать, когда плоскостной перебор кончится.
#
# ЗАЧЕМ. Перебор конечен; когда он завершится, тридцать ядер замолчат. Упрямые куски
# (те, что не дались за 600 с) требуют ДРУГОГО приёма — сцепки плоскости со столбцами.
# Список упрямых собирается ИЗ ЖУРНАЛОВ, а не назначается.
#
# СТОП-ФЛАГ ОБЯЗАТЕЛЕН. Мой прошлый самопополняющийся цикл после отмены стратегии
# ВОСКРЕСИЛ её и довёл машину до нагрузки 112 при 32 ядрах. Механизм, умеющий
# восстанавливаться, обязан уметь получить приказ остановиться:
#     touch /tmp/СТОП_ПОСЛЕ_ПЕРЕБОРА     — и он не запустится.
set -u
STOP=/tmp/СТОП_ПОСЛЕ_ПЕРЕБОРА
REPO=/home/iwasborninbali/sat
PAR=${AS_PAR:-30}

while pgrep -f plane_sweep_second >/dev/null 2>&1; do
  [ -f "$STOP" ] && { echo "СТОП-ФЛАГ выставлен — выхожу, ничего не запуская"; exit 0; }
  sleep 120
done
[ -f "$STOP" ] && { echo "СТОП-ФЛАГ выставлен — выхожу"; exit 0; }

echo "=== перебор завершён $(date -u +%H:%M:%S) ==="
C=$(grep -c '^plx0_' /tmp/facts_plane.txt 2>/dev/null); C=${C:-0}
echo "закрыто плоскостных кусков: $C из 19650"
if [ "$C" -lt 19000 ]; then
  echo "ОТКАЗ: закрыто меньше 19000 — перебор оборвался, а не завершился. Упрямые собирать рано."
  exit 3
fi
cat /tmp/p42_*.log 2>/dev/null | grep -o 'plx0_[0-9-]*' | sort -u > /tmp/stubborn_final.txt
N=$(wc -l < /tmp/stubborn_final.txt)
echo "упрямых собрано: $N"
if [ "$N" -eq 0 ]; then
  echo "УПРЯМЫХ НЕТ — плоскостной перебор закрыл ВСЁ. Проверь вердиктом, это либо победа, либо ошибка сбора."
  exit 0
fi
: > /tmp/facts_hybrid.txt
mkdir -p /dev/shm/hy
for i in $(seq 0 $((PAR-1))); do
  setsid nohup env HY_BASE=/tmp/wq/base.cnf HY_OUT=/dev/shm/hy HY_FACTS=/tmp/facts_hybrid.txt HY_BUD=120 \
    python3 "$REPO/hybrid_second.py" "$i" "$PAR" /tmp/stubborn_final.txt > "/tmp/hy_$i.log" 2>&1 < /dev/null &
done
sleep 30
echo "сцепка запущена: решателей $(pgrep -c kissat), load $(cut -d' ' -f1 /proc/loadavg)"
