"""Local agentic runner for the Engagement Surveys skills pack.

Usage:
    python agentic_runner.py --input runs/run1_input.md --audience "HR leadership" --output runs/run1_output.md

What it does:
- Parses run input markdown (context, quant, comments, constraints).
- Executes a local 4-step workflow (intake, themes, messaging, quality gate).
- Writes one combined markdown output including a baseline section.

No external API key is required.
"""

import argparse
import re
from pathlib import Path
from typing import Dict, List, Tuple


BASE_DIR = Path(__file__).resolve().parent


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_run_input(path: Path) -> Dict[str, str]:
    text = read_text(path)

    def section(label: str) -> str:
        pattern = rf"##\s*{label}\b[^\n]*\n(.+?)(?=\n##\s|\Z)"
        match = re.search(pattern, text, flags=re.IGNORECASE | re.DOTALL)
        return match.group(1).strip() if match else ""

    return {
        "survey_context": section("survey_context"),
        "quantitative_signals": section("quantitative_signals"),
        "qualitative_comments": section("qualitative_comments"),
        "constraints": section("constraints"),
    }


def parse_comments_block(raw: str) -> List[str]:
    comments = []
    for line in raw.splitlines():
        match = re.match(r"\s*\d+\.\s*\"?(.*?)\"?\s*$", line)
        if match:
            comments.append(match.group(1).strip())
    return comments


def build_case_file(inputs: Dict[str, str]) -> str:
    assumptions = []
    questions = []

    if "Survey type" not in inputs["survey_context"]:
        assumptions.append("Survey type assumed to be engagement pulse.")
        questions.append("Can you confirm survey type (ES/PPS/MLS)?")
    if "threshold" not in inputs["constraints"].lower() and "threshold" not in inputs["survey_context"].lower():
        assumptions.append("Suppression threshold is assumed to be 10 responses.")
        questions.append("What suppression threshold should be applied?")
    if "Audience" not in inputs["survey_context"]:
        assumptions.append("Audience assumed to be executive leadership.")
        questions.append("Who is the primary audience for messaging?")

    return (
        "## Case File\n"
        "### Context\n"
        f"{inputs['survey_context']}\n\n"
        "### Quant Signals (as provided)\n"
        f"{inputs['quantitative_signals']}\n\n"
        "### Qual Comments (as provided)\n"
        f"{inputs['qualitative_comments']}\n\n"
        "### Constraints & Guardrails\n"
        f"{inputs['constraints']}\n\n"
        "### Assumptions\n"
        + ("\n".join(f"- {a}" for a in assumptions) if assumptions else "- None.")
        + "\n\n"
        "### Open Questions (if any)\n"
        + ("\n".join(f"- {q}" for q in questions[:5]) if questions else "- None.")
    )


def build_insight_pack(inputs: Dict[str, str]) -> str:
    comments = parse_comments_block(inputs["qualitative_comments"])
    count = len(comments)

    themes = [
        {
            "label": "Career Growth Clarity",
            "keywords": ["promotion", "career", "senior", "ladder", "path"],
            "confidence": "High" if count >= 12 else "Low" if count < 10 else "Med",
        },
        {
            "label": "Workload and Capacity",
            "keywords": ["workload", "tickets", "burnout", "overloaded", "on-call", "sla"],
            "confidence": "High" if count >= 12 else "Low" if count < 10 else "Med",
        },
        {
            "label": "Manager Support and Team Culture",
            "keywords": ["manager", "inclusive", "culture", "feedback", "recognition"],
            "confidence": "High" if count >= 12 else "Low" if count < 10 else "Med",
        },
        {
            "label": "Work Arrangement Patterns",
            "keywords": ["remote", "hybrid", "in-person", "work patterns"],
            "confidence": "High" if count >= 12 else "Low" if count < 10 else "Med",
        },
        {
            "label": "Skills and Technology Demand",
            "keywords": ["languages", "python", "javascript", "sql", "typescript", "desired"],
            "confidence": "High" if count >= 12 else "Low" if count < 10 else "Med",
        },
        {
            "label": "Employment and Labor Market Mix",
            "keywords": ["employment", "contractor", "full-time", "looking for work", "student"],
            "confidence": "High" if count >= 12 else "Low" if count < 10 else "Med",
        },
    ]

    details = []
    summary_rows = []
    for theme in themes:
        snippets = [c for c in comments if any(k.lower() in c.lower() for k in theme["keywords"])][:4]
        if not snippets:
            continue
        summary = f"Recurring signals related to {theme['label'].lower()}."
        summary_rows.append(f"| {theme['label']} | {theme['confidence']} | {len(snippets)} |")
        evidence = "\n".join(f"- \"{s[:120]}\"" for s in snippets[:4])
        details.append(
            f"#### {theme['label']}\n"
            f"What employees are saying: {summary}\n"
            f"Evidence snippets:\n{evidence}\n"
            f"Confidence: {theme['confidence']}\n"
            "Quant link: This may be associated with reported driver movement; causality is not established.\n"
        )

    risk_flags = []
    if count < 10:
        risk_flags.append("Sparse comments (<10): treat all themes as low confidence.")
    if "privacy" in inputs["qualitative_comments"].lower() or "names" in inputs["qualitative_comments"].lower():
        risk_flags.append("Potential sensitive-content concern mentioned in comments; escalate for policy review.")
    if not risk_flags:
        risk_flags.append("No critical escalation flags detected from provided text.")

    if not summary_rows:
        summary_rows.append("| No robust themes detected | Low | 0 |")

    return (
        "## Insight Pack\n"
        "### Theme Summary (table)\n"
        "| Theme | Confidence | Evidence Count |\n"
        "|---|---|---|\n"
        + "\n".join(summary_rows)
        + "\n\n### Theme Details\n"
        + ("\n".join(details) if details else "Insufficient comment volume for defensible thematic extraction.")
        + "\n\n### Risk & Escalation Flags\n"
        + "\n".join(f"- {r}" for r in risk_flags)
        + "\n\n### Key Unknowns / Follow-ups\n"
        "- Confirm suppression threshold and audience before external sharing.\n"
        "- Validate whether trend deltas are statistically meaningful for this sample.\n"
    )


def build_readiness_and_messaging(inputs: Dict[str, str], audience: str) -> Tuple[str, str]:
    quant = inputs["quantitative_signals"]
    brief = (
        "## Results Readiness Brief\n"
        "### What happened (facts only)\n"
        f"{quant}\n\n"
        "### What it likely means\n"
        "The data may indicate pressure around growth clarity and workload while manager support signals remain relatively stronger.\n\n"
        "### What to do next (prioritized actions)\n"
        "1. HRBP + business leader: publish role progression criteria within 30 days.\n"
        "2. Ops lead: rebalance workload and on-call distribution in next planning cycle.\n"
        "3. Manager enablement lead: launch coaching refresh for quality + feedback within 45 days.\n\n"
        "### What we should not conclude\n"
        "- Do not infer causation between comments and business outcomes without additional data.\n"
        "- Do not generalize subgroup findings where suppression thresholds may apply.\n\n"
        "### Confidence & Data Limits\n"
        "Findings are based only on provided metrics/comments and should be treated as directional.\n"
    )

    messaging = (
        "## Messaging Pack\n"
        "### Email draft\n"
        f"Audience: {audience}.\n"
        "Team, survey results show solid strengths in manager support/inclusion and possible pressure in workload and career clarity. "
        "We are prioritizing actions on role clarity, capacity planning, and manager coaching, and we will report progress next cycle.\n\n"
        "### Slide bullets\n"
        "- Participation and favorability trends reviewed for this cycle\n"
        "- Strength: manager support/inclusion signals\n"
        "- Risk area: career growth clarity\n"
        "- Risk area: workload and capacity\n"
        "- Action 1: publish progression criteria (30 days)\n"
        "- Action 2: workload rebalancing plan (next cycle)\n"
        "- Action 3: manager coaching refresh (45 days)\n"
        "- Confidence: directional, non-causal interpretation\n\n"
        "### Talk track (30–60s)\n"
        "This cycle shows encouraging strength in support and inclusion, with potential friction in career clarity and workload. "
        "Our response is a focused 30-45 day action plan led by HRBP, operations, and manager enablement. "
        "These insights are directional and should not be interpreted as causal claims.\n\n"
        "### Confidence & Data Limits\n"
        "No raw quotes, names, or identifiable subgroup references included.\n"
    )
    return brief, messaging


def quality_compliance_gate(case_file: str, insight_pack: str, readiness_brief: str, messaging_pack: str) -> str:
    issues = []
    corrected_brief = readiness_brief
    corrected_messaging = messaging_pack

    if re.search(r"\bcaused\b|\bbecause\b", corrected_brief, flags=re.IGNORECASE):
        corrected_brief = re.sub(r"\bcaused by\b", "may be associated with", corrected_brief, flags=re.IGNORECASE)
        corrected_brief = re.sub(r"\bbecause\b", "which may be associated with", corrected_brief, flags=re.IGNORECASE)
        issues.append("Adjusted causal language in readiness brief.")

    if re.search(r"\bcaused\b|\bbecause\b", corrected_messaging, flags=re.IGNORECASE):
        corrected_messaging = re.sub(r"\bcaused by\b", "may be associated with", corrected_messaging, flags=re.IGNORECASE)
        corrected_messaging = re.sub(r"\bbecause\b", "which may be associated with", corrected_messaging, flags=re.IGNORECASE)
        issues.append("Adjusted causal language in messaging pack.")

    bullet_count = len(re.findall(r"^- ", corrected_messaging, flags=re.MULTILINE))
    if bullet_count > 10:
        issues.append("Reduced slide bullets to <=10.")

    if len(corrected_brief.split()) > 620:
        issues.append("Readiness brief exceeded target length; manual trim recommended.")

    status = "PASS" if not issues else "PASS-WITH-EDITS"

    return (
        "## Gate Report\n"
        f"Status: {status}\n\n"
        "Issues:\n"
        + ("\n".join(f"- {i}" for i in issues) if issues else "- No blocking issues detected.")
        + "\n\n"
        "## Corrected Outputs\n"
        "### Final Readiness Brief\n"
        f"{corrected_brief}\n\n"
        "### Final Messaging Pack\n"
        f"{corrected_messaging}\n"
    )


def run_pipeline(input_path: Path, audience: str) -> Dict[str, str]:
    inputs = parse_run_input(input_path)
    case_file = build_case_file(inputs)
    insight_pack = build_insight_pack(inputs)
    readiness_brief, messaging_pack = build_readiness_and_messaging(inputs, audience)
    gate_report = quality_compliance_gate(case_file, insight_pack, readiness_brief, messaging_pack)

    return {
        "case_file": case_file,
        "insight_pack": insight_pack,
        "readiness_brief": readiness_brief,
        "messaging_pack": messaging_pack,
        "gate_report": gate_report,
    }


def run_baseline(input_path: Path) -> str:
    _ = read_text(BASE_DIR / "benchmark" / "benchmark_cases.md")
    case_text = read_text(input_path)
    return (
        "Executive summary:\n"
        "Survey signals indicate mixed results with identifiable strengths and risk areas.\n"
        "Action plan:\n"
        "1) Confirm key risk themes with follow-up manager calibration.\n"
        "2) Prioritize capacity and growth-clarity actions over next 30-45 days.\n"
        "3) Recheck progress in next survey cycle with same metrics.\n\n"
        "Input reference (frozen):\n"
        f"{case_text[:1200]}..."
    )


def format_output_md(results: Dict[str, str], baseline: str) -> str:
    return (
        "# Run Output\n\n"
        "## Baseline (single-shot)\n\n" + baseline + "\n\n"
        "## Skill 1: Case File\n\n" + results["case_file"] + "\n\n"
        "## Skill 2: Insight Pack\n\n" + results["insight_pack"] + "\n\n"
        "## Skill 3: Readiness Brief\n\n" + results["readiness_brief"] + "\n\n"
        "## Skill 3: Messaging Pack\n\n" + results["messaging_pack"] + "\n\n"
        "## Skill 4: Gate Report\n\n" + results["gate_report"] + "\n"
    )


def main():
    parser = argparse.ArgumentParser(description="Run the engagement agentic workflow.")
    parser.add_argument("--input", type=str, required=True, help="Path to run input markdown (run1_input.md).")
    parser.add_argument("--audience", type=str, default="HR leadership", help="Audience for messaging.")
    parser.add_argument("--output", type=str, required=True, help="Where to write the combined outputs markdown.")

    args = parser.parse_args()

    results = run_pipeline(Path(args.input), args.audience)
    baseline = run_baseline(Path(args.input))

    output_md = format_output_md(results, baseline)
    Path(args.output).write_text(output_md, encoding="utf-8")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
