# Rule 25 — Typography

> **Scope: shared by Modes A, B, and C.** It applies to every output format the factory
> produces: the Word export (`tools/md_to_docx.js`), HTML pages and online decks, and
> PowerPoint files. Markdown stays the master format (Rule 20). Writers never set fonts in
> Markdown; the exporters apply this rule.

## 1. Principles
- **One type system.** Every document, page, and slide uses the same families, scale, and
  colours, so a reader moves between formats without noticing a change.
- **Readability first.** Comfortable line length, generous line height, and strong
  contrast take priority over density or decoration.
- **Cross-platform.** Every family has a metric-compatible or system fallback, so layout
  does not shift on Windows, macOS, Linux, iOS, or Android.
- **Accessible.** All text meets WCAG 2.2 level AA contrast (section 7). Body text aims for
  level AAA (7:1).

## 2. Font families and CSS font stacks

| Role | Primary | CSS font stack (web) | Office (Word, PowerPoint) |
|------|---------|----------------------|---------------------------|
| Text and headings | Calibri | `Calibri, Carlito, "Segoe UI", system-ui, -apple-system, BlinkMacSystemFont, "Helvetica Neue", Roboto, "Noto Sans", Arial, sans-serif` | Calibri |
| Slide titles (display) | Cambria | `Cambria, Caladea, Georgia, "Times New Roman", serif` | Cambria |
| Code, paths, keys | Consolas | `Consolas, "Cascadia Mono", "SF Mono", Menlo, "DejaVu Sans Mono", "Liberation Mono", "Courier New", monospace` | Consolas |

- Carlito and Caladea are metric-compatible with Calibri and Cambria (Linux, LibreOffice).
  Line breaks stay the same when the primary font is missing.
- Use no other families. Never load web fonts from a third-party CDN in an exported page.
- Calibri has a small x-height. On the web, never set body text below 16 px.

```css
:root {
  --font-sans: Calibri, Carlito, "Segoe UI", system-ui, -apple-system, BlinkMacSystemFont,
    "Helvetica Neue", Roboto, "Noto Sans", Arial, sans-serif;
  --font-display: Cambria, Caladea, Georgia, "Times New Roman", serif;
  --font-mono: Consolas, "Cascadia Mono", "SF Mono", Menlo, "DejaVu Sans Mono",
    "Liberation Mono", "Courier New", monospace;
}
```

## 3. Type scale — print (Word export, A4)

Page: A4, 2 cm margins on all sides. Sizes are in points (pt); 1 pt = 1.333 px.

| Element | Markdown | Word style | Size | Weight | Line spacing | Space before / after | Colour |
|---------|----------|------------|------|--------|--------------|----------------------|--------|
| H1 — document title | `#` | Title | 20 pt | Bold (700) | 1.0 | 0 / 12 pt | `#1F3864` |
| H2 — major section | `##` | Heading 1 | 15 pt | Bold (700) | 1.0 | 18 / 6 pt | `#1F3864` |
| H3 — subsection | `###` | Heading 2 | 12.5 pt | Bold (700) | 1.0 | 12 / 5 pt | `#2F5496` |
| H4 — minor heading | `####` | Heading 3 | 11 pt | Bold (700) | 1.0 | 10 / 4 pt | `#2F5496` |
| Body text | paragraph | Normal | 10.5 pt | Regular (400) | 1.15 | 0 / 6 pt | `#000000` |
| Table text | table | Normal | 10.5 pt | Regular; header row Bold | 1.15 | 0 / 0 | `#000000`; header fill `#D9E2F3` |
| Caption, note, footer | — | — | 8–9 pt | Regular or Italic | 1.0 | 0 / 6 pt | `#595959` |
| Inline code, paths | `` `code` `` | — | 9.5 pt | Regular | inherit | — | `#000000` |
| Code block | fenced block | — | 8.5 pt | Regular | 1.0 | 3 / 6 pt | `#000000` on `#F2F2F2` |
| Keyboard key | `<kbd>` | — | body size | Bold | inherit | — | `#000000` |
| Review marker | `[TBD]` etc. | — | body size | Regular | inherit | — | `#000000` on yellow highlight |

- Headings keep with the next paragraph, so a heading never ends a page.
- Lists indent 0.25 in per level, with a hanging indent for the bullet or number.
- Footer: right-aligned, "<Document title> | Page X of Y".

## 4. Type scale — screen (HTML pages, online decks, rendered Markdown)

Base: `html { font-size: 100%; }` (16 px). Use `rem` for sizes and `em` for spacing that
should follow the element's own size.

| Element | Size (rem / px) | Weight | Line height | Letter spacing | Margin (top / bottom) |
|---------|-----------------|--------|-------------|----------------|-----------------------|
| H1 | 2rem / 32 px | 700 | 1.25 | -0.01em | 0 / 0.75em |
| H2 | 1.5rem / 24 px | 700 | 1.3 | -0.005em | 2em / 0.5em |
| H3 | 1.25rem / 20 px | 600 | 1.4 | 0 | 1.5em / 0.5em |
| H4 | 1.125rem / 18 px | 600 | 1.4 | 0 | 1.25em / 0.5em |
| Body text | 1rem / 16 px | 400 | 1.6 | 0 | 0 / 1em |
| Lead paragraph (optional) | 1.125rem / 18 px | 400 | 1.6 | 0 | 0 / 1em |
| Caption, footnote, source line | 0.875rem / 14 px | 400 | 1.45 | 0.01em | 0.5em / 1em |
| Inline code | 0.875em (of parent) | 400 | inherit | 0 | — |
| Code block | 0.875rem / 14 px | 400 | 1.5 | 0 | 1em / 1.25em; padding 1em |

### UI elements

| Element | Size (rem / px) | Weight | Line height | Letter spacing | Notes |
|---------|-----------------|--------|-------------|----------------|-------|
| Button | 0.9375rem / 15 px | 600 | 1.2 | 0.01em | Sentence case; minimum target 44 × 44 px |
| Form label | 0.875rem / 14 px | 600 | 1.4 | 0.01em | Above the field, 0.25em gap |
| Input text | 1rem / 16 px | 400 | 1.4 | 0 | 16 px avoids iOS zoom on focus |
| Helper or error text | 0.8125rem / 13 px | 400 | 1.4 | 0.01em | Error text also has an icon or prefix, not colour alone |
| Navigation item | 0.9375rem / 15 px | 500 | 1.3 | 0 | — |
| Table header | 0.875rem / 14 px | 600 | 1.4 | 0.02em | Sentence case; no all-caps |
| Table cell | 0.9375rem / 15 px | 400 | 1.45 | 0 | Numbers right-aligned with `font-variant-numeric: tabular-nums` |
| Badge or tag | 0.75rem / 12 px | 600 | 1.2 | 0.03em | The only text allowed at 12 px |
| Tooltip | 0.8125rem / 13 px | 400 | 1.4 | 0 | — |

- Never set text below 12 px (0.75rem). Body and input text never go below 16 px.
- Use letter spacing of 0.05em or more only for short all-caps labels, such as a slide
  eyebrow. Never use all caps for sentences.
- Use font weights 400, 500, 600, and 700 only.

## 5. Type scale — slides (online deck and PowerPoint, 16:9)

| Element | Family | Size | Weight | Line spacing |
|---------|--------|------|--------|--------------|
| Cover title | Cambria | 40–44 pt | Bold | 1.0 |
| Slide title | Cambria | 28–32 pt | Bold | 1.0; one line only (Mode C Rule 50) |
| Eyebrow (section label) | Calibri | 12–14 pt | Semibold, all caps, 0.08em spacing | 1.0 |
| Body and bullets | Calibri | 18–24 pt | Regular | 1.15 |
| Card heading, flow-step label | Calibri | 15–22 pt | Semibold or Bold | 1.0 |
| Card text, flow-step text, slide note | Calibri | 14–16 pt | Regular | 1.15 |
| Number badge (circle with a step number) | Calibri | 12–16 pt | Bold | 1.0 |
| Large figure (effort, cost) | Calibri | 40–60 pt | Bold | 1.0 |
| Table text | Calibri | 14–16 pt | Regular; header Bold | 1.1 |
| Source line, footer, slide number | Calibri | 11–12 pt | Regular | 1.0 |

- No free-standing body text or bullets below 18 pt. No card text, flow-step text, slide
  note, or table text below 14 pt. If text does not fit, move detail to the speaker notes
  instead of shrinking it.
- Text in an accent colour (eyebrows, highlighted labels, "New:" callouts) must still meet
  4.5:1 on its own background, including tinted cards. Check every accent against the page,
  card, and highlight fills it sits on.
- When a slide-deck artifact type or design system supplies its own fonts, keep them. It
  must still meet the minimum sizes and contrast in this rule.

## 6. Line length and layout
- **Screen prose:** 60–80 characters per line. Set `max-width: 72ch` on text columns.
  Tables, diagrams, and code may be wider.
- **Print prose:** A4 with 2 cm margins at 10.5 pt gives about 95 characters per line.
  That is the maximum for body text; never reduce margins or font size to fit more.
- **Code:** keep lines in code blocks at 100 characters or fewer, so they do not wrap in
  the Word export (8.5 pt Consolas fits about 100). Break long commands with the shell's
  continuation character (`\` in Bash, `` ` `` in PowerShell).
- **Headings:** keep heading text short enough for one line, about 60 characters.
- **Alignment:** left-align all text. Never justify, because it causes uneven word gaps.
  Centre only cover titles and short slide statements.
- **Paragraphs:** separate paragraphs with space, not first-line indents.

## 7. Colour and contrast

All pairs below were checked against WCAG 2.2. Normal text needs at least 4.5:1. Large
text (18 pt / 24 px, or 14 pt / 18.67 px bold) and UI components need at least 3:1.

| Use | Foreground | Background | Ratio | Level |
|-----|------------|------------|-------|-------|
| Body text (print) | `#000000` | `#FFFFFF` | 21:1 | AAA |
| Body text (screen, light) | `#1A1A1A` | `#FFFFFF` | 17.4:1 | AAA |
| H1, H2 | `#1F3864` | `#FFFFFF` | 11.6:1 | AAA |
| H3, H4 | `#2F5496` | `#FFFFFF` | 7.4:1 | AAA |
| Caption, footer, muted text | `#595959` | `#FFFFFF` | 7.0:1 | AAA |
| Muted text in a code or callout box | `#595959` | `#F2F2F2` | 6.3:1 | AA |
| Link | `#0563C1` | `#FFFFFF` | 5.9:1 | AA |
| Table header text | `#000000` | `#D9E2F3` | 16.1:1 | AAA |
| Code block text | `#000000` | `#F2F2F2` | 18.8:1 | AAA |
| Review marker | `#000000` | `#FFFF00` | 19.6:1 | AAA |
| Body text (screen, dark) | `#E6E6E6` | `#1E1E1E` | 13.4:1 | AAA |
| Link (screen, dark) | `#8AB4F8` | `#1E1E1E` | 7.9:1 | AAA |

- The lightest grey allowed for text on white is `#767676` (4.5:1). Never use `#808080`
  or lighter for text.
- Never use colour alone to carry meaning. Pair it with text, an icon, or a pattern; for
  example, a status cell reads "High" and is also shaded.
- HTML pages support light and dark themes with the colours above, set as CSS custom
  properties on `:root`.

## 8. What writers do in Markdown
Writers cannot set fonts in Markdown, but they control what the exporters can render well:
- Use no inline HTML styling (`<font>`, `style="…"`, `<span style>`) and no colour in
  Markdown.
- Use **bold** for UI labels and key terms. Use *italic* sparingly. Never use all caps
  for emphasis.
- Use heading levels H1–H4 only. H5 and H6 are not styled by the exporters.
- Keep code lines at 100 characters or fewer, and headings to one line (section 6).
- Put review markers in square brackets exactly as written (`[TBD: …]`), so the Word
  export can highlight them.

## 9. Where this rule is applied

| Output | Applied by |
|--------|------------|
| Word (`.docx`) | `tools/md_to_docx.js` (styles, footer, code and table formatting) |
| HTML pages Claude writes (INDEX views, online decks without a design system) | The CSS tokens in sections 2, 4, and 7 |
| PowerPoint (`.pptx`) | The `pptx` skill, using section 5 (Mode C Rule 50 section 8) |

If you change a value here, change the exporter in the same commit so they never drift.
