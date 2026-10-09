"""Tests for tools/md_to_pptx.js (proposal slides, Rule 60). Skipped without Node or pptxgenjs."""
from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
import textwrap
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "md_to_pptx.js"
NODE = shutil.which("node")
HAS_DEPS = (ROOT / "tools" / "node_modules" / "pptxgenjs").is_dir()

PROPOSAL = textwrap.dedent("""\
    # Demo App — Project Proposal

    | Field | Value |
    |-------|-------|
    | Project | Demo App |
    | Document | Project Proposal |
    | Version | 0.1 (Draft) |
    | Date | 2026-10-04 |
    | Prepared for | [TBD: approver] |
    | Status | Draft |

    ## Table of Contents

    ## 1. Executive Summary
    - **What:** an online booking system.

    ## 2. Background and Problem Statement
    > [!NOTE]
    > **In short:** Bookings are on paper.

    ### 2.2 Problem / Opportunity
    | Problem (users' words) | What it means for them |
    |------------------------|------------------------|
    | "We double-book" | Two customers at one time |

    ## 3. Objectives
    Not applicable — objectives are in the brief.

    ## 5. Scope
    ### 5.1 In Scope
    - Online booking page
    - Reminders by email and SMS, sent the day
      before each appointment
    ### 5.2 Out of Scope
    - Payments

    ## 7. Timeline and Milestones
    | Milestone | Description | Target date |
    |-----------|-------------|-------------|
    | Phase 1 complete | Foundation | End of week 2 |
    | Go-live | Release 1.0 | End of week 9 |

    ## 9. Budget and Cost Breakdown
    | Item | Description | Cost |
    |------|-------------|------|
    | Development | About 124 person-days | [TBD] |
    | Total | | [TBD] |

    ## 14. Recommendation and Next Steps
    1. Approve Phase 1 to begin on [TBD: start date].

    ## Open Items
    | Marker | Item | Needed from |
    |--------|------|-------------|
    | [TBD] | Start date | Client |

    ## Revision History
    | Version | Date | Author | Changes |
    |---|---|---|---|
    | 0.1 | 2026-10-04 | Claude | Initial draft |
    """)


@unittest.skipUnless(NODE and HAS_DEPS, "needs node and npm install in tools/")
class MdToPptxTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.folder = Path(self._tmp.name) / "output" / "mode-b" / "demo-app"
        self.folder.mkdir(parents=True)
        (self.folder / "04-project-proposal.md").write_text(PROPOSAL, encoding="utf-8")
        self.spec = self.folder / "deck" / "proposal-slides.json"

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def run_tool(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run([NODE, str(TOOL), str(self.folder), *args], capture_output=True,
                              text=True, encoding="utf-8", cwd=ROOT)

    def test_draft_follows_the_proposal(self):
        r = self.run_tool("--draft")
        self.assertEqual(r.returncode, 0, r.stderr)
        slides = json.loads(self.spec.read_text(encoding="utf-8"))["slides"]
        kinds = [(s["type"], s["title"]) for s in slides]
        self.assertEqual(kinds[0], ("cover", "Demo App"))
        self.assertEqual(kinds[-1], ("ask", "The ask"))
        self.assertNotIn("What we want to achieve", [t for _, t in kinds])  # Not applicable
        problem = next(s for s in slides if s["title"] == "The problem")
        self.assertEqual(problem["type"], "table")
        self.assertEqual(problem["lead"], "Bookings are on paper.")
        scope = next(s for s in slides if s["type"] == "columns")
        self.assertIn("Reminders by email and SMS, sent the day before each appointment",
                      scope["left"]["bullets"])  # wrapped list item joined
        self.assertEqual(next(s for s in slides if s["type"] == "timeline")["milestones"][1],
                         {"label": "Go-live", "date": "End of week 9"})

    def test_build_writes_slides_and_notes(self):
        r = self.run_tool()
        self.assertEqual(r.returncode, 0, r.stderr)
        out = self.folder / "export" / "Demo-App-Project-Proposal-Slides.pptx"
        with zipfile.ZipFile(out) as z:
            names = z.namelist()
            slides = [n for n in names if n.startswith("ppt/slides/slide") and n.endswith(".xml")]
            notes = [n for n in names if n.startswith("ppt/notesSlides/") and n.endswith(".xml")]
            budget = next(z.read(n).decode("utf-8") for n in slides if "Budget" in z.read(n).decode("utf-8"))
        spec = json.loads(self.spec.read_text(encoding="utf-8"))
        self.assertEqual(len(slides), len(spec["slides"]))
        self.assertEqual(len(notes), len(spec["slides"]))
        self.assertIn("[TBD]", budget)

    def test_existing_spec_is_kept_without_force(self):
        self.run_tool("--draft")
        r = self.run_tool("--draft")
        self.assertEqual(r.returncode, 2)
        self.assertIn("--force", r.stderr)

    def test_invented_figure_and_marker_are_reported(self):
        self.run_tool("--draft")
        spec = json.loads(self.spec.read_text(encoding="utf-8"))
        spec["slides"][1]["bullets"] = ["Saves 40 hours a month [TBD: savings]"]
        spec["slides"][1]["type"] = "bullets"
        self.spec.write_text(json.dumps(spec), encoding="utf-8")
        r = self.run_tool("--strict")
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn('figure "40" is not in the proposal', r.stdout)
        self.assertIn("marker [TBD: savings] is not in the proposal", r.stdout)


if __name__ == "__main__":
    unittest.main()
