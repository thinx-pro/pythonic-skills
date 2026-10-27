---
type: llm
focus: trace
weight: 1
---

The bare `except:` that returned None is gone. Load failures either propagate or are caught as specific exceptions (e.g. FileNotFoundError, json.JSONDecodeError) and re-raised or reported with context; nothing is silently swallowed.
