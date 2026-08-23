#!/usr/bin/env python3
"""Argument-height search: rational slope triples over all 16 classes.

The coupled-curve correspondence (torus_curve.py) makes the pattern
equations depend ONLY on the generator arguments: rho = pi/conj(pi) has
slope t = Im(pi)/Re(pi), and every scaling pi -> k*pi leaves the pattern
untouched while freely growing the entries.  A non-degenerate rational
slope triple (some Im(x_c) nonzero) therefore yields, for every scaling,
a 3x3 magic square of squares -- a counterexample to the open problem.
Conversely the committed scans bounded the norms, never the arguments,
so this is a genuinely new search axis.

The search enumerates t = b/a in lowest terms with 0 <= b <= a <= bound
(the remaining quadrants and signs are covered by the class set being
closed under per-generator conjugation and unit rotation), and for each
slope triple checks all 16 fixed-e0 patterns of all 16 classes in exact
Fraction arithmetic.  Hits are classified degenerate (all four Im zero)
or not; any non-degenerate hit must immediately be re-verified with
research/prime-power-rigidity/targeted_reconstruction.py and triple
checked before being called a magic square.

Hit classification.  A hit with exactly one zero offset is the classical
three-distinct-value family (the proved degenerate dichotomy of the
multimagie lineage: a non-distinct square has 1 or 3 distinct values);
these are counted and sampled but are not candidates.  A hit with all
four offsets nonzero is a CANDIDATE: the script immediately re-embeds
the primitive generators and runs the exact verify_candidate of
targeted_reconstruction.py (coupled relations, e^2 +- d squares,
positivity, nine-fold distinctness).  A passing candidate is a
counterexample to the open problem and must be triple-checked before
any claim.

Complementarity note: an empty candidate set at height H says no magic
square exists whose generators can be scaled to argument height <= H in
this 16-class monomial model; it does not bound composite-norm
configurations outside the model.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from fractions import Fraction
from itertools import product as iproduct
from math import gcd
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from test_coupled_p2qr_scan import load_table_classes  # noqa: E402


def cmul(p, q):
    return (p[0] * q[0] - p[1] * q[1], p[0] * q[1] + p[1] * q[0])


def unit(t: Fraction):
    """rho(t) = (1 + it)/(1 - it) in Q(i)."""

    num = (Fraction(1), t)
    den = (Fraction(1), -t)
    n = den[0] * den[0] + den[1] * den[1]
    return (num[0] / n, num[1] / n)


def unit_pows(t: Fraction):
    """rho(t)^e for e in -4..4 (all even exponents the classes need)."""

    u = unit(t)
    inv = (u[0], -u[1])  # norm one
    out = {}
    acc = (Fraction(1), Fraction(0))
    for e in range(0, 5):
        out[e] = acc
        out[-e] = (acc[0], -acc[1])
        acc = cmul(acc, u)
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bound", type=int, default=12)
    parser.add_argument("--json", type=str, default="")
    args = parser.parse_args()

    table = [c for c in load_table_classes() if not c["excluded"]]
    slopes = sorted(
        {
            Fraction(b, a)
            for a in range(1, args.bound + 1)
            for b in range(0, a + 1)
            if gcd(a, b) == 1
        }
    )
    print(f"{len(slopes)} slopes up to bound {args.bound}", flush=True)
    patterns = [
        (e1, e2, e3, swap)
        for swap in (False, True)
        for e1 in (1, -1)
        for e2 in (1, -1)
        for e3 in (1, -1)
    ]
    three_value: list[dict] = []
    candidates: list[dict] = []
    degenerate = 0
    started = time.time()

    def verify_candidate_record(record: dict) -> dict:
        import re as _re

        sys.path.insert(
            0, str(HERE.parent / "prime-power-rigidity")
        )
        from targeted_reconstruction import (
            exact_offsets,
            verify_candidate,
        )

        def gen_from_slope(ts: str):
            frac = Fraction(ts)
            return (frac.denominator, frac.numerator)

        cls = next(
            cc
            for cc in load_table_classes()
            if cc["form"] == record["form"]
        )
        gens = tuple(gen_from_slope(ts) for ts in record["slopes"])
        d = exact_offsets(cls["idx"], gens)
        v = verify_candidate(cls["idx"], gens)
        return {
            "offsets": list(d),
            "coupled": v.coupled,
            "squares": v.square_embeddings,
            "positive": v.positive,
            "distinct": v.distinct,
        }
    triples = 0
    for t1 in slopes:
        p1 = unit_pows(t1)
        for t2 in slopes:
            p2 = unit_pows(t2)
            for t3 in slopes:
                p3 = unit_pows(t3)
                triples += 1
                for c in table:
                    idx = c["idx"]
                    im = []
                    for col in range(4):
                        z = cmul(
                            cmul(
                                p1[2 * idx[0][col]],
                                p2[2 * idx[1][col]],
                            ),
                            p3[2 * idx[2][col]],
                        )
                        im.append(z[1])
                    if all(v == 0 for v in im):
                        # fully degenerate: the trivial all-equal square
                        degenerate += 1
                        continue
                    for e1, e2, e3, swap in patterns:
                        se, de = (3, 2) if swap else (2, 3)
                        if (
                            e2 * im[se] - im[0] - e1 * im[1] == 0
                            and e3 * im[de] - im[0] + e1 * im[1] == 0
                        ):
                            zeros = sum(1 for v in im if v == 0)
                            record = {
                                "form": c["form"],
                                "role": c["role"],
                                "slopes": [str(t1), str(t2), str(t3)],
                                "pattern": [1, e1, e2, e3, int(swap)],
                                "ims": [str(v) for v in im],
                            }
                            if zeros == 1:
                                # classical three-distinct-value family
                                three_value.append(record)
                                continue
                            candidates.append(record)
                            print(
                                "CANDIDATE (all offsets nonzero):",
                                record,
                                flush=True,
                            )
                            verdict = verify_candidate_record(record)
                            print("  verify_candidate:", verdict, flush=True)
        print(
            f"t1={t1}: {triples} triples done, "
            f"{len(candidates)} candidates, {len(three_value)} three-value,"
            f" {time.time() - started:.0f}s",
            flush=True,
        )
    report = {
        "bound": args.bound,
        "slopes": len(slopes),
        "triples": triples,
        "classes": len(table),
        "three_value_count": len(three_value),
        "three_value_samples": three_value[:20],
        "candidates": candidates,
        "degenerate_class_triples": degenerate,
        "seconds": round(time.time() - started, 1),
    }
    tag = (
        "NONE"
        if not candidates
        else f"{len(candidates)} -- VERIFICATION OUTPUT ABOVE"
    )
    print(
        f"bound {args.bound}: candidates (all offsets nonzero): {tag}; "
        f"three-value degenerate family: {len(three_value)}"
    )
    if args.json:
        Path(args.json).write_text(json.dumps(report, indent=2) + "\n")
        print(f"wrote {args.json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
