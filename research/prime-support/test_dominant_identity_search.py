import itertools
import math
import os
from pathlib import Path
import subprocess
import tempfile
import unittest


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "dominant_identity_search.cpp"


def gaussian_mul(left: tuple[int, int], right: tuple[int, int]) -> tuple[int, int]:
    return (
        left[0] * right[0] - left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


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


def is_split_only(value: int) -> bool:
    return all(prime % 4 == 1 for prime in factor(value))


def brute_gaussian_squares(norm_root: int) -> list[tuple[int, int]]:
    """Enumerate G=w^2 directly, without Gaussian factorization."""

    norm = norm_root * norm_root
    roots: set[tuple[int, int]] = set()
    for real in range(-norm_root, norm_root + 1):
        imag_squared = norm - real * real
        imag = math.isqrt(imag_squared)
        if imag * imag != imag_squared:
            continue
        roots.add((real, imag))
        roots.add((real, -imag))
    return sorted({gaussian_mul(root, root) for root in roots})


def exact_fourth_root(value: int) -> int | None:
    square_root = math.isqrt(value)
    if square_root * square_root != value:
        return None
    fourth_root = math.isqrt(square_root)
    return fourth_root if fourth_root**2 == square_root else None


def python_reference(limit: int) -> dict[str, dict[str, int]]:
    header = {"M_limit": limit, "eligible_M": 0, "total_G_values": 0}
    one = {
        "111_loops": 0,
        "norm_window": 0,
        "fourth_norms": 0,
    }
    two = {
        "211_loops": 0,
        "norm_window": 0,
        "fourth_norms": 0,
    }

    for norm_root in range(1, limit + 1, 2):
        if not is_split_only(norm_root):
            continue
        header["eligible_M"] += 1
        values = brute_gaussian_squares(norm_root)
        header["total_G_values"] += len(values)
        fourth_power = norm_root**4

        for terms in itertools.combinations_with_replacement(values, 3):
            one["111_loops"] += 1
            real = sum(term[0] for term in terms)
            imag = sum(term[1] for term in terms)
            result_norm = real * real + imag * imag
            if fourth_power < result_norm <= 9 * fourth_power:
                one["norm_window"] += 1
                root = exact_fourth_root(result_norm)
                if root is not None and root > norm_root:
                    one["fourth_norms"] += 1

        for doubled in values:
            for pair in itertools.combinations_with_replacement(values, 2):
                two["211_loops"] += 1
                real = (2 * doubled[0] + pair[0][0] + pair[1][0]) // 2
                imag = (2 * doubled[1] + pair[0][1] + pair[1][1]) // 2
                result_norm = real * real + imag * imag
                if fourth_power < result_norm <= 4 * fourth_power:
                    two["norm_window"] += 1
                    root = exact_fourth_root(result_norm)
                    if root is not None and root > norm_root:
                        two["fourth_norms"] += 1

    return {"header": header, "111": one, "211": two}


def parse_summary(output: str) -> dict[str, dict[str, int]]:
    parsed: dict[str, dict[str, int]] = {}
    for line in output.splitlines():
        if line.startswith("M_limit="):
            section = "header"
        elif line.startswith("111_loops="):
            section = "111"
        elif line.startswith("211_loops="):
            section = "211"
        else:
            continue
        parsed[section] = {
            key: int(value)
            for token in line.split()
            for key, value in [token.split("=", 1)]
        }
    return parsed


class DominantIdentityScannerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.temp_directory = tempfile.TemporaryDirectory()
        cls.binary = Path(cls.temp_directory.name) / "dominant_identity_search"
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

    def test_synthetic_identity_pipeline(self) -> None:
        completed = subprocess.run(
            [str(self.binary), "--self-test"],
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertIn("self_test=ok", completed.stdout)
        self.assertIn("HIT M=3 q=5", completed.stdout)
        self.assertIn("HIT M=11 q=13", completed.stdout)

    def test_cpp_enumeration_matches_independent_brute_force(self) -> None:
        limit = 200
        completed = subprocess.run(
            [str(self.binary), str(limit)],
            check=True,
            capture_output=True,
            text=True,
        )
        actual = parse_summary(completed.stdout)
        expected = python_reference(limit)

        for key, value in expected["header"].items():
            self.assertEqual(actual["header"][key], value, key)
        for section in ("111", "211"):
            for key, value in expected[section].items():
                self.assertEqual(actual[section][key], value, f"{section}:{key}")
            self.assertEqual(actual[section]["prime_power_norms"], 0)
            self.assertEqual(actual[section]["pure_targets"], 0)
            self.assertEqual(actual[section]["genuine_hits"], 0)


if __name__ == "__main__":
    unittest.main()
