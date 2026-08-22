#!/usr/bin/env python3
"""Independent torus-parametrized modular rigidity check.

For a p^2 q r class with local index matrix j, the four offsets satisfy
d_c = e^2 * |Im(x_c)| with x_c = rho^(2 j_p,c) sigma^(2 j_q,c) tau^(2 j_r,c)
on the norm-one torus of Z[i]/l.  The two additive offset relations with
free column signs reduce to sign equations among v_c = Im(x_c).

This implementation parametrizes the torus directly (rho = (t, 1/t) in the
split case, norm-one subgroup of F_l^2 in the inert case), which is an
independent code path from the Gaussian-unit enumeration in
modular_obstruction.cpp and much faster: |T|^3 instead of |units|^3.

A class with no non-degenerate solution at l forces l | d_c for all four
offsets in any integer realization with l not dividing 2 p q r.
"""

from __future__ import annotations

import argparse
import sys
from itertools import product as iproduct
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from test_coupled_p2qr_scan import load_table_classes  # noqa: E402


def torus_elements(mod: int) -> list[tuple[int, int]]:
    """Norm-one elements a+bi of Z[i]/mod as coordinate pairs."""

    if mod == 2:
        return [(1, 0)]
    if mod % 4 == 1:
        # Split: torus = {(t, t^{-1})} under (a+bi) <-> (a+bi, a-bi) with
        # i = sqrt(-1) in F_mod.  Parametrize by t and realize rho = (t,1/t)
        # as the pair over the two-component encoding: we work directly
        # with t and record Im via t - t^{-1}.
        return [("split", t) for t in range(1, mod)]  # type: ignore
    out = []
    for a in range(mod):
        for b in range(mod):
            if (a * a + b * b) % mod == 1 % mod:
                out.append((a, b))
    return out


def check_class(mod: int, indices: list[list[int]]) -> dict[str, object]:
    """Exhaustively decide non-degenerate solvability on the torus."""

    columns = [
        (indices[0][c], indices[1][c], indices[2][c]) for c in range(4)
    ]
    if mod % 4 == 1:
        ts = list(range(1, mod))
        inv = {t: pow(t, mod - 2, mod) for t in ts}
        two_i_inv = pow(2 * _sqrt_m1(mod), mod - 2, mod)

        def values(tp, tq, tr):
            out = []
            for jp, jq, jr in columns:
                w = (
                    pow(tp, 2 * jp, mod)
                    * pow(tq, 2 * jq, mod)
                    * pow(tr, 2 * jr, mod)
                ) % mod
                im = (w - inv[w]) % mod * two_i_inv % mod
                out.append(im)
            return out

        count = len(ts) ** 3
        for tp, tq, tr in iproduct(ts, repeat=3):
            v = values(tp, tq, tr)
            if all(x == 0 for x in v):
                continue
            if _pattern_ok(v, mod):
                return {"solvable": True, "torus_points": count}
        return {"solvable": False, "torus_points": count}

    tor = torus_elements(mod)

    def conj(z):
        return (z[0], -z[1] % mod)

    def gmul(z, w):
        return (
            (z[0] * w[0] - z[1] * w[1]) % mod,
            (z[0] * w[1] + z[1] * w[0]) % mod,
        )

    def ginv(z):
        # z^{-1} = conj(z) / N(z), valid in the field Z[i]/mod.
        n = (z[0] * z[0] + z[1] * z[1]) % mod
        ni = pow(n, mod - 2, mod)
        return ((z[0] * ni) % mod, ((-z[1]) * ni) % mod)

    def gpow(z, n):
        if n < 0:
            return gpow(ginv(z), -n)
        r = (1, 0)
        b = z
        e = n
        while e > 0:
            if e & 1:
                r = gmul(r, b)
            b = gmul(b, b)
            e >>= 1
        return r

    count = len(tor) ** 3
    for rho, sig, tau in iproduct(tor, repeat=3):
        v = []
        for jp, jq, jr in columns:
            x = gmul(
                gmul(gpow(rho, 2 * jp), gpow(sig, 2 * jq)),
                gpow(tau, 2 * jr),
            )
            # x = A + B i with Im(x) = B, the second coordinate.
            v.append(x[1] % mod)
        if all(t == 0 for t in v):
            continue
        if _pattern_ok(v, mod):
            return {"solvable": True, "torus_points": count}
    return {"solvable": False, "torus_points": count}


def _pattern_ok(v: list[int], mod: int) -> bool:
    for swap in (0, 1):
        se, de = (v[3], v[2]) if swap else (v[2], v[3])
        for e0, e1, e2, e3 in iproduct((1, -1), repeat=4):
            if (
                (e2 * se - (e0 * v[0] + e1 * v[1])) % mod == 0
                and (e3 * de - (e0 * v[0] - e1 * v[1])) % mod == 0
            ):
                return True
    return False


def _sqrt_m1(mod: int) -> int:
    for x in range(2, mod):
        if x * x % mod == mod - 1:
            return x
    raise AssertionError(mod)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("moduli", type=int, nargs="+")
    parser.add_argument("--all-classes", action="store_true")
    args = parser.parse_args()
    table = [c for c in load_table_classes() if args.all_classes or not c["excluded"]]
    for mod in args.moduli:
        print(f"modulus {mod}")
        for c in table:
            result = check_class(mod, c["idx"])
            tag = "solvable" if result["solvable"] else "ONLY DEGENERATE"
            print(
                f"  {c['form']} ({c['role']}): {tag}"
                f" [torus^3 = {result['torus_points']}]"
            )
        sys.stdout.flush()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
