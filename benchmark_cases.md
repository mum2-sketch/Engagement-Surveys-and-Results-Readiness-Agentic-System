# Benchmark Cases and Rubric

Use identical prompts/settings across runs. Score both baseline (single-shot) and the 4-skill system.

## Baseline prompt (single-shot)
"Here is survey context, metrics, and comments. Produce an executive summary and action plan." (No multi-skill orchestration.)

## Cases
- **Case A — Stack Overflow Standard (2024):** Large-sample derived case from Stack Overflow survey data (use `runs/so2024_standard_input.md`).
- **Case B — Stack Overflow Edge (2024):** Narrow subset derived from Stack Overflow survey data (use `runs/so2024_edge_input.md`).
- **Case C — Engagement Standard:** Original engagement scenario with clear driver movement (use `runs/run1_input.md`).
- **Case D — Engagement Edge/Ambiguous:** Original low-signal engagement scenario (use `runs/run2_input.md`).

## Metrics (1–5 anchors)
1. **Factual grounding** — 1 invents metrics; 3 mostly grounded; 5 fully grounded.
2. **Actionability** — 1 vague; 3 some concrete actions; 5 specific with owner/timeframe.
3. **Clarity / Exec readiness** — 1 messy/long; 3 readable but needs edits; 5 ready to paste.
4. **Risk & confidentiality safety** — 1 risky identifiers; 3 generally safe; 5 consistently safe + flags risks.
5. **Time saved (est.)** — 1 none; 3 moderate; 5 major.

## What to capture
- Average score per metric (baseline vs system).
- Worst failure (describe briefly).
- Prompt iteration applied (what changed, why, effect).

## Scoring steps
1. Run baseline once per case with frozen settings; score on the rubric.
2. Run the 4-skill system per case; score on the same rubric.
3. Log scores in benchmark_scores.csv. Note any PASS-WITH-EDITS from Skill 4.
