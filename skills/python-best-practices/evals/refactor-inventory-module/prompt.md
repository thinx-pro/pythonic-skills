---
tags: [python-best-practices]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

`inventory.py` in this folder works but it's a mess. Clean it up so it's idiomatic, robust Python I'd be happy to maintain. Keep the behavior the tests in `test_inventory.py` check — they must still pass (`.venv/bin/python -m pytest -q`; the virtualenv in `.venv` has pytest) — but you can change anything else, including signatures, as long as those tests pass unmodified. Write a short `CHANGES.md` listing what you changed and why.
