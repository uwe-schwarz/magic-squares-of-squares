#!/usr/bin/env python3
"""Exact six-coordinate Gaussian re-embedding and final verification.

A modular or reconstructed hit is never accepted until these functions
re-expand the original Gaussian monomials over the integers and check the
full magic-square conditions.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import isqrt
from typing import Sequence

Pair = tuple[int, int]

# Row exponents of (p, q, r) in the center root p^2 q r.
BLOCK = (2, 1, 1)


def is_square(n: int) -> bool:
    if n < 0:
        return False
    root = isqrt(n)
    return root * root == n


def gaussian_mul(z: Pair, w: Pair) -> Pair:
    return (z[0] * w[0] - z[1] * w[1], z[0] * w[1] + z[1] * w[0])


def gaussian_pow(z: Pair, exponent: int) -> Pair:
    if exponent < 0:
        z = (z[0], -z[1])
        exponent = -exponent
    out = (1, 0)
    while exponent:
        if exponent & 1:
            out = gaussian_mul(out, z)
        z = gaussian_mul(z, z)
        exponent >>= 1
    return out


def column_monomial(
    indices: Sequence[Sequence[int]],
    generators: Sequence[Pair],
    column: int,
) -> Pair:
    """Return z_c^2 with z_c = prod_s pi_s^(k_s+j_s) conj(pi_s)^(k_s-j_s)."""

    out = (1, 0)
    for row, g in enumerate(generators):
        j = int(indices[row][column])
        k = BLOCK[row]
        out = gaussian_mul(out, gaussian_pow(g, 2 * (k + j)))
        out = gaussian_mul(out, gaussian_pow((g[0], -g[1]), 2 * (k - j)))
    return out


def exact_offsets(
    indices: Sequence[Sequence[int]], generators: Sequence[Pair]
) -> tuple[int, int, int, int]:
    return tuple(
        abs(column_monomial(indices, generators, c)[1]) for c in range(4)
    )  # type: ignore[return-value]


def center_root(generators: Sequence[Pair]) -> int:
    norms = [a * a + b * b for a, b in generators]
    return norms[0] * norms[0] * norms[1] * norms[2]


@dataclass(frozen=True)
class Verification:
    coupled: bool
    square_embeddings: bool
    positive: bool
    distinct: bool
    entries: tuple[int, ...]


def verify_candidate(
    indices: Sequence[Sequence[int]], generators: Sequence[Pair]
) -> Verification:
    """Check a candidate against every exact magic-square condition."""

    d = exact_offsets(indices, generators)
    coupled = {d[2], d[3]} == {d[0] + d[1], abs(d[0] - d[1])}
    e = center_root(generators)
    center_square = e * e
    entries = tuple(
        [center_square]
        + [center_square - x for x in d]
        + [center_square + x for x in d]
    )
    square_embeddings = all(
        is_square(center_square - x) and is_square(center_square + x) for x in d
    )
    return Verification(
        coupled=coupled,
        square_embeddings=square_embeddings,
        positive=all(x > 0 for x in entries),
        distinct=len(set(entries)) == 9,
        entries=entries,
    )


def is_full_magic_square(
    indices: Sequence[Sequence[int]], generators: Sequence[Pair]
) -> bool:
    v = verify_candidate(indices, generators)
    return v.coupled and v.square_embeddings and v.positive and v.distinct
