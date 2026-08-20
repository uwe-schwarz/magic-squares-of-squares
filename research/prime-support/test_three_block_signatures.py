import unittest

from three_block_signatures import (
    PATTERNS,
    classify_all,
    common_factor_is_nontrivial,
    edges,
    is_coherent,
    survives_four_relations,
)


EXPECTED = {
    "FFF": (
        3264,
        (
            "0000/0000/0011",
            "0000/0001/0010",
            "0000/0011/0101",
        ),
    ),
    "FF1": (
        1344,
        (
            "0000/0001/*010",
            "0000/0011/*000",
            "0000/0011/*001",
            "0000/0111/*001",
        ),
    ),
    "F11": (384, ("0000/*001/*010",)),
    "F12": (
        448,
        ("0000/*001/0*10", "0000/*001/0*11", "0000/*011/0*11"),
    ),
    "111": (480, ("*000/*000/*001", "*000/*001/*010")),
    "112": (
        384,
        ("*000/*000/0*01", "*000/*001/0*00", "*000/*011/0*01"),
    ),
    "123": (256, ("*000/0*00/00*1", "*000/1*01/00*1")),
}


class ThreeBlockSignatureTests(unittest.TestCase):
    def test_complete_classification(self) -> None:
        results = classify_all()
        self.assertEqual(tuple(result.name for result in results), tuple(
            name for name, _ in PATTERNS
        ))
        self.assertEqual(sum(len(result.classes) for result in results), 18)
        for result in results:
            expected_assignments, expected_forms = EXPECTED[result.name]
            self.assertEqual(result.surviving_assignments, expected_assignments)
            self.assertEqual(
                tuple(item.canonical for item in result.classes), expected_forms
            )

    def test_coherent_signature_is_rejected_when_common_factor_remains(self) -> None:
        mask = (None, None, None)
        bits = {edge: 0 for edge in edges(mask)}
        self.assertTrue(is_coherent(mask, bits, (0, 1, 2)))
        self.assertFalse(survives_four_relations(mask, bits))

    def test_hadamard_signature_frustrates_every_deletion(self) -> None:
        mask = (None, None, None)
        rows = ("0000", "0011", "0101")
        bits = {
            (row, column): int(rows[row][column])
            for row, column in edges(mask)
        }
        self.assertTrue(survives_four_relations(mask, bits))
        for omitted in range(4):
            columns = tuple(column for column in range(4) if column != omitted)
            self.assertFalse(is_coherent(mask, bits, columns))

    def test_common_factor_rule_for_three_balanced_exceptions(self) -> None:
        mask = (0, 1, 2)
        self.assertFalse(common_factor_is_nontrivial(mask, 3))
        for omitted in (0, 1, 2):
            self.assertTrue(common_factor_is_nontrivial(mask, omitted))


if __name__ == "__main__":
    unittest.main()
