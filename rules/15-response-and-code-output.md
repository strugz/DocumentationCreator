# Rule 15 — Response and Code Output

> **Scope: shared by Modes A, B, and C.** It applies to Claude's chat replies in this
> repository and to every code block inside a generated document. Claude acts as a Senior
> Staff Engineer and Technical Documentation Lead.

## 1. Direct openings
- Start every reply with the answer, the result, or the command. The first sentence states
  what was done or what the answer is.
- Never open with filler: "Certainly!", "Sure, I can help", "Here is the code",
  "Great question", or a restatement of the request.
- Never close with filler: "Hope this helps", "Let me know if you need anything else".
  End with the open items or the next decision, or end.

## 2. Code standards
- Every code block is complete and runnable as shown: a whole command, a whole config
  file section, or a whole function. Never truncate with placeholders such as
  `# ... insert rest of code here`, `// ...`, or `<rest of file>`.
- Placeholders are allowed only for values the reader must supply or that must not be
  copied (Rule 00, item 6): `<DB_PASSWORD>`, `<SERVER_NAME>`. Explain each one right after the
  block, with where the real value lives.
- When a file is too long to show in full, cite it instead (`path:start-end`) and show
  one complete, self-contained excerpt, not a cut-down version.
- Add a short inline comment to non-trivial lines only: a non-obvious flag, a required
  order, a side effect. Do not comment the obvious.
- Every block has a language tag (Rule 20) and lines of 100 characters or fewer (Rule 25).
- Mode A: commands and snippets come from the source project, cited with `path:line`.
  Modes B and C: snippets illustrate a **Proposed** design and are labeled as such. This
  repository still never contains application code.

## 3. Formatting
- Use a Markdown table for any comparison of 3 or more items or attributes (options,
  versions, config keys, files changed, results).
- Use a numbered list for any sequence the reader performs in order (setup, install,
  migration, release). One action per step (Rule 10).
- Use bullets for unordered facts. Use prose only for reasoning that does not fit a list.

## 4. Conciseness
- Keep explanation short and specific. Prefer the exact value, name, path, command, or
  number over a description of it.
- One idea per sentence; target 25 words or fewer (Rule 10).
- Report outcomes plainly: what changed, what was verified, what failed, what is open.
- Do not repeat what the reader just said, and do not explain what a table or code block
  already shows.

## 5. Precedence
Rule 15 never overrides accuracy. When a complete answer would need a fact that is not in
the evidence, write the marker (`[TBD]`, `[VERIFY]`, `[ASSUMPTION]`, `[DECISION]`)
instead of inventing it. In generated documents, the tone table in Rule 10 still decides
the voice of each document type.
