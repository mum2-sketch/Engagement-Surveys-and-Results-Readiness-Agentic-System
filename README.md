# Engagement Surveys Agentic System

A four-skill workflow that turns messy survey inputs (participation, driver scores, comments, constraints) into exec-ready deliverables with a final quality/compliance gate. Built for repeatable cycles and safer outputs.

## Workflow
1. Run **engagement-intake-normalize** to produce a structured case file.
2. Run **engagement-theme-extraction** to derive grounded themes with evidence and risk flags.
3. Run **engagement-readiness-messaging** to build a results readiness brief and comms pack tailored to audience.
4. Run **engagement-quality-compliance-gate** to catch hallucinations, causality overclaims, and confidentiality risks; accept corrected outputs.

## Repo layout
- skills/ four markdown skills (inputs, outputs, behavior, constraints, examples)
- runs/ sample inputs and placeholders for outputs (run1 normal, run2 edge)
- benchmark/ cases, rubric, and scoring CSV template

## How to use (manual LLM flow)
- Paste the skill file into your LLM (Claude, GPT, Gemini) and provide the listed inputs.
- Preserve the output formats; each downstream skill consumes the prior outputs.
- Freeze prompts/settings when running benchmarks so results are comparable.

## How to use (code / automated)
- Script: `agentic_runner.py` sequences the four skills locally (no API key needed).
- Example: `python agentic_runner.py --input runs/run1_input.md --audience "HR leadership" --output runs/run1_output.md`
- Output file includes baseline single-shot and all skill outputs for scoring.

## Benchmarking (see benchmark/)
- Cases A (standard) and B (edge) provided; add Case C (ambiguous) if time permits.
- Baseline: single-shot prompt without skills.
- Score on 5 metrics (factual grounding, actionability, clarity, safety, time saved) using 1–5 anchors.
- Record scores in benchmark/benchmark_scores.csv and note worst failure.
