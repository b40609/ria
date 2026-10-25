"""Offline test for pin.py --refresh using local-path clones (no network)."""
import json
import shutil
import subprocess
import tempfile
import uuid
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from pin import main as pin_main  # noqa: E402

_TMP = Path(__file__).parent / ".tmp"


def _tmpdir(prefix: str) -> Path:
    _TMP.mkdir(exist_ok=True)
    return Path(tempfile.mkdtemp(dir=str(_TMP), prefix=f"{prefix}-{uuid.uuid4().hex[:6]}-"))


def _commit(repo: Path, msg: str) -> None:
    subprocess.run(["git", "-C", str(repo), "add", "-A"], capture_output=True)
    subprocess.run(["git", "-C", str(repo), "commit", "-m", msg, "--allow-empty"],
                   capture_output=True)


def test_pin_refresh_reports_moved_sha():
    d = _tmpdir("refresh")
    try:
        src = d / "src-repo"
        subprocess.run(["git", "init", "-q", str(src)], capture_output=True)
        (src / "LICENSE").write_text("MIT License\n", encoding="utf-8")
        (src / "code.py").write_text("print('v1')\n", encoding="utf-8")
        _commit(src, "v1")

        research = d / "research"
        sys.argv = ["pin.py", str(src), str(research)]
        pin_main()
        manifest = json.loads((research / "manifest.json").read_text(encoding="utf-8"))
        assert manifest[0]["repo"] == "local/src-repo"
        assert manifest[0]["license"] == "MIT"
        v1_sha = manifest[0]["pinned_sha"]

        # upstream moves; --refresh must detect and record it
        (src / "code.py").write_text("print('v2')\n", encoding="utf-8")
        _commit(src, "v2")
        sys.argv = ["pin.py", str(src), str(research), "--refresh"]
        pin_main()   # prints [moved]/[same]; we assert via manifest
        manifest = json.loads((research / "manifest.json").read_text(encoding="utf-8"))
        assert manifest[0]["pinned_sha"] != v1_sha
    finally:
        shutil.rmtree(d, ignore_errors=True)
