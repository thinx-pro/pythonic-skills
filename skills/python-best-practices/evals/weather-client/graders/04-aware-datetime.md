---
type: llm
focus: trace
weight: 1
---

observed_at is parsed into a timezone-aware datetime (the trailing Z handled), not left as a string or parsed naive.
