# Dominant Gaussian identity scan

## Status and scope

This is a deterministic, bounded falsification experiment for the exact
identities forced by a dominant prime-power block in the refined block-balance
argument. It is not a proof, a novelty claim, or a search bound stated in the
center root `e`.

The completed run is exhaustive in the parameter

\[
1\le M\le 10^6
\]

subject to every prime divisor of `M` being congruent to `1 mod 4`. For every
such `M`, it enumerates all relevant Gaussian values and all coefficient
relations described below. The program is single-threaded; there is no shard,
parallel merge, or probabilistic sampling step.

## Identities tested

For every Gaussian integer `w` with

\[
N(w)=M^2,
\]

the scanner forms every value

\[
G=\varepsilon^2w^2,\qquad \varepsilon\in\{\pm1,\pm i\}.
\]

It then exhausts the two relation types from
[block-balance.md](block-balance.md):

\[
H=G_1+G_2+G_3
\]

and

\[
J=\frac{2G_1+G_2+G_3}{2}.
\]

If `q=p^k>M` is a dominant block, the proof forces respectively

\[
H=\pm\bar\pi^{4k},
\qquad
J=\pm\bar\pi^{4k}.
\]

Before even checking whether `q` is a prime power or whether the Gaussian
direction is a pure power of a prime above `p`, the necessary norm condition is

\[
N(H)=q^4
\quad\text{or}\quad
N(J)=q^4.
\]

The scan found no such dominant fourth-power norm.

## Reproduction

On macOS with Apple clang 21.0.0 and Python 3.14.7:

```sh
cd magic-square-of-squares

clang++ -O3 -std=c++20 -Wall -Wextra -pedantic \
  dominant_identity_search.cpp -o /tmp/dominant_identity_search

/tmp/dominant_identity_search --self-test
python3 -m unittest -v test_dominant_identity_search.py
/tmp/dominant_identity_search 1000000
```

The exhaustive run reported:

```text
M_limit=1000000 eligible_M=87882 total_G_values=1669756
111_loops=1086476416 norm_window=805400664 fourth_norms=0 prime_power_norms=0 pure_targets=0 genuine_hits=0 degenerate_hits=0
211_loops=3185445820 norm_window=1904250228 fourth_norms=0 prime_power_norms=0 pure_targets=0 genuine_hits=0 degenerate_hits=0
```

Here `norm_window` counts resultants satisfying `M^4 < N(H) <= 9M^4` or
`M^4 < N(J) <= 4M^4`, before the exact fourth-power test.

## Completeness and validation checks

For a factor `r^h || M`, with `r=rho*conjugate(rho)` in `Z[i]`, every Gaussian
integer of norm `M^2` is represented, up to a unit, by choosing the exponent
of `rho` from `0` through `2h`. The scanner takes the Cartesian product of
these choices over all factors. Squaring removes the sign of the unit and the
remaining unit-square choice is exactly `+/-`, both of which are inserted.

The `111` loop uses combinations with replacement because its three terms are
symmetric. The `211` loop distinguishes the doubled term and uses combinations
with replacement for the two coefficient-one terms. Thus repeated terms are
included; only a later genuine-offset check rejects zero or repeated absolute
projections.

The test suite supplies two independent checks:

- a Python reference enumerates `w=(x,y)` directly from `x^2+y^2=M^2`, without
  Gaussian factorization, and matches every C++ counter through `M=200`;
- `--self-test` injects synthetic positive identities based on
  `conjugate((2+i)^4)=-7-24i` and
  `conjugate((2+3i)^4)=-119+120i`. These exercise exact fourth-root detection,
  prime-power recognition, Gaussian direction matching, the signed projection
  relation, distinct projections, and the `p`-unit check for both coefficient
  types. They are pipeline tests, not claimed common-norm examples.

An AddressSanitizer and UndefinedBehaviorSanitizer build passed the self-test
and a scan through `M=10000`.

## Integer-range audit

For the documented `M<=10^6` run:

- coordinates of `w` are at most `M` in magnitude;
- coordinates of `G` are at most `M^2`;
- resultant coordinates are at most `3M^2`;
- Gaussian coordinates fit in signed 64-bit integers;
- norms, fourth powers, and projection products use 128-bit integers;
- the largest relevant values are below `9*10^24`, far below the 128-bit
  limit.

Gaussian exponentiation avoids an unused final square, which could overflow
even when the requested power fits. Floating point supplies only a starting
estimate for a fourth root; monotone 128-bit comparisons adjust it and make the
accept/reject decision exact.

## Interpretation

The result supports the stronger conjecture that every prime-power block of a
primitive center root is strictly smaller than the product of the other
blocks. The data do not prove that conjecture. The precise supported statement
is only: no counterexample occurs for any completely enumerated `M<=10^6` in
the two exact-identity families above.

The later theoretical refinement in
[block-balance.md](block-balance.md) narrows the unresolved interpretation.
A dominant block cannot have a corner exception at all, and a prime
congruent to \(5\) modulo \(8\) satisfies \(p^k<M\) unconditionally.  Thus
a genuine dominant counterexample represented in this scan would have to use
\(p\equiv1\pmod8\), exactly one nonunit offset, and a genuinely intermediate
edge exception.  The scanner intentionally enumerates the larger abstract
`111` and `211` families, so its zero count remains valid but includes many
cases now excluded by proof.  In particular,
[two-block-exponent-one.md](two-block-exponent-one.md) now excludes the
entire two-prime-block specialization; any unresolved dominant block belongs
to a center supported on at least three rational primes.
