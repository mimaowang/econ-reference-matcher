#!/usr/bin/env python3
"""Generate a simple human-review packet from benchmark outputs."""

from __future__ import annotations

import argparse
from pathlib import Path

from common import read_json, write_text


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a Markdown human-review packet.")
    parser.add_argument("--root", required=True, help="workspace iteration root")
    parser.add_argument("--output", required=True, help="review packet markdown path")
    args = parser.parse_args()

    root = Path(args.root)
    sections = ["# Human Review Packet", ""]
    for grading_path in sorted(root.rglob("grading.json")):
        grading = read_json(grading_path)
        report_path = grading_path.parent / "report.md"
        sections.append(f"## {grading['task_id']} / {grading['run_id']}")
        sections.append("")
        sections.append(f"- Score: {grading['total_score']}")
        sections.append(f"- Critical failures: {', '.join(grading.get('critical_failures', [])) or 'none'}")
        sections.append("")
        if report_path.exists():
            sections.append("<details><summary>Report</summary>")
            sections.append("")
            sections.append(report_path.read_text(encoding="utf-8"))
            sections.append("")
            sections.append("</details>")
            sections.append("")
    write_text(Path(args.output), "\n".join(sections))
    print(f"Wrote review packet: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
