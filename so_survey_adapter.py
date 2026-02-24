"""Convert Stack Overflow survey CSVs into run input files for the engagement workflow.

Usage examples:
  python so_survey_adapter.py --survey-csv "../stack-overflow-developer-survey-2024/survey_results_public.csv" --label so2024_standard --output runs/so2024_standard_input.md
  python so_survey_adapter.py --survey-csv "../stack-overflow-developer-survey-2024/survey_results_public.csv" --label so2024_edge --country-filter "Kenya" --max-rows 120 --output runs/so2024_edge_input.md
"""

import argparse
import csv
import statistics
from collections import Counter
from pathlib import Path
from typing import Iterable, List, Dict


def parse_years_code(value: str) -> float | None:
    if not value:
        return None
    value = value.strip().lower()
    if value in {"nan", "na"}:
        return None
    if "less than" in value:
        return 0.5
    if "more than" in value:
        return 50.0
    try:
        return float(value)
    except ValueError:
        return None


def top_items(values: Iterable[str], sep: str = ";", n: int = 5) -> List[str]:
    counter = Counter()
    for value in values:
        if not value:
            continue
        parts = [p.strip() for p in value.split(sep) if p.strip()]
        counter.update(parts)
    return [f"{k} ({v})" for k, v in counter.most_common(n)]


def load_rows(path: Path) -> List[Dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def build_run_input(rows: List[Dict[str, str]], label: str, source_name: str) -> str:
    total = len(rows)
    if total == 0:
        raise ValueError("No rows selected; adjust your filter.")

    countries = [r.get("Country", "") for r in rows]
    remote = [r.get("RemoteWork", "") for r in rows]
    employment = [r.get("Employment", "") for r in rows]
    years_code = [parse_years_code(r.get("YearsCode", "")) for r in rows]
    years_code = [v for v in years_code if v is not None]

    langs_have = [r.get("LanguageHaveWorkedWith", "") for r in rows]
    langs_want = [r.get("LanguageWantToWorkWith", "") for r in rows]
    job_sat = [r.get("JobSat", "") for r in rows if r.get("JobSat")]

    country_top = top_items(countries, sep=";", n=3)
    remote_top = top_items(remote, sep=";", n=3)
    employment_top = top_items(employment, sep=";", n=3)
    langs_have_top = top_items(langs_have, sep=";", n=6)
    langs_want_top = top_items(langs_want, sep=";", n=6)
    jobsat_top = top_items(job_sat, sep=";", n=4)

    median_years = round(statistics.median(years_code), 1) if years_code else "unverified"

    comments = []
    comments.append(f"Most represented countries in selected sample: {', '.join(country_top) if country_top else 'unverified' }.")
    comments.append(f"Top remote-work patterns: {', '.join(remote_top) if remote_top else 'unverified' }.")
    comments.append(f"Common employment categories: {', '.join(employment_top) if employment_top else 'unverified' }.")
    comments.append(f"Most used languages currently: {', '.join(langs_have_top[:4]) if langs_have_top else 'unverified' }.")
    comments.append(f"Most desired languages next year: {', '.join(langs_want_top[:4]) if langs_want_top else 'unverified' }.")
    if jobsat_top:
        comments.append(f"Job satisfaction distribution (as reported): {', '.join(jobsat_top)}.")

    if total < 150:
        comments.append("Sample size is relatively small; interpret patterns as directional only.")
    comments.append("These comments are synthesized from structured survey fields, not free-text responses.")

    quant_lines = [
        f"- Selected response count: {total}",
        f"- Median years coding: {median_years}",
        f"- Top countries: {', '.join(country_top) if country_top else 'unverified'}",
        f"- Top remote-work categories: {', '.join(remote_top) if remote_top else 'unverified'}",
        f"- Top used languages: {', '.join(langs_have_top[:5]) if langs_have_top else 'unverified'}",
        f"- Top wanted languages: {', '.join(langs_want_top[:5]) if langs_want_top else 'unverified'}",
    ]
    if jobsat_top:
        quant_lines.append(f"- Job satisfaction categories (top): {', '.join(jobsat_top)}")

    qual_lines = [f"{i+1}. \"{text}\"" for i, text in enumerate(comments[:12])]

    return (
        f"# {label} Input\n\n"
        "## survey_context\n"
        f"Source: {source_name}. Case label: {label}. This is a derived people-experience snapshot from Stack Overflow survey microdata. Audience: HR leadership and people analytics stakeholders.\n\n"
        "## quantitative_signals\n"
        + "\n".join(quant_lines)
        + "\n\n"
        "## qualitative_comments (derived from structured fields)\n"
        + "\n".join(qual_lines)
        + "\n\n"
        "## constraints\n"
        "- Treat this as derived proxy sentiment from structured fields; do not claim direct verbatim employee quotes.\n"
        "- Avoid causal language unless explicit causal evidence is provided.\n"
        "- Keep messaging executive-safe and include confidence/data limits.\n"
        "- Do not include personal identifiers.\n"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate run input markdown from Stack Overflow survey CSV.")
    parser.add_argument("--survey-csv", required=True, help="Path to survey_results_public.csv")
    parser.add_argument("--label", required=True, help="Label for the generated case")
    parser.add_argument("--output", required=True, help="Output markdown path (runs/*.md)")
    parser.add_argument("--country-filter", default="", help="Optional country filter for edge-case subsets")
    parser.add_argument("--max-rows", type=int, default=0, help="Optional cap for selected rows")
    args = parser.parse_args()

    survey_path = Path(args.survey_csv)
    rows = load_rows(survey_path)

    if args.country_filter:
        rows = [r for r in rows if (r.get("Country", "").strip().lower() == args.country_filter.strip().lower())]

    if args.max_rows and len(rows) > args.max_rows:
        rows = rows[: args.max_rows]

    text = build_run_input(rows, args.label, survey_path.parent.name)
    out = Path(args.output)
    out.write_text(text, encoding="utf-8")
    print(f"Wrote {out} with {len(rows)} rows")


if __name__ == "__main__":
    main()
