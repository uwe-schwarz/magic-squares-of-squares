from fractions import Fraction
import itertools
import math
import os
from pathlib import Path
import subprocess
import tempfile
import unittest


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "rational_relation_search.cpp"


def direct_primitive_offsets(hypotenuse_limit: int) -> list[Fraction]:
    """Enumerate primitive circle points directly, without Euclid parameters."""

    values: set[Fraction] = set()
    for hypotenuse in range(1, hypotenuse_limit + 1):
        hypotenuse_squared = hypotenuse * hypotenuse
        for first_leg in range(1, hypotenuse):
            second_leg_squared = hypotenuse_squared - first_leg * first_leg
            second_leg = math.isqrt(second_leg_squared)
            if second_leg == 0 or second_leg * second_leg != second_leg_squared:
                continue
            if math.gcd(first_leg, second_leg) != 1:
                continue
            values.add(Fraction(2 * first_leg * second_leg, hypotenuse_squared))
    return sorted(values)


def relation_counts(values: list[Fraction]) -> tuple[int, int, int]:
    known = set(values)
    pairs = relation_111 = relation_211 = 0
    for left, right in itertools.combinations(values, 2):
        pairs += 1
        relation_111 += left + right in known
        relation_211 += 2 * left + right in known
        relation_211 += left + 2 * right in known
        relation_211 += 2 * right - left in known
    return pairs, relation_111, relation_211


def parse_summary(output: str) -> dict[str, int]:
    parsed: dict[str, int] = {}
    for line in output.splitlines():
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        try:
            parsed[key] = int(value)
        except ValueError:
            continue
    return parsed


class RationalRelationScannerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.temp_directory = tempfile.TemporaryDirectory()
        cls.binary = Path(cls.temp_directory.name) / "rational_relation_search"
        compiler = os.environ.get("CXX", "clang++")
        subprocess.run(
            [
                compiler,
                "-O2",
                "-std=c++20",
                "-Wall",
                "-Wextra",
                "-pedantic",
                str(SOURCE),
                "-o",
                str(cls.binary),
            ],
            check=True,
            capture_output=True,
            text=True,
        )

    @classmethod
    def tearDownClass(cls) -> None:
        cls.temp_directory.cleanup()

    def test_synthetic_detector(self) -> None:
        completed = subprocess.run(
            [str(self.binary), "--self-test"],
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertIn("self-test passed", completed.stdout)
        self.assertIn("synthetic_111=", completed.stdout)
        self.assertIn("synthetic_211=", completed.stdout)

    def test_cpp_scan_matches_direct_circle_enumeration(self) -> None:
        limit = 500
        expected_values = direct_primitive_offsets(limit)
        expected_pairs, expected_111, expected_211 = relation_counts(expected_values)
        summaries: list[dict[str, int]] = []
        for threads in (1, 4):
            completed = subprocess.run(
                [str(self.binary), str(limit), str(threads)],
                check=True,
                capture_output=True,
                text=True,
            )
            actual = parse_summary(completed.stdout)
            self.assertEqual(actual["hypotenuse_limit"], limit)
            self.assertEqual(actual["threads"], threads)
            self.assertEqual(actual["primitive_offset_values"], len(expected_values))
            self.assertEqual(actual["offset_pairs"], expected_pairs)
            self.assertEqual(actual["relation_111_events"], expected_111)
            self.assertEqual(actual["relation_211_events"], expected_211)
            summaries.append(actual)

        self.assertEqual(
            {key: value for key, value in summaries[0].items() if key != "threads"},
            {key: value for key, value in summaries[1].items() if key != "threads"},
        )


if __name__ == "__main__":
    unittest.main()
