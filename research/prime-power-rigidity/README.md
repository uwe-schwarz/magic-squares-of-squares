# Prime-power rigidity and class-targeted p-adic reconstruction

## Status

This package contains the code developed in the 2026-08-22 continuation of the `p^2 q r` attack, accidentally left unpushed in the initial response, and pushed on 2026-08-23.

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
- `scan_prime_powers.py` — turnkey 2-adic scan driver; lifts every solution branch of every class and records branch counts and forced common offset valuations (`scan_2adic_12.json` is the committed ledger through `2^12`).
- `deep_regular_lift.py` — deep 2-adic lift: the exact affine lift matrix at `bits >= 7`, the deflated rank-2 regularity criterion (some 2x2 lift minor with `v2` exactly 6), the theorem that regular branches never die, and one dual-path-verified witness branch per class lifted to `2^60` (`deep_regular_lift_60.json`).
- `targeted_reconstruction.py` — exact six-coordinate Gaussian re-embedding and final candidate verification.
- `test_prime_power_rigidity.py`, `test_deep_regular_lift.py` — independent model cross-checks and counter-for-counter lifting tests.
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

## Reproduced result: forced 2-adic divisibility

`scan_prime_powers.py` enumerates every solution branch of the coupled
system modulo `2^4` and lifts all branches level by level; it is the
turnkey driver for the engine in this package (about 2.5 minutes for all
16 classes at `--bits 12`, ledger in `scan_2adic_12.json`).

Verified outcome through `2^12`: exactly **six classes force `16 | d_c`
for all four offsets** — both `EFF` classes, three `EFE` classes
(`I2:0000/0011/01*0`, `I2:0000/0101/00*1`, `I2:0000/0101/01*0`), and
`I2:0000/01*0/01*1` (`EEE`). For the other ten classes the coupled
system admits solution branches with common valuation exactly 3 at every
level through `2^12`, so this 2-adic method caps their forced
divisibility at the classical `8 | d_c`. The forced valuation is
identical at every level from `2^4` to `2^12`.

The forced statement is unconditional for realizations of any size:
every integer realization reduces modulo `2^k` into the enumerated
branches for every `k`, and `v2(d_c) = v2(Im(W_c))` because the center
root is odd. Stacked with the classical `24 | d_c` congruences, the six
classes satisfy `48 | d_c` unconditionally.

All six `16 | d_c` classes also carry odd rigid primes — they are a
subset of the ten rigid classes of
[`../coupled-p2qr-scan/rigidity.md`](../coupled-p2qr-scan/rigidity.md),
not a complement — so their forced divisibility products grow further,
for example `16 * 3 * 7` for every realization of `I2:0000/0011/0101`
and additionally a factor `29` when `29` is not one of the center
primes: the rigidity lemma requires `l` not to divide `2 p q r`, and a
rigid prime `l = 1 mod 4` can itself occur in the center support
(primes `l = 3 mod 4` never can, so their factors are unconditional).
The six `ECE`/`EFC` classes, which have no odd rigid prime below 1000,
all sit in the valuation-3 group: for them **no divisibility beyond the
classical `24 | d_c` is currently known**.

## Deep lift: the forced valuations are exact and permanent

`deep_regular_lift.py` closes the previously quarantined "`2^60` branches"
observation.  For `bits >= 7` the residual of a solution branch is exactly
affine in the lift bits, giving a 2x3 lift matrix `M` (columns always
divisible by 8 — the classical `8 | d_c` structure).  Where the deflated
matrix `M/8` has rank 2 mod 2 ("regular"), children exist at every level
and regularity is inherited, so the branch lifts to `2^k` for all `k`:
eleven classes, including all six clean `ECE`/`EFC`-role classes that are
regular, have such branches, and their witness branches at `2^60` carry
common valuation exactly `v` (`v = 4` for the six `16 | d_c` classes, `v =
3` for the valuation-3 regular classes) already stabilized at `2^7`.  It
follows that mod-`2^k` enumeration can never force more than `2^v | d_c`
at any depth for these classes — the forced divisibility recorded above
is exact and permanent, not just a `2^12` snapshot.  Five classes (both
`CFF`, two `ECE`, one `EEE`) are rank-deficient at every branch tested;
their `2^60` survival is verified empirically with the same witness
machinery (they do survive, with valuation 3).

The fixture in `classes.py` is pinned to the generated table
[`../coupled-p2qr-scan/class_table.h`](../coupled-p2qr-scan/class_table.h) by
a regression test, and the normalized column here is the same
`(pi/conj(pi))^(2*j)` torus reduction proved in
[`../coupled-p2qr-scan/rigidity.md`](../coupled-p2qr-scan/rigidity.md),
restricted to the exactly realizable 2-adic generator quotients.

## Reproduce the checks

```sh
cd research/prime-power-rigidity
./run-tests.sh
python3 scan_prime_powers.py --bits 12 --json /tmp/scan.json
python3 deep_regular_lift.py --bits 60
```

The root `make test` also invokes this package. Tests run locally only;
this repository deliberately has no CI workflows.
