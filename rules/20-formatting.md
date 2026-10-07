# Rule 20 — Formatting

> **Scope: shared by Mode A and Mode B.**

## Markdown
- Use GitHub-Flavored Markdown (GFM).
- Exactly one `#` H1 per document (the document title). Use `##` for major sections
  and `###` for subsections. Do not skip levels.
- Number major sections in manuals and plans (`## 1. Introduction`) so they can be cited.
- Every document of more than 3 sections has a Table of Contents after the
  Document Control block.
- Every code block has a language tag: ` ```bash `, ` ```powershell `, ` ```python `,
  ` ```ts `, ` ```json `, ` ```yaml `, ` ```sql `, ` ```text `.
- Use tables for structured comparisons (modules, config keys, roles, risks, milestones).
- Use Mermaid (` ```mermaid `) for diagrams: architecture, data flow, sequence, ERD,
  Gantt timelines. Keep diagrams under about 20 nodes. Split larger ones.
- Use GFM alerts for callouts:
  `> [!NOTE]`, `> [!TIP]`, `> [!IMPORTANT]`, `> [!WARNING]`, `> [!CAUTION]`.

## Paths and references
- Write file paths relative to the source project root, in backticks: `src/api/users.ts`.
- When you cite code, use `path:line` or `path:start-end`: `src/auth/login.ts:42-60`.
- Do not put code references in the User Manual or the Proposal body. An appendix is allowed.

## Document Control block (required at the top of every document)
```markdown
| Field | Value |
|-------|-------|
| Project | <Product name> |
| Document | <Document type> |
| Version | 0.1 (Draft) |
| Date | YYYY-MM-DD |
| Prepared by | <Author / "Generated with Claude, reviewed by <name>"> |
| Status | Draft / In Review / Approved |
| Source revision | Mode A: <git commit SHA or "working copy, YYYY-MM-DD">. Mode B: <"Brief v<n>, YYYY-MM-DD"> |
```
Add a **Revision History** table at the end of every document.

## Files
- Output path: `output/<mode>/<project-slug>/NN-<document-name>.md`, where `<mode>` is
  `mode-a` (existing project) or `mode-b` (new project), and `<project-slug>` is
  lowercase-kebab-case.
- Images and diagrams that cannot be Mermaid go in `output/<mode>/<project-slug>/assets/`.
- Screenshots that are not available: insert `![Screenshot: <what it shows>](assets/TBD.png)`
  plus `[TBD: capture screenshot of <screen>]`.

## Export
- Markdown is the master format. If the user asks for Word or PDF, convert the
  finished Markdown. Do not author directly in those formats.
- Word: `node tools/md_to_docx.js output/<mode>/<slug>` writes `.docx` files to
  `output/<mode>/<slug>/export/` (first time: `npm install` in `tools/`). Mermaid diagrams
  appear as source with a note; review markers are highlighted.
- PDF: open the `.docx` in Word and save as PDF, or use the `pdf` skill.
