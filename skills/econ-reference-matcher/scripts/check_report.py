#!/usr/bin/env python3
"""Check final reference-match reports for required evidence fields."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


REQUIRED_MARKERS = [
    "Target Passage",
    "Claim Map",
    "Final Recommendations",
    "Journal filter status",
    "Category",
    "Supports claim",
    "Verifiable excerpt",
    "Why it supports",
    "APA",
    "BibTeX",
]


CATEGORIES = [
    "Direct Support",
    "Theory Support",
    "Literature Dialogue",
    "Strong Candidate Pending Full Text",
    "Topic Adjacent / Rejected",
]


def count_recommendations(text: str) -> int:
    return len(re.findall(r"^###\s+\d+\.", text, flags=re.MULTILINE))


def check_report(text: str, min_final: int) -> dict[str, object]:
    errors: list[str] = []
    warnings: list[str] = []

    for marker in REQUIRED_MARKERS:
        if marker not in text:
            errors.append(f"Missing required marker: {marker}")

    rec_count = count_recommendations(text)
    if rec_count < min_final:
        warnings.append(
            f"Found {rec_count} numbered recommendation(s); expected at least {min_final} unless the report explains why fewer papers passed."
        )

    if not any(category in text for category in CATEGORIES):
        errors.append("No recognized evidence category found")

    rejected_markers = [
        "Topic Adjacent / Rejected",
        "Rejected as Topic Adjacent",
        "Rejected Topic-Adjacent",
        "Rejected Decoy",
    ]
    if not any(marker.lower() in text.lower() for marker in rejected_markers):
        warnings.append("No rejected topic-adjacent candidates documented")

    if "Pending Full Text" in text and "Needed user input" not in text:
        warnings.append("Pending full-text candidates should state what user input is needed")

    dialogue_markers = [
        "How to use it in literature dialogue",
        "Citation and dialogue use",
        "Contribution/dialogue use",
        "consistent",
        "contrast",
        "extends",
    ]
    if not any(marker.lower() in text.lower() for marker in dialogue_markers):
        warnings.append("No explicit citation/dialogue use guidance found")

    return {
        "valid": not errors,
        "recommendation_count": rec_count,
        "errors": errors,
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check an econ-reference-matcher final report for required fields."
    )
    parser.add_argument("--report", required=True, help="Markdown report path")
    parser.add_argument("--min-final", type=int, default=3, help="minimum final papers")
    parser.add_argument(
        "--json",
        action="store_true",
        help="print machine-readable JSON instead of a text summary",
    )
    args = parser.parse_args()

    path = Path(args.report)
    text = path.read_text(encoding="utf-8")
    result = check_report(text, args.min_final)
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"Report: {path}")
        print(f"Valid: {result['valid']}")
        print(f"Recommendation count: {result['recommendation_count']}")
        for error in result["errors"]:  # type: ignore[index]
            print(f"ERROR: {error}", file=sys.stderr)
        for warning in result["warnings"]:  # type: ignore[index]
            print(f"WARNING: {warning}", file=sys.stderr)
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
