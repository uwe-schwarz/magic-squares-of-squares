# Prime-power rigidity and class-targeted p-adic reconstruction

## Status

This package contains the code developed in the 2026-08-22/23 continuation of the `p^2 q r` attack and accidentally left unpushed in the initial response.

The global 3x3 magic-square-of-distinct-squares problem remains **open**. Nothing in this folder is a proof of global nonexistence, and no counterexample is claimed.

## Important correction

An abandoned intermediate torus prototype used exponent `j` in the normalized Gaussian unit. That is wrong. Since an offset is `|Im(z_c^2)|`, the correct normalized column is

```text
W_c = product_s (pi_s / conjugate(pi_s)) ** (2*j[s,c]).
```

The factor `2` is covered by a regression test. Numerical conclusions from the incorrect prototype are not theorem statements and must not be quoted.

## Files

- `classes.py` — exact local-index matrices for the 16 unresolved switching classes, generated from the existing exporter.
- `prime_power_rigidity.py` — exact modular Gaussian arithmetic, half-slope parametrization, coupled equations, exhaustive low-level enumeration, and bitwise lifting.
- `targeted_reconstruction.py` — exact six-coordinate Gaussian re-embedding and final candidate verification.
- `test_prime_power_rigidity.py` — independent model cross-checks and counter-for-counter lifting tests.
- `results.json` — session ledger distinguishing reproduced facts from exploratory results that still require a long rerun.

## 2-adic parametrization

For `pi=a+bi` with `a` odd and `b` even, put `x=(b/2)/a`. Then

```text
u = pi / conjugate(pi)
  = (1+2*i*x)/(1-2*i*x)
  = ((1-4*x^2)+4*i*x)/(1+4*x^2).
```

The denominator is odd, so this is exact modulo every `2^k`. The coupled system is checked for all normalized sign choices and the physical edge swap. `lift_once` mirrors every retained branch into its eight bit lifts, so counters can be audited level by level.

## Exact verification rule

A modular or reconstructed hit is never called a square until `verify_candidate` re-expands the original Gaussian monomials and checks all of the following:

1. `{d2,d3}={d0+d1,|d0-d1|}` exactly;
2. `e^2-d` and `e^2+d` are integer squares for all four offsets;
3. all nine entries are positive;
4. all nine entries are pairwise distinct.

## Session outcome

The session explored prime-power lifting and a class-targeted reconstruction search and found no verified full square. The long-search numerical observations from the interrupted/unpushed run are preserved in `results.json` as `reported_uncommitted_session_result`, not upgraded to theorem statements. The exact source code and class fixture are now committed so those scans can be reproduced rather than trusted from prose.

The fixture in `classes.py` is pinned to the generated table
[`../coupled-p2qr-scan/class_table.h`](../coupled-p2qr-scan/class_table.h) by
a regression test, and the normalized column here is the same
`(pi/conj(pi))^(2*j)` torus reduction proved in
[`../coupled-p2qr-scan/rigidity.md`](../coupled-p2qr-scan/rigidity.md),
restricted to the exactly realizable 2-adic generator quotients.

## Reproduce the fast checks

```sh
cd research/prime-power-rigidity
./run-tests.sh
```

The root `make test` also invokes this package. Tests run locally only;
this repository deliberately has no CI workflows.
