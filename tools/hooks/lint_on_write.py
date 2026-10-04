#!/usr/bin/env python3
"""Claude Code PostToolUse hook: lint a generated document right after it is written.

Reads the hook JSON from stdin. If the written file is a Markdown file under
output/mode-a/ or output/mode-b/, runs tools/lint_docs.py on it. On errors, prints
the report to stderr and exits 2 so Claude sees it and fixes the document.
Warnings alone do not block. Any other file, or any internal failure, exits 0.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0
    tool_input = payload.get("tool_input") or {}
    tool_response = payload.get("tool_response") or {}
    raw = tool_input.get("file_path") or (tool_response.get("filePath") if isinstance(tool_response, dict) else None)
    if not raw:
        return 0
    path = Path(raw)
    if not path.is_absolute():
        path = ROOT / path
    path = path.resolve()
    if path.suffix.lower() != ".md" or not path.is_file():
        return 0
    try:
        rel = path.relative_to(ROOT / "output")
    except ValueError:
        return 0
    if not rel.parts or rel.parts[0] not in ("mode-a", "mode-b"):
        return 0

    import lint_docs  # noqa: E402  (after sys.path setup)

    try:
        findings = lint_docs.lint([path])
    except Exception as exc:  # never break the session because of the linter
        print(f"lint_docs hook failed: {exc}", file=sys.stderr)
        return 0
    errors = [f for f in findings if f.severity == "error"]
    if not errors:
        return 0
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    print(lint_docs.format_report(errors, ROOT), file=sys.stderr)
    print("Fix these errors in the document (Rule 50). Warnings are not shown; run "
          "`python tools/lint_docs.py <file>` to see them.", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
