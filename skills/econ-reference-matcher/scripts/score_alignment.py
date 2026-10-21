#!/usr/bin/env python3
"""Inspect lexical overlap without deciding whether a paper supports a claim."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "that",
    "the",
    "their",
    "this",
    "to",
    "with",
    "we",
}


def tokens(text: str) -> set[str]:
    return {
        token
        for token in re.findall(r"[a-zA-Z][a-zA-Z0-9\-]+", text.lower())
        if len(token) > 2 and token not in STOPWORDS
    }


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def extract_claims(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        if isinstance(payload.get("claims"), list):
            return payload["claims"]
        if isinstance(payload.get("claim_map"), list):
            return payload["claim_map"]
    raise ValueError("Claims JSON must be a list or contain claims/claim_map")


def extract_candidates(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict) and isinstance(payload.get("candidates"), list):
        return payload["candidates"]
    raise ValueError("Candidates JSON must be a list or contain candidates")


def jaccard(left: set[str], right: set[str]) -> float:
    if not left or not right:
        return 0.0
    return len(left & right) / len(left | right)


def evidence_text(candidate: dict[str, Any]) -> str:
    parts = [
        candidate.get("title", ""),
        candidate.get("abstract", ""),
        candidate.get("evidence_excerpt", ""),
        candidate.get("notes", ""),
    ]
    return " ".join(str(part or "") for part in parts)


def score_pair(claim: dict[str, Any], candidate: dict[str, Any]) -> dict[str, Any]:
    claim_text = " ".join(
        str(claim.get(field, "") or "")
        for field in ("text", "claim", "non_negotiable_terms", "flexible_terms")
    )
    claim_tokens = tokens(claim_text)
    paper_tokens = tokens(evidence_text(candidate))
    overlap = jaccard(claim_tokens, paper_tokens)
    excerpt_present = bool(str(candidate.get("evidence_excerpt", "")).strip())
    abstract_present = bool(str(candidate.get("abstract", "")).strip())

    return {
        "claim_id": claim.get("id") or claim.get("claim_id"),
        "candidate_id": candidate.get("id"),
        "lexical_overlap": round(overlap, 4) if claim_tokens and paper_tokens else None,
        "provided_text": "excerpt" if excerpt_present else "abstract" if abstract_present else "metadata_only",
        "review_required": True,
        "matched_terms": sorted(claim_tokens & paper_tokens),
        "note": "Word overlap is not support. Read the source to assess direction, mechanism, scope, and evidence; low overlap is not a rejection rule.",
    }


def cmd_score(args: argparse.Namespace) -> int:
    claims = extract_claims(load_json(Path(args.claims)))
    candidates = extract_candidates(load_json(Path(args.candidates)))
    results = []
    for claim in claims:
        for candidate in candidates:
            results.append(score_pair(claim, candidate))
    results.sort(
        key=lambda item: item["lexical_overlap"] if item["lexical_overlap"] is not None else -1,
        reverse=True,
    )
    output = {
        "schema": "econ-reference-matcher.alignment-scores.v2",
        "ordering": "Lexical overlap for inspection, not citation fitness. Review all candidates independently of this order.",
        "claims": len(claims),
        "candidates": len(candidates),
        "scores": results,
    }
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {len(results)} claim-candidate scores to {output_path}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Inspect claim-paper word overlap; does not classify, verify, or reject evidence."
    )
    parser.add_argument("--claims", required=True, help="claims JSON path")
    parser.add_argument("--candidates", required=True, help="normalized candidates JSON path")
    parser.add_argument(
        "--output",
        default=".econ-reference-matcher/alignment.scores.json",
        help="output JSON path",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return cmd_score(args)


if __name__ == "__main__":
    raise SystemExit(main())
