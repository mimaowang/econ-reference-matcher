#!/usr/bin/env python3
"""Normalize candidate-paper metadata from JSON or CSV."""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path
from typing import Any


def key(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", str(value or "").lower()).strip()


def split_authors(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    text = str(value or "")
    if not text:
        return []
    parts = re.split(r";|\band\b|,", text)
    return [part.strip() for part in parts if part.strip()]


def get(row: dict[str, Any], *names: str) -> Any:
    lowered = {str(k).lower().strip(): v for k, v in row.items()}
    for name in names:
        if name.lower() in lowered:
            return lowered[name.lower()]
    return ""


def parse_year(value: Any) -> int | None:
    match = re.search(r"(19|20)\d{2}", str(value or ""))
    return int(match.group(0)) if match else None


def read_input(path: Path) -> list[dict[str, Any]]:
    if path.suffix.lower() == ".json":
        payload = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(payload, list):
            return payload
        if isinstance(payload, dict):
            for field in ("candidates", "papers", "items", "results"):
                if isinstance(payload.get(field), list):
                    return payload[field]
        raise ValueError("JSON input must be a list or contain candidates/papers/items/results")

    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def normalize_candidate(row: dict[str, Any], index: int) -> dict[str, Any]:
    title = str(get(row, "title", "paper_title", "article_title")).strip()
    journal = str(get(row, "journal", "source", "publication", "container-title")).strip()
    abstract = str(get(row, "abstract", "summary")).strip()
    excerpt = str(get(row, "excerpt", "quote", "evidence_excerpt")).strip()
    return {
        "id": str(get(row, "id", "candidate_id")) or f"P{index + 1}",
        "title": title,
        "title_key": key(title),
        "authors": split_authors(get(row, "authors", "author")),
        "year": parse_year(get(row, "year", "published", "publication_year")),
        "journal": journal,
        "journal_key": key(journal),
        "doi": str(get(row, "doi", "DOI")).strip(),
        "url": str(get(row, "url", "link")).strip(),
        "abstract": abstract,
        "evidence_excerpt": excerpt,
        "evidence_location": str(get(row, "evidence_location", "location", "page")).strip(),
        "source": str(get(row, "metadata_source", "source_url", "source")).strip(),
        "claimed_category": str(get(row, "category", "claimed_category")).strip(),
        "notes": str(get(row, "notes")).strip(),
    }


def cmd_normalize(args: argparse.Namespace) -> int:
    input_path = Path(args.input)
    candidates = read_input(input_path)
    normalized = [normalize_candidate(row, index) for index, row in enumerate(candidates)]
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema": "econ-reference-matcher.candidates.v1",
        "source": str(input_path),
        "count": len(normalized),
        "candidates": normalized,
    }
    output_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {len(normalized)} candidates to {output_path}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Normalize candidate paper metadata.")
    parser.add_argument("--input", required=True, help="input JSON or CSV")
    parser.add_argument(
        "--output",
        default=".econ-reference-matcher/candidates.normalized.json",
        help="output JSON path",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return cmd_normalize(args)


if __name__ == "__main__":
    raise SystemExit(main())
