# Rule 35 — Readability Layer and Process Flows

> **Scope: shared by Modes A, B, and C.** Mode C applies the same layer through
> `mode-c-modernize-project/rules/50-readability-and-refinement.md` sections 1 and 3, which
> add the Mode C flows. Readers of a real suite found complete technical documents
> "complex and hard to read" until each one had a plain-language entry point. Write the
> layer in the **first** generation, not after review.

## 1. Which documents
| Has the layer | Does not |
|---------------|----------|
| Mode A: Completion Plan, Proposal, User Manual, Technical Manual, Developer Manual | Mode A Project Profile and Mode B Project Brief (internal evidence bases) |
| Mode B: Requirements, System Design, Project Plan, Proposal, Test Plan, draft manuals, Gap Report | Repo docs (README, ARCHITECTURE, API) and INDEX.md |
| Mode C: every document, including the brief (Mode C Rule 50) | — |

## 2. The layer
1. **A `## Read This First` section** right after the Table of Contents, listed in the
   Table of Contents. It has:
   - a **one-page table** of the questions this reader asks, each answered in one line
     with a link to the section that holds the detail ("When is it ready?" →
     "Release 1.0 in month 4, see [section 7](#7-timeline-and-milestones)");
   - **at least one picture**: a Mermaid flow from section 4 that fits the document;
   - a **"Where to Find What"** table (`I want to…` → section) when the document has
     more than 8 numbered sections.
2. **An "In short" note** at the start of every numbered `##` section, before any
   subsection. An Executive Summary or Summary section needs none; it is the summary.

   ```markdown
   > [!NOTE]
   > **In short:** The system runs on one Windows server and backs up nightly.
   ```

3. **A bullet executive summary** in plans and proposals instead of a dense paragraph:
   **What**, **How**, **When**, **Effort or cost**, **Risks**, **Needed to start** (and
   **The ask** in a proposal). Each bullet is one or two sentences.

## 3. Rules for the layer
- **It summarizes; it never adds.** Every fact in the layer also appears in a numbered
  section. Markers carry over: a `[TBD]` date stays `[TBD]` in the summary.
- **Plain words for the document's reader.** No IDs, code, or file paths in the
  questions table, except in the Developer and Technical Manuals, where an exact command
  or path is the answer.
- **User Manual:** no code, paths, or technical flows. Its picture is the main task or
  case flow in the users' own terms.
- **Mode B:** the layer describes the planned system in the future tense, like the rest of
  the document.
- **One page.** If the questions table needs more than about 10 rows, the document is
  answering too much at once; keep the 10 most important questions.

## 4. Standard process flows
Use the flow that fits the document. Reuse the **identical** Mermaid source when the same
flow appears in several documents, so it reads the same and renders once.

| Flow | Shows | Put it in |
|------|-------|-----------|
| System in one picture | Users, the main parts, the database, outside systems | Proposal, System Design, Technical Manual, Developer Manual |
| Case flow (main workflow) | One real case from start to end in the users' terms, with the key decision | User Manual, Requirements, System Design, Proposal |
| Remaining-work flow (Mode A) | Current state → finish open work → test → acceptance → go-live → handover | Completion Plan |
| SDLC flow | Plan → requirements → design → build in sprints → developer tests → QA → user acceptance → ready to deploy → handover; failed tests loop back to build | Project Plan, Proposal |
| Ready-to-deploy gate | All Must tests pass → testers sign off → acceptance signed → ready | Plan, Test Plan, Proposal |
| Requirement to acceptance | Requirement → design → work item → test → acceptance | Requirements |
| Testing flow | Unit → integration → system → acceptance | Test Plan |
| Defect flow | New → Triaged → In progress → Fixed → Retest → Verified → Closed | Test Plan |
| Request flow | A request from the screen through the API to the database and back | Developer Manual |
| Gap flow | Planned requirement → built? → gap → action | Gap Report |

## 5. Mermaid pitfalls
- A label that starts with a number and a period (`["1. Plan"]`) is parsed as a Markdown
  list and renders **blank**. Write `["Step 1: Plan"]`. `tools/lint_docs.py` reports it.
- Quote every label that contains punctuation or parentheses.
- Keep a flow under about 20 nodes; split a larger one.
- Render diagrams before the Word export (Rule 20 Export), or Word shows the source.
