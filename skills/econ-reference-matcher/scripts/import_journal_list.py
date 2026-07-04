#!/usr/bin/env python3
"""Normalize user-provided journal and ranking CSV files."""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path
from typing import Any


TRUE_VALUES = {"1", "true", "yes", "y", "t", "x"}
FALSE_VALUES = {"0", "false", "no", "n", "f", ""}


def norm_text(value: Any) -> str:
    return str(value or "").strip()


def journal_key(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def parse_bool(value: Any) -> bool | None:
    text = norm_text(value).lower()
    if text in TRUE_VALUES:
        return True
    if text in FALSE_VALUES:
        return False
    return None


def parse_int(value: Any) -> int | None:
    text = norm_text(value)
    if not text:
        return None
    match = re.search(r"\d+", text)
    return int(match.group(0)) if match else None


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return [dict(row) for row in reader]


def get(row: dict[str, str], *names: str) -> str:
    lowered = {key.lower().strip(): value for key, value in row.items()}
    for name in names:
        if name.lower() in lowered:
            return norm_text(lowered[name.lower()])
    return ""


def normalize_row(row: dict[str, str], source: str) -> dict[str, Any]:
    journal = get(row, "journal", "journal_name", "title", "source title")
    issn = get(row, "issn", "print_issn")
    eissn = get(row, "eissn", "e_issn", "electronic_issn")
    fields = get(row, "fields", "field", "category", "categories")
    return {
        "journal": journal,
        "journal_key": journal_key(journal),
        "issn": issn,
        "eissn": eissn,
        "ssci": parse_bool(get(row, "ssci", "in_ssci", "web_of_science_ssci")),
        "jcr_quartile": get(row, "jcr_quartile", "jcr", "quartile").upper(),
        "abs_stars": parse_int(get(row, "abs_stars", "ajg_stars", "abs", "ajg")),
        "ft50": parse_bool(get(row, "ft50", "ft_50")),
        "utd24": parse_bool(get(row, "utd24", "utd_24")),
        "fields": [part.strip() for part in fields.split(";") if part.strip()],
        "source": get(row, "source", "verification_source") or source,
        "verified_date": get(row, "verified_date", "date"),
    }


def cmd_import(args: argparse.Namespace) -> int:
    input_path = Path(args.input)
    rows = read_rows(input_path)
    normalized = [normalize_row(row, str(input_path)) for row in rows]
    missing_journal = [index + 1 for index, row in enumerate(normalized) if not row["journal"]]
    if missing_journal:
        raise SystemExit(f"Rows missing journal title: {missing_journal}")

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema": "econ-reference-matcher.journal-list.v1",
        "source_csv": str(input_path),
        "count": len(normalized),
        "journals": normalized,
    }
    output_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {len(normalized)} normalized journals to {output_path}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Normalize a user-provided journal/ranking CSV into JSON."
    )
    parser.add_argument("--input", required=True, help="source CSV path")
    parser.add_argument(
        "--output",
        default=".econ-reference-matcher/journals.normalized.json",
        help="output JSON path",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return cmd_import(args)


if __name__ == "__main__":
    raise SystemExit(main())
