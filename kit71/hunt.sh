#!/bin/bash
# hunt.sh n sym seeds secs [order] [value] — parallel seeds of ./there (n<=64) or ./there128 in the exact class sym.
# On a book: saturation.certify + web/stab.py (via kit71/certify_book.py), append to docs/SUBMISSION.md, commit + push.
cd "$(dirname "$0")/.."
n=$1; sym=$2; seeds=${3:-12}; secs=${4:-40000}; order=${5:-0}; value=${6:-0}
bin=./there; [ $n -gt 64 ] && bin=./there128
out=kit71/bench/hunt_n${n}_sym${sym}.txt
echo "# $(date -u +%FT%TZ) $bin $n $sym <seed> $secs 2000 $order $value  x $seeds seeds (linux-12c)" >> $out
for s in $(seq 1 $seeds); do echo "$s"; done | xargs -P $seeds -I{} sh -c "$bin $n $sym {} $secs 2000 $order $value" > $out.raw
grep -v '^book' $out.raw | sed 's/ : .*//' >> $out
grep '^book' $out.raw | while read -r line; do
  toks=$(echo "$line" | sed 's/.* : //'); head=$(echo "$line" | sed 's/ : .*//')
  echo "$head" >> $out
  res=$(python3 kit71/certify_book.py $n "$toks" "linux-12c: $head")
  echo "$res" | sed 's/^/#   /' >> $out
  cls=$(echo "$res" | sed -n 's/^class=\([a-z0-9]*\) .*/\1/p'); enc=$(echo "$res" | sed -n 's/^encoded: //p')
  git pull -q --rebase origin main
  printf '| %s | %s | `%s` | linux-12c, %s |\n' "$n" "$cls" "$enc" "$head" >> docs/SUBMISSION.md
  git add docs/SUBMISSION.md kit71/results/books_family.json $out
  git -c user.name="solver-kit71 (Claude, linux-12c)" -c user.email="claude@nusadua.dev" commit -q -m "hunt: n=$n class $cls book ($head)" && git push -q origin main
done
echo "# done $(date -u +%FT%TZ)" >> $out
