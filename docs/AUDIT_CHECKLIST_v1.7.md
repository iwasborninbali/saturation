# Чеклист внешней/человеческой проверки заметки hjsw_window v1.7 (что проверять и чем)

## Разделы 1–6 (гипербола, окна, коники, пара гипербол k=−1) — как в v1.2
- Theorem main / window / box formula: `slack/hjsw_window_check.py`, `slack/hjsw_boxes_check.py` (логи в slack/verification/).
- Lemma gadget (144): `slack/gadget11_check.py`. Theorem two (11/3): `slack/km1_theorem_check.py`, `slack/block_cover_km1.py`, `slack/km1_lines.py`.
- Prop m8asym (√p log⁴p): чисто аналитическая — читать Steps 1–4 (Selberg по четырём линейным формам; Bombieri).

## Раздел 7 — любая вторая гипербола (v1.4)
- Структура: строки/столбцы = рёбра графа классов; циклы = смежные классы ⟨k⟩; (4,8,4)-группы: `scratch struct_check.py` (в THREAD/§29 pair_bound_notes).
- Theorem general (потенциал): формула α ≤ 4(p−1) − (2G₈ − 2Σ|A_c−B_c|)/R и её LP‑подтверждение: `slack/exact_c.py`, `slack/cyc_model.py`.
- Prop g8k (G₈ = p/6 + O(√p log⁴p) при всех k): читать (тот же метод, что Prop m8asym); численно `slack/g8_general.py`.
- Lemma arc: `docs/research/arc_imbalance_lemma.md`, `slack/arc_imbalance.py`, `slack/mixed_sums_curve.py` (Бомбьери/Перельмутер/Кастро–Морено).

## Раздел 8 — кубические графики (v1.5)
- Lemma projection: тривиально. Dickson: ссылка. Value set (2/3)p + O(√p) — Чеботарёв (ссылка).
- Theorem cubic (11/4 p): структура ±1‑прямых и лифтов — брутфорс `slack/g35_agents/`, лог `slack/verification/g35_verify.txt`; стоимость покрытия при p=197…401 —
  `slack/cube_cover4.py`; закон (same = ½, независимость наклонов) — `slack/cube_local_law.py`, `slack/g_agents/group_types_output.txt` (p ≤ 5003).
- Аналитика: коники Q_± (норменная форма), твист Куммера χ(4/a − 3t²) — читать §3 `docs/research/permutation_cubic_note.md`.

## Раздел 9 — перестановочные мономы (v1.6–1.7)
- Lemma lifts: `slack/g_agents/profile_table_output.txt` (таблица по (k, n₀, класс)); Lemma rootcounts: критические точки/значения (одна строка);
  `docs/research/g_agents/galois_rootcounts.md` (Жордан/дискриминант тринома); Lemma positions/twoslopes: читать; ℓ‑адический аргумент для Res(D₊,D₋) ≠ 0 —
  проверять руками (одна страница); численно независимость наклонов — `slack/pp_joint_counts.py`.
- Константы C_k — точные дроби: `slack/pp_constant_exact.py`; проверка при p ≈ 10⁷: `slack/pp_exact_UL_np.py` (U/p = 1.7500 при k=3, 1.7631 при k=5).
- ε_k = 2/(k−1)! + 8/k! — учёт k‑корневых вычетов (читать доказательство теоремы).

## Что НЕ доказано (и так и написано)
- Пара гипербол: истинное значение ≈ 3(p−1)+O(1) (данные); модель вертикальных пар — условная теорема (Wigner‑край).
- Линейная константа для всех k (сертификат t = 1/m; локальный закон); сильная форма для кубик (LP ≈ 1.1 N); универсальная форма для всех
  перестановочных многочленов (только «общие»).
