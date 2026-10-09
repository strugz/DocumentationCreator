# Rule 30 (Mode C) — Evidence from the Profile and the Modernization Brief

> **Scope: Mode C only (modernize an existing project into a new one).** Mode A uses
> `mode-a-existing-project/rules/30-evidence-and-accuracy.md`; Mode B uses
> `mode-b-new-project/rules/30-evidence-from-brief.md`.

Mode C has **two subjects**: the current system, which exists as code, and the target
system, which does not exist yet. Each has its own evidence and its own tense.

| Subject | Evidence | Tense | Rules that apply |
|---------|----------|-------|------------------|
| Current system | The Mode A Project Profile and the source code behind it | Present ("The API reads the config from…") | Mode A Rule 30: cite `path:line`, mark `[VERIFY]` when stale |
| Target system | The Modernization Brief (interview answers and decisions) | Future or requirement ("The new system shall…") | Mode B Rule 30: label suggestions **Proposed**, mark `[DECISION]` |

Never mix the two. A sentence about the target system must not read as if it were built.
A sentence about the current system must not describe a feature the code does not have.

## Evidence hierarchy (strongest first)
1. Decisions and answers the user states in the modernization interview, recorded in the
   Modernization Brief (target stack, migration strategy, feature dispositions).
2. The Mode A Project Profile (`output/mode-a/<slug>/00-project-profile.md`) and the
   source code it cites. The profile is the record of what exists today.
3. Other Mode A documents for the same project (Completion Plan, Technical Manual,
   Developer Manual), for gaps, debt, and operational facts they already collected.
4. Material the user supplies: incident reports, performance logs, audit findings,
   roadmap notes, vendor end-of-life notices.
5. Public facts about technologies: end-of-life dates, supported versions, licensing.
   Cite the vendor page and mark `[VERIFY]` if it may have changed.
6. Industry practice (OWASP, Twelve-Factor, WCAG): usable only as the basis for a
   **Proposed** item.
7. Reasonable inference, always marked.

If the profile and the user disagree about the current system (for example, the user says
"we have no tests" and the profile lists a test suite), trust the code, record the
conflict in the brief's **Discrepancies** section, and mark `[VERIFY]`.

## Labels and markers (use exactly these forms)
| Label / Marker | Meaning | Example |
|----------------|---------|---------|
| **Proposed** | A target-system choice Claude suggests because the user did not decide it. Always give a one-line reason. | `Backend: ASP.NET Core 8 — **Proposed** (team already writes C#, LTS until 2026-11)` |
| `[DECISION: ...]` | The user must choose between named options. List the options and Claude's recommendation. | `[DECISION: migration strategy — big-bang rewrite / strangler fig / lift-and-shift then refactor. Recommended: strangler fig, because the current system is in production]` |
| `[TBD: ...]` | Information needed that neither the profile nor the user gave. | `[TBD: monthly transaction volume]` |
| `[ASSUMPTION: ...]` | Inferred, plausible, unconfirmed. | `[ASSUMPTION: single production server, based on docker-compose.yml]` |
| `[VERIFY: ...]` | Stated by a source but possibly stale or contradictory. | `[VERIFY: profile cites Node 14; the vendor end-of-life date is 2023-04-30]` |

- Never remove a marker unless the user or the evidence resolves it. When resolved,
  update the brief first, then every document that uses the fact.
- Every document ends with an **Open Items** section that lists all its markers,
  including every `[DECISION]`.

## Citing the current system
- Cite code as `path:line` relative to the **source project root** recorded in the
  brief's `Source location` field (copied from the profile). The linter verifies these
  citations against the source when it can find it.
- Cite the Mode A documents by section, never by line: `Profile section 7`, `Profile section 15`,
  `Technical Manual section 6`. Do not write `00-project-profile.md:42`; the linter would treat
  it as a code citation.
- Copy facts from the profile; do not re-derive them differently. If the profile is wrong,
  fix the profile first (Mode A Rule 00 section 4), then continue.

## Never invent
- Costs, budgets, rates, licence prices, or effort hours. Estimates are allowed only when
  labeled as estimates with the method shown (for example WBS size × team capacity).
- Dates, deadlines, or cutover windows not given by the user.
- Names of people, clients, vendors, or stakeholders.
- Business statistics: current outage counts, user numbers, response times, or defect
  rates that the profile does not contain. Use `[TBD]` and ask.
- Performance improvements ("40 % faster") or savings. State the mechanism ("replaces a
  per-row query with one batch query") and mark the number `[TBD]`.
- Technology end-of-life dates you are not sure of. Mark `[VERIFY]` with the vendor page.
- Features of the current system that the profile does not list. If the user mentions
  one, record it as `[VERIFY: not found in the profile]`.

## Tense and status
- **Current system:** present tense, with evidence. Status values come from the profile:
  Done / Partial / Stub / Broken / Not started.
- **Target system:** future tense or "shall". Never "the new system sends…" as if built.
- **Feature disposition** (brief section 6) uses exactly: **Keep / Improve / Replace / Drop / New**.
  - Keep: same behaviour, new implementation.
  - Improve: same purpose, changed behaviour (state what changes).
  - Replace: a different mechanism serves the same need (for example an off-the-shelf
    service replaces custom code).
  - Drop: not carried into the target system (state why).
  - New: not in the current system; added by the modernization.
- **Decision state** uses exactly: Proposed / Agreed / Deferred.
- **Priority** uses MoSCoW: Must / Should / Could / Won't.

## Traceability
- Features keep the Mode A profile's IDs (`F-01, F-02…`). The brief copies every profile
  feature with a disposition; new features continue the numbering. Roles keep `R-01…`;
  constraints get `C-01…`; assessment findings get `D-01…` (debt and risk items).
- Target requirements get `FR-01…` and `NFR-01…`, each pointing to a feature `F-xx` and,
  where it applies, to a finding `D-xx`.
- Design components, migration WBS items, and test cases point to the `FR`/`NFR` IDs they
  serve. The Target Requirements Specification holds the master **Traceability Matrix**.
- The Migration Test Plan also traces **parity tests** back to the current system's
  behaviour (`F-xx`, Profile section 7) so that nothing is lost in the rewrite.

## Source revision
In the Document Control block write
`Source revision | Profile <mode-a slug> @ <git SHA or "working copy, YYYY-MM-DD">; Modernization Brief v<n>, YYYY-MM-DD`.
