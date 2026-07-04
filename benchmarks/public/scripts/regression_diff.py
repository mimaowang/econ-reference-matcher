#!/usr/bin/env python3
"""Compare two benchmark aggregate JSON files."""

from __future__ import annotations

import argparse
from pathlib import Path

from common import read_json, write_text


def run_scores(summary: dict, run_id: str) -> dict[str, float]:
    scores = {}
    for result in summary.get("results", []):
        if result.get("run_id") == run_id:
            scores[result["task_id"]] = float(result["total_score"])
    return scores


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare benchmark scores across two iterations.")
    parser.add_argument("--previous", required=True, help="previous benchmark.json")
    parser.add_argument("--current", required=True, help="current benchmark.json")
    parser.add_argument("--run-id", default="with_skill", help="run ID to compare")
    parser.add_argument("--output", required=True, help="Markdown output path")
    args = parser.parse_args()

    previous = run_scores(read_json(Path(args.previous)), args.run_id)
    current = run_scores(read_json(Path(args.current)), args.run_id)
    task_ids = sorted(set(previous) | set(current))
    lines = ["# Regression Diff", "", "| Task | Previous | Current | Delta |", "| --- | ---: | ---: | ---: |"]
    for task_id in task_ids:
        old = previous.get(task_id)
        new = current.get(task_id)
        delta = "" if old is None or new is None else round(new - old, 2)
        lines.append(f"| {task_id} | {old if old is not None else 'n/a'} | {new if new is not None else 'n/a'} | {delta} |")
    write_text(Path(args.output), "\n".join(lines))
    print(f"Wrote regression diff: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
