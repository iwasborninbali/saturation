Ancillary files for "Nineteen certified configurations, eighteen independent bounds for the no-four-coplanar problem in the cube, and what they do not establish" (version 3.4, 3 September 2026; Zenodo doi:10.5281/zenodo.22272371).

verify_witness.py   -- checks a configuration file: all C(m,4) quadruples by exact 3x3 determinants (0 coplanar expected), distinctness, range.
witness_*.txt       -- the inequivalent optimal configurations of Section 9 (three classes of 18 at n=7, three of 20 at n=8, three of 23 at n=9,
                       two of 28 at n=11); header lines (#) give provenance; then one point "x y z" per line.
The complete table of certified lower bounds (n = 9..29) and all other configurations are in the Zenodo record and in
https://github.com/iwasborninbali/saturation (certs/a280537).

usage: python3 verify_witness.py <n> <file>
