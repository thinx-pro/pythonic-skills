---
type: llm
focus: trace
weight: 1
---

An unreadable or undecodable file is handled with a specific exception (OSError / UnicodeDecodeError), reported with the file's name, and does not crash the whole run or get silently ignored.
