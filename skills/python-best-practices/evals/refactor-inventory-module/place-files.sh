#!/usr/bin/env bash
set -eu
here="$(dirname "$0")/files"
cp "$here/inventory.py" "$here/test_inventory.py" .
# The eval sandbox has a bare python3; give the agent pytest so "the tests pass" is checkable.
python3 -m venv .venv
.venv/bin/python -m pip install --quiet --disable-pip-version-check pytest
