# Rule 55 — Applying a Change to an Existing Suite

> **Scope: Modes A and B.** Mode C follows
> `mode-c-modernize-project/rules/50-readability-and-refinement.md` section 5, which uses
> the same steps with the Mode C order. This rule is not preloaded: `/doc-suite` and
> `/new-suite` read it in Step 0 when the output folder already holds documents.

## 1. When it applies
The output folder already holds the documents, and the input describes a change instead
of a new project. Typical changes:

| Change | Example |
|--------|---------|
| Answers to open questions | "The approver is the Board; the deadline is 2027-03-31" |
| A decision | "Use PostgreSQL", "pilot at the main branch first" |
| Scope | "Add SMS reminders", "drop the mobile app" |
| Wording or names | "Do not say in-house", "replace the names with roles" |
| Readability | "It is hard to read", "the proposal is too technical" |
| Mode A: the code changed | A new commit adds or finishes features |

Do **not** regenerate the suite. Regeneration loses review changes the user already made.

## 2. Order
A change always flows from the evidence base outward, so every document reads the same
fact.

| Step | Mode A | Mode B |
|------|--------|--------|
| 1. Evidence base | `00-project-profile.md`: section 2 for answers, 17.1 for words to avoid. If the code changed, re-read the changed areas and update the inventory with new `path:line` cites. | `00-project-brief.md`: the changed section, the Interview Log, and section 16.1. Increase the brief version (`v3` → `v4`). |
| 2. Documents | 01 Plan → 02 Proposal → 03 User Manual → 04 Technical Manual → 05 Developer Manual → repo docs | 01 Requirements → 02 Design → 03 Plan → 04 Proposal → 05 Test Plan → 06–08 draft manuals → 09 Gap Report |
| 3. INDEX | Open Items and their counts, statuses | Open Items and their counts, Decisions Needed, statuses |
| 4. Slides and kit | The proposal `.pptx` (Rule 60), rebuilt from the updated proposal | Same, then the starter kit's `docs/design/` copy and the rule files that cite a changed section (Mode B Rule 40 section 10) |
| 5. Checks | Section 4 below | Section 4 below |
| 6. Exports | Render diagrams, then `node tools/md_to_docx.js output/mode-a/<slug>` | Same, for `output/mode-b/<slug>` |

Skip a document the change does not touch, but check it with a search before you skip it
(section 4).

## 3. In each changed document
1. Update the **Source revision** in the Document Control block (Mode A: the new commit
   SHA; Mode B: the new brief version).
2. Increase the document **Version** (`0.1` → `0.2`).
3. Add a **Revision History** row that says what changed and why, in one line.
4. Update the readability layer (Rule 35): the Read This First answers, the "In short"
   notes, and the executive summary must match the changed sections.
5. Move resolved markers out of **Open Items**, and add new ones.
6. Edit with small, exact replacements (each old text matches once). Do not rewrite a
   whole document for a local change.

## 4. Checks
1. Run `python tools/lint_docs.py output/<mode>/<slug>` and fix every error.
2. For every changed fact, term, or name, search the folder for the old value and fix
   every hit outside Revision History rows:

   ```bash
   grep -rn -i -E "<old value 1>|<old value 2>" output/<mode>/<slug> --include=*.md
   ```

3. Read the Read This First section of each changed document once more.

## 5. Scope additions
A new feature touches every layer. In Mode B, in this order:

1. Brief: a new `F-xx` with priority and decision state.
2. Requirements: new `FR-xx` with acceptance criteria, and a Traceability Matrix row.
3. Design: the component, screen, or endpoint that implements it.
4. Plan: new WBS items with sizes, then the capacity re-check (Rule 45 section 4). Say
   plainly when the slack is gone, and add a risk.
5. Test Plan: test cases for each new Must and Should requirement.
6. Proposal: scope, timeline, and cost; then the slides.

In Mode A, a feature the user wants added becomes a **Planned** feature in the profile,
then WBS items in the Plan, then Proposal scope. Never describe it as built.

## 6. When to ask
- Ask **one** question, with options, only when the change cannot be applied without it:
  for example, which role replaces each personal name.
- Otherwise apply the change, and report what changed and what is still open.

## 7. Report
List the files changed with their new versions, the old values replaced (with counts),
the final lint result, and the Open Items the change created or closed.
