# logs/ — finished sweep journals (audit trail for the papers)

`bench/*.txt` journals are written by running sweeps and are git-ignored to avoid conflicts between machines; when a sweep
is finished (or a snapshot is needed for a table), the journal is copied here **unchanged**.  Every line of a journal is one
sub-class: `PAIRS` string, then the solver's final line (`all n=.. sym=..: solutions=k nodes=.. secs=..` = exhausted;
`dead ...` = the fixed defect already violates the law; `timeout-all ...` = incomplete).  `BOOK <PAIRS> sol <tokens>` lines
list every labelled solution (PRINTALL=1).  Header lines (`#`) give date, sub-class count, time limit, program and commit.

| file | what | status |
|---|---|---|
| `sweeps/central3_*_n{13..25,33}.txt` | 3-cycle defects using the central class (bench/defects3.py --central-only), both bases | complete |
| `sweeps/mixed_{c4v2,v2c4}_n{9..27}.txt` | mixed families (bench/mixed3.py), both parities | complete, all empty |
| `sweeps/twoloop_n36_exh.txt`, `..._sols.txt` | two-loop family n=36, exhaustive over 153 sub-classes mod D4 | 152 exhausted (3 with solutions), sub-class (1,4) rerun pending |
| `sweeps/twoloop_n36_find.txt` | the earlier finding-mode sweep at n=36 (81 sub-classes, ~2 min each) | superseded |
| `sweeps/family3B_sym{9,10}_n{39,41}.txt` | 3-cycle family (non-central defects), second half of the canonical lists, second solver's machine | 41: complete (0); 39: V2 complete (0), C4 300 sub-classes (1) |
| (first solver's machine) `family3A_*` | first halves of the lists for 39, 41, 45, 47 | to be added by the first solver |
| (VM2) `family3full_*_n33`, `central3_*_n{37,39,41,45}` | full reruns with the corrected generator | running |
