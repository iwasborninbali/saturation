#!/bin/bash
# watch_family.sh — certify every BOOK line produced by family sweeps (kit71/bench/*_sym*_n*.txt), record, commit, push.
cd "$(dirname "$0")/.."
touch kit71/results/certified_lines.txt
while true; do
  for f in kit71/bench/family3_sym*_n*.txt kit71/bench/mixed_*_sym*_n*.txt; do
    [ -f "$f" ] || continue
    n=$(echo "$f" | sed -n 's/.*_n\([0-9]*\)\.txt/\1/p'); sym=$(echo "$f" | sed -n 's/.*_sym\([0-9]*\)_n.*/\1/p')
    grep '^BOOK' "$f" | while read -r line; do
      key=$(echo "$line" | md5sum | cut -c1-16)
      grep -q "$key" kit71/results/certified_lines.txt && continue
      pairs=$(echo "$line" | awk '{print $2}'); toks=$(echo "$line" | sed 's/^BOOK [^ ]* sol //')
      res=$(python3 kit71/certify_book.py $n "$toks" "linux-12c: there_tw sym$sym PAIRS=$pairs, exhaustive sub-class, $(date -u +%FT%TZ)") || continue
      cls=$(echo "$res" | sed -n 's/^class=\([a-z0-9]*\) .*/\1/p'); enc=$(echo "$res" | sed -n 's/^encoded: //p'); fresh=$(echo "$res" | sed -n 's/.*fresh=\([A-Za-z]*\).*/\1/p')
      echo "$key $n $sym $pairs $cls $enc" >> kit71/results/certified_lines.txt
      if [ "$fresh" = "True" ]; then
        git pull -q --rebase --autostash origin main
        printf '| %s | %s | `%s` | linux-12c, there_tw sym%s PAIRS=%s (odd-cycle defect family), exhaustive sub-class |\n' "$n" "$cls" "$enc" "$sym" "$pairs" >> docs/SUBMISSION.md
        git add docs/SUBMISSION.md kit71/results/books_family.json kit71/results/certified_lines.txt
        git -c user.name="solver-kit71 (Claude, linux-12c)" -c user.email="claude@nusadua.dev" commit -q -m "family sweep: n=$n class $cls book (sym$sym PAIRS=$pairs)" && git push -q origin main
      fi
    done
  done
  sleep 60
done
