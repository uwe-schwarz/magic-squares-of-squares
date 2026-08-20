# Exact two-block factor-height scan

## Status and scope

This is a deterministic bounded crosscheck of the edge-edge normal form that
remained before Section 10 of
[two-block-exponent-one.md](two-block-exponent-one.md) closed the
two-prime-block case.  The theorem there now excludes every two-block center
without a height bound; this scan is independent computational evidence for
the intermediate reduction, not part of the final proof.  No novelty claim
is made.

For a bound \(B\), the scan is exhaustive over center roots

\[
e=p^kq^\ell,
\qquad p\ne q,
\qquad \max(p^k,q^\ell)\le B,
\]

after applying the pre-Section-10 necessary conditions proved in
[block-balance.md](block-balance.md) and
[two-block-exponent-one.md](two-block-exponent-one.md):

- both primes are \(1\pmod 8\), and \(k,\ell\ge2\);
- the numerically larger block is unique, has exponent at least three, and
  its prime is \(1\pmod{24}\);
- \(3/2\) is a fourth-power residue modulo the dominant prime;
- if \(P>Q\) are the two block values, then \(P^2<3Q^2\).

For every pair surviving those preliminary filters it then stops using
filters: it enumerates every
Gaussian representation of norm (e^2), forms every nonzero opposite-pair
offset, and tests the complete four-offset condition

\[
\{a,b,a+b,|a-b|\}.
\]

The four offsets must be positive and pairwise distinct.  Every enumerated
offset already has both (e^2+d) and (e^2-d) equal to positive squares.

## Complete Gaussian enumeration

Choose \(p=\pi\bar\pi\).  For local index \(-k\le j\le k\), the squared
Gaussian factor is

\[
G_{p,j}=
\begin{cases}
p^{2(k-j)}\pi^{4j},&j\ge0,\\
\overline{G_{p,-j}},&j<0.
\end{cases}
\]

The analogous factors \(G_{q,t}\), \(-\ell\le t\le\ell\), give every
squared Gaussian representation of the two-block norm, up to a unit.  A
squared unit contributes only a sign and therefore does not change

\[
d=\left|\operatorname{Im}(G_{p,j}G_{q,t})\right|.
\]

The scanner sorts and deduplicates these exact integer offsets.  It tests
every unordered pair as possible corner offsets \(a,b\), rejecting
\(b=2a\), for which \(|b-a|=a\) would repeat an opposite pair.  Binary search
then checks both \(a+b\) and \(b-a\).  Thus `offset_pair_tests` counts every
unordered pair before this distinctness rejection.

## Reproduction

On macOS with Apple clang 21.0.0 and Python 3.14.7:

```sh
cd magic-square-of-squares

clang++ -O3 -std=c++20 -Wall -Wextra -pedantic \
  two_block_factor_search.cpp -o /tmp/two_block_factor_search

/tmp/two_block_factor_search --self-test
python3 -m unittest -v test_two_block_factor_search.py
/tmp/two_block_factor_search 1000000000000
```

The exhaustive run through \(B=10^{12}\) reported:

```text
limit=1000000000000
blocks=19903
dominant_blocks=73
block_pairs=130328
offset_values=2387660
offset_pair_tests=21507054
relation_events=0
candidate_pairs=0
elapsed_seconds=0.274565
```

The elapsed time is machine-dependent.  All integer counters and the zero
result are deterministic.

## Validation

The tests supply three independent checks:

- the built-in synthetic detector recognizes the distinct configuration
  \(\{1,2,3,4\}=\{1,3,1+3,3-1\}\) and rejects a negative control;
- a Python loop enumerates all integer circle points
  \(u^2+v^2=e^2\) directly for \(e=17^2\cdot41^2\), without Gaussian
  factorization, and matches the C++ offset and relation counts;
- an independent Python factor enumerator matches every filtered counter at
  \(B=10^6\): 43 blocks, one eligible dominant block, nine block pairs, 1,364
  offset-pair tests, and no candidate;
- a second Python comparison uses the pair
  \(97^6,693529^2\), whose offsets exceed 128 bits, and matches a limb-wise
  fingerprint of every sorted offset as well as the relation counters.

The C++ scanner uses signed 128-bit integers for individual block factors.
At \(B\le10^{12}\), their coordinates have magnitude below \(B^2=10^{24}\).
Products of two block coordinates, offset sums, and offset differences use a
four-limb unsigned 256-bit type.  They are below
\(2B^4=2\cdot10^{48}<2^{161}\), leaving more than 90 bits of headroom.  The
block-height comparison uses unsigned 128-bit arithmetic.  No floating-point
value participates in a mathematical accept/reject decision; the square-root
helper corrects its initial approximation by exact division comparisons.
An AddressSanitizer and UndefinedBehaviorSanitizer build passed the self-test
and the complete (B=10^6) filtered scan.

## Interpretation

No pair satisfying the preliminary necessary conditions produces a
two-block center with both block values at most \(10^{12}\).  The scan does
not bound the center root by \(10^{12}\): the scanned center roots can be as
large as \(10^{24}\).  Section 10 of
[two-block-exponent-one.md](two-block-exponent-one.md), rather than this
bounded computation, excludes larger block values as well.  Neither result
excludes a center with three or more distinct prime factors.
