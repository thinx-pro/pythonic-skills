---
type: llm
focus: trace
weight: 1
---

Every file open/read/write uses a context manager or Path.read_text/write_text, and passes an explicit encoding (e.g. encoding="utf-8").
