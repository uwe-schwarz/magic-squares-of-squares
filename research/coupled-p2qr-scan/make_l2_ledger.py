#!/usr/bin/env python3
"""Regenerate l2_rigidity_ledger.json, incrementally.

Stages (each written to the ledger file as it completes):
- enumeration[<l>] for each requested prime: exhaustive l^2 enumeration of
  all 16 classes; the dual Python path (brute cube == linear solve,
  counter-for-counter) is asserted at the small primes, the linear path
  alone at the larger ones (the C++ mirror torus_rigidity_l2.cpp covers
  every prime independently; its full-torus match counts are exactly 8x
  the Python counts);
- minor_check: the index-matrix finite verification behind the cap theorem;
- witnesses[<l>]: constructive valuation-1 witnesses at every odd rigid
  prime plus spot checks, each verified in direct Gaussian arithmetic.

Usage:
    python3 make_l2_ledger.py [--primes 7,11,13,17,19,29,31]

Runtime: about 25 minutes for 7..19, roughly 1-1.5 hours more each for
29 and 31 (single-threaded Python).
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from test_coupled_p2qr_scan import load_table_classes  # noqa: E402
from torus_obstruction_l2 import scan_brute, scan_linear  # noqa: E402
from l2_linearization import class_witness, minor_data  # noqa: E402

DUAL_PATH_PRIMES = {7, 11, 13}
WITNESS_PRIMES = [
    3, 5, 7, 11, 13, 17, 19, 29, 31, 37, 43, 53, 67, 89, 103, 127,
    149, 151, 197, 251,
]

OUT = HERE / "l2_rigidity_ledger.json"


def load_existing() -> dict:
    if OUT.exists():
        return json.loads(OUT.read_text())
    return {"enumeration": {}, "minor_check": {}, "witnesses": {}}


def save(ledger: dict) -> None:
    OUT.write_text(json.dumps(ledger, indent=2) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--primes", type=str, default="7,11,13,17,19,29,31")
    args = parser.parse_args()
    primes = [int(p) for p in args.primes.split(",")]
    table = [c for c in load_table_classes() if not c["excluded"]]
    ledger = load_existing()
    started = time.time()
    for l in primes:
        if str(l) in ledger["enumeration"]:
            print(f"enumeration l={l} already present, skipping", flush=True)
            continue
        print(f"enumerating l={l}", flush=True)
        ledger["enumeration"][str(l)] = {}
        for c in table:
            linear = scan_linear(c["idx"], l)
            entry = dict(linear)
            entry["forced_v"] = linear["min_common_v"]
            entry["role"] = c["role"]
            if l in DUAL_PATH_PRIMES:
                brute = scan_brute(c["idx"], l)
                assert brute["matches"] == linear["matches"]
                assert brute["min_common_v"] == linear["min_common_v"]
                entry["brute_verified"] = True
            ledger["enumeration"][str(l)][c["form"]] = entry
        save(ledger)
    if not ledger["minor_check"]:
        for c in table:
            minors, g, rank = minor_data(c["idx"])
            assert rank == 3 and g & (g - 1) == 0
            ledger["minor_check"][c["form"]] = {
                "minors": minors,
                "gcd": g,
                "rank": rank,
            }
        save(ledger)
    for l in WITNESS_PRIMES:
        if str(l) in ledger["witnesses"]:
            continue
        print(f"witnesses l={l}", flush=True)
        ledger["witnesses"][str(l)] = {}
        for c in table:
            w = class_witness(c["idx"], l)
            assert min(w["valuations"]) == 1
            ledger["witnesses"][str(l)][c["form"]] = {
                "b": w["b"],
                "pattern": w["pattern"],
            }
        save(ledger)
    ledger["seconds"] = round(time.time() - started, 1)
    save(ledger)
    print(f"wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
