#!/bin/sh
set -eu
cd "$(dirname "$0")"
python3 -m unittest -v test_coupled_identity_model.py
python3 coupled_identity_model.py >/dev/null
