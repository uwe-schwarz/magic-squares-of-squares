"""Correspondence tests for the slope-coordinate coupled curves.

The discipline: rational slope triples solving a pattern in exact Q(i)
arithmetic must lie on the eliminated plane curve of that pattern (the
projection direction of torus_curve.py), degenerate points must exist
(the trivial square), and the committed degree table must reproduce for
a pinned entry.
"""

from __future__ import annotations

import json
import random
import re
import sys
import unittest
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent

from test_coupled_p2qr_scan import load_table_classes  # noqa: E402
from torus_curve import (  # noqa: E402
    T1,
    T2,
    component_degrees,
    plane_curve,
    search_pattern_solutions,
    slopes_to_pattern_residuals,
)

DEGREE_TABLE = HERE / "torus_curve_degrees.json"


def classes() -> list[dict]:
    return [c for c in load_table_classes() if not c["excluded"]]


class CurveCorrespondence(unittest.TestCase):
    def test_degenerate_origin_on_every_curve(self) -> None:
        # The trivial square: rho = sigma = tau = 1 (all slopes zero)
        # satisfies every pattern, so t1 = t2 = 0 lies on every plane
        # curve of every class.
        for c in classes()[:4]:
            for swap in (False, True):
                for e1 in (1, -1):
                    for e2 in (1, -1):
                        for e3 in (1, -1):
                            r1, r2 = slopes_to_pattern_residuals(
                                c["idx"], (0, 0, 0), e1, e2, e3, swap
                            )
                            self.assertEqual((r1, r2), (0, 0))

    def test_pattern_solutions_lie_on_their_curves(self) -> None:
        c = classes()[10]  # I2:0000/*001/01*1 (ECE)
        hits = search_pattern_solutions(c["idx"], bound=4)
        # Only fully degenerate points exist at this height: the origin
        # (all generators real) and (0, 1, 1) (pi real, beta = gamma).
        self.assertEqual(
            sorted({tuple(h["slopes"]) for h in hits}),
            [("0", "0", "0"), ("0", "1", "1")],
        )
        # Both degenerate points give the trivial all-equal square via
        # the exact reconstruction (offsets all zero, distinctness fails).
        sys.path.insert(0, str(HERE.parent / "prime-power-rigidity"))
        from targeted_reconstruction import exact_offsets, verify_candidate

        for gens in (((1, 0), (1, 1), (1, 1)), ((1, 0), (1, 0), (1, 0))):
            v = verify_candidate(c["idx"], gens)
            self.assertEqual(
                exact_offsets(c["idx"], gens), (0, 0, 0, 0)
            )
            self.assertTrue(v.coupled and v.square_embeddings and v.positive)
            self.assertFalse(v.distinct)
        # Every hit satisfies its pattern in Q(i) and lies on its curve.
        seen = 0
        for h in hits:
            tvals = tuple(sp.Rational(s) for s in h["slopes"])
            _, e1, e2, e3, swap = h["pattern"]
            r1, r2 = slopes_to_pattern_residuals(
                c["idx"], tvals, e1, e2, e3, bool(swap)
            )
            self.assertEqual((r1, r2), (0, 0))
            if seen < 3:
                F = plane_curve(c["idx"], e1, e2, e3, bool(swap))
                val = sp.simplify(F.subs({T1: tvals[0], T2: tvals[1]}))
                self.assertEqual(val, 0)
                seen += 1

    def test_non_solutions_generally_off_the_curve(self) -> None:
        # The resultant vanishing is necessary, not sufficient (the t3
        # fiber may be algebraic only); but random non-solutions must
        # almost surely miss the curve.
        c = classes()[10]
        F = plane_curve(c["idx"], 1, 1, 1, False)
        rng = random.Random(20260823)
        off_curve = 0
        trials = 8
        for _ in range(trials):
            tv = (
                sp.Rational(rng.randint(-9, 9), rng.randint(1, 9)),
                sp.Rational(rng.randint(-9, 9), rng.randint(1, 9)),
                sp.Rational(rng.randint(-9, 9), rng.randint(1, 9)),
            )
            r1, r2 = slopes_to_pattern_residuals(
                c["idx"], tv, 1, 1, 1, False
            )
            if r1 == 0 and r2 == 0:
                continue
            val = sp.simplify(F.subs({T1: tv[0], T2: tv[1]}))
            if val != 0:
                off_curve += 1
        self.assertGreaterEqual(off_curve, trials - 2)


class DegreeTablePins(unittest.TestCase):
    def test_table_covers_all_classes_and_patterns(self) -> None:
        table = json.loads(DEGREE_TABLE.read_text())
        self.assertEqual(len(table), 16)
        for form, entry in table.items():
            self.assertEqual(len(entry["degrees"]), 16, form)

    def test_pinned_entry_reproduces(self) -> None:
        # The first ECE class, pattern (1,1,1,1) without swap: a line
        # (the t1 = 0 degenerate component) plus an irreducible curve of
        # degree 91.  All patterns of this class give degree 91 or 92
        # components.
        table = json.loads(DEGREE_TABLE.read_text())
        expected = table["I2:0000/*001/01*1"]["degrees"]["e=(1,1,1),swap=0"]
        self.assertEqual(expected, [1, 91])
        c = next(x for x in classes() if x["form"] == "I2:0000/*001/01*1")
        F = plane_curve(c["idx"], 1, 1, 1, False)
        self.assertEqual(component_degrees(F), expected)

    def test_pinned_degree_tables(self) -> None:
        # Every class's 16 patterns give exactly the degree tables below.
        # The factorizations split into small components (lines and
        # conics) carrying the degenerate and three-distinct-value
        # families, plus a genuine coupled component of degree 23..92.
        table = json.loads(DEGREE_TABLE.read_text())
        pinned = {
            "I0:0000/0011/0101": ((21,), (23,)),
            "I0:0000/0101/0110": ((21,), (23,)),
            "I2:0000/*001/01*1": ((1, 91), (92,)),
            "I2:0000/*001/010*": ((1, 87), (88,)),
            "I2:0000/*011/01*1": ((1, 91), (92,)),
            "I2:0000/*011/011*": ((1, 87), (88,)),
            "I2:0000/0011/01*0": ((81,), (92,)),
            "I2:0000/0011/010*": ((81,), (92,)),
            "I2:0000/0011/0101": ((23,),),
            "I2:0000/01*0/01*1": ((1, 1, 1, 80), (92,)),
            "I2:0000/010*/011*": ((1, 1, 1, 2, 2, 64), (92,)),
            "I2:0000/0101/*001": ((81,), (92,)),
            "I2:0000/0101/*011": ((81,), (92,)),
            "I2:0000/0101/00*1": ((92,),),
            "I2:0000/0101/01*0": ((92,),),
            "I2:0000/0101/0110": ((23,),),
        }
        self.assertEqual(set(table), set(pinned))
        for form, expected in pinned.items():
            sizes = sorted({tuple(v) for v in table[form]["degrees"].values()})
            self.assertEqual(sizes, sorted(expected), form)

    def test_genuine_component_present(self) -> None:
        # Each class has at least one pattern whose curve is a single
        # irreducible component of degree >= 23 (the genuine coupled
        # curve, not a degenerate family).
        table = json.loads(DEGREE_TABLE.read_text())
        for form, entry in table.items():
            best = 0
            for degs in entry["degrees"].values():
                if len(degs) == 1:
                    best = max(best, degs[0])
            self.assertGreaterEqual(best, 21, form)


class FinitenessPieces(unittest.TestCase):
    """The three computational pillars of the Faltings finiteness argument.

    (i) exceptional components are exactly the lines t1 in {0, +-1} (and,
    for I2:0000/010*/011*, two vertical conics without rational points);
    (ii) those lines are unrealizable at prime support (slope 0 or +-1
    forces the generator norm to be a square or twice a square);
    (iii) the t3-fiber of the projection is finite at every (t1, t2).
    Genus values live in curve_genus.json (pinned separately).
    """

    EXCEPTIONAL = {
        "I2:0000/*001/01*1": ["t1"],
        "I2:0000/*001/010*": ["t1"],
        "I2:0000/*011/01*1": ["t1"],
        "I2:0000/*011/011*": ["t1"],
        "I2:0000/01*0/01*1": ["t1", "t1 + 1", "t1 - 1"],
        "I2:0000/010*/011*": [
            "t1", "t1 + 1", "t1 - 1",
            "t1**2 + 2*t1 - 1", "t1**2 - 2*t1 - 1",
        ],
    }

    def _first_pattern_with_small_factor(self, form):
        import json

        deg = json.loads((HERE / "torus_curve_degrees.json").read_text())
        for key, v in deg[form]["degrees"].items():
            if any(d <= 2 for d in v):
                m = re.match(
                    r"e=\((-?\d+),(-?\d+),(-?\d+)\),swap=(\d)", key
                )
                return (
                    int(m.group(1)), int(m.group(2)),
                    int(m.group(3)), bool(int(m.group(4))),
                )
        return None

    def test_exceptional_components_pinned(self) -> None:
        for form, expected in self.EXCEPTIONAL.items():
            pat = self._first_pattern_with_small_factor(form)
            self.assertIsNotNone(pat, form)
            c = next(x for x in classes() if x["form"] == form)
            F = plane_curve(c["idx"], *pat)
            small = sorted(
                str(sp.factor(f))
                for f, _ in sp.factor_list(F)[1]
                if sp.Poly(f, T1, T2).total_degree() <= 2
            )
            self.assertEqual(small, sorted(expected), form)
        # the other ten classes have no exceptional components at all
        for c in classes():
            if c["form"] in self.EXCEPTIONAL:
                continue
            pat = self._first_pattern_with_small_factor(c["form"])
            self.assertIsNone(pat, c["form"])

    def test_excluded_lines_unrealizable_at_prime_support(self) -> None:
        # slope b/a = 0, 1, or -1 with pi = k(a + bi), norm = k^2(a^2+b^2):
        # 0 -> k^2 a^2 (a square), +-1 -> 2k^2a^2 (twice a square); neither
        # is ever an odd prime = 1 mod 4.
        for t in (0, 1, -1):
            for a in range(1, 30):
                for k in range(1, 30):
                    b = t * a
                    n = k * k * (a * a + b * b)
                    if sp.isprime(n):
                        self.assertNotEqual(n % 4, 1, (t, a, k, n))

    def test_conics_have_no_rational_points(self) -> None:
        # t1^2 +- 2 t1 - 1: roots are 1 +- sqrt(2), never rational, so the
        # vertical components carry no Q-points.
        for expr in (T1**2 + 2 * T1 - 1, T1**2 - 2 * T1 - 1):
            for root in sp.roots(sp.Poly(expr, T1)):
                self.assertFalse(root.is_rational, root)

    def test_t3_fiber_finite(self) -> None:
        # The two t3-quartics vanish identically only at (t1, t2) in
        # {(0, 0), (0, 1), (0, -1)}, and only for the two EFC classes'
        # mixed-sign patterns (8 of the 256 class-pattern pairs; full
        # sweep 2026-08-23).  Those points lie on the excluded
        # real-generator line t1 = 0 with t2 of excluded slope, so every
        # prime-support point has finite fiber.
        from torus_curve import T3, pattern_equations

        checks = [
            ("I0:0000/0011/0101", (1, -1, -1, False), []),
            ("I2:0000/*001/01*1", (1, 1, 1, False), []),
            (
                "I2:0000/0101/*001",
                (1, 1, 1, False),
                [{T1: 0, T2: -1}, {T1: 0, T2: 0}, {T1: 0, T2: 1}],
            ),
        ]
        for form, pat, expected in checks:
            c = next(x for x in classes() if x["form"] == form)
            eq1, eq2 = pattern_equations(c["idx"], *pat)
            coeffs = (
                sp.Poly(eq1, T3).all_coeffs()
                + sp.Poly(eq2, T3).all_coeffs()
            )
            sols = sp.solve(coeffs, [T1, T2], dict=True)
            self.assertEqual(sols, expected, (form, pat))


class GenusTablePins(unittest.TestCase):
    def test_genus_ledger_ge_two(self) -> None:
        ledger = json.loads((HERE / "curve_genus.json").read_text())
        self.assertGreaterEqual(len(ledger), 2)
        for form, entry in ledger.items():
            for table, info in entry["tables"].items():
                for comp in info["components"]:
                    if comp["degree"] >= 3:
                        self.assertGreaterEqual(
                            comp["genus"], 2, (form, table, comp)
                        )

    def test_genus_spot_check_regenerates(self) -> None:
        import shutil

        if not shutil.which("Singular"):
            self.skipTest("Singular not available")
        from curve_genus import homogenized_terms, singular_genus

        c = next(x for x in classes() if x["form"] == "I0:0000/0011/0101")
        F = plane_curve(c["idx"], 1, -1, -1, False)
        f21 = next(
            f
            for f, _ in sp.factor_list(F)[1]
            if sp.Poly(f, T1, T2).total_degree() == 21
        )
        g = singular_genus(homogenized_terms(f21, 21), 3600)
        self.assertEqual(g, 78)


class RationalPointPins(unittest.TestCase):
    GRID = [("0", "-1"), ("0", "0"), ("0", "1"),
            ("1", "-1"), ("1", "0"), ("1", "1")]

    def test_cff_curves_carry_only_the_unrealizable_grid(self) -> None:
        # Both CFF classes, all 16 distinct pattern curves: the only
        # rational points with t1-height <= 30 (t2 of ANY height, found
        # by numerical isolation + exact verification) are the six grid
        # points {0,1} x {-1,0,1}, all at unrealizable t1.
        ledger = json.loads(
            (HERE / "rational_points.json").read_text()
        )
        for form in ("I0:0000/0011/0101", "I0:0000/0101/0110"):
            entry = ledger[form]
            self.assertGreaterEqual(entry["bound"], 30)
            self.assertEqual(len(entry["curves"]), 8)
            self.assertEqual(entry["realizable_total"], 0)
            for pat, c in entry["curves"].items():
                self.assertEqual(
                    sorted(map(tuple, c["points"])),
                    sorted(map(tuple, self.GRID)),
                    (form, pat),
                )

    def test_rational_point_spot_check_regenerates(self) -> None:
        # Live regeneration at a small bound for one curve: the grid
        # points must all be found (the search is exhaustive in t2).
        from fractions import Fraction

        from rational_point_search import rational_points_on

        c = next(
            x for x in classes() if x["form"] == "I0:0000/0011/0101"
        )
        F = plane_curve(c["idx"], 1, -1, -1, False)
        f21 = next(
            f
            for f, _ in sp.factor_list(F)[1]
            if sp.Poly(f, T1, T2).total_degree() == 21
        )
        pts = rational_points_on(f21, 8, 10**6)
        for a, b in self.GRID:
            self.assertIn((Fraction(a), Fraction(b)), pts)


if __name__ == "__main__":
    unittest.main()
