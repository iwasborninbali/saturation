#!/bin/zsh
setopt null_glob   # пустое зеркало не должно валить цикл (zsh: «no matches found»)
# watch_strata_p.sh — независимая проверка стратных свидетелей A280537 (нет четырёх компланарных) с ВМ (~/strata_p), 3.09.2026, втора.
# Каждые 5 минут: scp ~/strata_p/* → strata_p_mirror/; каждый новый n<N>_c<..>_<m>.txt: certs/a280537/verify_witness.py N файл m
# (определители на четвёрках), затем rigid_check_a280537.py (прямой счёт оживления: лемма о κ здесь не работает). Печатает строку на событие.
export CLOUDSDK_CORE_ACCOUNT=saturation-agent@loyobondar-prod.iam.gserviceaccount.com
export CLOUDSDK_CORE_PROJECT=loyobondar-prod
ROOT=/Users/iwasborninbali/saturation
MIR=$ROOT/slack/night_2026-09-02/vtora/strata_p_mirror
MIRL=$ROOT/slack/night_2026-09-02/vtora/strata_p_long_mirror   # второй проход коллеги (~/strata_p_long, по часу на страту)
LOG=$ROOT/slack/night_2026-09-02/vtora/verify_p.log
mkdir -p "$MIR" "$MIRL"; touch "$LOG"
link=ok
while true; do
  if gcloud compute scp --zone us-east4-b --quiet --recurse 'saturation-alg-1:~/strata_p/*' "$MIR/" >/dev/null 2>&1; then
    [ "$link" = down ] && echo "связь с ВМ восстановлена $(date -u +%FT%TZ)"; link=ok
  else
    [ "$link" = ok ] && echo "scp ~/strata_p с ВМ не прошёл $(date -u +%FT%TZ) (каталога ещё нет, ВМ снесена или сеть)"; link=down
  fi
  gcloud compute scp --zone us-east4-b --quiet --recurse 'saturation-alg-1:~/strata_p_long/*' "$MIRL/" >/dev/null 2>&1
  for f in "$MIR"/n*_c*_*.txt "$MIRL"/n*_c*_*.txt; do
    [ -e "$f" ] || continue
    base=$(basename "$f"); tagdir=""; [ "$(dirname "$f")" = "$MIRL" ] && tagdir="long/"
    grep -q "^$tagdir$base " "$LOG" 2>/dev/null && continue
    n=$(echo "$base" | sed -E 's/^n([0-9]+)_.*/\1/')
    pts=$(echo "$base" | sed -E 's/.*_([0-9]+)\.txt$/\1/')
    res=$(python3 "$ROOT/certs/a280537/verify_witness.py" "$n" "$f" "$pts" 2>&1 | tail -1 | sed 's/^ *//')
    rig=$(python3 "$ROOT/slack/night_2026-09-02/vtora/rigid_check_a280537.py" "$f" 2>&1 | tail -1 | sed -E 's/^[^:]*: //')
    echo "$tagdir$base $(date -u +%FT%TZ) $res | $rig" >> "$LOG"
    case "$n" in 5) thr=13;; 6) thr=16;; 7) thr=18;; 8) thr=20;; 9) thr=23;; 10) thr=26;; 11) thr=28;; 12) thr=31;; *) thr=0;; esac
      tag=""; [ "$thr" -gt 0 ] 2>/dev/null && [ "$pts" -gt "$thr" ] 2>/dev/null && tag=" !!! РЕКОРД: больше лучшего известного $thr"
      [ "$thr" -gt 0 ] 2>/dev/null && [ "$pts" -eq "$thr" ] 2>/dev/null && tag=" — равен лучшему известному ($thr): проверить класс эквивалентности"
      cls=""; [ "$thr" -gt 0 ] 2>/dev/null && [ "$pts" -ge "$thr" ] 2>/dev/null && cls=" | $(python3 "$ROOT/slack/night_2026-09-02/vtora/class_check_a280537.py" "$f" 2>&1 | tail -1)"
      [ "$pts" -ge 10 ] 2>/dev/null && echo "A280537 новый свидетель $tagdir$base: $res | $rig$tag$cls"   # мелкие стратные конфигурации только в журнал
  done
  sleep 300
done
