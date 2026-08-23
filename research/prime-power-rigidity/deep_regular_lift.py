#!/usr/bin/env python3
"""Deep regular 2-adic branch lift: the 2^60 statement, honestly.

The committed scan (scan_prime_powers.py) keeps every solution branch of
the coupled system, so the tree doubles per level and dies computationally
around 2^20.  This module isolates the branches that can never die.

Key fact (exact, not heuristic): for bits >= 7 the residual of a solution
branch is affine in the lift bits modulo the next power of two, because the
second-order correction is a multiple of bit^2 = 2^(2*bits-6) >= 2^(bits+1).
Writing bit = 2^(bits-3) and R(a) for the residual of xs + a*bit at modulus
2^(bits+1), the 2x3 lift matrix

    M[t] = (R(e_t) - R(0)) / bit   (mod 2^4)

is therefore well defined, and a child add vector a solves the level-(bits+1)
system exactly when  R(0)/bit + M*a = 0 (mod 2^4).  Machine-checked against
the exact eight-child enumeration in the tests.

Every column of M is divisible by 8 (the classical 8 | d_c structure:
du/dx carries a factor 4 and the normalized column a factor 2j).  Write
M = 8*M~.  Call a branch REGULAR when M~ mod 2 has rank 2, i.e. some 2x2
minor of M has 2-adic valuation exactly 6.  For a regular branch the child
condition is solvable for every value of R(0)/bit, so children always
exist, and regularity is inherited (M mod 16 is stable under the lift
increment, since the derivative shifts only by multiples of the second
derivative times the even increment).  Hence a regular branch at 2^7
lifts to 2^k for every k -- the deep-lift half of the previously
quarantined 2^60 observation becomes a theorem for these branches.

Branches of the two CFF classes (and possibly others) are rank-deficient:
all their lift matrices at 2^7 have proportional columns (observed
exactly, e.g. (8,8) in every column), so child existence is conditional.
For those the module verifies survival empirically to the target depth
(they do survive, with stabilized valuation 3), which reproduces the
quarantined 2^60 claim from committed code without upgrading it to a
theorem.

The module lifts one witness per class to a target precision (default
2^60), preferring children of minimal common offset valuation, and
verifies the final branch through the independent direct-generator
arithmetic path.  If a REGULAR witness' common valuation stabilizes at v,
the depth-k truncations of its 2-adic limit are mod-2^k solutions with
common valuation exactly v for every k: no mod-2^k enumeration can ever
force more than 2^v | d_c, at any depth, for that class.

Honest scope: a 2-adic branch is not an integer realization.  The
statements here cap the *enumeration method*; they neither exhibit a magic
square nor prove one impossible.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import dataclass
from itertools import product
from pathlib import Path
from typing import Optional, Sequence

from classes import CLASSES
from prime_power_rigidity import (
    Branch,
    common_offset_v2,
    coupled_residual,
    gaussian_normalized_offsets,
    initial_branches,
    lift_once,
    normalized_offsets,
)

AFFINE_FROM_BITS = 7  # bit^2 >= 2^(bits+1) first holds here


def residual_at(
    indices: Sequence[Sequence[int]],
    xs: Sequence[int],
    bits: int,
    signs,
    edge_swap: bool,
) -> tuple[int, int]:
    modulus = 1 << bits
    return coupled_residual(
        normalized_offsets(indices, xs, modulus), signs, edge_swap, modulus
    )


def lift_matrix(
    indices: Sequence[Sequence[int]],
    xs: Sequence[int],
    bits: int,
    signs,
    edge_swap: bool,
) -> tuple[tuple[tuple[int, int], ...], tuple[int, int]]:
    """(M, q) with children a solving exactly q + M a = 0 (mod 16).

    Requires bits >= AFFINE_FROM_BITS and xs a solution mod 2^bits.
    """

    if bits < AFFINE_FROM_BITS:
        raise ValueError("affine lift needs bits >= 7")
    bit = 1 << (bits - 3)
    m = 1 << (bits + 1)
    r0 = coupled_residual(
        normalized_offsets(indices, xs, m), signs, edge_swap, m
    )
    assert r0 == (0, 0) or all(v % (1 << bits) == 0 for v in r0)
    columns = []
    for t in range(3):
        xs2 = list(xs)
        xs2[t] += bit
        rt = coupled_residual(
            normalized_offsets(indices, xs2, m), signs, edge_swap, m
        )
        columns.append(((rt[0] - r0[0]) // bit, (rt[1] - r0[1]) // bit))
    q = (r0[0] // bit, r0[1] // bit)
    return tuple(columns), q  # type: ignore[return-value]


def matrix_children(
    indices: Sequence[Sequence[int]],
    xs: Sequence[int],
    bits: int,
    signs,
    edge_swap: bool,
) -> list[tuple[int, int, int]]:
    """Children add in {0,1}^3 predicted by the affine lift matrix."""

    columns, q = lift_matrix(indices, xs, bits, signs, edge_swap)
    out = []
    for add in product((0, 1), repeat=3):
        s0 = (q[0] + sum(add[t] * columns[t][0] for t in range(3))) % 16
        s1 = (q[1] + sum(add[t] * columns[t][1] for t in range(3))) % 16
        if s0 == 0 and s1 == 0:
            out.append(add)
    return out


def is_regular(columns) -> bool:
    """Rank-2 deflated lift matrix: some 2x2 minor has v2 exactly 6.

    Columns are always divisible by 8 (the classical 8 | d structure);
    M = 8*M~ and rank(M~ mod 2) = 2 makes the child condition solvable
    for every right-hand side, so regular branches never die.
    """

    def v2(x: int) -> int:
        return (x & -x).bit_length() - 1 if x else 99

    m = [list(c) for c in columns]
    for i, j in ((0, 1), (0, 2), (1, 2)):
        det = m[i][0] * m[j][1] - m[j][0] * m[i][1]
        if v2(det) == 6:
            return True
    return False


@dataclass(frozen=True)
class Witness:
    form: str
    role: str
    signs: tuple[int, int, int, int]
    edge_swap: bool
    xs: tuple[int, ...]
    target_bits: int
    common_v2: int
    stabilized_at_bits: int
    regular: bool


def greedy_deep_lift(
    indices: Sequence[Sequence[int]],
    branch: Branch,
    start_bits: int,
    target_bits: int,
    require_regular_inheritance: bool = True,
    step_budget: int = 200000,
) -> Optional[Witness]:
    """Depth-first lift preferring minimal common valuation, with backtracking.

    Regular branches never backtrack (children always exist and stay
    regular).  Rank-deficient branches can die (half of them do at each
    level), so the search backs up and tries the next-preferred child.
    When the starting branch is regular, the chosen child is checked to
    stay regular at every level (the inheritance claim, asserted
    computationally rather than trusted).
    """

    bits0 = start_bits
    xs0 = tuple(branch.xs)
    columns0, _ = lift_matrix(
        indices, xs0, bits0, branch.signs, branch.edge_swap
    )
    regular = is_regular(columns0)
    steps = 0

    def children_of(xs: tuple, bits: int):
        bit = 1 << (bits - 3)
        m = 1 << (bits + 1)
        out = []
        for add in product((0, 1), repeat=3):
            cand = tuple(xs[t] + add[t] * bit for t in range(3))
            r = coupled_residual(
                normalized_offsets(indices, cand, m),
                branch.signs,
                branch.edge_swap,
                m,
            )
            if r == (0, 0):
                v = common_offset_v2(
                    normalized_offsets(indices, cand, m), bits + 1
                )
                out.append((v, cand))
        out.sort()
        return out

    def rec(xs, bits, prev_v, stabilized):
        nonlocal steps
        if bits == target_bits:
            return xs, prev_v, stabilized
        for v, cand in children_of(xs, bits):
            steps += 1
            if steps > step_budget:
                raise RuntimeError("deep lift exceeded step budget")
            if regular and require_regular_inheritance:
                cols, _ = lift_matrix(
                    indices, cand, bits + 1, branch.signs, branch.edge_swap
                )
                assert is_regular(cols), "regularity lost under lift"
            stab = stabilized if v == prev_v else bits + 1
            found = rec(cand, bits + 1, v, stab)
            if found is not None:
                return found
        return None

    v0 = common_offset_v2(
        normalized_offsets(indices, xs0, 1 << bits0), bits0
    )
    result = rec(xs0, bits0, v0, bits0)
    if result is None:
        return None
    xs, prev_v, stabilized = result
    if target_bits >= AFFINE_FROM_BITS:
        columns, _ = lift_matrix(
            indices, xs, target_bits, branch.signs, branch.edge_swap
        )
    else:
        columns = columns0
    return Witness(
        form="",
        role="",
        signs=branch.signs,
        edge_swap=branch.edge_swap,
        xs=xs,
        target_bits=target_bits,
        common_v2=prev_v,
        stabilized_at_bits=stabilized,
        regular=regular,
    )


def class_report(indices, form: str, role: str, target_bits: int,
                 reg_bits: int = AFFINE_FROM_BITS) -> dict:
    branches = initial_branches(indices, 4)
    for b in range(5, reg_bits + 1):
        branches = lift_once(indices, branches, b)
    regular_by_pattern: dict[tuple, list[Branch]] = {}
    for br in branches:
        columns, _ = lift_matrix(
            indices, br.xs, reg_bits, br.signs, br.edge_swap
        )
        if is_regular(columns):
            key = (br.signs, br.edge_swap)
            regular_by_pattern.setdefault(key, []).append(br)
    patterns_all = sorted({(br.signs, br.edge_swap) for br in branches})
    report: dict = {
        "form": form,
        "role": role,
        "branches_at_reg_bits": len(branches),
        "patterns_total": len(patterns_all),
        "patterns_with_regular_branch": len(regular_by_pattern),
    }
    best_witness = None
    for key in patterns_all:
        brs = regular_by_pattern.get(key, [])
        empirical = not brs
        if empirical:
            brs = [br for br in branches
                   if (br.signs, br.edge_swap) == key]
        brs_sorted = sorted(
            brs,
            key=lambda br: (
                common_offset_v2(
                    normalized_offsets(indices, br.xs, 1 << reg_bits),
                    reg_bits,
                ),
                br.xs,
            ),
        )
        for br in brs_sorted[:4]:  # up to four candidates per pattern
            w = greedy_deep_lift(indices, br, reg_bits, target_bits)
            if w is not None:
                w = Witness(
                    form=form, role=role, signs=w.signs, edge_swap=w.edge_swap,
                    xs=w.xs, target_bits=w.target_bits, common_v2=w.common_v2,
                    stabilized_at_bits=w.stabilized_at_bits, regular=w.regular,
                )
                if best_witness is None or (w.common_v2, w.xs) < (
                    best_witness.common_v2, best_witness.xs
                ):
                    best_witness = w
                break
    if best_witness is None:
        report["deep_witness"] = None
        return report
    # verify the witness through the independent direct-generator path
    m = 1 << target_bits
    generators = tuple((1, 2 * x) for x in best_witness.xs)
    values_gauss = gaussian_normalized_offsets(
        indices, generators, m
    )
    values_torus = normalized_offsets(indices, best_witness.xs, m)
    assert values_gauss == values_torus, form
    r = coupled_residual(
        values_torus, best_witness.signs, best_witness.edge_swap, m
    )
    assert r == (0, 0), form
    report["deep_witness"] = {
        "signs": list(best_witness.signs),
        "edge_swap": best_witness.edge_swap,
        "xs": list(best_witness.xs),
        "common_v2": best_witness.common_v2,
        "stabilized_at_bits": best_witness.stabilized_at_bits,
        "regular": best_witness.regular,
        "verified_dual_path": True,
    }
    report["min_common_v2_witness"] = best_witness.common_v2
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bits", type=int, default=60)
    parser.add_argument("--json", type=str, default="")
    args = parser.parse_args()
    out = {"target_bits": args.bits, "classes": {}}
    started = time.time()
    for form, role, indices in CLASSES:
        rep = class_report(indices, form, role, args.bits)
        out["classes"][form] = rep
        w = rep.get("deep_witness")
        print(
            f"{form} ({role}): patterns {rep['patterns_with_regular_branch']}"
            f"/{rep['patterns_total']} regular, "
            + (
                f"witness v2 = {w['common_v2']} stabilized at 2^{w['stabilized_at_bits']}"
                if w
                else "NO DEEP WITNESS"
            ),
            flush=True,
        )
    out["seconds"] = round(time.time() - started, 1)
    if args.json:
        Path(args.json).write_text(json.dumps(out, indent=2) + "\n")
        print(f"wrote {args.json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
