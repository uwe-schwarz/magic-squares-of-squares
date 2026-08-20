#!/usr/bin/env python3
"""Apply the exact monomial filter to the weighted ``p^2 q r`` classes.

The filter combines the three strict block-size inequalities with the
corner-quotient and edge-content inequalities.  It enumerates every extreme
ray of the resulting Farkas certificate cone over exact rational numbers.
It is a necessary-condition filter, not an existence search.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
from functools import cache
from itertools import combinations, product
from math import gcd, lcm

from three_block_p2qr_signatures import Pattern, classify_all


Vector = tuple[int, int, int]
Inequality = tuple[str, Vector, Fraction]
Certificate = tuple[int, ...]
# Exponents of ``2,3,241,433,1201,4201`` in an exact positive constant.
ExactConstant = tuple[
    Fraction, Fraction, Fraction, Fraction, Fraction, Fraction
]
ExactInequality = tuple[str, Vector, ExactConstant]


@dataclass(frozen=True)
class SafeComparison:
    """One aligned quotient that leaves a two-term divisor comparison."""

    aligned_row: int
    divisor_row: int
    remaining_row: int
    omitted_column: int
    family: str
    level: int
    divisor_content: int


@dataclass(frozen=True)
class CompositeComparison:
    """One affinely separable pair of blocks on a retained triple."""

    first_row: int
    second_row: int
    omitted_column: int


@dataclass(frozen=True)
class CommonFactorComparison:
    """One exact common-factor height after three column conjugations."""

    omitted_column: int
    column_signs: tuple[int, int, int]
    plus_minima: Vector
    minus_minima: Vector
    vector: Vector


@dataclass(frozen=True)
class MonomialClassResult:
    pattern: Pattern
    canonical_form: str
    role: tuple[str, str, str]
    edge_contents: tuple[tuple[int, Vector], ...]
    excluded: bool
    certificate: Certificate | None


@dataclass(frozen=True)
class CombinedClassResult:
    """One class after adding every safe aligned-quotient comparison."""

    pattern: Pattern
    canonical_form: str
    role: tuple[str, str, str]
    edge_contents: tuple[tuple[int, Vector], ...]
    comparisons: tuple[SafeComparison, ...]
    excluded: bool
    certificate: Certificate | None
    certificate_bounds: tuple[str, ...] | None
    aggregate_vector: Vector | None
    aggregate_constant: ExactConstant | None


@dataclass(frozen=True)
class FullClassResult:
    """One class after quotient comparisons and composite-block bounds."""

    pattern: Pattern
    canonical_form: str
    role: tuple[str, str, str]
    edge_contents: tuple[tuple[int, Vector], ...]
    comparisons: tuple[SafeComparison, ...]
    composites: tuple[CompositeComparison, ...]
    excluded: bool
    certificate: Certificate | None
    certificate_bounds: tuple[str, ...] | None
    aggregate_vector: Vector | None
    aggregate_constant: ExactConstant | None


@dataclass(frozen=True)
class CompleteClassResult:
    """One class after the general exact common-factor height filter."""

    pattern: Pattern
    canonical_form: str
    role: tuple[str, str, str]
    edge_contents: tuple[tuple[int, Vector], ...]
    comparisons: tuple[SafeComparison, ...]
    composites: tuple[CompositeComparison, ...]
    common_factors: tuple[CommonFactorComparison, ...]
    excluded: bool
    certificate: Certificate | None
    certificate_bounds: tuple[str, ...] | None
    aggregate_vector: Vector | None
    aggregate_constant: ExactConstant | None


@dataclass(frozen=True)
class GeneralizedClassResult:
    """One class after every coupled-conjugation divisor comparison."""

    pattern: Pattern
    canonical_form: str
    role: tuple[str, str, str]
    edge_contents: tuple[tuple[int, Vector], ...]
    comparisons: tuple[SafeComparison, ...]
    generalized_comparisons: tuple[SafeComparison, ...]
    composites: tuple[CompositeComparison, ...]
    common_factors: tuple[CommonFactorComparison, ...]
    excluded: bool
    certificate: Certificate | None
    certificate_bounds: tuple[str, ...] | None
    aggregate_vector: Vector | None
    aggregate_constant: ExactConstant | None


@dataclass(frozen=True)
class SharpAxisClassResult:
    """One class after the factorized even-level axis bounds."""

    pattern: Pattern
    canonical_form: str
    role: tuple[str, str, str]
    edge_contents: tuple[tuple[int, Vector], ...]
    comparisons: tuple[SafeComparison, ...]
    generalized_comparisons: tuple[SafeComparison, ...]
    sharp_axis_comparisons: tuple[SafeComparison, ...]
    composites: tuple[CompositeComparison, ...]
    common_factors: tuple[CommonFactorComparison, ...]
    excluded: bool
    certificate: Certificate | None
    certificate_bounds: tuple[str, ...] | None
    aggregate_vector: Vector | None
    aggregate_constant: ExactConstant | None


@dataclass(frozen=True)
class SharpSkewClassResult:
    """One class after the congruence-sharpened skew bounds."""

    pattern: Pattern
    canonical_form: str
    role: tuple[str, str, str]
    edge_contents: tuple[tuple[int, Vector], ...]
    comparisons: tuple[SafeComparison, ...]
    generalized_comparisons: tuple[SafeComparison, ...]
    sharp_axis_comparisons: tuple[SafeComparison, ...]
    sharp_skew_comparisons: tuple[SafeComparison, ...]
    composites: tuple[CompositeComparison, ...]
    common_factors: tuple[CommonFactorComparison, ...]
    excluded: bool
    certificate: Certificate | None
    certificate_bounds: tuple[str, ...] | None
    aggregate_vector: Vector | None
    aggregate_constant: ExactConstant | None


@dataclass(frozen=True)
class PrimeLowerClassResult:
    """One class after discrete congruence lower bounds on its primes."""

    pattern: Pattern
    canonical_form: str
    role: tuple[str, str, str]
    edge_contents: tuple[tuple[int, Vector], ...]
    comparisons: tuple[SafeComparison, ...]
    generalized_comparisons: tuple[SafeComparison, ...]
    sharp_axis_comparisons: tuple[SafeComparison, ...]
    sharp_skew_comparisons: tuple[SafeComparison, ...]
    composites: tuple[CompositeComparison, ...]
    common_factors: tuple[CommonFactorComparison, ...]
    prime_lower_bounds: Vector
    excluded: bool
    certificate: Certificate | None
    certificate_bounds: tuple[str, ...] | None
    aggregate_vector: Vector | None
    aggregate_constant: ExactConstant | None


@dataclass(frozen=True)
class ArithmeticClassResult:
    """One class after the complementary-axis arithmetic descent."""

    pattern: Pattern
    canonical_form: str
    role: tuple[str, str, str]
    previous_excluded: bool
    complementary_axis_descent: bool
    excluded: bool


def exception_type(column: int | None) -> str:
    """Return ``C``, ``E``, or ``F`` for one row's local pattern."""

    if column is None:
        return "F"
    return "C" if column < 2 else "E"


def parse_form(form: str) -> list[list[int]]:
    """Decode rendered bits as signs, with a balanced incidence equal to 0."""

    rows = form.split(":", 1)[1].split("/")
    return [
        [
            0 if value == "*" else (1 if value == "1" else -1)
            for value in row
        ]
        for row in rows
    ]


def local_indices(pattern: Pattern, form: str) -> list[list[int]]:
    """Restore the actual local-index magnitudes, not merely their signs."""

    signs = parse_form(form)
    intermediate = pattern[0]
    result: list[list[int]] = []
    for row, row_signs in enumerate(signs):
        values = []
        for column, sign in enumerate(row_signs):
            if sign == 0:
                values.append(0)
            elif row == 0:
                values.append(
                    sign * (1 if column == intermediate else 2)
                )
            else:
                values.append(sign)
        result.append(values)
    return result


def edge_content_exponents(
    pattern: Pattern,
    form: str,
    exceptional_row: int,
) -> Vector:
    """Return ``v_p(delta), v_q(delta), v_r(delta)`` for an edge row."""

    indices = local_indices(pattern, form)
    alignment = tuple(
        1 if indices[exceptional_row][column] > 0 else -1
        for column in (0, 1)
    )
    exponents = (2, 1, 1)
    values = tuple(
        2 * exponent
        - abs(
            alignment[0] * indices[row][0]
            - alignment[1] * indices[row][1]
        )
        for row, exponent in enumerate(exponents)
    )
    return values  # type: ignore[return-value]


def inequalities(pattern: Pattern, form: str) -> tuple[Inequality, ...]:
    """Encode every bound as ``A dot log_2(p,q,r) < c``."""

    result: list[Inequality] = [
        ("D_p", (2, -1, -1), Fraction(0)),
        ("D_q", (-2, 1, -1), Fraction(0)),
        ("D_r", (-2, -1, 1), Fraction(0)),
    ]
    for row, column in enumerate(pattern):
        if column is None:
            continue
        if column < 2:
            vector = [-2, -1, -1]
            vector[row] = 4 if row == 0 else 3
            result.append((
                f"C_{'pqr'[row]}",
                tuple(vector),  # type: ignore[arg-type]
                Fraction(1, 2),
            ))
            continue

        content = edge_content_exponents(pattern, form, row)
        vector = [content[0] - 4, content[1] - 2, content[2] - 2]
        vector[row] = 4
        result.append((
            f"E_{'pqr'[row]}{content}",
            tuple(vector),  # type: ignore[arg-type]
            Fraction(1),
        ))
    return tuple(result)


def relation_coefficients(omitted_column: int) -> tuple[int, int, int, int]:
    """Return coefficient magnitudes for one three-offset relation."""

    if omitted_column >= 2:
        return tuple(
            0 if column == omitted_column else 1 for column in range(4)
        )  # type: ignore[return-value]
    doubled_column = 1 - omitted_column
    return tuple(
        0
        if column == omitted_column
        else (2 if column == doubled_column else 1)
        for column in range(4)
    )  # type: ignore[return-value]


def safe_comparisons(
    pattern: Pattern,
    form: str,
) -> tuple[SafeComparison, ...]:
    """Enumerate aligned quotients with a nonzero two-term comparison.

    The aligned row is extreme with one orientation on all three retained
    columns.  The divisor row contributes its exceptional column and two
    equally oriented extremes.  Cancelling its common Gaussian factor
    leaves two terms from the remaining row.  Opposite extreme orientations,
    or an exceptional incidence in that pair, make the remaining factor a
    nonzero axis or skew expression.
    """

    bits = parse_form(form)
    special = pattern
    comparisons: list[SafeComparison] = []
    for omitted in range(4):
        retained = tuple(column for column in range(4) if column != omitted)
        coefficients = relation_coefficients(omitted)
        for aligned in range(3):
            if special[aligned] in retained:
                continue
            aligned_bits = tuple(bits[aligned][column] for column in retained)
            if 0 in aligned_bits or len(set(aligned_bits)) != 1:
                continue

            for divisor in range(3):
                divisor_special = special[divisor]
                if (
                    divisor == aligned
                    or divisor_special is None
                    or divisor_special not in retained
                ):
                    continue
                pair = tuple(
                    column
                    for column in retained
                    if column != divisor_special
                )
                pair_bits = tuple(bits[divisor][column] for column in pair)
                if 0 in pair_bits or len(set(pair_bits)) != 1:
                    continue

                remaining = 3 - aligned - divisor
                remaining_special = special[remaining]
                pair_coefficients = sorted(
                    coefficients[column] for column in pair
                )
                family = "S" if pair_coefficients == [1, 2] else "A"

                if remaining_special in pair:
                    if remaining == 0:
                        other = next(
                            column
                            for column in pair
                            if column != remaining_special
                        )
                        level = (
                            2
                            if bits[remaining][remaining_special]
                            == bits[remaining][other]
                            else 6
                        )
                    else:
                        level = 2
                elif bits[remaining][pair[0]] != bits[remaining][pair[1]]:
                    level = 8 if remaining == 0 else 4
                else:
                    # Equal associates with equal coefficients could cancel;
                    # no unconditional divisor comparison follows.  A skew
                    # pair cannot occur here: it would instead be an immediate
                    # coprime-support contradiction.
                    continue

                divisor_content = 2
                if divisor == 0:
                    divisor_content = (
                        6
                        if bits[divisor][divisor_special]
                        == bits[divisor][pair[0]]
                        else 2
                    )
                comparisons.append(SafeComparison(
                    aligned_row=aligned,
                    divisor_row=divisor,
                    remaining_row=remaining,
                    omitted_column=omitted,
                    family=family,
                    level=level,
                    divisor_content=divisor_content,
                ))
    return tuple(comparisons)


def generalized_comparisons(
    pattern: Pattern,
    form: str,
) -> tuple[SafeComparison, ...]:
    """Enumerate safe divisor comparisons after all coupled conjugations.

    This implementation uses actual local exponents rather than binary
    special cases.  It therefore derives levels 2, 4, 6, and 8 directly
    from the two remaining Gaussian monomials.
    """

    indices = local_indices(pattern, form)
    block_exponents = (2, 1, 1)
    result: set[SafeComparison] = set()
    for omitted in range(4):
        retained = tuple(column for column in range(4) if column != omitted)
        coefficients = relation_coefficients(omitted)
        for tail in product((1, -1), repeat=2):
            column_signs = (1,) + tail
            transformed = [
                [
                    column_signs[index] * indices[row][column]
                    for index, column in enumerate(retained)
                ]
                for row in range(3)
            ]
            for aligned, exponent in enumerate(block_exponents):
                if any(
                    abs(value) != exponent for value in transformed[aligned]
                ):
                    continue
                if len(set(transformed[aligned])) != 1:
                    continue

                for divisor, divisor_exponent in enumerate(block_exponents):
                    divisor_special = pattern[divisor]
                    if (
                        divisor == aligned
                        or divisor_special is None
                        or divisor_special not in retained
                    ):
                        continue
                    special_index = retained.index(divisor_special)
                    pair_indices = tuple(
                        index
                        for index in range(3)
                        if index != special_index
                    )
                    pair_values = tuple(
                        transformed[divisor][index]
                        for index in pair_indices
                    )
                    if any(
                        abs(value) != divisor_exponent
                        for value in pair_values
                    ):
                        continue
                    if len(set(pair_values)) != 1:
                        continue

                    divisor_plus = min(
                        2 * divisor_exponent + 2 * value
                        for value in transformed[divisor]
                    )
                    divisor_minus = min(
                        2 * divisor_exponent - 2 * value
                        for value in transformed[divisor]
                    )
                    if min(divisor_plus, divisor_minus) != 0:
                        raise AssertionError("divisor content must be one-sided")
                    divisor_content = max(divisor_plus, divisor_minus)

                    remaining = 3 - aligned - divisor
                    remaining_exponent = block_exponents[remaining]
                    monomials = []
                    for index in pair_indices:
                        value = transformed[remaining][index]
                        monomials.append((
                            2 * remaining_exponent + 2 * value,
                            2 * remaining_exponent - 2 * value,
                        ))
                    common_plus = min(value[0] for value in monomials)
                    common_minus = min(value[1] for value in monomials)
                    residual = tuple(
                        (plus - common_plus, minus - common_minus)
                        for plus, minus in monomials
                    )
                    pair_columns = tuple(retained[index] for index in pair_indices)
                    pair_coefficients = sorted(
                        coefficients[column] for column in pair_columns
                    )
                    family = "S" if pair_coefficients == [1, 2] else "A"

                    if residual[0] == residual[1]:
                        if family == "S":
                            raise AssertionError(
                                "a skew equal-monomial pair is immediately "
                                "inconsistent"
                            )
                        continue
                    level = sum(residual[0])
                    if (
                        level <= 0
                        or sum(residual[1]) != level
                        or set(residual) != {(level, 0), (0, level)}
                    ):
                        raise AssertionError(
                            "remaining factors must be conjugate monomials"
                        )
                    result.add(SafeComparison(
                        aligned_row=aligned,
                        divisor_row=divisor,
                        remaining_row=remaining,
                        omitted_column=omitted,
                        family=family,
                        level=level,
                        divisor_content=divisor_content,
                    ))

    return tuple(sorted(
        result,
        key=lambda value: (
            value.aligned_row,
            value.divisor_row,
            value.remaining_row,
            value.omitted_column,
            value.family,
            value.level,
            value.divisor_content,
        ),
    ))


def comparison_inequality(comparison: SafeComparison) -> ExactInequality:
    """Encode the axis/skew divisor comparison as an exact monomial bound."""

    vector = [0, 0, 0]
    vector[comparison.divisor_row] = (
        2 if comparison.family == "A" else 1
    )
    vector[comparison.remaining_row] -= comparison.level // 2
    name = (
        f"{comparison.family}{comparison.level}_"
        f"{'pqr'[comparison.divisor_row]}_"
        f"{'pqr'[comparison.remaining_row]}"
    )
    constant = tuple(Fraction(0) for _ in range(6))
    return name, tuple(vector), constant  # type: ignore[arg-type]


def sharp_axis_inequality(comparison: SafeComparison) -> ExactInequality:
    """Encode the factorized bound for an even-level axis comparison.

    If ``b^2`` divides a nonzero coordinate of ``gamma^d``, put
    ``gamma^(d/2) = X + iY``.  The coordinate of its square factors as
    ``(X-Y)(X+Y)`` or ``2XY``.  The odd prime ``b`` can divide only one
    factor, so ``b^2 < sqrt(2) c^(d/4)``.  Raising to the fourth power
    gives the integral encoding ``b^8 < 4 c^d`` used here.
    """

    if comparison.family != "A" or comparison.level % 2:
        raise ValueError("the sharp axis bound requires even-level A_d")
    vector = [0, 0, 0]
    vector[comparison.divisor_row] = 8
    vector[comparison.remaining_row] = -comparison.level
    name = (
        f"A{comparison.level}_sharp_"
        f"{'pqr'[comparison.divisor_row]}_"
        f"{'pqr'[comparison.remaining_row]}"
    )
    constant = (
        Fraction(2), Fraction(0), Fraction(0), Fraction(0), Fraction(0),
        Fraction(0),
    )
    return name, tuple(vector), constant  # type: ignore[arg-type]


def sharp_skew_inequality(comparison: SafeComparison) -> ExactInequality:
    """Encode the level-specific norm gap for an even-level skew event."""

    if comparison.family != "S" or comparison.level % 2:
        raise ValueError("the sharp skew bound requires even-level S_d")
    vector = [0, 0, 0]
    vector[comparison.divisor_row] = 2
    vector[comparison.remaining_row] = -comparison.level
    name = (
        f"S{comparison.level}_sharp_"
        f"{'pqr'[comparison.divisor_row]}_"
        f"{'pqr'[comparison.remaining_row]}"
    )
    gap_index = {2: 2, 6: 3, 4: 4, 8: 5}[comparison.level]
    constant = [Fraction(0)] * 6
    constant[1] = Fraction(2)
    constant[gap_index] = Fraction(-1)
    return name, tuple(vector), tuple(constant)  # type: ignore[return-value,arg-type]


def quotient_inequality(comparison: SafeComparison) -> ExactInequality:
    """Encode the height left after the divisor row's rational content."""

    aligned = comparison.aligned_row
    divisor = comparison.divisor_row
    remaining = comparison.remaining_row
    vector = [0, 0, 0]

    if aligned == 0:
        # The aligned p^2 block gives p^4 |H quotient| < K(B C)^2.
        # The balanced exponent-one divisor contributes B^2 to the quotient.
        vector[0] = 4
        vector[remaining] = -2
    elif divisor == 0:
        # At I and the two equally oriented p-extremes the squared local
        # factors have common content pi^6 (or pi^2 in the opposite case).
        # Rationality adds the conjugate content before the height estimate.
        vector[0] = comparison.divisor_content - 4
        vector[aligned] = 2
        vector[remaining] = -2
    else:
        # Two exponent-one rows leave p^2 as the third block.
        vector[aligned] = 2
        vector[0] = -4

    constant = (
        (
            Fraction(0), Fraction(1), Fraction(0), Fraction(0),
            Fraction(0), Fraction(0),
        )
        if comparison.omitted_column >= 2
        else (
            Fraction(1), Fraction(0), Fraction(0), Fraction(0),
            Fraction(0), Fraction(0),
        )
    )
    name = (
        f"Q_{'pqr'[aligned]}_{'pqr'[divisor]}_"
        f"o{comparison.omitted_column}"
    )
    return name, tuple(vector), constant  # type: ignore[arg-type]


def exact_inequalities(
    pattern: Pattern,
    form: str,
) -> tuple[ExactInequality, ...]:
    """Combine universal and safe quotient bounds with exact constants.

    The constant tuple stores exponents of ``2,3,241,433,1201,4201``.
    Duplicate monomial bounds are removed without discarding comparison
    events from the independently auditable event count.
    """

    result: list[ExactInequality] = [
        (
            name,
            vector,
            (
                constant,
                Fraction(0),
                Fraction(0),
                Fraction(0),
                Fraction(0),
                Fraction(0),
            ),
        )
        for name, vector, constant in inequalities(pattern, form)
    ]
    for comparison in safe_comparisons(pattern, form):
        result.append(comparison_inequality(comparison))
        result.append(quotient_inequality(comparison))

    unique: list[ExactInequality] = []
    seen: set[tuple[Vector, ExactConstant]] = set()
    for bound in result:
        key = (bound[1], bound[2])
        if key in seen:
            continue
        seen.add(key)
        unique.append(bound)
    return tuple(unique)


def composite_comparisons(
    pattern: Pattern,
    form: str,
) -> tuple[CompositeComparison, ...]:
    """Enumerate every affinely separable two-row extreme triple."""

    bits = parse_form(form)
    result: list[CompositeComparison] = []
    for omitted in range(4):
        retained = tuple(column for column in range(4) if column != omitted)
        for first, second in combinations(range(3), 2):
            if pattern[first] not in (None, omitted):
                continue
            if pattern[second] not in (None, omitted):
                continue
            if any(
                bits[row][column] == 0
                for row in (first, second)
                for column in retained
            ):
                continue
            relative = {
                bits[first][column] * bits[second][column]
                for column in retained
            }
            if len(relative) != 1:
                continue
            result.append(CompositeComparison(first, second, omitted))
    return tuple(result)


def composite_inequality(comparison: CompositeComparison) -> ExactInequality:
    """Encode ``(block_s block_t)^2 < K block_u^2``."""

    exponents = (2, 1, 1)
    remaining = 3 - comparison.first_row - comparison.second_row
    vector = [0, 0, 0]
    vector[comparison.first_row] = 2 * exponents[comparison.first_row]
    vector[comparison.second_row] = 2 * exponents[comparison.second_row]
    vector[remaining] = -2 * exponents[remaining]
    constant = (
        (
            Fraction(0), Fraction(1), Fraction(0), Fraction(0),
            Fraction(0), Fraction(0),
        )
        if comparison.omitted_column >= 2
        else (
            Fraction(1), Fraction(0), Fraction(0), Fraction(0),
            Fraction(0), Fraction(0),
        )
    )
    name = (
        f"G{comparison.omitted_column}_"
        f"{comparison.first_row}{comparison.second_row}"
    )
    return name, tuple(vector), constant  # type: ignore[arg-type]


def full_inequalities(
    pattern: Pattern,
    form: str,
) -> tuple[ExactInequality, ...]:
    """Add every safe two-row composite-block bound to the combined stage."""

    result = list(exact_inequalities(pattern, form))
    seen = {(bound[1], bound[2]) for bound in result}
    for comparison in composite_comparisons(pattern, form):
        bound = composite_inequality(comparison)
        key = (bound[1], bound[2])
        if key in seen:
            continue
        seen.add(key)
        result.append(bound)
    return tuple(result)


def common_factor_comparisons(
    pattern: Pattern,
    form: str,
) -> tuple[CommonFactorComparison, ...]:
    """Enumerate all exact common factors for every retained triple.

    Independent conjugation of three columns has four patterns modulo the
    simultaneous global flip.  For each rational-prime row, the minima of
    the two local Gaussian exponents give the full common divisor.
    """

    indices = local_indices(pattern, form)
    block_exponents = (2, 1, 1)
    result = []
    for omitted in range(4):
        retained = tuple(column for column in range(4) if column != omitted)
        for tail in product((1, -1), repeat=2):
            column_signs = (1,) + tail
            plus_minima = []
            minus_minima = []
            vector = []
            for row, exponent in enumerate(block_exponents):
                oriented = tuple(
                    column_signs[index] * indices[row][column]
                    for index, column in enumerate(retained)
                )
                plus = min(2 * exponent + 2 * value for value in oriented)
                minus = min(2 * exponent - 2 * value for value in oriented)
                plus_minima.append(plus)
                minus_minima.append(minus)
                vector.append(max(plus, minus) - 2 * exponent)
            result.append(CommonFactorComparison(
                omitted_column=omitted,
                column_signs=column_signs,
                plus_minima=tuple(plus_minima),  # type: ignore[arg-type]
                minus_minima=tuple(minus_minima),  # type: ignore[arg-type]
                vector=tuple(vector),  # type: ignore[arg-type]
            ))
    return tuple(result)


def common_factor_inequality(
    comparison: CommonFactorComparison,
) -> ExactInequality:
    """Encode the general common-factor height as a monomial bound."""

    constant = (
        (
            Fraction(0), Fraction(1), Fraction(0), Fraction(0),
            Fraction(0), Fraction(0),
        )
        if comparison.omitted_column >= 2
        else (
            Fraction(1), Fraction(0), Fraction(0), Fraction(0),
            Fraction(0), Fraction(0),
        )
    )
    signs = "".join("+" if sign == 1 else "-" for sign in comparison.column_signs)
    return (
        f"H{comparison.omitted_column}_{signs}",
        comparison.vector,
        constant,
    )


def complete_inequalities(
    pattern: Pattern,
    form: str,
) -> tuple[ExactInequality, ...]:
    """Add all exact common-factor heights to every preceding bound."""

    result = list(full_inequalities(pattern, form))
    seen = {(bound[1], bound[2]) for bound in result}
    for comparison in common_factor_comparisons(pattern, form):
        bound = common_factor_inequality(comparison)
        key = (bound[1], bound[2])
        if key in seen:
            continue
        seen.add(key)
        result.append(bound)
    return tuple(result)


def generalized_inequalities(
    pattern: Pattern,
    form: str,
) -> tuple[ExactInequality, ...]:
    """Add all coupled-conjugation quotient and divisor comparisons."""

    result = list(complete_inequalities(pattern, form))
    seen = {(bound[1], bound[2]) for bound in result}
    for comparison in generalized_comparisons(pattern, form):
        for bound in (
            comparison_inequality(comparison),
            quotient_inequality(comparison),
        ):
            key = (bound[1], bound[2])
            if key in seen:
                continue
            seen.add(key)
            result.append(bound)
    return tuple(result)


def sharp_axis_inequalities(
    pattern: Pattern,
    form: str,
) -> tuple[ExactInequality, ...]:
    """Add the factorized bound for every generalized axis event."""

    result = list(generalized_inequalities(pattern, form))
    seen = {(bound[1], bound[2]) for bound in result}
    for comparison in generalized_comparisons(pattern, form):
        if comparison.family != "A":
            continue
        bound = sharp_axis_inequality(comparison)
        key = (bound[1], bound[2])
        if key in seen:
            continue
        seen.add(key)
        result.append(bound)
    return tuple(result)


def sharp_skew_inequalities(
    pattern: Pattern,
    form: str,
) -> tuple[ExactInequality, ...]:
    """Add the congruence-sharpened bound for every skew event."""

    result = list(sharp_axis_inequalities(pattern, form))
    seen = {(bound[1], bound[2]) for bound in result}
    for comparison in generalized_comparisons(pattern, form):
        if comparison.family != "S":
            continue
        bound = sharp_skew_inequality(comparison)
        key = (bound[1], bound[2])
        if key in seen:
            continue
        seen.add(key)
        result.append(bound)
    return tuple(result)


def prime_lower_bounds(pattern: Pattern, form: str) -> Vector:
    """Return safe discrete lower bounds for the three center primes.

    An edge-exceptional base is ``1 mod 8``.  A skew comparison also makes
    ``+2`` or ``-2`` a ``d``-th power modulo its divisor base.  Levels 2
    and 6 therefore force a base of at least 17.  At levels 4 and 8, the
    candidates 17 and 41 fail the fourth-power test, so the base is at
    least 73.
    """

    result = [
        17 if exception_type(column) == "E" else 5
        for column in pattern
    ]
    for comparison in generalized_comparisons(pattern, form):
        if comparison.family != "S":
            continue
        lower = 73 if comparison.level in (4, 8) else 17
        result[comparison.divisor_row] = max(
            result[comparison.divisor_row], lower
        )
    return tuple(result)  # type: ignore[return-value]


def _one_dimensional_null_vector(
    matrix: list[list[int]], dimension: int
) -> list[Fraction] | None:
    """Return a null vector iff the matrix has rank ``dimension - 1``."""

    data = [[Fraction(value) for value in row] for row in matrix]
    pivot_columns: list[int] = []
    pivot_row = 0
    for column in range(dimension):
        nonzero = next(
            (
                row
                for row in range(pivot_row, len(data))
                if data[row][column]
            ),
            None,
        )
        if nonzero is None:
            continue
        data[pivot_row], data[nonzero] = data[nonzero], data[pivot_row]
        pivot = data[pivot_row][column]
        data[pivot_row] = [value / pivot for value in data[pivot_row]]
        for row in range(len(data)):
            if row == pivot_row or not data[row][column]:
                continue
            multiplier = data[row][column]
            data[row] = [
                data[row][index]
                - multiplier * data[pivot_row][index]
                for index in range(dimension)
            ]
        pivot_columns.append(column)
        pivot_row += 1
    if pivot_row != dimension - 1:
        return None

    free_column = next(
        column
        for column in range(dimension)
        if column not in pivot_columns
    )
    vector = [Fraction(0)] * dimension
    vector[free_column] = 1
    for row, column in enumerate(pivot_columns):
        vector[column] = -data[row][free_column]
    return vector


def _primitive_integer_vector(
    values: list[Fraction],
) -> Certificate:
    denominator = 1
    for value in values:
        denominator = lcm(denominator, value.denominator)
    integers = [int(value * denominator) for value in values]
    divisor = 0
    for value in integers:
        divisor = gcd(divisor, value)
    return tuple(value // divisor for value in integers)


def extreme_rays(bounds: tuple[Inequality, ...]) -> tuple[Certificate, ...]:
    """Enumerate rays ``lambda >= 0`` with ``sum lambda_i A_i >= 0``."""

    dimension = len(bounds)
    rays: set[Certificate] = set()
    # An extreme ray with ``m`` positive multipliers needs ``m - 1``
    # independent active output coordinates.  There are only three output
    # coordinates, so every ray has support at most four.  Enumerating those
    # small supports is equivalent to choosing ``dimension - 1`` active
    # facets in the full cone and is much faster once many safe bounds exist.
    for support_size in range(1, min(4, dimension) + 1):
        for support in combinations(range(dimension), support_size):
            for active_coordinates in combinations(
                range(3), support_size - 1
            ):
                restricted = [
                    [bounds[index][1][coordinate] for index in support]
                    for coordinate in active_coordinates
                ]
                vector = _one_dimensional_null_vector(
                    restricted, support_size
                )
                if vector is None:
                    continue
                for sign in (1, -1):
                    positive = [sign * value for value in vector]
                    if not all(value > 0 for value in positive):
                        continue
                    candidate = [Fraction(0)] * dimension
                    for index, value in zip(support, positive, strict=True):
                        candidate[index] = value
                    output = tuple(
                        sum(
                            candidate[index]
                            * bounds[index][1][coordinate]
                            for index in range(dimension)
                        )
                        for coordinate in range(3)
                    )
                    if all(value >= 0 for value in output):
                        rays.add(_primitive_integer_vector(candidate))
                        break
    return tuple(sorted(rays))


def is_contradiction(
    bounds: tuple[Inequality, ...], weights: Certificate
) -> bool:
    """Test ``5^(sum v) >= 2^(sum lambda*c)`` using exact integers."""

    output = tuple(
        sum(
            weights[index] * bounds[index][1][coordinate]
            for index in range(len(bounds))
        )
        for coordinate in range(3)
    )
    if not all(value >= 0 for value in output):
        return False
    exponent_sum = sum(output)
    twice_constant = sum(
        weights[index] * 2 * bounds[index][2]
        for index in range(len(bounds))
    )
    if twice_constant.denominator != 1:
        raise AssertionError("the constants must be half-integral")
    return 5 ** (2 * exponent_sum) >= 2 ** int(twice_constant)


def exact_is_contradiction(
    bounds: tuple[ExactInequality, ...],
    weights: Certificate,
) -> bool:
    """Test a certificate over the five supported constant primes."""

    return exact_is_contradiction_with_lower_bounds(
        bounds, weights, (5, 5, 5)
    )


def exact_is_contradiction_with_lower_bounds(
    bounds: tuple[ExactInequality, ...],
    weights: Certificate,
    lower_bounds: Vector,
) -> bool:
    """Test an exact certificate using per-coordinate prime floors."""

    output = tuple(
        sum(
            weights[index] * bounds[index][1][coordinate]
            for index in range(len(bounds))
        )
        for coordinate in range(3)
    )
    if not all(value >= 0 for value in output):
        return False
    exponents = tuple(
        sum(
            weights[index] * bounds[index][2][prime_index]
            for index in range(len(bounds))
        )
        for prime_index in range(6)
    )
    denominator = 1
    for exponent in exponents:
        denominator = lcm(denominator, exponent.denominator)
    left = 1
    for lower, exponent in zip(lower_bounds, output, strict=True):
        left *= lower ** int(denominator * exponent)
    right = 1
    for prime, exponent in zip(
        (2, 3, 241, 433, 1201, 4201), exponents, strict=True
    ):
        integral_exponent = int(denominator * exponent)
        if integral_exponent < 0:
            left *= prime ** -integral_exponent
        else:
            right *= prime ** integral_exponent
    return left >= right


def exact_extreme_rays(
    bounds: tuple[ExactInequality, ...],
) -> tuple[Certificate, ...]:
    """Reuse the rational cone enumeration; constants do not define it."""

    projected = tuple(
        (name, vector, Fraction(0)) for name, vector, _ in bounds
    )
    return extreme_rays(projected)


def certificate_aggregate(
    bounds: tuple[ExactInequality, ...],
    weights: Certificate,
) -> tuple[Vector, ExactConstant]:
    """Return the monomial vector and exact right-side constant."""

    vector = tuple(
        sum(
            weights[index] * bounds[index][1][coordinate]
            for index in range(len(bounds))
        )
        for coordinate in range(3)
    )
    constant = tuple(
        sum(
            weights[index] * bounds[index][2][constant_index]
            for index in range(len(bounds))
        )
        for constant_index in range(6)
    )
    return vector, constant  # type: ignore[return-value]


@cache
def classify_monomial_filter() -> tuple[MonomialClassResult, ...]:
    """Classify all 134 canonical forms under the exact monomial filter."""

    results = []
    for pattern_result in classify_all():
        for form in pattern_result.canonical_forms:
            bounds = inequalities(pattern_result.pattern, form)
            certificates = tuple(
                ray
                for ray in extreme_rays(bounds)
                if is_contradiction(bounds, ray)
            )
            edge_contents = tuple(
                (
                    row,
                    edge_content_exponents(
                        pattern_result.pattern, form, row
                    ),
                )
                for row, column in enumerate(pattern_result.pattern)
                if exception_type(column) == "E"
            )
            results.append(MonomialClassResult(
                pattern=pattern_result.pattern,
                canonical_form=form,
                role=tuple(
                    exception_type(column)
                    for column in pattern_result.pattern
                ),  # type: ignore[arg-type]
                edge_contents=edge_contents,
                excluded=bool(certificates),
                certificate=certificates[0] if certificates else None,
            ))
    return tuple(results)


@cache
def classify_combined_filter() -> tuple[CombinedClassResult, ...]:
    """Classify all forms after every safe aligned-quotient comparison."""

    base_results = {
        result.canonical_form: result for result in classify_monomial_filter()
    }
    results = []
    for pattern_result in classify_all():
        for form in pattern_result.canonical_forms:
            bounds = exact_inequalities(pattern_result.pattern, form)
            certificate = next(
                (
                    ray
                    for ray in exact_extreme_rays(bounds)
                    if exact_is_contradiction(bounds, ray)
                ),
                None,
            )
            aggregate_vector = None
            aggregate_constant = None
            certificate_bounds = None
            if certificate is not None:
                aggregate_vector, aggregate_constant = certificate_aggregate(
                    bounds, certificate
                )
                certificate_bounds = tuple(
                    bounds[index][0]
                    for index, weight in enumerate(certificate)
                    for _ in range(weight)
                )
            base = base_results[form]
            results.append(CombinedClassResult(
                pattern=pattern_result.pattern,
                canonical_form=form,
                role=base.role,
                edge_contents=base.edge_contents,
                comparisons=safe_comparisons(pattern_result.pattern, form),
                excluded=certificate is not None,
                certificate=certificate,
                certificate_bounds=certificate_bounds,
                aggregate_vector=aggregate_vector,
                aggregate_constant=aggregate_constant,
            ))
    return tuple(results)


@cache
def classify_full_filter() -> tuple[FullClassResult, ...]:
    """Classify all forms after safe quotient and composite-block bounds."""

    combined_results = {
        result.canonical_form: result for result in classify_combined_filter()
    }
    results = []
    for pattern_result in classify_all():
        for form in pattern_result.canonical_forms:
            bounds = full_inequalities(pattern_result.pattern, form)
            certificate = next(
                (
                    ray
                    for ray in exact_extreme_rays(bounds)
                    if exact_is_contradiction(bounds, ray)
                ),
                None,
            )
            aggregate_vector = None
            aggregate_constant = None
            certificate_bounds = None
            if certificate is not None:
                aggregate_vector, aggregate_constant = certificate_aggregate(
                    bounds, certificate
                )
                certificate_bounds = tuple(
                    bounds[index][0]
                    for index, weight in enumerate(certificate)
                    for _ in range(weight)
                )
            combined = combined_results[form]
            results.append(FullClassResult(
                pattern=pattern_result.pattern,
                canonical_form=form,
                role=combined.role,
                edge_contents=combined.edge_contents,
                comparisons=combined.comparisons,
                composites=composite_comparisons(pattern_result.pattern, form),
                excluded=certificate is not None,
                certificate=certificate,
                certificate_bounds=certificate_bounds,
                aggregate_vector=aggregate_vector,
                aggregate_constant=aggregate_constant,
            ))
    return tuple(results)


@cache
def classify_complete_filter() -> tuple[CompleteClassResult, ...]:
    """Classify all forms after the general common-factor height filter."""

    full_results = {
        result.canonical_form: result for result in classify_full_filter()
    }
    results = []
    for pattern_result in classify_all():
        for form in pattern_result.canonical_forms:
            bounds = complete_inequalities(pattern_result.pattern, form)
            certificate = next(
                (
                    ray
                    for ray in exact_extreme_rays(bounds)
                    if exact_is_contradiction(bounds, ray)
                ),
                None,
            )
            aggregate_vector = None
            aggregate_constant = None
            certificate_bounds = None
            if certificate is not None:
                aggregate_vector, aggregate_constant = certificate_aggregate(
                    bounds, certificate
                )
                certificate_bounds = tuple(
                    bounds[index][0]
                    for index, weight in enumerate(certificate)
                    for _ in range(weight)
                )
            full = full_results[form]
            results.append(CompleteClassResult(
                pattern=pattern_result.pattern,
                canonical_form=form,
                role=full.role,
                edge_contents=full.edge_contents,
                comparisons=full.comparisons,
                composites=full.composites,
                common_factors=common_factor_comparisons(
                    pattern_result.pattern, form
                ),
                excluded=certificate is not None,
                certificate=certificate,
                certificate_bounds=certificate_bounds,
                aggregate_vector=aggregate_vector,
                aggregate_constant=aggregate_constant,
            ))
    return tuple(results)


@cache
def classify_generalized_filter() -> tuple[GeneralizedClassResult, ...]:
    """Classify all forms after every coupled-conjugation comparison."""

    complete_results = {
        result.canonical_form: result
        for result in classify_complete_filter()
    }
    results = []
    for pattern_result in classify_all():
        for form in pattern_result.canonical_forms:
            bounds = generalized_inequalities(pattern_result.pattern, form)
            certificate = next(
                (
                    ray
                    for ray in exact_extreme_rays(bounds)
                    if exact_is_contradiction(bounds, ray)
                ),
                None,
            )
            aggregate_vector = None
            aggregate_constant = None
            certificate_bounds = None
            if certificate is not None:
                aggregate_vector, aggregate_constant = certificate_aggregate(
                    bounds, certificate
                )
                certificate_bounds = tuple(
                    bounds[index][0]
                    for index, weight in enumerate(certificate)
                    for _ in range(weight)
                )
            complete = complete_results[form]
            results.append(GeneralizedClassResult(
                pattern=pattern_result.pattern,
                canonical_form=form,
                role=complete.role,
                edge_contents=complete.edge_contents,
                comparisons=complete.comparisons,
                generalized_comparisons=generalized_comparisons(
                    pattern_result.pattern, form
                ),
                composites=complete.composites,
                common_factors=complete.common_factors,
                excluded=certificate is not None,
                certificate=certificate,
                certificate_bounds=certificate_bounds,
                aggregate_vector=aggregate_vector,
                aggregate_constant=aggregate_constant,
            ))
    return tuple(results)


@cache
def classify_sharp_axis_filter() -> tuple[SharpAxisClassResult, ...]:
    """Classify all forms after the factorized axis bounds."""

    generalized_results = {
        result.canonical_form: result
        for result in classify_generalized_filter()
    }
    results = []
    for pattern_result in classify_all():
        for form in pattern_result.canonical_forms:
            generalized = generalized_results[form]
            bounds = sharp_axis_inequalities(pattern_result.pattern, form)
            if generalized.excluded:
                if generalized.certificate is None:
                    raise AssertionError("excluded class must have a certificate")
                added = len(bounds) - len(
                    generalized_inequalities(pattern_result.pattern, form)
                )
                certificate = generalized.certificate + (0,) * added
                certificate_bounds = generalized.certificate_bounds
                aggregate_vector = generalized.aggregate_vector
                aggregate_constant = generalized.aggregate_constant
            else:
                certificate = next(
                    (
                        ray
                        for ray in exact_extreme_rays(bounds)
                        if exact_is_contradiction(bounds, ray)
                    ),
                    None,
                )
                aggregate_vector = None
                aggregate_constant = None
                certificate_bounds = None
                if certificate is not None:
                    aggregate_vector, aggregate_constant = (
                        certificate_aggregate(bounds, certificate)
                    )
                    certificate_bounds = tuple(
                        bounds[index][0]
                        for index, weight in enumerate(certificate)
                        for _ in range(weight)
                    )
            results.append(SharpAxisClassResult(
                pattern=pattern_result.pattern,
                canonical_form=form,
                role=generalized.role,
                edge_contents=generalized.edge_contents,
                comparisons=generalized.comparisons,
                generalized_comparisons=(
                    generalized.generalized_comparisons
                ),
                sharp_axis_comparisons=tuple(
                    comparison
                    for comparison in generalized.generalized_comparisons
                    if comparison.family == "A"
                ),
                composites=generalized.composites,
                common_factors=generalized.common_factors,
                excluded=certificate is not None,
                certificate=certificate,
                certificate_bounds=certificate_bounds,
                aggregate_vector=aggregate_vector,
                aggregate_constant=aggregate_constant,
            ))
    return tuple(results)


@cache
def classify_sharp_skew_filter() -> tuple[SharpSkewClassResult, ...]:
    """Classify all forms after the congruence-sharpened skew bounds."""

    sharp_axis_results = {
        result.canonical_form: result
        for result in classify_sharp_axis_filter()
    }
    results = []
    for pattern_result in classify_all():
        for form in pattern_result.canonical_forms:
            sharp_axis = sharp_axis_results[form]
            bounds = sharp_skew_inequalities(pattern_result.pattern, form)
            if sharp_axis.excluded:
                if sharp_axis.certificate is None:
                    raise AssertionError("excluded class must have a certificate")
                added = len(bounds) - len(
                    sharp_axis_inequalities(pattern_result.pattern, form)
                )
                certificate = sharp_axis.certificate + (0,) * added
                certificate_bounds = sharp_axis.certificate_bounds
                aggregate_vector = sharp_axis.aggregate_vector
                aggregate_constant = sharp_axis.aggregate_constant
            else:
                certificate = next(
                    (
                        ray
                        for ray in exact_extreme_rays(bounds)
                        if exact_is_contradiction(bounds, ray)
                    ),
                    None,
                )
                aggregate_vector = None
                aggregate_constant = None
                certificate_bounds = None
                if certificate is not None:
                    aggregate_vector, aggregate_constant = (
                        certificate_aggregate(bounds, certificate)
                    )
                    certificate_bounds = tuple(
                        bounds[index][0]
                        for index, weight in enumerate(certificate)
                        for _ in range(weight)
                    )
            results.append(SharpSkewClassResult(
                pattern=pattern_result.pattern,
                canonical_form=form,
                role=sharp_axis.role,
                edge_contents=sharp_axis.edge_contents,
                comparisons=sharp_axis.comparisons,
                generalized_comparisons=(
                    sharp_axis.generalized_comparisons
                ),
                sharp_axis_comparisons=(
                    sharp_axis.sharp_axis_comparisons
                ),
                sharp_skew_comparisons=tuple(
                    comparison
                    for comparison in sharp_axis.generalized_comparisons
                    if comparison.family == "S"
                ),
                composites=sharp_axis.composites,
                common_factors=sharp_axis.common_factors,
                excluded=certificate is not None,
                certificate=certificate,
                certificate_bounds=certificate_bounds,
                aggregate_vector=aggregate_vector,
                aggregate_constant=aggregate_constant,
            ))
    return tuple(results)


@cache
def classify_prime_lower_filter() -> tuple[PrimeLowerClassResult, ...]:
    """Classify all forms after discrete prime congruence floors."""

    sharp_skew_results = {
        result.canonical_form: result
        for result in classify_sharp_skew_filter()
    }
    results = []
    for pattern_result in classify_all():
        for form in pattern_result.canonical_forms:
            sharp_skew = sharp_skew_results[form]
            bounds = sharp_skew_inequalities(pattern_result.pattern, form)
            lower_bounds = prime_lower_bounds(pattern_result.pattern, form)
            if sharp_skew.excluded:
                certificate = sharp_skew.certificate
                certificate_bounds = sharp_skew.certificate_bounds
                aggregate_vector = sharp_skew.aggregate_vector
                aggregate_constant = sharp_skew.aggregate_constant
            else:
                certificate = next(
                    (
                        ray
                        for ray in exact_extreme_rays(bounds)
                        if exact_is_contradiction_with_lower_bounds(
                            bounds, ray, lower_bounds
                        )
                    ),
                    None,
                )
                aggregate_vector = None
                aggregate_constant = None
                certificate_bounds = None
                if certificate is not None:
                    aggregate_vector, aggregate_constant = (
                        certificate_aggregate(bounds, certificate)
                    )
                    certificate_bounds = tuple(
                        bounds[index][0]
                        for index, weight in enumerate(certificate)
                        for _ in range(weight)
                    )
            results.append(PrimeLowerClassResult(
                pattern=pattern_result.pattern,
                canonical_form=form,
                role=sharp_skew.role,
                edge_contents=sharp_skew.edge_contents,
                comparisons=sharp_skew.comparisons,
                generalized_comparisons=(
                    sharp_skew.generalized_comparisons
                ),
                sharp_axis_comparisons=(
                    sharp_skew.sharp_axis_comparisons
                ),
                sharp_skew_comparisons=(
                    sharp_skew.sharp_skew_comparisons
                ),
                composites=sharp_skew.composites,
                common_factors=sharp_skew.common_factors,
                prime_lower_bounds=lower_bounds,
                excluded=certificate is not None,
                certificate=certificate,
                certificate_bounds=certificate_bounds,
                aggregate_vector=aggregate_vector,
                aggregate_constant=aggregate_constant,
            ))
    return tuple(results)


@cache
def complementary_axis_descent_forms() -> tuple[str, ...]:
    """Find the surviving all-edge class with complementary ``A_8`` axes.

    For this physical class the two edge omissions give one real and one
    imaginary coordinate of the same squared Gaussian power.  Section 12 of
    ``three-block-p2qr.md`` proves that their simultaneous divisibilities are
    impossible.
    """

    forms = []
    for result in classify_prime_lower_filter():
        if result.excluded or result.role != ("E", "E", "E"):
            continue
        events = {
            (
                comparison.divisor_row,
                comparison.remaining_row,
                comparison.omitted_column,
            )
            for comparison in result.generalized_comparisons
            if comparison.family == "A" and comparison.level == 8
        }
        if events == {(1, 0, 3), (2, 0, 2)}:
            forms.append(result.canonical_form)
    return tuple(forms)


@cache
def classify_arithmetic_filter() -> tuple[ArithmeticClassResult, ...]:
    """Classify all forms after the complementary-axis descent."""

    descent_forms = frozenset(complementary_axis_descent_forms())
    return tuple(
        ArithmeticClassResult(
            pattern=result.pattern,
            canonical_form=result.canonical_form,
            role=result.role,
            previous_excluded=result.excluded,
            complementary_axis_descent=(
                result.canonical_form in descent_forms
            ),
            excluded=(
                result.excluded or result.canonical_form in descent_forms
            ),
        )
        for result in classify_prime_lower_filter()
    )


def main() -> None:
    base_results = classify_monomial_filter()
    base_excluded = tuple(result for result in base_results if result.excluded)
    combined_results = classify_combined_filter()
    combined_excluded = tuple(
        result for result in combined_results if result.excluded
    )
    full_results = classify_full_filter()
    full_excluded = tuple(result for result in full_results if result.excluded)
    complete_results = classify_complete_filter()
    complete_excluded = tuple(
        result for result in complete_results if result.excluded
    )
    generalized_results = classify_generalized_filter()
    generalized_excluded = tuple(
        result for result in generalized_results if result.excluded
    )
    sharp_axis_results = classify_sharp_axis_filter()
    sharp_axis_excluded = tuple(
        result for result in sharp_axis_results if result.excluded
    )
    sharp_skew_results = classify_sharp_skew_filter()
    sharp_skew_excluded = tuple(
        result for result in sharp_skew_results if result.excluded
    )
    prime_lower_results = classify_prime_lower_filter()
    prime_lower_excluded = tuple(
        result for result in prime_lower_results if result.excluded
    )
    results = classify_arithmetic_filter()
    excluded = tuple(result for result in results if result.excluded)
    survivors = tuple(result for result in results if not result.excluded)
    excluded_roles = Counter(result.role for result in excluded)
    surviving_roles = Counter(result.role for result in survivors)
    print(
        f"classes={len(results)} base_excluded={len(base_excluded)} "
        f"combined_excluded={len(combined_excluded)} "
        f"composite_excluded={len(full_excluded)} "
        f"common_excluded={len(complete_excluded)} "
        f"generalized_excluded={len(generalized_excluded)} "
        f"sharp_axis_excluded={len(sharp_axis_excluded)} "
        f"sharp_skew_excluded={len(sharp_skew_excluded)} "
        f"prime_lower_excluded={len(prime_lower_excluded)} "
        f"arithmetic_excluded={len(excluded)} survivors={len(survivors)} "
        f"safe_comparisons="
        f"{sum(len(result.comparisons) for result in prime_lower_results)} "
        f"composite_comparisons="
        f"{sum(len(result.composites) for result in prime_lower_results)} "
        f"common_factor_comparisons="
        f"{sum(len(result.common_factors) for result in prime_lower_results)} "
        f"generalized_comparisons="
        f"{sum(len(result.generalized_comparisons) for result in prime_lower_results)} "
        f"sharp_axis_comparisons="
        f"{sum(len(result.sharp_axis_comparisons) for result in prime_lower_results)} "
        f"sharp_skew_comparisons="
        f"{sum(len(result.sharp_skew_comparisons) for result in prime_lower_results)}"
    )
    print(f"excluded_roles={dict(sorted(excluded_roles.items()))}")
    print(f"surviving_roles={dict(sorted(surviving_roles.items()))}")


if __name__ == "__main__":
    main()
