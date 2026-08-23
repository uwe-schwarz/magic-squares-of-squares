from __future__ import annotations

import json
import unittest
from itertools import product as iproduct
from pathlib import Path

from classes import CLASSES
from deep_regular_lift import (
    class_report,
    greedy_deep_lift,
    is_regular,
    lift_matrix,
    matrix_children,
)
from prime_power_rigidity import (
    Branch,
    common_offset_v2,
    coupled_residual,
    gaussian_normalized_offsets,
    initial_branches,
    is_solution,
    lift_once,
    normalized_offsets,
)

HERE = Path(__file__).resolve().parent
LEDGER = HERE / "deep_regular_lift_60.json"

# Classes whose 2^7 lift matrices are rank-deficient (all columns
# proportional); every other class is regular at every branch.
RANK_DEFICIENT = {
    "I0:0000/0011/0101",
    "I0:0000/0101/0110",
    "I2:0000/*001/010*",
    "I2:0000/*011/011*",
    "I2:0000/010*/011*",
}

# Witness common valuations at 2^60 (stabilized since 2^7); equal to the
# forced 2-adic valuations of the committed scan_2adic_12.json ledger.
EXPECTED_V2 = {
    "I0:0000/0011/0101": 3,
    "I0:0000/0101/0110": 3,
    "I2:0000/0011/0101": 4,
    "I2:0000/0101/0110": 4,
    "I2:0000/0101/*001": 3,
    "I2:0000/0101/*011": 3,
    "I2:0000/0011/01*0": 4,
    "I2:0000/0101/00*1": 4,
    "I2:0000/0101/01*0": 4,
    "I2:0000/0011/010*": 3,
    "I2:0000/*001/01*1": 3,
    "I2:0000/*011/01*1": 3,
    "I2:0000/*001/010*": 3,
    "I2:0000/*011/011*": 3,
    "I2:0000/01*0/01*1": 4,
    "I2:0000/010*/011*": 3,
}


def branches_at(indices, bits: int) -> list[Branch]:
    out = initial_branches(indices, 4)
    for b in range(5, bits + 1):
        out = lift_once(indices, out, b)
    return out


class DeepLiftTests(unittest.TestCase):
    def test_matrix_children_match_exact_enumeration(self) -> None:
        # The affine lift matrix predicts the exact children of every
        # branch at bits >= 7; check on a spread of classes and branches.
        for form, _, indices in CLASSES[:4]:
            branches = branches_at(indices, 7)
            for br in branches[:24]:
                bit = 1 << 4
                exact = set()
                for add in iproduct((0, 1), repeat=3):
                    cand = tuple(br.xs[t] + add[t] * bit for t in range(3))
                    if is_solution(
                        indices, cand, 1 << 8, br.signs, br.edge_swap
                    ):
                        exact.add(add)
                predicted = set(
                    matrix_children(
                        indices, br.xs, 7, br.signs, br.edge_swap
                    )
                )
                self.assertEqual(exact, predicted, (form, br.xs))

    def test_rank_deficiency_classification(self) -> None:
        for form, _, indices in CLASSES:
            branches = branches_at(indices, 7)
            regular = [
                is_regular(
                    lift_matrix(
                        indices, br.xs, 7, br.signs, br.edge_swap
                    )[0]
                )
                for br in branches
            ]
            if form in RANK_DEFICIENT:
                self.assertFalse(any(regular), form)
            else:
                self.assertTrue(all(regular), form)

    def test_committed_witness_verifies_at_2p60(self) -> None:
        ledger = json.loads(LEDGER.read_text())
        self.assertEqual(ledger["target_bits"], 60)
        by_form = {c[0]: c for c in CLASSES}
        for form, rep in ledger["classes"].items():
            w = rep["deep_witness"]
            self.assertIsNotNone(w, form)
            self.assertEqual(w["common_v2"], EXPECTED_V2[form], form)
            self.assertEqual(
                rep["patterns_with_regular_branch"] > 0,
                form not in RANK_DEFICIENT,
            )
            _, _, indices = by_form[form]
            xs = tuple(w["xs"])
            signs = tuple(w["signs"])
            modulus = 1 << 60
            self.assertEqual(
                coupled_residual(
                    normalized_offsets(indices, xs, modulus),
                    signs,
                    w["edge_swap"],
                    modulus,
                ),
                (0, 0),
                form,
            )
            generators = tuple((1, 2 * x) for x in xs)
            self.assertEqual(
                gaussian_normalized_offsets(indices, generators, modulus),
                normalized_offsets(indices, xs, modulus),
                form,
            )
            self.assertEqual(
                common_offset_v2(
                    normalized_offsets(indices, xs, modulus), 60
                ),
                w["common_v2"],
                form,
            )

    def test_short_deep_lift_reproduces_valuation(self) -> None:
        # One regular and one rank-deficient class, lifted live to 2^28:
        # witnesses must exist with the ledger valuations.
        for form in ("I2:0000/0101/*001", "I0:0000/0011/0101"):
            entry = next(c for c in CLASSES if c[0] == form)
            _, _, indices = entry
            rep = class_report(indices, form, entry[1], 28)
            w = rep["deep_witness"]
            self.assertIsNotNone(w, form)
            self.assertEqual(w["common_v2"], EXPECTED_V2[form], form)
            self.assertEqual(w["stabilized_at_bits"], 7, form)

    def test_regular_inheritance_sample(self) -> None:
        form, _, indices = CLASSES[4]  # EFC, regular
        branches = branches_at(indices, 7)
        br = branches[0]
        w = greedy_deep_lift(indices, br, 7, 14)
        self.assertIsNotNone(w)
        self.assertTrue(w.regular)
        columns, _ = lift_matrix(
            indices, w.xs, 14, w.signs, w.edge_swap
        )
        self.assertTrue(is_regular(columns))


if __name__ == "__main__":
    unittest.main()
