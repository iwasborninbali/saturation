#!/bin/bash
read -r n best m0 m1 <<< "$1"
/tmp/claude-1000/-home-pmbot-projects-solver-kit/df30d6f4-57eb-4267-abb8-3e2d3cd04a69/scratchpad/no3p $n $best $m0 $m1 2>/dev/null
