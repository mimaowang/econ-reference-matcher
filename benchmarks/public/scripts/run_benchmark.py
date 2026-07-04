#!/usr/bin/env python3
"""Prepare isolated benchmark workspaces for agent runs."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from common import REPO_ROOT, TASKS_ROOT, WORKSPACE_ROOT, find_task_dirs, load_task, write_text


def copy_public_inputs(task_dir: Path, destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    for name in ("prompt.md", "manuscript_context.md", "target_passages.json", "constraints.json", "candidate_corpus.json"):
        source = task_dir / name
        if source.exists():
            shutil.copy2(source, destination / name)


def write_run_instructions(task: dict[str, object], run_dir: Path, with_skill: bool, skill_path: Path) -> None:
    mode = "with_skill" if with_skill else "without_skill"
    instruction = f"""# Benchmark Run Instructions

Task: {task['id']} - {task['title']}
Run mode: {mode}

Read the files in `inputs/` and produce:

```text
outputs/report.md
```

Do not read answer files, hidden evaluator data, grading outputs, sample reports, or any files outside this run directory. If this is a `with_skill` run, use the skill at:

```text
{skill_path}
```

If this is a `without_skill` run, solve the task without reading the skill folder.
"""
    write_text(run_dir / "RUN_INSTRUCTIONS.md", instruction)


def prepare_iteration(iteration: str, tasks_root: Path, workspace_root: Path, skill_path: Path) -> Path:
    iteration_dir = workspace_root / iteration
    iteration_dir.mkdir(parents=True, exist_ok=True)
    for task_dir in find_task_dirs(tasks_root):
        task = load_task(task_dir)
        task_run_dir = iteration_dir / task["id"]
        for mode, with_skill in (("with_skill", True), ("without_skill", False)):
            run_dir = task_run_dir / mode
            copy_public_inputs(task_dir, run_dir / "inputs")
            (run_dir / "outputs").mkdir(parents=True, exist_ok=True)
            write_run_instructions(task, run_dir, with_skill, skill_path)
    return iteration_dir


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare isolated benchmark run directories.")
    parser.add_argument("--iteration", default="iteration-001", help="iteration directory name")
    parser.add_argument("--tasks", default=str(TASKS_ROOT), help="public tasks directory")
    parser.add_argument("--workspace", default=str(WORKSPACE_ROOT), help="workspace root")
    parser.add_argument(
        "--skill-path",
        default=str(REPO_ROOT / "skills" / "econ-reference-matcher"),
        help="skill directory path to mention in with_skill run instructions",
    )
    args = parser.parse_args()

    iteration_dir = prepare_iteration(args.iteration, Path(args.tasks), Path(args.workspace), Path(args.skill_path))
    print(f"Prepared benchmark workspace: {iteration_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
