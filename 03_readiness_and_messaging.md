---
name: engagement-readiness-messaging
description: Turn insights into results readiness artifacts: executive brief, manager-ready actions, and comms snippets (email + slide bullets).
version: 1.1
inputs:
  - case_file: markdown
  - insight_pack: markdown
  - audience: string  # HR leadership, Sr Director, Managers, Comms
outputs:
  - readiness_brief: markdown
  - messaging_pack: markdown
---

# Engagement Results Readiness + Messaging Builder

## Purpose
Convert insights into "ready to ship" artifacts: brief + actions + messaging.

## Behavior
1) Create a Results Readiness Brief (≈1 page):
   - What happened (facts only)
   - What it likely means (careful language)
   - What to do next (prioritized actions)
   - What we should not conclude (anti-hallucination section)
2) Create a Messaging Pack:
   - Email draft (plain, minimal jargon)
   - Slide bullets (6–10 bullets)
   - Talk track (30–60 seconds)
3) Tailor tone to audience:
   - Exec: concise, risk-aware
   - Managers: practical, "what to do Monday"
4) Include a "Confidence & Data Limits" footer.

## Constraints / Failure modes
- Do not include raw comments if constraints forbid it.
- Do not include names, teams, or identifying info.
- Keep brief <= ~400–600 words; slide bullets <= 10.

## Output format
## Results Readiness Brief
## Messaging Pack
- Email draft
- Slide bullets
- Talk track
- Confidence & Data Limits

## Example usage
**Input**: case_file + insight_pack + audience.  
**Output**: brief + messaging pack for final gating.
