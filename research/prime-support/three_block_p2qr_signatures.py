#!/usr/bin/env python3
"""Classify the weighted intermediate signatures for a ``p^2 q r`` center.

The squared-prime row is distinguished.  Its unique nonunit incidence has
local-index magnitude one, while its other three incidences have extreme
magnitude two.  The two exponent-one rows have magnitude one at every
nonbalanced incidence and may each have one balanced incidence.

The classifier imposes exact nonzero/projective-distinctness of the four
weighted local-index vectors and orientation incoherence for every
three-column deletion.  It then quotients row and column sign switches, the
interchange of the ``q`` and ``r`` rows, and the physical corner and edge
swaps.  It is a necessary-signature classifier, not an existence search.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product

from three_block_signatures import (
    Bits,
    Mask,
    edges,
    is_coherent,
    switching_normal_form,
    transform_bits,
)
from three_block_squarefree import PHYSICAL_COLUMN_PERMUTATIONS


BalancedColumn = int | None
Pattern = tuple[int, BalancedColumn, BalancedColumn]

# The squared-prime row stays in row zero; only the exponent-one rows may be
# interchanged.
ROW_PERMUTATIONS: tuple[tuple[int, int, int], ...] = (
    (0, 1, 2),
    (0, 2, 1),
)
BALANCED_COLUMNS: tuple[BalancedColumn, ...] = (None, 0, 1, 2, 3)


@dataclass(frozen=True)
class WeightedPatternResult:
    pattern: Pattern
    edge_count: int
    surviving_assignments: int
    canonical_forms: tuple[str, ...]


def incidence_mask(pattern: Pattern) -> Mask:
    """Return the binary incidence mask underlying a weighted pattern."""

    return (None, pattern[1], pattern[2])


def transform_pattern(
    pattern: Pattern,
    row_permutation: tuple[int, int, int],
    column_permutation: tuple[int, int, int, int],
) -> Pattern:
    """Apply a physical symmetry to the marker and balanced columns."""

    inverse_columns = [0] * 4
    for new_column, old_column in enumerate(column_permutation):
        inverse_columns[old_column] = new_column

    old_mask = incidence_mask(pattern)
    new_mask: list[BalancedColumn] = []
    for new_row in range(3):
        old_balanced = old_mask[row_permutation[new_row]]
        new_mask.append(
            None
            if old_balanced is None
            else inverse_columns[old_balanced]
        )
    return (
        inverse_columns[pattern[0]],
        new_mask[1],
        new_mask[2],
    )


def pattern_order_key(pattern: Pattern) -> tuple[int, int, int]:
    """Give ``None`` a stable position in pattern sorting."""

    special, q_balanced, r_balanced = pattern
    return (
        special,
        -1 if q_balanced is None else q_balanced,
        -1 if r_balanced is None else r_balanced,
    )


def canonical_pattern(pattern: Pattern) -> Pattern:
    """Canonicalize a marker/mask pattern under exact physical symmetries."""

    return min(
        (
            transform_pattern(pattern, rows, columns)
            for rows in ROW_PERMUTATIONS
            for columns in PHYSICAL_COLUMN_PERMUTATIONS
        ),
        key=pattern_order_key,
    )


def physical_patterns() -> tuple[Pattern, ...]:
    """Return all 22 marker/mask orbits before orientation filtering."""

    return tuple(sorted(
        {
            canonical_pattern((special, q_balanced, r_balanced))
            for special in range(4)
            for q_balanced in BALANCED_COLUMNS
            for r_balanced in BALANCED_COLUMNS
        },
        key=pattern_order_key,
    ))


def weighted_index_vectors(
    pattern: Pattern,
    bits: Bits,
) -> tuple[tuple[int, int, int], ...]:
    """Return the four vectors with row magnitudes ``(2/1, 1, 1)``."""

    special, q_balanced, r_balanced = pattern
    balanced = (None, q_balanced, r_balanced)
    vectors: list[tuple[int, int, int]] = []
    for column in range(4):
        p_magnitude = 1 if column == special else 2
        values = [
            p_magnitude if bits[0, column] else -p_magnitude,
        ]
        for row in (1, 2):
            if balanced[row] == column:
                values.append(0)
            else:
                values.append(1 if bits[row, column] else -1)
        vectors.append(tuple(values))  # type: ignore[arg-type]
    return tuple(vectors)


def has_distinct_projective_vectors(pattern: Pattern, bits: Bits) -> bool:
    """Enforce nonzero offsets and distinct absolute offset magnitudes."""

    vectors = weighted_index_vectors(pattern, bits)
    if any(all(coordinate == 0 for coordinate in vector) for vector in vectors):
        return False
    for first in range(4):
        for second in range(first):
            if vectors[first] == vectors[second]:
                return False
            if vectors[first] == tuple(-value for value in vectors[second]):
                return False
    return True


def survives_required_relations(pattern: Pattern, bits: Bits) -> bool:
    """Apply projective distinctness and all four frustration conditions."""

    if not has_distinct_projective_vectors(pattern, bits):
        return False
    mask = incidence_mask(pattern)
    for omitted in range(4):
        retained = tuple(column for column in range(4) if column != omitted)
        if is_coherent(mask, bits, retained):
            return False
    return True


def automorphisms(
    pattern: Pattern,
) -> tuple[
    tuple[tuple[int, int, int], tuple[int, int, int, int]], ...
]:
    """Return physical symmetries preserving the full weighted pattern."""

    return tuple(
        (rows, columns)
        for rows in ROW_PERMUTATIONS
        for columns in PHYSICAL_COLUMN_PERMUTATIONS
        if transform_pattern(pattern, rows, columns) == pattern
    )


def canonical_form(pattern: Pattern, bits: Bits) -> str:
    """Canonicalize orientations after row and column switching."""

    mask = incidence_mask(pattern)
    return min(
        switching_normal_form(
            mask,
            transform_bits(mask, bits, rows, columns),
        )
        for rows, columns in automorphisms(pattern)
    )


def render_form(pattern: Pattern, form: str) -> str:
    """Render one form while recording the intermediate marker separately."""

    mask = incidence_mask(pattern)
    normalized = dict(zip(edges(mask), map(int, form), strict=True))
    rows = []
    for row in range(3):
        rows.append("".join(
            "*" if mask[row] == column else str(normalized[row, column])
            for column in range(4)
        ))
    return f"I{pattern[0]}:" + "/".join(rows)


def classify_pattern(pattern: Pattern) -> WeightedPatternResult:
    """Classify every orientation assignment for one canonical pattern."""

    mask = incidence_mask(pattern)
    pattern_edges = edges(mask)
    forms: set[str] = set()
    surviving_assignments = 0
    for values in product((0, 1), repeat=len(pattern_edges)):
        bits = dict(zip(pattern_edges, values, strict=True))
        if not survives_required_relations(pattern, bits):
            continue
        surviving_assignments += 1
        forms.add(canonical_form(pattern, bits))
    return WeightedPatternResult(
        pattern=pattern,
        edge_count=len(pattern_edges),
        surviving_assignments=surviving_assignments,
        canonical_forms=tuple(
            render_form(pattern, form) for form in sorted(forms)
        ),
    )


def classify_all() -> tuple[WeightedPatternResult, ...]:
    """Classify all weighted physical patterns."""

    return tuple(classify_pattern(pattern) for pattern in physical_patterns())


def format_balanced(column: BalancedColumn) -> str:
    if column is None:
        return "F"
    return str(column)


def format_pattern(pattern: Pattern) -> str:
    return "/".join((
        f"I{pattern[0]}",
        format_balanced(pattern[1]),
        format_balanced(pattern[2]),
    ))


def main() -> None:
    results = classify_all()
    for result in results:
        print(
            f"pattern={format_pattern(result.pattern)} "
            f"edges={result.edge_count} "
            f"surviving_assignments={result.surviving_assignments} "
            f"switching_classes={len(result.canonical_forms)} "
            f"forms={','.join(result.canonical_forms)}"
        )
    print(
        f"physical_patterns={len(results)} "
        f"surviving_assignments="
        f"{sum(result.surviving_assignments for result in results)} "
        f"switching_classes="
        f"{sum(len(result.canonical_forms) for result in results)}"
    )


if __name__ == "__main__":
    main()
