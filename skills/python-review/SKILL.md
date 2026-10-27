---
name: python-review
description: Review existing Python code — a file, a package, a diff or a pull request — and write a prioritized report where every finding cites a location, the rule it breaks and the smallest fix. Use when the user asks to review, audit, critique or "look over" Python code, asks "what would you change here?", or wants a second opinion before merging. Does not edit the code unless asked.
---

# Python review

Review like a senior engineer whose time is expensive: find what will actually hurt (wrong results, silent failures, crashes, security holes, things that will rot), say exactly where and how to fix it, and don't drown it in style nits.

The rules you review against are in the `python-best-practices` skill. Load it if it is installed; cite its section numbers (for example "§5 Errors") alongside lint codes.

## Scope

- Review what the user pointed at: a file, a directory, `git diff`, or a PR's changed files. For a diff, also read the callers and callees of changed functions that are in the repository; bugs often sit where changed code is used, not in the changed lines.
- Do not modify any file unless the user asks you to apply fixes. The report is the deliverable.

## Steps

1. **Understand intent.** Read the README, the module docstrings and the tests for the code under review. Write one sentence on what the code is supposed to do. If you can't tell, that is a finding.
2. **Run the tools the project has** (only read-only commands): `ruff check <paths>` (or the project's linter), `ruff format --check <paths>`, the type checker if configured (`pyright` / `mypy`), and `pytest -q` for the relevant tests. If a tool isn't installed, say so and continue without it; don't install tools globally. Treat tool output as input to your judgement, not as the review itself: report the findings that matter, grouped, and summarise the rest as a count.
3. **Read the code** with these questions, in this order:
   1. **Correctness**: does it do what it claims for normal, empty, huge and malformed input? Off-by-one, wrong comparison, mutating shared state, mutable default arguments, timezone-naive datetimes, float money, non-deterministic ordering in output.
   2. **Silent failure**: bare or broad `except` that swallows errors, `.get()` defaults on required data, returning `None` on failure, skipped records that aren't counted, retries without limits, unchecked HTTP status codes or subprocess return codes.
   3. **Fragile workarounds**: logic that special-cases test inputs, parses error messages or log lines to detect conditions, sleeps to wait for something, or catches an exception to make a symptom disappear.
   4. **Security**: `eval`/`exec`/`pickle` on untrusted data, `shell=True` with interpolated values, SQL built with string formatting, `yaml.load`, secrets in code or logs, unsafe archive extraction, `random` for tokens.
   5. **Resources**: files, connections and sessions not closed (no `with`); network calls without timeouts; blocking calls inside `async def`; tasks created and dropped.
   6. **API and types**: missing or wrong annotations on public functions, `Any` leaks, boolean positional flags, dicts and tuples where a dataclass or enum belongs, getters and setters instead of properties, a library that prints, exits or configures logging.
   7. **Tests**: are the failure paths tested? Would the tests fail if the bug they cover came back? Do they hit the network or real time?
   8. **Maintainability**: only what will genuinely cost time later: dead code, duplicated logic, misleading names, functions doing several unrelated things.

## Report format

Write the report in your reply (or to `REVIEW.md` if the user asked for a file):

```markdown
# Python review: <what was reviewed>

**What it does:** <one sentence>
**Verdict:** <ship / ship after must-fix / needs rework> — <one line why>
**Tools:** ruff <n findings>, pyright <n>, pytest <passed/failed/not run> (<why not>)

## Must fix
1. **<short title>** — `path/to/file.py:42`
   <what goes wrong, concretely: the input, the wrong result or crash>
   Rule: <python-best-practices § / ruff code / reference>
   Fix:
   ```python
   <the smallest change that fixes it>
   ```

## Should fix
...

## Consider
...

## What's good
- <specific things the code does well, with locations>
```

Rules for findings:

- **Must fix**: wrong results, crashes on plausible input, silent data loss, security issues, resource leaks in long-running code.
- **Should fix**: things that will cause bugs or confusion soon (missing timeouts in scripts, naive datetimes, untested failure paths, fragile workarounds).
- **Consider**: everything else worth saying. Keep this short; group lint-level nits into one line with a count.
- Every finding has a `file:line` location, a concrete failure scenario (not "could be problematic"), the rule, and a code fix. If you are not sure something is a bug, say what you'd check and put it under Consider.
- Don't report the same pattern ten times: report it once and list the other locations.
- End with what the code already does well. Be specific; skip it rather than invent praise.
