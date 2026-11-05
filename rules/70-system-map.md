# Rule 70 — System Map

> **Scope: shared by Modes A, B, and C.** This rule is not preloaded; `/system-map`,
> `/doc-suite`, `/new-suite`, and `/mod-suite` read it in the step that writes the
> document. One template serves all three modes: `templates/system-map.md`.

## 1. What it is
The System Map is the one place where a reader sees the whole system and finds every
part of it: who uses it, its parts, its screens, where the data lives, what it connects
to, and where it runs. Each view links to the document section that holds the detail.
It answers "where is it, and where is it described?", never "how is it built?".

- **Audience:** new team members, the technical lead, support staff, and the project
  manager. A reader who knows nothing about the system should be able to point to any
  part of it after ten minutes with the map.
- **It summarizes; it never decides.** Every part, screen, entity, outside system, and
  server comes from the evidence base or a suite document, cited by section. A fact that
  no document holds is a gap in that document: add it there first (Rule 00, item 4), then
  cite it.
- **Tone:** precise and plain, like the Developer Manual (Rule 10). The Read This First
  page, the role map, and the screen map follow Rule 12 vocabulary; the part, data, and
  deployment tables keep their exact technical names.
- **Tense by mode:** Mode A describes the system as built (present tense, code evidence).
  Mode B describes the planned system (future tense; nothing is described as built).
  Mode C shows the current system in the present tense and the target system in the future
  tense, side by side, never mixed in one table row.

## 2. File name and place

| Mode | File | Written by | After |
|------|------|------------|-------|
| A | `output/mode-a/<slug>/07-system-map.md` | `/doc-suite` Step 3a, or `/system-map <slug>` | The profile (alone) or the Step 3 review (in a suite) |
| B | `output/mode-b/<slug>/11-system-map.md` | `/new-suite` Step 3a, or `/system-map <slug>` | The System Design |
| C | `output/mode-c/<slug>/09-system-map.md` | `/mod-suite` Step 3a, or `/system-map <slug>` | The Target System Design |

- In a suite it is written in **Step 3a**, after the consistency review and **before** the
  Project Documentation and Implementation Plan (Rule 65), so that plan lists it in its
  inventory and points developers to it from its reading order.
- `--only map` writes it alone in a suite, provided its prerequisites exist. The INDEX
  lists it, the Word export includes it, and the build repository starter kit (Modes B
  and C) copies it with the rest of the suite into `docs/design/`.
- Mode A may write it from the profile alone. Then the "Detail in" column cites profile
  sections and is refreshed when the manuals are written.

## 3. Where each section gets its facts

| Section | Mode A (existing project) | Mode B (new project) | Mode C (modernization) |
|---------|---------------------------|----------------------|------------------------|
| 2 System in One Picture | Profile sections 6, 8, 12 | Brief sections 4, 9; Design section 2.2 | Today: Profile sections 6, 8, 12. Target: Design sections 2.3, 9 |
| 3 Users and Roles | Profile section 8 | Brief section 4; Design section 7 | Brief section 5; Design section 8 |
| 4 Parts (Module Map) | Profile sections 4–6 (with `path:line`) | Design sections 2.3, 2.4, 14 | Current: Profile sections 4–6. Target: Design sections 2.4, 2.5, 4 (Component Mapping) |
| 5 Screens and Navigation | Profile section 9; User Manual | Design sections 6.1, 6.2 | Current: Profile section 9. Target: Design sections 7.1, 7.2 |
| 6 Data Map | Profile section 10; Developer Manual data model | Brief section 7; Design section 4 | Current: Profile section 10. Target: Design sections 5.1–5.3 |
| 7 Integration Map | Profile section 12 | Brief section 9; Design section 8 | Current: Brief section 10. Target: Design section 9 |
| 8 Deployment Map | Profile sections 11, 13; Technical Manual | Design section 12 | Current: Profile section 13. Target: Design section 13 |
| 9 Feature Cross-Reference | Profile section 7 (F-xx) | Brief section 5; Requirements Traceability Matrix | Brief section 6 (Feature Disposition); Requirements Traceability Matrix |
| 10 Main Flow | The case flow of the User Manual or Proposal | Brief section 6; Design section 9 | Design section 10; the case flow of the brief |

Use the mode's evidence rule for every citation (Rule 30 of the active mode). Mode A
statements about code keep their `path:line` citations; a statement taken from a document
cites the document and section instead.

## 4. Section rules
1. **Read This First (Rule 35).** The questions table answers at least: What is the
   system? Who uses it? What are its main parts? Where does the data live? What does it
   connect to? Where does it run? Where do I find the detail? Its picture is the section 2
   picture with the identical Mermaid source. Add the Where to Find What table.
2. **One picture per level.** Context (section 2), parts (section 4), screens (section 5),
   deployment (section 8). Keep each diagram under about 20 nodes (Rule 20); split a large
   system by area, one diagram per area, rather than shrinking labels.
3. **Same names everywhere.** Part, screen, role, entity, and outside-system names are the
   ones the evidence base and its Glossary use. The map introduces no new names.
4. **Every row has a "Detail in" cell** that names a document and section (or a profile
   section in Mode A when the manuals do not exist yet). A row with nothing to cite is a
   gap: mark it `[TBD: not documented in <document>]` and list it in Open Items.
5. **Complete feature cross-reference.** Every feature in the evidence base appears once in
   section 9. Mode C keeps Drop features with "—" in the target columns and their
   disposition. Modes B and C add the requirement IDs; the linter checks that each cited
   `FR-xx` exists.
6. **Mode C side by side.** Sections 2, 4, 5, 6, 7, and 8 show "Today" first, then
   "Target". Section 4.1 maps each current part to its target part with the brief's
   disposition. Modes A and B keep the 4.1 heading with
   `Not applicable — no target system in this mode.`
7. **No secrets or private addresses.** Server names, IP addresses, connection strings,
   and accounts become placeholders (`<APP_SERVER>`, `<DB_SERVER>`), with a note on where
   the real value lives (Rule 00, item 6).
8. **Markers.** Parts, servers, stack layers, and labels keep the markers they carry in the
   source documents (`[TBD]`, `[ASSUMPTION]`, `[DECISION]`, `[VERIFY]`). Collect them in Open
   Items; the INDEX counts them.

## 5. Checks before reporting it done
- [ ] Every part, screen, data store, outside system, and server cites its source.
- [ ] Names match the evidence base Glossary; no new names were introduced.
- [ ] Every feature in the evidence base appears exactly once in section 9.
- [ ] Mode C: every current part maps to a target part or is marked Drop, with the same
      disposition as the brief.
- [ ] Every diagram has at most about 20 nodes, quoted labels, and no label that starts
      with a number and a period (Rule 35 section 5).
- [ ] No secret, private host name, or IP address appears.
- [ ] `python tools/lint_docs.py output/<mode>/<slug>` reports no error.

## 6. After a change to the suite
Rule 55 (Modes A and B) and Mode C Rule 50 section 5 apply. The System Map is updated after
the documents it cites and **before** the Project Documentation and Implementation Plan,
which copies its version into the inventory. A change to parts, screens, data, outside
systems, servers, or features always touches the map. Refresh the starter kit's copy in
`docs/design/` at the same time.
