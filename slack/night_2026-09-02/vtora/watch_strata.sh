#!/bin/zsh
# watch_strata.sh — независимая проверка свидетелей куба A399138 (ночь 2→3.09.2026, втора).
# Каждые 5 минут зеркалит ~/strata с ВМ saturation-alg-1 в strata_mirror/, каждый НОВЫЙ файл
# n<N>_c<страта>_<точек>.txt прогоняет через certs/no3_3d/verify_witness_lines.py (перебор всех троек
# векторными произведениями; cube_strata.py не читается) и пишет строку в verify.log.
# Печатает строку только на событие: новый свидетель (с пометкой, если выше известного 73/93) или
# смена состояния связи с ВМ.  Лёгкий: scp + проверка ≤ 100 точек.
export CLOUDSDK_CORE_ACCOUNT=saturation-agent@loyobondar-prod.iam.gserviceaccount.com
export CLOUDSDK_CORE_PROJECT=loyobondar-prod
ROOT=/Users/iwasborninbali/saturation
MIR=$ROOT/slack/night_2026-09-02/vtora/strata_mirror
LOG=$ROOT/slack/night_2026-09-02/vtora/verify.log
mkdir -p "$MIR"; touch "$LOG"
link=ok
while true; do
  if gcloud compute scp --zone us-east4-b --quiet --recurse 'saturation-alg-1:~/strata/*' "$MIR/" >/dev/null 2>&1; then
    [ "$link" = down ] && echo "связь с ВМ восстановлена $(date -u +%FT%TZ)"; link=ok
  else
    [ "$link" = ok ] && echo "scp с ВМ не прошёл $(date -u +%FT%TZ) (ВМ снесена или сеть)"; link=down
  fi
  for f in "$MIR"/n*_c*_*.txt; do
    [ -e "$f" ] || continue
    base=$(basename "$f")
    grep -q "^$base " "$LOG" 2>/dev/null && continue
    n=$(echo "$base" | sed -E 's/^n([0-9]+)_.*/\1/')
    pts=$(echo "$base" | sed -E 's/.*_([0-9]+)\.txt$/\1/')
    res=$(python3 "$ROOT/certs/no3_3d/verify_witness_lines.py" "$n" "$f" "$pts" 2>&1 | tail -1 | sed 's/^ *//')
    # жёсткость: min κ (число пар, коллинеарных с пустой клеткой) и число заменяемых точек — rigidity_kappa.py (лемма: жёстко ⟺ min κ ≥ 2)
    kap=$(python3 "$ROOT/slack/night_2026-09-02/vtora/rigidity_kappa.py" cube "$f" 2>&1 | tail -1 | sed -E 's/.*(min κ=[0-9]+).*нежёстких точек ([0-9]+\/[0-9]+).*/\1, заменяемых \2/')
    # исчерпывающий обмен радиуса ≤ 3 (exchange_search.py): улучшаем ли стратный оптимум перестановкой ≤ 3 точек вне страты
    J=3; [ "$n" -ge 11 ] 2>/dev/null && J=2      # при n ≥ 11 радиус 3 стоит ~10 мин на файл — монитор не успевал бы
    exch=$(python3 "$ROOT/slack/night_2026-09-02/vtora/exchange_search.py" $J "$f" 2>&1 | grep -q "УЛУЧШЕНИЕ" && echo "обмен ≤$J: УЛУЧШЕНИЕ НАЙДЕНО" || echo "обмен ≤$J: нет")
    echo "$base $(date -u +%FT%TZ) $res | $kap | $exch" >> "$LOG"
    case "$n" in 7) thr=73;; 8) thr=94;; 9) thr=116;; *) thr=0;; esac
    flag=""; if [ "$n" -ge 10 ] 2>/dev/null; then flag="  (n=$n: свидетелей не было — любой чистый файл есть первая нижняя граница a($n))"; elif [ "$pts" -gt "$thr" ] 2>/dev/null; then flag="  !!! ВЫШЕ ИЗВЕСТНОГО ($thr) — кандидат в A399138"; fi
    case "$exch" in *НАЙДЕНО*) flag="$flag  !!! обмен ≤3 даёт больше точек — смотреть exchange_search.py";; esac
    echo "новый свидетель $base: $res | $kap | $exch$flag"
  done
  sleep 300
done
