Ancillary files for "The direction spectrum of no-three-in-line solutions: a line model derives its shape, not its scale"
(version 1.1, 3 September 2026; Zenodo doi:10.5281/zenodo.22278951; concept doi:10.5281/zenodo.22275037).

direction_spectrum_model_values.txt   -- the line model's predicted constants c_v^model(n) (Section 3) for the fifteen measured
                                          direction classes, at n = 20, 30, 40; header gives the renormalisation constants
                                          Z_20, Z_30, Z_40.
direction_spectrum_data_by_strata.txt -- the measured constants c_v on Flammenkamp's database of no-three-in-line solutions,
                                          broken out by n-stratum (n = 19-20, 29-31, 32-57) rather than pooled, so that the
                                          model can be compared with the data at matched n; measured independently of the
                                          model, by a second agent (abs_spectrum_classes.py, 3 September 2026), with the
                                          solution counts per stratum recorded at the end of the file.

Both files are also referenced in the note's Sections 1 and 3 (Table of results). The full measurement and model code, the
prior-art search of Section 6, and the dated blind-prediction ledger are in
https://github.com/iwasborninbali/saturation and https://github.com/iwasborninbali/lemma-atelier (lemma 005, need 008).
