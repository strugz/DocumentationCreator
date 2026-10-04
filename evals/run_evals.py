#!/usr/bin/env python3
"""Run, collect, grade, and compare documentation eval cases.

Commands
  list                              List the eval cases.
  prompt <case>                     Print the generation prompt for a case (to run it in a
                                    Claude Code session or subagent yourself).
  run <case|all> [--judge]          Generate with the `claude` CLI (headless), then collect
                                    and grade. Requires the Claude Code CLI on PATH.
  collect <case> [--run RUN_ID]     Move output/mode-x/<slug>/ (generated in-session) into
                                    evals/runs/<RUN_ID>/<case>/output/ and grade it.
  grade <RUN_ID> [case]             Re-grade a stored run (picks up judge.json if present).
  judge-prompt <RUN_ID> <case>      Print the prompt for a fresh judge agent (rubric.md).
  baseline <RUN_ID>                 Save a run's results as the baseline to compare against.
  compare <RUN_ID>                  Compare a run with the baseline: score deltas, regressions.

Typical loop after changing a rule, template, or skill:
  python evals/run_evals.py run all            # or: prompt + collect, in-session
  python evals/run_evals.py compare <RUN_ID>
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

EVALS = Path(__file__).resolve().parent
ROOT = EVALS.parent
CASES = EVALS / "cases"
RUNS = EVALS / "runs"
BASELINE = EVALS / "baseline.json"
sys.path.insert(0, str(EVALS))
import grade as grader  # noqa: E402

ALLOWED_TOOLS = ["Read", "Write", "Edit", "Glob", "Grep", "Task", "Agent", "Skill",
                 "Bash(python *)", "Bash(git *)", "Bash(ls *)", "Bash(mkdir *)"]


# ---------------------------------------------------------------- cases

def all_cases() -> list[str]:
    return sorted(p.name for p in CASES.iterdir() if (p / "case.json").is_file())


def case_dir(case_id: str) -> Path:
    d = CASES / case_id
    if not (d / "case.json").is_file():
        sys.exit(f"Unknown case '{case_id}'. Known: {', '.join(all_cases())}")
    return d


def output_dir_for(case: dict) -> Path:
    return ROOT / "output" / f"mode-{case['mode']}" / case["slug"]


def build_prompt(case_id: str) -> str:
    d = case_dir(case_id)
    case = grader.load_case(d)
    out = f"output/mode-{case['mode']}/{case['slug']}/"
    skill = case["skill"]
    common = (
        f"Product name: {case['product_name']}. Use exactly the slug `{case['slug']}`, so all "
        f"documents go to `{out}`.\n"
        f"This is a NON-INTERACTIVE EVALUATION RUN. {case.get('context', '')} Do not ask the user "
        "anything and do not pause: where the procedure would wait for answers, continue and mark "
        "unknowns with the markers from the rules. Do not run the application or its tests. Write "
        f"only inside `{out}`.\n"
        f"(Skill file: `.claude/skills/{skill}/SKILL.md` — follow it exactly.)"
    )
    if case["mode"] == "a":
        project = (d / case["input"]).relative_to(ROOT).as_posix()
        return f"/{skill} {project} {case.get('suite_args', '')}".rstrip() + "\n\n" + common
    idea = (d / case["input"]).read_text(encoding="utf-8").strip()
    answers = (d / case["answers"]).read_text(encoding="utf-8").strip()
    return (f"/{skill} {idea} {case.get('suite_args', '')}".rstrip() + "\n\n" + common +
            "\n\nThe interview has already happened. Use these answers instead of asking:\n\n" + answers)


def judge_prompt(run_id: str, case_id: str) -> str:
    d = case_dir(case_id)
    case = grader.load_case(d)
    run_case = (RUNS / run_id / case_id).relative_to(ROOT).as_posix()
    evidence = (f"`{(d / 'project').relative_to(ROOT).as_posix()}/`" if case["mode"] == "a"
                else f"`{(d / case['input']).relative_to(ROOT).as_posix()}` and "
                     f"`{(d / case['answers']).relative_to(ROOT).as_posix()}`")
    return (
        "You are an independent reviewer. You did not write these documents.\n"
        f"Read `evals/rubric.md` and follow it exactly. Documents: `{run_case}/output/`. "
        f"Evidence: {evidence}. Rules: `rules/` and `mode-{case['mode']}-*/rules/`.\n"
        f"Write the result to `{run_case}/judge.json` in the rubric's format. Do not edit any "
        "other file."
    )


# ---------------------------------------------------------------- run storage

def new_run_id() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def collect(case_id: str, run_id: str, meta: dict | None = None) -> Path:
    d = case_dir(case_id)
    case = grader.load_case(d)
    src = output_dir_for(case)
    if not src.is_dir():
        sys.exit(f"Nothing to collect: {src} does not exist. Generate it first (see `prompt {case_id}`).")
    dest = RUNS / run_id / case_id
    if (dest / "output").exists():
        shutil.rmtree(dest / "output")
    dest.mkdir(parents=True, exist_ok=True)
    shutil.move(str(src), str(dest / "output"))
    info = {"case": case_id, "run": run_id, "collected": datetime.now().isoformat(timespec="seconds")}
    info.update(meta or {})
    (dest / "meta.json").write_text(json.dumps(info, indent=2), encoding="utf-8")
    return dest


def grade_run(run_id: str, case_id: str) -> grader.CaseResult:
    dest = RUNS / run_id / case_id
    result = grader.grade(case_dir(case_id), dest / "output", dest / "judge.json")
    (dest / "result.json").write_text(json.dumps(asdict(result), indent=2, ensure_ascii=False), encoding="utf-8")
    (dest / "report.md").write_text(grader.to_markdown(result), encoding="utf-8")
    return result


def run_summary(run_id: str) -> dict[str, dict]:
    out = {}
    for f in sorted((RUNS / run_id).glob("*/result.json")):
        out[f.parent.name] = json.loads(f.read_text(encoding="utf-8"))
    return out


# ---------------------------------------------------------------- CLI generation

def claude_cli() -> str | None:
    return shutil.which("claude")


def generate_with_cli(prompt: str, timeout: int) -> dict:
    exe = claude_cli()
    if not exe:
        sys.exit("The `claude` CLI is not on PATH. Install Claude Code CLI, or generate in-session:\n"
                 "  python evals/run_evals.py prompt <case>   (run it in Claude Code)\n"
                 "  python evals/run_evals.py collect <case>")
    cmd = [exe, "-p", prompt, "--output-format", "json", "--permission-mode", "acceptEdits",
           "--allowedTools", *ALLOWED_TOOLS]
    proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", timeout=timeout)
    try:
        data = json.loads(proc.stdout)
    except json.JSONDecodeError:
        data = {"raw_stdout": proc.stdout[-2000:]}
    data["exit_code"] = proc.returncode
    if proc.stderr:
        data["stderr_tail"] = proc.stderr[-2000:]
    keep = ("exit_code", "total_cost_usd", "duration_ms", "num_turns", "is_error", "stderr_tail", "raw_stdout")
    return {k: data[k] for k in keep if k in data}


# ---------------------------------------------------------------- commands

def cmd_run(args) -> int:
    run_id = args.run or new_run_id()
    cases = all_cases() if args.case == "all" else [args.case]
    for cid in cases:
        case = grader.load_case(case_dir(cid))
        stale = output_dir_for(case)
        if stale.exists():
            shutil.rmtree(stale)
        print(f"[{cid}] generating with claude CLI …", flush=True)
        meta = {"generator": "claude-cli", **generate_with_cli(build_prompt(cid), args.timeout)}
        collect(cid, run_id, meta)
        if args.judge:
            print(f"[{cid}] judging …", flush=True)
            generate_with_cli(judge_prompt(run_id, cid), args.timeout)
        r = grade_run(run_id, cid)
        print(f"[{cid}] score {r.score} ({r.passed}/{r.total}), lint errors {r.lint_errors}")
    print(f"\nRun {run_id} stored in {RUNS / run_id}")
    return 0


def cmd_compare(args) -> int:
    if not BASELINE.is_file():
        sys.exit("No baseline yet. Create one with: python evals/run_evals.py baseline <RUN_ID>")
    base = json.loads(BASELINE.read_text(encoding="utf-8"))
    cur = run_summary(args.run_id)
    print(f"Run {args.run_id} vs baseline {base.get('run')}\n")
    print("| Case | Baseline | Now | Δ | Lint errors (base → now) |")
    print("|---|---|---|---|---|")
    regressions = []
    for cid in sorted(set(base["cases"]) | set(cur)):
        b, c = base["cases"].get(cid), cur.get(cid)
        if not b or not c:
            print(f"| {cid} | {b['score'] if b else '—'} | {c['score'] if c else '—'} | — | — |")
            continue
        delta = round(c["score"] - b["score"], 1)
        print(f"| {cid} | {b['score']} | {c['score']} | {delta:+} | {b['lint_errors']} → {c['lint_errors']} |")
        was = {x["id"]: x["passed"] for x in b["checks"]}
        for x in c["checks"]:
            if was.get(x["id"]) and not x["passed"]:
                regressions.append(f"{cid}: `{x['id']}` now fails — {x['detail']}")
            elif was.get(x["id"]) is False and x["passed"]:
                regressions.append(f"{cid}: `{x['id']}` now passes (fixed)")
    if regressions:
        print("\nChanges in individual checks:")
        for r in regressions:
            print(f"- {r}")
    return 1 if any("now fails" in r for r in regressions) else 0


def main(argv=None) -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list")
    p = sub.add_parser("prompt"); p.add_argument("case")
    p = sub.add_parser("run"); p.add_argument("case"); p.add_argument("--run"); p.add_argument("--judge", action="store_true")
    p.add_argument("--timeout", type=int, default=3600)
    p = sub.add_parser("collect"); p.add_argument("case"); p.add_argument("--run")
    p = sub.add_parser("grade"); p.add_argument("run_id"); p.add_argument("case", nargs="?")
    p = sub.add_parser("judge-prompt"); p.add_argument("run_id"); p.add_argument("case")
    p = sub.add_parser("baseline"); p.add_argument("run_id")
    p = sub.add_parser("compare"); p.add_argument("run_id")
    args = ap.parse_args(argv)

    if args.cmd == "list":
        for cid in all_cases():
            print(f"{cid:22} {grader.load_case(case_dir(cid))['title']}")
    elif args.cmd == "prompt":
        print(build_prompt(args.case))
    elif args.cmd == "run":
        return cmd_run(args)
    elif args.cmd == "collect":
        run_id = args.run or new_run_id()
        collect(args.case, run_id, {"generator": "in-session"})
        r = grade_run(run_id, args.case)
        print(grader.to_markdown(r))
        print(f"Stored in {RUNS / run_id / args.case}")
    elif args.cmd == "grade":
        cases = [args.case] if args.case else [p.name for p in (RUNS / args.run_id).iterdir() if p.is_dir()]
        for cid in sorted(cases):
            print(grader.to_markdown(grade_run(args.run_id, cid)))
    elif args.cmd == "judge-prompt":
        print(judge_prompt(args.run_id, args.case))
    elif args.cmd == "baseline":
        summary = run_summary(args.run_id)
        if not summary:
            sys.exit(f"No graded cases in run {args.run_id}")
        BASELINE.write_text(json.dumps({"run": args.run_id, "cases": summary}, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"Baseline set to run {args.run_id} ({', '.join(summary)})")
    elif args.cmd == "compare":
        return cmd_compare(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
