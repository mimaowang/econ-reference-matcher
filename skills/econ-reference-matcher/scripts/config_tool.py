#!/usr/bin/env python3
"""Initialize and validate econ-reference-matcher project config files."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


DEFAULT_CONFIG = """# econ-reference-matcher project configuration
project:
  manuscript_language: english
  report_language: auto
  citation_style: APA

filters:
  # These are eligibility rules. Prefer strong relevant journals within them;
  # a quality preference alone should not become another required filter.
  # AND means all active require_* filters must pass.
  # OR means any active accept_if_* filter may pass; blacklists still override.
  filter_logic: AND
  require_ssci: true
  jcr_quartiles: []
  min_abs_stars: null
  require_ft50: false
  require_utd24: false
  accept_if_ssci_and_jcr_quartile_in: []
  accept_if_min_abs_stars: null
  accept_if_ft50: false
  accept_if_utd24: false
  allowed_fields: ["economics", "finance", "management", "public policy"]
  journal_whitelist: []
  journal_blacklist: []
  min_publication_year: null

journal_lists:
  normalized_json: ".econ-reference-matcher/journals.normalized.json"
  source_csv: []
"""


def parse_scalar(value: str) -> Any:
    value = value.strip()
    if value in {"", "null", "None", "~"}:
        return None
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [parse_scalar(part.strip()) for part in inner.split(",")]
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]
    return value


def minimal_yaml_load(text: str) -> dict[str, Any]:
    """Parse the simple two-level YAML shape used by this skill."""
    data: dict[str, Any] = {}
    current_section: str | None = None

    for raw_line in text.splitlines():
        line = raw_line.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        if not line.startswith(" "):
            if not line.endswith(":"):
                raise ValueError(f"Unsupported top-level line: {raw_line}")
            current_section = line[:-1].strip()
            data[current_section] = {}
            continue
        if current_section is None:
            raise ValueError(f"Key without section: {raw_line}")
        stripped = line.strip()
        if ":" not in stripped:
            raise ValueError(f"Unsupported key line: {raw_line}")
        key, value = stripped.split(":", 1)
        data[current_section][key.strip()] = parse_scalar(value)
    return data


def load_config(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    try:
        import yaml  # type: ignore

        loaded = yaml.safe_load(text)
        return loaded if isinstance(loaded, dict) else {}
    except ImportError:
        return minimal_yaml_load(text)


def validate_config(data: dict[str, Any]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    for section in ("project", "filters", "journal_lists"):
        if section not in data or not isinstance(data[section], dict):
            errors.append(f"Missing required section: {section}")

    filters = data.get("filters", {})
    if isinstance(filters, dict):
        filter_logic = str(filters.get("filter_logic", "AND")).upper()
        if filter_logic not in {"AND", "OR"}:
            errors.append("filters.filter_logic must be AND or OR")
        if not isinstance(filters.get("require_ssci", True), bool):
            errors.append("filters.require_ssci must be true or false")
        quartiles = filters.get("jcr_quartiles", [])
        if quartiles is not None and not isinstance(quartiles, list):
            errors.append("filters.jcr_quartiles must be a list")
        elif isinstance(quartiles, list):
            invalid = [q for q in quartiles if str(q).upper() not in {"Q1", "Q2", "Q3", "Q4"}]
            if invalid:
                errors.append("filters.jcr_quartiles may only contain Q1, Q2, Q3, or Q4")
        min_abs = filters.get("min_abs_stars")
        if min_abs is not None and (type(min_abs) is not int or not 1 <= min_abs <= 4):
            errors.append("filters.min_abs_stars must be an integer from 1 to 4 or null")
        union_quartiles = filters.get("accept_if_ssci_and_jcr_quartile_in", [])
        if union_quartiles is not None and not isinstance(union_quartiles, list):
            errors.append("filters.accept_if_ssci_and_jcr_quartile_in must be a list")
        elif isinstance(union_quartiles, list):
            invalid = [
                q for q in union_quartiles if str(q).upper() not in {"Q1", "Q2", "Q3", "Q4"}
            ]
            if invalid:
                errors.append(
                    "filters.accept_if_ssci_and_jcr_quartile_in may only contain Q1, Q2, Q3, or Q4"
                )
        union_min_abs = filters.get("accept_if_min_abs_stars")
        if union_min_abs is not None and (
            type(union_min_abs) is not int or not 1 <= union_min_abs <= 4
        ):
            errors.append("filters.accept_if_min_abs_stars must be an integer from 1 to 4 or null")
        for key in ("require_ft50", "require_utd24", "accept_if_ft50", "accept_if_utd24"):
            if not isinstance(filters.get(key, False), bool):
                errors.append(f"filters.{key} must be true or false")
        for key in ("journal_whitelist", "journal_blacklist", "allowed_fields"):
            if filters.get(key) is not None and not isinstance(filters.get(key), list):
                errors.append(f"filters.{key} must be a list")
        if filter_logic == "OR":
            active_or_rules = [
                bool(union_quartiles),
                union_min_abs is not None,
                bool(filters.get("accept_if_ft50", False)),
                bool(filters.get("accept_if_utd24", False)),
                bool(filters.get("journal_whitelist", [])),
            ]
            if not any(active_or_rules):
                warnings.append(
                    "filters.filter_logic is OR, but no accept_if_* or whitelist rule is active."
                )
        elif filter_logic == "AND":
            active_and_rules = [
                bool(filters.get("require_ssci", True)),
                bool(quartiles),
                min_abs is not None,
                bool(filters.get("require_ft50", False)),
                bool(filters.get("require_utd24", False)),
            ]
            if sum(active_and_rules) >= 3:
                warnings.append(
                    "Multiple AND journal filters are active; confirm this is intended and not a union requirement."
                )

    lists = data.get("journal_lists", {})
    if isinstance(lists, dict):
        normalized = lists.get("normalized_json")
        if not normalized:
            warnings.append("journal_lists.normalized_json is empty")
        source_csv = lists.get("source_csv", [])
        if source_csv is not None and not isinstance(source_csv, list):
            errors.append("journal_lists.source_csv must be a list")

    if isinstance(filters, dict) and filters.get("require_ssci", True):
        warnings.append(
            "SSCI is enabled by default. Verification still requires a traceable source or user-provided list."
        )

    return errors, warnings


def cmd_init(args: argparse.Namespace) -> int:
    output = Path(args.output)
    if output.exists() and not args.force:
        print(f"Refusing to overwrite existing file: {output}", file=sys.stderr)
        print("Use --force to overwrite.", file=sys.stderr)
        return 2
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(DEFAULT_CONFIG, encoding="utf-8")
    print(f"Wrote config: {output}")
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    path = Path(args.config)
    if not path.exists():
        print(f"Config does not exist: {path}", file=sys.stderr)
        return 2
    data = load_config(path)
    errors, warnings = validate_config(data)
    result = {
        "config": str(path),
        "valid": not errors,
        "errors": errors,
        "warnings": warnings,
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 1 if errors else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Initialize or validate econ-reference-matcher config files."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    init = subparsers.add_parser("init", help="write a default config.yml")
    init.add_argument(
        "--output",
        default=".econ-reference-matcher/config.yml",
        help="output config path",
    )
    init.add_argument("--force", action="store_true", help="overwrite existing file")
    init.set_defaults(func=cmd_init)

    validate = subparsers.add_parser("validate", help="validate a config.yml")
    validate.add_argument(
        "--config",
        default=".econ-reference-matcher/config.yml",
        help="config file path",
    )
    validate.set_defaults(func=cmd_validate)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
