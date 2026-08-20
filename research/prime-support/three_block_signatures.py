#!/usr/bin/env python3
"""Classify the binary orientation obstructions for exactly three blocks.

The four columns are the four magic-square offsets.  A row is one rational
prime block.  ``None`` means that the row has no balanced local index; a
column number means that this column is the row's balanced exception.  Bits
record the Gaussian orientation at every nonbalanced incidence.

Row switches, column switches, prime permutations, and (for this incidence-
only classification) arbitrary offset permutations are quotiented out.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import permutations, product


Mask = tuple[int | None, int | None, int | None]
Edge = tuple[int, int]
Bits = dict[Edge, int]

ROW_PERMUTATIONS = tuple(permutations(range(3)))
COLUMN_PERMUTATIONS = tuple(permutations(range(4)))


@dataclass(frozen=True)
class SignatureClass:
    canonical: str
    representatives: int


@dataclass(frozen=True)
class PatternResult:
    name: str
    mask: Mask
    edge_count: int
    surviving_assignments: int
    classes: tuple[SignatureClass, ...]


PATTERNS: tuple[tuple[str, Mask], ...] = (
    ("FFF", (None, None, None)),
    ("FF1", (None, None, 0)),
    ("F11", (None, 0, 0)),
    ("F12", (None, 0, 1)),
    ("111", (0, 0, 0)),
    ("112", (0, 0, 1)),
    ("123", (0, 1, 2)),
)


def edges(mask: Mask, columns: tuple[int, ...] = (0, 1, 2, 3)) -> list[Edge]:
    return [
        (row, column)
        for row in range(3)
        for column in columns
        if mask[row] != column
    ]


def common_factor_is_nontrivial(mask: Mask, omitted_column: int) -> bool:
    """Whether the three retained primitive denominators share a prime."""

    return any(
        missing is None or missing == omitted_column for missing in mask
    )


def is_coherent(mask: Mask, bits: Bits, columns: tuple[int, ...]) -> bool:
    """Test affine separability by propagating vertex switching labels."""

    adjacency: dict[int, list[tuple[int, int]]] = {
        vertex: [] for vertex in range(7)
    }
    for row, column in edges(mask, columns):
        column_vertex = 3 + column
        adjacency[row].append((column_vertex, bits[row, column]))
        adjacency[column_vertex].append((row, bits[row, column]))

    labels: dict[int, int] = {}
    for root in adjacency:
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


def survives_four_relations(mask: Mask, bits: Bits) -> bool:
    """Apply the coherent-orientation obstruction to all four deletions."""

    for omitted in range(4):
        columns = tuple(column for column in range(4) if column != omitted)
        if common_factor_is_nontrivial(mask, omitted) and is_coherent(
            mask, bits, columns
        ):
            return False
    return True


def transformed_mask(
    mask: Mask, row_permutation: tuple[int, ...],
    column_permutation: tuple[int, ...]
) -> Mask:
    inverse_columns = [0] * 4
    for new_column, old_column in enumerate(column_permutation):
        inverse_columns[old_column] = new_column
    return tuple(
        None
        if mask[row_permutation[new_row]] is None
        else inverse_columns[mask[row_permutation[new_row]]]  # type: ignore[index]
        for new_row in range(3)
    )


def automorphisms(mask: Mask) -> list[tuple[tuple[int, ...], tuple[int, ...]]]:
    return [
        (rows, columns)
        for rows in ROW_PERMUTATIONS
        for columns in COLUMN_PERMUTATIONS
        if transformed_mask(mask, rows, columns) == mask
    ]


def transform_bits(
    mask: Mask, bits: Bits, row_permutation: tuple[int, ...],
    column_permutation: tuple[int, ...]
) -> Bits:
    return {
        (new_row, new_column): bits[
            row_permutation[new_row], column_permutation[new_column]
        ]
        for new_row, new_column in edges(mask)
    }


def switching_normal_form(mask: Mask, bits: Bits) -> str:
    """Zero a deterministic spanning forest; remaining bits are cycle parities."""

    adjacency: dict[int, list[tuple[int, int]]] = {
        vertex: [] for vertex in range(7)
    }
    for row, column in edges(mask):
        column_vertex = 3 + column
        adjacency[row].append((column_vertex, bits[row, column]))
        adjacency[column_vertex].append((row, bits[row, column]))
    for neighbors in adjacency.values():
        neighbors.sort()

    switches: dict[int, int] = {}
    for root in range(7):
        if root in switches or not adjacency[root]:
            continue
        switches[root] = 0
        queue = [root]
        for vertex in queue:
            for neighbor, edge_bit in adjacency[vertex]:
                if neighbor not in switches:
                    switches[neighbor] = switches[vertex] ^ edge_bit
                    queue.append(neighbor)

    return "".join(
        str(bits[row, column] ^ switches[row] ^ switches[3 + column])
        for row, column in edges(mask)
    )


def canonical_form(mask: Mask, bits: Bits) -> str:
    return min(
        switching_normal_form(mask, transform_bits(mask, bits, rows, columns))
        for rows, columns in automorphisms(mask)
    )


def render_form(mask: Mask, form: str) -> str:
    normalized = dict(zip(edges(mask), map(int, form), strict=True))
    return "/".join(
        "".join(
            "*" if mask[row] == column else str(normalized[row, column])
            for column in range(4)
        )
        for row in range(3)
    )


def classify_pattern(name: str, mask: Mask) -> PatternResult:
    pattern_edges = edges(mask)
    classes: dict[str, int] = {}
    surviving_assignments = 0
    for values in product((0, 1), repeat=len(pattern_edges)):
        bits = dict(zip(pattern_edges, values, strict=True))
        if not survives_four_relations(mask, bits):
            continue
        surviving_assignments += 1
        canonical = canonical_form(mask, bits)
        classes[canonical] = classes.get(canonical, 0) + 1
    return PatternResult(
        name=name,
        mask=mask,
        edge_count=len(pattern_edges),
        surviving_assignments=surviving_assignments,
        classes=tuple(
            SignatureClass(render_form(mask, canonical), count)
            for canonical, count in sorted(classes.items())
        ),
    )


def classify_all() -> tuple[PatternResult, ...]:
    return tuple(classify_pattern(name, mask) for name, mask in PATTERNS)


def main() -> None:
    for result in classify_all():
        forms = ",".join(item.canonical for item in result.classes)
        print(
            f"pattern={result.name} edges={result.edge_count} "
            f"surviving_assignments={result.surviving_assignments} "
            f"switching_classes={len(result.classes)} forms={forms}"
        )


if __name__ == "__main__":
    main()
