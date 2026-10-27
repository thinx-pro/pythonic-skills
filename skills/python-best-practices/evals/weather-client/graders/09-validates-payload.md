---
type: llm
focus: trace
weight: 1
---

Missing or wrongly typed fields in the JSON (e.g. no temp_c) produce the module's clear exception rather than a raw KeyError/TypeError deep inside the code.
