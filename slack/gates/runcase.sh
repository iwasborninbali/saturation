#!/bin/bash
f="$1"; out="$2"
s=$(date +%s)
timeout "${LIM:-3600}" kissat -q "$f" > /dev/null 2>&1; rc=$?
e=$(date +%s)
case $rc in 20) st=UNSAT;; 10) st=SAT;; 124) st=TIMEOUT;; *) st="rc=$rc";; esac
echo "$(basename "$f") $st $((e-s))с" >> "$out"
