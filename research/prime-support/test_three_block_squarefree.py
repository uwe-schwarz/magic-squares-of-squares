import unittest

from three_block_squarefree import (
    REPRESENTATIVE_A,
    REPRESENTATIVE_B,
    classify_physical_masks,
    d_equation_spaces,
    has_distinct_nonzero_orientation_vectors,
    physical_masks,
    signed_variable_orbits,
)


class ThreeBlockSquarefreeTests(unittest.TestCase):
    def test_complete_d_relation_enumeration(self) -> None:
        spaces = d_equation_spaces()
        self.assertEqual(sum(spaces.values()), 24 * 16)
        self.assertEqual(len(spaces), 48)
        self.assertEqual(set(spaces.values()), {8})

    def test_two_signed_prime_variable_orbits(self) -> None:
        spaces = d_equation_spaces()
        orbits = signed_variable_orbits(set(spaces))
        self.assertEqual(len(orbits), 2)
        self.assertEqual(sorted(len(orbit) for orbit in orbits), [24, 24])
        self.assertEqual(set().union(*orbits), set(spaces))
        self.assertTrue(any(REPRESENTATIVE_A in orbit for orbit in orbits))
        self.assertTrue(any(REPRESENTATIVE_B in orbit for orbit in orbits))
        self.assertFalse(any(
            REPRESENTATIVE_A in orbit and REPRESENTATIVE_B in orbit
            for orbit in orbits
        ))

    def test_orbit_a_elliptic_substitution(self) -> None:
        # Orbit A: V^2=t(1+2t)(2-t), X=-2t-1, Y=2V.
        for t in range(-8, 9):
            x_coordinate = -2 * t - 1
            self.assertEqual(
                4 * t * (1 + 2 * t) * (2 - t),
                x_coordinate * (x_coordinate + 1) * (x_coordinate + 5),
            )

    def test_physical_squarefree_classification(self) -> None:
        self.assertEqual(len(physical_masks()), 16)
        results = classify_physical_masks()
        self.assertEqual(
            tuple(
                (result.mask, result.surviving_assignments,
                 len(result.canonical_forms))
                for result in results
            ),
            (
                ((None, None, None), 384, 1),
                ((None, None, 0), 768, 4),
                ((None, None, 2), 768, 4),
                ((None, 0, 0), 384, 2),
                ((None, 0, 1), 384, 2),
                ((None, 0, 2), 384, 6),
                ((None, 2, 2), 384, 2),
                ((None, 2, 3), 384, 2),
                ((0, 0, 0), 0, 0),
                ((0, 0, 1), 64, 1),
                ((0, 0, 2), 64, 1),
                ((0, 1, 2), 64, 1),
                ((0, 2, 2), 64, 1),
                ((0, 2, 3), 64, 1),
                ((2, 2, 2), 0, 0),
                ((2, 2, 3), 64, 1),
            ),
        )
        self.assertEqual(
            sum(len(result.canonical_forms) for result in results), 29
        )
        by_mask = {result.mask: result for result in results}
        self.assertIn(
            "0000/0001/*010",
            by_mask[(None, None, 0)].canonical_forms,
        )
        self.assertIn(
            "0000/0100/*001",
            by_mask[(None, None, 0)].canonical_forms,
        )
        self.assertIn(
            "0000/0001/01*0",
            by_mask[(None, None, 2)].canonical_forms,
        )
        self.assertIn(
            "0000/0100/00*1",
            by_mask[(None, None, 2)].canonical_forms,
        )
        self.assertIn(
            "0000/*001/*010",
            by_mask[(None, 0, 0)].canonical_forms,
        )
        self.assertIn(
            "0000/*001/*011",
            by_mask[(None, 0, 0)].canonical_forms,
        )
        self.assertIn(
            "0000/00*1/01*0",
            by_mask[(None, 2, 2)].canonical_forms,
        )
        self.assertIn(
            "0000/01*0/01*1",
            by_mask[(None, 2, 2)].canonical_forms,
        )
        # These are exactly the ten one-F representatives addressed by the
        # paired Gaussian divisor comparisons in the squarefree note.
        excluded_one_f_forms = {
            (None, 0, 1): {
                "0000/*001/0*10",
                "0000/*001/0*11",
            },
            (None, 0, 2): {
                "0000/*001/01*0",
                "0000/*001/01*1",
                "0000/*010/00*1",
                "0000/*010/01*0",
                "0000/*011/00*1",
                "0000/*011/01*1",
            },
            (None, 2, 3): {
                "0000/00*1/010*",
                "0000/01*0/011*",
            },
        }
        for mask, expected_forms in excluded_one_f_forms.items():
            self.assertEqual(
                set(by_mask[mask].canonical_forms),
                expected_forms,
            )
        self.assertEqual(
            by_mask[(0, 0, 1)].canonical_forms,
            ("*000/*011/0*01",),
        )
        self.assertEqual(
            by_mask[(0, 0, 2)].canonical_forms,
            ("*000/*010/00*1",),
        )
        self.assertEqual(
            by_mask[(0, 1, 2)].canonical_forms,
            ("*000/1*01/00*1",),
        )
        self.assertEqual(
            by_mask[(0, 2, 2)].canonical_forms,
            ("*000/00*1/10*1",),
        )
        self.assertEqual(
            by_mask[(0, 2, 3)].canonical_forms,
            ("*000/00*1/101*",),
        )
        self.assertEqual(
            by_mask[(2, 2, 3)].canonical_forms,
            ("00*0/00*1/010*",),
        )
        self.assertEqual(
            sum(
                len(result.canonical_forms)
                for result in results
                if result.mask != (None, None, None)
            ),
            28,
        )

    def test_projective_orientation_distinctness(self) -> None:
        all_unit = (None, None, None)
        repeated = {
            (row, column): 0
            for row in range(3)
            for column in range(4)
        }
        self.assertFalse(
            has_distinct_nonzero_orientation_vectors(all_unit, repeated)
        )

        hadamard_rows = ("0000", "0011", "0101")
        hadamard = {
            (row, column): int(hadamard_rows[row][column])
            for row in range(3)
            for column in range(4)
        }
        self.assertTrue(
            has_distinct_nonzero_orientation_vectors(all_unit, hadamard)
        )

        zero_mask = (0, 0, 0)
        zero_bits = {
            edge: 0
            for edge in (
                (row, column)
                for row in range(3)
                for column in range(4)
                if zero_mask[row] != column
            )
        }
        self.assertFalse(
            has_distinct_nonzero_orientation_vectors(zero_mask, zero_bits)
        )


if __name__ == "__main__":
    unittest.main()
