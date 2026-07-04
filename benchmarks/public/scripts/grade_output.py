#!/usr/bin/env python3
"""Grade a benchmark report against sealed gold."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any

from common import DIMENSIONS, PRIVATE_GOLD_ROOT, load_gold, normalize, write_json


def contains(text: str, value: str) -> bool:
    return bool(value) and normalize(value) in normalize(text)


def count_present(text: str, items: list[dict[str, Any]], key: str) -> int:
    return sum(1 for item in items if contains(text, str(item.get(key, ""))))


def evidence_markers(text: str) -> int:
    markers = [
        "Verifiable excerpt",
        "Location:",
        "abstract",
        "publisher",
        "DOI",
        "doi",
        "page",
        "section",
    ]
    return sum(1 for marker in markers if marker in text)


def category_near_title(text: str, title: str, category: str) -> bool:
    if not title or title not in text:
        return False
    title_index = text.find(title)
    window = text[title_index : title_index + 1500]
    return category in window


def window_near_title(text: str, title: str, before: int = 600, after: int = 1500) -> str:
    if not title or title not in text:
        return ""
    title_index = text.find(title)
    start = max(0, title_index - before)
    return text[start : title_index + after]


def rejected_near_title(text: str, title: str) -> bool:
    window = window_near_title(text, title)
    rejection_terms = [
        "Topic Adjacent / Rejected",
        "Rejected Topic-Adjacent",
        "Rejected Decoy",
        "Rejected",
        "Reject",
        "Do not use",
        "not suitable",
    ]
    return any(term.lower() in window.lower() for term in rejection_terms)


def direct_support_label_near_title(text: str, title: str) -> bool:
    window = window_near_title(text, title, before=200, after=1200)
    direct_patterns = [
        r"Category:\s*\**Direct Support",
        r"Direct support judgment\s*\|[^\n]*Direct support",
        r"Direct support:\s*\**" + re.escape(title),
    ]
    return any(re.search(pattern, window, flags=re.IGNORECASE) for pattern in direct_patterns)


def grade(report_text: str, gold: dict[str, Any], task_id: str, run_id: str) -> dict[str, Any]:
    findings: list[dict[str, Any]] = []
    critical_failures: list[str] = []
    dimensions = {name: 0.0 for name in DIMENSIONS}

    # Canary leakage
    leaked_canaries = [c for c in gold.get("canaries", []) if c and c in report_text]
    if leaked_canaries:
        critical_failures.append("private_gold_leakage")

    has_claim_map = "Claim Map" in report_text or "claim map" in report_text.lower()
    target_claims = gold.get("target_claims", [])
    claim_hits = count_present(report_text, target_claims, "claim_id")
    dimensions["claim_decomposition"] = DIMENSIONS["claim_decomposition"] * (
        0.5 * bool(has_claim_map) + 0.5 * min(1.0, claim_hits / max(1, len(target_claims)))
    )
    if not has_claim_map:
        critical_failures.append("missing_claim_map")

    must_find = gold.get("must_find", [])
    must_title_hits = count_present(report_text, must_find, "title")
    must_doi_hits = count_present(report_text, must_find, "doi")
    direct_hit_ratio = min(1.0, (must_title_hits + must_doi_hits) / max(1, len(must_find)))
    direct_category_hits = sum(
        1
        for item in must_find
        if category_near_title(report_text, str(item.get("title", "")), "Direct Support")
    )
    dimensions["direct_support_precision"] = DIMENSIONS["direct_support_precision"] * min(
        1.0, 0.6 * direct_hit_ratio + 0.4 * (direct_category_hits / max(1, len(must_find)))
    )

    forbidden = gold.get("forbidden_decoys", [])
    rejected_decoys = 0
    direct_decoys = 0
    for item in forbidden:
        title = str(item.get("title", ""))
        if contains(report_text, title):
            if direct_support_label_near_title(report_text, title) and not rejected_near_title(report_text, title):
                direct_decoys += 1
            if rejected_near_title(report_text, title):
                rejected_decoys += 1
    if direct_decoys:
        critical_failures.append("forbidden_decoy_labeled_direct_support")
    dimensions["decoy_rejection"] = DIMENSIONS["decoy_rejection"] * (
        rejected_decoys / max(1, len(forbidden))
    )

    evidence_score = min(1.0, evidence_markers(report_text) / 4)
    no_pending_fabrication = "Strong Candidate Pending Full Text" in report_text or "Verifiable excerpt" in report_text
    dimensions["evidence_integrity"] = DIMENSIONS["evidence_integrity"] * (
        0.8 * evidence_score + 0.2 * bool(no_pending_fabrication)
    )

    dialogue_terms = ["literature dialogue", "contribution", "consistent", "contrast", "extends", "How to use"]
    dimensions["literature_dialogue_quality"] = DIMENSIONS["literature_dialogue_quality"] * min(
        1.0, sum(1 for term in dialogue_terms if term.lower() in report_text.lower()) / 3
    )

    journal_terms = ["SSCI", "JCR", "ABS", "FT50", "UTD", "Journal filter status"]
    dimensions["journal_filter_compliance"] = DIMENSIONS["journal_filter_compliance"] * min(
        1.0, sum(1 for term in journal_terms if term in report_text) / 3
    )

    usability_terms = ["APA", "BibTeX", "Paper-ready sentence", "DOI"]
    dimensions["output_usability"] = DIMENSIONS["output_usability"] * min(
        1.0, sum(1 for term in usability_terms if term in report_text) / len(usability_terms)
    )

    retry_terms = ["keep searching", "unsupported", "pending", "PDF", "not enough", "insufficient"]
    dimensions["retry_insufficiency_behavior"] = DIMENSIONS["retry_insufficiency_behavior"] * min(
        1.0, sum(1 for term in retry_terms if term.lower() in report_text.lower()) / 2
    )

    total = round(sum(dimensions.values()), 2)
    caps = []
    if "forbidden_decoy_labeled_direct_support" in critical_failures:
        caps.append(60)
    if "missing_claim_map" in critical_failures:
        caps.append(70)
    if re.search(r"CANARY_[A-Z0-9_]+", report_text):
        caps.append(0)
    if caps:
        total = min(total, min(caps))

    novel_candidates = []
    known_titles = {
        str(item.get("title", ""))
        for bucket in ("must_find", "acceptable_alternatives", "forbidden_decoys")
        for item in gold.get(bucket, [])
    }
    for match in re.finditer(r"^###\s+\d+\.\s+(.+)$", report_text, flags=re.MULTILINE):
        title = match.group(1).strip()
        if title and title not in known_titles:
            novel_candidates.append({"title": title, "needs_expert_review": True})

    return {
        "task_id": task_id,
        "run_id": run_id,
        "total_score": total,
        "invalid": "private_gold_leakage" in critical_failures,
        "dimensions": {key: round(value, 2) for key, value in dimensions.items()},
        "critical_failures": critical_failures,
        "findings": findings,
        "novel_candidate_review": novel_candidates,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Grade a benchmark output report.")
    parser.add_argument("--task-id", required=True, help="task ID, e.g. E001")
    parser.add_argument("--run-id", default="manual", help="run ID label")
    parser.add_argument("--report", required=True, help="report.md path")
    parser.add_argument("--gold-dir", default=str(PRIVATE_GOLD_ROOT), help="sealed gold directory")
    parser.add_argument("--output", required=True, help="grading JSON output path")
    args = parser.parse_args()

    report_text = Path(args.report).read_text(encoding="utf-8")
    gold = load_gold(args.task_id, Path(args.gold_dir))
    result = grade(report_text, gold, args.task_id, args.run_id)
    write_json(Path(args.output), result)
    print(f"{args.task_id}/{args.run_id}: {result['total_score']}")
    return 1 if result["invalid"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
