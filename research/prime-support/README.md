# Magic square of squares research

This directory is the detailed proof and computation archive for the first
public research package in this repository. It concerns the unresolved `3 x 3`
magic square of distinct positive integer squares.

- [block-balance.md](block-balance.md) gives a corrected and strengthened
  Gaussian valuation argument, including the exact squareclass and Legendre
  filter for the remaining dominant edge factor.  It also excludes a
  dominant three-block center when both complementary blocks are extremal at
  all four offsets.
- [squarefree-semiprime.md](squarefree-semiprime.md) excludes a center root
  that is the product of two distinct primes.
- [two-block-exponent-one.md](two-block-exponent-one.md) excludes every center
  root supported on exactly two rational primes.  Its final step couples the
  two Gaussian edge relations and closes the resulting genus-one curve by a
  self-contained \(2\)-isogeny descent.
- [composite-blocks.md](composite-blocks.md) groups compatible local
  orientations into stronger composite block inequalities.
- [literature-audit.md](literature-audit.md) records the source/status check and
  the gap in the 2025/2026 claimed nonexistence proof.
- [search.py](search.py) exactly enumerates center offsets from Gaussian norm
  factorizations and checks the full additive configuration.
- [test_search.py](test_search.py) contains deterministic regression tests.
- [dominant-identity-scan.md](dominant-identity-scan.md) records a bounded,
  exhaustive falsification scan of the exact identities forced by a dominant
  prime-power block.
- [dominant_identity_search.cpp](dominant_identity_search.cpp) is the scanner;
  [test_dominant_identity_search.py](test_dominant_identity_search.py) checks it
  against an independent brute-force enumerator and synthetic positive hits.
- [center-relation-scan.md](center-relation-scan.md) documents an exhaustive
  center-root scan for all three-offset `111` and `211` relations through
  `e = 5 * 10^8`.
- [center_relation_search.cpp](center_relation_search.cpp) implements that
  scan; [test_center_relation_search.py](test_center_relation_search.py)
  crosschecks it against direct root enumeration and positive relation tests.
- [hourglass-sunit.md](hourglass-sunit.md) gives the exact primitive-denominator
  and paired Gaussian S-unit normal form for three-offset `111` and `211`
  relations, and proves that every such relation is orientation-frustrated.
- [rational_relation_search.cpp](rational_relation_search.cpp) searches exact
  rational parameters independently of a fixed common-center bound;
  [test_rational_relation_search.py](test_rational_relation_search.py)
  crosschecks it against direct enumeration of integer circle points.
- [two-block-factor-scan.md](two-block-factor-scan.md) records an independent
  bounded crosscheck of the now-excluded two-block normal form through factor
  height `max(P,Q) = 10^12`;
  [two_block_factor_search.cpp](two_block_factor_search.cpp) implements it and
  [test_two_block_factor_search.py](test_two_block_factor_search.py) supplies
  direct-circle, independent-reference, and synthetic checks.
- [three-block-squarefree.md](three-block-squarefree.md) excludes the
  all-unit case for exactly three prime-power blocks and gives a complete
  corner/edge-aware binary normal form.  Exact Gaussian quotient comparisons,
  Fermat and simultaneous-square descents, unit-circle elimination, and a
  final UFD height argument exclude all 28 physical switching classes.  A
  block-substitution audit extends the conclusion to arbitrary exponents when
  every local index is balanced or extreme.  In particular, no squarefree
  three-prime center is admissible, and a hypothetical \(p^2qr\) center must
  have the unique nonextreme `p`-index \(\mathord\pm1\).  General
  intermediate-index configurations remain open.
  [three_block_signatures.py](three_block_signatures.py) and
  [three_block_squarefree.py](three_block_squarefree.py) reproduce the finite
  classifications.
- [three-block-p2qr.md](three-block-p2qr.md) starts from the forced
  intermediate index in the squared-prime row.  Exact exceptional-row,
  aligned-quotient, composite-block, general common-factor, and coupled
  divisor-comparison inequalities, followed by factorized axis and
  congruence-sharpened skew bounds and discrete prime floors, reduce the 134
  weighted switching classes to 16 necessary survivors.  The
  independent implementations in
  [three_block_p2qr_signatures.py](three_block_p2qr_signatures.py) and
  [p2qr_monomial_filter.py](p2qr_monomial_filter.py), with their tests,
  reproduce every stage; no surviving class is asserted realizable.

Nothing in this directory is a proof of existence or global nonexistence. The
material is public for independent review and has not been peer reviewed.
