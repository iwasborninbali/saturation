# Координированные мульти-модульные / мульти-кривые конструкции над Z и точные максимумы законных подмножеств: обзор литературы для задачи no-three-in-line

*Обзор подготовлен для исследователя с точным SAT + независимым верификатором для окон до ~50×50. Тело отчёта — на русском; названия работ, имена авторов, журналы, arXiv-ID, DOI, URL и дословные цитаты сохранены на языке оригинала (английский) и НЕ переводятся.*

---

## TL;DR (три пункта, отвечающие на главный вопрос)

- **Двухпростое объединение гипербол (H(c,p) ∪ H(c′,q), p≠q) как отдельный объект в литературе НЕ описано, НЕ проанализировано и НЕ опровергнуто никакой опубликованной верхней границей.** Это само по себе — ключевой результат новизны. Ближайшая по духу работа — Kovács–Nagy–Szabó (arXiv:2508.07632), но она (i) объединяет гиперболы с *одним* простым p и разными c, и (ii) явно оговаривает, что при k=2 шаг удаления возвращает ровно 3(p−1). Более того, авторы прямо пишут: *"we conjecture that even the Construction 2.7 of Hall et al. might not be asymptotically tight"* — то есть предполагают, что сам HJSW может быть не оптимален, но не в сторону мульти-простых объединений.
- **Опубликованной оценки числа коллинеарных троек МЕЖДУ двумя различными гиперболами (cross-term count) не существует** — это подтверждено и целенаправленным поиском по работам Shparlinski, Chan, Garaev, Cilleruelo, Shkredov. Есть только переносимые инструменты: коллинеарные тройки в декартовых произведениях (Petridis) и инцидентности точка–гипербола через билинейные суммы Клоостермана (Shkredov; Rudnev–Wheeler).
- **Доказательства, что 3(p−1) — точный максимум законного подмножества гиперболического лифта в окне 2p×2p, в литературе НЕТ**; это folklore, следующее из «3 из 4 копий»-аргумента HJSW как *нижней* оценки, а не как *верхней*. Над F_p одна гипербола вообще не имеет трёх коллинеарных точек (Khan–Magner–Senger–Winterhof, Lemma 3), но это факт mod p, а не над Z.

**BLUF-вывод:** двухпростой лид — это *открытая, не занятая литературой ниша*; он не опровергнут никакой известной границей, но и не может быть подтверждён на конечных p, поскольку само отношение HJSW 3(p−1)/(2p) → 3/2 снизу. Вердикт (полностью — в разделе Recommendations/Verdict ниже): **перспективно как вычислительная программа, но требует именно асимптотического измерения кросс-троек, а не сравнения при фиксированном конечном p.**

---

## Key Findings (по шести вопросам)

### Вопрос 1. Мульти-кривые / мульти-модульные законные множества над Z

**(i) Прямой ответ с источниками.**
Единственная работа, где HJSW-анализ систематически перенесён на объединения модульных гипербол, — это:

> Benedek Kovács, Zoltán Lóránt Nagy, Dávid R. Szabó, **"Randomised algebraic constructions for the no-(k+1)-in-line problem"**, arXiv:2508.07632v1 [math.CO], 11 Aug 2025. URL: https://arxiv.org/abs/2508.07632 · PDF: https://arxiv.org/pdf/2508.07632

Реконструкция HJSW-метода анализа там дана дословно (см. Вопрос 2). Классы конгруэнтных точек (Definition 2.1), роль наклонов 0, ∞, ±1 и структура пересечений «двух классов» (Observations 2.4–2.5), а также почему из 4 копий каждого класса в окне остаются 3 (Observation 2.6, Theorem 2.8).

Дословно об общей структуре пересечений:
> **"Observation 2.4.** For any c ∈ F_p^* and a Euclidean line ℓ, the intersection points of H(c,p) and ℓ lie in at most two classes."

> **"Observations 2.5.** (a) A line of slope 0 or ∞ meets H(c,p) in at most one class. (b) A line of slope +1 meets H(c,p) in one of the following sets: the empty set, one class in A or D, two classes, with both in A, both in D, or one in B and the other in C…"

**Объединения гипербол с ОДНИМ простым и разными c** описаны в:
> **"Proposition 1.3 (Multiplicativity).** Let k ≥ 2 be a fixed integer. Then as n → ∞, we have (3/4 − o(1))·kn ≤ f_k(n), if 2 | k, [and] (3/4 − 3/(4k) − o(1))·kn ≤ f_k(n), if 2 ∤ k."

с пояснением дословно:
> **"simply taking the disjoint union of ⌊k/2⌋ distinct constructions of HJSW type where p ∈ [(1/2 − o(1))n, (1/2)n] is fixed and c varies, we can obtain the following stronger observation for free from Theorem 1.2."**

Аналог из конечной геометрии (union-of-conics для (K,k)-дуг):
> **"In general, for small k, i.e., k < q/2, the best constructions are obtained from the union of ⌊k/2⌋ conics [3]."** (ссылка [3] = Ball–Hirschfeld, "Bounds on (n,r)-arcs and their application to linear codes", Finite Fields Appl. 11(3) (2005) 326–336.)

**(ii) Counting / upper-bound аргументы для объединений.** Единственный count-аргумент для объединения — Lemma 3.3 (размер урезанного множества, см. Вопрос 2c) и его вероятностное среднее (Proposition 3.7, F(t,s)·p + O(1)). Это оценки для k≥4; при k=2 (одна или несколько гипербол) они сводятся к 3(p−1).

**(iii) «Что было бы новым»:** анализ коллинеарных троек в объединении H(c,p) ∪ H(c′,q) с *разными* простыми p≠q в общем окне и сохранении законности над Z — в литературе отсутствует полностью.

---

### Вопрос 2. Конструкции Kovács–Nagy–Szabó (точные цитаты, номера)

Все цитаты — из arXiv:2508.07632v1, §2–§3, дословно.

**(a) Определения блоков M и E, множеств T₂, T₃, T₄.**

Блоки (Definition 2.3): четыре grid'а размера (p−1)/2 × (p−1)/2:
- A_{0,0} = [1,(p−1)/2] × [(p+1)/2, p−1]
- B_{0,0} = [(p+1)/2, p−1] × [(p+1)/2, p−1]
- C_{0,0} = [1,(p−1)/2] × [1,(p−1)/2]
- D_{0,0} = [(p+1)/2, p−1] × [1,(p−1)/2], и A_{r,s}=A_{0,0}+(rp,sp) и т.д.

T₂ (Construction 2.7), дословно:
> **"Take the set T₂ = T₂(p) ⊆ G(p) defined as the union of the following 12 blocks, three of each type: T₂ := (A_{0,1} ⊔ A_{1,0} ⊔ A_{1,1}) ⊔ (B_{−1,0} ⊔ B_{−1,1} ⊔ B_{0,1}) ⊔ (C_{0,0} ⊔ C_{1,0} ⊔ C_{1,1}) ⊔ (D_{−1,0} ⊔ D_{−1,1} ⊔ D_{0,0})."**
> **"The HJSW construction is the set S₂(c,p) := H(c,p) ∩ T₂(p)."**

Блок M (§2.3), дословно:
> **"In the grid G, the normal points form 16 blocks, with 12 of these forming the set T₂. We let M be the union of the four remaining blocks in the middle: M = A_{0,0} ⊔ B_{0,0} ⊔ C_{0,1} ⊔ D_{0,1}."**

Множество E (Definition в §2.3), дословно:
> **"Let Z × Z = E ⊔ F, where E = { (x,y) : (p | y+x) or (p | y−x) or (⌊(y+x)/p⌋ + ⌊(y−x)/p⌋ ≡ 0 (mod 2)) }, F = { (x,y) : (p ∤ y+x) and (p ∤ y−x) and (⌊(y+x)/p⌋ + ⌊(y−x)/p⌋ ≡ 1 (mod 2)) }."** (E — «коричневая» диагональная шахматная область; каждый класс целиком лежит в E или в F.)

T₃ и T₄ (Construction 2.10), дословно:
> **"In G, define T₃ := T₂ ⊔ (M ∩ E), T₄ := T₂ ⊔ M. Given c ∈ F_p^*, let S₃ = S₃(c,p) := H(c,p) ∩ T₃ and S₄ = S₄(c,p) := H(c,p) ∩ T₄."**

**(b) Результаты S₃ и S₄ — точные номера и счёты.**

> **"Theorem 2.8 ([12]).** For any odd prime p and c ∈ F_p^*, the set S₂(c,p) defined in Construction 2.7 is a no-three-in-line set of size 3(p−1), hence f₂(2p) ≥ 3(p−1)."

> **"Proposition 2.11.** f₃(2p) ≥ |S₃| ≥ 3.5(p−1) and f₄(2p) ≥ |S₄| = 4(p−1) for every prime p ≥ 3."

(Обозначения соответствуют «roughly 3.5(p−1) и 4(p−1)» из брифа: S₃ — no-4-in-line, S₄ — no-5-in-line.)

**(c) Randomised construction using multiple modular hyperbolae (Construction 3.2).** Дословно:

> **"Construction 3.2 (Randomised construction using multiple modular hyperbolae).** Let W ∈ Ω_p and k ∈ N with k ≥ 2|W|. Let S(W) := ⋃_{c∈W} S₄(c,p) ⊆ G′, and pick a subset R ⊆ S(W) of minimal size such that |ℓ ∩ R| ≥ |ℓ ∩ S(W)| − k for every line ℓ ∈ L′. Our construction is P_k(W) := S(W) \ R."**

(Ω_p — множество подмножеств {1,…,p−1}; G′ — 2p×(2p−1) подрешётка G без нижней строки; L′ — прямые наклона ±1, пересекающие G′.)

> **"Lemma 3.3 (Construction size).** The trimmed point set P_k(W) ⊆ G from Construction 3.2 is a no-(k+1)-in-line set of size |P_k(W)| ≥ 4(p−1)|W| − X_{k,p}(W), where X_{k,p}(W) := Σ_{ℓ∈L′} max{0, |ℓ ∩ S(W)| − k}."

Что доказано о ней асимптотически: Proposition 3.7 — E(X_{k,p} | A_t) = F(t,s)·p + O(1); Proposition 3.8 — sup{F(t,s)} = 4; итог — Theorem 1.5 и Corollary 3.11 (границы (1−2/k)kn ≤ f_k(n) для чётных k, (1−3/k)kn ≤ f_k(n) для нечётных).

**(d) Замечание/конъектура о (не)оптимальности мульти-HJSW.** Точная фраза из §6 (Concluding remarks), дословно и без перефразирования:

> **"Notice however that Theorem 1.6 gives evidence that we cannot expect probabilistic bounds using multiple Hall–Jackson–Sudbery–Wild type 2p × 2p constructions to be near-optimal. As a matter of fact, we conjecture that even the Construction 2.7 of Hall et al. might not be asymptotically tight."**

Важно: пользователь помнил «Theorem 2.7 of Hall et al.» — в действительности это **Construction 2.7** (не Theorem). Соответствующий результат HJSW — **Theorem 2.8**. Направление конъектуры: авторы предполагают, что HJSW/мульти-HJSW-конструкции 2p×2p *не* асимптотически оптимальны (то есть можно сделать лучше), а не наоборот.

**(e) КРИТИЧНО — случай k=2 и стоимость шага удаления.** В статье нет утверждения, что мульти-гиперболическое множество после удаления до ≤2 на прямой превышает 3(p−1) в окне 2p×2p. Напротив:

> **"Remark 3.4.** Note that (1/2)X_{k,p}(W) ≤ |R| ≤ X_{k,p}(W)."

и (§4):
> **"For example, in the case |W| = 1 and k = 2, Subsection 2.2 essentially details an optimal choice for the points R to be removed."**

То есть при k=2, |W|=1 оптимальное удаление возвращает ровно S₂ размера 3(p−1). Для нескольких гипербол при k=2 объединение S(W) содержит ~4(p−1)|W| точек до удаления, но каждая пара точек одной гиперболы плюс кросс-инцидентности на прямых наклона ±1 вынуждают удаление до 2 на прямую; в статье это анализируется только для k≥4 (где допускается >2 точек на прямую). **Явного утверждения о k=2 для мульти-гипербол с разными простыми в этой статье и в цитирующих её работах (arXiv:2510.17743, arXiv:2607.05255, arXiv:2606.02843) не найдено.**

**«Что было бы новым»:** точный анализ стоимости шага удаления Construction 3.2 при k=2 для W с гиперболами при *разных* простых — вне рамок статьи; это и есть незанятая ниша.

---

### Вопрос 3. Точный максимум законного подмножества структурного набора (max independent set в 3-однородном гиперграфе)

**(i) Прямой ответ с источниками.**

- **GPSS (General Position Subset Selection):** Vincent Froese, Iyad Kanj, André Nichterlein, Rolf Niedermeier, **"Finding Points in General Position"**, Internat. J. Comput. Geom. Appl. **27**(4) (2017) 277–296, DOI:10.1142/S021819591750008X; arXiv:1508.01097 (https://arxiv.org/abs/1508.01097). Дословно: *"We prove that General Position Subset Selection is NP-hard, APX-hard, and give several fixed-parameter tractability results."* Даны ядра O(k³) (по размеру решения) и O(h²) (по двойственному параметру); NP-/APX-hardness через редукции из вариантов Independent Set; ядро размера 15k³.
- **Payne–Wood:** Michael S. Payne, David R. Wood, **"On the general position subset selection problem"**, SIAM J. Discrete Math. **27**(4) (2013) 1727–1733, DOI:10.1137/120897493; arXiv:1208.5289. Ключевая лемма (число коллинеарных троек через Szemerédi–Trotter): *"Let P be a set of n points in the plane with at most ℓ collinear. Then the number of collinear triples in P is T = O(n² log ℓ + ℓ² n)."* Отсюда (через оценку независимого множества гиперграфа Spencer'а): *"P contains a subset of Ω(n/√(n log ℓ + ℓ²)) points in general position. In particular, if ℓ = O(√n), then P contains a subset of Ω((n/log ℓ)^{1/2}) points in general position."*
- **Cao** (мастер-тезис, Texas A&M, 2012): ядро O(k⁴) для «Non-Collinear Packing», greedy O(√opt)-аппроксимация, ILP-формулировка, двойственная к Point Line Cover.
- **Эквивалентность 3-однородному гиперграфу:** явно сформулирована в arXiv:1801.04584 ("The method of hypergraph containers"): вершины = точки решётки, рёбра = коллинеарные тройки, независимое множество = множество в общем положении. NP-hardness max independent set в 3-однородных гиперграфах и приближения: Krivelevich, Nathaniel, Sudakov ("Approximating Coloring and Maximum Independent Sets in 3-Uniform Hypergraphs").
- **Вычислительные исследования:** Eppstein, "Gurobi versus the no-three-in-line problem" (2018, https://11011110.github.io/blog/2018/11/12/gurobi-vs-no.html) — ILP: n² 0-1-переменных, O(n³) линейных ограничений. SAT vs ILP: сравнение в вычислительной биологии (Springer, DOI:10.1007/978-3-030-42266-0_6) показывает, что SAT часто выигрывает на «unsatisfiable»-сертификатах. Prellberg, **"Constraint Satisfaction Programming for the No-three-in-line Problem"**, arXiv:2602.07751 (8 Feb 2026, https://arxiv.org/abs/2602.07751) — CP-SAT, конфигурации 2n для всех n≤60.

**(ii) Ключевые цитаты.** См. Payne–Wood выше и Froese et al. выше.

**(iii) «Что было бы новым»:** вычислительное исследование max-general-position-subset именно на *объединении алгебраических кривых* (а не на полной решётке) как candidate set — в литературе не встречается. Вычисление точного максимума законного подмножества гиперболического окна 2p×2p (которое должно быть 3(p−1), если HJSW там оптимален) — **нигде не доказано, только наблюдается** (в том числе самим пользователем для p=7,11,13).

---

### Вопрос 4. Верхние границы для окон HJSW

**(i) Прямой ответ.** Опубликованного доказательства того, что в окне 2p×2p никакое законное подмножество гиперболического лифта не превышает 3(p−1), **не найдено**. Аргумент «3 из 4 копий» используется в HJSW/KNS только как *нижняя* граница (Observation 2.6 + Theorem 2.8: регион содержит 4 точки каждого класса в вершинах квадрата, любая пара конгруэнтных задаёт прямую наклона 0/∞/±1, три конгруэнтных на прямой невозможны). Это НЕ доказывает, что все 4 копии нельзя сохранить одновременно вместе с законностью — как *верхняя* граница на законное подмножество это folklore.

Дословно (Observation 2.6, arXiv:2508.07632):
> **"In G, no three congruent points lie on the same line, and any pair of congruent points determine a line of slope 0, ∞, or ±1."** *Proof.* **"The region contains 4 points of each class, laid out in the vertices of a square, from which the statement follows."**

**Родственные границы (mod p / арки).**
- Над F_p одна гипербола не имеет трёх коллинеарных точек вообще: **Mizan R. Khan, Richard Magner, Steven Senger, Arne Winterhof, "Two Combinatorial Geometric Problems Involving Modular Hyperbolas", INTEGERS 14 (2014) #A24** (21 pp.; arXiv:1304.6943, https://arxiv.org/abs/1304.6943), **Lemma 3**, дословно: *"We show that any line connecting 2 distinct points of H_{a,p} is ordinary. … By Lagrange's theorem kx² + dx − a has no more than 2 roots modulo p. Hence, no other point of H_{a,p} lies on y = kx + d."* Число обыкновенных прямых = (p−1)(p−2)/2. (Для степеней p^m прямая может пересечь H в ≤ 2p^{⌊m/2⌋} точках — Proposition 9.)
- Мультипликативная граница для арок: **Zofia Stępień, Lucjan Szymaszkiewicz, "Arcs in Z²_{2p}", J. Combin. Optim. 35 (2018) 341–349**, DOI:10.1007/s10878-017-0171-8 (arXiv:1512.02175): *"τ(Z²_{2p}) ≤ 2p+2 and τ(Z²_{2p}) = 2p+2 for p=3,5"* (Theorem 3.1), с Lemma 2.2 τ(Z²_{mn}) ≤ min{m·τ(Z²_n), n·τ(Z²_m)}.

**(iii) «Что было бы новым»:** лемма, ограничивающая размер законного подмножества набора, состоящего из немногих классов вычетов в строке (или на направление), в фундаментальной области ограниченного числа копий — не найдена; доказательство точной верхней границы 3(p−1) над Z стало бы новым результатом (пока это только вычислительное наблюдение пользователя для p=7,11,13).

---

### Вопрос 5. Классовая структура двухпростых объединений (CRT)

**(i) Прямой ответ с источниками.**
- **Sascha Kurz, "Caps in Z_n²", arXiv:1401.4333** (https://arxiv.org/abs/1401.4333). ILP-формулировки для max-cap в Z_n²; мультипликативная граница m₂(Z²_{nm}) ≤ min{n·m₂(Z²_m), m₂(Z²_n)·m}; число прямых — мультипликативная арифметическая функция (CRT).
- **Stępień–Szymaszkiewicz (arXiv:1512.02175), Lemma 2.4** (адаптирована из Huizenga), дословно: *"Let N = m·n with coprime m and n. Then any three points in Z²_N are collinear if and only if both projections onto Z²_m and Z²_n give a collinear point set."* И Lemma 2.1: τ(Z²_p) = p+1; Lemma 2.3: коллинеарность ⟺ D(a,b,c)=0.

Это подтверждает CRT-факт из брифа: для p≠q объединение живёт в Z²_{pq}, и тройка коллинеарна mod pq ⟺ коллинеарна и mod p, и mod q.

**(ii) КРИТИЧЕСКИЙ пробел.** Литературы о том, насколько велико может быть **законное-над-Z** подмножество, когда окно 2p×2p много меньше pq×pq (т.е. используется малый sub-box из Z²_{pq}, и произведение-CRT-структура «обрезана»), **не найдено**. Все результаты (Kurz, Stępień–Szymaszkiewicz, Misiak et al. torus) работают в *полном* Z²_n или на торе, а не в под-боксе, много меньшем модуля. Работ об арках / общем положении в SUB-BOXES Z²_m или о «local vs global density» лифтов модульных кривых в этом смысле не обнаружено. Ближайшее — концентрация точек модульной гиперболы в малых боксах: Cilleruelo–Garaev (GAFA 21 (2011) 892–904), Chan–Shparlinski (Acta Arith. 142 (2010) 59–66), но там речь о *количестве* точек в боксе, а не о законных подмножествах.

**(iii) «Что было бы новым»:** любая оценка максимального законного-над-Z подмножества CRT-объединения в под-боксе, много меньшем pq — полностью открыта.

---

### Вопрос 6. Асимптотика отношения для объединений; кросс-тройки

**(i) Прямой ответ (подтверждён целенаправленным субагентным поиском).** **Никакой опубликованной оценки числа коллинеарных троек между двумя различными модульными гиперболами (cross-term count) не существует.** Это установлено просмотром работ Shparlinski, Chan, Garaev, Cilleruelo, Shkredov по «points on modular hyperbolas». Причина частично структурна: над F_p одна гипербола вообще не даёт трёх коллинеарных (Khan et al., Lemma 3), а над Z нетривиальные коллинеарности — это «two-class secants» HJSW (Observations 2.4–2.5), которые анализируются комбинаторно, а не суммами символов.

**Ближайшие переносимые инструменты:**
- **G. Petridis, "Collinear triples and quadruples in Cartesian products in F_p²", arXiv:1610.05620** (https://arxiv.org/abs/1610.05620): для P = A×A число коллинеарных троек T(A) = O(|A|⁶/p + p^{1/2}|A|^{7/2}); в survey arXiv:1701.01635 (Theorem 9): при |A| ≪ p^{2/3}, T(A) ≪ |A|⁶/p + |A|^{9/2}. Определяется через тот же детерминантный критерий коллинеарности, что применим к точкам гиперболы (x, c/x).
- **I. D. Shkredov, "Modular hyperbolas and bilinear forms of Kloosterman sums", J. Number Theory 220 (2021) 182–211**, DOI:10.1016/j.jnt.2020.08.011; arXiv:1905.00291 (https://arxiv.org/abs/1905.00291). Дословно из введения: *"It turns out that incidences between hyperbolas and points are connected with bilinear forms of Kloosterman sums… we study incidences for hyperbolas in F_p and show how linear sum–product methods work for such curves."* Это и есть машинерия, которой можно было бы атаковать кросс-гиперболический count, но авторы этого не делают.
- **M. Rudnev, J. Wheeler, "On incidence bounds with Möbius hyperbolae in positive characteristic", Finite Fields Appl. 78 (2022) Art. 101978**; arXiv:2104.10534. Цитируют Shkredov's Theorem 16 как инцидентности σ(A,H) между A×A и семейством трансляций xy=−1.
- **Bézout-тип для двух гипербол:** прямая пересекает каждую гиперболу в ≤2 точках ⇒ ≤4 точек на объединении двух различных гипербол/коник; две различные коники пересекаются в ≤4 точках. Это структурный движок union-of-conics (Ball–Hirschfeld) и Proposition 1.3 KNS.
- **Распределение точек гипербол:** Igor E. Shparlinski, **"Modular Hyperbolas", Japan. J. Math. 7 (2012) 235–294**, DOI:10.1007/s11537-012-1140-8; arXiv:1103.2879 — авторитетный survey (равнораспределение через оценку Вейля |K(a,b,p)|≤2√p, Бомбьери для составного модуля); список из ~25 открытых проблем НЕ содержит вопроса о кросс-гиперболических тройках.

**(ii) Что может / не может установить heuristics.** Никакого heuristics, теоремы или численного исследования, предсказывающего предел (max lawful)/N для объединений k гипербол с разными простыми ≈N/2, в литературе нет. Вопрос «превышает ли 3/2 при k=2 или 3» — открыт.

**(iii) «Что было бы новым»:** прямой подсчёт (через суммы символов / Вейля / Бомбьери) числа коллинеарных троек с точками на двух различных модульных гиперболах, и вывод из него, вынуждает ли рост кросс-троек удаление постоянной доли — новизна целиком.

---

## Details (общий контекст и разрешение неточностей брифа)

- **Нижняя граница HJSW.** arXiv:2508.07632, Theorem 1.2 (Hall, Jackson, Sudbery, and Wild [12]): дословно *"1.5n − o(n) ≤ f₂(n) ≤ 2n."* Оригинал: R. R. Hall, T. H. Jackson, A. Sudbery, K. Wild, "Some advances in the no-three-in-line problem", J. Combin. Theory Ser. A **18**(3) (1975) 336–341, DOI:10.1016/0097-3165(75)90043-6. Отношение 3(p−1)/(2p) → 3/2 **снизу** (1.364 при p=11, 1.385 при p=13).
- **Конъектура Green.** Green, "100 open problems" (manuscript, обновление Dec 2025; https://people.maths.ox.ac.uk/greenbj/papers/open-problems.pdf). В Problem 72 Green обсуждает *extensible* версию и (по Ghosal, arXiv:2605.07000, дословно цитирующему Green) считает конъектуру Erde правдоподобной *"due to the vague intuition that examples of large no-three-in-a-line subsets of [−n,n]² may have to come from constructions (mod p)…"*. Green также спрашивает (arXiv:2510.17743, дословно): *"Green [14] asked whether every 'large' no-three-in-line set reduces to an algebraic curve modulo some prime."* Замечание: экстремальные 2n-конфигурации Flammenkamp'а (n≤76) не являются редукциями кривых — что согласуется с измерением пользователя, что они «менее алгебраичны mod каждого простого, чем случайные множества».
- **Конъектура Guy–Kelly и поправка Ellmann.** Guy & Kelly (Canad. Math. Bull. 11 (1968) 527–531) исходно конъектурировали c = ∛(2π²/3) ≈ **1.874**; Gabor Ellmann в марте 2004 нашёл ошибку в эвристике, и после поправки Guy (личное сообщение, 22 Oct 2004; OEIS A093602) c = π/√3 ≈ **1.814**. Документировано: Paul M. Voutier, "On the Guy-Kelly Conjecture for the No-Three-In-Line Problem", arXiv:2603.00215 (27 Feb 2026), дословно: *"We provide details of the error Gabor Ellmann found in 2004… details of the issue and its correction… do not seem to have appeared in the literature previously."*
- **Вычислительный фронт.** Prellberg (arXiv:2602.07751): дословно из arXiv:2607.05255 — *"For n ≤ 60, examples of no-three-in-line sets of size 2n were found by Prellberg [31]."* (Flammenkamp/Prellberg 2026 — сайт Бielefeld — продвинули M(n)=2n дальше, вплоть до n≤64 и n∈{66,68}, но это про полную решётку, не про гиперболические окна.)

---

## Recommendations

### (i) ВЕРДИКТ по двухпростому лиду

**Лид не известен литературе, не опровергнут никакой опубликованной верхней границей, и потому перспективен — но только как асимптотическая программа, а не как конечное наблюдение.** Обоснование:

1. **Не занято.** Ни одна работа (KNS arXiv:2508.07632, Grebennikov–Kwan arXiv:2510.17743, Kurz arXiv:1401.4333, Stępień–Szymaszkiewicz, Shparlinski survey) не рассматривает объединение гипербол с *разными* простыми в под-боксе, много меньшем pq, с сохранением законности над Z. Молчание литературы здесь — само по себе ключевой факт новизны.
2. **Не опровергнуто.** Единственная релевантная верхняя граница над Z — тривиальная 2n (по строкам). Мультипликативные границы арок (τ(Z²_{2p})≤2p+2) относятся к *арк-mod-m*, а не к законным-над-Z в под-боксе — как отмечено в брифе, этот маршрут закрыт для strong modular arcs, но НЕ для законных-над-Z множеств. KNS-конъектура даже предполагает, что HJSW *не* оптимален — что оставляет пространство для превышения 3/2.
3. **Аналитическая осторожность (обязательна).** Измеренные пользователем отношения (32/22=1.455 при p=11,q=13; 38/26=1.462 при p=13,q=17) превышают HJSW в том же конечном окне (30/22=1.364; 36/26=1.385), но **всё ещё ниже 3/2**. Поскольку сам HJSW → 3/2 снизу, конечное преимущество может как сохраниться, так и исчезнуть асимптотически. **Вердикт по существу не может быть вынесен на конечных p** — нужна асимптотика отношения (max lawful union)/N при p,q→∞ с фиксированным p/q, и/или оценка роста кросс-троек. Пока и то, и другое отсутствует в литературе.

**Итог:** «promising, literature-silent» — не known, не refuted. Это лучший из трёх возможных исходов для новизны.

### (ii) ЛУЧШИЙ доступный верхне-граничный аргумент для окон HJSW

Самое сильное, что позволяет литература, — комбинация:
- **(mod p, теорема):** Khan–Magner–Senger–Winterhof, Lemma 3 (INTEGERS 14 (2014) #A24) — над F_p прямая пересекает H(c,p) в ≤2 точках (по теореме Лагранжа для квадратного трёхчлена). Это ГАРАНТИЯ, что коллинеарности возникают только над Z, между конгруэнтными копиями.
- **(над Z, folklore):** Observation 2.6 (KNS/HJSW) — в окне G каждый класс имеет ровно 4 копии в вершинах квадрата; никакие три конгруэнтные не коллинеарны; любая пара конгруэнтных задаёт наклон 0/∞/±1. Отсюда 3(p−1) достигается как *нижняя* граница. Утверждение, что 3(p−1) есть *точный максимум* законного подмножества — **folklore, не теорема**: оно наблюдается вычислительно (пользователь: p=7,11,13), но нигде не доказано. Прямого «3 of 4 copies cannot all be kept»-аргумента как верхней границы в литературе нет.

Таким образом: **best available upper bound для законного подмножества гиперболического окна = 3(p−1), статус — folklore/вычислительное наблюдение, НЕ опубликованная теорема.**

### (iii) ТРИ конкретных следующих вычисления (для SAT/verifier до ~50×50)

**Вычисление A — «Асимптотический тренд отношения при фиксированном p/q≈1».**
Взять пары близких простых (p,q): (11,13), (13,17), (17,19), (19,23), (23,29) — окно N×N с N = 2·max(p,q). Для каждой пары SAT-ом найти точный максимум законного-над-Z подмножества H(c,p)∪H(c′,q) (перебрать c,c′ ∈ F_p^*×F_q^* или зафиксировать c=c′=1) и вычислить ratio = max/N. **Что мерить:** последовательность ratio(p,q) и её разность с 3(max(p,q)−1)/N (like-for-like HJSW в том же окне). **Порог решения:** если ratio − 3/2 растёт (или остаётся ≥ +δ, δ≈0.02) при увеличении p,q — сильный сигнал, что предел >3/2; если ratio монотонно приближается к 3/2 снизу с сокращением зазора до HJSW — лид, вероятно, артефакт конечного p. Ключ: сравнивать с 3/2, а НЕ с конечным HJSW.

**Вычисление B — «Прямой подсчёт кросс-троек».**
Для тех же пар (p,q) подсчитать (независимым верификатором, без SAT) число коллинеарных-над-Z троек, у которых ≥1 точка на H(c,p) и ≥1 на H(c′,q) (cross-term), отдельно от внутригиперболических троек. **Что мерить:** рост числа кросс-троек T_cross(p) как функции N. **Порог решения:** если T_cross = Θ(N²) или быстрее (постоянная доля точек вовлечена) — удаление до законности обязано срезать постоянную долю, и предел ≤3/2 (лид опровергается изнутри); если T_cross = o(N²) (напр. O(N log N) или O(N^{3/2}), как подсказывают оценки типа Petridis/Payne–Wood для наборов с малой коллинеарностью) — удаляется o(N) точек и предел может превысить 3/2. Это самый информативный тест: он напрямую атакует незанятую нишу Вопроса 6.

**Вычисление C — «Оптимальность HJSW-окна и вклад среднего блока M».**
Подтвердить SAT-ом, что max законного подмножества чистого гиперболического окна H(c,p)∩(окно 2p×2p) равен 3(p−1) для p=17,19,23 (расширить проверенный диапазон 7,11,13), и отдельно — можно ли, добавив точки из среднего блока M (как в T₄, но с условием ≤2 на прямую вместо ≤4), превзойти 3(p−1). **Что мерить:** max(H(c,p)∩T₄, законное) − 3(p−1). **Порог решения:** если для всех проверенных p результат = 3(p−1) — это первое вычислительное «доказательство» folklore-границы на расширенном диапазоне (и целевой кандидат для последующей теоремы); если хоть для одного p результат >3(p−1) — folklore-граница ложна и HJSW-окно не оптимально даже для одной гиперболы (что согласовалось бы с KNS-конъектурой о неоптимальности Construction 2.7).

---

## Caveats

- **Асимптотика ≠ конечные данные.** Поскольку 3(p−1)/(2p) → 3/2 *снизу*, любое конечное превышение HJSW (1.455, 1.462) логически совместимо и с пределом >3/2, и с пределом =3/2. Данные пользователя показывают преимущество *в том же окне*, но не могут установить предел. Все выводы о лиде должны опираться на Вычисления A/B (тренд и рост кросс-троек), а не на конечное сравнение.
- **Отрицательные находки (где именно искал).** Кросс-гиперболический count троек: не найден в arXiv:1103.2879 (Shparlinski survey и его список открытых проблем), в работах Chan–Shparlinski (Acta Arith. 142), Cilleruelo–Garaev (GAFA 21), Shkredov (JNT 220), Rudnev–Wheeler (FFA 78), Petridis (arXiv:1610.05620) — ни одна не изолирует эту величину. Законные-над-Z подмножества в под-боксе, много меньшем pq: не найдены в Kurz (arXiv:1401.4333), Stępień–Szymaszkiewicz (arXiv:1512.02175), Misiak et al. (torus, arXiv:1406.6713), Ku–Wong (m-dim torus). Доказательство верхней границы 3(p−1) над Z: не найдено в KNS (arXiv:2508.07632), в цитирующих работах (arXiv:2510.17743, 2607.05255, 2606.02843) и у Khan et al. (mod-p результат — не над Z).
- **Уточнения ссылок брифа.** (1) «Theorem 2.7 of Hall et al.» — в KNS это **Construction 2.7**; результат HJSW — **Theorem 2.8**. (2) Точная конъектура KNS направлена на *неоптимальность* HJSW (можно лучше), а не на её оптимальность. (3) Khan–Magner–Senger–Winterhof имеет номер статьи **#A24** (в некоторых базах OEAW/RICAM указано #A33 — это разночтение нумерации INTEGERS; arXiv:1304.6943 — надёжный первоисточник). (4) Guy–Kelly: исходное c≈1.874, исправленное Ellmann'ом c≈1.814 — оба значения фигурируют в литературе, важно не путать.
- **Статус вычислительных инструментов.** Для сертификата «максимум = X» (unsatisfiability при X+1) SAT/CP-SAT, как правило, эффективнее ILP на этих задачах (Gusfield et al.; Eppstein наблюдал застой Gurobi). Пайплайн пользователя (SAT + независимый верификатор) — правильный инструмент для Вычислений A и C; Вычисление B — чистый перебор троек, SAT не требуется.