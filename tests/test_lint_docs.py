"""Tests for tools/lint_docs.py. Run: python -m unittest discover -s tests -v"""
from __future__ import annotations

import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import lint_docs  # noqa: E402


def control(doc_type: str, revision: str = "Brief v1, 2026-10-04") -> str:
    return textwrap.dedent(f"""\
        | Field | Value |
        |-------|-------|
        | Project | Demo App |
        | Document | {doc_type} |
        | Version | 0.1 (Draft) |
        | Date | 2026-10-04 |
        | Prepared by | Generated with Claude |
        | Status | Draft |
        | Source revision | {revision} |
        """)


def document(title: str, doc_type: str, body: str, open_items: str = "", revision: str = "Brief v1, 2026-10-04") -> str:
    sections = [line[3:] for line in body.splitlines() if line.startswith("## ")]
    toc = "\n".join(f"- [{s}](#{lint_docs.github_slug(s)})" for s in sections + ["Open Items", "Revision History"])
    oi = open_items or "| — | None | — |"
    return (
        f"# {title}\n\n{control(doc_type, revision)}\n## Table of Contents\n{toc}\n\n{body}\n\n"
        f"## Open Items\n| Marker | Item | Needed from |\n|--------|------|-------------|\n{oi}\n\n"
        "## Revision History\n| Version | Date | Author | Changes |\n|---|---|---|---|\n"
        "| 0.1 | 2026-10-04 | Claude | Initial draft |\n"
    )


BRIEF = textwrap.dedent("""\
    # Project Brief — Demo App

    | Field | Value |
    |-------|-------|
    | Project | Demo App |

    ## 5. Features
    | ID | Feature | Priority |
    |----|---------|----------|
    | F-01 | Sign in | Must |
    | F-02 | Reports | Should |
    """)

REQ_BODY = textwrap.dedent("""\
    ## 1. Functional Requirements
    | ID | Requirement | Priority | Source | Acceptance criteria |
    |----|-------------|----------|--------|---------------------|
    | FR-01 | The system shall let users sign in. | Must | F-01 | Valid users reach the dashboard. |
    | FR-02 | The system shall export reports. | Should | F-02 | A CSV file downloads. |
    | FR-03 | The system shall support dark mode. | Could | F-02 | Theme toggles. |

    ## 2. Diagram
    ```mermaid
    flowchart LR
        U[Users] --> S["Demo App (web)"]
        S --> DB[(Database)]
    ```

    ## 3. Traceability Matrix
    | Feature | Requirement | Design component | WBS item | Test case |
    |---------|-------------|------------------|----------|-----------|
    | F-01 | FR-01 | Auth module | 1.1 | TC-01 |
    | F-02 | FR-02 | Reports module | 2.1 | TC-02 |
    | F-02 | FR-03 | — | — | — |
    """)

DESIGN_BODY = "## 1. Components\n| Component | Implements |\n|---|---|\n| Auth module | FR-01 |\n| Reports module | FR-02 |\n"
PLAN_BODY = "## 1. WBS\n| WBS ID | Implements |\n|---|---|\n| 1.1 | FR-01 |\n| 2.1 | FR-02 |\n"
TEST_BODY = "## 1. Test Cases\n| TC ID | Requirement |\n|---|---|\n| TC-01 | FR-01 |\n| TC-02 | FR-02 |\n"


class LintTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.proj = self.root / "output" / "mode-b" / "demo-app"
        self.proj.mkdir(parents=True)
        self.write("00-project-brief.md", BRIEF)
        self.write("01-requirements-specification.md", document("Demo App — SRS", "SRS", REQ_BODY))
        self.write("02-system-design.md", document("Demo App — Design", "System Design", DESIGN_BODY))
        self.write("03-project-plan.md", document("Demo App — Plan", "Project Plan", PLAN_BODY))
        self.write("05-test-plan.md", document("Demo App — Test Plan", "Test Plan", TEST_BODY))

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def write(self, name: str, text: str, folder: Path | None = None) -> Path:
        path = (folder or self.proj) / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def errors(self, *paths: Path, source: str | None = None) -> list[lint_docs.Finding]:
        return [f for f in lint_docs.lint(list(paths) or [self.proj], source) if f.severity == "error"]

    def assertCheck(self, findings, check: str, fragment: str = "") -> None:
        hits = [f for f in findings if f.check == check and fragment in f.message]
        self.assertTrue(hits, f"expected a '{check}' finding containing {fragment!r}; got {findings}")


class TestValidProject(LintTestCase):
    def test_valid_project_has_no_errors(self):
        self.assertEqual(self.errors(), [])


class TestStructure(LintTestCase):
    def test_two_h1(self):
        p = self.write("02-system-design.md", document("D", "System Design", DESIGN_BODY + "\n# Another H1\n"))
        self.assertCheck(self.errors(p), "structure", "exactly one H1")

    def test_skipped_heading_level(self):
        p = self.write("02-system-design.md", document("D", "System Design", DESIGN_BODY + "\n#### Too deep\n"))
        self.assertCheck(self.errors(p), "structure", "skipped")

    def test_missing_doc_control_field(self):
        text = document("D", "System Design", DESIGN_BODY).replace("| Source revision | Brief v1, 2026-10-04 |\n", "")
        p = self.write("02-system-design.md", text)
        self.assertCheck(self.errors(p), "structure", "Source revision")

    def test_missing_revision_history(self):
        text = document("D", "System Design", DESIGN_BODY).split("## Revision History")[0]
        p = self.write("02-system-design.md", text)
        self.assertCheck(self.errors(p), "structure", "Revision History")

    def test_evidence_base_is_exempt_from_doc_control(self):
        self.assertEqual(self.errors(self.proj / "00-project-brief.md"), [])


class TestContent(LintTestCase):
    def test_unfilled_placeholder(self):
        p = self.write("02-system-design.md", document("D", "System Design", DESIGN_BODY + "\nOwner: {{name}}\n"))
        self.assertCheck(self.errors(p), "placeholders", "{{name}}")

    def test_code_block_without_language(self):
        p = self.write("02-system-design.md", document("D", "System Design", DESIGN_BODY + "\n```\nnpm start\n```\n"))
        self.assertCheck(self.errors(p), "code", "language tag")

    def test_unclosed_fence(self):
        p = self.write("02-system-design.md", document("D", "System Design", DESIGN_BODY + "\n```bash\nnpm start\n"))
        self.assertCheck(self.errors(p), "code", "never closed")

    def test_mermaid_unknown_type(self):
        p = self.write("02-system-design.md", document("D", "System Design", DESIGN_BODY + "\n```mermaid\nflowchat LR\n  A --> B\n```\n"))
        self.assertCheck(self.errors(p), "mermaid", "Unknown")

    def test_mermaid_unquoted_special_label(self):
        p = self.write("02-system-design.md", document("D", "System Design", DESIGN_BODY + "\n```mermaid\nflowchart LR\n  A[Web (SPA)] --> B\n```\n"))
        self.assertCheck(self.errors(p), "mermaid", "quoted")

    def test_mermaid_cylinder_shape_is_fine(self):
        p = self.write("02-system-design.md", document("D", "System Design", DESIGN_BODY + "\n```mermaid\nflowchart LR\n  A --> DB[(Database)]\n```\n"))
        self.assertEqual([f for f in self.errors(p) if f.check == "mermaid"], [])

    def test_broken_anchor(self):
        p = self.write("02-system-design.md", document("D", "System Design", DESIGN_BODY + "\nSee [x](#no-such-heading).\n"))
        self.assertCheck(self.errors(p), "links", "no-such-heading")

    def test_secret_detected(self):
        p = self.write("02-system-design.md", document("D", "System Design", DESIGN_BODY + "\n```text\nDB_PASSWORD=Hunter2Secret\n```\n"))
        self.assertCheck(self.errors(p), "secrets")

    def test_placeholder_secret_is_fine(self):
        p = self.write("02-system-design.md", document("D", "System Design", DESIGN_BODY + "\n```text\nDB_PASSWORD=<DB_PASSWORD>\n```\n"))
        self.assertEqual([f for f in self.errors(p) if f.check == "secrets"], [])

    def test_markers_without_open_items(self):
        text = document("D", "System Design", DESIGN_BODY + "\nHosting: [TBD: hosting provider]\n")
        p = self.write("02-system-design.md", text)
        self.assertCheck(self.errors(p), "markers", "Open Items lists no TBD")

    def test_markers_listed_in_open_items(self):
        text = document("D", "System Design", DESIGN_BODY + "\nHosting: [TBD: hosting provider]\n",
                        open_items="| TBD | Hosting provider | Client |")
        p = self.write("02-system-design.md", text)
        self.assertEqual([f for f in lint_docs.lint([p]) if f.check == "markers"], [])


class TestTraceability(LintTestCase):
    def test_undefined_requirement_reference(self):
        p = self.write("02-system-design.md", document("D", "System Design", DESIGN_BODY + "| Billing | FR-99 |\n"))
        self.assertCheck(self.errors(p), "ids", "FR-99")

    def test_undefined_feature_reference(self):
        p = self.write("03-project-plan.md", document("P", "Project Plan", PLAN_BODY + "\nCovers F-07.\n"))
        self.assertCheck(self.errors(p), "ids", "F-07")

    def test_must_requirement_missing_from_test_plan(self):
        p = self.write("05-test-plan.md", document("T", "Test Plan", "## 1. Test Cases\n| TC ID | Requirement |\n|---|---|\n| TC-02 | FR-02 |\n"))
        self.assertCheck(self.errors(p), "trace", "FR-01")

    def test_could_requirement_may_be_uncovered(self):
        # FR-03 is "Could" and appears nowhere downstream: allowed.
        self.assertEqual([f for f in self.errors() if "FR-03" in f.message], [])

    def test_empty_matrix_cell_for_must(self):
        req = REQ_BODY.replace("| F-01 | FR-01 | Auth module | 1.1 | TC-01 |", "| F-01 | FR-01 | Auth module | — | TC-01 |")
        p = self.write("01-requirements-specification.md", document("S", "SRS", req))
        self.assertCheck(self.errors(p), "trace", "WBS item")

    def test_matrix_column_not_required_before_document_exists(self):
        (self.proj / "03-project-plan.md").unlink()
        req = REQ_BODY.replace("| F-01 | FR-01 | Auth module | 1.1 | TC-01 |", "| F-01 | FR-01 | Auth module | — | TC-01 |")
        p = self.write("01-requirements-specification.md", document("S", "SRS", req))
        self.assertEqual([f for f in self.errors(p) if f.check == "trace"], [])


class TestCitations(LintTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.src = self.root / "src-project"
        self.write("app.py", "line1\nline2\nline3\n", folder=self.src / "src")
        self.a = self.root / "output" / "mode-a" / "demo"
        self.a.mkdir(parents=True)
        self.write("00-project-profile.md",
                   f"# Project Profile — Demo\n\n| Field | Value |\n|---|---|\n| Source location | {self.src} |\n", folder=self.a)

    def manual(self, cite: str) -> Path:
        return self.write("05-developer-manual.md",
                          document("Dev", "Developer Manual", f"## 1. Code\nEntry point: `{cite}`.\n", revision="abc1234"),
                          folder=self.a)

    def test_valid_citation(self):
        self.assertEqual(self.errors(self.manual("src/app.py:2-3")), [])

    def test_missing_file(self):
        self.assertCheck(self.errors(self.manual("src/nope.py:1")), "citations", "does not exist")

    def test_line_out_of_range(self):
        self.assertCheck(self.errors(self.manual("src/app.py:2-9")), "citations", "outside")


if __name__ == "__main__":
    unittest.main()
