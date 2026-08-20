# Excluding a squarefree semiprime center

## Status

This note proves a second necessary condition for a hypothetical primitive
`3 x 3` magic square of nine pairwise distinct positive integer squares.  The
proof is elementary once the Gaussian representations are organized, but it
has not been peer reviewed and no novelty claim is made here.

A 13 August 2026 Zenodo preprint by Voronsbekher, discussed in
[literature-audit.md](literature-audit.md), independently proves the stronger
semiprime exclusion for the seven-cell magic hourglass.  The argument below
is therefore not a priority claim; it is a shorter full-square-specific
derivation and a base for the two-prime-power refinements later in the note.

## Theorem

The center root of such a square cannot be a product of two distinct primes.
Equivalently, if the center is \(e^2\), then

\[
e\ne pq
\]

for distinct primes \(p,q\).

By the primitive-center argument in [block-balance.md](block-balance.md), only
the case \(p\equiv q\equiv1\pmod4\) needs consideration.

## 1. The complete offset set for \(e=pq\)

Choose Gaussian primes \(p=\pi\bar\pi\) and \(q=\rho\bar\rho\).  Up to a
unit, every Gaussian integer of norm \(e^2=p^2q^2\) is obtained by assigning
the two copies of each split prime between it and its conjugate.  For either
rational prime there are three choices: both copies on one side, one on each
side, or both on the other side.

Write

\[
\pi^4=X+iY,
\qquad
\rho^4=U+iV.
\]

Neither coordinate is zero.  Set

\[
\frac{|X|}{p^2}=\cos\alpha,
\quad
\frac{|Y|}{p^2}=\sin\alpha,
\qquad
\frac{|U|}{q^2}=\cos\beta,
\quad
\frac{|V|}{q^2}=\sin\beta,
\]

with \(0<\alpha,\beta<\pi/2\).  Conjugation and the possible coordinate signs
do not affect the absolute imaginary parts.

For completeness, if \(\pi=a+ib\), then
\(\operatorname{Im}(\pi^4)=4ab(a^2-b^2)\ne0\) for the odd prime
\(p=a^2+b^2\).  A zero real part would give
\((a^2-b^2)^2=4a^2b^2\), and hence the irrational ratio
\(a/b=1+\sqrt2\) or one of its signed reciprocals.  The same argument applies
to \(\rho^4\).

If both rational primes are split evenly, the Gaussian integer is an
associate of \(pq\) and gives offset zero.  If only \(p\) is split evenly, or
only \(q\) is split evenly, the normalized positive offset is respectively

\[
\sin\beta
\quad\text{or}\quad
\sin\alpha.
\]

If both primes are assigned extremely, the two possible normalized positive
offsets are

\[
\sin(\alpha+\beta)
\quad\text{and}\quad
|\sin(\alpha-\beta)|.
\]

More explicitly, the local allocation indices are
\((j,h)\in\{-1,0,1\}^2\).  Modulo simultaneous conjugation
\((j,h)\sim(-j,-h)\), their nonzero-offset orbits are represented by
\((1,0),(0,1),(1,1),(1,-1)\); \((0,0)\) gives offset zero.  This proves that
the displayed list is complete.

Thus, after division by \(e^2\), every positive opposite-pair offset belongs
to the four-element set

\[
S=\{A,B,C,D\}
 =\{\sin\alpha,\sin\beta,
      \sin(\alpha+\beta),|\sin(\alpha-\beta)|\}.
\tag{1}
\]

A square with distinct entries needs four distinct positive offsets, so all
four values in (1) would have to occur and have the additive form

\[
\{a,b,a+b,|a-b|\}.
\tag{2}
\]

## 2. A trigonometric obstruction

Interchange \(p,q\) if necessary and assume

\[
0<\beta<\alpha<\frac\pi2.
\]

Equality of the angles would make \(D=0\), which is already incompatible with
four positive offsets.  The following strict comparisons and identities will
be used repeatedly:

\[
A>B,
\qquad C>D,
\qquad D>A-B,
\tag{3}
\]

and

\[
C+D=2A\cos\beta,
\qquad
C-D=2B\cos\alpha.
\tag{4}
\]

The first two claims are immediate.  For the third,

\[
D=2\sin\frac{\alpha-\beta}{2}
       \cos\frac{\alpha-\beta}{2}
  >2\sin\frac{\alpha-\beta}{2}
       \cos\frac{\alpha+\beta}{2}
  =A-B.
\]

In (2), choose which two members of \(S\) are the corner offsets \(a,b\);
the complementary pair must then be their sum and absolute difference.  The
six possibilities are all impossible:

1. If \(A,B\) are the corners, then \(C=A+B\), but
   \(\sin(\alpha+\beta)<\sin\alpha+\sin\beta\).
2. If \(C,D\) are the corners, ordering forces \(A=C+D\) and \(B=C-D\).
   Equations (4) then give \(\cos\beta=\cos\alpha=1/2\), hence
   \(\alpha=\beta\), a contradiction.
3. If \(A,C\) are the corners, neither \(B\le A\) nor \(D<C\) can be their
   sum.
4. If \(A,D\) are the corners, \(B\le A\) cannot be their sum, so
   \(C=A+D\) and \(B=A-D\).  The latter equality contradicts \(D>A-B\).
5. If \(B,C\) are the corners, \(D<C\) cannot be their sum, so \(A=B+C\).
   It follows that \(A-B=C\), whereas (3) gives \(D>A-B=C>D\).
6. Suppose \(B,D\) are the corners.  If \(A=B+D\), then \(D=A-B\), again
   contradicting (3).  The only remaining ordering is
   \(C=B+D\) and \(A=|B-D|\).  From (4),
   \[
   B=C-D=2B\cos\alpha,
   \]
   so \(\alpha=\pi/3\).  For \(0<\beta<\pi/3\), however,
   \[
   |B-D|
   =\left|\sin\beta-\sin\left(\frac\pi3-\beta\right)\right|
   <\sin\frac\pi3=A.
   \]
   The last inequality is strict because the difference is strictly
   increasing from \(-\sin(\pi/3)\) to \(\sin(\pi/3)\) on the open interval.

No partition of \(S\) has the required form (2).  This contradiction proves
the theorem.

## 3. A partial extension to two prime-power blocks

The same obstruction covers a little more than the squarefree case.  Suppose

\[
e=p^kq^\ell
\]

has exactly two distinct prime divisors.  For each of \(p,q\), at least three
of the four offsets are local units by the valuation spectrum in
[block-balance.md](block-balance.md).  Their two unit sets have an intersection
of size at least two.  An offset in the intersection is extreme at both
primes.  Modulo simultaneous conjugation there are only two absolute
imaginary parts of this kind, corresponding to the two relative orientations.
Distinctness therefore makes the intersection have size exactly two.  It
also follows that each prime has exactly one nonunit offset and that the two
exceptional offsets are different.

Call the exceptional \(p\)-offset *balanced* if its local Gaussian index is
zero.  Equivalently, its valuation is at least \(2k\); a nonzero intermediate
index has valuation strictly between zero and \(2k\).  Define a balanced
exception at \(q\) analogously.

If both exceptional offsets were balanced, choose acute folded arguments

\[
\alpha=\operatorname{fold}(\arg\pi^{4k}),
\qquad
\beta=\operatorname{fold}(\arg\rho^{4\ell}).
\]

Here \(\operatorname{fold}(\arg Z)\) is the unique angle
\(\theta\in(0,\pi/2)\) for which

\[
\cos\theta=\frac{|\operatorname{Re}Z|}{|Z|},
\qquad
\sin\theta=\frac{|\operatorname{Im}Z|}{|Z|}.
\]

Neither coordinate of \(\pi^{4k}\) can vanish: otherwise
\((\pi/\bar\pi)^{4k}=1\) or \(-1\), making \(\pi/\bar\pi\) a root of unity in
\(\mathbb Q(i)\) and making \(\pi\) associate to \(\bar\pi\), which is
impossible for a split odd prime.  The same applies to \(\rho^{4\ell}\), so
the folded angles really are acute.

The \(p\)-exception, the \(q\)-exception, and the two common unit offsets,
after division by \(e^2\), would again be exactly

\[
\sin\beta,\quad \sin\alpha,\quad
\sin(\alpha+\beta),\quad |\sin(\alpha-\beta)|.
\]

The trigonometric obstruction above rules this out.  Consequently:

\[
\boxed{\text{For a two-prime-block center, at least one exceptional offset
has a nonzero intermediate local index.}}
\tag{5}
\]

The squarefree theorem is the special case \(k=\ell=1\), when zero is the
only non-extreme local index.

## 4. Cross-divisibility when the exceptions have the same type

There is another useful restriction on the cases left by (5).  Write

\[
\pi^{4k}=x+iy,\qquad \rho^{4\ell}=u+iv.
\]

The two offsets extreme at both blocks are

\[
|xv+yu|,\qquad |yu-xv|.
\]

If \(r=|xv|\) and \(s=|yu|\), their half-sum and half-difference are
\(\{r,s\}\).  Consequently, if the two exceptional offsets have the same
geometric type, then their values as an unordered pair are

\[
\{r,s\}
\quad\text{if both are corner offsets }a,b,
\]

or

\[
\{2r,2s\}
\quad\text{if both are edge offsets }a+b,|a-b|.
\]

Let \(j_p\) be the local index of the \(p\)-exception.  Its valuation is
\(2(k-|j_p|)>0\).  Since neither \(x\) nor \(y\) is divisible by \(p\), the
displayed formulas force

\[
p^{2(k-|j_p|)}\mid u\ \text{or}\ v.
\tag{6}
\]

Similarly,

\[
q^{2(\ell-|j_q|)}\mid x\ \text{or}\ y.
\tag{7}
\]

All four coordinates are nonzero and have absolute value strictly smaller
than the modulus of their Gaussian number.  For balanced exceptions, (6)
therefore gives \(p^{2k}<q^{2\ell}\), while (7) gives the reverse strict
inequality.  This is already a contradiction when the
two balanced exceptions have the same type; the trigonometric argument is
needed for the mixed corner/edge arrangements.

If \(p\equiv q\equiv5\pmod8\), the modulo-eight result in
[block-balance.md](block-balance.md) forces both exceptions to be corner
offsets.  Hence every remaining two-block case for such primes must satisfy
the reciprocal cross-divisibilities (6) and (7).

## Scope

The argument in this note does not by itself exclude every
\(p^kq^\ell\).  Once a nonzero intermediate index occurs, additional angles
replace one or both of the single-block sine values, and the six-part
obstruction no longer applies.  The later coupled-edge argument in
[two-block-exponent-one.md](two-block-exponent-one.md) now excludes all of
those two-block cases.
