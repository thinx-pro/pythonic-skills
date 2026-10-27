---
type: llm
focus: trace
weight: 1
---

Tests replace the HTTP layer (monkeypatch, a fake session, responses/requests-mock, or unittest.mock) so no real network call happens, cover at least one failure path (5xx or timeout or bad payload), and the trace shows them passing.
