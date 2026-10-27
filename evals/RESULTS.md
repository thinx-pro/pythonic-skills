# Eval results

Raw per-grader results behind the numbers in the README. Each case ran **2 times with the skill and 2 times without** (`claude plugin eval`'s no-plugin baseline arm). Each grader is an LLM judgement (the default judge model, 3 votes, majority). Model under test and Claude Code version are listed per case.

## python-best-practices / logsum-cli

Claude Code 2.1.311, 2 runs per arm.

| Grader | with skill | without |
|---|---|---|
| 01-missing-dir-clean-error | 2/2 | 2/2 |
| 02-unreadable-file-handled | 2/2 | 0/2 |
| 03-skipped-counted | 2/2 | 2/2 |
| 04-no-broad-swallow | 2/2 | 2/2 |
| 05-pathlib | 2/2 | 2/2 |
| 06-explicit-encoding | 2/2 | 0/2 |
| 07-sorted-deterministic | 2/2 | 2/2 |
| 08-structure | 2/2 | 2/2 |
| 09-annotations | 2/2 | 0/2 |
| 10-tests-cover-failure | 2/2 | 2/2 |

Mean agent cost per run (list-price estimate from the eval runner): with $0.48, without $0.32.

## python-best-practices / refactor-inventory-module

Claude Code 2.1.311, 2 runs per arm.

| Grader | with skill | without |
|---|---|---|
| 01-tests-still-pass | 2/2 | 2/2 |
| 02-no-eval | 2/2 | 2/2 |
| 03-no-silent-except | 2/2 | 2/2 |
| 04-no-mutable-defaults | 2/2 | 2/2 |
| 05-files-with-encoding | 1/2 | 1/2 |
| 06-pathlib | 2/2 | 2/2 |
| 07-no-debug-print | 2/2 | 2/2 |
| 08-aware-datetime | 2/2 | 2/2 |
| 09-is-none | 2/2 | 2/2 |
| 10-no-bool-positional | 2/2 | 1/2 |
| 11-deterministic-report | 2/2 | 2/2 |
| 12-formatting | 2/2 | 2/2 |
| 13-missing-price | 2/2 | 0/2 |
| 14-annotations | 2/2 | 2/2 |
| 15-changes-file | 2/2 | 2/2 |

Mean agent cost per run (list-price estimate from the eval runner): with $0.62, without $0.44.

## python-best-practices / weather-client

Claude Code 2.1.311, 2 runs per arm.

| Grader | with skill | without |
|---|---|---|
| 01-timeout | 2/2 | 2/2 |
| 02-status-checked | 2/2 | 2/2 |
| 03-own-exception-chained | 2/2 | 1/2 |
| 04-aware-datetime | 2/2 | 2/2 |
| 05-typed-result | 2/2 | 2/2 |
| 06-reusable-client | 2/2 | 2/2 |
| 07-no-print | 2/2 | 2/2 |
| 08-bounded-retry | 2/2 | 2/2 |
| 09-validates-payload | 2/2 | 2/2 |
| 10-tests-mock-boundary | 2/2 | 2/2 |

Mean agent cost per run (list-price estimate from the eval runner): with $0.54, without $0.41.

## python-review / review-inventory-module

Claude Code 2.1.311, 2 runs per arm.

| Grader | with skill | without |
|---|---|---|
| 01-eval-is-top-priority | 2/2 | 2/2 |
| 02-bare-except | 2/2 | 2/2 |
| 03-mutable-defaults | 2/2 | 2/2 |
| 04-file-handling | 2/2 | 2/2 |
| 05-utcnow | 2/2 | 2/2 |
| 06-nondeterministic-report | 2/2 | 2/2 |
| 07-silent-zero-value | 2/2 | 2/2 |
| 08-locations | 2/2 | 2/2 |
| 09-code-fixes | 2/2 | 2/2 |
| 10-prioritized | 2/2 | 2/2 |
| 11-code-unchanged | 2/2 | 2/2 |

Mean agent cost per run (list-price estimate from the eval runner): with $0.38, without $0.20.

## Totals

| Skill | with skill | without |
|---|---|---|
| python-best-practices | 69/70 | 59/70 |
| python-review | 22/22 | 22/22 |

## Notes on method

- The skills were written before the eval cases, and were not edited after seeing any result.
- In the first run, the sandbox had a bare `python3` without pytest or requests, so the "tests pass" graders of `refactor-inventory-module` and `weather-client` could not pass in either arm. Those two cases' scaffold scripts now create a `.venv` with pytest (and requests), and the numbers above are from the re-run. Skill text was unchanged between runs.
- Two runs per arm is a small sample; treat differences of one or two graders as noise.
- The same author wrote the skills and the graders. The graders check concrete, observable things (a timeout argument, an encoding argument, a test run in the trace) to limit judgement calls, but they are not an independent benchmark.
