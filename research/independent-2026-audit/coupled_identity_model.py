#!/usr/bin/env python3
"""Extract exact local-index data for the unresolved p^2*q*r classes.

This is deliberately a bridge, not another proof filter.  The existing
prime-support machinery repeatedly projects Gaussian identities to monomial
inequalities.  Here we preserve the four columns together so that a future
solver can build one coupled polynomial system per surviving switching class.

Run from this directory or from the repository root.  No third-party packages
are required.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PRIME_SUPPORT = Path(__file__).resolve().parents[1] / "prime-support"
sys.path.insert(0, str(PRIME_SUPPORT))

from p2qr_monomial_filter import (  # noqa: E402
    classify_arithmetic_filter,
    generalized_comparisons,
    local_indices,
    relation_coefficients,
)
from three_block_p2qr_signatures import classify_all  # noqa: E402


def unresolved_records() -> list[dict[str, object]]:
    """Return a stable JSON-ready description of the 16 unresolved classes."""

    patterns = {
        form: result.pattern
        for result in classify_all()
        for form in result.canonical_forms
    }
    unresolved = [
        result
        for result in classify_arithmetic_filter()
        if not result.excluded
    ]
    records: list[dict[str, object]] = []
    for result in unresolved:
        form = result.canonical_form
        pattern = patterns[form]
        indices = local_indices(pattern, form)
        deletions = []
        for omitted in range(4):
            retained = [column for column in range(4) if column != omitted]
            deletions.append({
                "omitted_column": omitted,
                "retained_columns": retained,
                "coefficient_magnitudes": list(relation_coefficients(omitted)),
                "retained_local_indices": [
                    [indices[row][column] for column in retained]
                    for row in range(3)
                ],
            })
        comparisons = [
            {
                "aligned_row": item.aligned_row,
                "divisor_row": item.divisor_row,
                "remaining_row": item.remaining_row,
                "omitted_column": item.omitted_column,
                "family": item.family,
                "level": item.level,
                "divisor_content": item.divisor_content,
            }
            for item in generalized_comparisons(pattern, form)
        ]
        records.append({
            "canonical_form": form,
            "role": list(result.role),
            "pattern": list(pattern),
            "block_exponents": [2, 1, 1],
            "local_indices": indices,
            "deletions": deletions,
            "generalized_divisor_comparisons": comparisons,
        })
    return records


def validate(records: list[dict[str, object]]) -> None:
    """Check invariants needed by a coupled-identity implementation."""

    assert len(records) == 16
    forms = [record["canonical_form"] for record in records]
    assert len(set(forms)) == 16
    for record in records:
        indices = record["local_indices"]
        assert isinstance(indices, list) and len(indices) == 3
        assert all(isinstance(row, list) and len(row) == 4 for row in indices)
        # p^2 has one intermediate magnitude 1 and three extreme magnitudes 2.
        assert sorted(abs(value) for value in indices[0]) == [1, 2, 2, 2]
        # q and r are exponent-one rows: at most one balanced incidence.
        for row in indices[1:]:
            assert all(abs(value) <= 1 for value in row)
            assert sum(value == 0 for value in row) <= 1
        deletions = record["deletions"]
        assert isinstance(deletions, list) and len(deletions) == 4


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--pretty", action="store_true", help="pretty-print the JSON output"
    )
    args = parser.parse_args()
    records = unresolved_records()
    validate(records)
    print(json.dumps(
        {"unresolved_classes": len(records), "classes": records},
        indent=2 if args.pretty else None,
        sort_keys=True,
    ))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
