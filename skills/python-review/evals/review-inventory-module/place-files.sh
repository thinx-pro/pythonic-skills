#!/usr/bin/env bash
set -eu
here="$(dirname "$0")/files"
cp "$here/inventory.py" "$here/test_inventory.py" .
