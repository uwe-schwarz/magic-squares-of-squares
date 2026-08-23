#!/usr/bin/env python3
"""Prime-power (l^2) torus rigidity check for the unresolved p^2 q r classes.

The rigidity lemma of rigidity.md works verbatim with Z[i]/l replaced by
Z[i]/l^2: every integer realization of a class with l not dividing 2 p q r
reduces to a solution of the coupled pattern equations on the norm-one torus
of Z[i]/l^2, and Im(z_c^2) = e^2 * Im(x_c) with e a unit, so the l-valuation
of an offset is the l-valuation of the imaginary part of its normalized
column.  If every torus solution modulo l^2 has all four imaginary parts
divisible by l^2, the class forces l^2 | d_c for all four offsets -- a
one-power upgrade of the mod-l statement.

Valuations are capped at 2 (the modulus cannot see beyond l^2).  Outcomes per
(class, l): min common valuation 0 (not rigid at l), 1 (l | d forced, no
l^2 upgrade: a valuation-1 branch exists), or 2 (l^2 | d forced).

Two independent code paths must agree counter-for-counter:

- brute: enumerate all triples of the squares subgroup U of the torus (the
  columns only depend on rho^2, sigma^2, tau^2), check all 16 fixed-e0
  sign/edge patterns directly, counting every (triple, pattern) match;
- linear: enumerate (rho^2, sigma^2) in U^2 only.  Each offset is affine in
  (u, v) = (Re tau^2, Im tau^2) because the r-row exponents lie in {-1,0,1}:
  Im(P (u+vi)) = b u + a v, Im(P (u-vi)) = b u - a v, Im(P) = b.  So each
  fixed-e0 pattern collapses to a 2x2 linear system mod l^2 solved for
  (u, v); the candidate is kept only if it is a square in the torus, and
  non-invertible systems fall back to enumerating tau^2 over U.  Solutions
  are recounted per (triple, pattern), so the two paths must find exactly
  the same multiset.
"""

from __future__ import annotations

import argparse
import json
import sys
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


def build_torus(l: int) -> list[Pair]:
    """All norm-one elements of Z[i]/l^2 (l odd), as coordinate pairs."""

    mod = l * l
    torus = [
        (a, b)
        for a in range(mod)
        for b in range(mod)
        if (a * a + b * b) % mod == 1 % mod
    ]
    expected = l * (l - 1 if l % 4 == 1 else l + 1)
    assert len(torus) == expected, (l, len(torus), expected)
    return torus


def squares_subgroup(torus: list[Pair], mod: int) -> list[Pair]:
    seen: dict[Pair, None] = {}
    for z in torus:
        seen.setdefault(gmul(z, z, mod), None)
    order = len(torus)
    assert len(seen) == order // 2, (order, len(seen))
    return list(seen)


def valuation(value: int, l: int, mod: int) -> int:
    """l-valuation capped at 2: 0, 1, or 2 (meaning divisible by l^2)."""

    if value % l:
        return 0
    if value % mod:
        return 1
    return 2


def pattern_match_count(v: list[int], l: int, mod: int) -> tuple[int, int]:
    """Matching fixed-e0 sign/edge patterns and best common valuation.

    The 16 patterns are (e1, e2, e3) in {+1,-1}^3 with e0 = +1 identified
    up to global sign, times the edge swap.  Pattern (e1, e2, e3, swap)
    matches when e2*se == v0 + e1*v1 and e3*de == v0 - e1*v1 (mod l^2) with
    (se, de) the swapped or unswapped edge pair.  The common valuation of a
    match is the minimum l-valuation over the four offsets; the return is
    (match count, minimum common valuation, or 3 if no match).
    """

    matches = 0
    best = 3
    for swap in (0, 1):
        se, de = (v[3], v[2]) if swap else (v[2], v[3])
        s1 = (v[0] + v[1]) % mod
        d1 = (v[0] - v[1]) % mod
        ms = (se == s1) + (se == (-s1) % mod)
        md = (de == d1) + (de == (-d1) % mod)
        ms2 = (se == d1) + (se == (-d1) % mod)
        md2 = (de == s1) + (de == (-s1) % mod)
        matches += ms * md + ms2 * md2
        if ms * md or ms2 * md2:
            common = min(valuation(x, l, mod) for x in (v[0], v[1], se, de))
            best = min(best, common)
    return matches, best


def powers5(u: Pair, mod: int) -> list[Pair]:
    """u^j for j in -2..2 (p-row: rho^(2 j) = (rho^2)^j)."""

    ui = ginv(u, mod)
    ui2 = gmul(ui, ui, mod)
    u2 = gmul(u, u, mod)
    return [ui2, ui, (1, 0), u, u2]


def powers3(u: Pair, mod: int) -> list[Pair]:
    """u^j for j in -1..1 (q- and r-rows)."""

    return [ginv(u, mod), (1, 0), u]


def column_triples(indices: list[list[int]]) -> list[tuple[int, int, int]]:
    """Per-column (j_p, j_q, j_r) exponent triples."""

    return [
        (indices[0][c], indices[1][c], indices[2][c]) for c in range(4)
    ]


def scan_brute(indices: list[list[int]], l: int) -> dict[str, int]:
    """Exhaustive U^3 enumeration with direct pattern checks."""

    mod = l * l
    torus = build_torus(l)
    group = squares_subgroup(torus, mod)
    p5 = [powers5(u, mod) for u in group]
    q3 = [powers3(u, mod) for u in group]
    columns = column_triples(indices)
    matches = 0
    best = 3
    for ip in range(len(group)):
        pcol = [p5[ip][columns[c][0] + 2] for c in range(4)]
        for iq in range(len(group)):
            scol = [gmul(pcol[c], q3[iq][columns[c][1] + 1], mod) for c in range(4)]
            for it in range(len(group)):
                tc = q3[it]
                v = [
                    gmul(scol[c], tc[columns[c][2] + 1], mod)[1]
                    for c in range(4)
                ]
                m, b = pattern_match_count(v, l, mod)
                matches += m
                if b < best:
                    best = b
    return {"matches": matches, "min_common_v": best, "group": len(group)}


def scan_linear(indices: list[list[int]], l: int) -> dict[str, int]:
    """(rho^2, sigma^2) enumeration with the tau^2 row solved linearly."""

    mod = l * l
    torus = build_torus(l)
    group = squares_subgroup(torus, mod)
    square_set = set(group)
    p5 = [powers5(u, mod) for u in group]
    q3 = [powers3(u, mod) for u in group]
    columns = column_triples(indices)
    matches = 0
    best = 3
    fallbacks = 0
    for ip in range(len(group)):
        pcol = [p5[ip][columns[c][0] + 2] for c in range(4)]
        for iq in range(len(group)):
            scol = [gmul(pcol[c], q3[iq][columns[c][1] + 1], mod) for c in range(4)]
            for swap in (0, 1):
                se_col, de_col = (3, 2) if swap else (2, 3)
                for e1 in (1, -1):
                    for e2 in (1, -1):
                        for e3 in (1, -1):
                            # Eq1: e2*v[se_col] - v[0] - e1*v[1] == 0
                            # Eq2: e3*v[de_col] - v[0] + e1*v[1] == 0
                            # v_c = ucoef*u + vcoef*v + const with
                            # ucoef = b if jr != 0 else 0,
                            # vcoef = jr * a, const = b if jr == 0 else 0.
                            a1 = b1 = c1 = 0
                            a2 = b2 = c2 = 0
                            for c, kappa1, kappa2 in (
                                (0, -1, -1),
                                (1, -e1, e1),
                                (se_col, e2, 0),
                                (de_col, 0, e3),
                            ):
                                a, b = scol[c]
                                jr = columns[c][2]
                                uc = b if jr else 0
                                vc = jr * a
                                cst = b if not jr else 0
                                a1 += kappa1 * uc
                                b1 += kappa1 * vc
                                c1 += kappa1 * cst
                                a2 += kappa2 * uc
                                b2 += kappa2 * vc
                                c2 += kappa2 * cst
                            det = (a1 * b2 - a2 * b1) % mod
                            if det % l:
                                inv = pow(det, -1, mod)
                                u = (-(c1 * b2 - c2 * b1) * inv) % mod
                                v = (-(a1 * c2 - a2 * c1) * inv) % mod
                                candidates: list[Pair] = [(u, v)]
                            else:
                                fallbacks += 1
                                candidates = group
                            for u, v in candidates:
                                if (u, v) not in square_set:
                                    continue
                                w = (u, v)
                                wi = ginv(w, mod)
                                tc = (wi, (1, 0), w)
                                vvals = [
                                    gmul(scol[c], tc[columns[c][2] + 1], mod)[1]
                                    for c in range(4)
                                ]
                                ok1 = (
                                    e2 * vvals[se_col]
                                    - vvals[0]
                                    - e1 * vvals[1]
                                ) % mod == 0
                                ok2 = (
                                    e3 * vvals[de_col]
                                    - vvals[0]
                                    + e1 * vvals[1]
                                ) % mod == 0
                                if not (ok1 and ok2):
                                    continue
                                matches += 1
                                common = min(
                                    valuation(x, l, mod) for x in vvals
                                )
                                if common < best:
                                    best = common
    return {
        "matches": matches,
        "min_common_v": best,
        "group": len(group),
        "fallbacks": fallbacks,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("primes", type=int, nargs="+")
    parser.add_argument("--all-classes", action="store_true")
    parser.add_argument("--linear-only", action="store_true")
    parser.add_argument("--json", type=str, default="")
    args = parser.parse_args()
    table = [
        c for c in load_table_classes() if args.all_classes or not c["excluded"]
    ]
    report: dict[str, dict] = {}
    for l in args.primes:
        print(f"prime {l} (modulus {l * l})")
        sys.stdout.flush()
        report[str(l)] = {}
        for c in table:
            linear = scan_linear(c["idx"], l)
            entry = dict(linear)
            if not args.linear_only:
                brute = scan_brute(c["idx"], l)
                assert brute["matches"] == linear["matches"], (
                    c["form"],
                    l,
                    brute["matches"],
                    linear["matches"],
                )
                assert brute["min_common_v"] == linear["min_common_v"], (
                    c["form"],
                    l,
                )
            forced = linear["min_common_v"]
            tag = {
                0: "solvable mod l",
                1: "l | d forced, valuation-1 branch exists",
                2: "RIGID AT l^2 (l^2 | d forced)",
            }[forced]
            entry["forced_v"] = forced
            entry["role"] = c["role"]
            report[str(l)][c["form"]] = entry
            print(
                f"  {c['form']} ({c['role']}): {tag} "
                f"[matches={linear['matches']}, fallbacks={linear['fallbacks']}]"
            )
            sys.stdout.flush()
    if args.json:
        Path(args.json).write_text(json.dumps(report, indent=2) + "\n")
        print(f"wrote {args.json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
