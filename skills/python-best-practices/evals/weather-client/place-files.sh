#!/usr/bin/env bash
set -eu
# The eval sandbox has a bare python3; give the agent requests and pytest to build and test with.
python3 -m venv .venv
.venv/bin/python -m pip install --quiet --disable-pip-version-check pytest requests
