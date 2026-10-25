import shutil
import subprocess
import tempfile
import uuid
from pathlib import Path

from scripts.slop_check import analyze

_TMP = Path(__file__).parent / ".tmp"


def _tmpdir(prefix: str) -> Path:
    _TMP.mkdir(exist_ok=True)
    return Path(tempfile.mkdtemp(dir=str(_TMP), prefix=f"{prefix}-{uuid.uuid4().hex[:6]}-"))


def _git(path: Path, message: str) -> None:
    subprocess.run(["git", "-C", str(path), "add", "-A"], capture_output=True)
    subprocess.run(["git", "-C", str(path), "commit", "-m", message,
                    "--allow-empty"], capture_output=True)


def make_repo(path: Path, *, files: dict[str, str], commits: list[str]) -> Path:
    subprocess.run(["git", "init", "-q", str(path)], capture_output=True)
    for msg in commits:
        for name, content in files.items():
            (path / name).parent.mkdir(parents=True, exist_ok=True)
            (path / name).write_text(content, encoding="utf-8")
        _git(path, msg)
    return path


def test_real_project_passes():
    d = _tmpdir("real")
    try:
        unit = "def f():\n    return " + " + ".join(str(j) for j in range(30)) + "\n" * 5
        files = {f"src/mod{i}.py": unit * 40 for i in range(6)}   # ~5KB each
        files["tests/test_mod.py"] = "def test_f():\n    assert True\n"
        files["README.md"] = "# Real project\n" + "x" * 2000
        make_repo(d / "repo", files=files, commits=["init", "add mods", "fix"])
        result = analyze(d / "repo")
        assert result["verdict"] == "PASS", result
        assert all(c["pass"] for c in result["checks"])
    finally:
        shutil.rmtree(d, ignore_errors=True)


def test_shell_project_drops():
    d = _tmpdir("shell")
    try:
        files = {
            "README.md": "# Amazing AI product\n" + ("brilliant marketing copy. " * 300),
            "app.py": "# TODO implement\ndata = 'placeholder'\n",
            "utils.py": "# TODO\n",
        }
        make_repo(d / "repo", files=files, commits=["Initial commit"])
        result = analyze(d / "repo")
        assert result["verdict"] == "DROP", result
        failed = {c["check"] for c in result["checks"] if not c["pass"]}
        assert {"readme_code_consistency", "commit_texture"} <= failed
        assert "tests_present" in failed
    finally:
        shutil.rmtree(d, ignore_errors=True)


def test_mid_project_demotes_with_single_fail():
    d = _tmpdir("mid")
    try:
        unit = "def g():\n    return 42\n"
        files = {f"src/m{i}.py": unit * 200 for i in range(6)}    # ~3KB each
        files["README.md"] = "# Mid\nno tests yet\n"
        make_repo(d / "repo", files=files, commits=["init", "iterate"])
        result = analyze(d / "repo")
        assert result["verdict"] == "DEMOTE", result      # only tests missing
        failed = [c["check"] for c in result["checks"] if not c["pass"]]
        assert failed == ["tests_present"]
    finally:
        shutil.rmtree(d, ignore_errors=True)


def test_discover_and_pin_syntax():
    # siblings must at least compile & expose CLIs
    for script in ("discover.py", "pin.py", "slop_check.py"):
        res = subprocess.run(
            ["python", "-m", "py_compile", str(Path(__file__).parent.parent / "scripts" / script)],
            capture_output=True)
        assert res.returncode == 0, script
