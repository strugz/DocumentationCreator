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
