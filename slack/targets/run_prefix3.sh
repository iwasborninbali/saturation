#!/bin/bash
read -r n best m0 m1 m2 <<< "$1"
B=/tmp/claude-1000/-home-pmbot-projects-solver-kit/df30d6f4-57eb-4267-abb8-3e2d3cd04a69/scratchpad/no3p3
out=$($B "$n" "$best" "$m0" "$m1" "$m2" 2>/dev/null); rc=$?
last=$(echo "$out" | tail -1)
if [ $rc -ne 0 ] || [ -z "$last" ] || ! echo "$last" | grep -q "MAX="; then
  echo "$m0 $m1 $m2 :: FAIL rc=$rc raw=[$last]"
else
  echo "$m0 $m1 $m2 :: OK $last"
fi
