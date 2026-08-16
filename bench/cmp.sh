#!/bin/bash
# usage: cmp.sh n sym secs "cfgs" ; cfg = order:value:shave
n=$1; sym=$2; secs=$3; cfgs=$4
for cfg in $cfgs; do IFS=: read o v sh <<< "$cfg"; for seed in 1 2 3 4 5 6 7 8; do
  echo "$n $sym $seed $secs 2000 $o $v 50 $sh"
done; done | xargs -P 8 -L 1 sh -c './there $0 $1 $2 $3 $4 $5 $6 $7 $8 | sed "s/ : .*//"' | sort
