#!/bin/sh
set -eu
python3 -m unittest -v test_prime_power_rigidity.py test_deep_regular_lift.py
