# Rule 10 — Writing Style

> **Scope: shared by Modes A, B, and C.**

## Voice
- Use plain, professional English. Prefer short sentences (target ≤ 25 words).
- Use active voice and present tense: "The system validates the form", not
  "The form will be validated by the system".
- In procedures, use the imperative and address the reader as "you":
  "Click **Save**." / "Run the migration."
- Avoid marketing language and filler ("seamless", "robust", "cutting-edge",
  "simply", "just", "easily"). State capabilities and let facts speak.
- Avoid unexplained jargon. Define every acronym on first use, e.g.
  "Role-Based Access Control (RBAC)", and add it to the Glossary.
- Never use the section sign (§) in a document, a slide, or speaker notes. Write the word:
  "section 4", "Brief section 7", "Profile sections 10 and 12", "sections 4 to 8"
  ("Section 4" at the start of a sentence or table cell).

## Tone per document
| Document | Tone |
|----------|------|
| Completion Plan | Direct, factual, status-oriented. Report problems plainly. |
| Proposal | Persuasive but evidence-based. Benefits are tied to features that exist or are planned. |
| User Manual | Friendly, task-focused, non-technical. No code, no file paths, no stack traces. |
| Technical Manual | Precise, operational. Exact commands, values, ports, and paths. |
| Developer Manual | Precise, explanatory. Explains *why* as well as *how*. |
| Project Brief (Mode B) | Neutral, factual record of what the user said and decided. |
| Requirements Specification (Mode B) | Exact and testable. Uses "shall" for mandatory requirements. |
| System Design (Mode B) | Precise, explanatory. States each design decision and its reason. |
| Test Plan (Mode B) | Exact, checklist-style. Every test traces to a requirement. |
| Modernization Brief (Mode C) | Neutral record: current facts from the profile, user decisions, and labeled proposals, kept apart. |
| Current State Assessment (Mode C) | Direct, evidence-based. Each finding has a severity and a one-line reason. No blame. |
| Target Requirements / Design / Migration Plan / Test Plan (Mode C) | As the Mode B equivalents. Current system in present tense with code evidence; target system in future tense. |
| Modernization Proposal (Mode C) | Persuasive but evidence-based. Problems come from assessment findings; benefits from features and findings resolved. |

## Procedures
- One action per numbered step. Put the expected result after the step when useful:
  "3. Click **Submit**. A confirmation message appears."
- State prerequisites before the first step.
- UI labels go in **bold**, exactly as they appear on screen.
- Keyboard keys use `<kbd>`: <kbd>Ctrl</kbd> + <kbd>S</kbd>.

## Terminology
- Use the product's own names for screens, menus, roles, and entities (Mode A: taken
  from the UI strings, routes, or models in the code; Mode B: taken from the brief's
  Glossary).
- Pick one term per concept and never vary it ("user" vs "member" vs "account").

## Audience and wording
- **Problems from the users' point of view.** In proposals and plans, state each problem as
  the people who use the system feel it ("cannot find last month's records", "reports take
  a day"), then confirm it with evidence. Technical causes follow in one short paragraph
  or go to an appendix.
- **Approvers read only what helps them decide.** Keep proposal bodies to the decision:
  problem, solution, scope, time, cost, risk, the ask. Technical detail goes in an appendix.
- **Roles, not personal names.** Name approvers, builders, and testers by role
  ("Management", "the development team", "QA personnel"), unless the user asks for names.
  The evidence base records the choice (Mode A Profile section 2, Mode B Brief section 3).
  Never invent a person's name.
- **Words to avoid are binding.** When the user rejects a word or phrase, add it to the
  **Words to Avoid** table in the evidence base (Profile section 17.1, Brief section 16.1;
  Mode C: the brief's Decisions and Interview Log). Replace it in every document, the
  INDEX, and the slides. Paraphrase an earlier quote that contains it and mark it
  "user, paraphrased". `tools/lint_docs.py` reports any remaining use in Modes A and B.
- After a wording change, search the whole output folder for the old terms and fix every
  hit outside Revision History rows:
  `grep -rn -i -E "<old term 1>|<old term 2>" output/<mode>/<slug> --include=*.md`.
