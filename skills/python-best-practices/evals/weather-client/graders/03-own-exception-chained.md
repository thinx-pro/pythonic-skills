---
type: llm
focus: trace
weight: 1
---

Failures are raised as a module-specific exception (e.g. WeatherError) and chained from the underlying exception with `raise ... from err`.
