#!/usr/bin/env python3
"""Dual-track competitor discovery — the executable half of the survey protocol.

Track A (baseline): high-star maintained incumbents.
Track B (emerging):  recently-created, actively-pushed, mid-band stars —
                    the vibe-coding cluster that star-sorted search misses.

Requires the `gh` CLI (authenticated). Outputs a merged markdown shortlist.
"""
import argparse
import json
import subprocess
import sys
from datetime import date, timedelta

FIELDS = "fullName,stargazersCount,createdAt,pushedAt,description,license"


def gh_search(args: list[str]) -> list[dict]:
    res = subprocess.run(["gh", "search", "repos", *args, "--json", FIELDS],
                         capture_output=True, text=True)
    if res.returncode != 0:
        print(f"gh search failed: {res.stderr.strip()}", file=sys.stderr)
        return []
    try:
        return json.loads(res.stdout)
    except json.JSONDecodeError:
        return []


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("query", help="keyword query, e.g. 'self-hosted second brain'")
    ap.add_argument("--days", type=int, default=90, help="emerging track: created within N days")
    ap.add_argument("--stars", default="5..500", help="emerging track star band (gh syntax)")
    ap.add_argument("--limit", type=int, default=10, help="per-track limit")
    args = ap.parse_args()

    cutoff = (date.today() - timedelta(days=args.days)).isoformat()

    baseline = gh_search([args.query, "--sort", "stars", "--limit", str(args.limit)])
    emerging = gh_search([args.query, "--sort", "updated",
                          "--created", f">{cutoff}", "--stars", args.stars,
                          "--limit", str(args.limit)])

    seen: dict[str, dict] = {}
    for repo in baseline:
        repo["_track"] = "baseline"
        seen[repo["fullName"]] = repo
    for repo in emerging:
        if repo["fullName"] in seen:
            seen[repo["fullName"]]["_track"] += "+emerging"
        else:
            repo["_track"] = "emerging"
            seen[repo["fullName"]] = repo

    print("| Track | Stars | Created | Last push | License | Repo | Description |")
    print("|---|---|---|---|---|---|---|")
    for repo in sorted(seen.values(), key=lambda r: -r["stargazersCount"]):
        lic = (repo.get("license") or {}).get("spdx_id", "?")
        desc = (repo.get("description") or "").replace("|", "/")[:60]
        print(f"| {repo['_track']} | {repo['stargazersCount']}★ | "
              f"{str(repo.get('createdAt', ''))[:10]} | {str(repo.get('pushedAt', ''))[:10]} | "
              f"{lic} | [{repo['fullName']}](https://github.com/{repo['fullName']}) | {desc} |")

    if not seen:
        print("(no results — try different phrasings, see survey-protocol.md)",
              file=sys.stderr)


if __name__ == "__main__":
    main()
