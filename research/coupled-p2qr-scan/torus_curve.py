#!/usr/bin/env python3
"""The coupled curves: pattern equations as algebraic curves in slopes.

Correspondence (the reason these curves exist).  Fix one of the sixteen
surviving classes with local-index matrix j and a fixed-e0 sign/edge
pattern.  Parametrize each norm-one generator quotient rho = pi/conj(pi)
by the rational slope of pi itself:

    rho(t) = (1 + i t) / (1 - i t),   t = Im(pi)/Re(pi) in Q.

Every rational slope is realized by a Gaussian integer, and every
Gaussian integer gives a rational slope; the parametrization is exact in
Q(i).  The normalized column x_c = rho^(2 j_p) sigma^(2 j_q) tau^(2 j_r)
is then a point of Q(i) for rational slopes, and the two pattern
equations

    e2*Im(x_se) - Im(x_0) - e1*Im(x_1) = 0,
    e3*Im(x_de) - Im(x_0) + e1*Im(x_1) = 0

are two polynomial equations in (t1, t2, t3) after clearing the (never
rational-vanishing) denominators (1 + t^2).  Their common-zero locus is
an algebraic curve C; eliminating t3 by the resultant gives a plane curve
F(t1, t2) whose rational points carry every rational solution.

Why this matters: the monomial identity d_c = |Im(z_c^2)| in S_e with
e = N(pi)^2 N(beta) N(gamma) needs NO primality.  A non-degenerate
rational point of C (some Im(x_c) nonzero) gives, via any Gaussian
integer realization of the slopes, four offsets with e^2 +- d_c squares
and the pattern relation -- a 3x3 magic square of squares with center
root of p^2 q r shape, N(pi), N(beta), N(gamma) arbitrary.  Conversely
every genuine solution with PRIME support p, q, r lands on one of the
sixteen curves by the committed switching-class classification.  Hence:

    if all sixteen curves have only degenerate rational points
    (all four Im(x_c) = 0), then no magic square of squares with
    prime-support center root p^2 q r exists, of any size.

Degenerate rational points do exist: t = 0 gives rho = 1 (pi real), and
the all-real locus collapses every Im(x_c) to 0 -- the trivial square
with all entries equal.  The committed scans (p, q, r <= 2*10^4, zero
events) show no non-degenerate point with prime slopes in that box.

This module builds the curves exactly (sympy), factors the resultant,
and provides the correspondence checks used by the tests: rational slope
triples satisfying the pattern in Q(i) must land on every irreducible
component's product F, and partially degenerate points (some Im = 0)
found by exhaustive search give positive test vectors.
"""

from __future__ import annotations

import argparse
import json
import sys
from itertools import product as iproduct
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from test_coupled_p2qr_scan import load_table_classes  # noqa: E402

T1, T2, T3 = sp.symbols("t1 t2 t3", rational=True)


def _cmul(p, q):
    return (
        sp.expand(p[0] * q[0] - p[1] * q[1]),
        sp.expand(p[0] * q[1] + p[1] * q[0]),
    )


def _unit_factor(t, exponent: int):
    """(1 + i t)^e (1 - i t)^(-e) as a fraction of Gaussian polynomials."""

    num, den = (1, 0), (1, 0)
    for _ in range(abs(exponent)):
        if exponent > 0:
            num = _cmul(num, (1, t))
            den = _cmul(den, (1, -t))
        else:
            num = _cmul(num, (1, -t))
            den = _cmul(den, (1, t))
    return num, den


def normalized_column_real_imag(
    indices: list[list[int]], column: int, ts=(T1, T2, T3)
):
    """(Re, Im) of x_c = prod_s rho_s^(2 j[s,c]) over a common denominator.

    Returns (numerator pair, denominator pair); the value is num/den with
    den a product of powers of (1 +- i t), nonzero at every rational t.
    """

    num, den = (1, 0), (1, 0)
    for s in range(3):
        num_f, den_f = _unit_factor(ts[s], 2 * indices[s][column])
        num = _cmul(num, num_f)
        den = _cmul(den, den_f)
    return num, den


def pattern_equations(
    indices: list[list[int]],
    e1: int,
    e2: int,
    e3: int,
    swap: bool,
):
    """The two pattern equations as polynomials in (t1, t2, t3).

    Im(x_c) * common positive denominator, so the rational zero set of
    each polynomial is exactly the rational zero set of Im(x_c) (the
    denominators (1 + t^2) never vanish at rational t).
    """

    se, de = (3, 2) if swap else (2, 3)
    ims = []
    for c in range(4):
        num, den = normalized_column_real_imag(indices, c)
        conj_den = (den[0], -den[1])
        prod = _cmul(num, conj_den)
        ims.append(sp.expand(prod[1]))
    eq1 = sp.expand(e2 * ims[se] - ims[0] - e1 * ims[1])
    eq2 = sp.expand(e3 * ims[de] - ims[0] + e1 * ims[1])
    return eq1, eq2


def plane_curve(
    indices: list[list[int]],
    e1: int,
    e2: int,
    e3: int,
    swap: bool,
):
    """Eliminated plane curve F(t1, t2) (factored, with multiplicities)."""

    eq1, eq2 = pattern_equations(indices, e1, e2, e3, swap)
    res = sp.resultant(sp.Poly(eq1, T3), sp.Poly(eq2, T3))
    return sp.factor(res.as_expr())


def component_degrees(F) -> list[int]:
    """Total degrees of the irreducible factors of F (with multiplicity)."""

    _, factors = sp.factor_list(F)
    return sorted(
        sp.Poly(f, T1, T2).total_degree() for f, _ in factors
    )


def slopes_to_pattern_residuals(
    indices: list[list[int]],
    tvals,
    e1: int,
    e2: int,
    e3: int,
    swap: bool,
):
    """Exact Q(i) residuals of the pattern equations at a slope triple.

    tvals are rationals (int, Fraction, or sympy Rational).  Returns
    (r1, r2) as fractions.Fraction: the Im-based residuals of the two
    pattern equations, zero exactly when the pattern holds.
    """

    from fractions import Fraction

    def to_fraction(t):
        if isinstance(t, Fraction):
            return t
        if isinstance(t, int):
            return Fraction(t)
        r = sp.Rational(t)
        return Fraction(int(r.p), int(r.q))

    tv = [to_fraction(t) for t in tvals]

    def cmul(p, q):
        return (p[0] * q[0] - p[1] * q[1], p[0] * q[1] + p[1] * q[0])

    def cpow_inv(p, n):  # p^(-n)
        # inverse in Q(i)
        norm = p[0] * p[0] + p[1] * p[1]
        conj = (p[0], -p[1])
        inv = (conj[0] / norm, conj[1] / norm)
        out = (Fraction(1), Fraction(0))
        for _ in range(n):
            out = cmul(out, inv)
        return out

    units = []
    for t in tv:
        # rho(t) = (1 + it)/(1 - it) as a Q(i) point
        num = (Fraction(1), t)
        den = (Fraction(1), -t)
        norm = den[0] * den[0] + den[1] * den[1]
        conj = (den[0], -den[1])
        units.append((conj[0] / norm, conj[1] / norm))

    ims = []
    for c in range(4):
        x = (Fraction(1), Fraction(0))
        for s in range(3):
            e = 2 * indices[s][c]
            if e > 0:
                for _ in range(e):
                    x = cmul(x, units[s])
            elif e < 0:
                x = cmul(x, cpow_inv(units[s], -e))
        ims.append(x[1])
    se, de = (3, 2) if swap else (2, 3)
    r1 = e2 * ims[se] - ims[0] - e1 * ims[1]
    r2 = e3 * ims[de] - ims[0] + e1 * ims[1]
    return r1, r2


def search_pattern_solutions(
    indices: list[list[int]],
    bound: int = 6,
):
    """Exhaustive small-height slope search for pattern solutions.

    Enumerates t_i = b/a with 0 <= b <= |a| <= bound (plus the t = 0
    degenerate line) and every pattern; returns hits with their
    degeneracy status (which Im(x_c) vanish).  Used to produce positive
    test vectors for the curve correspondence, not as a search for magic
    squares (non-degenerate hits at composite norms WOULD be magic
    squares of squares -- none are expected, and none below this bound
    can exist anyway by the committed exhaustive scans).
    """

    slopes = []
    for a in range(1, bound + 1):
        for b in range(0, a + 1):
            from math import gcd

            if gcd(a, b) == 1:
                slopes.append(sp.Rational(b, a))
    hits = []
    for tvals in iproduct(slopes, repeat=3):
        for swap in (False, True):
            for e1 in (1, -1):
                for e2 in (1, -1):
                    for e3 in (1, -1):
                        r1, r2 = slopes_to_pattern_residuals(
                            indices, tvals, e1, e2, e3, swap
                        )
                        if r1 == 0 and r2 == 0:
                            hits.append(
                                {
                                    "slopes": [str(t) for t in tvals],
                                    "pattern": [1, e1, e2, e3, int(swap)],
                                }
                            )
    return hits


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--classes", type=str, default="",
                        help="comma-separated class forms (default: all 16)")
    parser.add_argument("--json", type=str, default="")
    args = parser.parse_args()
    table = [c for c in load_table_classes() if not c["excluded"]]
    if args.classes:
        wanted = set(args.classes.split(","))
        table = [c for c in table if c["form"] in wanted]
    report: dict = {}
    for c in table:
        degs: dict[str, list[int]] = {}
        for swap in (False, True):
            for e1 in (1, -1):
                for e2 in (1, -1):
                    for e3 in (1, -1):
                        F = plane_curve(c["idx"], e1, e2, e3, swap)
                        key = f"e=({e1},{e2},{e3}),swap={int(swap)}"
                        degs[key] = component_degrees(F)
        report[c["form"]] = {"role": c["role"], "degrees": degs}
        sizes = sorted({tuple(v) for v in degs.values()})
        print(f"{c['form']} ({c['role']}): degree tables {sizes}", flush=True)
    if args.json:
        Path(args.json).write_text(json.dumps(report, indent=2) + "\n")
        print(f"wrote {args.json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
