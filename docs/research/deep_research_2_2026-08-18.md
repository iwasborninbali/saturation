# Обзор: конструкции в «целочисленном зазоре» задачи no-three-in-line — дуги над Z_m, CRT-склейки и барьер 3n/2

## TL;DR
- Для БЕСКВАДРАТНЫХ m «сильная модулярная дуга» A(m) (условие det≡0 mod m) НЕ может превзойти 3n/2: субмультипликативная оценка A(mn)≤min{m·A(n), n·A(m)} (Stępień–Szymaszkiewicz, Lemma 2.2; Kurz) даёт A(m)/m ≤ 1+1/P → 1. Для m=2p доказано A(2p)≤2p+2, с равенством лишь при p=3,5.
- Для непростых степеней (p², 2^k) det≡0 — лишь НЕОБХОДИМОЕ, но не достаточное условие коллинеарности; таблицы Hjelmslev/ring-arc (Honold–Kiermaier–Landjev, Kurz) относятся к БОЛЕЕ СЛАБОМУ понятию линии и НЕ сертифицируют законность в Z². Эмпирически A(p²)/p²≈0.8<1.5.
- Классическая верхняя граница по-прежнему тривиальная 2n (без улучшения со времён Дюдени, 1917); Green (Problem 72) считает оптимальным именно 3n/2 и формулирует тентативную «алгебраическую» гипотезу; ни одна опубликованная работа не даёт семейства A(m)/m>3/2.

## Key Findings
Центральный вывод обзора отрицательный и решающий: маршрут «сильных модулярных дуг» A(m) с определением det≡0 (mod m) доказуемо упирается в отношение ≈1 для бесквадратных m и <1 для степеней простых, поэтому не способен превзойти барьер 3n/2 — рекорд Hall–Jackson–Sudbery–Wild (1975) достигается принципиально иным механизмом: законностью троек напрямую над Z (через структуру гиперболы mod p), а НЕ арк-условием по фиксированному модулю. Единственные семейства, где эта оценка формально неприменима, — модули, делящиеся на p² (несвободные от квадратов), и именно там надо искать; но имеющиеся данные (m₂(Z²_25)=20) пока против.

Точная библиография рекорда: **R. R. Hall, T. H. Jackson, A. Sudbery, K. Wild, «Some advances in the no-three-in-line problem», J. Combin. Theory Ser. A 18 (Issue 3, May 1975) 336–341**, DOI 10.1016/0097-3165(75)90043-6. Конструкция кладёт точки на модулярную гиперболу xy≡k (mod p), p≈n/2, давая 3(p−1) точек в сетке 2p×2p, т.е. (3/2−ε)n.

---

## Q1. Дуги в плоскостях над кольцами Z_m (Hjelmslev, chain rings, Galois rings)

**Прямой ответ и источники.**

**(a) Stępień, Szymaszkiewicz, «Arcs in Z²_{2p}», J. Combin. Optim. 35 (2018) 341–349**, DOI 10.1007/s10878-017-0171-8, препринт arXiv:1512.02175. (Важно: опубликованная статья 2018 г. имеет ДВУХ авторов — Zofia Stępień и Lucjan Szymaszkiewicz. Вариант с пятью авторами, включая Alicja Szymaszkiewicz, — это отдельная заметка про тор, Discrete Math. 339 (2016) 217–221.)

Ключевые результаты (verbatim):
- Lemma 2.1: «Let p be an odd prime, then τ(Z²_p)=p+1.»
- Lemma 2.2 (субмультипликативность, из Kurz): «τ(Z²_{mn}) ≤ min{m·τ(Z²_n), n·τ(Z²_m)} for coprime integers m,n>1.»
- Theorem 2.5: для различных простых p₁≠p₂ «points a,b,c∈Z²_{p₁·p₂} are in a line if and only if D(a,b,c)=0.» — т.е. для бесквадратного m понятия «коллинеарны как линия кольца» и «det≡0» СОВПАДАЮТ.
- Remark 2.6: «Generally, zeroing of determinant is necessary but not sufficient for three points to be collinear. Let p²|m … but these points are not collinear.» (пример (0,0),(p,0),(0,p), у которых det≡0).
- Theorem 3.1: «τ(Z²_{2p}) ≤ 2p+2 and τ(Z²_{2p})=2p+2 for p=3,5.» Remark 3.2: «We conjecture that p=3 and 5 are the only values for which the equality holds.»
- Theorem 3.3: полная дуга X⊂Z²_p поднимается отображением α₂ до полной дуги α₂(X)⊂Z²_{2p}.

**Является ли 3(p−1) максимальным в Z²_{2p}? — Прямой ответ: НЕТ, и это ложная посылка задания.** Множество HJSW из 3(p−1) точек ЗАКОННО в Z² (нет трёх коллинеарных над Z), но оно НЕ является сильной дугой с условием det≡0 (mod 2p): при p≥7 имеем 3(p−1)=3p−3 > 2p+2 ≥ A(2p), что прямо противоречит определению сильной модулярной дуги. Строгий максимум сильной модулярной дуги A(2p) ограничен 2p+2 (SS Thm 3.1) и равен ему лишь при p=3,5. Иными словами, HJSW сертифицирует незаконность троек напрямую над Z, а не как арк по модулю 2p.

**(b) Kurz, «Caps in Z²_n», arXiv:1401.4333** (2000 MSC 51E22; 51C05). Определяет линию как сдвиг циклической подгруппы; Lemma 2.5: «If n=a·b with coprime a and b, then three points p₁,p₂,p₃∈Z²_n are collinear if and only if both projections into Z²_a and Z²_b give a collinear point set.» Lemma 2.7: для степени p^r при обратимости одного из миноров условие det≡0 достаточно. Замечание: в Z²_8 точки (0,0),(2,4),(4,4) удовлетворяют det≡0, но НЕ коллинеарны как линии кольца. Валидировано m₂(Z²_25)=20. Даётся алгоритм проверки коллинеарности за O(log n) с использованием факторизации n.

**(c) Hjelmslev-плоскости (ring-line notion).**
- **Honold, Kiermaier, Landjev, «New Results on Arcs in Projective Hjelmslev Planes over Small Chain Rings», arXiv:2409.02099 (3 Sep 2024)**: «We present various new constructions and bounds for arcs in projective Hjelmslev planes over finite chain rings of nilpotency index 2. For the chain rings of cardinality at most 25 we give updated tables with the best known upper and lower bounds for the maximum size of such arcs.»
- **Honold, Kiermaier, «The existence of maximal (q²,2)-arcs in projective Hjelmslev planes over chain rings of length 2 and odd prime characteristic», Des. Codes Cryptogr. 68 (2013) 105–126**, DOI 10.1007/s10623-012-9653-y: «We prove that (q²,2)-arcs exist in the projective Hjelmslev plane PHG(2,R) over a chain ring R of length 2, order |R|=q² and prime characteristic. For odd prime characteristic, our construction solves the maximal arc problem.» Для Galois-кольца нечётной характеристики p²: дуги размера (q+1)²/4.
- **Kiermaier, Koch, Kurz, «2-arcs of maximal size in the affine and the projective Hjelmslev plane over Z_25», Adv. Math. Commun. 5 (2011) 287–301**, arXiv:1401.4340: макс. 2-дуга в PHG(2,Z_25) = 21 (единственна с точностью до изоморфизма), в AHG(2,Z_25) = 20. Сводная таблица m₂(R): для чётного q и Galois-кольца — гиперовал q²+q+1; q нечётного и R не Galois — q²; q нечётного и R Galois — между ((q+1)/2)² и q² (наименее изученный случай).
- **Kiermaier, Kohnert, «New arcs in projective Hjelmslev planes over Galois rings» (OC2007), phg07.pdf**, + online-таблицы (algorithm.uni-bayreuth.de): n₂(R) для Galois/chain rings малого порядка (Z4:7, Z9:9, Z25:21, GR(16,4):21, и т.д.).

**КРИТИЧЕСКОЕ ПРЕДОСТЕРЕЖЕНИЕ (два понятия коллинеарности).** Существуют ДВА разных понятия: (i) det≡0 (mod m) и (ii) «три точки лежат на общей линии Hjelmslev-плоскости / смежном классе циклической подгруппы». Для БЕСКВАДРАТНОГО m они совпадают (SS Thm 2.5, Kurz Lemma 2.5), и только тогда таблицы Hjelmslev-дуг переносятся на det-условие и сертифицируют законность в Z². Для m, делящегося на p², det≡0 — лишь необходимое условие; Hjelmslev/ring-line дуга МОЖЕТ БЫТЬ СТРОГО БОЛЬШЕ det-дуги (меньше троек считаются коллинеарными). Поэтому большая Hjelmslev-дуга mod p² НЕ даёт законного множества в сетке; безопасно только det≡0. Все таблицы Honold–Kiermaier–Landjev и Kurz для степеней простых — по ring-line понятию, и НЕ переносятся напрямую.

*Что было бы новым:* явное семейство det≡0-дуг A(m) с A(m)/m>3/2 (в литературе отсутствует), либо теорема о том, что det-дуга mod p² асимптотически совпадает с ring-arc.

---

## Q2. Малые точные значения

- **Kurz (arXiv:1401.4333)**: значения m₂(Z²_n) вычислены для n≤21 методом ILP, плюс m₂(Z²_25)=20.
- **Stępień–Szymaszkiewicz (2018)**: вычислены недостающие τ(Z²_22) и τ(Z²_24) (solver Gurobi; τ(Z²_22) потребовал теории арок, ILP напрямую не справился); τ(Z²_p)=p+1; τ(Z²_6)=8, τ(Z²_10)=12 (=2p+2 для p=3,5).
- **OEIS**: A272651 — максимум no-3-in-line в сетке n×n (классическая задача, Euclidean lines); A000769 — число классов эквивалентности решений на 2n; A000755 — общее число решений; A277433 — минимальные насыщенные. **Специальной OEIS-последовательности для «max det≡0-дуги в Z²_m» я не нашёл — отдельной последовательности нет** (это пробел, который вычисления пользователя могли бы заполнить).
- **Hjelmslev-таблицы**: Kiermaier–Kohnert (phg07.pdf), online-таблицы Bayreuth, HKL arXiv:2409.02099 — n₂(R) для Galois/chain rings порядка ≤25–27.

*Что было бы новым:* опубликованная таблица именно A(m)=max det≡0-дуги для всех m≤30; в литературе такой таблицы для det-понятия при непростых степенях нет.

---

## Q3. CRT-склейки

**Прямой ответ.** Механизм CRT для коллинеарности описан явно и однозначно:
- Kurz Lemma 2.5 и SS Theorem 2.5 (см. Q1): для взаимно простых сомножителей тройка коллинеарна ⟺ коллинеарна проекция по каждому сомножителю. Следствие: A(mn) (для взаимно простых m,n) — это в точности множества, чьи обе проекции суть дуги; отсюда субмультипликативная оценка A(mn)≤min{m·A(n), n·A(m)}.
- **Fowler, Groot, Pandya, Snapp, «The no-three-in-line problem on a torus», arXiv:1203.6604**: «T(Z_p×Z_{p²})=2p, T(Z_p×Z_{pq})=p+1. Via Gröbner bases, we compute T(Z_m×Z_n) for 2≤m≤7 and 2≤n≤19.» Здесь линия = смежный класс циклической подгруппы (тороидальное понятие). Это ближайший к «CRT-склейкам разных модулей» результат.
- **Misiak, Stępień, A. Szymaszkiewicz, L. Szymaszkiewicz, Zwierzchowski, «A note on the no-three-in-line problem on a torus», Discrete Math. 339 (2016) 217–221**, arXiv:1406.6713: «at most 2 gcd(m,n) points can be placed with no three in a line on an m×n discrete torus. In the situation when gcd(m,n) is a prime, we completely solve the problem.»

**Почему HJSW — про 2p, а не 3p/4p/5p (структурный анализ).** В опубликованной литературе я НЕ нашёл строгого доказательства невозможности обобщения HJSW до kp×kp с плотностью >3/2 для k≥3. HJSW используют именно две «копии» гиперболы mod p в сетке 2p×2p (отсюда 3p≈1.5·2p). Формального препятствия к 3p, 4p не опубликовано — это наблюдение, а не теорема. Однако субмультипликативная оценка (Q4/Key Findings) показывает, что для det-дуги над Z_{kp} отношение всё равно →1, что косвенно объясняет отсутствие успеха на этом пути. Отдельно отмечу: недавнее полное решение задачи no-(k+1)-in-line при БОЛЬШИХ k (см. Q5) использует доминирование малого числа «тяжёлых» линий, а не CRT-склейку.

*Что было бы новым:* доказанное препятствие к CRT-обобщению HJSW на kp (k≥3) с сохранением плотности 3/2, либо конструкция, его достигающая одновременно по нескольким модулям.

---

## Q4. Вопрос Грина (точная формулировка)

**Green, «100 open problems», Problem 72** (Section 9, «Discrete and combinatorial geometry»), https://people.maths.ox.ac.uk/greenbj/papers/open-problems.pdf (последнее обновление December 2025).

Точная формулировка (verbatim):
> «**Problem 72.** What is the largest subset of the grid [N]² with no three points in a line? In particular, for N sufficiently large is it impossible to have a set of size 2N with this property?»

Комментарий (verbatim, ключевые фрагменты):
> «Specific cases of this problem date back to Dudeney over 100 years ago. … It was shown in [167] that for arbitrary N one can have (3/2 + o(1))N such points, and my personal suspicion is that this is optimal. It is possible that any no-three-in-a-line subset of [N]² is either small, or has a large subset which reduces (mod p) to a set of points on a curve in F²ₚ. It might be interesting to formulate a precise conjecture of this type and see whether it can be used to show that the construction of [167] is optimal. I would find this a lot more convincing than the heuristic given by Guy and Kelly [165].»
> «An interesting related question is the following: is there a subset A ⊂ Z² with no three points on a line, and with |A∩[−N,N]²| ⩾ cN for some absolute constant c>0 and all sufficiently large N? The answer to this may well be no, as conjectured by Erde [102, Conjecture 5.1]. … On the other hand, Nagy, Nagy and Woodroofe [235] take the contrary view, and provide numerical evidence based on greedy constructions that c may exist and be at least around 0.8.»
> «Update 2025. Finally we mention the recent work of Grebennikov and Kwan [139], in which it is shown that for sufficiently large k (k > 10³⁷ will do) it is possible to place kN points in the grid with no (k + 1) on a line, provided N ⩾ N₀(k).»

**Green формулирует «алгебраическую» гипотезу тентативно** («It is possible that…», «It might be interesting to formulate a precise conjecture») — это НЕ строгая гипотеза, а приглашение её сформулировать. Green явно считает 3n/2 оптимальным (в отличие от эвристики Guy–Kelly ~1.814n и мнения Brass–Moser–Pach ~2n).

**Соседние релевантные проблемы того же раздела** (все — про сетки/арки/коллинеарность, verbatim):
- **Problem 68**: «Suppose that A⊂F²ₚ is a set meeting every line in at most 2 points. Is it true that all except o(p) points of A lie on a cubic curve?»
- **Problem 69**: «Fix a number k. Let A⊂R² be a set of n points, with no more than k on any line. Suppose that, for at least δn² pairs of points (x,y)∈A×A, the line xy contains a third point of A. Is there some cubic curve containing at least cn points of A, for some c=c(k,δ)>0?»
- **Problem 71**: «Suppose that A⊂R² is a set of size n with cn² collinear 4-tuples. Does it contain 5 points on a line?»
- **Problem 74**: «What is the largest subset of [N]^d with no 5 points on a 2-plane?»

**Кто цитирует.** No-(k+1)-in-line problem for k≥3, **arXiv:2607.05255, Remark 1.2**: «All previous constructions for small k have been "algebraic", in the sense that they are based on algebraic curves in an affine plane (Z/pZ)² for some prime p≤n (in fact, Green [17] asked whether every "large" no-three-in-line set reduces to an algebraic curve modulo some prime).» Также Grebennikov–Kwan arXiv:2510.17743; Kovács–Nagy–Szabó arXiv:2502.00176; Ghosal arXiv:2605.07000.

*Замечание о нумерации ссылок:* в манускрипте Грина внутренние номера ([167]=HJSW, [165]=Guy–Kelly, [164]=Guy's book, [235]=Nagy–Nagy–Woodroofe, [102]=Erde) менялись между версиями. Verbatim-текст Problem 72 подтверждён по актуальному PDF (fetch субагента), но типографику «(3/2 + o(1))N» стоит сверять при цитировании.

*Что было бы новым:* точная формализация «алгебраической» гипотезы Грина + любой частичный результат в её сторону (в литературе отсутствует).

---

## Q5. Верхние границы

**Прямой ответ: ничего лучше тривиальной 2n не известно — даже 2n−1.** Ghosal (arXiv:2605.07000): «An upper bound of 2n follows immediately by noticing that there can be at most 2 points on each of the n vertical lines of the grid. Interestingly, this is the best-known upper bound on f(n) for any n.» Аналогично **arXiv:2607.05255**: «the best known upper bound 2n comes from the observation that each of the n horizontal lines can contain at most two points» — и это остаётся лучшей границей более 100 лет со времён Дюдени (1917).

Эвристики (НЕ доказательства): Guy–Kelly (Canad. Math. Bull. 11 (1968) 527–531) дали 3c³=2π² ⇒ c≈1.874; после указания Gabor Ellmann (март 2004) на ошибку подстановки исправление даёт 3c²=π² ⇒ c≈1.813799 (OEIS A000769, примечание Guy). Детали ошибки теперь опубликованы отдельно: **Paul M. Voutier, «On the Guy–Kelly Conjecture for the No-Three-In-Line Problem», arXiv:2603.00215 (27 Feb 2026)**. Survey «The General Position Problem» (arXiv:2501.19385): «the heuristic probabilistic argument only applies for n≥493, and so the fact that the 2n upper bound can be met for small n is not strong evidence against the conjecture of Guy and Kelly.»

**Важный контекст — обобщение при k≥3 РЕШЕНО.** Ghosal, Goenka, Grebennikov, Keevash, Kwan, Pham, **arXiv:2607.05255 (2026)**: для k≥3 и достаточно больших n максимум no-(k+1)-in-line точно равен kn; ключевое наблюдение — доминирование малого числа «тяжёлых» линий, применён результат Ehard–Glock–Joos о псевдослучайных гиперграфовых паросочетаниях. Grebennikov–Kwan arXiv:2510.17743: «for n ≥ k ≥ 10³⁷ the maximum number of points is exactly kn». Но при k=2 (исходная задача) методы неприменимы — «there are some important statistical differences between the case k=2 and the case k≥3».

Инцидентностных/фурье-препятствий к (2−o(1))n я НЕ нашёл — таких результатов в литературе нет. Для тороидального (Z/nZ)² при простом n «trivial bound for generalised arcs» даёт ≤ (k−1)(n+1)+1 (arXiv:2607.05255), но это другая, «substantially different» задача.

*Что было бы новым:* любое улучшение до 2n−1 (или 2n−c) для бесконечного семейства n — первое нетривиальное продвижение по верхней границе за >100 лет.

---

## Q6. Структурные/устойчивостные результаты

**Прямой ответ.** Наиболее релевантны формулировки самого Грина (Problem 68/69/71, см. Q4) — это прямые inverse/structure-версии «арк ⟹ кубическая/коническая кривая». Эмпирический принцип пользователя (все насыщенные конфигурации содержат тройки, коллинеарные mod 2,3,5,7) как ТЕОРЕМА в литературе НЕ сформулирован — это пробел.

Устойчивость теоремы Сегре (stability of arcs):
- **Segre B., «Ovals in a finite projective plane», Canad. J. Math. 7 (1955) 414–416**: для нечётного q всякий (q+1)-арк в PG(2,q) — коника. Segre также показал (тот же год), что всякий q-арк можно достроить до коники.
- **Boros, Szőnyi, «On the sharpness of a theorem of B. Segre», Combinatorica 6 (1986) 261–268**, DOI 10.1007/BF02579386: полный арк в PG(2,q), q чётное, не гиперовал, имеет ≤ q−√q+1 точек, и построением показано, что для q=s² граница точна.
- **Ball, Blokhuis, Mazzocca, «Maximal arcs in Desarguesian planes of odd order do not exist», Combinatorica 17 (1997) 31–41.**
- Обзор: Ball, Lavrauw, «Arcs in finite projective spaces», EMS Surv. Math. Sci. 6 (2020) 133–172; Ball–Hirschfeld, «Bounds on (n,r)-arcs and their application to linear codes», Finite Fields Appl. 11 (2005) 326–336.

Теорем вида «cn точек в [n]² обязаны содержать много троек, коллинеарных mod малых простых» я НЕ нашёл.

*Что было бы новым:* строгая версия эмпирического наблюдения пользователя — теорема «rigidity mod small primes» для плотных законных множеств; это близко к Green Problem 68/69 и было бы самостоятельным публикуемым результатом.

---

## Q7. Параметрические симметричные семейства

**Прямой ответ.** Прямых аналогов «симметрия + контролируемые дефекты (Eulerian digraph на классах строк), продолжаемых по n» именно для no-three-in-line я НЕ нашёл. Balance-lemma-семейство пользователя (rct4 с одной диагональной петлёй; 3-циклы пар; две петли для чётного n) в опубликованной литературе прямого аналога не имеет. Flammenkamp («Progress in the no-three-in-line problem», J. Combin. Theory Ser. A 60 (1992) 305–311; «…II», 81 (1998) 108–113) исследует классы симметрии (включая rct4) вычислительно, но без параметрической «продолжаемой по n» теории.

Параллели в родственных задачах:
- **Cap sets**: продуктовые/рекурсивные конструкции — Pellegrino (F₃⁴, 20 точек, 1970); Calderbank–Fishburn (c≈2.2101, 1994); Edel (c≈2.217389, 2004; product construction, «union of cap sets is a cap set» при условиях admissibility); улучшение **Tyrrell, «New Lower Bounds for Cap Sets», Discrete Analysis 2023:20, arXiv:2209.10045 (c≥2.218)**; Naslund (анонс 2.2208). Elsholtz–Pach «Exponentially larger affine and projective caps», arXiv:2211.09772 — семейства по простым p.
- **Sidon / perfect difference sets**: Singer, Bose — явные семейства по q=p^k.
- **k-AP-free**: Behrend; Elkin; Green–Wolf — параметрические по масштабам.
- **n-queens / тороидальные**: **Pólya** — решение модулярной задачи существует ⟺ gcd(n,6)=1; линейные семейства col=(a·row) mod n; **Rivin, Vardi, Zimmermann, Amer. Math. Monthly 101 (1994) 629–639**; **Bell–Stevens, «A survey of known results and research areas for n-queens», Discrete Math. (2009)**; Simkin, «A lower bound for the n-queens problem», arXiv:2105.11431 (settles Rivin–Vardi–Zimmermann в экспоненте, но конструкция вероятностная, не алгебраическая). Тороидальные симметричные решения → panmagic/associative squares.

Показательно: в задаче n-queens прежние нижние границы были алгебраическими, а недавние прорывы — вероятностными (random greedy + absorption). Это тот же водораздел «алгебраическое vs. неалгебраическое», что и в вопросе Грина.

*Что было бы новым:* параметрическое семейство четвертьоборотно-симметричных законных конфигураций, заданное формулой n=f(t) — в литературе отсутствует.

---

## Q8. Проекция из 3D

**Прямой ответ.** **Pór, Wood, «No-Three-in-Line-in-3D», Algorithmica 47 (2007) 481–488**, DOI 10.1007/s00453-006-0158-9: «the maximum number of points in the n×n×n grid with no three collinear is Θ(n²).» Lemma 1: «There are at most 2n² points in the n×n×n grid with no three collinear» (каждая X-линия — ≤2 точки, n² линий). Конструкция — moment curve / параболоид mod p. Обобщения: «On the general no-three-in-line problem», arXiv:2106.15621 (произвольная размерность d); Lefmann («No ℓ grid-points in spaces of small dimension»); Sudakov–Tomon; «On Higher Dimensional Point Sets in General Position» (SoCG 2023, drops.dagstuhl.de).

Работ, ПРОЕЦИРУЮЩИХ 3D-множество на плоскость с сохранением no-three-in-line, я НЕ нашёл — общая проекция разрушает коллинеарность непредсказуемо, и специальной техники «lifting/projection» для сертификации в литературе нет. Moment-curve аргумент (Wikipedia «Moment curve»): любая гиперплоскость пересекает кривую момента в ≤d точках, что даёт affine general position; но это конструкция В самой размерности, а не проекция вниз.

*Что было бы новым:* техника проекции 3D-множества Pór–Wood в плоскость с контролем коллинеарности (в литературе отсутствует).

---

## Details: сводная ТАБЛИЦА A(m) / ring-arc максимума для непростых m

| Семейство m | Нижняя граница | Верхняя граница | Источник | Понятие линии |
|---|---|---|---|---|
| p (нечёт. простое) | p+1 | p+1 | Segre 1955; SS Lemma 2.1 | det = ring-line (поле) |
| 2p | α₂-подъём дуги из Z²_p | 2p+2, «=» лишь p=3,5 | SS Thm 3.1, 3.3 | det = ring-line (бескв.) |
| pq (разн. нечёт.) | ≥ подъём дуг проекций | min{p(q+1),q(p+1)} = pq+min(p,q) | SS Lemma 2.2, Thm 2.5 | det = ring-line (бескв.) |
| p² | ((q+1)/2)² (Galois, Hjelmslev) | q²=p² (ring-arc); m₂(Z²_25)=20 | Honold–Kiermaier 2013; Kurz | **ring-line ≥ det** (det строго меньше) |
| 2^k | малые (ILP) | ≤ ring-arc; в Z²_8 (0,0),(2,4),(4,4) det≡0, но не линия | Kurz | **ring-line ≠ det** |
| 2^k·p, общий m=∏pᵢ^aᵢ | — | A(m) ≤ (m/p^a)·τ(Z²_{p^a}) по любому коприм. сомножителю | SS/Kurz Lemma 2.2 | det (безопасно) |

**Решающее следствие субмультипликативной оценки.** Для любого m с взаимно простым разложением m=a·b (a,b>1): A(m) ≤ a·A(b). Взяв b=наибольший простой делитель P с P‖m: A(m) ≤ (m/P)(P+1) = m(1+1/P) → m. Значит для бесквадратных m отношение A(m)/m ≤ 1+1/P, стремящееся к 1 при росте P (значение >3/2 достижимо лишь при P=2, т.е. вырожденно). Для степеней простых данные (m₂(Z²_25)=20 ⇒ 0.8) дают A(p²)/p²<1. **Вывод: маршрут det≡0-дуг не может дать A(m)/m>3/2 ни для одного изучавшегося семейства.**

## Три наиболее конкретные цели для конструкций (ранжировано)

1. **Модуль-степень p^a (несвободный от квадратов).** Единственное семейство, где субмультипликативная оценка НЕ применяется. Нужно: det≡0-дуга (именно det, НЕ ring-line!) mod p² с плотностью >1.5·p². Опора: Remark 2.6 SS показывает, что det≡0-троек «фиктивно» много, значит det-дуга в принципе может отличаться от ring-arc в обратную сторону — но данные (0.8) пока против; проверить для p=3,5,7.
2. **CRT-склейка нескольких модулей для законности НАД Z (не арк по одному модулю).** Это и есть механизм HJSW. Нужно: обобщение на одновременные условия mod p И mod q, дающее >3/2. Опора: Fowler–Groot–Pandya–Snapp (Gröbner), Kurz Lemma 2.5, SS Thm 2.5. Единственный доказанно работающий путь к 3/2.
3. **Параметрическое симметричное семейство «balance lemma».** Опора: аналогии с cap sets (Edel product) и тороидальными queens (Pólya, gcd(n,6)=1; Rivin–Vardi–Zimmermann). Наиболее спекулятивно, но не закрыто ни одной теоремой.

## Явные ТУПИКИ (с причиной)

- **Бесквадратные m (2p, pq, general squarefree)** — доказуемо A(m)/m ≤ 1+1/P → 1 (SS Lemma 2.2 + Thm 2.5). Не превзойдёт 3/2. Причина: субмультипликативность + совпадение det = ring-line.
- **m=p (простое)** — Segre: A(p)=p+1≈m. Закрыто.
- **Hjelmslev/ring-arc mod p² как сертификат законности в Z²** — НЕ работает: ring-line ≠ det для p²|m (SS Remark 2.6; Kurz, пример Z²_8). Большая Hjelmslev-дуга не даёт законного grid-множества.
- **Улучшение верхней границы 2n инцидентностными/фурье-методами** — в литературе НЕТ ни одного результата <2n; препятствий не опубликовано.
- **Наивная проекция 3D→2D** — разрушает коллинеарность; техники сохранения нет.

## Recommendations
1. **Сосредоточить вычисления на p² и p^a с ПРАВИЛЬНЫМ (det≡0) понятием**, а не Hjelmslev: вычислить A(p²) по det-условию для p=3,5,7 и сравнить с ring-arc m₂(Z²_{p²}). Порог смены решения: если A(p²)/p² устойчиво <1 при росте p — семейство закрыть как тупик; если хоть раз >1.5·p² — немедленно публиковать и проверять перенос в grid.
2. **Формализовать эмпирику mod 2,3,5,7** как гипотезу в духе Green Problem 68/69 («плотное законное множество ⟹ большое подмножество на кривой mod p») — самостоятельный публикуемый результат и мост к «алгебраической» гипотезе Грина.
3. **Строить CRT-склейку как HJSW, а не как арк**: искать множества, законные над Z через одновременные условия mod p и mod q; проверить, можно ли превзойти две копии гиперболы (3p в 2p×2p) тремя/четырьмя согласованными кривыми.
4. **Balance-lemma-семейство** — оформить как параметрическую конструкцию n=f(t) по аналогии с Edel product / тороидальными queens; даже суб-2n результат с явной формулой был бы новым (ср. цель №2 в списке Siehler/Guy: «A construction which achieves more than (3n/2) would be new»).
5. Бенчмарк для смены стратегии: появление доказанного улучшения верхней границы <2n (напр. arXiv-препринт) немедленно переориентирует усилия с конструкций на структурные ограничения.

## Caveats
- Посылка «A(2p)≥3(p−1)» НЕкорректна для det≡0-понятия: A(2p)≤2p+2 (SS Thm 3.1). HJSW — законное множество над Z, но НЕ сильная дуга mod 2p; эти два объекта не следует отождествлять.
- Номера внутренних ссылок в манускрипте Грина менялись между версиями; verbatim-текст Problem 72 подтверждён по актуальному PDF (December 2025), но типографику «(3/2 + o(1))N» стоит сверять при прямом цитировании.
- Отдельной OEIS-последовательности для A(m)=max det≡0-дуги не найдено — вычисления пользователя её заполнили бы.
- Полную числовую таблицу Honold–Kiermaier–Landjev 2024 (arXiv:2409.02099) я видел только по абстракту; конкретные ячейки для |R|≤25 нужно извлечь из самого PDF и online-таблиц Bayreuth (algorithm.uni-bayreuth.de).
- Результаты по no-(k+1)-in-line при k≥3 (arXiv:2607.05255, 2510.17743) РЕШЕНЫ, но методы явно не переносятся на исходный случай k=2 — авторы это подчёркивают.
- Эвристики Guy–Kelly (~1.814n) и Brass–Moser–Pach (~2n) — это ПРЕДПОЛОЖЕНИЯ, а не доказанные границы; единственная доказанная верхняя граница — тривиальная 2n.