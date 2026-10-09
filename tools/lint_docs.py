#!/usr/bin/env python3
"""Deterministic checks for generated documentation (Rule 50, mechanical part).

Usage:
    python tools/lint_docs.py <file-or-folder> [...] [--source PATH] [--json] [--strict]

Checks every Markdown document under output/mode-a/, output/mode-b/, or output/mode-c/<slug>/:
  structure    one H1, no skipped heading levels, Document Control block,
               Table of Contents vs headings, Open Items and Revision History present
  markers      every [TBD]/[ASSUMPTION]/[VERIFY]/[DECISION] is listed in Open Items
  placeholders no unfilled {{...}} template placeholders, leftover template comments,
               or section signs (write 'section N')
  code         every fenced code block has a language tag; fences are balanced
  mermaid      known diagram type, balanced brackets, quoted special labels, size,
               no label that starts with 'N.' (renders blank)
  wording      no word from the evidence base's 'Words to Avoid' table in other documents
  readability  (warning) a 'Read This First' section and an 'In short' note under every
               numbered ## section (Rule 35)
  links        internal #anchors resolve to a heading
  secrets      no credentials, keys, or connection strings with passwords
  citations    (Modes A and C) every `path:line` exists in the source project
  ids          F-xx / FR-xx / NFR-xx references point to defined IDs
  trace        (Modes B and C) Must/Should requirements reach Design, Plan, and Test Plan

Exit code: 0 = no errors, 1 = errors found (or warnings with --strict), 2 = usage error.
Standard library only.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from dataclasses import asdict, dataclass, field
from pathlib import Path

# ---------------------------------------------------------------- constants

MARKER_RE = re.compile(r"\[(TBD|ASSUMPTION|VERIFY|DECISION)(?::\s*([^\]]*))?\]")
PLACEHOLDER_RE = re.compile(r"\{\{[^}]*\}\}")
TEMPLATE_COMMENT_RE = re.compile(r"<!--.*?-->", re.S)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
FENCE_RE = re.compile(r"^(\s*)(`{3,}|~{3,})(.*)$")
LINK_ANCHOR_RE = re.compile(r"\]\(#([^)\s]+)\)")
CITATION_RE = re.compile(r"`([A-Za-z0-9_.\-/\\]+\.[A-Za-z0-9]+):(\d+)(?:-(\d+))?`")
ID_DEF_RE = re.compile(r"^\|\s*((?:N?FR|F|R|US|TC|UAT|S|C|G|D|P)-[\w-]+)\s*\|")
REQ_REF_RE = re.compile(r"\b(N?FR-\d+)\b")
FEATURE_REF_RE = re.compile(r"\bF-\d+\b")

DOC_CONTROL_FIELDS = ["Project", "Document", "Version", "Date", "Status", "Source revision"]
MERMAID_TYPES = {
    "flowchart", "graph", "sequenceDiagram", "erDiagram", "gantt", "classDiagram",
    "stateDiagram", "stateDiagram-v2", "pie", "journey", "mindmap", "timeline",
    "gitGraph", "quadrantChart", "requirementDiagram", "C4Context", "C4Container",
    "C4Component", "block-beta", "sankey-beta", "xychart-beta",
}
MERMAID_MAX_NODES = 20

SECRET_PATTERNS = [
    (re.compile(r"(?i)(?<![a-z])(password|passwd|pwd|secret|api[_-]?key|access[_-]?token|auth[_-]?token)(?![a-z])\s*[:=]\s*[\"']?(?![<{\[$%])(?=[^\s\"'`|]*[0-9!@#^&*])[^\s\"'`|]{6,}"),
     "Looks like a credential value"),
    (re.compile(r"\bAKIA[0-9A-Z]{16}\b"), "Looks like an AWS access key"),
    (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"), "Private key block"),
    (re.compile(r"\bgh[pousr]_[A-Za-z0-9]{36,}\b"), "Looks like a GitHub token"),
    (re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"), "Looks like an API secret key"),
    (re.compile(r"\b[a-z][a-z0-9+.-]*://[^:\s/@<>]+:(?![<{\[$%])[^@\s<>]+@"), "Connection string with an embedded password"),
]

# Documents that are evidence bases, not reader-facing documents.
EVIDENCE_BASE = {"00-project-profile.md", "00-project-brief.md", "00-modernization-brief.md"}
# Per mode: the evidence base that defines F-xx IDs (first match wins).
FEATURE_SOURCES = ("00-project-brief.md", "00-modernization-brief.md", "00-project-profile.md")
# Per mode: the requirements document that holds the Traceability Matrix.
REQUIREMENTS = {
    "b": "01-requirements-specification.md",
    "c": "02-target-requirements-specification.md",
}
# Per mode: document -> traceability matrix column it fills.
TRACE_TARGETS = {
    "b": {
        "02-system-design.md": "Design component",
        "03-project-plan.md": "WBS item",
        "05-test-plan.md": "Test case",
    },
    "c": {
        "03-target-system-design.md": "Design component",
        "04-migration-plan.md": "WBS item",
        "06-migration-test-plan.md": "Test case",
    },
}
MODES = ("mode-a", "mode-b", "mode-c")


# ---------------------------------------------------------------- model

@dataclass
class Finding:
    file: str
    line: int
    severity: str  # "error" | "warning"
    check: str
    message: str


@dataclass
class Doc:
    path: Path
    lines: list[str]
    mode: str  # "a" | "b" | "c" | "?"
    kind: str  # "evidence" | "repo" | "index" | "document"
    headings: list[tuple[int, int, str]] = field(default_factory=list)  # (line, level, text)
    fences: list[tuple[int, int, str]] = field(default_factory=list)  # (start, end, lang)

    @property
    def text(self) -> str:
        return "\n".join(self.lines)

    def in_fence(self, lineno: int) -> bool:
        return any(s <= lineno <= e for s, e, _ in self.fences)


# ---------------------------------------------------------------- parsing

def load_doc(path: Path) -> Doc:
    raw = path.read_text(encoding="utf-8", errors="replace")
    lines = raw.splitlines()
    parts = {p.lower() for p in path.parts}
    mode = next((m[-1] for m in MODES if m in parts), "?")
    if path.name in EVIDENCE_BASE:
        kind = "evidence"
    elif "repo" in parts:
        kind = "repo"
    elif path.name.upper() == "INDEX.MD":
        kind = "index"
    else:
        kind = "document"
    doc = Doc(path=path, lines=lines, mode=mode, kind=kind)

    open_fence = None  # (start_line, marker, lang)
    for i, line in enumerate(lines, 1):
        m = FENCE_RE.match(line)
        if m:
            marker = m.group(2)
            if open_fence is None:
                open_fence = (i, marker, m.group(3).strip())
                continue
            if marker[0] == open_fence[1][0] and len(marker) >= len(open_fence[1]) and not m.group(3).strip():
                doc.fences.append((open_fence[0], i, open_fence[2]))
                open_fence = None
                continue
        if open_fence is None:
            h = HEADING_RE.match(line)
            if h:
                doc.headings.append((i, len(h.group(1)), h.group(2).strip()))
    if open_fence is not None:
        doc.fences.append((open_fence[0], len(lines), open_fence[2] + "\0unclosed"))
    return doc


def github_slug(text: str) -> str:
    text = re.sub(r"`|\*\*|__|\[|\]\([^)]*\)", "", text)
    text = unicodedata.normalize("NFKC", text).lower()
    text = "".join(ch for ch in text if ch.isalnum() or ch in " -_")
    return text.replace(" ", "-")


def heading_slugs(doc: Doc) -> set[str]:
    seen: dict[str, int] = {}
    slugs = set()
    for _, _, text in doc.headings:
        base = github_slug(text)
        n = seen.get(base, 0)
        slugs.add(base if n == 0 else f"{base}-{n}")
        seen[base] = n + 1
    return slugs


def section_span(doc: Doc, title_pattern: str, level: int = 2) -> tuple[int, int] | None:
    """Return (first_line, last_line) of the section whose heading matches the pattern."""
    pat = re.compile(title_pattern, re.I)
    for idx, (ln, lvl, text) in enumerate(doc.headings):
        if lvl == level and pat.search(text):
            end = len(doc.lines)
            for ln2, lvl2, _ in doc.headings[idx + 1:]:
                if lvl2 <= level:
                    end = ln2 - 1
                    break
            return ln, end
    return None


def table_rows(lines: list[str]) -> list[list[str]]:
    rows = []
    for line in lines:
        s = line.strip()
        if not s.startswith("|"):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c):
            continue
        rows.append(cells)
    return rows


# ---------------------------------------------------------------- checks

def check_structure(doc: Doc, out: list[Finding]) -> None:
    f = str(doc.path)
    h1 = [h for h in doc.headings if h[1] == 1]
    if len(h1) != 1:
        out.append(Finding(f, h1[1][0] if len(h1) > 1 else 1, "error", "structure",
                           f"Expected exactly one H1, found {len(h1)}"))
    prev = 0
    for ln, lvl, text in doc.headings:
        if prev and lvl > prev + 1:
            out.append(Finding(f, ln, "error", "structure",
                               f"Heading level skipped (H{prev} → H{lvl}): {text}"))
        prev = lvl

    if doc.kind != "document":
        return

    # Document Control block: first table after the H1 with Field | Value.
    head = doc.lines[: min(len(doc.lines), 40)]
    rows = table_rows(head)
    fields = {r[0].strip("* ").lower(): (r[1] if len(r) > 1 else "") for r in rows}
    if "field" not in fields:
        out.append(Finding(f, 1, "error", "structure", "Missing Document Control block (| Field | Value |)"))
    else:
        for name in DOC_CONTROL_FIELDS:
            if name.lower() not in fields:
                out.append(Finding(f, 1, "error", "structure", f"Document Control block is missing '{name}'"))
            elif not fields[name.lower()].strip():
                out.append(Finding(f, 1, "error", "structure", f"Document Control field '{name}' is empty"))
        date = fields.get("date", "")
        if date and not re.search(r"\d{4}-\d{2}-\d{2}", date) and not PLACEHOLDER_RE.search(date):
            out.append(Finding(f, 1, "warning", "structure", f"Date is not YYYY-MM-DD: {date}"))

    h2 = [(ln, t) for ln, lvl, t in doc.headings if lvl == 2]
    if len(h2) > 3:
        toc = section_span(doc, r"^table of contents$")
        if not toc:
            out.append(Finding(f, 1, "error", "structure", "More than 3 sections but no 'Table of Contents'"))
        else:
            toc_text = "\n".join(doc.lines[toc[0]: toc[1]])
            toc_body = TEMPLATE_COMMENT_RE.sub("", toc_text).strip()
            if not toc_body:
                out.append(Finding(f, toc[0], "error", "structure", "Table of Contents is empty"))
            else:
                for ln, t in h2:
                    if re.match(r"(?i)table of contents", t):
                        continue
                    if github_slug(t) not in toc_text and t not in toc_text:
                        out.append(Finding(f, ln, "warning", "structure",
                                           f"Section not listed in Table of Contents: {t}"))

    for title, label in ((r"open items", "Open Items"), (r"revision history", "Revision History")):
        if not section_span(doc, title):
            out.append(Finding(f, len(doc.lines), "error", "structure", f"Missing '{label}' section"))


def check_placeholders(doc: Doc, out: list[Finding]) -> None:
    f = str(doc.path)
    for i, line in enumerate(doc.lines, 1):
        for m in PLACEHOLDER_RE.finditer(line):
            out.append(Finding(f, i, "error", "placeholders", f"Unfilled template placeholder {m.group(0)}"))
    for m in TEMPLATE_COMMENT_RE.finditer(doc.text):
        ln = doc.text.count("\n", 0, m.start()) + 1
        if doc.in_fence(ln):
            continue
        snippet = " ".join(m.group(0)[4:-3].split())[:60]
        out.append(Finding(f, ln, "warning", "placeholders", f"Leftover template comment: {snippet}"))
    for i, line in enumerate(doc.lines, 1):
        if "§" in line and not doc.in_fence(i):
            out.append(Finding(f, i, "error", "placeholders",
                               "Section sign used; write 'section N' instead (Rule 10)"))


def check_code_blocks(doc: Doc, out: list[Finding]) -> None:
    f = str(doc.path)
    for start, end, lang in doc.fences:
        if lang.endswith("\0unclosed"):
            out.append(Finding(f, start, "error", "code", "Code fence is never closed"))
            lang = lang[:-9]
        if not lang:
            out.append(Finding(f, start, "error", "code", "Code block has no language tag"))


def _strip_quoted(s: str) -> str:
    return re.sub(r'"[^"]*"', '""', s)


def check_mermaid(doc: Doc, out: list[Finding]) -> None:
    f = str(doc.path)
    for start, end, lang in doc.fences:
        if lang.split()[0:1] != ["mermaid"]:
            continue
        body = [l for l in doc.lines[start: end - 1]]
        content = [(start + 1 + i, l) for i, l in enumerate(body) if l.strip() and not l.strip().startswith("%%")]
        if not content:
            out.append(Finding(f, start, "error", "mermaid", "Empty Mermaid diagram"))
            continue
        first = content[0][1].strip().split()[0]
        if first not in MERMAID_TYPES:
            out.append(Finding(f, content[0][0], "error", "mermaid", f"Unknown Mermaid diagram type '{first}'"))
            continue
        if first not in ("flowchart", "graph"):
            continue
        nodes: set[str] = set()
        for ln, line in content[1:]:
            s = PLACEHOLDER_RE.sub("X", _strip_quoted(line))  # placeholders are reported separately
            for o, c in ("[]", "()", "{}"):
                if s.count(o) != s.count(c):
                    out.append(Finding(f, ln, "error", "mermaid", f"Unbalanced '{o}{c}' in: {line.strip()}"))
                    break
            if NUMBERED_LABEL_RE.search(line):
                out.append(Finding(f, ln, "error", "mermaid",
                                   "Label starts with 'N.' and renders blank; write 'Step N: ...': "
                                   + line.strip()))
            for m in re.finditer(r"\[([^\]\"]*)\]", s):
                label = m.group(1)
                inner = label[1:-1] if label.startswith("(") and label.endswith(")") else label
                inner = inner.strip("/\\")
                if re.search(r"[(){}]", inner):
                    out.append(Finding(f, ln, "error", "mermaid",
                                       f"Label with special characters must be quoted: [{label}]"))
            nodes.update(m.group(1) for m in re.finditer(r"\b([A-Za-z_][\w]*)\s*(?:\[|\(|\{|>)", s)
                         if m.group(1) not in ("subgraph", "end", "style", "classDef", "class", "click", "linkStyle"))
        if len(nodes) > MERMAID_MAX_NODES:
            out.append(Finding(f, start, "warning", "mermaid",
                               f"Diagram has about {len(nodes)} nodes (limit ~{MERMAID_MAX_NODES}); consider splitting"))


NUMBERED_LABEL_RE = re.compile(r"""[\[\(\{>|]\(?["']?\s*\d+\.\s""")
NUMBERED_SECTION_RE = re.compile(r"^\d+\.\s")
SUMMARY_SECTION_RE = re.compile(r"^\d+\.\s+(executive\s+)?summary$", re.I)


def check_readability(doc: Doc, out: list[Finding]) -> None:
    """Rule 35: Read This First page and an 'In short' note per numbered section."""
    if doc.kind != "document" or doc.mode not in ("a", "b", "c"):
        return
    f = str(doc.path)
    if not section_span(doc, r"^read this first$"):
        out.append(Finding(f, 1, "warning", "readability",
                           "Missing 'Read This First' section (Rule 35)"))
    missing = []
    h2 = [(i, ln, t) for i, (ln, lvl, t) in enumerate(doc.headings) if lvl == 2]
    for i, ln, text in h2:
        if not NUMBERED_SECTION_RE.match(text) or SUMMARY_SECTION_RE.match(text):
            continue
        end = next((l for l, lvl, _ in doc.headings[i + 1:] if lvl <= 3), len(doc.lines) + 1)
        intro = "\n".join(doc.lines[ln: end - 1])
        if not re.search(r"\*\*In short:?\*\*", intro, re.I):
            missing.append(text.split()[0].rstrip("."))
    if missing:
        out.append(Finding(f, 1, "warning", "readability",
                           "No 'In short' note under section(s) " + ", ".join(missing) + " (Rule 35)"))


def check_links(doc: Doc, out: list[Finding]) -> None:
    f = str(doc.path)
    slugs = heading_slugs(doc)
    for i, line in enumerate(doc.lines, 1):
        if doc.in_fence(i):
            continue
        for m in LINK_ANCHOR_RE.finditer(line):
            if m.group(1).lower() not in slugs:
                out.append(Finding(f, i, "error", "links", f"Anchor #{m.group(1)} does not match any heading"))


def check_secrets(doc: Doc, out: list[Finding]) -> None:
    f = str(doc.path)
    for i, line in enumerate(doc.lines, 1):
        for pat, msg in SECRET_PATTERNS:
            if pat.search(line):
                out.append(Finding(f, i, "error", "secrets", f"{msg}. Replace it with a placeholder like <DB_PASSWORD>"))
                break


def check_markers(doc: Doc, out: list[Finding]) -> None:
    if doc.kind != "document":
        return
    f = str(doc.path)
    oi = section_span(doc, r"open items")
    rh = section_span(doc, r"revision history")
    excluded = [s for s in (oi, rh) if s]

    def excluded_line(ln: int) -> bool:
        return any(a <= ln <= b for a, b in excluded) or doc.in_fence(ln)

    body: list[tuple[int, str, str]] = []
    for i, line in enumerate(doc.lines, 1):
        if excluded_line(i):
            continue
        for m in MARKER_RE.finditer(line):
            body.append((i, m.group(1), (m.group(2) or "").strip()))
    if not body:
        return
    if not oi:
        return  # missing section already reported by check_structure
    oi_lines = doc.lines[oi[0]: oi[1]]
    oi_rows = [r for r in table_rows(oi_lines) if r and r[0].lower() != "marker"]
    if not oi_rows:
        out.append(Finding(f, oi[0], "error", "markers",
                           f"Document has {len(body)} markers but the Open Items table is empty"))
        return
    oi_text = " ".join(" ".join(oi_lines).lower().split())
    for ln, kind, text in body:
        if not text:
            continue  # bare [TBD] in a table cell; only the empty-table rule applies
        key = " ".join(text.lower().split())[:40]
        if key and key not in oi_text:
            out.append(Finding(f, ln, "warning", "markers",
                               f"[{kind}: {text[:50]}] is not listed in Open Items"))
    types_in_body = {k for _, k, _ in body}
    for kind in sorted(types_in_body):
        if kind.lower() not in oi_text:
            out.append(Finding(f, oi[0], "error", "markers", f"Open Items lists no {kind} items, but the document has some"))


# ---------------------------------------------------------------- cross-document checks

def defined_ids(doc: Doc, prefix_re: str) -> set[str]:
    ids = set()
    pat = re.compile(prefix_re)
    for i, line in enumerate(doc.lines, 1):
        m = ID_DEF_RE.match(line.strip())
        if m and pat.fullmatch(m.group(1)):
            ids.add(m.group(1))
    return ids


def requirement_priorities(req: Doc) -> dict[str, str]:
    prio = {}
    for row in table_rows(req.lines):
        if row and re.fullmatch(r"N?FR-\d+", row[0]):
            for cell in row[1:]:
                c = cell.strip("* ").capitalize()
                if c in ("Must", "Should", "Could", "Won't"):
                    prio[row[0]] = c
                    break
            else:
                prio.setdefault(row[0], "?")
    return prio


def find_source_root(folder: Path, cli_source: str | None) -> Path | None:
    if cli_source:
        return Path(cli_source)
    # Mode A: the profile. Mode C: the modernization brief copies the profile's value.
    for name in ("00-project-profile.md", "00-modernization-brief.md"):
        base = folder / name
        if not base.exists():
            continue
        for row in table_rows(base.read_text(encoding="utf-8", errors="replace").splitlines()[:30]):
            if len(row) > 1 and row[0].strip("* ").lower() == "source location":
                value = row[1].strip("` ")
                if value and not value.startswith("{{") and not value.lower().startswith("http"):
                    return Path(value)
    return None


def check_citations(doc: Doc, source: Path | None, out: list[Finding], cache: dict) -> None:
    if doc.mode not in ("a", "c") or doc.kind == "index":
        return
    f = str(doc.path)
    cites = [(i, m) for i, line in enumerate(doc.lines, 1) for m in CITATION_RE.finditer(line)]
    if not cites:
        return
    if source is None or not source.is_dir():
        out.append(Finding(f, cites[0][0], "warning", "citations",
                           f"{len(cites)} code citations not verified: source project not found "
                           "(pass --source or fill 'Source location' in the profile or modernization brief)"))
        return
    for ln, m in cites:
        rel, start, end = m.group(1), int(m.group(2)), int(m.group(3) or m.group(2))
        target = source / rel.replace("\\", "/")
        if target not in cache:
            try:
                if target.is_file():
                    with target.open(encoding="utf-8", errors="replace") as fh:
                        cache[target] = sum(1 for _ in fh)
                else:
                    cache[target] = None
            except OSError:
                cache[target] = None
        count = cache[target]
        if count is None:
            out.append(Finding(f, ln, "error", "citations", f"Cited file does not exist in the source: {rel}"))
        elif start < 1 or end < start or end > count:
            out.append(Finding(f, ln, "error", "citations",
                               f"Cited lines {start}-{end} are outside {rel} ({count} lines)"))


def words_to_avoid(base: Doc | None) -> list[str]:
    """The 'Avoid' column of the evidence base's Words to Avoid table (Rule 10)."""
    span = section_span(base, r"words to avoid", level=3) if base else None
    if not span:
        return []
    rows = table_rows(base.lines[span[0]: span[1]])
    if not rows or rows[0][0].strip("* ").lower() != "avoid":
        return []
    words = [r[0].strip().strip('"\u201c\u201d`*') for r in rows[1:]]
    return [w for w in words if w and not PLACEHOLDER_RE.search(w)]


def check_wording(doc: Doc, words: list[str], out: list[Finding]) -> None:
    f = str(doc.path)
    history = section_span(doc, r"^revision history$")
    pats = [(w, re.compile(r"(?<!\w)" + re.escape(w) + r"(?!\w)", re.I)) for w in words]
    for i, line in enumerate(doc.lines, 1):
        if history and history[0] <= i <= history[1]:
            continue
        for w, pat in pats:
            if pat.search(line):
                out.append(Finding(f, i, "error", "wording",
                                   f"'{w}' is in the Words to Avoid table; use the replacement"))


def check_project(folder: Path, docs: dict[str, Doc], targets: set[Path], out: list[Finding]) -> None:
    """Cross-document ID and traceability checks for one output/<mode>/<slug>/ folder."""
    mode = folder.parent.name[-1] if folder.parent.name in MODES else "?"
    base = next((docs[n] for n in FEATURE_SOURCES if n in docs), None)
    features = defined_ids(base, r"F-\d+") if base else set()
    req_name = REQUIREMENTS.get(mode, "")
    req = docs.get(req_name)
    prio = requirement_priorities(req) if req else {}
    trace_targets = TRACE_TARGETS.get(mode, {})
    evidence = next((d for n, d in docs.items() if n in EVIDENCE_BASE), None)
    avoid = words_to_avoid(evidence)

    for name, doc in docs.items():
        if doc.path not in targets:
            continue
        f = str(doc.path)
        if avoid and doc is not evidence:
            check_wording(doc, avoid, out)
        if features and doc is not base:
            for i, line in enumerate(doc.lines, 1):
                for ref in set(FEATURE_REF_RE.findall(line)):
                    if ref not in features:
                        out.append(Finding(f, i, "error", "ids", f"{ref} is not defined in {base.path.name}"))
        if prio and doc is not req:
            for i, line in enumerate(doc.lines, 1):
                for ref in set(REQ_REF_RE.findall(line)):
                    if ref not in prio:
                        out.append(Finding(f, i, "error", "ids", f"{ref} is not defined in {req_name}"))

        # Modes B and C: each trace target must cover every Must/Should requirement.
        if prio and name in trace_targets:
            mentioned = set(REQ_REF_RE.findall(doc.text))
            for rid, p in sorted(prio.items()):
                if p in ("Must", "Should") and rid not in mentioned:
                    out.append(Finding(f, 1, "error", "trace", f"{p} requirement {rid} is not covered in {name}"))

    # Modes B and C: the traceability matrix must be filled for every target document that exists.
    if req and req.path in targets and trace_targets:
        span = section_span(req, r"traceability matrix")
        if not span:
            out.append(Finding(str(req.path), 1, "error", "trace", "Missing 'Traceability Matrix' section"))
            return
        rows = table_rows(req.lines[span[0]: span[1]])
        if not rows:
            return
        header = [h.lower() for h in rows[0]]
        for target_name, column in trace_targets.items():
            if target_name not in docs or column.lower() not in header:
                continue
            col = header.index(column.lower())
            for row in rows[1:]:
                rid = next((c for c in row if REQ_REF_RE.fullmatch(c)), None)
                if not rid or prio.get(rid) not in ("Must", "Should"):
                    continue
                cell = row[col] if col < len(row) else ""
                if cell.strip() in ("", "—", "-", "–") or PLACEHOLDER_RE.search(cell):
                    out.append(Finding(str(req.path), span[0], "error", "trace",
                                       f"Traceability Matrix: '{column}' is empty for {rid} although {target_name} exists"))


# ---------------------------------------------------------------- driver

def project_folder(path: Path) -> Path | None:
    """Return the output/<mode>/<slug>/ folder that contains path, if any."""
    p = path.resolve()
    for parent in [p] + list(p.parents):
        if parent.parent.name in MODES and parent.parent.parent.name == "output":
            return parent
    return None


def lint(paths: list[Path], source: str | None = None) -> list[Finding]:
    targets: set[Path] = set()
    for p in paths:
        p = p.resolve()
        if p.is_dir():
            targets.update(x.resolve() for x in p.rglob("*.md") if "export" not in x.parts)
        elif p.suffix.lower() == ".md":
            targets.add(p)
    out: list[Finding] = []
    cache: dict = {}
    by_project: dict[Path | None, None] = {}
    loaded: dict[Path, Doc] = {}

    for path in sorted(targets):
        doc = load_doc(path)
        loaded[path] = doc
        check_structure(doc, out)
        check_placeholders(doc, out)
        check_code_blocks(doc, out)
        check_mermaid(doc, out)
        check_readability(doc, out)
        check_links(doc, out)
        check_secrets(doc, out)
        check_markers(doc, out)
        by_project.setdefault(project_folder(path))

    for folder in by_project:
        if folder is None:
            continue
        docs = {}
        for md in folder.glob("*.md"):
            md = md.resolve()
            docs[md.name] = loaded.get(md) or load_doc(md)
        check_project(folder, docs, targets, out)
        src = find_source_root(folder, source)
        for name, doc in docs.items():
            if doc.path in targets:
                check_citations(doc, src, out, cache)
        repo = folder / "repo"
        if repo.is_dir():
            for md in repo.glob("*.md"):
                if md.resolve() in targets:
                    check_citations(loaded[md.resolve()], src, out, cache)
    return out


def format_report(findings: list[Finding], root: Path) -> str:
    if not findings:
        return "lint_docs: no problems found."
    lines = []
    by_file: dict[str, list[Finding]] = {}
    for fd in findings:
        by_file.setdefault(fd.file, []).append(fd)
    for file, items in sorted(by_file.items()):
        try:
            shown = Path(file).resolve().relative_to(root.resolve())
        except ValueError:
            shown = Path(file)
        lines.append(str(shown).replace("\\", "/"))
        for fd in sorted(items, key=lambda x: (x.severity != "error", x.line)):
            lines.append(f"  {fd.severity.upper():7} L{fd.line:<5} [{fd.check}] {fd.message}")
    errors = sum(fd.severity == "error" for fd in findings)
    warnings = len(findings) - errors
    lines.append(f"\n{errors} error(s), {warnings} warning(s) in {len(by_file)} file(s).")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):  # Windows consoles default to cp1252
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    ap =argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("paths", nargs="+", help="Markdown files or folders (e.g. output/mode-b/my-app)")
    ap.add_argument("--source", help="Modes A and C: path to the documented project, for citation checks")
    ap.add_argument("--json", action="store_true", help="Print findings as JSON")
    ap.add_argument("--strict", action="store_true", help="Fail on warnings too")
    args = ap.parse_args(argv)

    paths = [Path(p) for p in args.paths]
    missing = [p for p in paths if not p.exists()]
    if missing:
        print(f"lint_docs: not found: {', '.join(map(str, missing))}", file=sys.stderr)
        return 2
    findings = lint(paths, args.source)
    if args.json:
        print(json.dumps([asdict(f) for f in findings], indent=2))
    else:
        print(format_report(findings, Path.cwd()))
    errors = any(f.severity == "error" for f in findings)
    return 1 if errors or (args.strict and findings) else 0


if __name__ == "__main__":
    sys.exit(main())
