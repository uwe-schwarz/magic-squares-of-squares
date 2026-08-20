from __future__ import annotations

from collections import Counter
import unittest

from p2qr_monomial_filter import (
    classify_arithmetic_filter,
    classify_combined_filter,
    classify_complete_filter,
    classify_full_filter,
    classify_generalized_filter,
    classify_monomial_filter,
    classify_prime_lower_filter,
    classify_sharp_axis_filter,
    classify_sharp_skew_filter,
    complementary_axis_descent_forms,
    edge_content_exponents,
    sharp_axis_inequality,
    sharp_skew_inequality,
)


EXPECTED_EXCLUDED_ROLES = {
    ("C", "C", "C"): 7,
    ("C", "C", "E"): 13,
    ("C", "E", "E"): 7,
    ("C", "F", "E"): 8,
    ("E", "C", "C"): 7,
    ("E", "C", "E"): 4,
    ("E", "E", "E"): 4,
    ("E", "F", "C"): 8,
}

EXPECTED_SURVIVING_ROLES = {
    ("C", "F", "C"): 15,
    ("C", "F", "E"): 10,
    ("C", "F", "F"): 7,
    ("E", "C", "E"): 9,
    ("E", "E", "E"): 3,
    ("E", "F", "C"): 10,
    ("E", "F", "E"): 15,
    ("E", "F", "F"): 7,
}

EXPECTED_COMBINED_SURVIVING_ROLES = {
    ("C", "F", "C"): 9,
    ("C", "F", "E"): 6,
    ("C", "F", "F"): 5,
    ("E", "C", "E"): 6,
    ("E", "E", "E"): 3,
    ("E", "F", "C"): 6,
    ("E", "F", "E"): 9,
    ("E", "F", "F"): 5,
}

EXPECTED_FULL_SURVIVING_ROLES = {
    ("C", "F", "C"): 7,
    ("C", "F", "E"): 5,
    ("C", "F", "F"): 2,
    ("E", "C", "E"): 6,
    ("E", "E", "E"): 3,
    ("E", "F", "C"): 5,
    ("E", "F", "E"): 8,
    ("E", "F", "F"): 3,
}

EXPECTED_COMPLETE_SURVIVING_ROLES = {
    ("C", "F", "C"): 4,
    ("C", "F", "E"): 1,
    ("C", "F", "F"): 2,
    ("E", "C", "E"): 6,
    ("E", "E", "E"): 3,
    ("E", "F", "C"): 4,
    ("E", "F", "E"): 7,
    ("E", "F", "F"): 3,
}

EXPECTED_GENERALIZED_SURVIVING_ROLES = {
    ("C", "F", "C"): 3,
    ("C", "F", "F"): 2,
    ("E", "C", "E"): 5,
    ("E", "E", "E"): 3,
    ("E", "F", "C"): 3,
    ("E", "F", "E"): 5,
    ("E", "F", "F"): 3,
}

EXPECTED_SHARP_AXIS_SURVIVING_ROLES = {
    ("C", "F", "F"): 2,
    ("E", "C", "E"): 5,
    ("E", "E", "E"): 3,
    ("E", "F", "C"): 3,
    ("E", "F", "E"): 5,
    ("E", "F", "F"): 3,
}

EXPECTED_SHARP_SKEW_SURVIVING_ROLES = {
    ("C", "F", "F"): 2,
    ("E", "C", "E"): 5,
    ("E", "E", "E"): 3,
    ("E", "F", "C"): 2,
    ("E", "F", "E"): 4,
    ("E", "F", "F"): 2,
}

EXPECTED_PRIME_LOWER_SURVIVING_ROLES = {
    ("C", "F", "F"): 2,
    ("E", "C", "E"): 4,
    ("E", "E", "E"): 3,
    ("E", "F", "C"): 2,
    ("E", "F", "E"): 4,
    ("E", "F", "F"): 2,
}

EXPECTED_ARITHMETIC_SURVIVING_ROLES = {
    **EXPECTED_PRIME_LOWER_SURVIVING_ROLES,
    ("E", "E", "E"): 2,
}

COMPOSITE_ONLY_EXCLUDED = {
    "I0:0000/0001/0011",
    "I0:0000/0001/0101",
    "I0:0000/0100/0101",
    "I0:0000/0101/0*01",
    "I0:0000/0111/0*01",
    "I0:0000/0111/00*1",
    "I2:0000/0001/0101",
    "I2:0000/0010/010*",
    "I2:0000/0011/0100",
    "I2:0000/0110/*001",
}

COMMON_FACTOR_ONLY_EXCLUDED = {
    "I0:0000/0011/01*1",
    "I0:0000/0101/*001",
    "I0:0000/0101/0*10",
    "I0:0000/0101/0*11",
    "I0:0000/0101/00*1",
    "I0:0000/0110/00*0",
    "I0:0000/0110/00*1",
    "I2:0000/0101/001*",
    "I2:0000/0110/*010",
}

GENERALIZED_ONLY_EXCLUDED = {
    "I0:0000/0011/01*0",
    "I0:0000/0101/0*00",
    "I2:0000/*001/011*",
    "I2:0000/0101/000*",
    "I2:0000/0101/010*",
    "I2:0000/0110/*000",
}

SHARP_AXIS_ONLY_EXCLUDED = {
    "I0:0000/0011/*001",
    "I0:0000/0011/0*01",
    "I0:0000/0101/*011",
}

SHARP_SKEW_ONLY_EXCLUDED = {
    "I2:0000/0100/0101",
    "I2:0000/0101/011*",
    "I2:0000/0110/*011",
}

PRIME_LOWER_ONLY_EXCLUDED = {
    "I2:0000/*001/01*0",
}

COMPLEMENTARY_AXIS_ONLY_EXCLUDED = {
    "I2:0000/01*0/011*",
}


class P2QRMonomialFilterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.results = classify_monomial_filter()
        cls.combined_results = classify_combined_filter()
        cls.full_results = classify_full_filter()
        cls.complete_results = classify_complete_filter()
        cls.generalized_results = classify_generalized_filter()
        cls.sharp_axis_results = classify_sharp_axis_filter()
        cls.sharp_skew_results = classify_sharp_skew_filter()
        cls.prime_lower_results = classify_prime_lower_filter()
        cls.arithmetic_results = classify_arithmetic_filter()

    def test_exact_breakdown(self) -> None:
        excluded = tuple(result for result in self.results if result.excluded)
        survivors = tuple(
            result for result in self.results if not result.excluded
        )
        self.assertEqual(len(self.results), 134)
        self.assertEqual(len(excluded), 58)
        self.assertEqual(len(survivors), 76)
        self.assertEqual(
            Counter(result.role for result in excluded),
            EXPECTED_EXCLUDED_ROLES,
        )
        self.assertEqual(
            Counter(result.role for result in survivors),
            EXPECTED_SURVIVING_ROLES,
        )
        self.assertTrue(all(result.certificate for result in excluded))

    def test_content_uses_intermediate_index_magnitude(self) -> None:
        pattern = (0, None, 2)
        self.assertEqual(
            edge_content_exponents(
                pattern,
                "I0:0000/0001/01*0",
                2,
            ),
            (1, 0, 2),
        )
        self.assertEqual(
            edge_content_exponents(
                pattern,
                "I0:0000/0100/00*1",
                2,
            ),
            (3, 0, 2),
        )

    def test_aligned_extreme_row_separates_same_role(self) -> None:
        by_form = {result.canonical_form: result for result in self.results}
        survivor = by_form["I0:0000/0100/00*1"]
        excluded = by_form["I0:0000/0100/01*1"]
        self.assertEqual(survivor.role, ("C", "F", "E"))
        self.assertEqual(excluded.role, survivor.role)
        self.assertEqual(survivor.edge_contents, ((2, (3, 0, 2)),))
        self.assertEqual(excluded.edge_contents, ((2, (1, 2, 2)),))
        self.assertFalse(survivor.excluded)
        self.assertTrue(excluded.excluded)

    def test_safe_quotient_comparison_stage(self) -> None:
        excluded = tuple(
            result for result in self.combined_results if result.excluded
        )
        survivors = tuple(
            result for result in self.combined_results if not result.excluded
        )
        self.assertEqual(len(excluded), 85)
        self.assertEqual(len(survivors), 49)
        self.assertEqual(
            sum(len(result.comparisons) for result in self.combined_results),
            86,
        )
        self.assertEqual(
            sum(bool(result.comparisons) for result in self.combined_results),
            70,
        )
        self.assertEqual(
            Counter(result.role for result in survivors),
            EXPECTED_COMBINED_SURVIVING_ROLES,
        )
        self.assertFalse(any(
            comparison.remaining_row == 0
            for result in self.combined_results
            for comparison in result.comparisons
        ))

    def test_intermediate_content_and_corner_coefficient(self) -> None:
        by_form = {
            result.canonical_form: result
            for result in self.combined_results
        }
        result = by_form["I0:0000/0001/0*11"]
        q_alignment = next(
            comparison
            for comparison in result.comparisons
            if comparison.aligned_row == 1
        )
        self.assertEqual(q_alignment.divisor_row, 0)
        self.assertEqual(q_alignment.divisor_content, 6)
        r_comparison = next(
            comparison
            for comparison in result.comparisons
            if comparison.aligned_row == 0
        )
        self.assertEqual(r_comparison.omitted_column, 0)
        self.assertEqual((r_comparison.family, r_comparison.level), ("A", 4))

    def test_composite_block_stage(self) -> None:
        excluded = tuple(
            result for result in self.full_results if result.excluded
        )
        survivors = tuple(
            result for result in self.full_results if not result.excluded
        )
        self.assertEqual(len(excluded), 95)
        self.assertEqual(len(survivors), 39)
        self.assertEqual(
            sum(len(result.composites) for result in self.full_results),
            18,
        )
        self.assertEqual(
            Counter(result.role for result in survivors),
            EXPECTED_FULL_SURVIVING_ROLES,
        )
        combined_by_form = {
            result.canonical_form: result
            for result in self.combined_results
        }
        newly_excluded = {
            result.canonical_form
            for result in self.full_results
            if result.excluded
            and not combined_by_form[result.canonical_form].excluded
        }
        self.assertEqual(newly_excluded, COMPOSITE_ONLY_EXCLUDED)

    def test_general_common_factor_stage(self) -> None:
        excluded = tuple(
            result for result in self.complete_results if result.excluded
        )
        survivors = tuple(
            result for result in self.complete_results if not result.excluded
        )
        self.assertEqual(len(excluded), 104)
        self.assertEqual(len(survivors), 30)
        self.assertEqual(
            sum(
                len(result.common_factors)
                for result in self.complete_results
            ),
            134 * 4 * 4,
        )
        self.assertEqual(
            Counter(result.role for result in survivors),
            EXPECTED_COMPLETE_SURVIVING_ROLES,
        )
        full_by_form = {
            result.canonical_form: result for result in self.full_results
        }
        newly_excluded = {
            result.canonical_form
            for result in self.complete_results
            if result.excluded
            and not full_by_form[result.canonical_form].excluded
        }
        self.assertEqual(newly_excluded, COMMON_FACTOR_ONLY_EXCLUDED)

        by_form = {
            result.canonical_form: result
            for result in self.complete_results
        }
        sample = by_form["I0:0000/0101/*001"]
        bound = next(
            comparison
            for comparison in sample.common_factors
            if comparison.omitted_column == 1
            and comparison.column_signs == (1, 1, -1)
        )
        self.assertEqual(bound.plus_minima, (0, 0, 0))
        self.assertEqual(bound.minus_minima, (0, 4, 2))
        self.assertEqual(bound.vector, (-4, 2, 0))

    def test_generalized_comparison_stage(self) -> None:
        excluded = tuple(
            result for result in self.generalized_results
            if result.excluded
        )
        survivors = tuple(
            result for result in self.generalized_results
            if not result.excluded
        )
        self.assertEqual(len(excluded), 110)
        self.assertEqual(len(survivors), 24)
        self.assertEqual(
            sum(
                len(result.generalized_comparisons)
                for result in self.generalized_results
            ),
            300,
        )
        self.assertEqual(
            sum(
                bool(result.generalized_comparisons)
                for result in self.generalized_results
            ),
            114,
        )
        self.assertEqual(
            Counter(result.role for result in survivors),
            EXPECTED_GENERALIZED_SURVIVING_ROLES,
        )
        complete_by_form = {
            result.canonical_form: result
            for result in self.complete_results
        }
        newly_excluded = {
            result.canonical_form
            for result in self.generalized_results
            if result.excluded
            and not complete_by_form[result.canonical_form].excluded
        }
        self.assertEqual(newly_excluded, GENERALIZED_ONLY_EXCLUDED)

        by_form = {
            result.canonical_form: result
            for result in self.generalized_results
        }
        opposite_extremes = by_form["I0:0000/0011/*001"]
        signatures = {
            (
                value.divisor_row,
                value.remaining_row,
                value.family,
                value.level,
            )
            for value in opposite_extremes.generalized_comparisons
        }
        self.assertIn((2, 0, "A", 8), signatures)
        self.assertNotIn((2, 0, "A", 4), signatures)

        intermediate_opposite = by_form["I0:0000/0001/01*1"]
        self.assertTrue(any(
            value.omitted_column == 1
            and value.remaining_row == 0
            and value.family == "S"
            and value.level == 6
            for value in intermediate_opposite.generalized_comparisons
        ))

    def test_sharp_axis_stage(self) -> None:
        excluded = tuple(
            result for result in self.sharp_axis_results
            if result.excluded
        )
        survivors = tuple(
            result for result in self.sharp_axis_results
            if not result.excluded
        )
        self.assertEqual(len(excluded), 113)
        self.assertEqual(len(survivors), 21)
        self.assertEqual(
            sum(
                len(result.sharp_axis_comparisons)
                for result in self.sharp_axis_results
            ),
            200,
        )
        self.assertEqual(
            sum(
                bool(result.sharp_axis_comparisons)
                for result in self.sharp_axis_results
            ),
            109,
        )
        self.assertEqual(
            Counter(result.role for result in survivors),
            EXPECTED_SHARP_AXIS_SURVIVING_ROLES,
        )
        generalized_by_form = {
            result.canonical_form: result
            for result in self.generalized_results
        }
        newly_excluded = {
            result.canonical_form
            for result in self.sharp_axis_results
            if result.excluded
            and not generalized_by_form[result.canonical_form].excluded
        }
        self.assertEqual(newly_excluded, SHARP_AXIS_ONLY_EXCLUDED)

        by_form = {
            result.canonical_form: result
            for result in self.sharp_axis_results
        }
        sample = by_form["I0:0000/0011/*001"]
        bounds = {
            sharp_axis_inequality(comparison)
            for comparison in sample.sharp_axis_comparisons
        }
        self.assertIn(
            ("A4_sharp_p_r", (8, 0, -4), (2, 0, 0, 0, 0, 0)),
            bounds,
        )
        self.assertIn(
            ("A8_sharp_r_p", (-8, 0, 8), (2, 0, 0, 0, 0, 0)),
            bounds,
        )
        self.assertTrue(any(
            name.startswith("A") and "_sharp_" in name
            for name in sample.certificate_bounds or ()
        ))

    def test_sharp_skew_stage(self) -> None:
        excluded = tuple(
            result for result in self.sharp_skew_results
            if result.excluded
        )
        survivors = tuple(
            result for result in self.sharp_skew_results
            if not result.excluded
        )
        self.assertEqual(len(excluded), 116)
        self.assertEqual(len(survivors), 18)
        self.assertEqual(
            sum(
                len(result.sharp_skew_comparisons)
                for result in self.sharp_skew_results
            ),
            100,
        )
        self.assertEqual(
            sum(
                bool(result.sharp_skew_comparisons)
                for result in self.sharp_skew_results
            ),
            76,
        )
        self.assertEqual(
            Counter(result.role for result in survivors),
            EXPECTED_SHARP_SKEW_SURVIVING_ROLES,
        )
        sharp_axis_by_form = {
            result.canonical_form: result
            for result in self.sharp_axis_results
        }
        newly_excluded = {
            result.canonical_form
            for result in self.sharp_skew_results
            if result.excluded
            and not sharp_axis_by_form[result.canonical_form].excluded
        }
        self.assertEqual(newly_excluded, SHARP_SKEW_ONLY_EXCLUDED)

        by_form = {
            result.canonical_form: result
            for result in self.sharp_skew_results
        }
        sample = by_form["I2:0000/0100/0101"]
        bounds = {
            sharp_skew_inequality(comparison)
            for comparison in sample.sharp_skew_comparisons
        }
        self.assertIn(
            ("S4_sharp_p_q", (2, -4, 0), (0, 2, 0, 0, -1, 0)),
            bounds,
        )
        self.assertEqual(sample.aggregate_vector, (0, 0, 0))
        self.assertEqual(sample.aggregate_constant, (1, 3, 0, 0, -1, 0))

        level_constants = {
            comparison.level: sharp_skew_inequality(comparison)[2]
            for result in self.sharp_skew_results
            for comparison in result.sharp_skew_comparisons
        }
        self.assertEqual(level_constants, {
            2: (0, 2, -1, 0, 0, 0),
            4: (0, 2, 0, 0, -1, 0),
            6: (0, 2, 0, -1, 0, 0),
            8: (0, 2, 0, 0, 0, -1),
        })

    def test_prime_lower_stage(self) -> None:
        excluded = tuple(
            result for result in self.prime_lower_results
            if result.excluded
        )
        survivors = tuple(
            result for result in self.prime_lower_results
            if not result.excluded
        )
        self.assertEqual(len(excluded), 117)
        self.assertEqual(len(survivors), 17)
        self.assertEqual(
            Counter(result.role for result in survivors),
            EXPECTED_PRIME_LOWER_SURVIVING_ROLES,
        )
        sharp_skew_by_form = {
            result.canonical_form: result
            for result in self.sharp_skew_results
        }
        newly_excluded = {
            result.canonical_form
            for result in self.prime_lower_results
            if result.excluded
            and not sharp_skew_by_form[result.canonical_form].excluded
        }
        self.assertEqual(newly_excluded, PRIME_LOWER_ONLY_EXCLUDED)

        by_form = {
            result.canonical_form: result
            for result in self.prime_lower_results
        }
        sample = by_form["I2:0000/*001/01*0"]
        self.assertEqual(sample.prime_lower_bounds, (17, 5, 73))
        self.assertEqual(sample.aggregate_vector, (0, 0, 2))
        self.assertEqual(sample.aggregate_constant, (10, 0, 0, 0, 0, 0))

    def test_complementary_axis_descent_stage(self) -> None:
        excluded = tuple(
            result for result in self.arithmetic_results
            if result.excluded
        )
        survivors = tuple(
            result for result in self.arithmetic_results
            if not result.excluded
        )
        self.assertEqual(len(excluded), 118)
        self.assertEqual(len(survivors), 16)
        self.assertEqual(
            Counter(result.role for result in survivors),
            EXPECTED_ARITHMETIC_SURVIVING_ROLES,
        )
        newly_excluded = {
            result.canonical_form
            for result in self.arithmetic_results
            if result.complementary_axis_descent
            and not result.previous_excluded
        }
        self.assertEqual(
            newly_excluded,
            COMPLEMENTARY_AXIS_ONLY_EXCLUDED,
        )
        self.assertEqual(
            set(complementary_axis_descent_forms()),
            COMPLEMENTARY_AXIS_ONLY_EXCLUDED,
        )


if __name__ == "__main__":
    unittest.main()
