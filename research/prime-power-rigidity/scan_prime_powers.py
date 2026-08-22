#!/usr/bin/env python3
"""Reproducible 2-adic prime-power scan for the 16 unresolved classes.

For each class this driver enumerates every solution branch of the coupled
system modulo 2^4 and lifts every branch level by level to a target
precision, recording the branch counts and the minimum common offset
valuation at each level.  If every branch at level k has common valuation
at least m, then every integer realization of the class has 2^m dividing
all four offsets, so the recorded minimum is exactly the forced 2-adic
divisibility of the class at that precision.

Usage:
    python3 scan_prime_powers.py [--bits 12] [--json OUT.json]
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

from classes import CLASSES
from prime_power_rigidity import (
    common_offset_v2,
    initial_branches,
    lift_once,
    normalized_offsets,
)


def scan_class(indices, target_bits: int, start_bits: int = 4) -> dict:
    modulus = 1 << start_bits
    branches = initial_branches(indices, start_bits)
    levels = []
    for bits in range(start_bits, target_bits + 1):
        modulus = 1 << bits
        valuations = [
            common_offset_v2(normalized_offsets(indices, b.xs, modulus), bits)
            for b in branches
        ]
        levels.append(
            {
                "bits": bits,
                "branches": len(branches),
                "min_common_v2": min(valuations),
                "max_common_v2": max(valuations),
            }
        )
        if bits < target_bits:
            branches = lift_once(indices, branches, bits + 1)
    return {
        "levels": levels,
        "forced_v2_at_target": levels[-1]["min_common_v2"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bits", type=int, default=12)
    parser.add_argument("--json", type=str, default="")
    args = parser.parse_args()

    report: dict = {"target_bits": args.bits, "classes": {}}
    started = time.time()
    for form, role, indices in CLASSES:
        result = scan_class(indices, args.bits)
        report["classes"][form] = result
        tail = result["levels"][-1]
        print(
            f"{form} ({role}): branches@2^{args.bits} = {tail['branches']}, "
            f"forced common v2 = {result['forced_v2_at_target']} "
            f"(range {tail['min_common_v2']}..{tail['max_common_v2']})",
            flush=True,
        )
    report["seconds"] = round(time.time() - started, 1)

    if args.json:
        Path(args.json).write_text(json.dumps(report, indent=2) + "\n")
        print(f"wrote {args.json} ({report['seconds']}s)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
