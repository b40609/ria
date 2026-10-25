#!/usr/bin/env python3
"""Clone + evidence pin — shallow-clone a repo into the research dir and record
the exact commit + license into research/manifest.json, so every later citation
is reproducible ("evidence pinned to the commit analyzed").

License classes: permissive (MIT/BSD/Apache/ISC/MPL) / copyleft (GPL/AGPL/LGPL)
/ NONE (ideas only, per the skill's red line #3).
"""
import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

LICENSE_PATTERNS = [
    ("MIT", "MIT License"),
    ("Apache-2.0", "Apache License"),
    ("BSD-2-Clause", "Redistributions of source code"),
    ("BSD-3-Clause", "Redistributions in binary form"),
    ("ISC", "ISC License"),
    ("MPL-2.0", "Mozilla Public License"),
    ("LGPL", "Lesser General Public License"),
    ("GPL-3.0", "GNU GENERAL PUBLIC LICENSE"),
    ("GPL-2.0", "GNU General Public License"),
    ("AGPL-3.0", "Affero General Public License"),
]


def sh(args: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(args, cwd=str(cwd) if cwd else None,
                          capture_output=True, text=True)


def _load_manifest(path: Path) -> list[dict]:
    if path.exists():
        try:
            return list(json.loads(path.read_text(encoding="utf-8")))
        except (json.JSONDecodeError, OSError):
            return []
    return []


def detect_license(repo: Path) -> tuple[str, str]:
    for candidate in ["LICENSE", "LICENSE.md", "LICENSE.txt", "COPYING", "LICENCE"]:
        p = repo / candidate
        if p.exists():
            head = p.read_text(encoding="utf-8", errors="ignore")[:800]
            for spdx, marker in LICENSE_PATTERNS:
                if marker.lower() in head.lower():
                    cls = ("copyleft" if spdx.startswith(("GPL", "AGPL", "LGPL"))
                           else "permissive")
                    return spdx, cls
            return "CUSTOM", "review-required"
    return "NONE", "no-license-file"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("url", help="https://github.com/owner/repo (or a local path, for offline/dev use)")
    ap.add_argument("research_dir", type=Path, help="e.g. ./research (created if missing)")
    ap.add_argument("--refresh", action="store_true",
                    help="re-pull every manifest clone and report SHA changes since last pin")
    args = ap.parse_args()

    manifest_path = args.research_dir / "manifest.json"

    if args.refresh:
        entries = _load_manifest(manifest_path)
        for entry in entries:
            clone = Path(entry["clone"])
            if not clone.exists():
                print(f"[gone] {entry['repo']} — clone missing, re-pin it")
                continue
            res = sh(["git", "-C", str(clone), "pull", "--ff-only"])
            if res.returncode != 0:  # diverged history: fetch only, report stale
                sh(["git", "-C", str(clone), "fetch", "--depth=100"])
                print(f"[warn] {entry['repo']}: pull not fast-forward, check manually")
                continue
            new_sha = sh(["git", "-C", str(clone), "rev-parse", "--short", "HEAD"]).stdout.strip()
            if new_sha and new_sha != entry["pinned_sha"]:
                print(f"[moved] {entry['repo']}: {entry['pinned_sha']} -> {new_sha} "
                      f"(evidence older than this pin may be stale)")
                entry["pinned_sha"] = new_sha
                entry["pinned_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
            else:
                print(f"[same]  {entry['repo']} @ {entry['pinned_sha']}")
        manifest_path.write_text(json.dumps(entries, ensure_ascii=False, indent=2),
                                 encoding="utf-8")
        return

    is_local = Path(args.url).exists()
    src = args.url
    if is_local:
        name = Path(args.url).resolve().name
        owner = "local"
    else:
        name = args.url.rstrip("/").rsplit("/", 1)[-1].removesuffix(".git")
        owner = args.url.rstrip("/").rsplit("/", 2)[-2] if len(args.url.rstrip("/").split("/")) >= 2 else "unknown"
    dest = args.research_dir / "clones" / f"{owner}--{name}"

    if dest.exists():
        res = sh(["git", "-C", str(dest), "pull", "--ff-only"])
        if res.returncode != 0:
            print(f"pull failed, keeping existing clone: {res.stderr.strip()}", file=sys.stderr)
    else:
        dest.parent.mkdir(parents=True, exist_ok=True)
        # depth 100 (not 1): slop_check's commit-texture heuristic needs real
        # history — a depth-1 clone makes every repo look like a single commit
        res = sh(["git", "clone", "--depth", "100", args.url, str(dest)])
        if res.returncode != 0:
            print(f"clone failed: {res.stderr.strip()}", file=sys.stderr)
            sys.exit(1)

    sha_res = sh(["git", "-C", str(dest), "rev-parse", "--short", "HEAD"])
    sha = sha_res.stdout.strip() if sha_res.returncode == 0 else "?"

    spdx, cls = detect_license(dest)
    entry = {
        "repo": f"{owner}/{name}", "url": args.url, "clone": str(dest),
        "pinned_sha": sha, "license": spdx, "license_class": cls,
        "pinned_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }

    manifest_path = args.research_dir / "manifest.json"
    manifest = _load_manifest(manifest_path)
    manifest = [m for m in manifest if m.get("repo") != entry["repo"]]
    manifest.append(entry)
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2),
                             encoding="utf-8")

    print(f"cloned {owner}/{name} @ {sha} — license: {spdx} ({cls})")
    print(f"manifest updated: {manifest_path}")
    if cls == "no-license-file":
        print("RED LINE: no license — ideas only, never code.")
    elif cls == "copyleft":
        print("WARNING: copyleft — forking/deriving contaminates your release. Borrow ideas.")


if __name__ == "__main__":
    main()
