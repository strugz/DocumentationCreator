#!/usr/bin/env python3
"""Split the Mode C Tech Stack Questionnaire into one copy per audience.

Usage:
    python tools/split_questionnaire.py output/mode-c/<slug>

Reads <folder>/07-tech-stack-questionnaire.md and writes two Markdown copies to
<folder>/export/questionnaire/ (inside export/, so the linter skips them):
    07-tech-stack-questionnaire-stakeholders.md   Part A
    07-tech-stack-questionnaire-developers.md     Parts B and C
Each copy keeps Read This First, How to Answer, the current system, its own parts and
Respondent Details; drops the Response Summary; renumbers sections and their references;
rebuilds the Table of Contents; and keeps only the Open Items that its body mentions.
Then export them to Word:
    node tools/md_to_docx.js <folder>/export/questionnaire/<file>.md <folder>/export
Standard library only.
"""
from __future__ import annotations

import re
import sys
import unicodedata
from pathlib import Path

SOURCE = "07-tech-stack-questionnaire.md"
AUDIENCES = {
    "stakeholders": {
        "title": "for Stakeholders",
        "document": "Tech Stack Questionnaire — Stakeholders (Part A)",
        "parts": ("Part A",),
        "label": "Part A",
        "other": "Parts B and C",
        "intro": "- This copy is for stakeholders: Management, the people who use the system "
                 "every day, and IT staff. It holds Part A only.",
    },
    "developers": {
        "title": "for Developers",
        "document": "Tech Stack Questionnaire — Developers (Parts B and C)",
        "parts": ("Part B", "Part C"),
        "label": "Parts B and C",
        "other": "Part A",
        "intro": "- This copy is for developers and technical staff, including the testers "
                 "of integrations. It holds Parts B and C.",
    },
}
ALWAYS = ("Read This First", "How to Answer", "Current System", "Respondent Details",
          "Open Items", "Revision History")
H2 = re.compile(r"^## (?:(\d+)\. )?(.*)$")
H3_NUM = re.compile(r"^### (\d+)\.(\d+) ")
REF = re.compile(r"(?<![Bb]rief )\b(sections?) (\d+)(\.\d+)?(?: and (\d+)(\.\d+)?)?")
TIME = re.compile(r"(\d+\s*minutes)\s+for\s+(Part A|Parts B and C)")
MARKER = re.compile(r"\[(?:TBD|ASSUMPTION|VERIFY|DECISION)[^\]]*\]")


def slug(text: str) -> str:
    text = unicodedata.normalize("NFKC", re.sub(r"`|\*\*", "", text)).lower()
    return "".join(c for c in text if c.isalnum() or c in " -_").replace(" ", "-")


def split_sections(lines: list[str]) -> tuple[list[str], list[tuple[str | None, str, list[str]]]]:
    head, sections, cur = [], [], None
    for line in lines:
        m = H2.match(line)
        if m:
            cur = (m.group(1), m.group(2), [])
            sections.append(cur)
        elif cur is None:
            head.append(line)
        else:
            cur[2].append(line)
    return head, sections


def remap_refs(text: str, nmap: dict[str, str]) -> str:
    def one(num: str, sub: str | None) -> str | None:
        return nmap[num] + (sub or "") if num in nmap else None

    def repl(m: re.Match) -> str:
        nums = [one(m.group(2), m.group(3))]
        if m.group(4):
            nums.append(one(m.group(4), m.group(5)))
        kept = [n for n in nums if n]
        if not kept:
            return "\0"
        word = "sections" if len(kept) > 1 else "section"
        return f"{word} {' and '.join(kept)}"

    text = REF.sub(repl, text)
    text = re.sub(r"\s*\(\0\)", "", text)  # a parenthesis that only named dropped sections
    return text.replace("\0", "a later section")


def build(src: Path, audience: str) -> str:
    cfg = AUDIENCES[audience]
    head, sections = split_sections(src.read_text(encoding="utf-8").splitlines())
    fields = {l.split("|")[1].strip(): l.split("|")[2].strip() for l in head if l.count("|") >= 3}
    date, version = fields.get("Date", ""), fields.get("Version", "").split(" ")[0]

    keep = [s for s in sections
            if s[1] != "Table of Contents"
            and (any(k in s[1] for k in ALWAYS) or any(p in s[1] for p in cfg["parts"]))]
    nmap, n = {}, 0
    for num, _, _ in keep:
        if num:
            n += 1
            nmap[num] = str(n)

    out = []
    for line in head:
        if line.startswith("# "):
            line = f"{line} {cfg['title']}"
        elif line.startswith("| Document |"):
            line = f"| Document | {cfg['document']} |"
        out.append(line)

    body: list[tuple[str, list[str]]] = []
    for num, title, lines in keep:
        heading = f"## {nmap[num]}. {title}" if num else f"## {title}"
        new_lines, skip_bullet = [], False
        for line in lines:
            if title == "Revision History":
                new_lines.append(line)
                continue
            m = H3_NUM.match(line)
            if m and m.group(1) in nmap:
                line = f"### {nmap[m.group(1)]}.{m.group(2)} " + line[m.end():]
            if "How to Answer" in title:
                if line.startswith("- Answer only the parts"):
                    new_lines.append(cfg["intro"])
                    skip_bullet = True
                    continue
                if skip_bullet and line.startswith("  "):
                    continue
                skip_bullet = False
            if title == "Read This First" and line.startswith("|") and cfg["other"] in line \
                    and cfg["label"] not in line:
                continue
            if title == "Respondent Details" and line.startswith("| Parts answered"):
                continue
            if title == "Read This First" and line.startswith("|"):
                times = dict((who, mins) for mins, who in TIME.findall(line))
                own = [times[p] for p in times if p == cfg["label"]]
                if len(times) > 1 and own:
                    cells = line.split("|")
                    cells[2] = f" About {own[0]} "
                    line = "|".join(cells)
            new_lines.append(remap_refs(line, nmap))
        if title == "Revision History":
            while new_lines and not new_lines[-1].strip():
                new_lines.pop()
            new_lines += [f"| — | {date} | Generated with Claude | Copy for {audience}, made from "
                          f"`{src.name}` version {version}. Section numbers in the rows above refer "
                          "to the full questionnaire. |", ""]
        body.append((heading, new_lines))

    text_so_far = "\n".join(l for h, ls in body if "Open Items" not in h for l in ls)
    used = set(MARKER.findall(text_so_far))
    for i, (heading, lines) in enumerate(body):
        if "Open Items" in heading:
            rows = [l for l in lines if not l.startswith("| ")
                    or l.startswith("| Marker") or any(mk in l for mk in used)]
            if not any(mk in "\n".join(rows) for mk in used):
                rows = [l for l in rows if not l.startswith("|")] + ["Not applicable — no open items in this copy."]
            body[i] = (heading, rows)

    toc = ["## Table of Contents"] + [f"- [{h[3:]}](#{slug(h[3:])})" for h, _ in body] + [""]
    first = next(i for i, l in enumerate(out) if l.strip() == "" and i > 2 and out[i - 1].startswith("|"))
    out = out[: first + 1] + toc
    for heading, lines in body:
        out.append(heading)
        out.extend(lines)
    return "\n".join(out).rstrip() + "\n"


def main(argv: list[str]) -> int:
    if len(argv) != 1:
        print(__doc__.split("Usage:")[1].split("Reads")[0].strip(), file=sys.stderr)
        return 2
    folder = Path(argv[0])
    src = folder / SOURCE
    if not src.is_file():
        print(f"split_questionnaire: {src} not found", file=sys.stderr)
        return 2
    out_dir = folder / "export" / "questionnaire"
    out_dir.mkdir(parents=True, exist_ok=True)
    for audience in AUDIENCES:
        target = out_dir / f"{src.stem}-{audience}.md"
        target.write_text(build(src, audience), encoding="utf-8")
        print("wrote", target)
    return 0


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    sys.exit(main(sys.argv[1:]))
