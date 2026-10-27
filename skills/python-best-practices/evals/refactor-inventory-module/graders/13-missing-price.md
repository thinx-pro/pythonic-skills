---
type: llm
focus: trace
weight: 1
---

value() no longer silently returns 0 for an unknown item: it raises a clear error (e.g. KeyError with the item name) or documents and handles the missing price explicitly rather than multiplying by a default 0.
