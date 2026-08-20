# Independent 2026 audit and next-attack map

This folder is intentionally separate from `research/prime-support/`. It records an
independent status check performed on 2026-08-20 before making any new mathematical
claim, and narrows the next useful attack on the 3x3 magic square of distinct positive
integer squares.

## Bottom line

No complete square and no global nonexistence proof was found in this pass.

The problem should still be treated as open. In particular, the 2026 Acta Arithmetica
paper of Peter Müller proves nonexistence only for the additional Euler condition
`M M^T = gamma I`; it explicitly describes the unrestricted order-three square-of-squares
problem as open. Oscar Hill's arXiv preprint claims full nonexistence, but the coefficient
comparison issue already documented in `../prime-support/literature-audit.md` prevents us
from treating that claim as established.

The strongest concrete new outcome of this audit is not a theorem: it is a correction to
our research map. A second active 2026 computational project has independently exhausted
all 9/9 root-box candidates through root bound `R = 1,000,000`, while this repository has
exhausted the *center-root* parameter through `e = 500,000,000`. These are different
height functions and neither result should be silently substituted for the other.

## Sources checked

### Peer-reviewed / primary literature

1. Andrew Bremner, **On squares of squares**, Acta Arithmetica 88 (1999), 289-297,
   DOI `10.4064/aa-88-3-289-297`.
2. Andrew Bremner, **On squares of squares II**, Acta Arithmetica 99 (2001), 289-308,
   DOI `10.4064/aa99-3-6`.
3. Paul Pierrat, Francois Thiriet, Paul Zimmermann, **Magic Squares of Squares**
   (2015 note). It gives the `1 mod 24` condition and a complete parametrization of
   arithmetic progressions of squares around a fixed square center. Importantly, it also
   explains why earlier hourglass searches that imposed pairwise coprimality do not cover
   the general case.
4. Onno Cain, **Gaussian Integers, Rings, Finite Fields, and the Magic Square of Squares**,
   arXiv:1908.03236 (2019). This is prior art for Gaussian-integer and finite-ring
   formulations.
5. Nick Rome and Shuntaro Yamagishi, **On the existence of magic squares of powers**,
   Research in Number Theory (2026 publication). Their existence theorem covers square
   magic squares of order at least four, not the order-three problem.
6. Peter Müller, **On Euler's magic matrices of sizes 3 and 8**, Acta Arithmetica 222
   (2026), 71-82, DOI `10.4064/aa250422-2-8`. The order-three nonexistence result has the
   extra orthogonality condition `M M^T = gamma I` and therefore is not a solution of the
   unrestricted problem.

### Current preprints / active computation

7. Oscar Hill, **An Algebraic Proof of the Nonexistence of 3x3 Magic Squares of Square
   Integers**, arXiv:2510.08286. This is a claimed solution, not treated here as an
   established theorem; see the detailed gap audit in the existing literature note.
8. `mystimath/magic-square-of-squares-3x3`, status dated 2026-07-21. Its B6 scanner
   reports an exhaustive 9/9 search through root-box bound `R = 1,000,000`, with no
   candidate. This is useful independent computational evidence, but it is not a proof of
   global nonexistence.

This is still a bounded literature search, not a MathSciNet/zbMATH priority search. No
novelty claim follows from absence in these sources.

## Height coordinates: do not conflate them

Three different bounded statements now occur in the ecosystem:

- this repository: all centered offset relations of types `111` and `211` are absent for
  center root `e <= 500,000,000`;
- the independent 2026 B6 computation: no full 9/9 square with every entry root in its
  root box through `R = 1,000,000`;
- older hourglass searches use still different parametrizations and sometimes extra
  coprimality assumptions.

A root-box bound and a center-root bound are not equivalent. A future README should state
which height is bounded whenever a search number is quoted.

## Re-derivation of the exact four-offset target

Every 3x3 magic square is determined by its center `E` and two offsets `a,b`:

```text
E+a       E-a-b     E+b
E-a+b     E         E+a-b
E-b       E+a+b     E-a
```

For a square of squares, write `E=e^2`. Define

`S_e = { d>0 : e^2-d and e^2+d are both integer squares }`.

Then a full solution is exactly a choice of distinct positive `a,b` for which

`{a, b, a+b, |a-b|} subset S_e`, with all nine resulting entries positive and distinct.

This is the right interface between the additive problem and Gaussian factorization. It is
also why a `111` relation is already fatal to a bounded full search: every full four-offset
configuration contains such a triple.

## What the current prime-support result actually leaves

The existing work proves that a primitive center root cannot have support on exactly two
rational primes and eliminates the balanced/extreme three-block cases. For the first
intermediate pattern `e=p^2 q r`, the exact switching classifier has 134 physical classes;
118 are currently excluded and 16 necessary classes remain.

Those 16 survivors are therefore a much smaller and more structured target than another
uniform scan over all centers.

## Recommended next attack

The next useful step is to couple the **four exact Gaussian quotient identities** for each
of the 16 surviving `p^2 q r` classes, rather than add another independent monomial bound.
The present filter deliberately projects each identity down to valuations, heights,
quadratic-character snippets, or two-term divisibility. That loses correlations between
relations sharing the same Gaussian primes.

A concrete implementation should:

1. reconstruct the actual local Gaussian monomials for all four physical offsets of each
   survivor;
2. introduce one Gaussian prime representative for each of `p,q,r` and preserve the same
   representatives across all four relations;
3. normalize units and global conjugation once, not independently per deletion;
4. impose the two additive offset equations simultaneously;
5. eliminate units first, then compare the resulting rational real/imaginary parts;
6. only after this exact coupling, project to congruences or height inequalities.

This attacks exactly the information that the current Farkas/monomial machinery throws
away. If it closes all 16 classes, it would prove that a center of type `p^2 q r` is
impossible. If it leaves classes, the residual polynomial systems are candidates for
Gröbner, resultant, elliptic/hyperelliptic, or Brauer-Manin analysis.

## A useful negative conclusion

A generic finite-field attack is unlikely to settle the problem by itself. Cain already
places finite rings/fields in the prior art, and current computational work finds local
configurations broadly enough that a proof will need compatibility across primes or a
global Diophantine obstruction. Modular arithmetic remains valuable as a sieve *after*
the exact Gaussian coupling, not as a stand-alone existence test.

## Claim discipline

Nothing in this folder is claimed to be mathematically new. The contribution of this pass
is an updated independent source audit, separation of incompatible computational height
claims, and a sharply scoped next proof target. Any theorem produced by the proposed
coupled-identity attack must be rechecked against the sources above and then against a
systematic MathSciNet/zbMATH search before priority language is used.
