# OEIS — что и куда вставлять. Две правки, обе в существующие последовательности.

Заводить новые последовательности не нужно. Нужно добавить комментарии к двум имеющимся.

---

## ПРАВКА 1 — A280537 (трёхмерная, наши девять границ)

**Ссылка:** https://oeis.org/A280537
**Действие:** войти → на странице последовательности нажать **«edit»** → в поле **COMMENT** добавить.

**Текст (вставить как есть, английский — OEIS принимает только его):**

```
Lower bounds beyond the published data, each certified by an explicit configuration:
a(9) >= 23, a(10) >= 26, a(11) >= 28, a(12) >= 31, a(13) >= 32, a(14) >= 34,
a(15) >= 35, a(16) >= 37, a(17) >= 38.
Each configuration was verified twice by structurally different programs (all C(m,4)
quadruples via 3x3 determinants in exact integer arithmetic; and independently, the plane
of every non-collinear triple checked against every remaining point), together with
distinctness and range checks; the verifier passes a self-test that rejects a deliberately
corrupted witness. The configurations are available at
https://github.com/iwasborninbali/saturation (directory certs/a280537_first_solver).
Also a(n) <= 3n for all n, since each of the n planes x = const carries at most 3 points.
```

**В поле LINK добавить (одной строкой):**

```
Aleksei Kudriashov and Claude agents, <a href="https://github.com/iwasborninbali/saturation">Certified configurations for n = 9..17</a>
```

**Почему комментарием, а не членами:** это НИЖНИЕ ГРАНИЦЫ, а не значения. В поле DATA
идут только доказанные величины; наши свидетели доказывают «не меньше» и никогда «не больше».

---

## ПРАВКА 2 — A000755 (двумерная, кандидат на двадцатый член)

**Ссылка:** https://oeis.org/A000755
**Действие:** то же — **«edit»** → поле **COMMENT**.

**Текст:**

```
Summing the orbit sizes 8/|stabiliser| over the D4-classes in A. Flammenkamp's database
of known solutions (file all_known_solutions, state 2026-08-11) reproduces a(2)..a(19)
exactly, and gives 941580 for n = 20. Hence a(20) >= 941580, with equality if that
database is complete for n = 20. Indirect evidence that it is: the proportion of classes
with non-trivial stabiliser decreases smoothly through n = 20 (3.68%, 4.14%, 1.83%,
1.87%, 0.60% for n = 16..20) and then jumps to 92.63% at n = 21, which is where the
database stops being exhaustive and holds only found (hence overwhelmingly symmetric)
solutions.
```

**Почему НЕ вписывать 941580 в DATA:** полнота базы при n=20 — наш ВЫВОД из косвенного
признака, а не установленный факт. Если Ахим подтвердит полноту, член можно будет добавить
отдельной правкой со ссылкой на его подтверждение. Пока — комментарий.

---

## Порядок действий

1. Регистрация: https://oeis.org/wiki/Special:RequestAccount — нужны имя и краткое описание
   интереса к последовательностям. Одобрение обычно за день-два.
2. После входа — открыть страницу последовательности, нажать «edit» вверху.
3. Вставить текст в нужное поле, внизу заполнить строку **«Comment to editors»**, например:
   `Lower bounds with machine-verified certificates; see the linked repository.`
4. Отправить. Правку смотрит редактор; он может попросить сократить или переформулировать —
   это нормальная часть процесса, отвечать по существу.

**Если редактор спросит про роль ИИ** — говорить как есть: поиск и проверка выполнены
автономными агентами под руководством человека, все результаты перепроверены независимо.
В прошлых публикациях (база Фламменкампа, наши статьи) это указывалось прямо, и вопросов
не вызывало.
