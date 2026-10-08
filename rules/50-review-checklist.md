# Rule 50 — Review Checklist (run before declaring a document done)

> **Scope: shared by Modes A, B, and C.** Run the common sections plus the section for
> the active mode.

## Structure
- [ ] Document Control block is filled in (project, version, date, status, source revision).
- [ ] Table of Contents exists and matches the headings.
- [ ] Every template section is present (or marked "Not applicable — reason").
- [ ] Revision History and Open Items sections exist at the end.

## Accuracy (common)
- [ ] No invented numbers, dates, costs, names, or SLAs.
- [ ] No secrets or personal data copied into the document.

## Accuracy — Mode A (existing project)
- [ ] Every feature, command, endpoint, config key, and screen was confirmed in the source.
- [ ] All uncertainty is marked with `[TBD]`, `[ASSUMPTION]`, or `[VERIFY]`.
- [ ] Facts match `00-project-profile.md` (names, versions, module list, roles).

## Accuracy — Mode B (new project)
- [ ] Every feature, role, and requirement traces to the brief (`F-xx`, `R-xx`, `Brief §n`).
- [ ] Every design choice Claude suggested is labeled **Proposed** with its reason.
- [ ] Every requirement has an ID (`FR-xx` / `NFR-xx`) and acceptance criteria.
- [ ] All uncertainty is marked with `[TBD]`, `[ASSUMPTION]`, `[DECISION]`, or `[VERIFY]`.
- [ ] Facts match `00-project-brief.md` (names, roles, feature IDs, glossary).
- [ ] Nothing is described as already built, working, or tested.

## Accuracy — Mode C (modernize an existing project)
- [ ] Every statement about the current system traces to the Mode A profile or to code
      (`path:line`); no current feature is described that the profile does not list.
- [ ] Every statement about the target system traces to the modernization brief (`F-xx`
      with its disposition, `D-xx`, `R-xx`, Brief §n) and is in the future tense.
- [ ] Every feature from the profile appears in the brief's Feature Disposition table with
      Keep / Improve / Replace / Drop / New, and the same disposition is used everywhere.
- [ ] Every target stack layer is Agreed or **Proposed** with a reason; undecided layers
      are `[DECISION]` items; end-of-support dates are `[VERIFY]`.
- [ ] Every Keep and Improve feature has a parity requirement and a parity test.
- [ ] Every Critical and High assessment finding is resolved by a requirement.
- [ ] All uncertainty is marked with `[TBD]`, `[ASSUMPTION]`, `[DECISION]`, or `[VERIFY]`.
- [ ] Facts match `00-modernization-brief.md` (names, roles, feature IDs, stack, glossary).

## Quality
- [ ] Written for the stated audience (no code in the User Manual; exact commands in
      the Technical Manual).
- [ ] Procedures: one action per step, prerequisites first, expected results stated.
- [ ] All code blocks have language tags; all paths are relative to the project root
      (Mode A) or to the proposed repository structure (Mode B).
- [ ] Mermaid diagrams are syntactically valid (balanced brackets, quoted labels that
      contain special characters).
- [ ] Acronyms are defined on first use and in the Glossary.
- [ ] Internal links and anchors resolve.

## Suite consistency (when more than one document exists)
- [ ] Same product name, version, and terminology everywhere.
- [ ] Proposal scope matches the Plan's WBS; the Plan's features match the User Manual's tasks.
- [ ] Technical Manual config reference matches the Developer Manual's environment setup.
- [ ] Mode B: every Must requirement appears in the Plan's WBS, the System Design, and the
      Test Plan (check the traceability matrix).
- [ ] Mode C: every Must requirement appears in the Migration Plan's WBS, the Target
      System Design, and the Migration Test Plan; the design's Stack Comparison matches
      the brief's Target Tech Stack layer by layer; the proposal's strategy, timeline,
      and scope equal the plan's.

Report the checklist result to the user as a short pass/fail summary. List failures, if any.
