# Комплексный research / referee report по *The Hall–Jackson–Sudbery–Wild window is tight*

## Итог в двух абзацах

После проверки самого доказательства, независимой вычислительной верификации, сопоставления с оригинальной работой Hall–Jackson–Sudbery–Wild 1975 и версиями Kovács–Nagy–Szabó 2025/2026 мой общий вывод такой: **основная теорема выглядит корректной, а математический вклад — реальным и достаточно интересным для отдельной короткой combinatorics note**. Я не обнаружил контрпримера, логического разрыва или недостающего класса опасных прямых. Более того, независимо от кода, описанного в manuscript, я восстановил point set, перечислял все прямые с ≥3 точками и решал возникающую exact independence problem по компонентам; результаты систематически совпали с
\[
\alpha(P)=3(p-1),\qquad N_{\max}=9^s.
\]

Однако **само утверждение об optimal value \(3(p-1)\) нельзя подавать как впервые обнаруженное**. Hall–Jackson–Sudbery–Wild в 1975 году только построили множество размера \(3(p-1)\), то есть дали lower bound/construction. citeturn107785view0turn517048search1 Но Kovács–Nagy–Szabó уже в arXiv v1 от **11 августа 2025 года** прямо назвали HJSW removal при \(|W|=1,k=2\) an “optimal choice”; в v2 от **21 июля 2026 года** они усилили формулировку до “largest no-3-in-line set \(S_2(c,p)\) inside \(S(W)\)”. citeturn728277view4turn728277view6turn564981view0 При этом я не обнаружил у них полноценного доказательства этого upper bound во всех случаях. И именно здесь у нового manuscript появляется гораздо более сильное и defensible позиционирование: **direct proof + exact structure + classification of all extremizers + LP certificate**.

---

## 1. Что именно здесь математически новое и сильное

В manuscript рассматривается полный набор
\[
P=H(c,p)\cap G(p),
\]
состоящий из \(4(p-1)\) точек, по четыре lift'а каждой из \(p-1\) residue classes. Основной результат говорит, что любое no-three-in-line множество \(S\subseteq P\) удовлетворяет
\[
|S|\le 3(p-1),
\]
причём число максимальных множеств равно
\[
9^s,\qquad
s=[c\text{ is QR}]+[-c\text{ is QR}].
\]
Если \(s=0\), HJSW set является единственным maximizer. fileciteturn0file0L69-L87

Значительная часть ценности результата, на мой взгляд, находится **не в самом числе \(3(p-1)\)**, а в rigidity theorem за ним. Paper отвечает не только на “сколько?”, но фактически на “почему именно столько?” и “какие ровно конфигурации достигают equality?”.

Это существенно сильнее HJSW. Их Theorem 2 утверждает существование no-three-in-line subset размера \(3(p-1)\) и затем проверяет, что их конкретно выбранные 12 blocks действительно lawful. Никакого statement о максимальности среди всех точек той же modular hyperbola в окне там нет. citeturn107785view0

---

## 2. Audit доказательства

Основная proof architecture очень хорошая. Она имеет естественную цепочку
\[
\text{geometry}
\to
\text{classification of rich lines}
\to
\text{incidence certificate}
\to
\text{equality structure}.
\]

### Lemma 2 и Corollary 4

Параметризация lattice line
\[
(x,y)=(x_0+tu,y_0+tv)
\]
сводит условие \(xy\equiv c\pmod p\) к
\[
t\bigl(uvt+x_0v+y_0u\bigr)\equiv0\pmod p.
\]
Отсюда на прямой может встретиться не более двух residue classes. Для slope \(+1\) второй класс оказывается
\[
\sigma(a,b)=(-b,-a),
\]
для slope \(-1\)
\[
\tau(a,b)=(b,a).
\]
Это корректно. fileciteturn0file0L89-L101

Далее четыре copies одного класса образуют axis-parallel \(p\times p\) square. Поэтому если три точки \(P\) лежат на одной прямой, две принадлежат одному классу, а line through such a pair имеет slope \(0,\infty,\pm1\). Horizontal/vertical lines третью точку дать не могут. Следовательно любая rich line имеет slope только \(\pm1\). fileciteturn0file0L102-L111

Я не вижу здесь скрытого genericity assumption. Аргумент покрывает также small primes, включая \(p=3,5\).

### Lemma 5

Это самая bookkeeping-heavy часть текста: действие \(\sigma,\tau\) на типы \(A,B,C,D\), а также shifts \(d_\kappa,e_\kappa\). fileciteturn0file0L114-L130

Формулы согласованы с выбором base representatives и с вычислительной проверкой. Здесь скорее exposition risk, чем mathematical risk: referee легко ошибётся глазами на одной из восьми coordinate transforms. Таблица вида

\[
A\xrightarrow{\sigma}A,\quad
D\xrightarrow{\sigma}D,\quad
B\leftrightarrow C,
\]

\[
B\xrightarrow{\tau}B,\quad
C\xrightarrow{\tau}C,\quad
A\leftrightarrow D
\]

с отдельной колонкой для shift в \(d/e\) сделала бы доказательство заметно легче проверяемым.

### Proposition 6 — центральная структурная часть

Это, по-моему, ядро статьи. Все rich lines полностью классифицированы в четыре семейства: 4-point diagonal lines на \(\sigma\)-pairs, 4-point antidiagonal lines на \(\tau\)-pairs и соответствующие 3-point lines для cross-type partners. Затем получаются
\[
|\mathcal L|
 =\frac32(p-1)-\frac{f_\sigma+f_\tau}{2}
 =\frac32(p-1)-s
\]
и
\[
Z=f_\sigma+f_\tau=2s.
\]
fileciteturn0file0L131-L160

Я бы добавил сюда один маленький missing-exposition lemma: **почему перечисленные линии не могут случайно совпасть между двумя различными partner-pairs**. Это и так следует из Lemma 2: если \(D_\kappa=D_\lambda\), одна и та же slope-\(+1\) line встречает classes \(\kappa,\lambda\), поэтому \(\lambda\in\{\kappa,\sigma\kappa\}\). Аналогично для \(E\) и \(\tau\). Но поскольку дальше количество этих линий буквально используется в theorem certificate, это стоит сказать явно одной фразой.

### Верхняя граница

После Proposition 6 доказательство практически идеально короткое. Если \(m(q)\) — число rich lines через \(q\), то

\[
|S|
\le
Z+
\sum_{\ell\in\mathcal L}|S\cap\ell|
-
\sum_{q\in S}(m(q)-1)^+
\le Z+2|\mathcal L|.
\]

Следовательно
\[
|S|\le 2s+2\left(\frac32(p-1)-s\right)=3(p-1).
\]
fileciteturn0file0L182-L207

Это хороший proof именно потому, что не требует delicate extremal manipulation. Полная геометрическая сложность была заранее упакована в \(\mathcal L\) и \(Z\).

Единственная косметическая правка: определить
\[
x^+=\max\{x,0\}
\]
перед формулой (3).

### Equality case

Equality требует одновременно: взять все \(m=0\) points, насыщать каждую rich line ровно двумя выбранными точками и не выбирать ни одной точки с \(m=2\). fileciteturn0file0L208-L217

Дальше decomposition по Klein group
\[
\langle\sigma,\tau\rangle
=\{1,\sigma,\tau,\nu\}
\]
работает хорошо.

Generic 4-class orbit содержит 16 points. Четыре middle-block copies имеют \(m=2\) и обязаны быть исключены; оставшиеся 12 имеют \(m=1\) и все forced. Поэтому там extremizer совпадает с HJSW.

Nongeneric 2-class orbit состоит из двух fixed-partner classes. Он содержит две disjoint 3-point constraints и две isolated \(m=0\) points. Isolated points forced, а из каждой тройки нужно выбрать ровно две точки:
\[
{3\choose2}{3\choose2}=9.
\]
Каждый такой orbit поэтому вносит independent factor 9.

Я бы здесь добавил буквально предложение: every line of \(\mathcal L\) stays inside a single \(\langle\sigma,\tau\rangle\)-orbit, поскольку её два возможных classes связаны \(\sigma\) или \(\tau\). Тогда независимость факторов \(9\) полностью формализована.

---

## 3. Особенно красивое следствие, которого сейчас почти не видно

Формула \(9^s\) допускает гораздо более прозрачную reformulation.

Если
\[
p\equiv3\pmod4,
\]
то \(-1\) — quadratic nonresidue. Поэтому ровно одно из \(c,-c\) является quadratic residue и
\[
s=1.
\]
Следовательно **для любого \(c\ne0\) имеется ровно 9 maximum sets**.

Если
\[
p\equiv1\pmod4,
\]
то \(-1\) — quadratic residue, поэтому \(c\) и \(-c\) имеют одинаковый QR status. Значит:

\[
c\text{ QR}\quad\Rightarrow\quad s=2,\quad N_{\max}=81,
\]

а

\[
c\text{ NQR}\quad\Rightarrow\quad s=0,\quad N_{\max}=1.
\]

Иными словами, очень чистый corollary:

**HJSW configuration is the unique maximum iff**
\[
p\equiv1\pmod4
\quad\text{and}\quad
c\text{ is a quadratic nonresidue}.
\]

Я бы вынес это непосредственно после Theorem 1. Это значительно запоминаемее определения \(s\), а сейчас manuscript иллюстрирует только частный случай \(c=1\). fileciteturn0file0L79-L87

---

## 4. Независимая computational verification

Я специально не полагался на script/SAT log, заявленные в paper. Там авторский verifier сообщает проверку primes до \(101\), включая exact maxima и число extremizers. fileciteturn0file0L233-L256

Я построил отдельный checker с другой логикой. Для каждого \(p,c\) сначала непосредственно генерировался
\[
P=\{(x,y)\in G(p):xy\equiv c\pmod p\}.
\]
Затем **по всем парам точек** восстанавливались нормализованные Euclidean lines, а не только линии предполагаемых slopes. После deduplication выбирались все линии, содержащие минимум три points. Они становились hyperedges exact no-three-in-line constraint problem. Полученный constraint hypergraph разбивался на connected components; внутри компонент exact maximum и число maxima определялись exhaustive enumeration, после чего компоненты перемножались.

Полностью проверены все \(c\in\mathbf F_p^\*\) для каждого prime
\[
p\le31,
\]
а также наборы \(c=1,2,3,-1,-2,(p+1)/2\) для
\[
p=37,43,59,73,101.
\]

Во всех случаях получено ровно
\[
\alpha(P)=3(p-1)
\]
и
\[
N_{\max}=9^s.
\]

Кроме того, при полном enumerating всех pair-determined lines ни в одном тесте не появилась rich line slope, отличного от \(+1,-1\).

Это, конечно, не заменяет proof, но хорошо проверяет именно те места, где вероятнее всего могла скрываться bookkeeping error: Proposition 6, exceptional fixed classes и equality count.

---

## 5. Prior art: что было у HJSW

Оригинальная paper Hall–Jackson–Sudbery–Wild 1975 совершенно явно представляет \(3(p-1)\) как **construction**. Introduction говорит: при \(n=2p\) они “can construct” no-three-in-line subset with \(3(p-1)\) points, а Theorem 2 формулируется как existence theorem. citeturn107785view0turn517048search1

Их proof затем определяет конкретный набор из 12 blocks и доказывает, что в нём нет collinear triples. citeturn107785view0

Таким образом, я не вижу основания считать, что HJSW уже доказали
\[
\alpha(H(c,p)\cap G(p))=3(p-1).
\]

В этом отношении новый manuscript действительно делает нечто существенно более сильное, чем работа 1975 года.

---

## 6. Prior art: важная ситуация с Kovács–Nagy–Szabó

Здесь необходима максимальная аккуратность.

KNS paper была первоначально размещена на arXiv **11 августа 2025 года**; current v2 датирована **21 июля 2026 года**. На 18 августа 2026 года arXiv указывает journal reference *Advances in Combinatorics 2026:7* и планируемую дату публикации **18 сентября 2026 года**. citeturn564981view0

В основной Subsection 2.2 current version их Theorem 2.8 говорит только:

\[
S_2(c,p)=H(c,p)\cap T_2
\]
есть no-three-in-line set размера \(3(p-1)\), поэтому
\[
f_2(2p)\ge3(p-1).
\]

И proof действительно проверяет только cardinality и отсутствие triple lines. citeturn728277view5

Однако уже **v1** позже говорит:

> for \(|W|=1\) and \(k=2\), Subsection 2.2 “essentially details an optimal choice” of removed points.

И далее авторы говорят, что эти local subtasks can be solved optimally. citeturn728277view4

В **v2** statement стал ещё более прямым: HJSW removal назван optimal choice, позволяющим получить the **largest no-3-in-line set \(S_2(c,p)\) inside \(S(W)\)**. citeturn728277view6

Следовательно приоритет на **assertion**
\[
\alpha(P)=3(p-1)
\]
у KNS публично существует по крайней мере с 11 августа 2025 года.

Это главный факт, который необходимо исправить в positioning manuscript.

---

## 7. Новая находка: где именно KNS machinery не даёт весь новый theorem автоматически

Это, пожалуй, наиболее интересное наблюдение всего comparison.

В Construction 3.2 KNS берут полный \(S(W)\) и удаляют минимальное множество \(R\), чтобы на каждой slope-\(\pm1\) line осталось не больше \(k\) points. Они вводят
\[
X_{k,p}(W)
=
\sum_{\ell}
\max\{0,|\ell\cap S(W)|-k\}
\]
и доказывают общий bound
\[
\frac12X_{k,p}(W)\le |R|\le X_{k,p}(W).
\] citeturn728277view7

Теперь применим **структурную классификацию нового manuscript** к \(W=\{c\},k=2\).

В \(P\) имеется ровно \(p-1\) three-point rich lines. Число four-point rich lines равно
\[
\frac{p-1-(f_\sigma+f_\tau)}2
=
\frac{p-1-2s}{2}.
\]

Следовательно, как мой вывод из двух papers,

\[
X_{2,p}(\{c\})
=
(p-1)+
2\frac{p-1-2s}{2}
=
2(p-1)-2s.
\]

Общий KNS lower bound поэтому даёт только

\[
|R|
\ge
\frac{X}{2}
=
p-1-s.
\]

Но чтобы доказать новый theorem,
\[
|S|\le3(p-1),
\]
из \(|P|=4(p-1)\) нужно
\[
|R|\ge p-1.
\]

То есть KNS generic averaging certificate **точен при \(s=0\)**, но при \(s=1\) теряет одну deletion, а при \(s=2\) — две.

Это очень содержательно.

При
\[
s=0
\]
оптимальность HJSW value практически уже следует из их общего framework плюс HJSW construction.

Но exceptional fixed-class cases
\[
s=1,2
\]
этот displayed general bound сам по себе не закрывает.

И именно здесь новый manuscript вводит
\[
Z=2s
\]
exceptional points и получает более точный certificate
\[
Z+2|\mathcal L|=3(p-1).
\]

То есть новый argument можно интерпретировать как **exact correction to the KNS averaging bound at the fixed classes**.

Это, на мой взгляд, очень сильный способ связать papers в Introduction. Вместо конкуренции “они задали вопрос — мы решили” появляется более точная история:

KNS recognized the HJSW deletion as optimal; their general averaging framework explains the generic case; the present structural analysis yields an exact certificate in all cases and completely determines equality.

Я в просмотренном тексте KNS не нашёл отдельного proof, который восполняет эту \(s\)-gap для \(s>0\). Это не доказательство того, что такого аргумента у авторов никогда не было, поэтому в manuscript нельзя писать “KNS did not prove it” без оговорки. Правильная формулировка — “we are not aware of a proof appearing in [2]” или, ещё лучше, предварительно спросить авторов.

---

## 8. Что с novelty после этого comparison

После research я бы разделил claims так.

**Exact numerical optimum \(3(p-1)\):** ново как theorem/proof, возможно, но **не ново как публичное assertion**, поскольку KNS называли HJSW removal optimal уже в v1.

**Direct self-contained upper-bound proof for arbitrary \(c\):** выглядит новым. Особенно содержательны exceptional fixed-class cases.

**Complete classification of every rich line:** я не нашёл её в таком виде в prior literature. HJSW/KNS знают достаточно slope-\(\pm1\) structure для своих constructions, но Proposition 6 значительно сильнее — это exact incidence structure всего \(P\).

**LP/fractional certificate:** выглядит новым и концептуально интересным. Manuscript фактически доказывает, что даже fractional relaxation имеет optimum \(3(p-1)\). fileciteturn0file0L218-L221

**Classification of all maximizers and formula \(9^s\):** это, по результатам targeted literature search, наиболее чистая novelty. Я не нашёл другого occurrence ни формулы \(9^s\), ни uniqueness statement, ни 9/81 classification для этого problem.

Я проводил отдельные searches по combinations “modular hyperbola”, “HJSW”, “largest/maximum”, “\(9^s\)”, “81 maximum”, “unique maximum” и просмотрел ближайшую литературу по modular hyperbolas/no-three-in-line. Никакого competing equality-classification result не surfaced. Это повышает уверенность, но, естественно, не может математически доказать отсутствие unpublished или трудно индексируемой работы.

---

## 9. Я бы изменил центральный narrative статьи

Текущий Remark 7(b) говорит, что theorem “settles ... the question raised there whether the HJSW construction can be improved”. fileciteturn0file0L222-L229

Эту формулировку нужно убрать. KNS не просто raised the question: они уже asserted optimality. citeturn728277view4turn728277view6

Гораздо сильнее и безопаснее звучит примерно такая история:

“Kovács, Nagy and Szabó observed/stated that for a single modular hyperbola the HJSW deletion is optimal. We give an exact structural proof of this assertion. We classify every line containing at least three points of the full HJSW window, derive an explicit linear-programming certificate for the bound \(3(p-1)\), and classify all equality cases.”

Это не defensive wording. Наоборот, оно подчёркивает, что contribution представляет собой **solution of the complete extremal structure**, а не просто повтор числа, которое уже фигурировало в литературе.

---

## 10. Title и abstract

Текущий title *The HJSW window is tight* ставит на первое место ровно ту часть claim, которая уже была asserted KNS.

Я бы предпочёл:

**Extremal no-three-in-line subsets of a modular hyperbola in the Hall–Jackson–Sudbery–Wild window**

или более короткий:

**Optimality and extremizers in the Hall–Jackson–Sudbery–Wild window**

Первый вариант мне кажется наиболее journal-safe: он сразу обещает exact extremal analysis.

В abstract также нужно буквально одной clause признать KNS assertion. Сейчас abstract после описания HJSW сразу говорит “We prove that this is optimal”. fileciteturn0file0L16-L32 Лучше дать readers chronology сразу, а затем продать новые части: exact proof, LP certificate, all extremizers.

---

## 11. Структура статьи

Сейчас после Abstract почти сразу начинается “Statement” и notation. fileciteturn0file0L33-L58 Для пятистраничной note это допустимо, но после обнаруженного priority nuance я бы добавил примерно полстраницы Introduction.

Она должна объяснить HJSW 1975 → KNS 2025/26 → exact question solved here → contributions. Особенно полезно прямо различить “construction optimality was stated” и “we determine the complete extremal structure”.

Equality analysis заслуживает маленькой figure. Один generic 4-class orbit и один exceptional 2-class orbit сделали бы proof of \(9^s\) практически визуальным:

generic gadget:
16 points → 4 forbidden middle points → remaining 12 forced;

exceptional gadget:
8 points → 2 isolated forced + two triples → \(3\times3=9\).

При таком рисунке самая новая часть paper станет одновременно самой понятной.

---

## 12. Computer section

Section 4 полезен, но его роль я бы немного понизил. Теорема имеет self-contained short proof; поэтому computational verification следует подавать как independent sanity check, а не как часть основания доверять result.

Сейчас называются конкретные paths
`slack/hjsw window check.py`,
`bench/hjsw window check all.log`,
SAT encodings и verifier, но из самого PDF не следует, где получить repository. fileciteturn0file0L233-L247

Перед submission здесь нужен public repository URL и желательно immutable commit hash/tag или archived release. Это особенно важно из-за заявленной AI-generated provenance: reproducibility становится одной из сильных сторон работы, и стоит её довести до standards настоящего computational supplement.

---

## 13. Authorship / AI disclosure — важный submission issue

Титульная страница сейчас пишет:

“with three autonomous Claude agents (Anthropic); this note was written by the third agent”. fileciteturn0file0L5-L8

В конце также прямо сказано, что theorem, proof и verification program были produced by an autonomous Claude agent, а owner поставил question. fileciteturn0file0L261-L264

Прозрачность хорошая, но **такой вид byline я бы не оставлял**.

Текущая официальная policy arXiv требует disclosure significant use of generative AI, подчёркивает, что named human authors несут полную ответственность за content, и прямо говорит, что generative AI language tools **should not be listed as an author**. citeturn728277view1turn728277view2

Поэтому правильнее оставить human authors в author line, а AI involvement подробно описать в “AI/tool-use disclosure” или acknowledgements/methodology.

Причём disclosure можно оставить очень прозрачным: theorem discovery, proof search, drafting и program generation осуществлялись с существенной помощью autonomous LLM agents; указать модели/process/repository; затем human author принимает ответственность за submitted statements.

Ключевой практический момент: если human author ещё **не провёл собственную line-by-line verification proof**, это стоит сделать до submission. Не ради косметики: arXiv policy буквально возлагает responsibility на named author. citeturn728277view1

---

## 14. Приоритетный план до submission

1. **Связаться с KNS до публичного claim “first proof”.** Отправить им theorem statement и спросить, имеется ли у них записанный или intended proof фразы “optimal choice / largest no-3-in-line set”, особенно для fixed-class cases \(s>0\). Это один email, который может полностью снять priority uncertainty.

2. **Перепозиционировать novelty.** Основные selling points: exact structural proof, classification of all rich lines, LP certificate, equality classification \(9^s\), uniqueness.

3. **Переписать Remark 7(b) и добавить Introduction.** Не говорить, что KNS лишь raised the question. Прямо признать их prior assertion.

4. **Усилить Proposition 6/equality exposition.** Добавить отсутствие duplicate rich lines, independence of Klein-four orbits, определение \(x^+\), и желательно маленькую orbit figure.

5. **Добавить QR corollary.** При \(p\equiv3\pmod4\) всегда 9 maxima; при \(p\equiv1\pmod4\) — 81 для QR \(c\), unique для NQR \(c\).

6. **Сделать verification reproducible.** Public repository, immutable version, commands/environment, лог проверок. Отдельно сохранить independent implementation, если хочется особенно сильного reproducibility claim.

7. **Исправить authorship presentation.** AI tools — disclosure, не coauthor/byline; human author explicitly assumes responsibility только после собственной проверки.

---

## 15. Referee-style оценка

**Correctness:** высокая уверенность. Я не нашёл существенной ошибки; independent exact computation подтверждает theorem в широком диапазоне параметров.

**Significance:** хорошая для concise combinatorics note. Это не решение глобального no-three-in-line problem, но очень чистый exact extremal theorem внутри важной классической construction.

**Originality of \(3(p-1)\) value:** низкая как claim — KNS asserted it раньше.

**Originality of proof:** вероятно высокая для all-\(c\) exact statement, особенно fixed-class cases, но перед категоричным “first proof” разумно получить clarification от KNS.

**Originality of \(9^s\) extremizer classification:** высокая по результатам проведённого literature search.

**Originality of LP/fractional certificate:** также выглядит высокой.

**Exposition:** proof short and elegant, но relation to prior work сейчас сформулирована недостаточно точно, а наиболее новая equality structure недопродана.

**Submission readiness v0.1:** major revision.

**Submission readiness после перечисленных исправлений:** я бы считал paper вполне серьёзным кандидатом на submission как короткую research note.

---

## 16. Моя главная рекомендация

Я бы не строил статью вокруг лозунга

\[
\boxed{\text{“We discovered that }3(p-1)\text{ is optimal.”}}
\]

Исторически это уязвимо.

Я бы строил её вокруг более сильного утверждения:

\[
\boxed{\text{“We completely solve the extremal problem inside the HJSW window.”}}
\]

То есть вы не просто получаете optimum. Вы описываете **всю obstruction geometry**, даёте **exact LP certificate**, объясняете **почему exceptional quadratic-residue classes являются единственным источником nonuniqueness**, а затем считаете **каждый maximizer**.

И особенно удачным мне кажется новое conceptual connection с KNS:
\[
\frac12X=p-1-s
\]
показывает ровно, где их general averaging bound теряет information, тогда как
\[
Z=2s
\]
в новом incidence certificate восстанавливает недостающую correction и одновременно объясняет \(9^s\).

Вот это уже не просто proof известного числа. Это структурное объяснение того, **почему HJSW window устроено именно так**.

Мой итоговый verdict: **математику сохранять, paper развивать и подавать; novelty narrative существенно переписать. Самые ценные новые результаты — Proposition 6 + exact certificate + full equality classification, а не голое число \(3(p-1)\).**