Ancillary files for "Certified computations on no-three-in-line problems: exact values and witnesses in the cube,
and the Guy-Kelly count in the plane" (version 1.0, 21 September 2026).  The article consolidates four earlier notes;
their Zenodo records are listed in its Section 8.  Witness archive for Part I: doi:10.5281/zenodo.22271375.

Part I (cube, no three collinear, OEIS A399138) -- Section 3.4 of the article
  verify_witness_lines.py          checks a configuration: all C(m,3) triples by exact integer cross products
                                   (0 collinear expected), distinctness, range.   usage: python3 verify_witness_lines.py <n> <file>
                                   (--selftest needs the calibration file sat_witness_n6_64.txt from certs/no3_3d/ of the repository)
  n8_94_c08_ord4_strata.txt        a(8)  >= 94,  stabiliser of order 4 (stratum c08)
  n8_94_c11_ord4_strata.txt        a(8)  >= 94,  stabiliser of order 4 (stratum c11), inequivalent to the previous
  n9_116_c08_ord4_strata.txt       a(9)  >= 116, stabiliser of order 4
  n9_116_c26_ord12_strata.txt      a(9)  >= 116, stabiliser of order 12; exact maximum of its stratum (CP-SAT status OPTIMAL)
  n10_138_c16_ord6_strata.txt      a(10) >= 138, exact maximum of its stratum
  n11_164_c26_ord12_strata.txt     a(11) >= 164, stabiliser of order 12; the bound inside the stratum is not closed
                                   Header lines (#) give provenance (symmetry class, solver status); then one point "x y z" per line.

Part I' (cube, no four coplanar, OEIS A280537) -- Section 4.4 of the article
  verify_witness.py                checks a configuration: all C(m,4) quadruples by exact 3x3 determinants
                                   (0 coplanar expected), distinctness, range.   usage: python3 verify_witness.py <n> <file>
                                   (--selftest needs the calibration file witness_n5.txt from certs/a280537/ of the repository)
  witness_n7_18_c03_ord2_strata.txt   n=7,  18 points, stabiliser of order 2
  witness_n7_18_c06_ord3_strata.txt   n=7,  18 points, stabiliser of order 3
  witness_n8_20_c03_ord2_strata.txt   n=8,  20 points, stabiliser of order 2
  witness_n8_20_c06_ord3_strata.txt   n=8,  20 points, stabiliser of order 3
  witness_n9_23_c06_ord3_strata.txt   n=9,  23 points, stabiliser of order 3
  witness_n9_23_c06_ord3_long.txt     n=9,  23 points, stabiliser of order 3, inequivalent to the previous
  witness_n11_28_c06_ord3_long.txt    n=11, 28 points, stabiliser of order 3 (best known; optimality not proved)
                                   Header lines (#) give provenance; then one point "x y z" per line.  The complete table of
                                   certified lower bounds (n = 9..29) and all other configurations are in the repository
                                   https://github.com/iwasborninbali/saturation (certs/a280537) and its mirror no3-results.

Part II' (plane, direction spectrum) -- Sections 6.1-6.3 of the article
  direction_spectrum_model_values.txt   the line model's predicted constants c_v^model(n) for the fifteen measured direction
                                        classes at n = 20, 30, 40; the header gives the renormalisation constants, called Z_n
                                        in the file and lambda_n in the article.
  direction_spectrum_data_by_strata.txt the measured constants c_v on Flammenkamp's database of no-three-in-line solutions,
                                        by n-stratum (n = 19-20, 29-31, 32-57) rather than pooled, measured independently
                                        of the model by a second agent (abs_spectrum_classes.py, 3 September 2026), with the
                                        solution counts per stratum recorded at the end of the file.

All thirteen configurations were re-verified with the two scripts above on 21 September 2026 (0 collinear triples, 0 coplanar
quadruples).  Programs, journals and the full record: https://github.com/iwasborninbali/saturation and
https://github.com/iwasborninbali/lemma-atelier (lemma 005, need 008).
