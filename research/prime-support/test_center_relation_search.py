import itertools
import math
import os
from pathlib import Path
import subprocess
import tempfile
import unittest


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "center_relation_search.cpp"


def factor(value: int) -> dict[int, int]:
    factors: dict[int, int] = {}
    divisor = 2
    while divisor * divisor <= value:
        while value % divisor == 0:
            factors[divisor] = factors.get(divisor, 0) + 1
            value //= divisor
        divisor = 3 if divisor == 2 else divisor + 2
    if value > 1:
        factors[value] = factors.get(value, 0) + 1
    return factors


def brute_offsets(center_root: int) -> list[int]:
    """Enumerate the lower square root directly, without Euclid triples."""

    center = center_root * center_root
    offsets: set[int] = set()
    for lower_root in range(1, center_root):
        upper_squared = 2 * center - lower_root * lower_root
        upper_root = math.isqrt(upper_squared)
        if upper_root * upper_root == upper_squared:
            offsets.add(upper_squared - center)
    return sorted(offsets)


def relation_counts(offsets: list[int]) -> dict[str, int]:
    counts = {
        "offset_pair_tests": 0,
        "relation_111_events": 0,
        "relation_211_events": 0,
        "full_candidates": 0,
    }
    values = set(offsets)
    for a, b in itertools.combinations(offsets, 2):
        counts["offset_pair_tests"] += 1
        difference = b - a
        total = a + b
        has_difference = difference in values
        has_total = total in values
        if has_difference and difference not in (a, b):
            counts["relation_111_events"] += 1
        if has_total and total not in (a, b):
            counts["relation_111_events"] += 1
        if 2 * a + b in values:
            counts["relation_211_events"] += 1
        if a + 2 * b in values:
            counts["relation_211_events"] += 1
        midpoint_partner = 2 * b - a
        if midpoint_partner not in (a, b) and midpoint_partner in values:
            counts["relation_211_events"] += 1
        if has_difference and has_total and len({a, b, difference, total}) == 4:
            counts["full_candidates"] += 1
    return counts


def python_reference(limit: int) -> dict[str, int]:
    stats = {
        "limit": limit,
        "scaled_representations": 0,
        "expected_scaled_representations": 0,
        "centers_with_representations": 0,
        "expected_centers_with_representations": 0,
        "representation_count_failures": 0,
        "duplicate_offset_failures": 0,
        "offset_pair_tests": 0,
        "relation_111_events": 0,
        "relation_211_events": 0,
        "full_candidates": 0,
        "eligible_primitive_centers": 0,
        "eligible_centers_with_at_least_4_offsets": 0,
        "eligible_four_rejected_by_original_constant_2": 0,
        "eligible_four_rejected_by_universal_sqrt3": 0,
        "eligible_four_rejected_by_sqrt3_plus_p5mod8_sqrt2": 0,
    }

    for center_root in range(1, limit + 1):
        offsets = brute_offsets(center_root)
        stats["scaled_representations"] += len(offsets)
        stats["expected_scaled_representations"] += len(offsets)
        if offsets:
            stats["centers_with_representations"] += 1
            stats["expected_centers_with_representations"] += 1
        for key, count in relation_counts(offsets).items():
            stats[key] += count

        factors = factor(center_root)
        eligible = center_root > 1 and all(prime % 4 == 1 for prime in factors)
        if not eligible:
            continue
        stats["eligible_primitive_centers"] += 1
        if len(offsets) < 4:
            continue
        stats["eligible_centers_with_at_least_4_offsets"] += 1
        passes_two = True
        passes_three = True
        passes_refined = True
        for prime, exponent in factors.items():
            block = prime**exponent
            complement = center_root // block
            if block > 2 * complement:
                passes_two = False
            if block * block > 3 * complement * complement:
                passes_three = False
            if (
                block * block > 3 * complement * complement
                or prime % 8 == 5
                and block * block > 2 * complement * complement
            ):
                passes_refined = False
        if not passes_two:
            stats["eligible_four_rejected_by_original_constant_2"] += 1
        if not passes_three:
            stats["eligible_four_rejected_by_universal_sqrt3"] += 1
        if not passes_refined:
            stats["eligible_four_rejected_by_sqrt3_plus_p5mod8_sqrt2"] += 1

    return stats


def parse_summary(output: str) -> dict[str, int]:
    parsed: dict[str, int] = {}
    for line in output.splitlines():
        if "=" not in line or line.startswith("  "):
            continue
        key, value = line.split("=", 1)
        try:
            parsed[key] = int(value)
        except ValueError:
            continue
    return parsed


class CenterRelationScannerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.temp_directory = tempfile.TemporaryDirectory()
        cls.binary = Path(cls.temp_directory.name) / "center_relation_search"
        compiler = os.environ.get("CXX", "clang++")
        subprocess.run(
            [compiler, "-O2", "-std=c++20", str(SOURCE), "-o", str(cls.binary)],
            check=True,
            capture_output=True,
            text=True,
        )

    @classmethod
    def tearDownClass(cls) -> None:
        cls.temp_directory.cleanup()

    def test_synthetic_relation_detector(self) -> None:
        completed = subprocess.run(
            [str(self.binary), "--self-test"],
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertIn("self_test=ok", completed.stdout)
        self.assertIn("positive_111_events=", completed.stdout)
        self.assertIn("positive_211_events=", completed.stdout)
        self.assertIn("positive_full_candidates=1", completed.stdout)

    def test_cpp_scan_matches_direct_root_enumeration(self) -> None:
        limit = 500
        completed = subprocess.run(
            [str(self.binary), str(limit), "125"],
            check=True,
            capture_output=True,
            text=True,
        )
        actual = parse_summary(completed.stdout)
        expected = python_reference(limit)
        for key, value in expected.items():
            self.assertEqual(actual[key], value, key)
        self.assertEqual(actual["relation_examples"], 0)


if __name__ == "__main__":
    unittest.main()
