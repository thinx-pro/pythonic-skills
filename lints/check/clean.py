"""The same jobs as violations.py, written the way the skill asks. Must produce no findings.

scripts/check_lints.py fails if ruff reports anything here, so the config can't drift
into flagging idiomatic code.
"""

from __future__ import annotations

import asyncio
import datetime
import logging
import shutil
import sqlite3
import subprocess
import tarfile
from dataclasses import dataclass, field
from pathlib import Path

import requests
import yaml

logger = logging.getLogger(__name__)


class SettingsError(Exception):
    """Raised when a settings file is missing or malformed."""


def add_tag(tag: str, tags: list[str] | None = None) -> list[str]:
    tags = [] if tags is None else tags
    tags.append(tag)
    return tags


def load_settings(path: Path) -> dict[str, str]:
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError as err:
        msg = f"settings file not found: {path}"
        raise SettingsError(msg) from err
    return dict(line.split("=", 1) for line in text.splitlines() if "=" in line)


def pair_up(xs: list[int], ys: list[int]) -> list[tuple[int, int]]:
    return list(zip(xs, ys, strict=True))


def fetch_status(session: requests.Session, url: str) -> int:
    response = session.get(url, timeout=10)
    response.raise_for_status()
    return response.status_code


def run_tool(args: list[str]) -> str:
    if shutil.which(args[0]) is None:
        msg = f"{args[0]} is not installed"
        raise FileNotFoundError(msg)
    result = subprocess.run(args, check=True, capture_output=True, text=True, timeout=60)
    return result.stdout


def read_yaml(text: str) -> object:
    return yaml.safe_load(text)


def find_user(conn: sqlite3.Connection, name: str) -> list[tuple[object, ...]]:
    return conn.execute("SELECT id, name FROM users WHERE name = ?", (name,)).fetchall()


def stamp() -> datetime.datetime:
    return datetime.datetime.now(datetime.UTC)


def config_path(base: Path) -> Path:
    return base / "config.toml"


def log_rows(n: int) -> None:
    logger.info("loaded %d rows", n)


def report(rows: list[str], *, verbose: bool = False) -> str:
    return "\n".join(rows) if verbose else str(len(rows))


def is_missing(value: object) -> bool:
    return value is None


def safe_parse(text: str) -> int:
    try:
        return int(text)
    except ValueError:
        logger.exception("bad number %s", text)
        raise


def total(items: list[int]) -> int:
    return sum(items)


async def fetch_async(client_get: object, url: str) -> None:
    async with asyncio.timeout(10):
        await asyncio.sleep(0)
    logger.debug("would fetch %s with %r", url, client_get)


async def run_all() -> None:
    async with asyncio.TaskGroup() as tg:
        tg.create_task(asyncio.sleep(0))


@dataclass(slots=True)
class Registry:
    handlers: list[str] = field(default_factory=list)


def unpack(archive: Path, dest: Path) -> None:
    with tarfile.open(archive) as tf:
        tf.extractall(dest, filter="data")
