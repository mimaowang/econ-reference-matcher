#!/usr/bin/env python3
"""Aggregate benchmark grading JSON files."""

from __future__ import annotations

import argparse
from pathlib import Path
from statistics import mean
from typing import Any

from common import DIMENSIONS, markdown_table, read_json, write_json, write_text


def collect_gradings(root: Path) -> list[dict[str, Any]]:
    return [read_json(path) for path in sorted(root.rglob("grading.json"))]


def aggregate(results: list[dict[str, Any]]) -> dict[str, Any]:
    by_run: dict[str, list[dict[str, Any]]] = {}
    for result in results:
        by_run.setdefault(result.get("run_id", "unknown"), []).append(result)

    runs = {}
    for run_id, items in by_run.items():
        runs[run_id] = {
            "count": len(items),
            "mean_score": round(mean(item["total_score"] for item in items), 2),
            "invalid_count": sum(1 for item in items if item.get("invalid")),
            "dimension_means": {
                dim: round(mean(item.get("dimensions", {}).get(dim, 0) for item in items), 2)
                for dim in DIMENSIONS
            },
            "critical_failures": sorted(
                {
                    failure
                    for item in items
                    for failure in item.get("critical_failures", [])
                }
            ),
        }
    return {"runs": runs, "results": results}


def write_markdown(summary: dict[str, Any], output: Path) -> None:
    rows = []
    for run_id, data in summary["runs"].items():
        rows.append([run_id, data["count"], data["mean_score"], data["invalid_count"], ", ".join(data["critical_failures"])])
    content = "# Benchmark Summary\n\n"
    content += markdown_table(["Run", "Cases", "Mean score", "Invalid", "Critical failures"], rows)
    content += "\n\n## Dimension Means\n\n"
    for run_id, data in summary["runs"].items():
        content += f"### {run_id}\n\n"
        dim_rows = [[dim, score] for dim, score in data["dimension_means"].items()]
        content += markdown_table(["Dimension", "Mean points"], dim_rows)
        content += "\n\n"
    write_text(output, content)


def write_failure_analysis(summary: dict[str, Any], output: Path) -> None:
    lines = ["# Failure Analysis", ""]
    for result in summary["results"]:
        failures = result.get("critical_failures", [])
        if failures or result.get("total_score", 100) < 75:
            lines.append(f"## {result['task_id']} / {result['run_id']}")
            lines.append("")
            lines.append(f"- Score: {result['total_score']}")
            lines.append(f"- Critical failures: {', '.join(failures) if failures else 'none'}")
            weak = [
                f"{dim}: {score}"
                for dim, score in result.get("dimensions", {}).items()
                if score < DIMENSIONS.get(dim, 0) * 0.6
            ]
            lines.append(f"- Weak dimensions: {', '.join(weak) if weak else 'none'}")
            lines.append("")
    write_text(output, "\n".join(lines))


def main() -> int:
    parser = argparse.ArgumentParser(description="Aggregate benchmark grading results.")
    parser.add_argument("--root", required=True, help="workspace iteration root")
    parser.add_argument("--output-json", required=True, help="benchmark.json output")
    parser.add_argument("--output-md", required=True, help="benchmark.md output")
    parser.add_argument("--failure-md", required=True, help="failure_analysis.md output")
    args = parser.parse_args()

    results = collect_gradings(Path(args.root))
    summary = aggregate(results)
    write_json(Path(args.output_json), summary)
    write_markdown(summary, Path(args.output_md))
    write_failure_analysis(summary, Path(args.failure_md))
    print(f"Aggregated {len(results)} grading files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
