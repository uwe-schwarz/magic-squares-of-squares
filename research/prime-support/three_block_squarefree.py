#!/usr/bin/env python3
"""Finite sign reduction for the all-unit squarefree three-block case.

After the unique Hadamard orientation normalization, the four signed
projections have coefficient rows

    x + y + z - xyz,
    x + y - z + xyz,
    x - y + z + xyz,
    x - y - z - xyz.

This program assigns their absolute values to ``a,b,a+b,a-b`` in every
possible way, records the resulting two-dimensional equation spaces, and
then quotients by signed permutations of the three prime-block variables.
All arithmetic in the classification is exact.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import permutations, product

from three_block_signatures import (
    Bits,
    Mask,
    edges,
    is_coherent,
    render_form,
    switching_normal_form,
    transform_bits,
    transformed_mask,
)


Row = tuple[Fraction, Fraction, Fraction, Fraction]
RowSpace = tuple[Row, Row]

# Coefficients of x, y, z, xyz in the four signed projections.
PROJECTIONS: tuple[tuple[int, int, int, int], ...] = (
    (1, 1, 1, -1),
    (1, 1, -1, 1),
    (1, -1, 1, 1),
    (1, -1, -1, -1),
)

# Relations c-a-b=0 and d-a+b=0 for roles (a,b,c,d), with a>b>0.
D_RELATIONS: tuple[tuple[int, int, int, int], ...] = (
    (-1, -1, 1, 0),
    (-1, 1, 0, 1),
)

REPRESENTATIVE_A: RowSpace = (
    (Fraction(1), Fraction(0), Fraction(-1), Fraction(-2)),
    (Fraction(0), Fraction(1), Fraction(-2), Fraction(1)),
)

REPRESENTATIVE_B: RowSpace = (
    (
        Fraction(1),
        Fraction(0),
        Fraction(-1, 2),
        Fraction(-1, 2),
    ),
    (
        Fraction(0),
        Fraction(1),
        Fraction(-5, 2),
        Fraction(-1, 2),
    ),
)

# Columns 0,1 are the corners a,b; columns 2,3 are the edges a+b,a-b.
PHYSICAL_COLUMN_PERMUTATIONS: tuple[tuple[int, int, int, int], ...] = tuple(
    corners + edge_pair
    for corners in ((0, 1), (1, 0))
    for edge_pair in ((2, 3), (3, 2))
)
ROW_PERMUTATIONS = tuple(permutations(range(3)))


@dataclass(frozen=True)
class PhysicalPatternResult:
    mask: Mask
    surviving_assignments: int
    canonical_forms: tuple[str, ...]


def reduced_row_space(rows: list[list[int | Fraction]]) -> RowSpace:
    """Return the exact reduced row echelon form of a rank-two matrix."""

    matrix = [[Fraction(value) for value in row] for row in rows]
    pivot_row = 0
    for column in range(4):
        pivot = next(
            (
                row
                for row in range(pivot_row, len(matrix))
                if matrix[row][column]
            ),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        pivot_value = matrix[pivot_row][column]
        matrix[pivot_row] = [
            value / pivot_value for value in matrix[pivot_row]
        ]
        for row in range(len(matrix)):
            if row == pivot_row or not matrix[row][column]:
                continue
            multiplier = matrix[row][column]
            matrix[row] = [
                matrix[row][entry] - multiplier * matrix[pivot_row][entry]
                for entry in range(4)
            ]
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    if pivot_row != 2:
        raise ValueError("the two D relations unexpectedly lost rank")
    return tuple(tuple(row) for row in matrix)  # type: ignore[return-value]


def d_equation_spaces() -> dict[RowSpace, int]:
    """Enumerate all 24 role assignments and all 16 projection signs."""

    spaces: dict[RowSpace, int] = {}
    for role_to_projection in permutations(range(4)):
        for signs in product((-1, 1), repeat=4):
            rows: list[list[int]] = []
            for relation in D_RELATIONS:
                projection_coefficients = [0, 0, 0, 0]
                for role in range(4):
                    projection = role_to_projection[role]
                    projection_coefficients[projection] = (
                        relation[role] * signs[projection]
                    )
                rows.append(
                    [
                        sum(
                            projection_coefficients[projection]
                            * PROJECTIONS[projection][monomial]
                            for projection in range(4)
                        )
                        for monomial in range(4)
                    ]
                )
            space = reduced_row_space(rows)
            spaces[space] = spaces.get(space, 0) + 1
    return spaces


def transform_variables(
    space: RowSpace,
    variable_permutation: tuple[int, int, int],
    signs: tuple[int, int, int],
) -> RowSpace:
    """Apply a signed permutation of x,y,z and the induced sign on xyz."""

    transformed: list[list[Fraction]] = []
    for row in space:
        new_row = [Fraction(0) for _ in range(4)]
        for old_variable in range(3):
            new_row[variable_permutation[old_variable]] += (
                row[old_variable] * signs[old_variable]
            )
        new_row[3] = row[3] * signs[0] * signs[1] * signs[2]
        transformed.append(new_row)
    return reduced_row_space(transformed)


def signed_variable_orbits(
    spaces: set[RowSpace] | None = None,
) -> tuple[frozenset[RowSpace], ...]:
    """Partition equation spaces by prime permutations and conjugations."""

    universe = set(d_equation_spaces()) if spaces is None else set(spaces)
    unseen = set(universe)
    orbits: list[frozenset[RowSpace]] = []
    while unseen:
        seed = min(unseen)
        orbit = {
            transform_variables(seed, permutation, signs)
            for permutation in permutations(range(3))
            for signs in product((-1, 1), repeat=3)
        }
        if not orbit <= universe:
            raise ValueError("signed variable action left the D-equation set")
        unseen -= orbit
        orbits.append(frozenset(orbit))
    return tuple(orbits)


def mask_order_key(mask: Mask) -> tuple[int, int, int]:
    return tuple(-1 if column is None else column for column in mask)


def canonical_physical_mask(mask: Mask) -> Mask:
    """Canonicalize a mask without exchanging corners and edges."""

    return min(
        (
            transformed_mask(mask, rows, columns)
            for rows in ROW_PERMUTATIONS
            for columns in PHYSICAL_COLUMN_PERMUTATIONS
        ),
        key=mask_order_key,
    )


def physical_masks() -> tuple[Mask, ...]:
    """The 16 squarefree balanced-exception masks up to safe symmetries."""

    values: tuple[int | None, ...] = (None, 0, 1, 2, 3)
    return tuple(sorted(
        {
            canonical_physical_mask(mask)  # type: ignore[arg-type]
            for mask in product(values, repeat=3)
        },
        key=mask_order_key,
    ))


def has_distinct_nonzero_orientation_vectors(mask: Mask, bits: Bits) -> bool:
    """Apply exact squarefree offset nonzero-ness and distinctness."""

    vectors = tuple(
        tuple(
            0 if mask[row] == column else (1 if bits[row, column] else -1)
            for row in range(3)
        )
        for column in range(4)
    )
    if any(all(coordinate == 0 for coordinate in vector) for vector in vectors):
        return False
    for first in range(4):
        for second in range(first):
            if vectors[first] == vectors[second] or vectors[first] == tuple(
                -coordinate for coordinate in vectors[second]
            ):
                return False
    return True


def survives_physical_relations(mask: Mask, bits: Bits) -> bool:
    """Require the orientation of each of the four D relations to frustrate."""

    if not has_distinct_nonzero_orientation_vectors(mask, bits):
        return False
    for omitted in range(4):
        columns = tuple(column for column in range(4) if column != omitted)
        # Both coefficient types 111 and 211 are impossible under a coherent
        # orientation.  The latter conclusion uses the square-norm condition
        # on every one-sided Gaussian denominator block.
        if is_coherent(mask, bits, columns):
            return False
    return True


def physical_automorphisms(
    mask: Mask,
) -> tuple[tuple[tuple[int, ...], tuple[int, ...]], ...]:
    return tuple(
        (rows, columns)
        for rows in ROW_PERMUTATIONS
        for columns in PHYSICAL_COLUMN_PERMUTATIONS
        if transformed_mask(mask, rows, columns) == mask
    )


def canonical_physical_form(mask: Mask, bits: Bits) -> str:
    return min(
        switching_normal_form(
            mask, transform_bits(mask, bits, rows, columns)
        )
        for rows, columns in physical_automorphisms(mask)
    )


def classify_physical_masks() -> tuple[PhysicalPatternResult, ...]:
    """Exhaust the exact binary signatures for the physical D columns."""

    results: list[PhysicalPatternResult] = []
    for mask in physical_masks():
        pattern_edges = edges(mask)
        forms: set[str] = set()
        surviving_assignments = 0
        for values in product((0, 1), repeat=len(pattern_edges)):
            bits = dict(zip(pattern_edges, values, strict=True))
            if not survives_physical_relations(mask, bits):
                continue
            surviving_assignments += 1
            canonical = canonical_physical_form(mask, bits)
            forms.add(render_form(mask, canonical))
        results.append(PhysicalPatternResult(
            mask=mask,
            surviving_assignments=surviving_assignments,
            canonical_forms=tuple(sorted(forms)),
        ))
    return tuple(results)


def format_row(row: Row) -> str:
    return "[" + ",".join(str(value) for value in row) + "]"


def main() -> None:
    spaces = d_equation_spaces()
    orbits = signed_variable_orbits(set(spaces))
    print(
        f"raw_assignments={sum(spaces.values())} "
        f"equation_spaces={len(spaces)} "
        f"multiplicities={sorted(set(spaces.values()))} "
        f"signed_variable_orbits={len(orbits)} "
        f"orbit_sizes={sorted(len(orbit) for orbit in orbits)}"
    )
    for name, representative in (
        ("A", REPRESENTATIVE_A),
        ("B", REPRESENTATIVE_B),
    ):
        containing = next(
            orbit for orbit in orbits if representative in orbit
        )
        print(
            f"representative={name} orbit_size={len(containing)} "
            f"rows={format_row(representative[0])};"
            f"{format_row(representative[1])}"
        )
    physical_results = classify_physical_masks()
    for result in physical_results:
        mask = ",".join("F" if item is None else str(item) for item in result.mask)
        print(
            f"mask={mask} surviving_assignments={result.surviving_assignments} "
            f"switching_classes={len(result.canonical_forms)} "
            f"forms={','.join(result.canonical_forms)}"
        )
    total_classes = sum(
        len(result.canonical_forms) for result in physical_results
    )
    remaining_classes = sum(
        len(result.canonical_forms)
        for result in physical_results
        if result.mask != (None, None, None)
    )
    print(
        f"physical_switching_classes={total_classes} "
        f"after_all_unit_exclusion={remaining_classes}"
    )


if __name__ == "__main__":
    main()
