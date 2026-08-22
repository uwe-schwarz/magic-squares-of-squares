from __future__ import annotations

import re
import unittest
from pathlib import Path

from classes import CLASSES
from prime_power_rigidity import (
    cmul,
    cpow,
    gaussian_normalized_offsets,
    half_slope_unit,
    initial_branches,
    lift_once,
    normalized_offsets,
)
from targeted_reconstruction import exact_offsets, verify_candidate

HERE = Path(__file__).resolve().parent
CLASS_TABLE = HERE.parent / "coupled-p2qr-scan" / "class_table.h"


class PrimePowerTests(unittest.TestCase):
    def test_exact_class_fixture(self):
        self.assertEqual(len(CLASSES), 16)
        self.assertEqual(len({c[0] for c in CLASSES}), 16)

    def test_fixture_matches_generated_class_table(self):
        """Pin the fixture to the upstream generated table."""

        pattern = re.compile(
            r'\s*\{"([^"]+)", "([A-Z]+)", (true|false), '
            r"\{\{(.+)\},\{(.+)\},\{(.+)\}\}\},"
        )
        expected: dict[str, tuple[str, tuple[tuple[int, ...], ...]]] = {}
        for line in CLASS_TABLE.read_text().splitlines():
            m = pattern.match(line)
            if m and m.group(3) == "false":
                form, role, _, r0, r1, r2 = m.groups()
                expected[form] = (
                    role,
                    tuple(
                        tuple(int(x) for x in row.split(",")) for row in (r0, r1, r2)
                    ),
                )
        actual = {form: (role, idx) for form, role, idx in CLASSES}
        self.assertEqual(actual, expected)

    def test_half_slope_is_norm_one(self):
        for bits in range(4, 13):
            modulus = 1 << bits
            for x in range(min(32, 1 << (bits - 2))):
                a, b = half_slope_unit(x, modulus)
                self.assertEqual((a * a + b * b) % modulus, 1)

    def test_torus_matches_direct_gaussian_ratio(self):
        js = CLASSES[0][2]
        for bits in (6, 8, 10):
            modulus = 1 << bits
            for xs in ((0, 1, 2), (1, 3, 5), (2, 5, 7)):
                generators = tuple((1, 2 * x) for x in xs)
                self.assertEqual(
                    normalized_offsets(js, xs, modulus),
                    gaussian_normalized_offsets(js, generators, modulus),
                )

    def test_factor_two_is_observable(self):
        js = CLASSES[0][2]
        modulus = 256
        correct = normalized_offsets(js, (1, 2, 3), modulus)
        units = [half_slope_unit(x, modulus) for x in (1, 2, 3)]
        wrong = []
        for col in range(4):
            z = (1, 0)
            for row in range(3):
                z = cmul(z, cpow(units[row], int(js[row][col]), modulus), modulus)
            wrong.append(z[1] % modulus)
        self.assertNotEqual(correct, tuple(wrong))

    def test_counter_for_counter_lift(self):
        js = CLASSES[0][2]
        lifted = lift_once(js, initial_branches(js, 4), 5)
        direct = initial_branches(js, 5)
        key = lambda b: (b.xs, b.signs, b.edge_swap)  # noqa: E731
        self.assertEqual({key(b) for b in lifted}, {key(b) for b in direct})

    def test_exact_reembedding_rejects_toy_triple(self):
        js = CLASSES[0][2]
        generators = ((2, 1), (3, 2), (4, 1))
        self.assertEqual(len(exact_offsets(js, generators)), 4)
        self.assertFalse(verify_candidate(js, generators).coupled)

    def test_scan_driver_matches_committed_ledger(self):
        import json

        from scan_prime_powers import scan_class

        ledger = json.loads(
            (HERE / "scan_2adic_12.json").read_text()
        )
        for form, _, indices in CLASSES:
            expected = ledger["classes"][form]["forced_v2_at_target"]
            quick = scan_class(indices, 6)["levels"][-1]["min_common_v2"]
            self.assertEqual(quick, expected, form)


if __name__ == "__main__":
    unittest.main()
