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

**Correction (2026-08-23).**  A full re-verification with the committed code
(unmodified `torus_rigidity.cpp`, cross-checked against
`torus_obstruction.py`) found several errors in the table first recorded
here.  `I2:0000/01*0/01*1` is *solvable* modulo 19 — all three independent
implementations agree — so 19 is dropped from its rigid set.  Conversely,
the old table missed rigid primes: 29 and 149 for `I0:0000/0101/0110`, 151
for `I2:0000/0011/0101`, and 151 and 197 for `I2:0000/0101/0110`; every
added (class, prime) pair is confirmed by both implementations, and the
`l^2` sweep of Section 4b independently reproduces the whole classification
through 31 (rigid at `l` exactly when the `l^2` minimum common valuation is
1).  The old claim that no prime between 131 and 997 rigidifies any class
is therefore false (149, 151 and 197 do).  The likely cause is a
transcription loss when the original two-machine sweep was merged into this
table; the code was right, the recorded table was not.  A re-verification
sweep of 307-997 (committed code, four parallel ranges) found no further
rigid prime, so the table below is the complete classification below 1000.  (Two printed products were also
wrong: 3703 should be 3689, and 2035411 should be 106981 / 2032639.)

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

Verified rigid primes through `l = 997` (re-verified 2026-08-23 with the
committed code; `7..293` additionally cross-checked against the independent
Python implementation):

| class (role) | rigid primes | product |
| --- | --- | ---: |
| `I2:0000/0101/0110` (EFF) | 7, 17, 29, 31, 53, 67, 151, 197 | 11300573878657 |
| `I2:0000/0101/01*0` (EFE) | 7, 17, 31, 89, 103, 127 | 4294767001 |
| `I0:0000/0101/0110` (CFF) | 11, 13, 29, 37, 43, 67, 149 | 65866606091 |
| `I2:0000/010*/011*` (EEE) | 7, 17, 19, 29, 31 | 2032639 |
| `I2:0000/0011/0101` (EFF) | 7, 29, 151 | 30653 |
| `I2:0000/01*0/01*1` (EEE) | 7, 17, 29, 31 | 106981 |
| `I2:0000/0011/010*` (EFE) | 7, 17, 31 | 3689 |
| `I2:0000/0011/01*0` (EFE) | 7 | 7 |
| `I2:0000/0101/00*1` (EFE) | 7 | 7 |
| `I0:0000/0011/0101` (CFF) | 29 | 29 |
| four `ECE` and two `EFC` classes | none | 1 |

The complete list of rigid primes below 1000 is
`{7, 11, 13, 17, 19, 29, 31, 37, 43, 53, 67, 89, 103, 127, 149, 151, 197}`;
there are no others between 199 and 997.  No pattern conjecture is
offered: `l = 23` has no rigid class, `l = 127` rigidifies one class that
`l = 31` does not, and `l = 257` rigidifies none.  The six `ECE/EFC`
classes, whose corner sum `c_0 + c_1` has an odd coordinate and a
coordinate not divisible by `3`, have no rigid prime at all in the tested
range.

Note that 151 is 3 mod 4, hence never a factor of any center root
`e = p^2 q r` (whose prime factors all split in Z[i]): its divisibility is
unconditional for the two `EFF` classes it rigidifies.

## 4b. The l^2 cap: rigidity never doubles at odd primes

**Theorem (l^2 cap).**  For each of the sixteen classes and every odd prime
`l`, the coupled torus system modulo `l^2` admits a solution whose four
offsets have common `l`-valuation exactly 1.  Consequently the rigidity
lemma of Section 2 can never be strengthened to a forced `l^2 | d_c` by
torus enumeration: at every odd prime where a class is rigid, the forced
divisibility of the method is exactly `l | d_c`.

*Proof.*  Every element of the norm-one torus of `Z[i]/l^2` factors uniquely
as `omega * (1 + l*b*i)` with `omega` Teichmüller and `b` in `Z/l`, because
`N(1 + l*(a+bi)) = 1 + 2*l*a` (mod `l^2`) forces the principal part purely
imaginary.  Using `(1 + l*z)^n = 1 + n*l*z` (mod `l^2`) for every integer
`n`, the normalized column at generators `1 + l*b_s*i` (all-ones base) is

```
x_c = (1 + l*K_c*i),   K_c = sum_s 2*j[s,c]*b_s,   Im(x_c) = l*K_c,
```

*exactly* modulo `l^2` — no linearization error.  Writing `u = M b` for the
`4x3` local-index matrix `M`, a sign/edge pattern holds modulo `l^2` on the
offsets `l*u_c` exactly when the same linear relations hold on `u` modulo
`l`.  Two finite computations finish the argument for all odd primes at
once ([l2_linearization.py](l2_linearization.py), pinned by tests):

1. `M` has rank 3 over `Q` for all sixteen classes, and the gcd of its four
   `3x3` minors is a power of two (2 or 4), so `M` is injective modulo
   every odd `l`: `b != 0` implies `M b != 0`.
2. Two homogeneous linear equations in three unknowns always have a
   nonzero solution.

So any nonzero solution `b` of a pattern's linear pair yields the witness
generators `1 + l*b_s*i`, which satisfy the pattern equations modulo `l^2`
with common valuation exactly 1 (some `u_c` is nonzero, so the
corresponding offset is divisible by `l` but not `l^2`).  `[]`

The module verifies each witness *independently of the derivation*: it
recomputes the four columns with exact Gaussian arithmetic, checks the
generators are norm-one, checks both pattern equations, and checks the
common valuation is exactly 1.  Verified at every prime in
`{3, 5, 7, 11, 13, 17, 19, 29, 31, 37, 43, 53, 67, 89, 103, 127, 149,
151, 197, 251, 997}` for all sixteen classes.  The exhaustive `l^2`
enumerations agree: at every rigid prime `l <= 31` the minimum common
valuation over all solutions is exactly 1, never 2 (dual Python path with
counter-for-counter brute agreement and the C++ full-torus mirror at exact
factor-8 counts through `l = 19`; C++ mirror plus witnesses at 29 and 31,
committed ledger [l2_rigidity_ledger.json](l2_rigidity_ledger.json)).

Scope, stated honestly.  The theorem caps the *mod-`l^2` enumeration*
argument only.  It does not assert that integer realizations with
`v_l(d) = 1` exist (a valuation-1 torus branch need not lift to `l^3`
compatibly, let alone come from a realization); it does not exclude deeper
`l`-adic forcing at level `l^3`; and it says nothing at `l = 2`, where the
committed prime-power-rigidity scans *do* find genuine forced `16 | d_c`
structure (there `+-1` coincide and the pattern equations degenerate
modulo 2, which is exactly why the odd-prime argument does not apply).

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

## 5b. Cross-validation against Roberts–Underwood (external)

Roberts (2013) and Underwood (2014), in exactly the centered parametrization
used by this repository (neighbors of `x = e^2` at offsets
`y, z, y+z, y-z`), proved by direct residue analysis that `y*z` is divisible
by `2^6 * 3^2 * 5^2 * 7^2 * 11 * 13 * 19 * 31`, that `x*y*z` is divisible by
every prime below 40 except 23, and that `x*y*z*(y+z)*(y-z)` is divisible by
every prime below 70 except 59 (about `1.5 * 10^30` in total), with `24 | y`
and `24 | z` individually.  Their two escape primes are exactly 23 and 59.

Our torus sweep is an independent computation in a different model (the
norm-one reduction of the per-class monomial system).  It found the rigid
primes for surviving classes inside
{7, 11, 13, 17, 19, 29, 31, 37, 43, 53, 67, 89, 103, 127}, with **23 and 59
not rigid for any class** — matching their escape primes exactly.  The two
analyses also have complementary strength: theirs forces divisibility of the
five-term product by all primes below 70 except 59; ours forces divisibility
of *all four offsets simultaneously* by each class's rigid product, which
includes the primes 89, 103 and 127 beyond their range but only for the
classes whose torus is degenerate there.  See
[`../independent-2026-audit/multimagie-lineage.md`](../independent-2026-audit/multimagie-lineage.md)
for the source record, including Zimmermann et al.'s `24 | d` lemma which
stacks with both.

A consistency check rather than a new constraint: the classical
`entries = 1 mod 24` congruences (Zimmermann's Lemma 1, Underwood's
`24 | y, 24 | z`) are *automatic* in the monomial model — enumerating all
generator flips and all generator residues mod 8 and mod 3 shows every
class realizes `8 | d_c` and `3 | d_c` for all four columns at every
residue choice (the odd-square AP step is a multiple of 8 by construction,
and the Gaussian algebra forces the mod-3 part).  These congruences
therefore cannot eliminate any class; only the auxiliary-prime rigidity
above carries class-specific information.

## 6. Reproduction

```sh
clang++ -O3 -std=c++20 -Wall -Wextra -pedantic \
  torus_rigidity.cpp -o /tmp/torus_rigidity
/tmp/torus_rigidity 7 11 13 17 19          # theorems + verified set
python3 torus_obstruction.py 7 11 13 17 19 # independent path, same output
clang++ -O3 -std=c++20 modular_obstruction.cpp -o /tmp/modular_obstruction
/tmp/modular_obstruction 7 11 13           # Gaussian-unit enumeration
python3 -m unittest -v test_coupled_p2qr_scan

# prime-power (l^2) layer: enumeration (dual path), C++ mirror, cap theorem
python3 torus_obstruction_l2.py 7 11 13            # brute == linear, asserted
python3 torus_obstruction_l2.py 17 19 --linear-only
clang++ -O2 -std=c++20 torus_rigidity_l2.cpp -o /tmp/torus_rigidity_l2
/tmp/torus_rigidity_l2 7 11 13 17 19 29 31         # counts = 8x the Python
python3 l2_linearization.py 7 19 151               # cap-theorem witnesses
python3 -m unittest -v test_torus_l2
```

The test suite pins: the exact coupled model (`d_c in S_e` for sampled
classes, brute-force agreement on full configurations and 111/211
relations), the class table against the upstream classifier, the prune
evaluation counts against an independent mirror, and the Section 3
criterion correspondence at `l = 7, 11, 13`.  The `l^2` layer
([test_torus_l2.py](test_torus_l2.py)) pins: counter-for-counter agreement
of the brute and linear Python paths and the factor-8 agreement of the C++
full-torus counts, the corrected rigid-prime classification through 31
against the committed mod-`l` checker, the rank/minor finite verification
behind the Section 4b theorem, and witnesses for every rigid prime.
