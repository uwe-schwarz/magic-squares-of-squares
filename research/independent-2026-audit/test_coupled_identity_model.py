from __future__ import annotations

import unittest

from coupled_identity_model import unresolved_records, validate


class CoupledIdentityModelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.records = unresolved_records()

    def test_exact_survivor_count(self) -> None:
        self.assertEqual(len(self.records), 16)
        validate(self.records)

    def test_every_class_has_all_four_physical_relations(self) -> None:
        for record in self.records:
            deletions = record["deletions"]
            self.assertEqual(
                [item["omitted_column"] for item in deletions],
                [0, 1, 2, 3],
            )
            # Omitting a corner gives a 211 relation; omitting an edge gives 111.
            self.assertEqual(
                sorted(deletions[0]["coefficient_magnitudes"]),
                [0, 1, 1, 2],
            )
            self.assertEqual(
                sorted(deletions[1]["coefficient_magnitudes"]),
                [0, 1, 1, 2],
            )
            self.assertEqual(
                sorted(deletions[2]["coefficient_magnitudes"]),
                [0, 1, 1, 1],
            )
            self.assertEqual(
                sorted(deletions[3]["coefficient_magnitudes"]),
                [0, 1, 1, 1],
            )

    def test_intermediate_p_index_is_preserved(self) -> None:
        for record in self.records:
            p_row = record["local_indices"][0]
            self.assertEqual(sorted(abs(value) for value in p_row), [1, 2, 2, 2])


if __name__ == "__main__":
    unittest.main()
