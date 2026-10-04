"""Tests for evals/grade.py. Run: python -m unittest discover -s tests -v"""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "evals"))
import grade  # noqa: E402

DOC = """# Demo

| Field | Value |
|-------|-------|
| Project | Demo |

Budget: [TBD: budget]
Slack notifications are listed in the README but not implemented [VERIFY].
Slack sends alerts every hour.
| FR-01 | The system shall book. |
| FR-02 | The system shall remind. |
TASKS_PER_PAGE | No | 20 | missing from .env.example
"""


class GradeTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        root = Path(self._tmp.name)
        self.case_dir = root / "case"
        self.case_dir.mkdir()
        self.out = root / "out"
        self.out.mkdir()
        (self.out / "01-doc.md").write_text(DOC, encoding="utf-8")

    def tearDown(self):
        self._tmp.cleanup()

    def run_check(self, check: dict) -> grade.CheckResult:
        check.setdefault("id", "c")
        (self.case_dir / "case.json").write_text(json.dumps({"id": "t", "mode": "b", "checks": [check]}),
                                                 encoding="utf-8")
        return grade.grade(self.case_dir, self.out).checks[0]

    def test_files(self):
        self.assertTrue(self.run_check({"type": "files", "files": ["01-doc.md"]}).passed)
        r = self.run_check({"type": "files", "files": ["01-doc.md", "02-missing.md"]})
        self.assertFalse(r.passed)
        self.assertIn("02-missing.md", r.detail)

    def test_contains_and_case_sensitivity(self):
        self.assertTrue(self.run_check({"type": "contains", "file": "01-doc.md", "pattern": "slack"}).passed)
        self.assertFalse(self.run_check({"type": "contains", "file": "01-doc.md", "pattern": "slack",
                                         "case_sensitive": True}).passed)

    def test_contains_all(self):
        r = self.run_check({"type": "contains_all", "file": "*", "patterns": ["FR-01", "nope"]})
        self.assertFalse(r.passed)
        self.assertIn("nope", r.detail)

    def test_absent(self):
        self.assertTrue(self.run_check({"type": "absent", "file": "*", "pattern": r"\$\d"}).passed)
        r = self.run_check({"type": "absent", "file": "*", "pattern": "hourly|every hour"})
        self.assertFalse(r.passed)
        self.assertIn("01-doc.md:L9", r.detail)

    def test_line(self):
        self.assertTrue(self.run_check({"type": "line", "file": "*", "all": ["TASKS_PER_PAGE", r"\b20\b"]}).passed)
        self.assertFalse(self.run_check({"type": "line", "file": "*", "all": ["TASKS_PER_PAGE", "FR-01"]}).passed)

    def test_qualified_flags_unqualified_claim(self):
        r = self.run_check({"type": "qualified", "file": "*", "pattern": "slack",
                            "allowed_if": "not implemented|verify"})
        # Line 9 is within ±1 of line 8 (qualified), so widen the gap to prove detection.
        self.assertTrue(r.passed)
        (self.out / "02-other.md").write_text("Intro\n\n\nSlack alerts run hourly.\n\n", encoding="utf-8")
        r = self.run_check({"type": "qualified", "file": "*", "pattern": "slack",
                            "allowed_if": "not implemented|verify"})
        self.assertFalse(r.passed)
        self.assertIn("02-other.md:L4", r.detail)

    def test_min_count(self):
        self.assertTrue(self.run_check({"type": "min_count", "file": "01-doc.md",
                                        "pattern": r"^\|\s*FR-\d+", "min": 2}).passed)
        self.assertFalse(self.run_check({"type": "min_count", "file": "01-doc.md",
                                         "pattern": r"^\|\s*FR-\d+", "min": 3}).passed)

    def test_lint_check_counts_errors(self):
        (self.out / "01-doc.md").unlink()
        (self.out / "00-project-brief.md").write_text("# Brief\n\nClean evidence base.\n", encoding="utf-8")
        self.assertTrue(self.run_check({"type": "lint", "max_errors": 0}).passed)
        (self.out / "03-bad.md").write_text("# A\n\n```\nx\n```\n", encoding="utf-8")
        self.assertFalse(self.run_check({"type": "lint", "max_errors": 0}).passed)

    def test_weighted_score(self):
        (self.case_dir / "case.json").write_text(json.dumps({"id": "t", "mode": "b", "checks": [
            {"id": "a", "type": "contains", "file": "*", "pattern": "FR-01", "weight": 3},
            {"id": "b", "type": "contains", "file": "*", "pattern": "nope", "weight": 1},
        ]}), encoding="utf-8")
        r = grade.grade(self.case_dir, self.out)
        self.assertEqual(r.score, 75.0)
        self.assertEqual((r.passed, r.total), (1, 2))

    def test_missing_output_folder(self):
        (self.case_dir / "case.json").write_text(json.dumps({"id": "t", "mode": "b", "checks": [
            {"id": "a", "type": "contains", "file": "*", "pattern": "x"}]}), encoding="utf-8")
        r = grade.grade(self.case_dir, self.out / "nope")
        self.assertEqual(r.score, 0.0)

    def test_real_case_files_are_valid(self):
        cases = Path(__file__).resolve().parents[1] / "evals" / "cases"
        for case_json in cases.glob("*/case.json"):
            data = json.loads(case_json.read_text(encoding="utf-8"))
            ids = [c["id"] for c in data["checks"]]
            self.assertEqual(len(ids), len(set(ids)), f"duplicate check ids in {case_json}")
            for c in data["checks"]:
                self.assertIn(c["type"], grade.CHECKS, f"{case_json}: {c['id']}")


if __name__ == "__main__":
    unittest.main()
