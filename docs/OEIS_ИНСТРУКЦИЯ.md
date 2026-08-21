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
a(15) >= 35, a(16) >= 38, a(17) >= 38, a(18) >= 41, a(19) >= 43, a(20) >= 45, a(22) >= 47, a(23) >= 50.
(Twelve configurations were verified; the bound at n = 17 follows from the one at n = 16 by
monotonicity and is listed for completeness rather than as an independent result.)
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

## ПРАВКА 2 — A000755: ЖДЁМ СЛОВА ФЛАММЕНКАМПА, НЕ ПОДАЁМ

**Положение дел, восстановленное по переписке (важно, я сам его сперва переврал):**

* `a(20) = 941580` — **число Фламменкампа**, оно стоит на его ЖИВОЙ таблице
  `https://wwwhomes.uni-bielefeld.de/achim/no3in/table.html`. Не наше.
* A000769 (неэквивалентные решения, «sum»-столбец той же таблицы) **уже несёт** n=20 = 118057.
  То есть одну последовательность с его страницы обновили, а вторую нет.
* Письмом от 20.08 мы сами ему это написали и **прямо предложили выбор**: вносит он или мы
  с указанием авторства и ссылкой на его таблицу. **Ответа пока нет.**

**Что делаем: НИЧЕГО, пока он не ответит.** Вносить чужое число, предложив автору решать
самому и не дождавшись ответа, — плохо.

**Что появилось сегодня и снимает нашу вчерашнюю оговорку.** Вчера мы написали ему, что
проверить 941580 сами не можем (нашим перебором это порядка 500 ядро-лет). Сегодня проверили
иначе: сумма размеров орбит по его БАЗЕ решений даёт ровно 941580, а та же сумма
воспроизводит A000755 на восемнадцати подряд опубликованных членах (n=2..19) без единого
расхождения. Значит два его источника — таблица и база — согласуются, и это установлено
независимо от его таблицы.

**Когда он ответит «вносите»** — текст комментария к A000755:

```
a(20) = 941580, from A. Flammenkamp's table at
https://wwwhomes.uni-bielefeld.de/achim/no3in/table.html.
Independently confirmed by summing the orbit sizes 8/|stabiliser| over the D4-classes
in his database file all_known_solutions (state 2026-08-11); the same computation
reproduces a(2)..a(19) exactly.
```

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
