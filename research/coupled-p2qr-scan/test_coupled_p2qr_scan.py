#!/usr/bin/env python3
"""Cross-validation tests for coupled_p2qr_scan.cpp.

The tests check the scanner against independent Python references:

- every class offset produced by --dump lies in the directly enumerated
  offset set S_e of the center root e = p^2 q r;
- brute-force search for full four-offset configurations and 111/211
  relations over S_e agrees with a complete small scanner run;
- the exact count of (triple, class, generator) evaluations surviving the
  prune filters matches an independent Python mirror of the proved
  inequalities (1), (5), (8), (9) of three-block-p2qr.md;
- the embedded class table matches the upstream classifier output.
"""

from __future__ import annotations

import re
import subprocess
import sys
import unittest
from itertools import combinations
from pathlib import Path

HERE = Path(__file__).resolve().parent
PRIME_SUPPORT = HERE.parent / "prime-support"
sys.path.insert(0, str(PRIME_SUPPORT))

from p2qr_monomial_filter import (  # noqa: E402
    classify_arithmetic_filter,
    local_indices,
)
from three_block_p2qr_signatures import classify_all  # noqa: E402

SCANNER = HERE / "coupled_p2qr_scan.cpp"


def build_scanner() -> Path:
    binary = Path("/tmp/coupled_p2qr_scan_test")
    subprocess.run(
        [
            "clang++",
            "-O2",
            "-std=c++20",
            SCANNER.name,
            "-o",
            str(binary),
        ],
        cwd=HERE,
        check=True,
        capture_output=True,
    )
    return binary


def run_scanner(binary: Path, *args: str) -> str:
    result = subprocess.run(
        [str(binary), *args], cwd=HERE, check=True, capture_output=True,
        text=True,
    )
    return result.stdout


# ---------------------------------------------------------------------------
# Independent Gaussian reference implemented with plain Python integers.
# ---------------------------------------------------------------------------

def gaussian_prime_of(prime: int) -> tuple[int, int]:
    """Return (a, b) with a^2 + b^2 = prime for a prime 1 mod 4."""

    for a in range(1, prime):
        b2 = prime - a * a
        if b2 <= 0:
            break
        b = int(b2**0.5)
        while b * b > b2:
            b -= 1
        while (b + 1) * (b + 1) <= b2:
            b += 1
        if b * b == b2 and b > 0:
            return (a, b)
    raise AssertionError(prime)


def gmul(z: tuple[int, int], w: tuple[int, int]) -> tuple[int, int]:
    return (z[0] * w[0] - z[1] * w[1], z[0] * w[1] + z[1] * w[0])


def gpow(z: tuple[int, int], n: int) -> tuple[int, int]:
    result = (1, 0)
    for _ in range(n):
        result = gmul(result, z)
    return result


def offset_set(p: int, q: int, r: int) -> set[int]:
    """Directly enumerate S_e for e = p^2 q r over all Gaussian divisors."""

    pi = gaussian_prime_of(p)
    beta = gaussian_prime_of(q)
    gamma = gaussian_prime_of(r)
    pib = (pi[0], -pi[1])
    betab = (beta[0], -beta[1])
    gammab = (gamma[0], -gamma[1])
    values = set()
    for a in range(5):
        for d in range(3):
            for g in range(3):
                z = gmul(
                    gmul(gpow(pi, a), gpow(pib, 4 - a)),
                    gmul(
                        gmul(gpow(beta, d), gpow(betab, 2 - d)),
                        gmul(gpow(gamma, g), gpow(gammab, 2 - g)),
                    ),
                )
                value = abs(2 * z[0] * z[1])
                if value:
                    values.add(value)
    return values


def has_full_config(offsets: set[int]) -> tuple[int, int] | None:
    """Return (a, b) with {a, b, a+b, a-b} in the offset set, or None."""

    for a, b in combinations(sorted(offsets), 2):
        if a + b in offsets and a - b in offsets:
            return (a, b)
    return None


def triple_relations(offsets: set[int]) -> list[tuple[str, int, int, int]]:
    """All 111 and 211 relations among distinct offsets, with labels."""

    events: list[tuple[str, int, int, int]] = []
    for x, y, z in combinations(sorted(offsets), 3):
        if x + y == z:
            events.append(("111", x, y, z))
        if 2 * x + y == z:
            events.append(("211", x, y, z))
        if x + 2 * y == z:
            events.append(("211", x, y, z))
        if 2 * x + z == y:
            events.append(("211", x, y, z))
        if x + 2 * z == y:
            events.append(("211", x, y, z))
        if 2 * y + z == x:
            events.append(("211", x, y, z))
    return events


# ---------------------------------------------------------------------------
# Python mirror of the prune inequalities from three-block-p2qr.md.
# ---------------------------------------------------------------------------

def python_prune(p: int, q: int, r: int, indices: list[list[int]]) -> bool:
    p2, q2, r2 = p * p, q * q, r * r
    if not p2 < q * r:
        return True
    if not q < p2 * r:
        return True
    if not r < p2 * q:
        return True
    ms2 = {(0,): (q * r) ** 2, (1,): (p2 * r) ** 2, (2,): (p2 * q) ** 2}
    bases = (p, q, r)
    k = (2, 1, 1)
    for row in range(3):
        vals = indices[row]
        extreme = k[row]
        if all(abs(v) == extreme for v in vals):
            continue  # role F
        s = bases[row]
        if abs(vals[0]) != extreme and abs(vals[1]) != extreme:
            pass  # cannot happen in this pattern
        # corner columns are 0 and 1; a corner role means the exceptional
        # column is 0 or 1.
        exc = [c for c in range(4) if abs(vals[c]) != extreme][0]
        if exc < 2:
            spow = s ** (4 + 2 * k[row])
            if not spow < 2 * ms2[(row,)]:
                return True
        else:
            if s % 8 != 1:
                return True
            sign = 1 if vals[0] > 0 else -1
            delta = 1
            for t in range(3):
                if t == row:
                    continue
                d0 = sign * indices[t][0]
                d1 = sign * indices[t][1]
                dt = 2 * k[t] - abs(d0 - d1)
                delta *= bases[t] ** dt
            if not s**4 * delta < 2 * ms2[(row,)]:
                return True
    return False


def load_table_classes() -> list[dict[str, object]]:
    text = (HERE / "class_table.h").read_text()
    entry = re.compile(r'\{"([^"]+)", "([CEF]+)", (true|false), \{')
    classes = []
    for m in entry.finditer(text):
        form, role, excluded = m.group(1), m.group(2), m.group(3)
        tail = text[m.end():text.index("}},", m.end())]
        rows = [
            [int(v) for v in row.split(",")]
            for row in re.findall(r"\{(-?\d+,-?\d+,-?\d+,-?\d+)\}", tail)
        ]
        assert len(rows) == 3, form
        classes.append(
            {"form": form, "role": role, "excluded": excluded == "true",
             "idx": rows}
        )
    return classes


def primes_one_mod_four(limit: int) -> list[int]:
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(limit**0.5) + 1):
        if sieve[i]:
            for j in range(i * i, limit + 1, i):
                sieve[j] = False
    return [n for n in range(5, limit + 1) if sieve[n] and n % 4 == 1]


class CoupledP2QRScanTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.binary = build_scanner()

    def test_class_table_matches_upstream_classifier(self) -> None:
        patterns: dict[str, tuple[int, int | None, int | None]] = {}
        for result in classify_all():
            for form in result.canonical_forms:
                patterns[form] = result.pattern
        excluded_map = {
            result.canonical_form: bool(result.excluded)
            for result in classify_arithmetic_filter()
        }
        table = load_table_classes()
        self.assertEqual(len(table), 134)
        self.assertEqual(
            {c["form"] for c in table}, set(patterns), "table form mismatch"
        )
        for c in table:
            expected = local_indices(patterns[c["form"]], c["form"])
            self.assertEqual(c["idx"], expected, c["form"])
            self.assertEqual(
                c["excluded"], excluded_map[c["form"]], c["form"]
            )
            self.assertEqual(
                c["role"],
                c["role"].upper(),
            )

    def test_offset_set_size_formula(self) -> None:
        # |S_e| = (prod (2k+1) - 1) / 2 = (5*3*3 - 1)/2 = 22.
        for p, q, r in [(5, 13, 17), (13, 17, 29), (5, 17, 41)]:
            offsets = offset_set(p, q, r)
            self.assertEqual(len(offsets), 22, (p, q, r))

    def test_dump_offsets_lie_in_S_e(self) -> None:
        table = load_table_classes()
        samples = [table[0], table[40], table[90], table[-1]]
        for c in samples:
            out = run_scanner(
                self.binary, f"--dump=5,13,29,{c['form']}"
            )
            e2 = (25 * 13 * 29) ** 2
            offsets = offset_set(5, 13, 29)
            for line in out.strip().splitlines():
                m = re.match(r"gen=(\d+) d=\((\d+),(\d+),(\d+),(\d+)\)", line)
                assert m
                for value in map(int, m.groups()[1:]):
                    self.assertIn(value, offsets)
                    self.assertLess(value, e2)

    def test_bruteforce_agrees_with_small_complete_scan(self) -> None:
        limit = 350
        primes = primes_one_mod_four(limit)
        for p, q, r in combinations(primes, 3):
            offsets = offset_set(p, q, r)
            self.assertIsNone(
                has_full_config(offsets), (p, q, r)
            )
            self.assertEqual(
                triple_relations(offsets), [], (p, q, r)
            )
        out = run_scanner(
            self.binary, f"--primes={limit}", "--threads=4"
        )
        summary = [
            line for line in out.splitlines() if line.startswith("SUMMARY")
        ][0]
        m = re.search(
            r"relation_111_events=(\d+) relation_211_events=(\d+) "
            r"full_configs=(\d+)",
            summary,
        )
        assert m
        self.assertEqual(m.group(1), "0")
        self.assertEqual(m.group(2), "0")
        self.assertEqual(m.group(3), "0")

    def test_prune_evaluation_count_matches_mirror(self) -> None:
        limit = 600
        primes = primes_one_mod_four(limit)
        table = load_table_classes()
        expected = 0
        for p, q, r in combinations(primes, 3):
            for squared, pair in (
                (p, (q, r)),
                (q, (p, r)),
                (r, (p, q)),
            ):
                e = squared * squared * pair[0] * pair[1]
                if e > 12_000_000_000_000_000_000:
                    continue
                for cls in table:
                    if cls["excluded"]:
                        continue
                    # Both ordered assignments of the exponent-one primes.
                    for flip in (False, True):
                        qv, rv = (
                            (pair[1], pair[0]) if flip else pair
                        )
                        if python_prune(squared, qv, rv, cls["idx"]):
                            continue
                        expected += 4  # generator choices
        out = run_scanner(
            self.binary,
            f"--primes={limit}",
            "--survivors-only",
            "--prune",
            "--threads=4",
        )
        m = re.search(r"evaluations=(\d+)", out)
        assert m
        self.assertEqual(int(m.group(1)), expected)

    def test_self_test_passes(self) -> None:
        run_scanner(self.binary, "--self-test")

    def test_smooth_scan_matches_python_mirror(self) -> None:
        # smooth_center_scan enumerates every center root whose split prime
        # factors are all at most sqrt(bound); the Python mirror rebuilds
        # S_e from Gaussian divisors and checks the same relation forms.
        binary = Path("/tmp/smooth_center_scan_test")
        subprocess.run(
            ["clang++", "-O2", "-std=c++20", "smooth_center_scan.cpp",
             "-o", str(binary)],
            cwd=HERE, check=True, capture_output=True,
        )
        bound = 250000
        limit = 500
        split = [
            p for p in range(5, limit + 1, 2)
            if p % 4 == 1 and all(p % q for q in range(3, int(p**0.5) + 1, 2))
        ]
        centers = []

        def dfs(e, idx, parts):
            if e > 1:
                centers.append((e, parts))
            for ii in range(idx, len(split)):
                p = split[ii]
                if e * p > bound:
                    break
                ee, k = e, 0
                while ee * p <= bound:
                    ee *= p
                    k += 1
                    dfs(ee, ii + 1, parts + [(p, k)])

        dfs(1, 0, [])
        total_offsets = 0
        rel111 = rel211 = full = 0
        for e, parts in centers:
            offsets = set()

            def build(i, z, parts=parts, offsets=offsets):
                if i == len(parts):
                    d = abs(2 * z[0] * z[1])
                    if d:
                        offsets.add(d)
                    return
                g = gaussian_prime_of(parts[i][0])
                gb = (g[0], -g[1])
                m = 2 * parts[i][1]
                for a in range(m + 1):
                    build(i + 1, gmul(z, gmul(gpow(g, a), gpow(gb, m - a))))

            build(0, (1, 0))
            total_offsets += len(offsets)
            for x in offsets:
                for y in offsets:
                    if x >= y:
                        continue
                    if x + y in offsets:
                        rel111 += 1
                    if 2 * x + y in offsets or x + 2 * y in offsets:
                        rel211 += 1
                    if 2 * y - x in offsets:
                        rel211 += 1
                    if (
                        y != 2 * x
                        and (y - x) in offsets
                        and (x + y) in offsets
                    ):
                        full += 1
        out = subprocess.run(
            [str(binary), f"--bound={bound}", "--threads=4"],
            cwd=HERE, check=True, capture_output=True, text=True,
        ).stdout
        m = re.search(
            r"centers_scanned=(\d+) offsets=(\d+) relation_111_events=(\d+)"
            r" relation_211_events=(\d+) full_configs=(\d+)",
            out,
        )
        assert m
        self.assertEqual(int(m.group(1)), len(centers))
        self.assertEqual(int(m.group(2)), total_offsets)
        self.assertEqual(int(m.group(3)), rel111)
        self.assertEqual(int(m.group(4)), rel211)
        self.assertEqual(int(m.group(5)), full)

    def test_rigidity_criterion_matches_small_primes(self) -> None:
        # Theorem (rigidity.md, section 3): at l = 7 (n = 2) and
        # l in {11, 13} (n = 3), a class is rigid exactly when the corner
        # column sum c0 + c1 lies in (nZ)^3.
        import torus_obstruction

        rigid7_expected = {
            "I2:0000/0011/01*0", "I2:0000/0011/010*", "I2:0000/0011/0101",
            "I2:0000/01*0/01*1", "I2:0000/010*/011*", "I2:0000/0101/00*1",
            "I2:0000/0101/01*0", "I2:0000/0101/0110",
        }
        rigid1113_expected = {"I0:0000/0101/0110"}
        for c in load_table_classes():
            if c["excluded"]:
                continue
            cols = [
                [c["idx"][r][col] for r in range(3)] for col in range(4)
            ]
            corner_sum = [a + b for a, b in zip(cols[0], cols[1])]
            lock2 = all(v % 2 == 0 for v in corner_sum)
            lock3 = all(v % 3 == 0 for v in corner_sum)
            self.assertEqual(
                lock2, c["form"] in rigid7_expected, (c["form"], corner_sum)
            )
            self.assertEqual(
                lock3, c["form"] in rigid1113_expected, (c["form"], corner_sum)
            )
        # Exhaustive torus decision agrees with the criterion at 7, 11, 13
        # and pins the larger verified rigid sets at 17 and 19.
        table = [c for c in load_table_classes() if not c["excluded"]]
        expected = {
            7: rigid7_expected,
            11: rigid1113_expected,
            13: rigid1113_expected,
            17: {
                "I2:0000/0011/010*", "I2:0000/01*0/01*1",
                "I2:0000/010*/011*", "I2:0000/0101/01*0",
                "I2:0000/0101/0110",
            },
            19: {"I2:0000/010*/011*"},
        }
        for mod, rigid_set in expected.items():
            for c in table:
                result = torus_obstruction.check_class(mod, c["idx"])
                self.assertEqual(
                    result["solvable"], c["form"] not in rigid_set,
                    (mod, c["form"]),
                )


if __name__ == "__main__":
    unittest.main()
