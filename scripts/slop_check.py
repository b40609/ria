#!/usr/bin/env python3
"""Emerging-project quality screen — the executable half of survey-protocol Step 3b.

The vibes era produces shells: a brilliant README over hollow code. This tool
scores a cloned repo on four checks and issues the protocol's verdict:
  0 fails -> PASS (worth a deep read)
  1 fail  -> DEMOTE (reference notes only)
  2+ fails-> DROP  (record why, move on)

Stdlib only. Heuristics are deliberately transparent — read them before
trusting them.
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

CODE_EXT = {".py", ".js", ".ts", ".tsx", ".jsx", ".mjs", ".go", ".rs", ".java",
            ".rb", ".php", ".c", ".cpp", ".h", ".swift", ".kt", ".sh", ".vue", ".svelte"}
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist",
             "build", "target", ".next", "site-packages"}
SLOP_RE = re.compile(r"\b(TODO|FIXME|placeholder|dummy data|mock response)\b", re.I)

MIN_CODE_FILES = 3       # deliberate-minimalism (a 4-file single-container app) is
                         # legitimate; the target is the 2-file-plus-brochure shell
MIN_CODE_KB = 10         # and at least ~10KB of code
README_HEAVY_RATIO = 4.0  # README KB per code KB above this = shell suspicion
MIN_COMMITS = 2          # single init commit = no iteration history


def walk_code(root: Path) -> list[Path]:
    out, stack = [], [root]
    while stack:
        d = stack.pop()
        try:
            entries = list(d.iterdir())
        except OSError:
            continue
        for e in entries:
            if e.is_dir():
                if e.name not in SKIP_DIRS:
                    stack.append(e)
            elif e.suffix.lower() in CODE_EXT:
                out.append(e)
    return out


def count_commits(root: Path) -> int | None:
    res = subprocess.run(["git", "-C", str(root), "rev-list", "--count", "HEAD"],
                         capture_output=True, text=True)
    return int(res.stdout.strip()) if res.returncode == 0 else None


def analyze(repo: Path) -> dict:
    code = walk_code(repo)
    code_kb = sum(min(f.stat().st_size, 2_000_000) for f in code if f.exists()) / 1024

    readme = next((p for p in repo.glob("README*") if p.is_file()), None)
    readme_kb = (readme.stat().st_size / 1024) if readme and readme.exists() else 0.0

    has_tests = any(
        p.match("test_*") or p.match("*_test.*") or p.match("*.spec.*")
        or p.parent.name in ("tests", "test", "__tests__")
        for p in repo.rglob("*") if p.is_file()
    ) if any(True for _ in repo.rglob("*")) else False

    slop_hits = 0
    for f in code[:500]:
        try:
            slop_hits += len(SLOP_RE.findall(
                f.read_text(encoding="utf-8", errors="ignore")[:100_000]))
        except OSError:
            continue

    commits = count_commits(repo)

    checks = []

    def add(name, ok, reason):
        checks.append({"check": name, "pass": bool(ok), "reason": reason})

    # 1. README <-> code consistency (substance)
    substance_ok = len(code) >= MIN_CODE_FILES and code_kb >= MIN_CODE_KB
    shell_suspect = readme_kb > 0 and (readme_kb / max(code_kb, 0.001)) > README_HEAVY_RATIO
    add("readme_code_consistency",
        substance_ok and not shell_suspect,
        f"{len(code)} code files, {code_kb:.0f}KB code, {readme_kb:.0f}KB README"
        + (" — README-heavy shell" if shell_suspect else ""))

    # 2. Tests
    add("tests_present", has_tests, "any test/spec files found" if has_tests else "zero tests")

    # 3. Commit texture (shallow-clone aware: a depth-N clone reporting N
    #    commits means history was clipped, not that the repo has none)
    shallow = (repo / ".git" / "shallow").exists()
    if commits is None:
        add("commit_texture", True, "no git history available (imported source) — skipped")
    elif shallow and commits >= 90:
        add("commit_texture", True, f"history clipped at ~{commits}+ commits (shallow clone)")
    else:
        add("commit_texture", commits >= MIN_COMMITS,
            f"{commits} commit(s)" + (" — single init commit, no iteration" if commits < MIN_COMMITS else ""))

    # 4. Slop density
    per_kb = slop_hits / max(code_kb, 0.001)
    add("slop_density", per_kb <= 1.0,
        f"{slop_hits} TODO/mock markers ({per_kb:.1f}/KB)")

    fails = sum(1 for c in checks if not c["pass"])
    verdict = "PASS" if fails == 0 else ("DEMOTE" if fails == 1 else "DROP")
    return {"repo": str(repo), "verdict": verdict, "fails": fails, "checks": checks}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("repo", type=Path, help="path to a cloned repository")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    args = ap.parse_args()
    result = analyze(args.repo)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return
    print(f"verdict: {result['verdict']}  ({result['fails']} check(s) failed) — {result['repo']}")
    for c in result["checks"]:
        mark = "PASS" if c["pass"] else "FAIL"
        print(f"  [{mark}] {c['check']}: {c['reason']}")
    print("  protocol action: " + {
        "PASS": "deep-read candidate",
        "DEMOTE": "reference notes only",
        "DROP": "drop, record the reason in shortlist.md",
    }[result["verdict"]])


if __name__ == "__main__":
    main()
