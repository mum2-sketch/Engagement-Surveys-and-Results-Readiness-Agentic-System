---
name: engagement-intake-normalize
description: Normalize survey inputs (metrics + comments + context) into a structured case file used by downstream skills. Use first in the workflow.
version: 1.1
inputs:
  - survey_context: string
  - quantitative_signals: string
  - qualitative_comments: string
  - constraints: string
outputs:
  - case_file: markdown
  - clarification_questions: list
---

# Engagement Intake & Normalize

## Purpose
Convert messy, mixed-format survey inputs into a consistent case file with explicit assumptions and data boundaries.

## Behavior
1) Parse inputs into sections:
   - Population & scope (org, time window, audience)
   - Quant signals (participation, favorability, top drivers)
   - Qual comments (raw)
   - Constraints (suppression, tone, what not to claim)
2) Detect missing critical info:
   - Survey type (ES/PPS/MLS), date range, population size, min thresholds, audience
3) Produce:
   - A structured case file (Markdown)
   - Up to 5 clarification questions **only if required** to avoid unsafe assumptions.
4) If info is missing but not critical, proceed with explicit assumptions.

## Constraints / Failure modes
- Do not invent metrics.
- If numbers are ambiguous, label them as "unverified" and request confirmation.
- Keep the case file compact and reusable.

## Output format (case_file)
## Case File
### Context
### Quant Signals (as provided)
### Qual Comments (as provided)
### Constraints & Guardrails
### Assumptions
### Open Questions (if any)

## Example usage
**Input**: survey_context + metrics + comments.  
**Output**: normalized case file for downstream agents plus only necessary clarifications.
