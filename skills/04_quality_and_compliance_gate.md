---
name: engagement-quality-compliance-gate
description: Final gate that checks for hallucinations, overclaiming, confidentiality risks, and formatting issues. Outputs pass/fail + fixes.
version: 1.1
inputs:
  - case_file: markdown
  - insight_pack: markdown
  - readiness_brief: markdown
  - messaging_pack: markdown
outputs:
  - gate_report: markdown
  - corrected_outputs: markdown
---

# Engagement Quality & Compliance Gate

## Purpose
Catch the most common failure modes before sharing outputs.

## Checks
1) Hallucination check:
   - Any metric not present in case_file? Flag + remove.
2) Causality check:
   - Replace "because/caused" with "may be associated" unless evidence exists.
3) Confidentiality check:
   - Remove PII, names, unique identifiers.
   - Ensure no small-group identification risk (if thresholds provided).
4) Actionability check:
   - Each recommendation must be specific (owner/action/timeframe).
5) Format check:
   - Brief <= ~400–600 words
   - Slide bullets <= 10

## Behavior
- Produce a gate_report with:
  - Status: PASS / PASS-WITH-EDITS / FAIL
  - List of issues
  - Exact edits applied
- Produce corrected outputs in one combined block.

## Output format
## Gate Report
## Corrected Outputs
- Final Readiness Brief
- Final Messaging Pack

## Example usage
**Input**: case_file + insight_pack + readiness_brief + messaging_pack.  
**Output**: gate_report + corrected_outputs ready to ship.
