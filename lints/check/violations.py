"""One deliberate violation per rule in the README table.

Each offending line ends with `# expect: CODE`. scripts/check_lints.py runs ruff with
lints/ruff.toml on this file and fails if any expected code does not fire on its line.
This file is never imported or executed.
"""

import asyncio
import datetime
import logging
import os
import pickle
import subprocess
import tarfile
import time
from typing import List, Optional  # expect: UP035

import requests
import yaml

logger = logging.getLogger(__name__)
_CACHE = {}


def add_tag(tag: str, tags: list[str] = []) -> list[str]:  # expect: B006
    tags.append(tag)
    return tags


def load_settings(path: str) -> dict[str, str]:
    try:
        with open(path, encoding="utf-8") as fh:
            return dict(line.split("=", 1) for line in fh)
    except FileNotFoundError:
        raise ValueError("missing settings")  # expect: B904


def pair_up(xs: list[int], ys: list[int]) -> list[tuple[int, int]]:
    return list(zip(xs, ys))  # expect: B905


def parse_count(text: str) -> int:
    try:
        return int(text)
    except:  # expect: E722
        return 0


def fetch_status(url: str) -> int:
    try:
        return requests.get(url).status_code  # expect: S113
    except Exception:  # expect: BLE001
        return -1


def cleanup(path: str) -> None:
    try:
        os.remove(path)
    except Exception:  # expect: S110
        pass


def run_user_command(cmd: str) -> None:
    subprocess.Popen(cmd, shell=True)  # expect: S602


def calc(expr: str) -> int:
    return eval(expr)  # expect: S307


def load_blob(data: bytes) -> object:
    return pickle.loads(data)  # expect: S301


def read_yaml(text: str) -> object:
    return yaml.load(text)  # expect: S506


def find_user(cur: object, name: str) -> None:
    cur.execute(f"SELECT * FROM users WHERE name = '{name}'")  # expect: S608


def stamp() -> datetime.datetime:
    return datetime.datetime.now()  # expect: DTZ005


def legacy_stamp() -> datetime.datetime:
    return datetime.datetime.utcnow()  # expect: DTZ003


def config_path(base: str) -> str:
    return os.path.join(base, "config.toml")  # expect: PTH118


def has_config(base: str) -> bool:
    return os.path.exists(base)  # expect: PTH110


def log_rows(n: int) -> None:
    logger.info(f"loaded {n} rows")  # expect: G004


def show(n: int) -> None:
    print(n)  # expect: T201


def report(rows: list[str], verbose: bool) -> str:  # expect: FBT001
    return "\n".join(rows) if verbose else str(len(rows))


def remember(key: str, value: str) -> None:
    global _CACHE  # expect: PLW0603
    _CACHE = {key: value}


def is_missing(value: object) -> bool:
    return value == None  # expect: E711


def first(items: List[int]) -> int:  # expect: UP006
    return items[0]


def maybe(value: Optional[int]) -> int:  # expect: UP045
    return value or 0


def risky() -> int:
    return int("3")  # type: ignore  # expect: PGH003


def safe_parse(text: str) -> int:
    try:
        return int(text)
    except ValueError:
        logger.error("bad number %s", text)  # expect: TRY400
        raise


def no_return_type(x: int):  # expect: ANN201
    return x


def untyped(x) -> int:  # expect: ANN001
    return int(x)


def shadow(items: list[int]) -> int:
    sum = 0  # expect: A001
    for item in items:
        sum += item
    return sum


def compute(a: int) -> int:
    # result = a * 2 + 1  # expect: ERA001
    return a


def git_head() -> str:
    return subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True).stdout  # expect: PLW1510


async def fetch_async(url: str) -> int:
    return requests.get(url, timeout=5).status_code  # expect: ASYNC210


async def wait_a_bit() -> None:
    time.sleep(1)  # expect: ASYNC251


async def fire_and_forget() -> None:
    asyncio.create_task(wait_a_bit())  # expect: RUF006


class Registry:
    handlers: list[str] = []  # expect: RUF012


def unpack(archive: str, dest: str) -> None:
    with tarfile.open(archive) as tf:
        tf.extractall(dest)  # expect: S202
