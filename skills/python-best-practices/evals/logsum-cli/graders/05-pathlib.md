---
type: llm
focus: trace
weight: 1
---

Paths are handled with pathlib.Path (e.g. Path(arg).glob('*.jsonl')), not os.path string manipulation.
