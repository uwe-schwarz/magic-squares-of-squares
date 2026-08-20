# Hourglass denominator and Gaussian S-unit normal form

## Status

This note isolates the exact three-offset problem behind a magic hourglass of
squares.  It gives a denominator-support normal form, proves that every such
three-offset relation has a frustrated Gaussian-orientation cycle, and records
bounded exact evidence.  It is not a proof of global nonexistence, has not
been peer reviewed, and makes no novelty claim.

The two coefficient patterns considered below are

\[
 c_1r_1+c_2r_2+c_3r_3=0,
 \qquad
 \{|c_1|,|c_2|,|c_3|\}=\{1,1,1\}\text{ or }\{2,1,1\},
 \tag{1}
\]

for three pairwise distinct positive admissible offsets.  The first pattern
is the magic-hourglass equation.  Both patterns occur among the three-element
subsets of the four offsets of a full `3 x 3` magic square.

## 1. Primitive rational offsets

Put

\[
 f(t)=\frac{4t(1-t^2)}{(1+t^2)^2}.
\]

Every positive rational number \(r\) for which \(1-r\) and \(1+r\) are
rational squares has the following primitive form.  Choose coprime integers
\(m>n>0\) of opposite parity and set

\[
 h=m^2+n^2,\qquad u=m^2-n^2,\qquad v=2mn,
\]
\[
 q=2uv=4mn(m^2-n^2),\qquad r=\frac q{h^2}=f(n/m).
\tag{2}
\]

Indeed \(u^2+v^2=h^2\) and \(1\mathbin\pm r=(u\mathbin\pm v)^2/h^2\).
Conversely, clearing a rational point on \(x^2+y^2=1\) and dividing out the
gcd gives (2).  Primitivity gives

\[
 h\text{ odd},\qquad \gcd(q,h)=1,
 \tag{3}
\]

and every prime divisor of \(h\) is congruent to `1 mod 4`.

Let \(r_i=q_i/h_i^2\) be three such reduced offsets.  They can be realized
around the common center root

\[
 L=\operatorname{lcm}(h_1,h_2,h_3).
\]

Writing \(w_i=u_i+iv_i\), the Gaussian integer
\(z_i=(L/h_i)w_i\) has norm \(L^2\), and its signed integer offset is

\[
 D_i=\operatorname{Im}(z_i^2)=\left(\frac L{h_i}\right)^2q_i.
\tag{4}
\]

Thus the rational and common-integer-center formulations are equivalent.

## 2. Denominator-support lemma

### Lemma

If (1) holds, then for every rational prime \(p\), the maximum of

\[
 v_p(h_1),\quad v_p(h_2),\quad v_p(h_3)
\tag{5}
\]

is attained at least twice.

### Proof

The denominators \(h_i\) are odd, so \(p=2\) is absent.  Suppose an odd
prime has a unique maximum, at \(h_1\), say.  Multiply (1) by the square of a
common denominator.  By (3), the first term is a `p`-adic unit after removal
of the largest denominator power, while the other two terms remain divisible
by `p`.  This cannot sum to zero.  The possible coefficient `2` is also a
`p`-adic unit.  This proves the lemma.

### Canonical support decomposition

Let \(g=\gcd(h_1,h_2,h_3)\).  Applying the lemma prime by prime after removing
the common minimum exponent gives unique positive integers \(A,B,C\) such
that

\[
 \boxed{h_1=gAB,\qquad h_2=gAC,\qquad h_3=gBC,}
 \tag{6}
\]

where \(A,B,C\) are pairwise coprime.  A prime-power layer in `A` occurs at
the same maximal exponent in \(h_1,h_2\), a layer in `B` occurs in
\(h_1,h_3\), and a layer in `C` occurs in \(h_2,h_3\).  The factor `g` may
share rational primes with one of `A`, `B`, or `C`; it records the common
minimum exponent.

Since \(L=gABC\), equation (1) becomes the exact integer equation

\[
 \boxed{c_1C^2q_1+c_2B^2q_2+c_3A^2q_3=0.}
 \tag{7}
\]

This four-block decomposition is the global form of the local rule that the
minimum offset valuation must occur at least twice.

## 3. The paired Gaussian S-unit equation

Fix \(p=\pi_p\bar\pi_p\) in \(\mathbb Z[i]\) for every prime occurring in the
denominators.  Since \(w_i\) is primitive and \(N(w_i)=h_i^2\), unique
factorization gives

\[
 w_i=\varepsilon_i
 \prod_{p\mid h_i}\pi_{p,i}^{\,2v_p(h_i)},
 \tag{8}
\]

where each \(\pi_{p,i}\) is either \(\pi_p\) or \(\bar\pi_p\).  Define

\[
 x_i=\frac{w_i^2}{h_i^2}
 =\varepsilon_i^2\prod_{p\mid h_i}
 \left(\frac{\pi_p}{\bar\pi_p}\right)^{2\sigma_{p,i}v_p(h_i)},
 \qquad \sigma_{p,i}\in\{1,-1\}.
\tag{9}
\]

Then \(\bar x_i=x_i^{-1}\), and (1) is exactly the paired six-term S-unit
equation

\[
 \boxed{\sum_{i=1}^3c_i(x_i-x_i^{-1})=0.}
 \tag{10}
\]

The unit squares \(\varepsilon_i^2\in\{1,-1\}\) can be absorbed into the
signed coefficients.  Pairwise distinct positive offsets mean

\[
 x_i\notin\{\mathord\pm x_j,\mathord\pm x_j^{-1}\}
 \quad(i\ne j).
\tag{11}
\]

Equation (10), together with the support skeleton (6), is the exact global
Gaussian/S-unit formulation; it does not discard intermediate prime-power
allocations.

## 4. Coherent-orientation obstruction

View the signs \(\sigma_{p,i}\) as labels on the incidence graph whose left
vertices are rational primes and whose right vertices are the three offsets,
with an edge when \(p\mid h_i\).

The orientation signature is **coherent** if there are prime signs
\(\tau_p\in\{1,-1\}\) and column signs \(\kappa_i\in\{1,-1\}\) such that

\[
 \sigma_{p,i}=\tau_p\kappa_i
 \quad\text{whenever }p\mid h_i.
\tag{12}
\]

Equivalently, independently conjugating the three \(w_i\) makes every
rational-prime block use one common chosen Gaussian orientation.  In binary
notation this is affine separability on the incomplete incidence matrix.  It
holds exactly when every cycle of the signed bipartite incidence graph has
even parity.

### Theorem

If three pairwise distinct positive admissible offsets satisfy (1) and their
orientation signature is coherent, then

\[
 \boxed{g=1.}
\tag{13}
\]

Moreover, after choosing the coherent orientations, the relation satisfies
an exact Gaussian identity with quotient of absolute value one.

### Proof

For a rational factor `T` in (6), let \(\mathcal T\) be the product of the
chosen Gaussian prime powers with

\[
 N(\mathcal T)=T^2,\qquad |\mathcal T|=T.
\]

Coherence and independent conjugation give, up to units,

\[
 w_1=\mathcal G\mathcal A\mathcal B,\qquad
 w_2=\mathcal G\mathcal A\mathcal C,\qquad
 w_3=\mathcal G\mathcal B\mathcal C.
\tag{14}
\]

This remains valid when `g` shares a rational prime with one pair factor:
coherence selects the same Gaussian prime on both exponent layers.

Put

\[
 X=\mathcal G\mathcal A\mathcal B\mathcal C,
 \qquad R=\mathcal G X=\mathcal G^2\mathcal A\mathcal B\mathcal C,
\]
\[
 T_1=\mathcal A\mathcal B\bar{\mathcal C},\qquad
 T_2=\mathcal A\bar{\mathcal B}\mathcal C,\qquad
 T_3=\bar{\mathcal A}\mathcal B\mathcal C.
\tag{15}
\]

All three \(T_i\) have modulus \(ABC\).  After absorbing the unit squares and
projection signs into \(c_i\), direct multiplication shows

\[
 R(c_1T_1+c_2T_2+c_3T_3)
   =c_1z_1^2+c_2z_2^2+c_3z_3^2\in\mathbb Z.
\tag{16}
\]

Let \(K=c_1T_1+c_2T_2+c_3T_3\).  The Gaussian integer `R` contains only one
prime from each conjugate pair, so \(\gcd(R,\bar R)=1\).  If \(K\ne0\), (16)
implies

\[
 \bar R\mid K,
 \qquad K=\bar R n,\quad n\in\mathbb Z\setminus\{0\}.
\tag{17}
\]

For coefficient type `111`, \(K\ne0\): a zero sum of three vectors of equal
length would make their ratios primitive cube roots of unity, which are not
in \(\mathbb Q(i)\).  Equality in the triangle bound would make the signed
vectors equal and would repeat an absolute offset.  Hence

\[
 g^2ABC|n|=|K|<3ABC.
\tag{18}
\]

Every block in (15) is congruent to `1` modulo \(2\mathbb Z[i]\).  Therefore
`n` is odd.  Equation (18) gives \(g^2<3\), and the positive odd integer `g`
must be `1`.  When `g=1`, (18) also gives \(|n|=1\), so

\[
 K=\mathord\pm\bar X.
\tag{19}
\]

For coefficient type `211`, a hypothetical \(K=0\) would force equality in
the triangle inequality: the two coefficient-one vectors would be equal and
opposite the doubled vector.  Multiplication by `R` would then make two of the
absolute offsets equal, contrary to the hypothesis.  Parity gives
\(K\in2\mathbb Z[i]\).  Applying (17) to \(K/2\) and using the strict bound
\(|K/2|<2ABC\) gives

\[
 g^2ABC|n|=|K/2|<2ABC.
\tag{20}
\]

Thus `g=1`, and then \(|n|=1\), so

\[
 K=\mathord\pm2\bar X.
\tag{21}
\]

This proves the theorem.

### A `111` relation is never coherent

For coefficient type `111`, the conclusion can be sharpened: the orientation
signature of any three pairwise distinct positive admissible offsets is
necessarily incoherent.

The theorem already excludes a coherent signature when \(g>1\).  Suppose
therefore that \(g=1\), and put

\[
 \alpha=\frac{\mathcal A}{\bar{\mathcal A}},\qquad
 \beta =\frac{\mathcal B}{\bar{\mathcal B}},\qquad
 \gamma=\frac{\mathcal C}{\bar{\mathcal C}}.
\]

Dividing (19) by \(\bar X\), and retaining the absorbed coefficient signs,
gives

\[
 c_1\alpha\beta+c_2\alpha\gamma+c_3\beta\gamma=s,
 \qquad c_1,c_2,c_3,s\in\{1,-1\}.
\]

The four terms obtained by moving \(s\) to the left all have complex modulus
one and sum to zero.  Any four complex units with zero sum split into two
antipodal pairs.  One quick proof is to call them \(u_1,\ldots,u_4\): their
first elementary symmetric function is zero, while
\[
 e_3=u_1u_2u_3u_4\sum_i u_i^{-1}
     =u_1u_2u_3u_4\,\overline{\sum_i u_i}=0.
\]
Thus their monic root polynomial contains only even powers, so its roots occur
in opposite pairs.

There are only three possible pairings.  They respectively force both
\(\mathcal B,\mathcal C\), both \(\mathcal A,\mathcal C\), or both
\(\mathcal A,\mathcal B\) to be Gaussian units.  For example, one pairing
gives \(\beta=\pm\gamma\); unique factorization and the disjoint rational-prime
supports of \(B,C\), together with
\(\gcd(\mathcal B,\bar{\mathcal B})=1\), force \(B=C=1\).  Pairing a product
with the constant similarly gives \(\alpha\beta=\pm1\) and forces
\(A=B=1\).  The other cases are symmetric.

In every pairing at least two of \(A,B,C\) are therefore one.  But (6) would
then make one of \(h_1,h_2,h_3\) equal to one, impossible in the positive
primitive parametrization (2), where \(m>n>0\).  This contradiction proves

\[
 \boxed{\text{Every coefficient-`111` relation has a frustrated
 orientation cycle.}}
\]

### A `211` relation is never coherent

The same conclusion holds for coefficient type `211`, but one genus-one
calculation is needed.  The theorem again reduces a hypothetical coherent
signature to \(g=1\) and (21).  Relabel the pair-support factors so that the
doubled term is \(T_1\).  After division by \(\bar X\), the most general
signed identity is

\[
 2a\alpha\beta+b\alpha\gamma+c\beta\gamma=2d,
 \qquad a,b,c,d\in\{1,-1\}.
\]

Put

\[
 x=\alpha,\qquad y=da\beta,\qquad z=db\gamma,
 \qquad s=abcd.
\]

Multiplication of a chosen Gaussian block by \(i\) realizes each sign change
without changing its rational support.  The identity is now

\[
 \boxed{2xy+xz+s yz=2},\qquad |x|=|y|=|z|=1.
\]

A ratio \(\mathcal T/\bar{\mathcal T}\) belonging to a nontrivial one-sided
Gaussian block is neither real nor purely imaginary.  Otherwise
\(\mathcal T\) would be associated to \(\bar{\mathcal T}\), contrary to
unique factorization and \(\gcd(\mathcal T,\bar{\mathcal T})=1\).

Taking absolute values in

\[
 x(2y+z)=2-syz,
 \qquad y(2x+sz)=2-xz
\]

gives, respectively,

\[
 \operatorname{Re}(y\bar z)+s\operatorname{Re}(yz)=0,
 \qquad
 s\operatorname{Re}(x\bar z)+\operatorname{Re}(xz)=0.
\]

For \(s=1\), these say
\(2\operatorname{Re}(y)\operatorname{Re}(z)=0\) and
\(2\operatorname{Re}(x)\operatorname{Re}(z)=0\).  For \(s=-1\), they say
\(2\operatorname{Im}(y)\operatorname{Im}(z)=0\) and
\(-2\operatorname{Im}(x)\operatorname{Im}(z)=0\).  Thus three nontrivial
pair-support factors are impossible.  If exactly one factor is trivial, the
same two equations exclude a trivial factor occurring in the doubled product
\(xy\).  If at least two factors are trivial, (6) makes one primitive
denominator \(h_i\) equal to one, which is impossible for a positive offset.

The only case not yet excluded therefore has \(C=1\): the factor opposite
the doubled term is trivial, while \(A,B>1\).  Absorb the sign of the unit
\(\gamma\) so that \(z=1\).  The first norm identity excludes \(s=1\), and
the remaining equation is

\[
 2xy+x-y=2,
 \qquad
 y=\frac{2-x}{2x-1}.
\]

Write \(x=\mathcal A/\bar{\mathcal A}\) with
\(\mathcal A=R+iS\) and \(R^2+S^2=A^2\).  Both \(R,S\) are nonzero.  The
last display becomes

\[
 y=\frac{R-3iS}{R+3iS}.
\]

On the other hand, \(y=\mathcal B/\bar{\mathcal B}\) and
\(N(\mathcal B)=B^2\).  Hence
\(\mathcal B(R+3iS)\) is a rational integer.  Taking norms shows that
\(R^2+9S^2\) is a rational square.  Since it is an integer, it is an integer
square, say

\[
 R^2+S^2=A^2,
 \qquad R^2+9S^2=W^2.
\]

It remains to exclude this simultaneous pair.  Put

\[
 t=\frac RS,\qquad T=t^2,
 \qquad V=t\frac AS\frac WS.
\]

Then \(T>0\) is a rational square and

\[
 E:\qquad V^2=T(T+1)(T+9)=T^3+10T^2+9T.
\]

Here is a self-contained rank computation.  The standard `2`-isogeny at
\((0,0)\) sends this curve to

\[
 E':\qquad v^2=u^3-20u^2+64u.
\]

For a curve \(v^2=u^3+a u^2+b u\), the descent image is represented by
square-free divisors \(b_1\) of \(b\); writing \(b=b_1b_2\), the associated
cover is

\[
 N^2=b_1M^4+aM^2E_0^2+b_2E_0^4,
 \qquad \gcd(M,E_0)=1.
\]

For \(E\), the only possible classes are
\(1,-1,3,-3\), and all four occur: they are represented by the point at
infinity (or \((0,0)\)), \((-1,0)\), \((3,12)\), and \((-3,6)\).
For \(E'\), the possible classes are \(1,-1,2,-2\).  The covers for
\(-1\) and \(-2\) are negative definite.  The class `2` would require

\[
 N^2=2M^4-20M^2E_0^2+32E_0^4.
\]

An odd \(M\) makes the right side `2 mod 4`.  Otherwise write
\(M=2m\); primitivity makes \(E_0\) odd, and then \(N=4n\) and

\[
 n^2=2m^4-5m^2E_0^2+2E_0^4.
\]

For even \(m\) the right side is `2 mod 4`, while for odd \(m\) it is
`7 mod 8`.  Thus the two descent-image sizes are `4` and `1`, and the
`2`-isogeny rank formula gives

\[
 2^{\operatorname{rank}E(\mathbb Q)}=\frac{4\cdot1}{4}=1.
\]

The primes `5` and `7` are of good reduction, and direct residue counts give

\[
 \#E(\mathbb F_5)=\#E(\mathbb F_7)=8.
\]

Consequently the rational torsion has order at most eight.  The eight points

\[
 O,\ (0,0),\ (-1,0),\ (-9,0),\ (3,\mathord\pm12),\
 (-3,\mathord\pm6)
\]

are rational, so rank zero and the reduction bound show that this is all of
\(E(\mathbb Q)\).  Its nonnegative first coordinates are `0` and `3`; the
former is the excluded boundary \(t=0\), and the latter is not a rational
square.  This contradiction proves

\[
 \boxed{\text{Every coefficient-`211` relation has a frustrated
 orientation cycle.}}
\]

### What any survivor must look like

- Every relation of type `111` or `211` has a frustrated orientation cycle,
  whether or not \(g\) is one.  On three offset vertices this is either a
  four-cycle from two prime blocks supported on the same offset pair with
  inconsistent relative orientations, or a six-cycle through three prime
  blocks and all three offsets.
- If \(g=1\), every prime occurs in exactly one of the pair-support factors
  `A`, `B`, `C`.  With at most three distinct center primes, incoherence can
  occur only through two incompatible parallel pair supports, or through one
  block of each pair type `12`, `13`, `23` with odd triangle parity.
- For a full four-offset configuration with exactly three center-prime
  blocks, each of its four three-offset deletion relations must therefore be
  frustrated.  The incidence pattern in which all three blocks are balanced
  at the same offset is impossible independently: that offset would have
  primitive denominator one and hence would be zero.

This separates a genuine global obstruction - orientation frustration - from
mere bookkeeping choices of Gaussian conjugates.

## 5. Prime powers and two prime-power blocks

For a single prime-power center, the incidence graph is coherent.  All three
primitive hypotenuses are positive powers of the same prime, so `g > 1`.
The theorem therefore recovers the exclusion of coefficient types `111` and
`211`.  The sharper elementary proof is the distinct-valuation argument:
the admissible offsets for \(p^k\) have pairwise distinct `p`-adic valuations.

There is also a useful extension of the squarefree-semiprime result.  Suppose
the common center root is

\[
 e=p^kq^\ell
\]

and every local allocation used by the three offsets is either balanced or
extreme - its absolute index is in \(\{0,k\}\) at `p` and in
\(\{0,\ell\}\) at `q`.  Put \(P=p^k,Q=q^\ell\), and choose primitive Gaussian
integers

\[
 \alpha=A+iB,\quad A^2+B^2=P^2,\qquad
 \beta=C+iD,\quad C^2+D^2=Q^2.
\]

Up to signs and the common factor `2`, the only four common-center offset
values are

\[
 Q^2AB,\quad P^2CD,\quad
 (AC-BD)(AD+BC),\quad (AC+BD)(BC-AD).
\tag{22}
\]

The sixteen signed sums of three distinct values in (22) are all nonzero.
Twelve factor into expressions excluded by positivity, coprimality, or the
irrationality of \(\sqrt3\).  The remaining four would force

\[
 A^4-3A^2B^2+B^4=W^2
\tag{23}
\]

or the analogous equation for `C,D`.  The curve
\(y^2=x^4-3x^2+1\) maps birationally to

\[
 E:Y^2=X(X+1)(X+5)
\]

by

\[
 U=\frac{y+1}{x^2},\qquad X=2U-3,qquad
 Y=2x(U^2-1).
\]

The curve `E` has rank zero and torsion
\((\mathbb Z/2\mathbb Z)^2\); the quartic therefore has only its degenerate
rational points.  This proves:

\[
 \boxed{\text{A two-prime-block `111` relation needs a genuine intermediate
 local index.}}
\tag{24}
\]

In particular, the squarefree case is excluded.  The argument is algebraic
in the two coprime blocks `P,Q`; primality of the blocks is not used.  This
section alone does not exclude an intermediate index \(0<|j|<k\); the later
coupled-edge proof in
[two-block-exponent-one.md](two-block-exponent-one.md) excludes the complete
two-prime-block center.

The calculation in this section is the semiprime argument of Valentyn
Voronsbekher's 2026 preprint, applied to arbitrary prime-power blocks.  The
preprint is unrefereed.  Its algebra and elliptic-curve conclusion were
independently checked here; no priority or reliability claim beyond that
bounded audit is intended.

## 6. Independent rational-parameter scan

[rational_relation_search.cpp](rational_relation_search.cpp) enumerates every
primitive pair `m,n` in (2) with

\[
 h=m^2+n^2\le H,
\]

deduplicates the exact reduced fractions `q/h^2`, and tests every pair for

\[
 x+y=z,\qquad 2x+y=z,\qquad x+2y=z,\qquad x+z=2y.
\tag{25}
\]

The first identity is type `111`; the other three exhaust type `211` for
three sorted distinct positive values.  All arithmetic decisions are exact;
128-bit integers are used for cross-products and reduction.  An optional
thread count partitions the outer pair loop dynamically; workers share only
the immutable fraction table and hash set, then reduce integer counters after
joining.  It changes runtime, not the enumerated pairs or acceptance criteria.

The initial single-threaded scan through `H = 1000000` reported

```text
hypotenuse_limit=1000000
primitive_offset_values=159139
offset_pairs=12662531091
relation_111_events=0
relation_211_events=0
```

A larger four-thread run on the `dev` host completed on 2026-08-20.  Its exact
summary was

```text
hypotenuse_limit=5500000
threads=4
primitive_offset_values=875336
offset_pairs=383106118780
relation_111_events=0
relation_211_events=0
```

The wall-clock time was `8:42:23.86` (`124124.96s` user, `52.63s` system,
`396%` CPU).  The pair count is independently checkable from the number of
deduplicated values:

\[
\binom{875336}{2}=383106118780.
\]

The `H` here is the primitive Pythagorean hypotenuse (m^2+n^2).  It should
not be compared numerically with the unreproduced `height <= 213281` claim in
a 2017 MathOverflow comment: that comment does not define its height
convention or provide code, and the standard height of the rational parameter
(n/m) would be (max(m,n)), not (m^2+n^2).  The present run does add a
fully reproducible `211` test under its stated hypotenuse bound.

This is independent of the common-center scan through `e = 5 * 10^8`: three
individual primitive denominators below `5500000` can have least common
multiple far above `5 * 10^8`.  The result is still only a bounded falsification,
not a proof.

[test_rational_relation_search.py](test_rational_relation_search.py) checks
the C++ result through `H = 500` against a direct Python enumeration of
integer points on \(u^2+v^2=h^2\), without using Euclid's parameterization.
The C++ self-test also injects positive synthetic `111` and `211` examples.
AddressSanitizer and UndefinedBehaviorSanitizer passed the self-test and a
scan through `H = 5000`.

Reproduce the main run with:

```sh
clang++ -O3 -std=c++20 -Wall -Wextra -pedantic \
  rational_relation_search.cpp -o /tmp/rational_relation_search
/tmp/rational_relation_search --self-test
python3 -m unittest -v test_rational_relation_search.py
/tmp/rational_relation_search 1000000 1
# The same exact scan may use, for example, 12 worker threads:
/tmp/rational_relation_search 1000000 12
# Reproduce the larger recorded run (approximately 8 h 42 min on `dev`):
/tmp/rational_relation_search 5500000 4
```

A positive event may be detected through more than one pair identity, so the
event counters are not equivalence-class counts.  A zero count is
unambiguous.

## 7. Audit notes on the 2026 hourglass preprint

Valentyn Voronsbekher,
[Magic hourglasses of squares have no centre of prime-power or semiprime
type](https://doi.org/10.5281/zenodo.21910218), proves the `p^alpha` and
squarefree `pq` exclusions.

The prime-power proof is sound: the primitive representations have distinct
`p`-adic valuations, so a signed three-term sum has a unique term of minimum
valuation.

The semiprime expansion and reduction to (23) are also sound.  Its printed
2-descent has four terse parity/divisibility steps: in each local obstruction
it explicitly forces three of the four homogenized variables to share a
prime but does not say that the other conic forces the fourth one to share it
too.  Those missing one-line implications are:

- `(1,2)`: even `u1,u3,v` make `u2` even in the first conic;
- `(5,2)`: even `u1,u2,v` make `u3` even in the second conic;
- `(-1,-2)`: divisibility of `u1,u3,v` by `5` makes `u2` divisible by `5`;
- `(-5,-2)`: divisibility of `u1,u2,v` by `5` makes `u3` divisible by `5`.

With those steps supplied, each case contradicts primitivity.  The resulting
curve is [LMFDB 80.a2](https://www.lmfdb.org/EllipticCurve/Q/80/a/2), whose
rank-zero and torsion data agree with the descent.  This repairs the terse
presentation; it does not turn an unrefereed preprint into an established
literature result.
