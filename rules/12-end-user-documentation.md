# Rule 12 — End-User Documentation (Non-Technical Readers)

> **Scope: shared by Modes A, B, and C.** It governs every document, or part of a
> document, written for people who use the system rather than build or run it. It applies
> in full to the **User Manual** (Mode A `03-user-manual.md`, Mode B
> `06-user-manual-draft.md`). Its vocabulary (section 2) and error guidance (section 3)
> also bind the **Read This First** layer of every document (Rule 35), the **Proposal
> body** in all three modes, and user-facing slides. The Technical and Developer Manuals
> keep their exact commands and technical terms; this rule does not apply to them.
>
> Claude acts as a technical writer for end users: the reader has no technical background
> and no knowledge of software architecture, code, or databases.

## 1. Core writing principles
- **User goals, not mechanics.** Frame every heading and task around what the reader
  wants to accomplish ("How to Approve an Invoice"), never around the internal process,
  a module, or a data structure.
- **Zero technical background.** Write at about an 8th-grade reading level. Short
  sentences, common words, one idea each (Rule 10).
- **One action per step.** Break every procedure into short, numbered, sequential steps.
  State the expected result after the step when it helps ("A confirmation message
  appears").
- **Day-one test.** A new user must be able to complete the task on their first day
  without asking a developer or administrator for help.

## 2. Vocabulary: banned terms and their replacements
Never use developer or technical jargon in end-user text. Replace each term with the
user-friendly equivalent below. Add product-specific jargon the user rejects to the
evidence base's **Words to Avoid** table (Rule 10), which `tools/lint_docs.py` enforces.

| Do not use | Use instead |
|------------|-------------|
| Backend, API, server | System, application |
| Execute, trigger | Run, start, click |
| Input parameters, arguments | Details, fields, information |
| Authenticate, authorization | Log in, permissions |
| Database record, query | Item, saved details |
| Null, Boolean | Empty, a Yes or No option |
| Exception, stack trace | Error message, technical issue |

- The table is a minimum. Treat any word the reader would have to ask an engineer about
  the same way (endpoint, schema, cache, payload, token, deploy, instance, log file).
- The only exception is a product whose user interface **is** the command line (Mode A
  Rule 40 section 3). There, name the command the user types, still in plain words.
- `tools/lint_docs.py` reports every banned term in a User Manual (check `jargon`) and
  warns about any fenced code block in it.

## 3. Structure and formatting
1. **Action-oriented titles.** Title documents and task sections with a verb and the
   user's task: "Updating Your Profile", not "User Profile Management Logic".
2. **User interface references.**
   - Put every clickable element, button, and menu label in **bold**, exactly as it
     appears on screen: "Click **Save Details**."
   - Capitalize field labels exactly as the screen shows them.
   - Write menu navigation with `>` between the steps: Go to **Settings** >
     **Account Preferences**.
   - Mode B: labels come from the Design's screen inventory and carry
     `[VERIFY: final label]` until the screen exists.
3. **Error guidance.** When a step can fail, tell the reader what to do next ("Check
   your internet connection, or contact Support"). Do not explain why the system failed
   internally. Quote the on-screen message exactly (Mode A) or mark it `[VERIFY]`
   (Mode B).
4. **No code.** No code snippets, SQL, file paths, configuration keys, or explanations of
   backend logic. Mode A `path:line` citations go to the evidence base, not the manual
   (Rule 20).

## 4. Self-verification audit
Before reporting a User Manual, or the user-facing layer of any other document, as
done, check:
- [ ] Does it contain code, SQL, file paths, or backend logic? Remove them.
- [ ] Does it use a term from section 2, or any other developer jargon? Replace it.
- [ ] Is every heading and task named by what the user wants to do?
- [ ] Does every step contain one action, with UI labels in **bold**?
- [ ] Does every error tell the user what to do next?
- [ ] Could a non-technical user complete each workflow on day one without asking an
      engineer? If not, add the missing step or prerequisite.

Rule 50's checklist repeats these items under Quality. The linter catches the mechanical
part; the judgment items remain a manual review.
