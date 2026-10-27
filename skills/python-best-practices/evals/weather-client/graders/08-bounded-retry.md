---
type: llm
focus: trace
weight: 1
---

If the code retries, retries are bounded (max attempts) with backoff and only for transient errors (timeouts, connection errors, 5xx/429), not for 4xx or parsing errors. If it doesn't retry at all, this grader passes only if the code clearly surfaces transient failures to the caller.
