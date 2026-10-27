---
name: python-best-practices
description: Use whenever you write, modify, refactor or generate Python code (scripts, CLIs, libraries, services, tests). Steers toward modern, typed, robust Python 3.10+ that fails loudly instead of silently, handles files, subprocesses, network calls and time correctly, and passes ruff and pytest before hand-back.
---

# Python best practices

Write Python that a careful senior engineer would approve on first review: boring, typed, explicit about failure, and consistent with the project it lives in.

This file is ordered for scanning while you work. Section 2 is the hand-back checklist; run it every time.

## 1. Mindset

- **Match the project first.** Before writing, look at `pyproject.toml`, the Python version it targets, the formatter and linter it uses, its test layout and its existing style. Follow them even where this skill would choose differently. Only use syntax the project's minimum Python version supports.
- **Application or library?** Applications (CLIs, services, scripts) may print, exit, configure logging and pick concrete dependencies. Libraries never print, never call `sys.exit`, never configure logging, and raise their own documented exceptions.
- **Fail loudly, early, with context.** Most bad agent-written Python is code that hides errors: `except Exception: pass`, `.get(key, default)` on keys that must exist, returning `None` on failure, retry loops without limits. A crash with a clear message is better than a wrong answer.
- **Fix the cause, not the symptom.** Never make a test pass by special-casing its input, parsing an error message or log line to detect a condition, catching an exception you don't understand, or weakening an assertion. If the proper fix is out of scope, say so.
- **Simple beats clever.** A function is fine; you don't need a class. A dict comprehension is fine; you don't need a framework. Don't add a dependency for something the standard library does in five lines.

## 2. Before you hand back

Run what the project has; if it has nothing, use these:

```bash
ruff format .
ruff check .
pyright        # or: mypy .   (only if the project uses one; don't add one uninvited)
pytest -q
```

Then:

- Run the code at least once the way a user would (the CLI with real arguments, the function from a REPL or a test).
- Fix every warning you introduced. Don't add `# noqa` or `# type: ignore` to silence one unless the rule is wrong for that line, and then name the code and give the reason: `# noqa: S603 -- args are a fixed list, no user input`.
- State what you ran and what passed. If you couldn't run something, say so.

## 3. Project layout and dependencies

- One `pyproject.toml` (PEP 621 `[project]` table) holds metadata, dependencies and tool config. Don't add `setup.py`, `setup.cfg` or a new `requirements.txt` to a project that doesn't have them.
- Use the project's tool to add dependencies (`uv add`, `poetry add`, `pip install` + edit `pyproject.toml`). Give libraries version ranges (`httpx>=0.27`); pin exact versions only in lock files or applications that already pin.
- Prefer the standard library: `pathlib`, `json`, `csv`, `argparse`, `logging`, `dataclasses`, `subprocess`, `concurrent.futures`, `sqlite3`, `tomllib` (3.11+), `zoneinfo`.
- Libraries use the `src/` layout. Scripts and CLIs get a `main()` function and an `if __name__ == "__main__":` guard; packaged CLIs get a `[project.scripts]` entry point.
- No work at import time: no network calls, file writes, `logging.basicConfig`, or heavy computation at module level.

## 4. Types and data

- Annotate every public function and method: parameters and return type. Annotate private ones when it helps.
- Use modern syntax for the project's minimum version: `list[int]`, `dict[str, Any]`, `X | None` (3.10+), `type Alias = ...` (3.12+).
- Accept abstract types, return concrete ones: take `Iterable[str]`, `Sequence[T]`, `Mapping[K, V]` (from `collections.abc`); return `list[str]`, `dict[K, V]`.
- Model data with types, not loose dicts and tuples:
  - `@dataclass(frozen=True, slots=True)` for plain records (slots needs 3.10+); a `NamedTuple` when tuple unpacking matters.
  - `TypedDict` for JSON-shaped dicts you don't own.
  - `enum.Enum` (or `StrEnum`, 3.11+) instead of magic strings and int flags.
  - Validate untrusted input once at the boundary (pydantic or attrs if the project uses them, otherwise explicit checks), then pass typed objects inward.
- Avoid `Any`; use `object` when you mean "anything" and narrow it. Use `Protocol` for duck typing instead of an ABC nobody else inherits from.
- `typing.Self` (3.11+) for methods returning their own class; `@typing.override` (3.12+) on overrides if the project uses a type checker.
- Keep imports needed only for annotations under `if TYPE_CHECKING:`.

## 5. Errors and exceptions

- **Raise, don't return error values.** Don't return `None`, `False`, `-1` or `{"error": ...}` to signal failure from a function whose callers then forget to check.
- **Catch narrowly.** Catch the specific exceptions you can handle at that point (`FileNotFoundError`, `json.JSONDecodeError`, `KeyError`). Never write a bare `except:`; never `except Exception: pass`. `except Exception` is acceptable only at a top-level boundary (a CLI's `main`, a request handler, a worker loop) and must log with the traceback (`logger.exception(...)`) or re-raise.
- **Keep the try block small**: wrap only the line that can raise the exception you catch, and put the rest in `else:`.
- **Chain exceptions** when translating: `raise ConfigError(f"bad config in {path}") from err`. Use `from None` only to deliberately hide an irrelevant cause.
- **Messages carry context**: which file, which line, which key, which value. `ValueError(f"line {lineno}: expected 3 fields, got {len(parts)}")`, not `ValueError("invalid input")`.
- **Libraries define one base exception** (`class MyLibError(Exception)`) with specific subclasses, and document what each public function raises.
- **`assert` is not validation.** Asserts are removed under `python -O`. Use them for internal invariants and tests only; validate input with `if ...: raise`.
- **Required data is required.** `config["database_url"]` (KeyError if missing) is correct when the key must exist; `config.get("database_url", "")` turns a clear error into a confusing one later. Use `.get()` only for genuinely optional keys, with a default that is actually valid.
- **Don't swallow and continue in loops** without counting and reporting: if you skip bad records, count them and report the count (and log the first few) so the user knows data was dropped.
- **Retries are bounded**: a maximum attempt count, backoff, and only for errors that are actually transient (timeouts, 429, 5xx). Never retry on 4xx validation errors or programming errors.
- **Exit codes**: a CLI returns 0 on success and non-zero on failure, printing the error to stderr (`sys.exit(f"error: {err}")` or `print(..., file=sys.stderr); return 1`). No traceback for expected user errors (missing file, bad argument); keep the traceback for bugs.

## 6. Files, processes, network, time

- **Context managers for every resource**: `with open(...)`, `with sqlite3.connect(...)`, locks, temp dirs, HTTP sessions/clients.
- **Text files**: always pass `encoding="utf-8"` (or the format's documented encoding) to `open`, `Path.read_text` and `Path.write_text`. The default depends on the OS locale.
- **Paths**: `pathlib.Path`, not string concatenation or `os.path`. `path / "sub" / name`, `path.read_text(encoding="utf-8")`, `path.glob("*.jsonl")`, `path.mkdir(parents=True, exist_ok=True)`. Accept `str | os.PathLike[str]` in public APIs and convert once with `Path(p)`.
- **Atomic writes** for files other processes read: write to a temp file in the same directory, then `os.replace(tmp, target)`.
- **Subprocess**: pass a list of arguments, never `shell=True` with any interpolated value. Use `subprocess.run([...], check=True, capture_output=True, text=True, timeout=...)`. Use `shutil.which` to check for an executable before relying on it.
- **Network calls always have a timeout.** `requests` has none by default and can hang forever: `requests.get(url, timeout=10)`. Reuse a `requests.Session` / `httpx.Client` for many calls. Call `response.raise_for_status()` (or check the status) before using the body.
- **Time**: use timezone-aware datetimes. `datetime.now(UTC)` (`from datetime import UTC`, 3.11+; `timezone.utc` before that). Never `datetime.utcnow()` (deprecated in 3.12, returns a naive datetime). Store and compare in UTC; convert to local time only for display, with `zoneinfo.ZoneInfo`. Measure durations with `time.monotonic()`, not wall-clock time.
- **Logging, not print**, in anything that isn't a CLI's user-facing output: `logger = logging.getLogger(__name__)` at module level; `logger.info("loaded %d rows from %s", n, path)` with %-style args (lazy formatting, groups messages in aggregators), not f-strings. Configure logging once, in the application entry point.
- **JSON**: `json.loads` / `json.dumps(..., ensure_ascii=False)` for human-readable output; never build JSON by string formatting.

## 7. Everyday idioms

- Iterate directly: `for item in items`, `for i, item in enumerate(items)`, `for a, b in zip(xs, ys, strict=True)` (3.10+; catches length mismatches). Never `for i in range(len(items))` just to index.
- Comprehensions for simple transforms and filters; a loop when there are side effects or more than two clauses. Generator expressions when you only iterate once: `sum(x.size for x in files)`, `any(...)`, `all(...)`.
- Counting and grouping: `collections.Counter`, `defaultdict(list)`. Sorting: `sorted(rows, key=lambda r: (-r.count, r.name))` for a deterministic order with ties broken.
- f-strings for formatting (except logging calls, see above). `"".join(parts)` to build strings in loops.
- `is None` / `is not None`, never `== None`. Don't rely on truthiness when `0`, `""` or `[]` are valid values: `if count is not None`, not `if count`.
- **No mutable default arguments**: `def f(items: list[str] | None = None)` then `items = [] if items is None else items`. The same applies to dataclass fields: `field(default_factory=list)`.
- **No boolean positional flags**: `report(rows, include_empty=True)` with a keyword-only parameter (`def report(rows, *, include_empty: bool = False)`), or two functions, or an enum.
- No `global` state for anything but true constants (`UPPER_CASE`). Pass dependencies in (clients, clocks, paths) so code is testable.
- Properties instead of `get_x()` / `set_x()` methods; plain attributes until you need a property.
- `match` (3.10+) for destructuring structured data; `if`/`elif` for simple value checks.
- No `from module import *`. Absolute imports, sorted (ruff's `I` rules do this).
- Name things for what they are: `user_ids` not `data`, `parse_header` not `process`. Don't shadow builtins (`list`, `id`, `type`, `input`, `file`).

## 8. Concurrency and async

- **Threads** for I/O-bound work (`ThreadPoolExecutor`), **processes** for CPU-bound work (`ProcessPoolExecutor`), and only when measured to matter.
- **Never block the event loop** in `async def`: no `requests`, `time.sleep`, blocking file or DB calls. Use async libraries (`httpx.AsyncClient`, `asyncio.sleep`) or `await asyncio.to_thread(blocking_fn, ...)`.
- Structured concurrency: `async with asyncio.TaskGroup() as tg:` (3.11+) instead of loose `create_task` calls. If you must use `create_task`, keep a reference to the task or it can be garbage-collected mid-run.
- Timeouts on awaited I/O: `async with asyncio.timeout(10):` (3.11+) or `asyncio.wait_for`.
- Bound concurrency against external services with `asyncio.Semaphore`.

## 9. Security

- No `eval`, `exec` or `pickle.load` on data you didn't produce. `yaml.safe_load`, never `yaml.load` without a safe loader.
- SQL: parameterized queries (`cur.execute("... WHERE id = ?", (user_id,))`), never f-strings or `%` into SQL.
- `secrets` module (`secrets.token_urlsafe(32)`) for tokens and passwords; `random` is not for security.
- Secrets come from the environment or a secrets manager, never from source code, and never get logged (log `key=...{key[-4:]}` at most).
- Archive extraction: `tarfile.extractall(dest, filter="data")` (3.12+, and backported to recent 3.8–3.11 security releases); check `zipfile` member paths stay inside the destination.
- Password hashing: a dedicated library (argon2-cffi, bcrypt), never a bare `hashlib` digest.

## 10. Tests

- pytest with plain `assert`. One behavior per test; the name says the behavior: `test_skips_malformed_lines_and_counts_them`.
- Use fixtures: `tmp_path` for files, `monkeypatch` for env vars, `capsys` for output. `pytest.mark.parametrize` for input tables. `pytest.raises(ConfigError, match="missing key")` for errors.
- Test behavior through the public interface, not private helpers or call order. Mock only at the boundary (network, clock, filesystem when `tmp_path` can't do it), with `autospec=True`.
- No network or real time in unit tests: inject a client or a clock.
- A bug fix comes with a test that fails without the fix. Check that it does.
- Cover the failure paths you wrote: missing file, bad input, empty input, timeout.

## 11. Documentation and comments

- Docstrings on public modules, classes and functions: one summary line, then args, returns and raised exceptions in the project's style (Google style if none). Type information lives in annotations, not docstrings.
- Comments explain why, not what. Delete commented-out code. `TODO` comments name what's missing.
- Keep the README's usage examples runnable.

## 12. Performance, in order

1. Pick the right algorithm and data structure: `set`/`dict` for membership and lookup, not a list.
2. Avoid repeated work: hoist invariants out of loops, read a file once, batch queries.
3. Stream large inputs (iterate a file line by line, generators) instead of loading everything.
4. Measure before optimizing further (`python -m cProfile -s cumtime`, `timeit`), then optimize the measured hotspot.
5. `functools.cache` on pure functions only, never on methods of long-lived objects (it keeps `self` alive).

## 13. Final checklist

- [ ] Follows the project's version, tools and conventions.
- [ ] Public functions annotated; no new `Any`; data modelled with dataclasses/enums/TypedDicts.
- [ ] No bare or silent `except`; exceptions are specific, chained, and carry context.
- [ ] No `.get()` defaults or `try/except` that hide required data or real bugs.
- [ ] Files opened with an explicit encoding; paths are `pathlib.Path`.
- [ ] Every network call has a timeout; every subprocess uses an argument list, `check=True`, and a timeout.
- [ ] Datetimes are timezone-aware; no `utcnow()`.
- [ ] `logging` instead of `print` outside CLI output; no logging configuration in libraries.
- [ ] No mutable defaults, no boolean positional flags, no `global` state.
- [ ] Output that users or tests compare is deterministic (sorted, ties broken).
- [ ] `ruff format`, `ruff check`, the type checker (if any) and `pytest` pass; you ran the code once.
- [ ] You told the user what you ran, and anything you couldn't verify.
