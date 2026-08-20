import math
import os
from pathlib import Path
import subprocess
import tempfile
import unittest


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "two_block_factor_search.cpp"


def parse_summary(output: str) -> dict[str, int]:
    summary: dict[str, int] = {}
    for line in output.splitlines():
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        try:
            summary[key] = int(value)
        except ValueError:
            continue
    return summary


def primes_through(limit: int) -> list[int]:
    is_prime = bytearray(b"\x01") * (limit + 1)
    is_prime[:2] = b"\x00\x00"
    for prime in range(2, math.isqrt(limit) + 1):
        if is_prime[prime]:
            start = prime * prime
            is_prime[start : limit + 1 : prime] = b"\x00" * (
                (limit - start) // prime + 1
            )
    return [value for value in range(2, limit + 1) if is_prime[value]]


def is_fourth_power_residue(value: int, prime: int) -> bool:
    return pow(value % prime, (prime - 1) // 4, prime) == 1


def gaussian_multiply(
    left: tuple[int, int], right: tuple[int, int]
) -> tuple[int, int]:
    return (
        left[0] * right[0] - left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


def gaussian_power(value: tuple[int, int], exponent: int) -> tuple[int, int]:
    result = (1, 0)
    while exponent:
        if exponent & 1:
            result = gaussian_multiply(result, value)
        value = gaussian_multiply(value, value)
        exponent //= 2
    return result


def split_prime(prime: int) -> tuple[int, int]:
    for imag in range(2, math.isqrt(prime) + 1, 2):
        real = math.isqrt(prime - imag * imag)
        if real % 2 == 1 and real * real + imag * imag == prime:
            return real, imag
    raise AssertionError(f"no split representation for {prime}")


def local_squared_factors(prime: int, exponent: int) -> list[tuple[int, int]]:
    gaussian_prime = split_prime(prime)
    factors: list[tuple[int, int]] = []
    for index in range(-exponent, exponent + 1):
        real, imag = gaussian_power(gaussian_prime, 4 * abs(index))
        if index < 0:
            imag = -imag
        scale = prime ** (2 * (exponent - abs(index)))
        factors.append((scale * real, scale * imag))
    return factors


def offsets_from_local_factors(
    first: tuple[int, int], second: tuple[int, int]
) -> set[int]:
    _, first_prime, first_exponent = first
    _, second_prime, second_exponent = second
    offsets: set[int] = set()
    for left in local_squared_factors(first_prime, first_exponent):
        for right in local_squared_factors(second_prime, second_exponent):
            imag = left[0] * right[1] + left[1] * right[0]
            if imag:
                offsets.add(abs(imag))
    return offsets


def relation_count(offsets: set[int]) -> tuple[int, int]:
    ordered = sorted(offsets)
    relations = 0
    for first_index, first in enumerate(ordered):
        for second in ordered[first_index + 1 :]:
            if second != 2 * first:
                relations += (
                    second - first in offsets and second + first in offsets
                )
    return len(ordered) * (len(ordered) - 1) // 2, relations


def offset_fingerprint(offsets: set[int]) -> int:
    result = 1_469_598_103_934_665_603
    mask = (1 << 64) - 1
    for value in sorted(offsets):
        for shift in range(0, 256, 64):
            result ^= (value >> shift) & mask
            result = (result * 1_099_511_628_211) & mask
    return result


def reference_summary(limit: int) -> dict[str, int]:
    blocks: list[tuple[int, int, int]] = []
    for prime in primes_through(math.isqrt(limit)):
        if prime % 8 != 1:
            continue
        value = prime * prime
        exponent = 2
        while value <= limit:
            blocks.append((value, prime, exponent))
            value *= prime
            exponent += 1
    blocks.sort()

    dominant_blocks = [
        block
        for block in blocks
        if block[2] >= 3
        and block[1] % 24 == 1
        and is_fourth_power_residue(
            3 * pow(2, -1, block[1]), block[1]
        )
    ]
    block_pairs = 0
    offset_values = 0
    offset_pair_tests = 0
    relation_events = 0
    candidate_pairs = 0
    for dominant in dominant_blocks:
        for smaller in blocks:
            if smaller[0] >= dominant[0]:
                break
            if (
                smaller[1] == dominant[1]
                or dominant[0] ** 2 >= 3 * smaller[0] ** 2
            ):
                continue
            block_pairs += 1
            offsets = offsets_from_local_factors(dominant, smaller)
            offset_values += len(offsets)
            pair_tests, relations = relation_count(offsets)
            offset_pair_tests += pair_tests
            relation_events += relations
            candidate_pairs += relations != 0
    return {
        "limit": limit,
        "blocks": len(blocks),
        "dominant_blocks": len(dominant_blocks),
        "block_pairs": block_pairs,
        "offset_values": offset_values,
        "offset_pair_tests": offset_pair_tests,
        "relation_events": relation_events,
        "candidate_pairs": candidate_pairs,
    }


def direct_circle_offsets(center_root: int) -> set[int]:
    """Enumerate u^2+v^2=e^2 directly, independent of factorization."""

    norm = center_root * center_root
    offsets: set[int] = set()
    for real in range(center_root + 1):
        imag_squared = norm - real * real
        imag = math.isqrt(imag_squared)
        if imag * imag == imag_squared and real and imag:
            offsets.add(2 * real * imag)
    return offsets


class TwoBlockFactorScannerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.temp_directory = tempfile.TemporaryDirectory()
        cls.binary = Path(cls.temp_directory.name) / "two_block_factor_search"
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

    def test_synthetic_detector_and_gaussian_invariants(self) -> None:
        completed = subprocess.run(
            [str(self.binary), "--self-test"],
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertIn("self_test=ok", completed.stdout)
        self.assertIn("synthetic_relations=1", completed.stdout)

    def test_pair_offsets_match_direct_circle_enumeration(self) -> None:
        completed = subprocess.run(
            [str(self.binary), "--pair", "17", "2", "41", "2"],
            check=True,
            capture_output=True,
            text=True,
        )
        actual = parse_summary(completed.stdout)
        offsets = direct_circle_offsets((17**2) * (41**2))
        pair_tests, relations = relation_count(offsets)
        self.assertEqual(actual["offset_values"], len(offsets))
        self.assertEqual(actual["offset_pair_tests"], pair_tests)
        self.assertEqual(actual["relation_events"], relations)
        self.assertEqual(actual["offset_fingerprint"], offset_fingerprint(offsets))

    def test_256_bit_offsets_match_python_integers(self) -> None:
        completed = subprocess.run(
            [str(self.binary), "--pair", "97", "6", "693529", "2"],
            check=True,
            capture_output=True,
            text=True,
        )
        actual = parse_summary(completed.stdout)
        offsets = offsets_from_local_factors(
            (97**6, 97, 6), (693529**2, 693529, 2)
        )
        self.assertGreater(max(offsets).bit_length(), 128)
        pair_tests, relations = relation_count(offsets)
        self.assertEqual(actual["offset_values"], len(offsets))
        self.assertEqual(actual["offset_pair_tests"], pair_tests)
        self.assertEqual(actual["relation_events"], relations)
        self.assertEqual(actual["offset_fingerprint"], offset_fingerprint(offsets))

    def test_filtered_scan_matches_independent_python_reference(self) -> None:
        limit = 1_000_000
        completed = subprocess.run(
            [str(self.binary), str(limit)],
            check=True,
            capture_output=True,
            text=True,
        )
        actual = parse_summary(completed.stdout)
        expected = reference_summary(limit)
        self.assertEqual(actual, expected)
        self.assertEqual(actual["blocks"], 43)
        self.assertEqual(actual["dominant_blocks"], 1)
        self.assertEqual(actual["block_pairs"], 9)
        self.assertEqual(actual["offset_pair_tests"], 1364)
        self.assertEqual(actual["candidate_pairs"], 0)


if __name__ == "__main__":
    unittest.main()
