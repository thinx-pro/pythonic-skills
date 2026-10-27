# pythonic-skills

**Two Agent Skills and a ruff config that make coding agents write and review Python like a careful senior engineer:** typed, failing loudly instead of silently, and safe with files, subprocesses, network calls and time.

![skills 2](https://img.shields.io/badge/skills-2-3f8f5a) ![ruff rules proven 36/36](https://img.shields.io/badge/ruff%20rules%20proven-36%2F36-3f8f5a) ![evals 69/70 vs 59/70](https://img.shields.io/badge/evals-69%2F70%20vs%2059%2F70%20without-3f8f5a) ![license MIT](https://img.shields.io/badge/license-MIT-blue)

- **`python-best-practices`** loads whenever an agent writes or changes Python and steers it toward modern (3.10+), typed, robust code that passes ruff and pytest before hand-back.
- **`python-review`** reviews a file, package or diff and writes a prioritized report where every finding has a location, a concrete failure, the rule it breaks and a code fix.
- **`lints/ruff.toml`** enforces the machine-checkable rules in CI. Every rule in the table below is proven to fire, and a clean reference module is proven to stay clean.

## What it changes

Measured with `claude plugin eval` on three writing tasks (a CLI, an HTTP client library for a service, refactoring a messy module) and one review task, each run twice with the skill and twice without:

| | with the skill | without |
|---|---|---|
| `python-best-practices`, 3 tasks | **69 / 70** checks | 59 / 70 |
| `python-review`, 1 task | 22 / 22 | 22 / 22 |

Without the skill, the agent (Claude Opus 5.5 in Claude Code 2.1.311) wrote working code, but in **both** runs of the CLI task it failed the checks for explicit file encodings, type annotations and handling of unreadable files. In the refactor it kept treating a missing price as `0` in both runs and left a boolean positional flag in one. With the skill, all of those checks passed in every run. The review skill made no measurable difference on its one task: the model already reviews that messy module well on its own.

It costs about 40% more per writing task by the eval runner's cost estimate (the agent reads the skill and checks more). Per-grader results and method notes: [evals/RESULTS.md](evals/RESULTS.md).

## Install

### Claude Code

```
/plugin marketplace add thinx-pro/pythonic-skills
/plugin install pythonic-skills@pythonic-skills
```

Or from a terminal: `claude plugin marketplace add thinx-pro/pythonic-skills`, then `claude plugin install pythonic-skills@pythonic-skills`. Claude loads them when you write or review Python; you can also call them as `/pythonic-skills:python-best-practices` and `/pythonic-skills:python-review`.

### Other agents (Codex, Cursor, Gemini CLI, Copilot…)

Each skill is a standard `SKILL.md` folder under `skills/`. Copy both folders into your agent's skills directory, for example:

```bash
git clone https://github.com/thinx-pro/pythonic-skills
mkdir -p ~/.agents/skills
cp -R pythonic-skills/skills/python-* ~/.agents/skills/
```

The `evals/` folders inside each skill are only for testing; you can leave them out. Only Claude Code was tested.

## What the writing skill covers

`skills/python-best-practices/SKILL.md`, ordered so an agent can scan it while coding:

1. **Mindset:** match the project first; application vs library; fail loudly; fix causes, not symptoms (no special-casing test inputs, no parsing error strings)
2. **Hand-back checklist:** `ruff format`, `ruff check`, the type checker, `pytest`, run it once, say what you ran
3. Project layout and dependencies (`pyproject.toml`, `src/` layout, no import-time work)
4. Types and data (modern syntax, `collections.abc` parameters, dataclasses, enums, `TypedDict`, `Protocol`)
5. **Errors:** raise instead of returning error values, narrow catches, chaining, context in messages, `assert` is not validation, required keys are required, bounded retries, exit codes
6. **Files, processes, network, time:** explicit encodings, `pathlib`, atomic writes, subprocess argument lists with `check=True` and timeouts, a timeout on every network call, timezone-aware datetimes, logging instead of print
7. Everyday idioms (no mutable defaults, no boolean positional flags, deterministic output)
8. Concurrency and async (don't block the loop, `TaskGroup`, timeouts, semaphores)
9. Security (`eval`, `pickle`, `yaml.load`, SQL parameters, `secrets`, archive extraction)
10. Tests, documentation, performance, and a final checklist

The review skill runs the project's own linters, type checker and tests (read-only), then reads the code for correctness, silent failure, fragile workarounds, security, resources, API design, tests and maintainability, in that order. It never edits code unless asked.

## The ruff config

Copy [`lints/ruff.toml`](lints/ruff.toml) next to your `pyproject.toml` (or merge its tables into `[tool.ruff]`), set `target-version` to your minimum Python, and run `ruff check .`. It targets ruff 0.17; rule selection is in the file with a comment per family.

Each rule below has one deliberate violation in [`lints/check/violations.py`](lints/check/violations.py), and [`scripts/check_lints.py`](scripts/check_lints.py) fails if any of them stops firing, if [`lints/check/clean.py`](lints/check/clean.py) gets any finding, or if this table lists a code with no violation:

```bash
pip install ruff
python3 scripts/check_lints.py      # ruff 0.17.3: 36/36 expected rules fired; clean.py findings: 0
```

| Code | Catches | Skill section |
|---|---|---|
| `B006` | mutable default argument | §7 |
| `B904` | `raise` inside `except` without `from` | §5 |
| `B905` | `zip()` without `strict=` | §7 |
| `E722` | bare `except:` | §5 |
| `BLE001` | `except Exception` | §5 |
| `S110` | `except Exception: pass` | §5 |
| `S113` | `requests` call without a timeout | §6 |
| `S602` | `subprocess` with `shell=True` | §6 |
| `PLW1510` | `subprocess.run` without `check=` | §6 |
| `S307` | `eval()` | §9 |
| `S301` | `pickle` on data | §9 |
| `S506` | `yaml.load` without a safe loader | §9 |
| `S608` | SQL built from strings | §9 |
| `S202` | `tarfile.extractall` without a filter | §9 |
| `DTZ005` | `datetime.now()` without a timezone | §6 |
| `DTZ003` | `datetime.utcnow()` | §6 |
| `PTH118` | `os.path.join` | §6 |
| `PTH110` | `os.path.exists` | §6 |
| `G004` | f-string in a logging call | §6 |
| `T201` | `print` (allow it per file in CLIs) | §6 |
| `TRY400` | `logging.error` in `except` instead of `logging.exception` | §5 |
| `FBT001` | boolean positional parameter | §7 |
| `PLW0603` | `global` statement | §7 |
| `E711` | `== None` | §7 |
| `A001` | variable shadowing a builtin | §7 |
| `RUF012` | mutable class attribute default | §7 |
| `UP006` | `List[int]` instead of `list[int]` | §4 |
| `UP045` | `Optional[X]` instead of `X \| None` | §4 |
| `UP035` | deprecated `typing` imports | §4 |
| `ANN001` | parameter without a type annotation | §4 |
| `ANN201` | public function without a return type | §4 |
| `PGH003` | blanket `# type: ignore` | §2 |
| `ERA001` | commented-out code | §11 |
| `ASYNC210` | blocking HTTP call in `async def` | §8 |
| `ASYNC251` | `time.sleep` in `async def` | §8 |
| `RUF006` | `asyncio.create_task` result dropped | §8 |

`open()` without `encoding=` (`PLW1514`) is still a preview rule in ruff 0.17, so it isn't enabled by default; the config explains how to turn it on.

## Testing the skills

The eval cases live in `skills/*/evals/` in the layout `claude plugin eval` reads: a prompt, a description of a good result, and one grader per file under `graders/`. Run them from a skill's folder; each case also runs without the skill for comparison:

```bash
cd skills/python-best-practices
claude plugin eval . --allow-tools Write Edit Bash --scaffold --runs 2 --no-publish
```

These are real model runs and are billed. `--scaffold` runs the cases' own setup scripts, which copy input files and create a `.venv` with pytest (and requests) from PyPI.

```bash
python -m pytest -q tests     # the lint check passes, and fails when a rule or the clean module breaks
```

## Limitations

- Two runs per arm on four tasks is a small sample, and the same author wrote the skills and the graders. The numbers show direction, not a benchmark.
- The skill targets Python 3.10+ and assumes the project's own tools win. It has no framework-specific guidance (Django, FastAPI, pandas) beyond general rules.
- The ruff config is opinionated (`FBT`, `ANN`, `T20`). Drop the families you disagree with; the check script will tell you which table rows to delete.

## Sources

The guidance is a synthesis written for this project. It draws on [PEP 8](https://peps.python.org/pep-0008/), [PEP 20](https://peps.python.org/pep-0020/), [PEP 484](https://peps.python.org/pep-0484/) and [PEP 604](https://peps.python.org/pep-0604/), the [Python standard library docs](https://docs.python.org/3/library/) (including the `datetime.utcnow()` deprecation and `tarfile` extraction filters), the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html), and the [ruff rule reference](https://docs.astral.sh/ruff/rules/). No text is copied from them.

## License

MIT. See [LICENSE](LICENSE).
