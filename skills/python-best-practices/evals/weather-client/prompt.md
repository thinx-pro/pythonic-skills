---
tags: [python-best-practices]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Write a small Python module `weather.py` that our long-running service will import. It needs one main function that gets the current temperature for a city from `https://api.weather.example/v1/current?city=<name>`, which returns JSON like `{"city": "Oslo", "temp_c": 4.5, "observed_at": "2026-10-27T08:00:00Z"}`. Use `requests`. The API is sometimes slow or returns 5xx errors, so handle failures sensibly for a service. Include tests (pytest) that don't hit the real network. The API host doesn't exist, so don't try to call it for real. A virtualenv with `requests` and `pytest` is in `.venv` (`.venv/bin/python -m pytest`).
