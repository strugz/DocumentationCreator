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

    def _write_prerequisite(self, text: str) -> Path:
        """A collected run stores the prerequisite next to output/."""
        pre = self.out.parent / "prerequisite"
        pre.mkdir(exist_ok=True)
        (pre / "00-project-profile.md").write_text(text, encoding="utf-8")
        return pre

    def test_prerequisite_prefix_resolves_next_to_output(self):
        self.assertFalse(self.run_check({"type": "files", "files": ["prerequisite/00-project-profile.md"]}).passed)
        self._write_prerequisite("# Profile\n")
        self.assertTrue(self.run_check({"type": "files", "files": ["prerequisite/00-project-profile.md"]}).passed)
        self.assertTrue(self.run_check({"type": "contains", "file": "prerequisite/00-project-profile.md",
                                        "pattern": "profile"}).passed)

    def test_prerequisite_falls_back_to_live_output_folder(self):
        case = {"id": "t", "mode": "c", "prerequisite": {"mode": "a", "slug": "zz-no-such-slug"}, "checks": []}
        self.assertIsNone(grade.prerequisite_dir(case, self.out))
        self._write_prerequisite("# Profile\n")
        self.assertEqual(grade.prerequisite_dir(case, self.out), self.out.parent / "prerequisite")

    def test_ids_covered(self):
        self._write_prerequisite("| ID | Feature |\n|---|---|\n| F-01 | Login |\n| F-02 | Export |\n| F-03 | Slack |\n")
        (self.out / "00-modernization-brief.md").write_text(
            "| F-01 | Login | Keep |\n| F-03 | Slack | Drop |\n", encoding="utf-8")
        check = {"type": "ids_covered", "source_file": "prerequisite/00-project-profile.md",
                 "id_pattern": r"^\|\s*(F-\d+)\s*\|", "file": "00-modernization-brief.md"}
        r = self.run_check(dict(check))
        self.assertFalse(r.passed)
        self.assertIn("F-02", r.detail)
        self.assertNotIn("F-01", r.detail)
        (self.out / "00-modernization-brief.md").write_text(
            "| F-01 | Login | Keep |\n| F-02 | Export | Improve |\n| F-03 | Slack | Drop |\n", encoding="utf-8")
        self.assertTrue(self.run_check(dict(check)).passed)

    def test_ids_covered_fails_when_source_has_no_ids(self):
        self._write_prerequisite("# Profile without a feature table\n")
        r = self.run_check({"type": "ids_covered", "source_file": "prerequisite/00-project-profile.md",
                            "id_pattern": r"^\|\s*(F-\d+)\s*\|", "file": "*"})
        self.assertFalse(r.passed)
        self.assertIn("no IDs", r.detail)

    def test_ids_covered_fails_when_prerequisite_missing(self):
        r = self.run_check({"type": "ids_covered", "source_file": "prerequisite/00-project-profile.md",
                            "id_pattern": r"(F-\d+)", "file": "*"})
        self.assertFalse(r.passed)
        self.assertIn("missing source file", r.detail)

    def test_source_dir_for_modes(self):
        (self.case_dir / "proj").mkdir()
        self.assertEqual(grade.source_dir({"mode": "a", "input": "proj"}, self.case_dir), (self.case_dir / "proj").resolve())
        self.assertEqual(grade.source_dir({"mode": "c", "input": "proj"}, self.case_dir), (self.case_dir / "proj").resolve())
        self.assertIsNone(grade.source_dir({"mode": "c", "input": "nope"}, self.case_dir))
        self.assertIsNone(grade.source_dir({"mode": "b", "input": "idea.md"}, self.case_dir))
        # Mode A keeps its historical default of `project/` when `input` is absent.
        (self.case_dir / "project").mkdir()
        self.assertEqual(grade.source_dir({"mode": "a"}, self.case_dir), (self.case_dir / "project").resolve())

    def test_mode_c_case_patterns_accept_expected_rows(self):
        """The Mode C case's structural regexes must match the shapes the templates produce."""
        case = json.loads((Path(__file__).resolve().parents[1] / "evals" / "cases" / "c-tasktrack-modernize"
                           / "case.json").read_text(encoding="utf-8"))
        checks = {c["id"]: c for c in case["checks"]}
        import re
        self.assertTrue(re.search(checks["parity-requirements"]["pattern"],
                                  "| FR-01 | The target system shall sign in users. | Parity | Must | F-01 | … |",
                                  re.M | re.I))
        self.assertTrue(re.search(checks["parity-tests"]["pattern"], "| TC-P-01 | Login parity | FR-01 |", re.M))
        self.assertTrue(re.search(checks["features-carried"]["id_pattern"], "| F-07 | Slack notifications |", re.M))
        self.assertFalse(re.search(checks["no-invented-org"]["pattern"], "Increment 2 moves the task list.", re.I))
        self.assertFalse(re.search(checks["target-not-built"]["pattern"],
                                   "The current system has been deployed on one server.", re.I))
        self.assertTrue(re.search(checks["target-not-built"]["pattern"],
                                  "The new system has been deployed to production.", re.I))

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
