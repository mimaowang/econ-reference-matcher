from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "econ-reference-matcher"


class RuntimeInstallationTests(unittest.TestCase):
    def test_marketplace_fetches_only_runtime_plugin(self) -> None:
        marketplace = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text(encoding="utf-8"))
        entry = marketplace["plugins"][0]
        self.assertEqual(entry["source"], {
            "source": "git-subdir",
            "url": "https://github.com/mimaowang/econ-reference-matcher.git",
            "path": "skills",
        })
        plugin_root = ROOT / entry["source"]["path"]
        manifest = json.loads((plugin_root / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["name"], entry["name"])
        self.assertEqual(manifest["skills"], ["./econ-reference-matcher"])
        self.assertNotIn("skills", entry)
        self.assertNotIn("version", manifest)  # Follow source commits, not a frozen package version.
        self.assertEqual(
            {path.name for path in plugin_root.iterdir()},
            {".claude-plugin", "econ-reference-matcher"},
        )

    def test_skill_contains_only_runtime_files(self) -> None:
        files = [
            path for path in SKILL.rglob("*")
            if path.is_file() and "__pycache__" not in path.parts and path.suffix != ".pyc"
        ]
        self.assertEqual(
            {path.relative_to(SKILL).parts[0] for path in files},
            {"SKILL.md", "references", "scripts", "agents", "LICENSE"},
        )
        self.assertEqual(
            (SKILL / "LICENSE").read_text(encoding="utf-8"),
            (ROOT / "LICENSE").read_text(encoding="utf-8"),
        )
        instructions = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        resources = re.findall(r"`((?:references|scripts)/[^`]+)`", instructions)
        self.assertTrue(resources)
        for resource in resources:
            with self.subTest(resource=resource):
                self.assertTrue((SKILL / resource).is_file())

    def test_development_evals_still_resolve_their_inputs(self) -> None:
        suite = json.loads((ROOT / "benchmarks/evals/evals.json").read_text(encoding="utf-8"))
        self.assertTrue(suite["evals"])
        for case in suite["evals"]:
            for filename in case["files"]:
                with self.subTest(case=case["id"], filename=filename):
                    self.assertTrue(filename.startswith("benchmarks/evals/"))
                    self.assertTrue((ROOT / filename).is_file())

    def test_helpers_work_without_repository_or_benchmark_files(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            installed = root / "econ-reference-matcher"
            shutil.copytree(SKILL, installed, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            for script in sorted((installed / "scripts").glob("*.py")):
                with self.subTest(script=script.name):
                    result = subprocess.run(
                        [sys.executable, "-I", str(script), "--help"],
                        cwd=root, capture_output=True, text=True, check=False,
                    )
                    self.assertEqual(result.returncode, 0, result.stderr)
            config = root / "project" / ".econ-reference-matcher" / "config.yml"
            for arguments in (
                ["init", "--output", str(config)],
                ["validate", "--config", str(config)],
            ):
                result = subprocess.run(
                    [sys.executable, "-I", str(installed / "scripts/config_tool.py"), *arguments],
                    cwd=root, capture_output=True, text=True, check=False,
                )
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertTrue(config.is_file())
            self.assertFalse((root / "benchmarks").exists())
            self.assertFalse((root / "tests").exists())


if __name__ == "__main__":
    unittest.main()
