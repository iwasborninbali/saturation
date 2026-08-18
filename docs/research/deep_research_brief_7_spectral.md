# Deep-research brief 7 — tools for two concrete estimates (run after brief 6)

(Русское резюме внизу.  Нужны точные теоремы с формулировками, константами и ссылками; никакого обзора.)

## Estimate A — quadratic residues among small sums of two squares
Let p be a large prime, χ the Legendre symbol mod p.  We need: for S = p^{δ} (some fixed small δ > 0, ideally any δ > 0, at least δ = 1/8 or 1/4),
   #{ (s₁, s₂) : 1 ≤ s₁ ≤ s₂ ≤ S,  χ(s₁² + s₂²) = +1 }  ≥  c · S²     (a positive proportion),
equivalently a nontrivial bound Σ_{s₁,s₂ ≤ S} χ(s₁²+s₂²) = o(S²).  Note: the complete 2D sum Σ_{s∈F_p²} χ(s₁²+s₂²) e(⟨h,s⟩/p) has modulus ≈ p
(χ∘Q is essentially self-dual), so plain completion (Pólya–Vinogradov in 2D) fails below S ≈ √p·log p; the Weil bound for the 1D restriction
χ(2s₁² − 2σ s₁ + σ²) over s₁ ≤ σ works only for σ ≫ √p log p.  Questions:
1. Burgess-type bounds for character sums over values of binary quadratic forms / norms from Z[i] in short ranges: exact statements
   (Burgess 1962–63 for polynomials of degree ≤ 2? Chang; Heath-Brown "Burgess bounds for short character sums of polynomials"; results on
   the least quadratic non-residue that is a sum of two squares / a norm; "character sums over Gaussian integers in a disc").
2. Alternatively: the distribution of χ on the values of the norm form in a box — any equidistribution theorem with an explicit exponent
   (e.g. via the Weil bound for the sum over a hyperbola u v ≡ c combined with the parametrisation s₁+is₂ ~ Gaussian integers).
3. If nothing exists below S = √p: state precisely what IS known and the best exponent.

## Estimate B — spectral edge of a deterministic arithmetic ±-matrix (Wigner-type)
Setting: an explicit symmetric (p−1)×(p−1) matrix C = (1/16)Σ_π (s_π s_πᵀ − diag), a sum over ~30 p log p rank-one ±1 matrices of support 3
(indices = residues mod p; the supports and signs come from collinear point-triples of the lifted modular hyperbolas xy ≡ ±1 in a 2p×2p box —
an explicit algebraic-arithmetic family).  Numerically the spectrum is semicircle-like with edge ≈ ±2.4√(tr C²/(p−1)).  Questions:
1. Known deterministic analogues of Wigner's semicircle / edge bounds for matrices defined by character sums or arithmetic structures:
   e.g. Paley graphs / conference matrices (eigenvalues ±√p exactly), Kloosterman-sum matrices, "arithmetic random matrices"
   (Fürer, Ismailescu?, "spectral properties of Kloosterman matrices"?), matrices A_{ab} = χ(f(a,b)) — precise references and the method
   (trace method with Weil/Deligne bounds for the closed-walk sums; or Fourier/character diagonalisation when the matrix is a group
   circulant/convolution).
2. General tools: trace method for structured (non-random) matrices with "pseudo-random" entries: conditions on short cycles/codegrees
   under which λ_max = O(√(max row ℓ²-norm)); results of the type "graphs with few short cycles / high girth have small second eigenvalue"
   (Alon–Boppana lower bound is the other direction); Friedman-type arguments requiring only local statistics; the "spectral gap from
   codegree control" lemma (e.g. in expander constructions from Cayley graphs / Ramanujan complexes; the Kahn–Szemerédi trace argument).
3. Concretely: if a symmetric matrix M has zero diagonal, |M_ab| ≤ 1, ≤ d nonzeros per row, and the number of closed walks of length 2k
   weighted by products of entries is ≤ (p−1)·(4d)^k·Cat_k·(1+o(1)) for k up to log p, then ‖M‖ ≤ 2√d(1+o(1)) — the exact form of this
   lemma and how the walk count is usually verified via "few short cycles" + cancellation.  Any version where cancellation comes from
   characters (Weil) rather than randomness.

## Deliverable
Per question: exact statements with references (author, title, journal, year, theorem/page); a one-paragraph judgement whether A and B are
"citable", "provable in a few pages with known tools", or "open in this generality"; and the best exponent obtainable for A today.

---
## Резюме по-русски
Два точечных запроса под доказательство: (A) положительная доля квадратичных вычетов среди малых сумм двух квадратов s₁²+s₂², s ≤ p^δ
(оценки типа Бёрджесса для значений бинарной квадратичной формы / гауссовых норм); (B) детерминированные оценки края спектра для арифметических
±‑матриц (аналоги Вигнера: матрицы Пэли/Клоостермана, метод следов с сокращениями Вейля, леммы «мало коротких циклов ⇒ малая норма»).
Нужны точные формулировки и ссылки, и честный вердикт «цитируемо / доказуемо / открыто».
