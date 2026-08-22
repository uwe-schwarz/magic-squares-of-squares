#!/usr/bin/env python3
"""Exact prime-power model for the 16 unresolved p^2*q*r switching classes.

The normalized squared Gaussian monomial for column c is
    W_c = prod_s (pi_s / conjugate(pi_s)) ** (2*j[s,c]).
The factor 2 is essential because an offset is |Im(z_c^2)|, not |Im(z_c)|.

For 2-adic work, write pi=a+bi with a odd and b even and set x=(b/2)/a.
Then u=pi/conj(pi) has the exact modular half-slope form
    u(x) = (1+2*i*x)/(1-2*i*x)
         = ((1-4*x^2) + 4*i*x)/(1+4*x^2).
All denominators are odd, hence invertible modulo 2^k.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from typing import Iterable, Sequence

Pair = tuple[int, int]
Signs = tuple[int, int, int, int]


def cmul(z: Pair, w: Pair, modulus: int) -> Pair:
    return ((z[0]*w[0]-z[1]*w[1]) % modulus,
            (z[0]*w[1]+z[1]*w[0]) % modulus)


def cinv(z: Pair, modulus: int) -> Pair:
    n = (z[0]*z[0] + z[1]*z[1]) % modulus
    ni = pow(n, -1, modulus)
    return (z[0]*ni % modulus, -z[1]*ni % modulus)


def cpow(z: Pair, exponent: int, modulus: int) -> Pair:
    if exponent < 0:
        return cpow(cinv(z, modulus), -exponent, modulus)
    out = (1, 0)
    while exponent:
        if exponent & 1:
            out = cmul(out, z, modulus)
        z = cmul(z, z, modulus)
        exponent >>= 1
    return out


def half_slope_unit(x: int, modulus: int) -> Pair:
    den = (1 + 4*x*x) % modulus
    inv = pow(den, -1, modulus)
    return ((1 - 4*x*x)*inv % modulus, 4*x*inv % modulus)


def normalized_offsets(indices: Sequence[Sequence[int]], xs: Sequence[int], modulus: int) -> tuple[int, int, int, int]:
    units = [half_slope_unit(int(x), modulus) for x in xs]
    values: list[int] = []
    for column in range(4):
        z = (1, 0)
        for row in range(3):
            z = cmul(z, cpow(units[row], 2*int(indices[row][column]), modulus), modulus)
        values.append(z[1] % modulus)
    return tuple(values)  # type: ignore[return-value]


def gaussian_normalized_offsets(indices: Sequence[Sequence[int]], generators: Sequence[Pair], modulus: int) -> tuple[int, int, int, int]:
    units = [cmul(g, cinv((g[0], -g[1]), modulus), modulus) for g in generators]
    values: list[int] = []
    for column in range(4):
        z = (1, 0)
        for row in range(3):
            z = cmul(z, cpow(units[row], 2*int(indices[row][column]), modulus), modulus)
        values.append(z[1] % modulus)
    return tuple(values)  # type: ignore[return-value]


def sign_patterns() -> tuple[tuple[Signs, bool], ...]:
    out = []
    for tail in product((1, -1), repeat=3):
        signs: Signs = (1, tail[0], tail[1], tail[2])
        out.append((signs, False))
        out.append((signs, True))
    return tuple(out)

PATTERNS = sign_patterns()


def coupled_residual(values: Sequence[int], signs: Signs, edge_swap: bool, modulus: int) -> tuple[int, int]:
    f = [signs[i] * int(values[i]) for i in range(4)]
    if edge_swap:
        f[2], f[3] = f[3], f[2]
    return ((f[2]-f[0]-f[1]) % modulus,
            (f[3]-f[0]+f[1]) % modulus)


def is_solution(indices: Sequence[Sequence[int]], xs: Sequence[int], modulus: int, signs: Signs, edge_swap: bool) -> bool:
    return coupled_residual(normalized_offsets(indices, xs, modulus), signs, edge_swap, modulus) == (0, 0)


def v2(value: int, modulus_bits: int) -> int:
    value %= 1 << modulus_bits
    if value == 0:
        return modulus_bits
    return (value & -value).bit_length() - 1


def common_offset_v2(values: Sequence[int], modulus_bits: int) -> int:
    return min(v2(int(value), modulus_bits) for value in values)

@dataclass(frozen=True)
class Branch:
    xs: tuple[int, int, int]
    signs: Signs
    edge_swap: bool


def initial_branches(indices: Sequence[Sequence[int]], bits: int = 4) -> list[Branch]:
    if bits < 4:
        raise ValueError("start at bits >= 4")
    modulus = 1 << bits
    domain = range(1 << (bits-2))
    out: list[Branch] = []
    for signs, swap in PATTERNS:
        for xs in product(domain, repeat=3):
            if is_solution(indices, xs, modulus, signs, swap):
                out.append(Branch(tuple(xs), signs, swap))
    return out


def lift_once(indices: Sequence[Sequence[int]], branches: Iterable[Branch], new_bits: int) -> list[Branch]:
    if new_bits < 5:
        raise ValueError("new_bits must be >= 5")
    modulus = 1 << new_bits
    bit = 1 << (new_bits-3)
    out: list[Branch] = []
    for branch in branches:
        for add in product((0, 1), repeat=3):
            xs = tuple(branch.xs[i] + add[i]*bit for i in range(3))
            if is_solution(indices, xs, modulus, branch.signs, branch.edge_swap):
                out.append(Branch(xs, branch.signs, branch.edge_swap))
    return out


def lift_to(indices: Sequence[Sequence[int]], target_bits: int, start_bits: int = 4) -> list[Branch]:
    branches = initial_branches(indices, start_bits)
    for bits in range(start_bits+1, target_bits+1):
        branches = lift_once(indices, branches, bits)
        if not branches:
            break
    return branches
