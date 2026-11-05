---
name: system-map
description: MODES A, B, AND C. Write the System Map of a project, one document that shows the whole system and where each part is described — users and roles, parts (modules), screens and navigation, data stores, outside systems, deployment, a feature-to-system cross-reference, and the main flow — with diagrams. Mode A maps the system as built, Mode B the planned system, Mode C the current and target systems side by side. Use when the user asks for a system map, system overview, system landscape, architecture map, module map, "map of the project", or "show me all the parts of the system".
argument-hint: <slug or path> [--mode a|b|c]
---

# System Map

> **Shared by all modes.** The System Map summarizes what the evidence base and the suite
> already say; it adds no facts of its own.

> **Rules:** Before starting, read `rules/70-system-map.md` and the active mode's rules
> (`mode-*/rules/30-*.md` and `mode-*/rules/40-document-specific.md`). They are not
> preloaded. Mode C also reads `mode-c-modernize-project/rules/50-readability-and-refinement.md`.

Input: `$ARGUMENTS`.

## Step 1 — Find the mode and the prerequisites
1. If `--mode` is given, use it. Otherwise look for the slug under `output/mode-c/`,
   `output/mode-b/`, and `output/mode-a/`. If it exists in more than one, ask once which
   one to map. A code path with no output folder is Mode A: run the `doc-intake`
   procedure first.
2. Check the prerequisites (Rule 70 section 2):

   | Mode | Needs | If missing |
   |------|-------|------------|
   | A | `00-project-profile.md` | Run `doc-intake` |
   | B | `00-project-brief.md` and `02-system-design.md` | Run `new-brief`, then `new-design` |
   | C | `00-modernization-brief.md` and `03-target-system-design.md` | Run `mod-brief`, then `mod-design` |

3. Read every document that exists in the folder. In Mode A, the manuals (`03`–`05`) give
   better "Detail in" targets than the profile when they exist.

## Step 2 — Write the map
Write `templates/system-map.md` to the file Rule 70 section 2 names (Mode A
`07-system-map.md`, Mode B `11-system-map.md`, Mode C `09-system-map.md`):
- Take each section's facts from the sources in Rule 70 section 3, and cite them.
- Keep every template heading; a heading that does not apply gets
  `Not applicable — <one-line reason>.`
- Reuse the identical Mermaid source for the "System in one picture" and the case flow
  when another document in the folder already has them (Rule 35 section 4).
- Write the Read This First page and an "In short" note under every numbered section
  (Rule 35; Mode C Rule 50 sections 1 and 3).
- Mode B: future tense, nothing described as built. Mode C: "Today" in the present tense,
  "Target" in the future tense, never mixed in one row.

## Step 3 — Check
1. Run `python tools/lint_docs.py output/<mode>/<slug>` and fix every error.
2. Run the Rule 70 section 5 checks and the Rule 50 checklist.
3. If the folder has an `INDEX.md`, add or update the System Map row (audience, status,
   Open Items count). If it has a Project Documentation and Implementation Plan, add the
   map to its inventory and reading order (Rule 65), with a new version and Revision
   History row.

## Step 4 — Report
Give the file written (as a link), the lint result, the gaps found (rows marked `[TBD]`
because no document describes that part), and every `[TBD]`, `[ASSUMPTION]`, `[VERIFY]`,
and `[DECISION]` marker that needs the user's input.
