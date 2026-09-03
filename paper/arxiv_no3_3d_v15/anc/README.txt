Ancillary files for "Exact values and certified lower bounds for the no-three-in-line problem in the cube" (version 1.5, 3 September 2026;
Zenodo doi:10.5281/zenodo.22273425; witnesses archive doi:10.5281/zenodo.22271375).

verify_witness_lines.py  -- checks a configuration: all C(m,3) triples by exact integer cross products (0 collinear expected), distinctness, range.
n<n>_<m>_c<ii>_ord<k>_strata.txt -- the witnesses for a(8) >= 94 (two classes), a(9) >= 116 (two classes), a(10) >= 138, a(11) >= 164;
                              header lines (#) give provenance (symmetry class, solver status); then one point "x y z" per line.
usage: python3 verify_witness_lines.py <n> <file>
