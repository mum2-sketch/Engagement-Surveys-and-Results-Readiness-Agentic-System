---
name: engagement-theme-extraction
description: Extract themes from survey comments and connect them to quant signals carefully (no invented causality). Produces themes, evidence, and risk flags.
version: 1.1
inputs:
  - case_file: markdown
outputs:
  - insight_pack: markdown
---

# Engagement Theme Extraction

## Purpose
Generate defensible insights: themes, sentiment, and evidence grounded in provided text.

## Behavior
1) Read the Case File.
2) Build 3–6 themes with:
   - Theme label
   - What employees are saying (summary)
   - Evidence: 2–4 short supporting snippets (<=20 words each)
   - Confidence: High/Med/Low (based on volume + clarity)
3) Link themes to quant signals only when explicitly supported:
   - Use "may be related" not "caused by" unless data explicitly shows causality.
4) Flag risks:
   - Contradictory signals
   - Sparse comments
   - Potential PII or sensitive content
   - Any "hot spots" (harassment, safety, discrimination) → escalate flag

## Constraints / Failure modes
- Never claim causality unless evidence exists; otherwise use "may be associated." (prompt-iteration change)
- If comments are too few (<10), set confidence Low and suggest "need more data."
- Do not restate or invent metrics not present in the case file.

## Output format (insight_pack)
## Insight Pack
### Theme Summary (table)
### Theme Details (1 section per theme)
### Risk & Escalation Flags
### Key Unknowns / Follow-ups

## Example usage
**Input**: case_file from Skill 1.  
**Output**: insight_pack for messaging + gating skills.
