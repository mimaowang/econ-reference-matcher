from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, relative_path: str):
    path = ROOT / relative_path
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


config_tool = load_module("config_tool", "skills/econ-reference-matcher/scripts/config_tool.py")
normalize_candidates = load_module(
    "normalize_candidates", "skills/econ-reference-matcher/scripts/normalize_candidates.py"
)
score_alignment = load_module("score_alignment", "skills/econ-reference-matcher/scripts/score_alignment.py")
check_report = load_module("check_report", "skills/econ-reference-matcher/scripts/check_report.py")
common = load_module("benchmark_common", "benchmarks/public/scripts/common.py")


class ConfigToolTests(unittest.TestCase):
    def test_default_config_validates(self) -> None:
        data = config_tool.minimal_yaml_load(config_tool.DEFAULT_CONFIG)
        errors, warnings = config_tool.validate_config(data)
        self.assertEqual(errors, [])
        self.assertEqual(data["filters"]["allowed_fields"], [])
        self.assertTrue(any("SSCI" in warning for warning in warnings))

    def test_union_filter_config_validates(self) -> None:
        data = config_tool.minimal_yaml_load(
            """
project:
  manuscript_language: english
  report_language: zh
  citation_style: APA

filters:
  filter_logic: OR
  require_ssci: false
  jcr_quartiles: []
  min_abs_stars: null
  require_ft50: false
  require_utd24: false
  accept_if_ssci_and_jcr_quartile_in: ["Q1", "Q2"]
  accept_if_min_abs_stars: 3
  accept_if_ft50: true
  accept_if_utd24: true
  allowed_fields: ["economics", "finance"]
  journal_whitelist: []
  journal_blacklist: []

journal_lists:
  normalized_json: ".econ-reference-matcher/journals.normalized.json"
  source_csv: []
"""
        )
        errors, warnings = config_tool.validate_config(data)
        self.assertEqual(errors, [])
        self.assertFalse(any("no accept_if" in warning for warning in warnings))

    def test_invalid_filter_logic_is_rejected(self) -> None:
        data = config_tool.minimal_yaml_load(config_tool.DEFAULT_CONFIG)
        data["filters"]["filter_logic"] = "XOR"
        errors, _ = config_tool.validate_config(data)
        self.assertIn("filters.filter_logic must be AND or OR", errors)

    def test_quality_preference_does_not_create_extra_hard_filters(self) -> None:
        data = config_tool.minimal_yaml_load(config_tool.DEFAULT_CONFIG)
        filters = data["filters"]
        self.assertTrue(filters["require_ssci"])
        self.assertEqual(filters["jcr_quartiles"], [])
        self.assertIsNone(filters["min_abs_stars"])
        self.assertFalse(filters["require_ft50"])
        self.assertFalse(filters["require_utd24"])

    def test_boolean_is_not_a_valid_abs_star_count(self) -> None:
        data = config_tool.minimal_yaml_load(config_tool.DEFAULT_CONFIG)
        data["filters"]["min_abs_stars"] = True
        data["filters"]["accept_if_min_abs_stars"] = False
        errors, _ = config_tool.validate_config(data)
        self.assertTrue(any("filters.min_abs_stars" in error for error in errors))
        self.assertTrue(any("filters.accept_if_min_abs_stars" in error for error in errors))


class CandidateNormalizationTests(unittest.TestCase):
    def test_normalize_candidate_from_common_fields(self) -> None:
        row = {
            "Title": "Online Marketplaces and Search Frictions",
            "Authors": "Alex Example and Riley Sample",
            "Year": "2024",
            "Journal": "Journal of Example Economics",
            "DOI": "10.0000/example",
            "Abstract": "Marketplaces lower search frictions.",
        }
        result = normalize_candidates.normalize_candidate(row, 0)
        self.assertEqual(result["title"], "Online Marketplaces and Search Frictions")
        self.assertEqual(result["year"], 2024)
        self.assertEqual(result["doi"], "10.0000/example")
        self.assertIn("Alex Example", result["authors"])


class AlignmentScoreTests(unittest.TestCase):
    def test_opposite_results_and_reversed_causality_are_not_auto_classified(self) -> None:
        claim = {
            "claim_id": "C1",
            "text": "Exports increase firm productivity.",
            "citation_need": "direct support",
        }
        for excerpt in (
            "Exports increase firm productivity.",
            "Exports do not increase firm productivity.",
            "Exports decrease firm productivity.",
            "Firm productivity increases exports.",
        ):
            with self.subTest(excerpt=excerpt):
                result = score_alignment.score_pair(claim, {"id": "P1", "evidence_excerpt": excerpt})
                self.assertGreater(result["lexical_overlap"], 0)
                self.assertNotIn("category", result)
                self.assertTrue(result["review_required"])

    def test_paraphrase_with_no_shared_words_is_not_rejected(self) -> None:
        result = score_alignment.score_pair(
            {"text": "Platforms lower search costs."},
            {"abstract": "Online marketplaces reduce information frictions."},
        )
        self.assertEqual(result["lexical_overlap"], 0)
        self.assertNotIn("category", result)
        self.assertTrue(result["review_required"])

    def test_non_latin_claim_is_not_given_a_failure_score(self) -> None:
        result = score_alignment.score_pair(
            {"text": "\u5e73\u53f0\u964d\u4f4e\u641c\u7d22\u6210\u672c"},
            {"abstract": "Platforms lower search costs."},
        )
        self.assertIsNone(result["lexical_overlap"])
        self.assertTrue(result["review_required"])

    def test_supplied_excerpt_is_not_scored_as_verified_evidence(self) -> None:
        result = score_alignment.score_pair(
            {"text": "Exports increase productivity."},
            {"evidence_excerpt": "Exports increase productivity."},
        )
        self.assertEqual(result["provided_text"], "excerpt")
        self.assertNotIn("evidence_score", result)
        self.assertNotIn("total_score", result)

    def test_cli_retains_all_pairs_for_review(self) -> None:
        from argparse import Namespace

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            claims = root / "claims.json"
            candidates = root / "candidates.json"
            output = root / "overlap.json"
            claims.write_text(json.dumps([{"id": "C1", "text": "Exports increase productivity."}]), encoding="utf-8")
            candidates.write_text(json.dumps([
                {"id": "P1", "abstract": "Exports increase productivity."},
                {"id": "P2", "abstract": "International sales improve efficiency."},
                {"id": "P3"},
            ]), encoding="utf-8")
            score_alignment.cmd_score(Namespace(claims=str(claims), candidates=str(candidates), output=str(output)))
            payload = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(payload["schema"], "econ-reference-matcher.alignment-scores.v2")
            self.assertEqual({item["candidate_id"] for item in payload["scores"]}, {"P1", "P2", "P3"})
            self.assertTrue(all(item["review_required"] for item in payload["scores"]))


class ReportCheckTests(unittest.TestCase):
    def test_sample_report_is_valid(self) -> None:
        text = (ROOT / "examples/report.sample.md").read_text(encoding="utf-8")
        result = check_report.check_report(text, min_final=3)
        self.assertTrue(result["valid"], result)
        self.assertEqual(result["warnings"], [])


class BenchmarkCommonTests(unittest.TestCase):
    def test_load_gold_requires_matching_task_id(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            gold_dir = Path(tmp)
            payload = {
                "task_id": "E999",
                "target_claims": [],
                "category_gold": [],
                "scoring": {},
            }
            (gold_dir / "E001.gold.json").write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaises(FileNotFoundError):
                common.load_gold("E001", gold_dir)


class BenchmarkGraderTests(unittest.TestCase):
    def grade_report(self, report: str, gold: dict) -> dict:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "E999.gold.json").write_text(json.dumps({"task_id": "E999", **gold}), encoding="utf-8")
            (root / "report.md").write_text(report, encoding="utf-8")
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "benchmarks/public/scripts/grade_output.py"),
                    "--task-id", "E999", "--report", str(root / "report.md"),
                    "--gold-dir", str(root), "--output", str(root / "grading.json"),
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertIn(result.returncode, (0, 1), result.stderr)
            return json.loads((root / "grading.json").read_text(encoding="utf-8"))

    def test_one_paper_title_and_doi_count_once(self) -> None:
        gold = {"must_find": [
            {"title": "Paper A", "doi": "10.0000/a"},
            {"title": "Paper B", "doi": "10.0000/b"},
        ]}
        report = "## Final Recommendations\n### 1. Paper A\n- **Category:** Direct Support\n- **DOI / URL:** 10.0000/a\n"
        result = self.grade_report(report, gold)
        self.assertEqual(result["dimensions"]["direct_support_precision"], 12.5)

    def test_decoy_in_final_list_is_not_excused_by_rejection_section(self) -> None:
        gold = {"forbidden_decoys": [{"title": "Decoy Paper"}]}
        report = (
            "## Final Recommendations\n### 1. Decoy Paper\n- **Category:** Direct Support\n\n"
            "## Rejected Topic-Adjacent Candidates\nSome other paper was rejected.\n"
        )
        result = self.grade_report(report, gold)
        self.assertIn("forbidden_decoy_labeled_direct_support", result["critical_failures"])
        self.assertEqual(result["dimensions"]["decoy_rejection"], 0)

    def test_custom_canary_leak_invalidates_score(self) -> None:
        result = self.grade_report("PRIVATE_MARKER_123", {"canaries": ["PRIVATE_MARKER_123"]})
        self.assertTrue(result["invalid"])
        self.assertEqual(result["total_score"], 0)


class BenchmarkLeakCheckTests(unittest.TestCase):
    def test_missing_gold_is_reported_as_skipped(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            task = root / "tasks" / "E999-test"
            task.mkdir(parents=True)
            (task / "target_passages.json").write_text('{"id":"E999"}', encoding="utf-8")
            gold_dir = root / "gold"
            gold_dir.mkdir()
            result = subprocess.run(
                [sys.executable, str(ROOT / "benchmarks/public/scripts/leak_check.py"),
                 "--tasks", str(root / "tasks"), "--gold", str(gold_dir)],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0)
            self.assertIn("E999: SKIP", result.stdout)

    def test_cli_does_not_print_private_marker(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            task = root / "tasks" / "E999-test"
            task.mkdir(parents=True)
            (task / "target_passages.json").write_text('{"id":"E999"}', encoding="utf-8")
            (task / "prompt.md").write_text("PRIVATE_MARKER_123", encoding="utf-8")
            gold_dir = root / "gold"
            gold_dir.mkdir()
            (gold_dir / "E999.gold.json").write_text(
                '{"task_id":"E999","canaries":["PRIVATE_MARKER_123"]}', encoding="utf-8"
            )
            result = subprocess.run(
                [sys.executable, str(ROOT / "benchmarks/public/scripts/leak_check.py"),
                 "--tasks", str(root / "tasks"), "--gold", str(gold_dir)],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, 1)
            self.assertIn("LEAK", result.stdout)
            self.assertNotIn("PRIVATE_MARKER_123", result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
