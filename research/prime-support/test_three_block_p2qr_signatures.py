from __future__ import annotations

from itertools import product
import unittest

from three_block_p2qr_signatures import classify_all


PhysicalPattern = tuple[int, int | None, int | None]
Bits = dict[tuple[int, int], int]

ROW_PERMUTATIONS = ((0, 1, 2), (0, 2, 1))
COLUMN_PERMUTATIONS = (
    (0, 1, 2, 3),
    (1, 0, 2, 3),
    (0, 1, 3, 2),
    (1, 0, 3, 2),
)
BALANCED_COLUMNS = (None, 0, 1, 2, 3)

EXPECTED_BREAKDOWN = {
    (0, None, None): (1536, 7),
    (0, None, 0): (768, 6),
    (0, None, 1): (1152, 9),
    (0, None, 2): (1152, 18),
    (0, 0, 0): (384, 2),
    (0, 0, 1): (384, 3),
    (0, 0, 2): (384, 6),
    (0, 1, 1): (384, 2),
    (0, 1, 2): (448, 7),
    (0, 2, 2): (384, 3),
    (0, 2, 3): (448, 4),
    (2, None, None): (1536, 7),
    (2, None, 0): (1152, 18),
    (2, None, 2): (768, 6),
    (2, None, 3): (1152, 9),
    (2, 0, 0): (384, 3),
    (2, 0, 1): (448, 4),
    (2, 0, 2): (384, 6),
    (2, 0, 3): (448, 7),
    (2, 2, 2): (384, 2),
    (2, 2, 3): (384, 3),
    (2, 3, 3): (384, 2),
}


def direct_mask(pattern: PhysicalPattern) -> tuple[int | None, ...]:
    return (None, pattern[1], pattern[2])


def direct_edges(pattern: PhysicalPattern) -> tuple[tuple[int, int], ...]:
    mask = direct_mask(pattern)
    return tuple(
        (row, column)
        for row in range(3)
        for column in range(4)
        if mask[row] != column
    )


def direct_transform_pattern(
    pattern: PhysicalPattern,
    rows: tuple[int, int, int],
    columns: tuple[int, int, int, int],
) -> PhysicalPattern:
    inverse_columns = [0] * 4
    for new_column, old_column in enumerate(columns):
        inverse_columns[old_column] = new_column
    old_mask = direct_mask(pattern)
    new_mask = []
    for new_row in range(3):
        old_balanced = old_mask[rows[new_row]]
        new_mask.append(
            None
            if old_balanced is None
            else inverse_columns[old_balanced]
        )
    return inverse_columns[pattern[0]], new_mask[1], new_mask[2]


def direct_pattern_key(pattern: PhysicalPattern) -> tuple[int, int, int]:
    return (
        pattern[0],
        -1 if pattern[1] is None else pattern[1],
        -1 if pattern[2] is None else pattern[2],
    )


def direct_canonical_pattern(pattern: PhysicalPattern) -> PhysicalPattern:
    return min(
        (
            direct_transform_pattern(pattern, rows, columns)
            for rows in ROW_PERMUTATIONS
            for columns in COLUMN_PERMUTATIONS
        ),
        key=direct_pattern_key,
    )


def direct_distinct(pattern: PhysicalPattern, bits: Bits) -> bool:
    vectors = []
    for column in range(4):
        p_magnitude = 1 if column == pattern[0] else 2
        vectors.append((
            p_magnitude if bits[0, column] else -p_magnitude,
            0 if pattern[1] == column else (
                1 if bits[1, column] else -1
            ),
            0 if pattern[2] == column else (
                1 if bits[2, column] else -1
            ),
        ))
    return all(
        vectors[first] != vectors[second]
        and vectors[first] != tuple(-value for value in vectors[second])
        for first in range(4)
        for second in range(first)
    )


def direct_is_coherent(
    pattern: PhysicalPattern,
    bits: Bits,
    omitted: int,
) -> bool:
    mask = direct_mask(pattern)
    adjacency: dict[int, list[tuple[int, int]]] = {
        vertex: [] for vertex in range(7)
    }
    for row in range(3):
        for column in range(4):
            if column == omitted or mask[row] == column:
                continue
            column_vertex = 3 + column
            adjacency[row].append((column_vertex, bits[row, column]))
            adjacency[column_vertex].append((row, bits[row, column]))

    labels: dict[int, int] = {}
    for root in range(7):
        if root in labels or not adjacency[root]:
            continue
        labels[root] = 0
        queue = [root]
        for vertex in queue:
            for neighbor, edge_bit in adjacency[vertex]:
                required = labels[vertex] ^ edge_bit
                if neighbor in labels:
                    if labels[neighbor] != required:
                        return False
                else:
                    labels[neighbor] = required
                    queue.append(neighbor)
    return True


def direct_canonical_form(pattern: PhysicalPattern, bits: Bits) -> tuple[int, ...]:
    """Enumerate switches explicitly instead of using a spanning forest."""

    best: tuple[int, ...] | None = None
    for rows in ROW_PERMUTATIONS:
        for columns in COLUMN_PERMUTATIONS:
            if direct_transform_pattern(pattern, rows, columns) != pattern:
                continue
            # Fix the first row switch to zero; the omitted global switch is
            # redundant.  The remaining six switches give all 64 gauges.
            for switches in product((0, 1), repeat=6):
                row_switches = (0, switches[0], switches[1])
                column_switches = switches[2:]
                transformed = tuple(
                    bits[rows[row], columns[column]]
                    ^ row_switches[row]
                    ^ column_switches[column]
                    for row, column in direct_edges(pattern)
                )
                if best is None or transformed < best:
                    best = transformed
    if best is None:
        raise AssertionError("a pattern unexpectedly had no automorphism")
    return best


def direct_breakdown() -> dict[PhysicalPattern, tuple[int, int]]:
    patterns = sorted(
        {
            direct_canonical_pattern((special, q_balanced, r_balanced))
            for special in range(4)
            for q_balanced in BALANCED_COLUMNS
            for r_balanced in BALANCED_COLUMNS
        },
        key=direct_pattern_key,
    )
    breakdown: dict[PhysicalPattern, tuple[int, int]] = {}
    for pattern in patterns:
        pattern_edges = direct_edges(pattern)
        surviving = 0
        forms: set[tuple[int, ...]] = set()
        for values in product((0, 1), repeat=len(pattern_edges)):
            bits = dict(zip(pattern_edges, values, strict=True))
            if not direct_distinct(pattern, bits):
                continue
            if any(
                direct_is_coherent(pattern, bits, omitted)
                for omitted in range(4)
            ):
                continue
            surviving += 1
            forms.add(direct_canonical_form(pattern, bits))
        breakdown[pattern] = surviving, len(forms)
    return breakdown


class ThreeBlockP2QRSignatureTests(unittest.TestCase):
    def test_expected_weighted_breakdown(self) -> None:
        actual = {
            result.pattern: (
                result.surviving_assignments,
                len(result.canonical_forms),
            )
            for result in classify_all()
        }
        self.assertEqual(actual, EXPECTED_BREAKDOWN)
        self.assertEqual(sum(classes for _, classes in actual.values()), 134)

    def test_direct_switch_enumeration_matches(self) -> None:
        self.assertEqual(direct_breakdown(), EXPECTED_BREAKDOWN)


if __name__ == "__main__":
    unittest.main()
