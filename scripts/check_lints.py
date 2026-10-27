#!/usr/bin/env python3
"""Prove every rule in lints/ruff.toml's table fires, and that clean code stays clean.

Usage (from the repo root, with ruff on PATH or passed via RUFF=/path/to/ruff):

    python3 scripts/check_lints.py

Fails (exit 1) if:
  - an `# expect: CODE` line in lints/check/violations.py does not get that code,
  - lints/check/clean.py gets any finding,
  - a code in the README's rule table has no `# expect:` line (the table drifted).
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "lints" / "ruff.toml"
VIOLATIONS = ROOT / "lints" / "check" / "violations.py"
CLEAN = ROOT / "lints" / "check" / "clean.py"
README = ROOT / "README.md"
EXPECT = re.compile(r"#\s*expect:\s*([A-Z]+[0-9]+)")
TABLE_CODE = re.compile(r"^\|\s*`([A-Z]+[0-9]+)`\s*\|", re.MULTILINE)


def ruff_json(ruff: str, path: Path) -> list[dict[str, object]]:
    result = subprocess.run(
        [ruff, "check", "--config", str(CONFIG), "--output-format", "json", "--no-cache", str(path)],
        capture_output=True,
        text=True,
        check=False,
        timeout=120,
    )
    if result.returncode not in (0, 1):
        sys.exit(f"ruff failed on {path.name}:\n{result.stderr}")
    return json.loads(result.stdout or "[]")


def main() -> int:
    ruff = os.environ.get("RUFF") or shutil.which("ruff")
    if not ruff:
        sys.exit("ruff not found: install it (pip install ruff) or set RUFF=/path/to/ruff")
    version = subprocess.run([ruff, "--version"], capture_output=True, text=True, check=True).stdout.strip()

    expected: dict[int, str] = {}
    for lineno, line in enumerate(VIOLATIONS.read_text(encoding="utf-8").splitlines(), start=1):
        if (m := EXPECT.search(line)) is not None:
            expected[lineno] = m.group(1)

    fired: dict[int, set[str]] = {}
    for f in ruff_json(ruff, VIOLATIONS):
        fired.setdefault(f["location"]["row"], set()).add(f["code"])

    problems = [
        f"violations.py:{lineno}: expected {code}, got {sorted(fired.get(lineno, set())) or 'nothing'}"
        for lineno, code in sorted(expected.items())
        if code not in fired.get(lineno, set())
    ]

    clean = ruff_json(ruff, CLEAN)
    problems += [
        f"clean.py:{f['location']['row']}: unexpected {f['code']} ({f['message']})" for f in clean
    ]

    if README.exists():
        table = set(TABLE_CODE.findall(README.read_text(encoding="utf-8")))
        missing = sorted(table - set(expected.values()))
        problems += [f"README table lists {code} but violations.py has no `# expect: {code}`" for code in missing]

    print(f"{version}: {len(expected) - sum(1 for p in problems if p.startswith('violations'))}"
          f"/{len(expected)} expected rules fired; clean.py findings: {len(clean)}")
    for p in problems:
        print("FAIL", p)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
