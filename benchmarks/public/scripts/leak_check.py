#!/usr/bin/env python3
"""Check that public benchmark tasks do not leak sealed gold answers."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from common import PRIVATE_GOLD_ROOT, TASKS_ROOT, find_task_dirs, load_gold, read_json


def public_text(task_dir: Path) -> str:
    parts: list[str] = []
    for path in task_dir.rglob("*"):
        if path.is_file():
            parts.append(path.read_text(encoding="utf-8", errors="ignore"))
    return "\n".join(parts).lower()


def check_task(task_dir: Path, gold_dir: Path) -> dict[str, object]:
    target = read_json(task_dir / "target_passages.json")
    task_id = target["id"]
    try:
        gold = load_gold(task_id, gold_dir)
    except FileNotFoundError:
        return {
            "task_id": task_id,
            "valid": True,
            "warnings": [f"No sealed gold found for {task_id}; skipped gold leak scan."],
            "leaks": [],
        }

    text = public_text(task_dir)
    secrets: list[str] = []
    for field in ("canaries",):
        secrets.extend(str(item) for item in gold.get(field, []) if item)
    for collection in ("must_find", "acceptable_alternatives", "forbidden_decoys"):
        for item in gold.get(collection, []):
            # Titles and DOIs that are already in closed candidate corpora are allowed.
            if (task_dir / "candidate_corpus.json").exists():
                continue
            for key in ("title", "doi"):
                value = str(item.get(key, "")).strip()
                if value:
                    secrets.append(value)

    leaks = sorted({secret for secret in secrets if secret and secret.lower() in text})
    return {
        "task_id": task_id,
        "valid": not leaks,
        "warnings": [],
        "leaks": leaks,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Check benchmark public tasks for gold leakage.")
    parser.add_argument("--tasks", default=str(TASKS_ROOT), help="public tasks directory")
    parser.add_argument("--gold", default=str(PRIVATE_GOLD_ROOT), help="private gold directory")
    args = parser.parse_args()

    results = [check_task(task, Path(args.gold)) for task in find_task_dirs(Path(args.tasks))]
    invalid = [result for result in results if not result["valid"]]
    for result in results:
        print(f"{result['task_id']}: {'OK' if result['valid'] else 'LEAK'}")
        for warning in result.get("warnings", []):
            print(f"  warning: {warning}")
        for leak in result.get("leaks", []):
            print(f"  leak: {leak}")
    return 1 if invalid else 0


if __name__ == "__main__":
    raise SystemExit(main())
