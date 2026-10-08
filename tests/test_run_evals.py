"""Tests for evals/run_evals.py (prompt building and collection). Run:
python -m unittest discover -s tests -v"""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "evals"))
import run_evals  # noqa: E402


class PromptTest(unittest.TestCase):
    def test_mode_a_prompt_unchanged(self):
        p = run_evals.build_prompt("a-tasktrack")
        self.assertTrue(p.startswith("/doc-suite evals/cases/a-tasktrack/project"))
        self.assertIn("Write only inside `output/mode-a/eval-tasktrack/`.", p)
        self.assertNotIn("Prerequisite", p)
        self.assertNotIn("interview has already happened", p)

    def test_mode_b_prompt_has_idea_and_answers(self):
        p = run_evals.build_prompt("b-clinic-booking")
        self.assertTrue(p.startswith("/new-suite A web system for our clinic"))
        self.assertIn("--no-manuals", p)
        self.assertIn("The interview has already happened", p)
        self.assertIn("go-live deadline 2027-03-31", p)

    def test_mode_c_prompt(self):
        p = run_evals.build_prompt("c-tasktrack-modernize")
        # Points at the shared fixture project, normalized (no `..`).
        self.assertTrue(p.startswith("/mod-suite evals/cases/a-tasktrack/project"), p.splitlines()[0])
        self.assertNotIn("..", p.splitlines()[0])
        self.assertIn("slug `eval-tasktrack`", p)
        self.assertIn("output/mode-c/eval-tasktrack/", p)
        # Prerequisite profile: reuse or build with doc-intake, in the same slug.
        self.assertIn("`output/mode-a/eval-tasktrack/00-project-profile.md`", p)
        self.assertIn(".claude/skills/doc-intake/SKILL.md", p)
        self.assertIn("for the prerequisite, `output/mode-a/eval-tasktrack/`", p)
        # Scripted interview answers are appended, as for Mode B.
        self.assertIn("The interview has already happened", p)
        self.assertIn("Hosting / infrastructure: not decided yet", p)
        self.assertIn("NON-INTERACTIVE EVALUATION RUN", p)

    def test_mode_c_judge_prompt_names_all_evidence(self):
        p = run_evals.judge_prompt("r1", "c-tasktrack-modernize")
        self.assertIn("evals/cases/a-tasktrack/project/", p)
        self.assertIn("evals/runs/r1/c-tasktrack-modernize/prerequisite/", p)
        self.assertIn("evals/cases/c-tasktrack-modernize/answers.md", p)
        self.assertIn("mode-c-*/rules/", p)

    def test_unknown_case_exits(self):
        with self.assertRaises(SystemExit):
            run_evals.build_prompt("zz-no-such-case")


class CollectTest(unittest.TestCase):
    """collect() moves the generated output and copies the prerequisite next to it."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        root = Path(self._tmp.name)
        self._saved = (run_evals.ROOT, run_evals.CASES, run_evals.RUNS)
        run_evals.ROOT, run_evals.CASES, run_evals.RUNS = root, root / "cases", root / "runs"
        case = root / "cases" / "c-demo"
        case.mkdir(parents=True)
        (case / "case.json").write_text(json.dumps({
            "id": "c-demo", "mode": "c", "slug": "demo",
            "prerequisite": {"mode": "a", "slug": "demo", "file": "00-project-profile.md", "skill": "doc-intake"},
            "checks": []}), encoding="utf-8")
        self.out_c = root / "output" / "mode-c" / "demo"
        self.out_c.mkdir(parents=True)
        (self.out_c / "00-modernization-brief.md").write_text("# Brief\n", encoding="utf-8")
        self.out_a = root / "output" / "mode-a" / "demo"

    def tearDown(self):
        run_evals.ROOT, run_evals.CASES, run_evals.RUNS = self._saved
        self._tmp.cleanup()

    def test_collect_copies_prerequisite_and_keeps_live_copy(self):
        self.out_a.mkdir(parents=True)
        (self.out_a / "00-project-profile.md").write_text("# Profile\n| F-01 | Login |\n", encoding="utf-8")
        dest = run_evals.collect("c-demo", "r1")
        self.assertTrue((dest / "output" / "00-modernization-brief.md").is_file())
        self.assertFalse(self.out_c.exists(), "generated output is moved")
        self.assertTrue((dest / "prerequisite" / "00-project-profile.md").is_file())
        self.assertTrue((self.out_a / "00-project-profile.md").is_file(), "prerequisite is copied, not moved")
        meta = json.loads((dest / "meta.json").read_text(encoding="utf-8"))
        self.assertEqual(meta["prerequisite"], str(self.out_a))

    def test_collect_without_prerequisite_still_collects(self):
        dest = run_evals.collect("c-demo", "r2")
        self.assertTrue((dest / "output").is_dir())
        self.assertFalse((dest / "prerequisite").exists())
        self.assertNotIn("prerequisite", json.loads((dest / "meta.json").read_text(encoding="utf-8")))


if __name__ == "__main__":
    unittest.main()
