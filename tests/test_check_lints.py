"""The lint check must pass on the repo, and must fail when a rule stops firing.

Run with ruff on PATH (or RUFF=/path/to/ruff): python -m pytest -q tests
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
RUFF = os.environ.get("RUFF") or shutil.which("ruff")
pytestmark = pytest.mark.skipif(RUFF is None, reason="ruff not installed")


def run_check(root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(root / "scripts" / "check_lints.py")],
        capture_output=True,
        text=True,
        check=False,
        timeout=120,
        env={**os.environ, "RUFF": str(RUFF)},
    )


@pytest.fixture
def repo_copy(tmp_path: Path) -> Path:
    for part in ("lints", "scripts"):
        shutil.copytree(ROOT / part, tmp_path / part)
    shutil.copy2(ROOT / "README.md", tmp_path / "README.md")
    return tmp_path


def test_repo_passes() -> None:
    result = run_check(ROOT)
    assert result.returncode == 0, result.stdout + result.stderr


def test_fails_when_a_rule_is_switched_off(repo_copy: Path) -> None:
    config = repo_copy / "lints" / "ruff.toml"
    text = config.read_text(encoding="utf-8")
    config.write_text(text.replace('ignore = [\n', 'ignore = [\n  "S113",\n', 1), encoding="utf-8")
    result = run_check(repo_copy)
    assert result.returncode == 1
    assert "expected S113" in result.stdout


def test_fails_when_clean_code_gets_flagged(repo_copy: Path) -> None:
    clean = repo_copy / "lints" / "check" / "clean.py"
    clean.write_text(clean.read_text(encoding="utf-8") + "\n\ndef shout(x):\n    print(x)\n", encoding="utf-8")
    result = run_check(repo_copy)
    assert result.returncode == 1
    assert "clean.py" in result.stdout
