#!/bin/bash
# wrapper with explicit status: a killed/failed solver must NOT look like a finished one,
# and every prefix must leave a line (so coverage can be checked mechanically).
read -r n best m0 m1 <<< "$1"
B=/tmp/claude-1000/-home-pmbot-projects-solver-kit/df30d6f4-57eb-4267-abb8-3e2d3cd04a69/scratchpad/no3p
out=$($B "$n" "$best" "$m0" "$m1" 2>/dev/null); rc=$?
last=$(echo "$out" | tail -1)
if [ $rc -ne 0 ] || [ -z "$last" ] || ! echo "$last" | grep -q "MAX="; then
  echo "$m0 $m1 :: FAIL rc=$rc raw=[$last]"
else
  echo "$m0 $m1 :: OK $last"
fi
