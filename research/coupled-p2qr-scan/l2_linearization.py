#!/usr/bin/env python3
"""The l^2 cap theorem: torus rigidity never upgrades from l | d to l^2 | d.

Statement.  For each of the sixteen unresolved p^2 q r classes and every odd
prime l, the coupled torus system modulo l^2 admits a solution whose four
offsets have common l-valuation exactly 1.  Consequently, the mod-l
rigidity lemma (rigidity.md, Section 2) can never be strengthened to a
forced l^2 | d_c by torus enumeration at any odd prime: whenever a class is
rigid at l, the forced divisibility of the method caps at l | d_c.

Proof (constructive).  Write any element of the norm-one torus of Z[i]/l^2
as omega * (1 + l*b*i): the principal unit is purely imaginary because
N(1 + l*(a+bi)) = 1 + 2*l*a (mod l^2).  Expanding the normalized column

    x_c = prod_s (omega_s (1 + l b_s i))^(2 j[s,c])
        = xbar_c * (1 + l * K_c * i),   K_c = sum_s 2 j[s,c] b_s,

exactly modulo l^2, since (1 + l z)^n = 1 + n l z (mod l^2) holds for every
integer n.  At the all-ones base xbar_c = 1, so v_c := Im(x_c) = l * K_c.
The pattern equations on v_c modulo l^2 therefore reduce, dividing by l, to
the SAME linear relations on u = M b (M the 4x3 matrix of local indices,
u_c = sum_s 2 j[s,c] b_s): a valuation-1 branch is exactly a nonzero
solution b of the two linear pattern equations with M b nonzero mod l.

Two finite facts finish the proof for every odd l at once:

1. rank_Q(M) = 3 and the gcd of the four 3x3 minors of M is a power of two
   for each class (checked in code below), so M stays injective modulo
   every odd l: b != 0 implies M b != 0.
2. Two homogeneous linear equations in three unknowns always have a
   nonzero solution.

So any nonzero kernel vector b of a pattern's equation pair yields the
witness generators 1 + l b_s i, and the branch has common valuation exactly
1 because M b is nonzero in at least one coordinate.

This module machine-checks everything: the minor computation per class,
and for any (class, l) an explicit witness whose pattern equations and
valuation-1 common divisibility are verified in full Gaussian arithmetic
modulo l^2, independent of the derivation above.

Note the honest scope: the theorem caps the MOD-l^2 ENUMERATION argument.
It does not exclude that deeper l-adic analysis (l^3 and beyond) could
force more, and it says nothing about l = 2, where the committed
prime-power-rigidity scans do find genuine forced 16 | d_c structure.
"""

from __future__ import annotations

import argparse
import json
import sys
from math import gcd
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from test_coupled_p2qr_scan import load_table_classes  # noqa: E402

Pair = tuple[int, int]


def gmul(z: Pair, w: Pair, mod: int) -> Pair:
    return (
        (z[0] * w[0] - z[1] * w[1]) % mod,
        (z[0] * w[1] + z[1] * w[0]) % mod,
    )


def ginv(z: Pair, mod: int) -> Pair:
    n = (z[0] * z[0] + z[1] * z[1]) % mod
    ni = pow(n, -1, mod)
    return (z[0] * ni % mod, (-z[1]) * ni % mod)


def gpow(z: Pair, exponent: int, mod: int) -> Pair:
    if exponent < 0:
        return gpow(ginv(z, mod), -exponent, mod)
    out: Pair = (1, 0)
    while exponent:
        if exponent & 1:
            out = gmul(out, z, mod)
        z = gmul(z, z, mod)
        exponent >>= 1
    return out


def column_vectors(indices: list[list[int]]) -> list[tuple[int, int, int]]:
    return [
        (indices[0][c], indices[1][c], indices[2][c]) for c in range(4)
    ]


def det3(cols: list[tuple[int, int, int]]) -> int:
    a, b, c = cols
    return (
        a[0] * (b[1] * c[2] - b[2] * c[1])
        - b[0] * (a[1] * c[2] - a[2] * c[1])
        + c[0] * (a[1] * b[2] - a[2] * b[1])
    )


def minor_data(indices: list[list[int]]) -> tuple[list[int], int, int]:
    """(four 3x3 minors, their gcd, rank over Q)."""

    cols = column_vectors(indices)
    from itertools import combinations

    minors = [det3(list(combo)) for combo in combinations(cols, 3)]
    g = 0
    for m in minors:
        g = gcd(g, abs(m))
    if all(m == 0 for m in minors):
        rank = 2  # columns are pairwise distinct
    else:
        rank = 3
    return minors, g, rank


def kernel_witness(
    indices: list[list[int]], l: int, e1: int, e2: int, e3: int, swap: bool
) -> tuple[int, int, int]:
    """A nonzero b solving the linearized pattern equations mod l.

    Rows: r1 = e2*col_se - col0 - e1*col1, r2 = e3*col_de - col0 + e1*col1
    (the factors of 2 from u_c = 2*(Mb)_c cancel).  Returns a nonzero
    element of ker(r1) cap ker(r2) over Z/l, l odd.
    """

    mod = l
    cols = column_vectors(indices)
    se, de = (3, 2) if swap else (2, 3)

    def row(kappa_se: int, kappa0: int, kappa1: int, kappa_de: int):
        return tuple(
            (kappa_se * cols[se][i] + kappa0 * cols[0][i]
             + kappa1 * cols[1][i] + kappa_de * cols[de][i]) % mod
            for i in range(3)
        )

    r1 = row(e2, -1, -e1, 0)
    r2 = row(0, -1, e1, e3)
    # Cross product of the two rows (independent rows -> spans the kernel).
    b = (
        (r1[1] * r2[2] - r1[2] * r2[1]) % mod,
        (r1[2] * r2[0] - r1[0] * r2[2]) % mod,
        (r1[0] * r2[1] - r1[1] * r2[0]) % mod,
    )
    if any(b):
        return b
    # Dependent rows: any nonzero vector orthogonal to a nonzero row of the
    # pair works; if both rows vanish the kernel is everything.
    r = r1 if any(r1) else r2
    if not any(r):
        return (1, 0, 0)
    for candidate in (
        (r[1], (-r[0]) % mod, 0),
        (r[2], 0, (-r[0]) % mod),
        (0, r[2], (-r[1]) % mod),
    ):
        if any(candidate):
            return candidate  # type: ignore[return-value]
    raise AssertionError("unreachable: some candidate is always nonzero")


def apply_index(u: tuple[int, int, int], indices: list[list[int]]) -> list[int]:
    """u_c = sum_s 2*j[s,c]*b_s (the linearized offset divided by l)."""

    return [
        2 * (indices[0][c] * u[0] + indices[1][c] * u[1] + indices[2][c] * u[2])
        for c in range(4)
    ]


def verify_witness(
    indices: list[list[int]],
    l: int,
    b: tuple[int, int, int],
    e1: int,
    e2: int,
    e3: int,
    swap: bool,
) -> dict[str, object]:
    """Full Gaussian check of a witness triple modulo l^2.

    Builds the generators 1 + l*b_s*i, recomputes the four normalized
    columns with schoolbook Gaussian powers, and checks: norm-one
    generators, the two pattern equations, and common valuation exactly 1.
    This path shares no logic with the linearization derivation.
    """

    mod = l * l
    generators = [(1 % mod, (l * b[s]) % mod) for s in range(3)]
    for g in generators:
        norm = (g[0] * g[0] + g[1] * g[1]) % mod
        if norm != 1 % mod:
            raise AssertionError(f"generator {g} not norm-one mod {mod}")
    values = []
    for c in range(4):
        x: Pair = (1, 0)
        for s in range(3):
            x = gmul(x, gpow(generators[s], 2 * indices[s][c], mod), mod)
        values.append(x[1] % mod)
    se, de = (3, 2) if swap else (2, 3)
    eq1 = (e2 * values[se] - values[0] - e1 * values[1]) % mod
    eq2 = (e3 * values[de] - values[0] + e1 * values[1]) % mod
    if eq1 or eq2:
        raise AssertionError("pattern equations fail in direct arithmetic")
    valuations = []
    for v in values:
        if v % l:
            valuations.append(0)
        elif v % mod:
            valuations.append(1)
        else:
            valuations.append(2)
    if min(valuations) != 1:
        raise AssertionError(f"common valuation {min(valuations)} != 1")
    return {
        "b": list(b),
        "pattern": [1, e1, e2, e3, int(swap)],
        "values": [v % mod for v in values],
        "valuations": valuations,
    }


def class_witness(indices: list[list[int]], l: int) -> dict[str, object]:
    """First pattern (fixed e0 = +1 order) with a verified valuation-1 branch."""

    for swap in (False, True):
        for e1 in (1, -1):
            for e2 in (1, -1):
                for e3 in (1, -1):
                    b = kernel_witness(indices, l, e1, e2, e3, swap)
                    if not any(b):
                        continue
                    return verify_witness(
                        indices, l, b, e1, e2, e3, swap  # type: ignore[arg-type]
                    )
    raise AssertionError("no witness found: contradicts the cap theorem")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("primes", type=int, nargs="+")
    parser.add_argument("--json", type=str, default="")
    args = parser.parse_args()
    table = [c for c in load_table_classes() if not c["excluded"]]
    report: dict[str, dict] = {"minor_check": {}, "witnesses": {}}
    for c in table:
        minors, g, rank = minor_data(c["idx"])
        # The finite verification behind the theorem: no odd prime divides
        # all 3x3 minors, so the index matrix stays injective mod every
        # odd l.
        assert rank == 3, c["form"]
        assert g & (g - 1) == 0, (c["form"], g)
        report["minor_check"][c["form"]] = {
            "minors": minors,
            "gcd": g,
            "rank": rank,
        }
    for l in args.primes:
        report["witnesses"][str(l)] = {}
        for c in table:
            w = class_witness(c["idx"], l)
            report["witnesses"][str(l)][c["form"]] = w
        print(f"prime {l}: verified valuation-1 witnesses for all "
              f"{len(table)} classes")
    if args.json:
        Path(args.json).write_text(json.dumps(report, indent=2) + "\n")
        print(f"wrote {args.json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
