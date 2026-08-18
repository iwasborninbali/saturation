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
| `sweeps/family3_sym{9,10}_n{33,37}.txt` | 3-cycle family (non-central defects), full canonical lists (there_tw, first solver's machine) | complete: 33 → 1 book (C4), 0 (V2); 37 → 2 books (C4), 0 (V2) |
| `sweeps/family3A_sym10_n41.txt` | first half of the 41 list, V2 base | complete (0) |
| `sweeps/family3A_sym10_n39_partial.txt`, `family3A_sym9_n41_partial.txt` | first halves of 39 (V2, 1339/1938) and 41 (C4, 1325/2280 at stop) | partial snapshots (0 books); both sweeps STOPPED on the first solver's machine (superseded by the full reruns with the corrected generator on VM2/VM4) |
| (VM2/VM4) `family3full_*_n{33,39,41}`, `central3_*_n{37,39,41,45}` | full reruns with the corrected generator (defects3.py, central classes included) | 33: complete; 37 central: complete; 39: sym10 done, sym9 running (VM2); 41 half A (VM4): sym10 884/2375, 41 half B (VM2): sym9 253/2375 — running unattended; 45 central: stopped; 47: stopped (`sweeps/f47A_sym10_n47_stopped.txt`, 0 sub-classes finished) |
