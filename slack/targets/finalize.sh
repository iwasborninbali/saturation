#!/bin/bash
# finalize.sh — окончательная сверка перед ЛЮБЫМ заявлением о значении.
# Собирает результаты со всех машин, строит ожидаемое множество независимо (из манифеста),
# и печатает вердикт. Отдельно проверяет свидетеля на нижнюю границу.
#   usage: finalize.sh <no3|no4> <n> <M_unsat> <manifest_dir> <результаты...>
# Заявлять a(n) = M_unsat-1 можно ТОЛЬКО если: (1) вердикт «покрытие полное, все UNSAT»
# и (2) свидетель на M_unsat-1 точек прошёл независимую проверку.
set -eu
kind=$1; n=$2; M=$3; mdir=$4; shift 4
R="$(cd "$(dirname "$0")/../.." && pwd)"
cat "$@" > /tmp/_all_results.txt
echo "== $(TZ=Asia/Makassar date '+%F %H:%M %Z')  $kind n=$n, решающее M=$M"
echo "-- покрытие:"
python3 "$R/slack/targets/check_split.py" "$mdir" /tmp/_all_results.txt || true
echo "-- свидетель на $((M-1)) точек:"
w="$R/certs/${kind}_3d/sat_witness_n${n}_$((M-1)).txt"
[ "$kind" = no4 ] && w="$R/certs/a280537/sat_witness_n${n}_$((M-1)).txt"
if [ -f "$w" ]; then
  python3 "$R/certs/no3_3d/verify_witness_lines.py" "$n" "$(cat "$w")" 2>/dev/null \
    || python3 "$R/certs/a280537/verify_witness.py" "$n" "$(cat "$w")"
else
  echo "   СВИДЕТЕЛЯ НЕТ — нижняя граница не подтверждена, заявлять нельзя"
fi
