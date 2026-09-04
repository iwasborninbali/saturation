# arXiv: просьбы об endorsement для math.CO — черновики (3.09.2026)

## Порядок (без кода письма бесполезны)
1. Владелец регистрируется на https://arxiv.org/user/register с адресом olegmikhb@gmail.com (аффилиация — «Independent researcher», это допустимо).
2. «Start New Submission» → archive **math**, subject class **math.CO**. arXiv скажет «you need endorsement» и покажет
   **endorsement code** (6 знаков) и ссылку вида https://arxiv.org/auth/endorse?x=XXXXXX. Код приходит и письмом.
3. Код/ссылку — мне (или в письмо ниже вместо XXXXXX). Письма уходят с адреса, на который зарегистрирован arXiv-аккаунт,
   иначе endorser не найдёт submitter'а. Правила arXiv: endorser ручается за автора, не рецензирует статью; просить можно,
   давить нельзя; отказ — нормальный исход, ответа может не быть.
4. Одного «да» достаточно. Пишем 3–4 адресатам по очереди с интервалом ~3 дня, не всем разом.

## Кому (в порядке приоритета; каждый — автор работ по теме, у первых двух статьи в math.CO на arXiv точно есть)
| # | адресат | почему он | статус |
|---|---|---|---|
| 1 | David R. Wood (Monash) | соавтор «No-Three-in-Line-in-3D» (Pór, Wood; Algorithmica 2007) — прямой предшественник A399138-ветви; много статей в math.CO | адрес — с сайта Monash |
| 2 | Attila Pór (Western Kentucky) | второй автор той же статьи | адрес — с сайта WKU |
| 3 | Nathan Kaplan (UC Irvine) | из прежнего списка кандидатов (см. переписку/статью) — проверить, что у него есть math.CO-статьи | проверить |
| 4 | Thomas Prellberg (QMUL) | из прежнего списка; решёточная комбинаторика — проверить math.CO | проверить |
Ахим Фламменкамп — не endorser (нужны недавние статьи в math.CO на arXiv; у него их, насколько знаем, нет), но его можно
упомянуть как человека, с которым идёт переписка по базе решений — это честно и проверяемо.

## Письмо (английский; ИМЯ и XXXXXX подставить; одно на адресата, без веерной рассылки)
Subject: arXiv endorsement request (math.CO) — no-three-in-line in the cube

Dear Professor Wood,

I am an independent researcher working on the no-three-in-line problem and its three-dimensional variants
(OEIS A399138 — no three collinear in [n]^3, and A280537 — no four coplanar). I would like to post two short notes
to arXiv (math.CO) and need an endorsement for that archive; the endorsement code is XXXXXX
(https://arxiv.org/auth/endorse?x=XXXXXX).

The notes are already public with DOIs, with every witness checkable by a small script:
- A280537, note v3.2: https://doi.org/10.5281/zenodo.22066410 (new lower bounds for n = 12, 21, 22, 27 against the
  monotone closure of previously known values; data and verifier in the record);
- A399138: new lower bounds a(8) ≥ 94, a(9) ≥ 116, a(10) ≥ 138, a(11) ≥ 164 obtained by exact optimisation inside
  symmetry strata (subgroups of the cube group), witnesses and verifier at
  https://github.com/iwasborninbali/saturation/tree/main/certs/no3_3d [ссылку заменить на репо a399138-witnesses после выпуска].
Your paper with Attila Pór on no-three-in-line in 3D is the starting point of the second note.

I am aware that an endorsement is a statement about the author rather than a review of the papers; if you would
rather not endorse, I fully understand and no reply is needed.

With best regards,
[ИМЯ]
olegmikhb@gmail.com

## Отправлено 3.09.2026 (Gmail API, с studio@nusadua.dev; код NJC4KO; текст — slack/gates/arxiv_endorse_letters_2026-09-03.py)
- david.wood@monash.edu — 2026-09-03 12:41:15 +0800, id 1a06592340d43af7
- attila.por@wku.edu — 2026-09-03 12:41:17 +0800, id 1a065923a4ef20c6
Вторая волна (Kaplan, Prellberg) — только если через 3 дня нет ответа. Endorser вводит код на https://arxiv.org/auth/endorse.

## Вторая волна — отправлено 5.09.2026 07:50 WITA (Gmail API, с studio@nusadua.dev; код NJC4KO; текст — slack/gates/arxiv_endorse_letters_2026-09-05.py)
Слово владельца 5.09: «отправим ещё 4 как планировали». Входящих ответов от Wood и Pór на 07:40 5.09 нет (проверено inbox_check.py).
Адреса сверены по страницам университетов 5.09; абзац «почему вам» — свой, только с тем, что действительно есть в наших заметках.
- t.prellberg@qmul.ac.uk (QMUL; его arXiv:2602.07751 и arXiv:2605.09215 цитируются в наших заметках) — 07:50:33, id 1a06ed4c42e21004
- O.Pikhurko@warwick.ac.uk (Warwick) — 07:50:33, id 1a06ed4c7d76c9f5
- jschmitt@middlebury.edu (Middlebury) — 07:50:34, id 1a06ed4c809195bd
- gswarrin@uvm.edu (Vermont) — 07:50:34, id 1a06ed4ca9578e37
Трое последних — соавторы «Martin Gardner's minimum no-3-in-a-line problem» (Amer. Math. Monthly 121, 2014; arXiv:1206.5350, math.CO).
Резерв на случай тишины: Nathan Kaplan (UC Irvine) — адрес и math.CO-статьи проверить перед письмом.
