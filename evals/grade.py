#!/usr/bin/env python3
"""Grade one generated documentation set against an eval case.

Usage:
    python evals/grade.py <case-dir> <output-dir> [--json] [--judge judge.json]

The case's case.json lists deterministic checks. Each check passes or fails; the case
score is the weighted pass rate (0-100). An optional judge.json (LLM rubric scores,
see evals/rubric.md) is reported next to it but never mixed into the deterministic score.

Check types
  files         every listed file exists in the output folder
  lint          tools/lint_docs.py reports at most `max_errors` errors
  contains      `pattern` matches somewhere in `file`
  contains_all  every regex in `patterns` matches in `file`
  absent        `pattern` matches nowhere in `file`
  line          one single line matches every regex in `all`
  qualified     every line matching `pattern` also matches `allowed_if` (within ±1 line)
  min_count     `pattern` matches at least `min` times (multiline: ^ = line start)

`file` is a file name, a list of names, or "*" (every .md file in the output folder).
Patterns are case-insensitive unless the check sets "case_sensitive": true.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import lint_docs  # noqa: E402


@dataclass
class CheckResult:
    id: str
    type: str
    passed: bool
    weight: float
    desc: str
    detail: str = ""


@dataclass
class CaseResult:
    case: str
    output_dir: str
    score: float
    passed: int
    total: int
    lint_errors: int
    lint_warnings: int
    checks: list[CheckResult] = field(default_factory=list)
    judge: dict | None = None


# ---------------------------------------------------------------- helpers

def _flags(check: dict) -> int:
    return re.M | (0 if check.get("case_sensitive") else re.I)


def _files(output: Path, spec) -> tuple[list[Path], list[str]]:
    """Resolve a file spec to existing paths plus the names that are missing."""
    if spec == "*":
        return sorted(p for p in output.rglob("*.md") if "export" not in p.parts), []
    names = [spec] if isinstance(spec, str) else list(spec)
    found, missing = [], []
    for name in names:
        p = output / name
        (found if p.is_file() else missing).append(p if p.is_file() else name)
    return found, missing


def _read(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace")


def _rel(p: Path, output: Path) -> str:
    try:
        return str(p.relative_to(output)).replace("\\", "/")
    except ValueError:
        return str(p)


def _short(s: str, n: int = 90) -> str:
    s = " ".join(s.split())
    return s if len(s) <= n else s[: n - 1] + "…"


# ---------------------------------------------------------------- check types

def check_files(check, output, _lint):
    _, missing = _files(output, check["files"])
    return not missing, ("missing: " + ", ".join(map(str, missing))) if missing else ""


def check_lint(check, output, lint):
    errors = [f for f in lint if f.severity == "error"]
    ok = len(errors) <= check.get("max_errors", 0)
    detail = ""
    if errors:
        top = errors[:5]
        detail = f"{len(errors)} lint error(s); first: " + "; ".join(
            f"{Path(f.file).name}:L{f.line} [{f.check}] {_short(f.message, 60)}" for f in top)
    return ok, detail


def check_contains(check, output, _lint):
    files, missing = _files(output, check["file"])
    if missing:
        return False, "missing file: " + ", ".join(map(str, missing))
    pat = re.compile(check["pattern"], _flags(check))
    ok = any(pat.search(_read(p)) for p in files)
    return ok, "" if ok else f"pattern not found: {check['pattern']}"


def check_contains_all(check, output, _lint):
    files, missing = _files(output, check["file"])
    if missing:
        return False, "missing file: " + ", ".join(map(str, missing))
    text = "\n".join(_read(p) for p in files)
    absent = [p for p in check["patterns"] if not re.search(p, text, _flags(check))]
    return not absent, ("not found: " + ", ".join(absent)) if absent else ""


def check_absent(check, output, _lint):
    files, missing = _files(output, check["file"])
    if missing and not files:
        return False, "missing file: " + ", ".join(map(str, missing))
    pat = re.compile(check["pattern"], _flags(check))
    hits = []
    for p in files:
        for i, line in enumerate(_read(p).splitlines(), 1):
            if pat.search(line):
                hits.append(f"{_rel(p, output)}:L{i}: {_short(line)}")
    return not hits, "; ".join(hits[:3]) + (f" (+{len(hits) - 3} more)" if len(hits) > 3 else "")


def check_line(check, output, _lint):
    files, missing = _files(output, check["file"])
    if missing and not files:
        return False, "missing file: " + ", ".join(map(str, missing))
    pats = [re.compile(p, _flags(check)) for p in check["all"]]
    for p in files:
        for line in _read(p).splitlines():
            if all(x.search(line) for x in pats):
                return True, ""
    return False, "no single line matches all of: " + " + ".join(check["all"])


def check_qualified(check, output, _lint):
    files, missing = _files(output, check["file"])
    if missing and not files:
        return False, "missing file: " + ", ".join(map(str, missing))
    pat = re.compile(check["pattern"], _flags(check))
    ok_pat = re.compile(check["allowed_if"], _flags(check))
    bad = []
    for p in files:
        lines = _read(p).splitlines()
        for i, line in enumerate(lines):
            if not pat.search(line):
                continue
            window = " ".join(lines[max(0, i - 1): i + 2])
            if not ok_pat.search(window):
                bad.append(f"{_rel(p, output)}:L{i + 1}: {_short(line)}")
    return not bad, "; ".join(bad[:3]) + (f" (+{len(bad) - 3} more)" if len(bad) > 3 else "")


def check_min_count(check, output, _lint):
    files, missing = _files(output, check["file"])
    if missing:
        return False, "missing file: " + ", ".join(map(str, missing))
    n = sum(len(re.findall(check["pattern"], _read(p), _flags(check))) for p in files)
    return n >= check["min"], f"found {n}, need ≥ {check['min']}"


CHECKS = {
    "files": check_files,
    "lint": check_lint,
    "contains": check_contains,
    "contains_all": check_contains_all,
    "absent": check_absent,
    "line": check_line,
    "qualified": check_qualified,
    "min_count": check_min_count,
}


# ---------------------------------------------------------------- driver

def load_case(case_dir: Path) -> dict:
    return json.loads((case_dir / "case.json").read_text(encoding="utf-8"))


def grade(case_dir: Path, output: Path, judge_path: Path | None = None) -> CaseResult:
    case = load_case(case_dir)
    source = str(case_dir / "project") if case.get("mode") == "a" else None
    lint = lint_docs.lint([output], source) if output.is_dir() else []
    results = []
    for check in case["checks"]:
        fn = CHECKS.get(check["type"])
        if fn is None:
            raise ValueError(f"{case['id']}: unknown check type {check['type']!r}")
        if not output.is_dir():
            ok, detail = False, "output folder does not exist"
        else:
            ok, detail = fn(check, output, lint)
        results.append(CheckResult(
            id=check["id"], type=check["type"], passed=bool(ok),
            weight=float(check.get("weight", 1)),
            desc=check.get("desc", check["id"]), detail="" if ok else detail))
    total_w = sum(r.weight for r in results) or 1
    score = round(100 * sum(r.weight for r in results if r.passed) / total_w, 1)
    judge = None
    if judge_path and judge_path.is_file():
        judge = json.loads(judge_path.read_text(encoding="utf-8"))
    return CaseResult(
        case=case["id"], output_dir=str(output), score=score,
        passed=sum(r.passed for r in results), total=len(results),
        lint_errors=sum(f.severity == "error" for f in lint),
        lint_warnings=sum(f.severity == "warning" for f in lint),
        checks=results, judge=judge)


def judge_summary(judge: dict) -> list[str]:
    lines = []
    docs = judge.get("documents", [])
    if docs:
        crit = sorted({k for d in docs for k in d.get("scores", {})})
        lines.append("| Document | " + " | ".join(crit) + " | Avg |")
        lines.append("|---|" + "---|" * (len(crit) + 1))
        for d in docs:
            s = d.get("scores", {})
            vals = [s.get(c) for c in crit]
            nums = [v for v in vals if isinstance(v, (int, float))]
            avg = f"{sum(nums) / len(nums):.1f}" if nums else "—"
            lines.append(f"| {d.get('file', '?')} | " + " | ".join(str(v) if v is not None else "—" for v in vals) + f" | {avg} |")
    for issue in judge.get("issues", [])[:10]:
        lines.append(f"- {issue}")
    return lines


def to_markdown(r: CaseResult) -> str:
    out = [f"## {r.case} — score {r.score} ({r.passed}/{r.total} checks)",
           "", f"Lint: {r.lint_errors} error(s), {r.lint_warnings} warning(s)", "",
           "| Result | Check | Weight | Detail |", "|---|---|---|---|"]
    for c in sorted(r.checks, key=lambda c: (c.passed, -c.weight)):
        mark = "✅" if c.passed else "❌"
        out.append(f"| {mark} | {c.desc} (`{c.id}`) | {c.weight:g} | {c.detail.replace('|', '¦')} |")
    if r.judge:
        out += ["", "### LLM judge (rubric scores, not part of the score above)", ""] + judge_summary(r.judge)
    return "\n".join(out) + "\n"


def main(argv=None) -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description="Grade a documentation output folder against an eval case")
    ap.add_argument("case_dir", type=Path)
    ap.add_argument("output_dir", type=Path)
    ap.add_argument("--judge", type=Path, help="judge.json with rubric scores")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    r = grade(args.case_dir, args.output_dir, args.judge)
    print(json.dumps(asdict(r), indent=2, ensure_ascii=False) if args.json else to_markdown(r))
    return 0


if __name__ == "__main__":
    sys.exit(main())
