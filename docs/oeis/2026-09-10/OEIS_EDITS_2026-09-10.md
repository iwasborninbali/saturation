# OEIS — what to paste on 10 Sep 2026 (three drafts: A398172, A398184, and one new triangle)

State measured 10.09 10:3x WITA from oeis.org: A280537 edit APPROVED (#43, Sep 08 2026: a(12) >= 31, a(n) <= 3n,
the a-file of nonprime sizes 8..18); A000755 a(20) APPROVED (#54, Aug 27 2026); A399138 no pending changes;
A398172 status "editing" after Sean A. Irvine's comment (Sep 09 17:23 EDT) and two by Andrew Howroyd (18:32, 18:37);
A398184 status "proposed" with Irvine's question (Sep 08 19:58 EDT). The draft quota is three: A398172 + A398184
+ the new triangle below = three. Nothing else is to be opened until one of them is approved.

Every number below was recomputed on 10.09 by a third program written independently (tri.c, C, bitmask DFS with
exact cross products; n = 7 in 1.5 s) and agrees with the drafts and the two programs of 3.09 in every entry:
rows T(n,k) for n = 1..7 and the maximal-by-size counts for n = 1..7 (see independent_recount_2026-09-10.txt).

## Order of operations (the A-number of the triangle is needed inside the other two edits)

1. Contribute -> "new sequence" -> switch to internal format -> paste BLOCK T below -> Save. Note the allocated
   A-number (call it AXXXXXX). Upload b_triangle.txt renamed to bXXXXXX.txt: tick "This is a b-file"
   (it IS one); "Text for Link line": Table of n, a(n) for n = 1..63 (rows 1..7, flattened).
2. Edit A398172 -> internal format -> replace the %C, %o, %H, %Y lines by BLOCK 1 (AXXXXXX filled in), keep
   %N %S %e %K %O. Upload a398172.txt: do NOT tick the b-file box; Text for Link line:
   Two independent programs (Python) for A398172 and A398184. Then paste REPLY 1 into Discussion, propose.
3. Edit A398184 -> internal format -> replace the %C, %o, %H, %Y lines by BLOCK 2. Upload a398184.txt (not a
   b-file); Text for Link line: Numbers of maximal subsets by size, n = 1..7. Paste REPLY 2, propose.

Editors' edits are never reverted; if an editor has changed a field since 10.09, keep the editor's version.

## BLOCK T — the new triangle (rows of length 2n+1; row sums = A398172; right edge = A000755)

%N Triangle read by rows: T(n,k) is the number of k-element subsets of the n X n grid with no three collinear points, 0 <= k <= 2n.
%S 1,1,0,1,4,6,4,1,1,9,36,76,78,28,2,1,16,120,516,1278,1668,998,204,11,1,25,300,2148,9498,25052,36698,26700,8242,840,32,1,36,630,6768,47331,215448,620210,1073076,1035097,496436,98950,5664,50
%C Row n has 2n + 1 entries, k = 0..2n; a subset of the n X n grid with no three collinear points has at most 2n points, so T(n,k) = 0 for k > 2n (T(1,2) = 0: the 1 X 1 grid has a single point).
%C Subsets are counted as sets of grid points; rotations and reflections are not identified (no symmetries are taken into account, as in A000755).
%C T(n,k) is the number of faces of size k of the independence complex of the 3-uniform hypergraph whose hyperedges are the collinear triples of the n X n grid (A000938(n) triples); the row sums give A398172(n), and A398184(n) counts the maximal faces.
%C All rows were computed by two independent programs (exhaustive depth-first enumeration).
%F T(n,k) = binomial(n^2, k) for 0 <= k <= 2.
%F T(n,3) = binomial(n^2, 3) - A000938(n).
%F T(n,2n) = A000755(n).
%F Sum_{k=0..2n} T(n,k) = A398172(n).
%e Triangle begins:
%e   1, 1, 0;
%e   1, 4, 6, 4, 1;
%e   1, 9, 36, 76, 78, 28, 2;
%e   1, 16, 120, 516, 1278, 1668, 998, 204, 11;
%e   1, 25, 300, 2148, 9498, 25052, 36698, 26700, 8242, 840, 32;
%e   ...
%e T(3,3) = 76: of the binomial(9,3) = 84 triples of points of the 3 X 3 grid, A000938(3) = 8 are collinear. T(3,6) = 2: the two 6-point no-three-in-line configurations of the 3 X 3 grid (A000755(3) = 2).
%o (Python)
%o from math import gcd
%o def row(n): # T(n,0..2n)
%o     N = n*n; P = [divmod(i, n) for i in range(N)]
%o     L = [[sum(1 << k for k in range(N) if k != i and k != j and (P[k][0]-P[i][0])*(P[j][1]-P[i][1]) == (P[k][1]-P[i][1])*(P[j][0]-P[i][0])) for j in range(N)] for i in range(N)]
%o     T = [0]*(2*n+1)
%o     def dfs(start, chosen, F): # F = cells collinear with two chosen cells
%o         T[len(chosen)] += 1
%o         for c in range(start, N):
%o             if not F >> c & 1:
%o                 G = F
%o                 for s in chosen: G |= L[s][c]
%o                 dfs(c+1, chosen + [c], G)
%o     dfs(0, [], 0); return T
%o print([row(n) for n in range(1, 6)]) # rows 1..5
%Y Cf. A398172 (row sums), A398184, A000755 (right edge), A000938, A000769, A005408 (row lengths).
%K nonn,tabf,more
%O 1,5

b-file: b_triangle.txt in this folder (63 lines, index 1..63, rows 1..7 flattened; row 7 is not in DATA).
The %o program was run on 10.09: rows 1..5 reproduced in the foreground, row 6 in a separate run (see the note
in independent_recount_2026-09-10.txt if present; otherwise rows 1..5 only were checked in Python, rows 6..7 by tri.c
and by the two programs of 3.09).

## BLOCK 1 — A398172 (replace %C, %o, %H, %Y; keep %N %S %e %K %O)

%C a(n) is the number of faces (the empty face included) of the independence complex of the 3-uniform hypergraph whose hyperedges are the collinear triples of the n X n grid (there are A000938(n) such triples). The largest faces have 2n points, and there are A000755(n) of them; A398184 counts the maximal faces.
%C Subsets are counted as sets of grid points; rotations and reflections are not identified (no symmetries are taken into account, as in A000755).
%C The numbers of such subsets by size are given in AXXXXXX (a triangle whose row sums are this sequence).
%C All terms were computed by two independent programs (exhaustive depth-first enumeration; both are in the attached file).
%H Aleksei Kudriashov, <a href="/A398172/a398172.txt">Two independent programs (Python) for A398172 and A398184</a>
%Y Cf. AXXXXXX (by size), A398184 (maximal subsets), A000755, A000769, A000938, A277433, A219760.

(no %o lines)

REPLY 1 (Discussion of A398172):
Thank you both. Done in this edit: (1) a statement on symmetries added - subsets are counted as sets of grid points, rotations and reflections are not identified, the same convention as A000755; (2) both programs moved to the attached file a398172.txt; (3) the numbers by size removed here and submitted as a separate triangle, AXXXXXX (row sums = this sequence, right edge = A000755), with cross-references.

## BLOCK 2 — A398184 (replace %C, %o, %H, %Y; keep %N %S %e %K %O)

%C These are the facets of the independence complex of the collinear-triples hypergraph of the n X n grid (A398172 counts all its faces). Their sizes range from A277433(n) (Martin Gardner's minimum no-3-in-a-line problem, all slopes) to 2n; exactly A000755(n) of them have the maximum size 2n. The complex is not pure for n >= 3.
%C Subsets are counted as sets of grid points; rotations and reflections are not identified (no symmetries are taken into account, as in A000755).
%C The numbers of maximal subsets by size for n <= 7 are given in the attached file.
%C All terms were computed by two independent programs (exhaustive depth-first enumeration with a maximality check); both programs are attached to A398172.
%H Aleksei Kudriashov, <a href="/A398184/a398184.txt">Numbers of maximal subsets by size, n = 1..7</a>
%Y Cf. A398172 (all subsets), AXXXXXX (all subsets by size), A000755, A000769, A000938, A277433, A219760.

(no %o lines)

REPLY 2 (Discussion of A398184):
Thank you. A statement on symmetries added: subsets are counted as sets of grid points, rotations and reflections are not identified, as in A000755. The counts by size are moved to the attached file a398184.txt; the two programs are attached to A398172 (a398172.txt).
