#!/usr/bin/env python3
"""Exact search helpers for the 3x3 magic square of squares problem.

The key observation is that an opposite pair around a center ``e**2`` is
square exactly when there is a Gaussian integer ``z = u + i*v`` of norm
``e**2``.  The corresponding positive offset is ``abs(Im(z**2)) = 2|uv|``.

This module enumerates those offsets from the Gaussian prime factorization of
the center root.  It then checks the complete additive condition

    {a, b, a + b, |a - b|}

rather than searching nine entries independently.
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass
from typing import Iterable

Gaussian = tuple[int, int]


def gaussian_mul(left: Gaussian, right: Gaussian) -> Gaussian:
    """Multiply two Gaussian integers represented by ``(real, imag)``."""

    a, b = left
    c, d = right
    return a * c - b * d, a * d + b * c


def gaussian_pow(base: Gaussian, exponent: int) -> Gaussian:
    """Raise a Gaussian integer to a nonnegative integer power."""

    if exponent < 0:
        raise ValueError("exponent must be nonnegative")
    result = (1, 0)
    factor = base
    power = exponent
    while power:
        if power & 1:
            result = gaussian_mul(result, factor)
        factor = gaussian_mul(factor, factor)
        power >>= 1
    return result


def factor_integer(value: int) -> dict[int, int]:
    """Return the prime factorization of a positive integer."""

    if value < 1:
        raise ValueError("value must be positive")
    factors: dict[int, int] = {}
    remaining = value
    divisor = 2
    while divisor * divisor <= remaining:
        while remaining % divisor == 0:
            factors[divisor] = factors.get(divisor, 0) + 1
            remaining //= divisor
        divisor = 3 if divisor == 2 else divisor + 2
    if remaining > 1:
        factors[remaining] = factors.get(remaining, 0) + 1
    return factors


def prime_as_sum_of_two_squares(prime: int) -> Gaussian:
    """Find positive ``a, b`` with ``prime = a**2 + b**2``.

    The caller must supply a prime congruent to 1 modulo 4.  Trial search is
    sufficient for the bounded, auditable experiments in this repository.
    """

    if prime % 4 != 1:
        raise ValueError(f"{prime} is not congruent to 1 modulo 4")
    for a in range(1, math.isqrt(prime) + 1):
        b_squared = prime - a * a
        b = math.isqrt(b_squared)
        if b > 0 and b * b == b_squared:
            return a, b
    raise ValueError(f"no sum-of-two-squares representation found for {prime}")


def is_primitive_center_candidate(center_root: int) -> bool:
    """Whether every prime divisor of a center root is 1 modulo 4."""

    return center_root > 1 and all(
        prime % 4 == 1 for prime in factor_integer(center_root)
    )


def passes_refined_block_balance(center_root: int) -> bool:
    """Apply the proved factorization and local block-balance filters.

    For ``P = p**k || e`` and ``M = e/P``, every primitive solution needs
    ``P**2 < 3*M**2``.  If ``p == 5 (mod 8)``, the stronger
    ``P < M`` holds.  More generally, a strictly dominant block ``P > M``
    must have exponent at least three and its prime must be 1 modulo 8.
    A center supported on exactly two rational primes is impossible.
    """

    if not is_primitive_center_candidate(center_root):
        return False
    factors = factor_integer(center_root)
    if len(factors) == 2:
        return False
    for prime, exponent in factors.items():
        block = prime**exponent
        complement = center_root // block
        if block > complement:
            if exponent < 3 or prime % 8 != 1:
                return False
        constant = 2 if prime % 8 == 5 else 3
        if block * block >= constant * complement * complement:
            return False
    return True


def gaussian_norm_representatives(center_root: int) -> set[Gaussian]:
    """Enumerate Gaussian integers of norm ``center_root**2`` up to units.

    Primitive center candidates have only split prime factors.  Choosing the
    exponent of one Gaussian prime above each rational prime therefore lists
    every representation.  Conjugate and unit associates are harmless later
    because offsets use an absolute imaginary part.
    """

    if not is_primitive_center_candidate(center_root):
        return set()

    representatives: set[Gaussian] = {(1, 0)}
    for prime, exponent in factor_integer(center_root).items():
        gaussian_prime = prime_as_sum_of_two_squares(prime)
        conjugate = gaussian_prime[0], -gaussian_prime[1]
        choices = {
            gaussian_mul(
                gaussian_pow(gaussian_prime, split_exponent),
                gaussian_pow(conjugate, 2 * exponent - split_exponent),
            )
            for split_exponent in range(2 * exponent + 1)
        }
        representatives = {
            gaussian_mul(existing, choice)
            for existing in representatives
            for choice in choices
        }

    expected_norm = center_root * center_root
    assert all(a * a + b * b == expected_norm for a, b in representatives)
    return representatives


def center_offsets(center_root: int) -> set[int]:
    """Return every positive offset whose two entries around the center square."""

    center = center_root * center_root
    offsets: set[int] = set()
    for real, imag in gaussian_norm_representatives(center_root):
        offset = abs(2 * real * imag)
        if 0 < offset < center:
            upper = center + offset
            lower = center - offset
            if math.isqrt(upper) ** 2 == upper and math.isqrt(lower) ** 2 == lower:
                offsets.add(offset)
    return offsets


def is_square(value: int) -> bool:
    """Return whether ``value`` is a nonnegative integer square."""

    return value >= 0 and math.isqrt(value) ** 2 == value


def line_sums(square: tuple[tuple[int, int, int], ...]) -> tuple[int, ...]:
    """Return the three row, three column, and two diagonal sums."""

    rows = tuple(sum(row) for row in square)
    columns = tuple(sum(square[row][column] for row in range(3)) for column in range(3))
    diagonals = (
        sum(square[index][index] for index in range(3)),
        sum(square[index][2 - index] for index in range(3)),
    )
    return rows + columns + diagonals


@dataclass(frozen=True)
class Candidate:
    """A fully verified magic-square candidate."""

    center_root: int
    a: int
    b: int
    entries: tuple[tuple[int, int, int], ...]

    @property
    def roots(self) -> tuple[tuple[int, int, int], ...]:
        return tuple(tuple(math.isqrt(entry) for entry in row) for row in self.entries)


def center_candidates(center_root: int) -> list[Candidate]:
    """Find and verify every offset configuration for one center root."""

    offsets = center_offsets(center_root)
    center = center_root * center_root
    candidates: list[Candidate] = []
    ordered_offsets = sorted(offsets)

    for index, a in enumerate(ordered_offsets):
        for b in ordered_offsets[index + 1 :]:
            difference = abs(a - b)
            total = a + b
            required = {a, b, difference, total}
            if len(required) != 4 or not required.issubset(offsets):
                continue

            square = (
                (center + a, center - a - b, center + b),
                (center - a + b, center, center + a - b),
                (center - b, center + a + b, center - a),
            )
            flat = tuple(entry for row in square for entry in row)
            if min(flat) <= 0 or len(set(flat)) != 9 or not all(map(is_square, flat)):
                continue
            sums = line_sums(square)
            if len(set(sums)) != 1 or sums[0] != 3 * center:
                continue
            candidates.append(Candidate(center_root, a, b, square))
    return candidates


def search_centers(limit: int, use_balance_filter: bool = True) -> dict[str, object]:
    """Search primitive center roots up to and including ``limit``."""

    stats = {
        "limit": limit,
        "primitive_center_candidates": 0,
        "after_balance_filter": 0,
        "with_at_least_four_offsets": 0,
        "configurations_tested": 0,
    }
    solutions: list[dict[str, object]] = []

    for center_root in range(2, limit + 1):
        if not is_primitive_center_candidate(center_root):
            continue
        stats["primitive_center_candidates"] += 1
        if use_balance_filter and not passes_refined_block_balance(center_root):
            continue
        stats["after_balance_filter"] += 1
        offsets = center_offsets(center_root)
        if len(offsets) < 4:
            continue
        stats["with_at_least_four_offsets"] += 1
        candidates = center_candidates(center_root)
        stats["configurations_tested"] += len(offsets) * (len(offsets) - 1) // 2
        for candidate in candidates:
            solutions.append(
                {
                    "center_root": center_root,
                    "offsets": [candidate.a, candidate.b],
                    "roots": candidate.roots,
                    "entries": candidate.entries,
                }
            )

    return {"stats": stats, "solutions": solutions}


def parse_args(argv: Iterable[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--center", type=int, help="inspect one center root")
    parser.add_argument("--limit", type=int, help="search all center roots up to this bound")
    parser.add_argument(
        "--no-balance-filter",
        action="store_true",
        help="do not apply the proved factorization and block-balance filters",
    )
    args = parser.parse_args(argv)
    if (args.center is None) == (args.limit is None):
        parser.error("choose exactly one of --center or --limit")
    return args


def main(argv: Iterable[str] | None = None) -> int:
    args = parse_args(argv)
    if args.center is not None:
        payload = {
            "center_root": args.center,
            "factorization": factor_integer(args.center),
            "primitive_center_candidate": is_primitive_center_candidate(args.center),
            "passes_refined_block_balance": passes_refined_block_balance(args.center),
            "offsets": sorted(center_offsets(args.center)),
            "solutions": [candidate.roots for candidate in center_candidates(args.center)],
        }
    else:
        payload = search_centers(args.limit, not args.no_balance_filter)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
