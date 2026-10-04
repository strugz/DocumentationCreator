# Rule 00 — Core Principles

> **Scope: shared by Mode A (existing project) and Mode B (new project).**

0. **Know the mode first.** Before writing anything, decide which mode applies:
   - **Mode A — Existing project:** source code exists. Evidence comes from the code.
     Follow `mode-a-existing-project/rules/`. Output goes to `output/mode-a/<slug>/`.
   - **Mode B — New project:** only an idea or brief exists, no code. Evidence comes from
     the user's brief and interview answers. Follow `mode-b-new-project/rules/`.
     Output goes to `output/mode-b/<slug>/`.
   If the request is ambiguous (e.g. "write a proposal for X" with no path), ask once:
   "Does code for this project already exist?"
1. **Accuracy over completeness.** A short, correct document beats a long, invented one.
   Every statement must trace to evidence (see Rule 30 of the active mode) or be
   explicitly marked.
2. **Audience first.** Before writing, name the reader and what they need to *do* after
   reading. Write only what serves that action.
   - Plan → decide what to do next and by when.
   - Proposal → approve, fund, or reject.
   - Requirements Specification → agree on what will be built and how it will be accepted.
   - System Design → build the system the same way across the team.
   - Test Plan → verify that each requirement is met.
   - User Manual → complete a task in the product.
   - Technical Manual → install, configure, operate, troubleshoot, recover.
   - Developer Manual → understand, change, test, and ship code safely.
3. **Read-only on the source project (Mode A).** Never edit, format, install into, or run
   destructive commands against the project being documented. Reading files, listing
   directories, and running read-only commands (`git log`, `--help`, `--version`,
   test listing) are allowed. Running the app or tests requires user approval.
   In Mode B there is no source project; write documents only, never application code.
4. **One source of truth.** Mode A facts live in `output/mode-a/<slug>/00-project-profile.md`.
   Mode B facts live in `output/mode-b/<slug>/00-project-brief.md`. Other documents reuse
   those facts instead of re-deriving them differently. If you find a contradiction, fix
   the profile or brief first.
5. **Consistency across the suite.** Product name, version, module names, role names,
   and terminology must be identical across all documents. Use the Glossary in the
   profile (Mode A) or brief (Mode B) as the canonical list.
6. **No secrets.** Never copy credentials, API keys, tokens, connection strings with
   passwords, private URLs, or personal data into documents.
   Replace with placeholders like `<DB_PASSWORD>` and note where the real value lives.
7. **Ask only when blocked.** If information is missing, mark it (`[TBD: ...]`) and
   continue. Collect all open questions and present them together at the end.
   (Exception: the Mode B brief interview, which asks its questions up front by design.)
