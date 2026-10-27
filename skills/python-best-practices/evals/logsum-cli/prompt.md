---
tags: [python-best-practices]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Write me a Python CLI, `logsum.py`. It takes a directory path as its only argument, reads every `*.jsonl` file in it (one JSON object per line, each with at least a `level` string field and a `ts` timestamp string), and prints how many events there are per level plus the total, sorted by count descending. Skip lines that aren't valid JSON or lack a `level`, but tell me how many were skipped at the end. Standard library only. It's an internal tool so keep it practical, but it must not crash with a traceback on bad input (missing directory, unreadable file, garbage lines). Add a couple of tests.
