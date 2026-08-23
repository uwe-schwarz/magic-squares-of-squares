"""Cross-validation tests for the prime-power (l^2) torus rigidity scan.

The discipline mirrors the mod-l tests: two independent Python paths
(exhaustive squares-subgroup cube vs. linear tau^2 solve) must agree
counter-for-counter, the C++ full-torus enumeration must agree on outcomes
with exactly eight times the match counts (rho -> rho^2 is 2-to-1 per
factor), and the outcome min_common_v >= 1 must reproduce the mod-l
rigidity classification of the committed checker.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent

from test_coupled_p2qr_scan import load_table_classes  # noqa: E402
from torus_obstruction import check_class  # noqa: E402
from torus_obstruction_l2 import scan_brute, scan_linear  # noqa: E402
from l2_linearization import (  # noqa: E402
    class_witness,
    minor_data,
)

SMALL_PRIMES = [7, 11]
AGREEMENT_PRIMES = [7, 11, 13]
LEDGER = HERE / "l2_rigidity_ledger.json"


def classes() -> list[dict]:
    return [c for c in load_table_classes() if not c["excluded"]]


def build_cpp() -> Path:
    binary = Path("/tmp/torus_rigidity_l2_test")
    compiler = os.environ.get("CXX", "clang++")
    subprocess.run(
        [compiler, "-O2", "-std=c++20", "torus_rigidity_l2.cpp",
         "-o", str(binary)],
        cwd=HERE, check=True, capture_output=True, text=True,
    )
    return binary


def run_cpp(binary: Path, primes: list[int]) -> dict[str, dict[str, dict]]:
    out = subprocess.run(
        [str(binary), *[str(p) for p in primes]],
        cwd=HERE, check=True, capture_output=True, text=True,
    ).stdout
    result: dict[str, dict[str, dict]] = {}
    prime = None
    for line in out.splitlines():
        m = re.match(r"prime (\d+) \(modulus (\d+)\)", line)
        if m:
            prime = m.group(1)
            result[prime] = {}
            continue
        m = re.match(
            r"  (\S+) \((\w+)\): (.+) \[matches=(\d+), min_common_v=(\d+)\]",
            line,
        )
        if m and prime:
            result[prime][m.group(1)] = {
                "matches": int(m.group(4)),
                "min_common_v": int(m.group(5)),
            }
    return result


class L2PathAgreement(unittest.TestCase):
    def test_brute_matches_linear_counter_for_counter(self) -> None:
        for l in SMALL_PRIMES:
            for c in classes():
                with self.subTest(l=l, form=c["form"]):
                    brute = scan_brute(c["idx"], l)
                    linear = scan_linear(c["idx"], l)
                    self.assertEqual(brute["matches"], linear["matches"])
                    self.assertEqual(
                        brute["min_common_v"], linear["min_common_v"]
                    )

    def test_cpp_matches_python_with_factor_eight(self) -> None:
        binary = build_cpp()
        cpp = run_cpp(binary, AGREEMENT_PRIMES)
        for l in AGREEMENT_PRIMES:
            for c in classes():
                with self.subTest(l=l, form=c["form"]):
                    linear = scan_linear(c["idx"], l)
                    entry = cpp[str(l)][c["form"]]
                    self.assertEqual(
                        entry["matches"], 8 * linear["matches"]
                    )
                    self.assertEqual(
                        entry["min_common_v"], linear["min_common_v"]
                    )

    def test_outcome_reproduces_mod_l_rigidity(self) -> None:
        # min_common_v >= 1 at l is exactly "no non-degenerate solution
        # mod l", i.e. the committed mod-l classification of rigidity.md.
        ledger = json.loads(LEDGER.read_text())
        for l in [7, 11, 13, 17, 19]:
            for c in classes():
                with self.subTest(l=l, form=c["form"]):
                    forced = ledger["enumeration"][str(l)][c["form"]][
                        "forced_v"
                    ]
                    rigid = not check_class(l, c["idx"])["solvable"]
                    self.assertEqual(forced >= 1, rigid)


class L2LedgerPins(unittest.TestCase):
    """Pinned outcomes of the committed authoritative run.

    At every rigid prime through 19 the exhaustive l^2 enumeration finds
    minimum common valuation exactly 1: no rigid (class, l) pair upgrades
    its forced divisibility from l | d to l^2 | d.  For 29 and 31 the same
    conclusion holds by the cap-theorem witnesses (constructive valuation-1
    branches, pinned above), and the rigid classification there is
    cross-checked against the committed mod-l checker.  The 19-rigid class
    set records the corrected rigidity.md table: only I2:0000/010*/011* is
    rigid at 19 (the old table wrongly listed I2:0000/01*0/01*1 as well).
    """

    RIGID_THROUGH_31 = {
        "I0:0000/0101/0110": [11, 13, 29],
        "I2:0000/0011/01*0": [7],
        "I2:0000/0011/010*": [7, 17, 31],
        "I2:0000/0011/0101": [7, 29],
        "I2:0000/01*0/01*1": [7, 17, 29, 31],
        "I2:0000/010*/011*": [7, 17, 19, 29, 31],
        "I2:0000/0101/00*1": [7],
        "I2:0000/0101/01*0": [7, 17, 31],
        "I2:0000/0101/0110": [7, 17, 29, 31],
        "I0:0000/0011/0101": [29],
    }

    def test_ledger_covers_enumerated_range(self) -> None:
        ledger = json.loads(LEDGER.read_text())
        for l in [7, 11, 13, 17, 19]:
            self.assertIn(str(l), ledger["enumeration"])
            self.assertEqual(len(ledger["enumeration"][str(l)]), 16)
        # the C++ mirror covers every enumerated prime; 29/31 may be added
        # by a longer rerun but are not required (witnesses cover them).
        for l in [29, 31]:
            if str(l) in ledger["enumeration"]:
                self.assertEqual(len(ledger["enumeration"][str(l)]), 16)

    def test_no_l2_upgrade_in_enumerated_range(self) -> None:
        ledger = json.loads(LEDGER.read_text())
        for l, per_class in ledger["enumeration"].items():
            for form, entry in per_class.items():
                if entry["forced_v"] >= 1:
                    self.assertEqual(entry["forced_v"], 1, (l, form, entry))

    def test_rigid_prime_sets_through_31(self) -> None:
        ledger = json.loads(LEDGER.read_text())
        rigid: dict[str, list[int]] = {
            form: [] for form in self.RIGID_THROUGH_31
        }
        for l in [7, 11, 13, 17, 19, 29, 31]:
            if str(l) in ledger["enumeration"]:
                for form, entry in ledger["enumeration"][str(l)].items():
                    if entry["forced_v"] >= 1:
                        rigid.setdefault(form, []).append(l)
            else:
                # fall back to the committed mod-l checker
                for c in classes():
                    if not check_class(l, c["idx"])["solvable"]:
                        rigid.setdefault(c["form"], []).append(l)
        self.assertEqual(
            {k: sorted(v) for k, v in rigid.items()},
            self.RIGID_THROUGH_31,
        )

    def test_ledger_spot_check_recompute(self) -> None:
        ledger = json.loads(LEDGER.read_text())
        for l, form in [
            (13, "I0:0000/0101/0110"),
            (17, "I2:0000/010*/011*"),
            (19, "I2:0000/010*/011*"),
            (19, "I2:0000/01*0/01*1"),
        ]:
            with self.subTest(l=l, form=form):
                cls = next(c for c in classes() if c["form"] == form)
                linear = scan_linear(cls["idx"], l)
                self.assertEqual(
                    linear["matches"],
                    ledger["enumeration"][str(l)][form]["matches"],
                )
                self.assertEqual(
                    linear["min_common_v"],
                    ledger["enumeration"][str(l)][form]["forced_v"],
                )


class L2CapTheorem(unittest.TestCase):
    """The Section 4b cap theorem of rigidity.md and its finite checks.

    The rank/minor computation is the theorem's finite verification: rank 3
    over Q with minor gcd a power of two makes the index matrix injective
    modulo every odd prime.  Witnesses are then verified in direct Gaussian
    arithmetic at every odd rigid prime through 197 (plus 3, 5, 251 spot
    checks), independent of the linearized derivation.
    """

    WITNESS_PRIMES = [
        3, 5, 7, 11, 13, 17, 19, 29, 31, 37, 43, 53, 67, 89, 103, 127,
        149, 151, 197, 251,
    ]

    def test_index_matrix_rank_and_minors(self) -> None:
        for c in classes():
            with self.subTest(form=c["form"]):
                minors, g, rank = minor_data(c["idx"])
                self.assertEqual(rank, 3)
                self.assertEqual(g & (g - 1), 0)  # power of two
                self.assertIn(g, (1, 2, 4))

    def test_witnesses_at_rigid_primes(self) -> None:
        for l in self.WITNESS_PRIMES:
            for c in classes():
                with self.subTest(l=l, form=c["form"]):
                    witness = class_witness(c["idx"], l)
                    self.assertEqual(min(witness["valuations"]), 1)
                    self.assertTrue(any(witness["b"]))

    def test_witness_agrees_with_enumeration(self) -> None:
        # The theorem predicts the enumeration never sees a forced l^2
        # divisibility; the ledger pins that for every (class, l) scanned.
        ledger = json.loads(LEDGER.read_text())
        for l, per_class in ledger["enumeration"].items():
            for form, entry in per_class.items():
                self.assertLessEqual(entry["forced_v"], 1)


if __name__ == "__main__":
    unittest.main()
