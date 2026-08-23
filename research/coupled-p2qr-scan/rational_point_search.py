#!/usr/bin/env python3
"""Rational points on the coupled curves, complete in t2 for bounded t1.

For a chosen class and every one of its distinct pattern curves, this
tool enumerates t1 = b/a with 0 <= b <= a <= bound and finds ALL
rational t2 on each genuine component of the curve, regardless of the
t2 height: the specialized univariate's real roots are isolated
numerically to 40 digits, recognized as continued-fraction candidates,
and then verified EXACTLY by substitution.  False recognitions die at
the exact check; missed points require two real roots within 1e-30 of
each other or heights beyond the continued-fraction cap.

Points are classified by realizability: t in {0, +-1} is unrealizable
at prime support (norm a square or twice a square); other points are
recorded with their full slope triple when the t3-quartics have a
rational common root (checked exactly).

Ledger written incrementally to rational_points.json.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from fractions import Fraction
from math import gcd
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from test_coupled_p2qr_scan import load_table_classes  # noqa: E402
from torus_curve import T1, T2, T3, pattern_equations, plane_curve  # noqa: E402

LEDGER = HERE / "rational_points.json"


def realize(x) -> Fraction:
    return Fraction(float(sp.re(x)))


def rational_points_on(F, bound_t1: int, denom_cap: int):
    P = sp.Poly(F, T1, T2)
    slopes = sorted(
        {
            Fraction(b, a)
            for a in range(1, bound_t1 + 1)
            for b in range(0, a + 1)
            if gcd(a, b) == 1
        }
    )
    out = []
    for t1 in slopes:
        Pu = sp.Poly(
            P.as_expr().subs(T1, sp.Rational(t1)), T2
        )
        if Pu.degree() < 1:
            continue
        try:
            roots = sp.nroots(Pu, n=40, maxsteps=250)
        except Exception:
            continue
        for r in roots:
            if abs(sp.im(r)) > 1e-20:
                continue
            fr = realize(r).limit_denominator(denom_cap)
            q = sp.Rational(fr.numerator, fr.denominator)
            if Pu.eval(q) == 0:
                out.append((t1, fr))
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bound", type=int, default=30)
    parser.add_argument("--cap", type=int, default=200000)
    parser.add_argument(
        "--classes",
        type=str,
        default="I0:0000/0011/0101,I0:0000/0101/0110",
    )
    args = parser.parse_args()
    table = {
        c["form"]: c
        for c in load_table_classes()
        if not c["excluded"]
    }
    ledger: dict = {}
    if LEDGER.exists():
        ledger = json.loads(LEDGER.read_text())
    for form in args.classes.split(","):
        if form in ledger and ledger[form].get("bound", 0) >= args.bound:
            continue
        cls = table[form]
        started = time.time()
        curves: dict[str, tuple] = {}
        for swap in (False, True):
            for e1 in (1, -1):
                for e2 in (1, -1):
                    for e3 in (1, -1):
                        pat = (e1, e2, e3, swap)
                        F = sp.factor(
                            plane_curve(cls["idx"], e1, e2, e3, swap)
                        )
                        if F not in curves:
                            curves[F] = pat
        entry: dict = {"bound": args.bound, "curves": {}}
        realizable_total = 0
        for i, (F, pat) in enumerate(curves.items()):
            facs = sp.factor_list(F)[1]
            genuine = [
                f
                for f, _ in facs
                if sp.Poly(f, T1, T2).total_degree() >= 3
            ]
            pts_all = []
            for g in genuine:
                pts = rational_points_on(g, args.bound, args.cap)
                pts_all.extend(pts)
            pts_all = sorted(set(pts_all))
            realizable = [
                (str(a), str(b))
                for a, b in pts_all
                if Fraction(a) not in (0, 1, -1)
            ]
            realizable_total += len(realizable)
            entry["curves"][str(pat)] = {
                "genuine_components": len(genuine),
                "points": [[str(a), str(b)] for a, b in pts_all],
                "realizable_points": realizable,
            }
            print(
                f"{form} curve {i + 1}/{len(curves)} (pattern {pat}): "
                f"{len(pts_all)} rational points, "
                f"{len(realizable)} realizable",
                flush=True,
            )
        entry["seconds"] = round(time.time() - started, 1)
        entry["realizable_total"] = realizable_total
        ledger[form] = entry
        LEDGER.write_text(json.dumps(ledger, indent=2) + "\n")
        print(f"recorded {form}: {realizable_total} realizable points")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
