"""Shared helpers for econ-reference-matcher benchmark scripts."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
REPO_ROOT = ROOT.parent
PUBLIC_ROOT = ROOT / "public"
TASKS_ROOT = PUBLIC_ROOT / "tasks"
PRIVATE_GOLD_ROOT = ROOT / "private-gold"
WORKSPACE_ROOT = ROOT / "workspace"


DIMENSIONS = {
    "claim_decomposition": 10,
    "direct_support_precision": 25,
    "decoy_rejection": 15,
    "evidence_integrity": 20,
    "literature_dialogue_quality": 10,
    "journal_filter_compliance": 10,
    "output_usability": 5,
    "retry_insufficiency_behavior": 5,
}


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


def slug_from_task_dir(task_dir: Path) -> str:
    return task_dir.name.split("-", 1)[0]


def find_task_dirs(tasks_root: Path = TASKS_ROOT) -> list[Path]:
    return sorted(path for path in tasks_root.iterdir() if path.is_dir())


def load_task(task_dir: Path) -> dict[str, Any]:
    payload = read_json(task_dir / "target_passages.json")
    payload["task_dir"] = str(task_dir)
    payload["task_slug"] = slug_from_task_dir(task_dir)
    constraints_path = task_dir / "constraints.json"
    payload["constraints"] = read_json(constraints_path) if constraints_path.exists() else {}
    return payload


def load_gold(task_id: str, gold_dir: Path = PRIVATE_GOLD_ROOT) -> dict[str, Any]:
    candidates = [gold_dir / f"{task_id}.gold.json", gold_dir / f"{task_id.upper()}.gold.json"]
    if task_id == "E001":
        candidates.append(gold_dir / "toy-example.gold.json")
    for path in candidates:
        if path.exists():
            data = read_json(path)
            if data.get("task_id") == task_id:
                return data
    raise FileNotFoundError(f"No gold file found for {task_id} in {gold_dir}")


def text_contains_any(text: str, values: list[str]) -> bool:
    haystack = normalize(text)
    return any(normalize(value) in haystack for value in values if value)


def extract_titles(items: list[dict[str, Any]]) -> list[str]:
    return [str(item.get("title", "")) for item in items if item.get("title")]


def extract_dois(items: list[dict[str, Any]]) -> list[str]:
    return [str(item.get("doi", "")) for item in items if item.get("doi")]


def markdown_table(headers: list[str], rows: list[list[Any]]) -> str:
    header = "| " + " | ".join(headers) + " |"
    sep = "| " + " | ".join("---" for _ in headers) + " |"
    body = ["| " + " | ".join(str(cell) for cell in row) + " |" for row in rows]
    return "\n".join([header, sep, *body])
