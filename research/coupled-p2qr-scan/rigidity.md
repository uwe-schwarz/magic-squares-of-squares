# Modular rigidity of the unresolved `p^2 q r` classes

## Status

This note records a new necessary condition for the sixteen `p^2 q r`
classes left open by the monomial-filter analysis in
[`../prime-support/three-block-p2qr.md`](../prime-support/three-block-p2qr.md).
For certain auxiliary primes `l`, the exact coupled Gaussian identities of a
class admit no non-degenerate solution modulo `l`.  Any integer realization
of such a class must then have `l` dividing all four offsets.  The small-
prime cases admit a complete algebraic proof; further primes are verified by
exhaustive torus enumeration.  This is not a nonexistence proof for any
class: the divisibility conditions are consistent a priori.  It is a new,
unbounded, exactly verifiable constraint of the coupled type that the
monomial filters cannot see.

## 1. The exact coupled system

Fix one of the sixteen classes with local-index matrix `j[row][column]`,
rows `(p, q, r)` with block exponents `(2, 1, 1)`, and columns
`(corner0, corner1, edge2, edge3)`.  Choose Gaussian primes
`pi pi_bar = p`, `beta beta_bar = q`, `gamma gamma_bar = r`.  For each
column `c` define the Gaussian integer

\[
 z_c \;=\; \pi^{2+j_{p,c}}\bar\pi^{2-j_{p,c}}\,
          \beta^{1+j_{q,c}}\bar\beta^{1-j_{q,c}}\,
          \gamma^{1+j_{r,c}}\bar\gamma^{1-j_{r,c}} .
\]

Then `N(z_c) = e^2` for `e = p^2 q r`, so
`d_c = |Im(z_c^2)| = 2|Re(z_c) Im(z_c)|`
lies in `S_e`: indeed `e^2 +- d_c = (Re z_c +- Im z_c)^2` are squares.
Distinctness of the four offsets follows from pairwise distinctness of the
projective index columns.  A full magic square of squares with center root
`e = p^2 q r` realizing this class exists **exactly when**

\[
 \{d_2, d_3\} \;=\; \{d_0 + d_1,\; |d_0 - d_1|\},
\]

because the centered square built from corner offsets `d_0, d_1` and edge
offsets `d_2, d_3` has all eight outer entries squares precisely for this
pattern.  All units, row conjugations, column conjugations, and the corner
and edge swaps either preserve the four offsets or are covered by
enumerating the eight choices of `(pi or pi_bar, ...)` modulo global
conjugation.  This reduces the entire class to one explicit system in the
three Gaussian primes; [coupled_p2qr_scan.cpp](coupled_p2qr_scan.cpp)
enumerates it exactly in 128-bit arithmetic.

## 2. The reduction lemma

Let `l` be an odd prime with `l !| 2 p q r`, and let `T` be the norm-one
torus of `Z[i]/l`.  Writing `rho = pi/pi_bar` and so on,

\[
 x_c \;=\; \frac{z_c^2}{e^2} \;=\;
 \rho^{2j_{p,c}} \sigma^{2j_{q,c}} \tau^{2j_{r,c}} \;\in\; T .
\]

The two additive relations among the signed values
`V_c = Im(z_c^2) = e^2 Im(x_c)` read

\[
 \varepsilon_2 V_2 = \varepsilon_0 V_0 + \varepsilon_1 V_1,
 \qquad
 \varepsilon_3 V_3 = \varepsilon_0 V_0 - \varepsilon_1 V_1,
\]

for unit signs `epsilon_c in {+-1}` arising from the free unit choices of
the `z_c`, with one of the two edge orders.  Reducing modulo `l` gives a
solution of the same system over `T` with generators of nonzero norm.
Hence:

**Lemma (rigidity).** If the class admits no solution of the reduced
system modulo `l` in which at least one offset value is nonzero, then
every integer realization of the class with `l !| 2pqr` satisfies
`l | d_c` for all four columns `c`.

## 3. The small-prime theorems

For `l = 7` the torus-squares group is `mu_4`; for `l = 11, 13` it is
`mu_6` (the two-component torus of `F_l x F_l` for `13`, the norm-one
subgroup of `F_121` for `11`).  In both cases every `x_c` lies in a cyclic
group `zeta^m` whose imaginary values are exactly `{0, +-T0}`: for `mu_6`,
`Im(zeta^2) = (zeta+zeta^{-1}) Im(zeta) = Im(zeta)` because
`zeta^2 - zeta + 1 = 0`, and `zeta^3 = -1`; for `mu_4` this is immediate.
Since `3 T0 != 0` for these `l`, a short sign analysis of the two relations
forces any non-degenerate solution to have **exactly one of the two corner
values equal to zero** and all other values nonzero.

Write `m_c` for the discrete log of `x_c` in the relevant cyclic group.
Vanishing of `Im(x_c)` is equivalent to `m_c = 0` modulo `2` (`l = 7`) or
modulo `3` (`l = 11, 13`).  The corner combination is

\[
 m_0 + m_1 \;=\; (c_0 + c_1)\cdot(r, t, w),
\]

where `c_0, c_1` are the corner index columns and `r, t, w` are the
discrete logs of `rho, sigma, tau`.  If every coordinate of the vector
`c_0 + c_1` is divisible by `n in {2, 3}`, then `m_0 + m_1 = 0 mod n`
always, so the two corners always have the **same** vanishing status,
contradicting the requirement that exactly one vanish.

**Theorem (mu_4 / mu_6 rigidity).** Let `l in {7}` with `n = 2`, or
`l in {11, 13}` with `n = 3`.  A class whose corner columns satisfy
`c_0 + c_1 in (n Z)^3` is rigid at `l`: every solution of its coupled
system modulo `l` is fully degenerate, and every integer realization has
`l | d_c` for all four offsets.

The criterion is exact: of the sixteen classes, exactly the eight with
`c_0 + c_1 in (2Z)^3` are rigid at `7`, and exactly the one class
`I0:0000/0101/0110` with `c_0 + c_1 = (-3, 0, 0) in (3Z)^3` is rigid at
`11` and at `13`.  The table in Section 5 pins this correspondence; the
test suite checks it against independent enumerations.

## 4. Verified rigidity at larger primes

Beyond `{7, 11, 13}` the torus-squares group is richer and no
two-parameter value collapse occurs; nevertheless specific classes remain
rigid at specific primes, for reasons that appear to involve subtler
additive coincidences of the value set.  The exhaustive torus enumeration
in [torus_rigidity.cpp](torus_rigidity.cpp) (C++) and
[torus_obstruction.py](torus_obstruction.py) (independent Python path)
decides each `(class, l)` pair exactly.  The two implementations agree at
every modulus tested; the Gaussian-unit checker
[modular_obstruction.cpp](modular_obstruction.cpp) agrees as well, and the
`11/13` claims were additionally re-derived by a third direct enumeration
in the test-suite development.

Verified rigid primes through `l = 997` (both implementations; the two
machines split the range):

| class (role) | rigid primes | product |
| --- | --- | ---: |
| `I2:0000/0101/01*0` (EFE) | 7, 17, 31, 89, 103, 127 | 4294767001 |
| `I2:0000/0101/0110` (EFF) | 7, 17, 29, 31, 53, 67 | 379889531 |
| `I0:0000/0101/0110` (CFF) | 11, 13, 37, 43, 67 | 15243371 |
| `I2:0000/01*0/01*1` (EEE) | 7, 17, 19, 29, 31 | 2035411 |
| `I2:0000/010*/011*` (EEE) | 7, 17, 19, 29, 31 | 2035411 |
| `I2:0000/0011/010*` (EFE) | 7, 17, 31 | 3703 |
| `I2:0000/0011/0101` (EFF) | 7, 29 | 203 |
| `I2:0000/0011/01*0` (EFE) | 7 | 7 |
| `I2:0000/0101/00*1` (EFE) | 7 | 7 |
| `I0:0000/0011/0101` (CFF) | 29 | 29 |
| four `ECE` and two `EFC` classes | none | 1 |

The complete list of rigid primes below 1000 is
`{7, 11, 13, 17, 19, 29, 31, 37, 43, 53, 67, 89, 103, 127}`;
there are none between 131 and 997.  No pattern conjecture is offered:
`l = 23` has no rigid class, `l = 127` rigidifies one class that
`l = 31` does not, and `l = 257` rigidifies none.  The six `ECE/EFC`
classes, whose corner sum `c_0 + c_1` has an odd coordinate and a
coordinate not divisible by `3`, have no rigid prime at all in the tested
range.

## 5. Corollary and limitations

**Corollary.** For a class with rigid set `S`, every integer realization
with center root `p^2 q r` satisfies: every `l in S` with
`l !in {2, p, q, r}` divides all four offsets, hence divides
`gcd(d_0, d_1, d_2, d_3)`.  Moreover each two-column monomial with exponent
vector in the difference lattice, such as `sigma^2` when
`c_1 - c_2 = (0, 2, 0)`, satisfies `sigma^2 = +-1 mod l` for those `l`,
so the product of the surviving rigid primes is bounded by a fixed power
of the center primes through the norm identity
`N(u^2 - 1) = |u^2 - 1|^2 <= 4` for unit-circle `S`-units `u`.

This is a genuine unbounded necessary condition, but it does not yet
exclude any class: the divisibility is consistent, and the norm-product
bound, with the current rigid sets, is weaker than the direct scan range.
Its value is twofold.  First, each newly verified rigid prime multiplies
the constraint at unit cost, independent of the size of the center.
Second, the phenomenon singles out the six `ECE/EFC` classes as the only
survivors that are everywhere locally non-degenerate; a future argument
that combines rigidity with the height inequalities may treat the rigid
ten first.

## 6. Reproduction

```sh
clang++ -O3 -std=c++20 -Wall -Wextra -pedantic \
  torus_rigidity.cpp -o /tmp/torus_rigidity
/tmp/torus_rigidity 7 11 13 17 19          # theorems + verified set
python3 torus_obstruction.py 7 11 13 17 19 # independent path, same output
clang++ -O3 -std=c++20 modular_obstruction.cpp -o /tmp/modular_obstruction
/tmp/modular_obstruction 7 11 13           # Gaussian-unit enumeration
python3 -m unittest -v test_coupled_p2qr_scan
```

The test suite pins: the exact coupled model (`d_c in S_e` for sampled
classes, brute-force agreement on full configurations and 111/211
relations), the class table against the upstream classifier, the prune
evaluation counts against an independent mirror, and the Section 3
criterion correspondence at `l = 7, 11, 13`.
