import unittest
import math

from search import (
    center_candidates,
    center_offsets,
    factor_integer,
    gaussian_mul,
    gaussian_pow,
    line_sums,
    passes_refined_block_balance,
)


class GaussianArithmeticTests(unittest.TestCase):
    def test_multiplication_and_power(self) -> None:
        self.assertEqual(gaussian_mul((1, 2), (3, -4)), (11, 2))
        self.assertEqual(gaussian_pow((1, 2), 3), (-11, -2))


class CenterEnumerationTests(unittest.TestCase):
    @staticmethod
    def brute_force_offsets(center_root: int) -> set[int]:
        center = center_root * center_root
        offsets: set[int] = set()
        for real in range(1, center_root):
            imag_squared = center - real * real
            imag = math.isqrt(imag_squared)
            if imag > 0 and imag * imag == imag_squared:
                offset = 2 * real * imag
                if 0 < offset < center:
                    offsets.add(offset)
        return offsets

    def test_center_65_has_the_four_classical_offsets(self) -> None:
        self.assertEqual(center_offsets(65), {2016, 3000, 3696, 4056})
        self.assertEqual(center_candidates(65), [])

    def test_gaussian_enumerator_matches_direct_enumeration(self) -> None:
        for center_root in range(2, 300):
            if center_offsets(center_root):
                self.assertEqual(
                    center_offsets(center_root),
                    self.brute_force_offsets(center_root),
                    center_root,
                )

    def test_refined_filter_rejects_cases_allowed_by_constant_two(self) -> None:
        # The dominant 17^3 block still passes P < 2M but fails P^2 < 3M^2.
        self.assertFalse(passes_refined_block_balance(17**3 * 13 * 197))

    def test_every_two_block_center_is_rejected(self) -> None:
        self.assertFalse(passes_refined_block_balance(17**3 * 2897))
        # This pair passed every earlier height and fourth-power-residue filter.
        self.assertFalse(passes_refined_block_balance(97**3 * 953**2))

    def test_two_block_exclusion_is_specific_to_two_blocks(self) -> None:
        self.assertTrue(passes_refined_block_balance(5 * 13 * 17))

    def test_strictly_dominant_block_requires_exponent_three(self) -> None:
        # 17^2 is strictly dominant, but both block-height inequalities hold.
        self.assertFalse(passes_refined_block_balance(17**2 * 5 * 53))

    def test_strictly_dominant_prime_must_be_one_modulo_eight(self) -> None:
        # The dominant 13^3 block passes both height bounds but 13 == 5 (mod 8).
        self.assertFalse(passes_refined_block_balance(13**3 * 17 * 109))

    def test_line_sums(self) -> None:
        lo_shu = ((4, 9, 2), (3, 5, 7), (8, 1, 6))
        self.assertEqual(line_sums(lo_shu), (15,) * 8)

    def test_factorization(self) -> None:
        self.assertEqual(factor_integer(5**2 * 13 * 17), {5: 2, 13: 1, 17: 1})


if __name__ == "__main__":
    unittest.main()
