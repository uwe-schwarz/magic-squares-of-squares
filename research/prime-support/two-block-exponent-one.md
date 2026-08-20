# Excluding every two-block center

## Status

This note strengthens the two-prime-block analysis in
[squarefree-semiprime.md](squarefree-semiprime.md).  Sections 1--6 first prove
that neither prime block can have a balanced exceptional offset.  Sections
7--10 then reduce the only surviving geometry to two coupled norm equations
and exclude it by a self-contained elliptic-curve descent.  Consequently a
primitive magic square cannot have a center root supported on exactly two
rational primes.  The note also gives an exact example showing why the older
cross-divisibility conditions alone could not reach that conclusion.  No
claim of novelty is made.

## Theorem

The center root of a primitive `3 x 3` magic square of nine pairwise distinct
positive integer squares cannot have exactly two prime blocks.  In other
words, there are no distinct rational primes \(p,q\) and positive integers
\(k,\ell\) for which

\[
e=p^kq^\ell,
\]

is the center root of such a square.

The proof first shows that neither block's unique exceptional offset can have
local index zero.  Thus a hypothetical example would have \(k,\ell\ge2\).
It then shows that both exceptions would have to be edges and uses the two
edge relations simultaneously to obtain the final contradiction.

For each center prime, call the unique offset which is not a local unit its
*exception*.  For the first stage of the proof, suppose that the
\(p\)-exception is balanced.  Sections 1--5 force the only possible
exception-type assignment under this assumption to be

\[
\boxed{\text{the balanced \(p\)-exception is an edge and the
\(q\)-exception is a corner.}}
\tag{1}
\]

Here the corners are \(a,b\), and the edges are \(a+b,|a-b|\).  Before its
final exclusion, this last assignment would have to satisfy

\[
p\equiv1\pmod8,
\qquad \ell\ge2,
\qquad P^2<3Q^2,
\qquad Q^2<2P^2,
\qquad P=p^k,\quad Q=q^\ell.
\tag{2}
\]

Section 6 excludes this last assignment.

## 1. The exact four local orbits

Assume from now on that the \(p\)-exception is balanced.  Choose Gaussian
primes

\[
p=\pi\bar\pi,
\qquad q=\rho\bar\rho,
\]

and put

\[
A=\pi^{4k}=x+iy,
\qquad B=\rho^{4\ell}=u+iv,
\qquad P=p^k,
\qquad Q=q^\ell.
\tag{3}
\]

The two offsets which are units at both primes come from the two relative
extreme orientations.  Their values are

\[
C_+=|xv+yu|,
\qquad C_-=|yu-xv|.
\tag{4}
\]

The assumed balanced \(p\)-exception has local index \(j_p=0\) and value

\[
E_p=P^2|v|.
\tag{5}
\]

The unit-set argument in
[squarefree-semiprime.md](squarefree-semiprime.md) shows that the two prime
exceptions are different, that these four offsets exhaust the square's four
offsets, and that the \(q\)-exception has a nonzero intermediate index.  The
last assertion follows from the earlier exclusion of two balanced exceptions.
In particular, \(\ell\ge2\).

All four coordinates in (3) are nonzero.  Moreover,

\[
\gcd(x,y)=\gcd(u,v)=1,
\qquad p\nmid y,
\tag{6}
\]

because \(A\) and \(B\) are pure powers of one Gaussian prime, with no factor
of its conjugate.  The real part of a fourth power of a Gaussian integer of
odd norm is odd, while its imaginary part is divisible by four.  Thus \(x,u\)
are odd.

## 2. A Fermat descent lemma

We use the following classical special case of Fermat's descent.

**Lemma.**  The equation

\[
X^2+Y^4=Z^4
\tag{7}
\]

has no solution in positive integers.

**Proof.**  Divide out \(d=\gcd(Y,Z)\); the equation implies \(d^2\mid X\),
so a hypothetical solution reduces to one in which \(X,Y,Z\) are pairwise
coprime.  Choose such a solution with \(Z\) minimal.  If neither \(X\) nor
\(Y\) is even, reduction modulo \(16\) is already impossible; the primitive
case therefore has exactly one of them even.

If \(X\) is even, the primitive Pythagorean triple
\((X,Y^2,Z^2)\) has a parametrization

\[
X=2rs,
\qquad Y^2=r^2-s^2,
\qquad Z^2=r^2+s^2
\]

with coprime \(r>s>0\).  It follows that

\[
(YZ)^2+s^4=r^4,
\]

which is another positive solution of (7), now with terminal variable
\(r<Z\).

If \(Y\) is even, then \(X\) and \(Z\) are odd, and the same primitive
triple has a parametrization

\[
X=r^2-s^2,
\qquad Y^2=2rs,
\qquad Z^2=r^2+s^2.
\]

The pair \((r,s,Z)\) is itself a primitive Pythagorean triple.  Name its
parameters so that its even leg is \(2mn\); then

\[
\{r,s\}=\{2mn,m^2-n^2\},
\qquad Z=m^2+n^2,
\]

where \(m>n>0\) are coprime.  Hence

\[
\left(\frac Y2\right)^2=mn(m^2-n^2).
\]

The three factors on the right are pairwise coprime, so each is a square:

\[
m=M^2,
\qquad n=N^2,
\qquad m^2-n^2=R^2.
\]

Therefore

\[
R^2+N^4=M^4
\]

is a new positive solution, with \(M<Z\).  The primitive parity alternatives
are exhausted by \(X\) even or \(Y\) even, so both cases contradict the
minimal choice of \(Z\).  This proves the lemma. \(\square\)

An immediate consequence used below is

\[
|u|=P^2
\quad\Longrightarrow\quad
v^2+P^4=Q^4,
\tag{8}
\]

which is impossible by the lemma.

## 3. Both exceptions cannot be corners

If both exceptions are corners, the common offsets \(C_+,C_-\) are the two
edges.  For any real numbers \(r,s\),

\[
\left\{\frac{|r+s|+|r-s|}{2},
\frac{\bigl||r+s|-|r-s|\bigr|}{2}\right\}
=\{|r|,|s|\}.
\]

Taking \(r=yu\) and \(s=xv\), the two corner values must therefore be

\[
\{|yu|,|xv|\}.
\tag{9}
\]

The value in (5) cannot equal \(|xv|\), because \(v\ne0\) and
\(|x|<P^2\).  Hence

\[
P^2|v|=|yu|.
\]

Since \(p\nmid y\), this implies \(P^2\mid u\).  A corner exception at \(q\)
gives the strong block bound

\[
Q^2<2P^2.
\]

As \(0<|u|<Q^2\), it follows that \(|u|=P^2\), contradicting (8).

## 4. A corner at \(p\) and an edge at \(q\) are impossible

Suppose the \(p\)-exception is a corner and the \(q\)-exception is an edge.
The three \(q\)-unit offsets omit an edge, so their additive relation has
coefficient type \(\{1,1,1\}\).  After aligning their extreme \(q\)-factors,
their residual squared Gaussian values are, up to independent signs,

\[
P^2,
\qquad A,
\qquad \bar A.
\]

The Gaussian divisibility argument from
[block-balance.md](block-balance.md) therefore gives

\[
\sigma_0P^2+\sigma_1A+\sigma_2\bar A
=n\bar B,
\qquad
\sigma_0,\sigma_1,\sigma_2\in\{\pm1\},
\quad n\in\mathbb Z\setminus\{0\}.
\tag{10}
\]

If \(\sigma_1=\sigma_2\), the left side is real, whereas the right side is
not.  Thus \(\sigma_1=-\sigma_2\), and the coordinates on the left side are

\[
(\sigma_0P^2,\,2\sigma_1y).
\]

Their gcd is one by (6) and the oddness of \(p\).  The coordinates of \(B\)
are also coprime, so (10) forces \(|n|=1\).  Comparing real coordinates now
gives \(|u|=P^2\), again contradicting (8).

## 5. Both exceptions cannot be edges

If both exceptions are edges, the common offsets \(C_+,C_-\) are the two
corners.  Their sum and absolute difference show that the edge values are

\[
\{2|yu|,2|xv|\}.
\tag{11}
\]

The value \(E_p=P^2|v|\) cannot equal \(2|xv|\), since cancellation would
give the parity-impossible equality \(P^2=2|x|\).  Therefore

\[
P^2|v|=2|yu|,
\]

and (6) gives \(P^2\mid u\).  An edge exception at \(q\) gives

\[
Q^2<3P^2.
\]

The nonzero coordinate \(|u|<Q^2\) is consequently either \(P^2\) or
\(2P^2\).  It is odd, so the second value is impossible.  Thus
\(|u|=P^2\), contradicting (8).

Sections 3--5 exclude every type assignment except (1).  An exceptional edge
at \(p\) can occur only for \(p\equiv1\pmod8\), and the two relevant relation
types give the bounds in (2).  It remains to exclude this last assignment.

## 6. The remaining mixed assignment

We first isolate the rational-point calculation needed below.

**Quartic lemma.**  If \(R,S\in\mathbb Z\) are nonzero, then

\[
R^4-3R^2S^2+4S^4
\tag{12}
\]

is not a square.

**Proof.**  A square in (12), after division by \(R^4\), would give a
nonzero rational point on

\[
w^2=4t^4-3t^2+1,
\qquad t=\frac SR.
\tag{13}
\]

For \(t\ne0\), set

\[
X=\frac{2(1-w)}{t^2},
\qquad
Y=\frac{t(X^2-16)}2.
\]

Direct substitution gives

\[
t^2=\frac{4(X-3)}{X^2-16},
\qquad
E:\quad Y^2=(X-3)(X-4)(X+4).
\tag{14}
\]

Conversely, away from \(X=3,4,-4\) and the point at infinity, (14) recovers
\(t=2Y/(X^2-16)\).  Thus this is a birational correspondence away from the
displayed exceptional points.

It remains to determine \(E(\mathbb Q)\).  Translate \(z=X-3\), giving

\[
E:\quad Y^2=z(z-1)(z+7).
\]

Away from the rational two-torsion, the Kummer map sends a point to the two
squareclasses represented by \((z,z-1)\).  Valuations at primes outside the
three root differences show that representatives may be chosen with

\[
b_1\in\{\pm1,\pm7\},
\qquad b_2\in\{\pm1,\pm2\}.
\]

The real signs leave eight pairs.  Four are represented by the point at
infinity and the three two-torsion points:

\[
(1,1),\quad(1,2),\quad(-7,-1),\quad(-7,-2).
\tag{15}
\]

For any other pair, take \(b_3\) to represent the squareclass \(b_1b_2\).
A rational point would give a primitive integral solution of

\[
b_1U^2-b_2V^2=T^2,
\qquad
b_3W^2-b_1U^2=7T^2.
\tag{16}
\]

The four remaining pairs are impossible:

- For \((7,1)\), the first equation is
  \(7U^2-V^2=T^2\).  Modulo \(7\), the nonresidue of \(-1\) forces
  \(7\mid V,T\), and then \(7\mid U\).  The second equation also forces
  \(7\mid W\), contradicting primitivity.
- For \((7,2)\), the first equation is
  \(7U^2-2V^2=T^2\).  The same argument uses the nonresidue
  \(-2\equiv5\pmod7\), after which the second equation again forces every
  variable to be divisible by seven.
- For \((-1,-1)\), equations (16) are
  \(-U^2+V^2=T^2\) and \(W^2+U^2=7T^2\).  The second equation modulo \(4\)
  forces \(W,U,T\) even, and the first then forces \(V\) even.
- For \((-1,-2)\), equations (16) are
  \(-U^2+2V^2=T^2\) and \(2W^2+U^2=7T^2\).  If \(V\) is odd, the first
  equation forces \(U,T\) odd, after which the second equation modulo \(8\)
  would give
  \(W^2\equiv3\pmod4\).  If \(V\) is even, the first equation forces
  \(U,T\) even and the second forces \(W\) even.

Thus the Kummer image consists only of (15), so \(E(\mathbb Q)\) has rank
zero.  In the short model \(y^2=x^3-19x+30\), direct counting gives four
points over both \(\mathbb F_3\) and \(\mathbb F_5\).  Both primes are of
good reduction.  Prime-to-\(3\) torsion injects into the first group and
prime-to-\(5\) torsion into the second; since both groups have order four,
the rational torsion has order at most four.  Hence \(E(\mathbb Q)\) consists
exactly of the point at infinity and the three rational two-torsion points
represented in (15).  In the original \(X\)-coordinate these are
\(O,(3,0),(4,0),(-4,0)\).  Formula (14) gives \(t=0\) at \((3,0)\), the
other \(t=0\) branch at \(O\), and the two points at infinity of the quartic
at \((\pm4,0)\).  Thus (13) has no nonzero rational point, proving the
quartic lemma. \(\square\)

Now assume the remaining assignment (1).  Since the \(q\)-exception is a
corner, its three \(q\)-unit offsets have coefficient type \(\{2,1,1\}\),
with the other corner as the doubled term.  After aligning their extreme
\(q\)-factors, their local \(p\)-indices are \(0,+k,-k\).  Indeed, the two
common offsets are the two relative-orientation orbits for blocks which are
extreme at both primes.  Independently conjugating their encodings to make
the \(q\)-index \(+\ell\) leaves the two \(p\)-indices \(+k,-k\), while the
balanced index remains zero.  Put

\[
T_0=\pi^{2k}=r+is.
\]

The three residual squared Gaussian values are therefore
\(T_0\bar T_0=P^2\), \(T_0^2=A\), and
\(\bar T_0^2=\bar A\).  The doubled term is one of the last two; interchange
\(T_0\) and \(\bar T_0\) if necessary.  Orient the three offsets so that
their squared encodings have the common extreme \(q\)-factor \(B\), and
absorb the projection signs and the signs in the additive relation.  This
defines

\[
H=\epsilon_0T_0\bar T_0+\epsilon_1T_0^2
  +2\epsilon_2\bar T_0^2,
\qquad
\epsilon_j\in\{\pm1\}.
\]

The signed offset relation is exactly
\(\operatorname{Im}(BH)=0\).  Since all three residual squares are
congruent to \(1\) modulo \(2\mathbb Z[i]\), the coefficient pattern gives
\(H\in2\mathbb Z[i]\).  Put \(J=H/2\).  The standard distinct-offset
argument for a \(\{2,1,1\}\) relation gives \(J\ne0\).  Since \(BJ\) is a
rational integer, equality of its \(\rho\)- and \(\bar\rho\)-valuations
gives \(\bar B\mid J\).  Write \(J=\bar B\gamma\) with
\(\gamma\in\mathbb Z[i]\).  Then
\(BJ=Q^4\gamma\in\mathbb Z\), so
\(\gamma\in\mathbb Z[i]\cap\mathbb Q=\mathbb Z\).  Therefore

\[
J=n\bar B,
\qquad
H=2n\bar B,
\qquad n\in\mathbb Z\setminus\{0\}.
\tag{17}
\]

Neither coordinate of \(T_0\) vanishes, since otherwise
\((\pi/\bar\pi)^{2k}=\pm1\).  A common rational divisor of \(r,s\) would
contribute both conjugate Gaussian prime factors to the pure power
\(\pi^{2k}\), so \(\gcd(r,s)=1\).  Finally, writing
\(\pi^k=a+ib\), its coordinates have opposite parity and
\[
r=a^2-b^2,\qquad s=2ab.
\]
Thus

\[
r,s\ne0,
\quad \gcd(r,s)=1,
\quad r\text{ is odd},
\quad4\mid s,
\quad r^2+s^2=P^2.
\tag{18}
\]

No sign convention is imposed on \(r\) or \(s\).  Because the coordinates of
\(B\) are coprime,

\[
|n|=\gcd(|\operatorname{Re}J|,|\operatorname{Im}J|).
\tag{19}
\]

Multiplying the defining expression for \(H\) by a global sign lets us take
\(\epsilon_1=1\).  Thus the eight original sign triples, paired under
simultaneous sign change, give exactly these four possibilities:

\[
\begin{array}{c|c|c}
\epsilon_0&\epsilon_2&J\\ \hline
+1&+1&(2r^2-s^2)-irs\\
-1&+1&(r^2-2s^2)-irs\\
+1&-1&s^2+3irs\\
-1&-1&r(-r+3is).
\end{array}
\]

If \(\epsilon_2=1\), direct expansion gives

\[
J=
\begin{cases}
(2r^2-s^2)-irs,&\epsilon_0=1,\\
(r^2-2s^2)-irs,&\epsilon_0=-1.
\end{cases}
\tag{20}
\]

In the first line the coordinate gcd is exactly two: an odd common divisor
would contradict \(\gcd(r,s)=1\), and \(2r^2-s^2\) has 2-adic valuation one.
Thus \(|n|=2\).  Writing \(s=2s_0\) and taking norms in (17) gives

\[
Q^4=r^4-3r^2s_0^2+4s_0^4,
\]

contrary to the quartic lemma.  In the second line of (20) the coordinate gcd
is one, so \(|n|=1\), and taking norms gives

\[
Q^4=r^4-3r^2s^2+4s^4,
\]

the same contradiction.

Suppose instead that \(\epsilon_2=-1\).  If \(\epsilon_0=1\), then

\[
J=\frac{(T_0-\bar T_0)(T_0+2\bar T_0)}2
  =s^2+3irs.
\tag{21}
\]

Its coordinate gcd is \(|s|\gcd(|s|,3)\).  Dividing by that gcd leaves an
even real coordinate and an odd imaginary coordinate.  This cannot equal
\(\pm B\) or \(\pm\bar B\), because a Gaussian fourth power of odd norm has
odd real coordinate and imaginary coordinate divisible by four.

Finally, if \(\epsilon_0=-1\), then

\[
J=\frac{(T_0+\bar T_0)(T_0-2\bar T_0)}2
  =r(-r+3is).
\tag{22}
\]

Equation (19) gives

\[
|n|=|r|\gcd(|r|,3).
\]

The strict \(\{2,1,1\}\) relation bound and (2) give

\[
|n|Q^2=|J|<2P^2<6Q^2,
\]

so \(|n|<6\).  If \(3\mid r\), the displayed gcd is at least nine.
Otherwise \(|r|\) is one or five.  The identity in (18) gives

\[
(P-|s|)(P+|s|)=r^2.
\]

For \(|r|=1\), both positive factors would be one, contrary to \(s\ne0\).
For \(|r|=5\), the only nonzero-\(s\) factorization is
\((P-|s|,P+|s|)=(1,25)\).  Hence \(P=13\) and \(|s|=12\).  Dividing
(22) by \(n\) would then give

\[
Q^4=5^2+(3\cdot12)^2=1321,
\]

but \(6^4<1321<7^4\).  This final contradiction excludes (1).  Thus a
\(p\)-exception cannot be balanced; interchanging \(p\) and \(q\) proves this
first-stage claim for both blocks.

## 7. The larger block and the modulo-eight corollary

Suppose

\[
e=p^kq^\ell,
\qquad P=p^k,\quad Q=q^\ell.
\]

The two coprime prime powers \(P,Q>1\) are unequal.  If \(P>Q\), the
\(p\)-block is strictly dominant.  Section 9 of
[block-balance.md](block-balance.md) proves that a dominant block cannot have
a corner exception; its exception must therefore be an edge.  Section 10
there then forces \(p\equiv1\pmod8\), and the dominant-index bound also gives
\(k\ge3\).

The smaller block cannot have a corner exception either.  Indeed, suppose
the \(q\)-exception is a corner and put \(g=\ell-|j_q|\ge1\).  The exact
corner quotient valuation from Section 9 of
[block-balance.md](block-balance.md) gives

\[
q^{4g}\mid\nu
\]

for its coefficient-\(\{2,1,1\}\) quotient.  Its strict height estimate and
the dominant \(p\)-block estimate give

\[
|\nu|Q^2<2P^2<6Q^2.
\]

This would imply \(q^{4g}<6\), impossible.  Hence both exceptions are edges,
so also \(q\equiv1\pmod8\).  Symmetrically the same conclusions hold with
\(p,q\) interchanged when \(Q>P\).  In particular,

\[
\boxed{\text{Both center primes are \(1\) modulo \(8\), and both
exceptions are edges.}}
\tag{23}
\]

## 8. Why the older cross-divisibility conditions did not suffice

Before the dominant-corner exclusion, the height bounds and reciprocal
cross-divisibilities were compatible even for two primes congruent to \(5\)
modulo \(8\).  An exact example is

\[
p=5,
\quad k=741,
\qquad q=13,
\quad \ell=465.
\tag{24}
\]

Put \(P=5^{741}\) and \(Q=13^{465}\).  Exact integer comparison gives

\[
P^2<2Q^2,
\qquad Q^2<2P^2,
\]

and \(P/Q\) is approximately
\(0.8976652024769772591973323669607549\).  With
\(\pi=1+2i\) and \(\rho=2+3i\), modular exponentiation gives

\[
\rho^{4\ell}\equiv76+75i\pmod{5^3},
\]

so \(v_5(\operatorname{Im}\rho^{4\ell})=2\), and

\[
\pi^{4k}\equiv508+1183i\pmod{13^3},
\qquad 1183=7\cdot13^2,
\]

so \(v_{13}(\operatorname{Im}\pi^{4k})=2\).  These are exactly the reciprocal
cross-valuations for intermediate indices

\[
|j_p|=740,
\qquad |j_q|=464.
\]

This is not a magic-square configuration and is not claimed to satisfy the
four exact additive offset equations.  It is an exact counterexample only to
the older idea that the strict \(\sqrt2\) block bounds, the modulo-eight
exception types, and cross-divisibilities by themselves are contradictory.
It is excluded by the newer dominant-edge result: here \(Q>P\), so the
\(13\)-block is dominant, while \(13\equiv5\pmod8\).  Thus the example is not
an obstacle to (23).

## 9. Exact normal form when both exceptions are edges

There is a sharper residue condition in the surviving two-block geometry.
Assume \(P=p^k>Q=q^\ell\) and that the smaller \(q\)-block also has an edge
exception.  Let \(j_p,j_q\) be the two intermediate local indices and put

\[
h=k-|j_p|,\qquad g=\ell-|j_q|.
\]

Choose \(q=\rho\bar\rho\) and write

\[
S=\rho^{2\ell}=r+is,\qquad
r^2+s^2=Q^2,
\qquad \gcd(r,s)=1,
\qquad r\ \text{odd},\quad4\mid s.
\tag{25}
\]

The two offsets which are units at both primes are the two corners.  After
aligning their common extreme \(p\)-factor, their residual squares are
signed copies of \(S^2\) and \(\bar S^2\).  Apply the notation \(U,V,W,n\)
from Section 9 of [block-balance.md](block-balance.md) to the dominant
\(p\)-exception.

If the two residual signs agree, then, up to units and overall signs,

\[
U=S^2+\bar S^2=2(r^2-s^2),\qquad
V=S^2-\bar S^2=4irs.
\]

The exact valuation \(v_p(U)=2h\) and
\(\gcd(r-s,r+s)=1\) show that exactly one of \(r-s,r+s\) is divisible by
\(p^{2h}\).  With

\[
z=\frac{r\mathbin\pm s}{p^{2h}},
\qquad p\nmid z,
\]

the selected linear factor and its norm are

\[
W\sim z(1+i),\qquad n=N(W)=2z^2.
\tag{26}
\]

If the two residual signs are opposite, then instead

\[
U\sim S^2-\bar S^2=4irs,\qquad
V\sim S^2+\bar S^2=2(r^2-s^2).
\]

Exactly one of \(r,s\) contains the factor \(p^{2h}\).  Writing that
coordinate as \(p^{2h}z\), with \(p\nmid z\), gives

\[
W\sim2z,\qquad n=N(W)=4z^2.
\tag{27}
\]

Thus both sign branches make \(V\) axis-aligned.  If \(F\) denotes the
residual square of the \(q\)-exception, the dominant exact identity is

\[
F=V\mathbin\pm\bar\pi^{4k},
\tag{28}
\]

where, up to a sign and conjugation,

\[
F=q^{2g}\rho^{4|j_q|}.
\tag{29}
\]

Equations (25)--(29) are an exact normal form, not merely a valuation
condition.  They do not by themselves yield a contradiction: the two
possible axis values are \(4irs\) and \(2(r^2-s^2)\), respectively.

They do, however, sharpen the residue class of the dominant prime.  The
dominant specialization of the Legendre-symbol condition (31) in
[block-balance.md](block-balance.md) says

\[
\left(\frac np\right)=\left(\frac3p\right).
\]

In both (26) and (27), \(n\) is a square times \(2\) or \(4\).  Since the
dominant edge already forces \(p\equiv1\pmod8\), it follows that
\((n/p)=1\), hence \((3/p)=1\).  Quadratic reciprocity now gives

\[
\boxed{p\equiv1\pmod{24}.}
\tag{30}
\]

In fact the same calculation retains fourth-power information.  In the
residue field modulo \(\pi\), the edge norm equation gives

\[
\bar\pi^{4k}
\equiv
\pm\frac32\,Q^2\frac{W}{\bar W}.
\]

In branch (26), \(W/\bar W=\pm i\), while
\(p\mid r^2-s^2=\operatorname{Re}(\rho^{4\ell})\).  Since
\(\rho^{4\ell}\) is a fourth power and has norm \(Q^4\), its reduction is
\(\pm iQ^2\).  In branch (27), \(W/\bar W=\pm1\), while
\(p\mid2rs=\operatorname{Im}(\rho^{4\ell})\), so the reduction of
\(\rho^{4\ell}\) is \(\pm Q^2\).  Dividing the two fourth powers in either
branch proves the stronger condition

\[
\boxed{\text{\(3/2\) is a fourth-power residue modulo \(p\)}.}
\tag{31}
\]

The nondominant edge relation at \(q\) also has only finitely many quotient
branches.  Write its coefficient-\(\{1,1,1\}\) identity as

\[
H_q=\nu\bar\rho^{4\ell},
\qquad \nu\in\mathbb Z\setminus\{0\}.
\]

The same two sign branches, now with the roles of \(p,q\) interchanged, make
the associated small norm \(n_q\) equal to \(2z_q^2\) or \(4z_q^2\).
Repeating the edge norm calculation before (31) of
[block-balance.md](block-balance.md), but retaining the quotient \(\nu\),
gives

\[
\left(\frac{n_q}{q}\right)
=\left(\frac{3\nu}{q}\right).
\]

An edge exception forces \(q\equiv1\pmod8\), so the left side is one.
Moreover, \(\nu\) is odd and the two strict height bounds give

\[
|\nu|Q^2<3P^2<9Q^2.
\]

Consequently

\[
\boxed{|\nu|\in\{1,3,5,7\},
\qquad
\left(\frac{3\nu}{q}\right)=1.}
\tag{32}
\]

For \(|\nu|=1\) this also forces \(q\equiv1\pmod{24}\).  The other three
branches are not excluded here.  Keeping fourth powers in the symmetric
calculation sharpens their residue condition to

\[
\boxed{\text{\(3/(2\nu)\) is a fourth-power residue modulo \(q\)}.}
\tag{33}
\]

Indeed, modulo \(\rho\) the norm equation expresses
\(\bar\rho^{4\ell}\) as
\(\pm(3/(2\nu))P^2W_q/\bar W_q\), while the vanishing coordinate of the
fourth power \(\pi^{4k}\) shows that
\(\pm P^2W_q/\bar W_q\) is itself a fourth power.  Section 10 now uses the
two edge relations simultaneously and excludes all of these residual cases.

## 10. Coupling the two edge relations

We finish the proof of the theorem.  Assume \(P=p^k>Q=q^\ell\), so by
Section 7 both exceptions are intermediate edges.  Retain

\[
A=\pi^{4k},\qquad B=\rho^{4\ell},
\qquad |A|=P^2,\qquad |B|=Q^2.
\]

Let \(a,b\) be the two common corner offsets, and write their positively
oriented full squared encodings as

\[
Z_a=s_aAB,\qquad Z_b=s_bA\bar B,
\qquad s_a,s_b\in\{\pm1\}.
\]

These are the two relative extreme-orientation orbits.  Conjugating an
encoding reverses its projected imaginary part, and the rational sign records
that reversal.  Let \(C_p\) and \(C_q\) denote signed residual squares of the
\(p\)- and \(q\)-exceptions, respectively.  Thus
\[
|C_p|=P^2,\qquad |C_q|=Q^2.
\]

The signs in the two edge relations are coupled.  For example, suppose that
the \(p\)-exception is \(c=a+b\) and the \(q\)-exception is \(d=a-b\).
After aligning the extreme factors, write
\[
Z_c=s_cC_pB,\qquad Z_d=s_dAC_q.
\]
The relations \(d-a+b=0\) and \(c-a-b=0\), with \(Z_b\) conjugated in the
second one to align its \(q\)-factor, give
\[
s_dC_q-s_aB+s_b\bar B=n_p\bar A,
\qquad
s_cC_p-s_aA+s_b\bar A=n_q\bar B
\]
for nonzero rational integers \(n_p,n_q\).  After multiplying the two
residuals by inessential rational signs, both equations therefore have the
same sign \(\epsilon=-s_as_b\) between their conjugate pair.  If the two
exceptions are interchanged, the relations instead give the same sign
\(\epsilon=s_as_b\) in both equations.  Hence all assignments have the
simultaneous normal form

\[
\boxed{
C_q=B+\epsilon\bar B+\delta\bar A,\qquad
C_p=A+\epsilon\bar A+\nu\bar B,
}
\tag{34}
\]

where \(\epsilon,\delta\in\{\pm1\}\) and
\(\nu\in\mathbb Z\setminus\{0\}\).  The dominant quotient has
\(|\delta|=1\); \(\nu\) is the nondominant coefficient-\(\{1,1,1\}\)
quotient from Section 9.

There is a useful modulo-\(16\) reduction before taking norms.  If a rational
prime \(r\equiv1\pmod8\) splits as \(r=\sigma\bar\sigma\), choose the
associate of \(\sigma\) whose odd coordinate is real.  Its even coordinate
is divisible by four, so
\[
\sigma^2\equiv1\pmod{8\mathbb Z[i]}.
\]
Every local residual root has, up to conjugation, the form
\[
w=\eta r^{m-|j|}\sigma^{2|j|},
\qquad \eta\in\{\pm1,\pm i\},
\]
and consequently \(w\equiv\eta\pmod{8\mathbb Z[i]}\) and
\(w^2\equiv\pm1\pmod{16\mathbb Z[i]}\).  Section 7 gives
\(p,q\equiv1\pmod8\), so this applies to all three residual squares in the
\(q\)-unit relation.  Moreover \(\bar B\equiv1\pmod{16\mathbb Z[i]}\).
The second equation in (34) therefore shows
\[
\nu\equiv\pm1\ \text{or}\ \pm3\pmod{16}.
\]
The strict bound \(|\nu|<9\) from (32) sharpens this to

\[
\boxed{|\nu|\in\{1,3\}.}
\tag{35}
\]

Now use both norm equations in (34).  Put
\[
\lambda=\frac{P^2}{Q^2},\qquad T=\lambda^2>1,
\]
and select the common axis of \(A+\epsilon\bar A\) and
\(B+\epsilon\bar B\).  Explicitly, set
\[
u=\frac{\operatorname{Re}A}{P^2},\quad
v=\frac{\operatorname{Re}B}{Q^2}
\quad(\epsilon=1),
\]
and use the corresponding imaginary coordinates when \(\epsilon=-1\).
Put \(D=v^2\).  Neither coordinate of the pure power \(B\) vanishes, so
\(0<D<1\).

For the real-axis branch the two cross terms have signs \(\delta,\nu\).
For the imaginary-axis branch both signs reverse.  Thus, with
\(\kappa=1\) in the first branch and \(\kappa=-1\) in the second, put
\[
\delta_0=\kappa\delta,\qquad \nu_0=\kappa\nu,\qquad
\mu=\frac{\nu_0}{\delta_0}=\frac{\nu}{\delta}.
\]
The equations \(|C_q|=Q^2\) and \(|C_p|=P^2\) become
\[
\begin{aligned}
1&=T+4D+4\delta_0\lambda uv,\\
T&=\nu^2+4Tu^2+4\nu_0\lambda uv.
\end{aligned}
\tag{36}
\]

Eliminating the cross term gives
\[
4Tu^2=(\mu+1)(T-\mu)+4\mu D,
\qquad
16Tu^2D=(T+4D-1)^2.
\]
Eliminating \(u^2\) in turn yields the single exact identity
\[
\boxed{
(\mu-1)\bigl(16D^2+4(T-\mu-2)D\bigr)=(T-1)^2.
}
\tag{37}
\]

By (35), \(\mu\in\{\pm1,\pm3\}\).  If \(\mu=1\), (37) gives
\(T=1\), contrary to \(P>Q\).  If \(\mu<1\), then
\[
16D^2+4(T-\mu-2)D
=4D(4D+T-\mu-2)>0,
\]
so the two sides of (37) have opposite signs.  The only possibility is
\(\mu=3\), for which

\[
32D^2+8(T-5)D=(T-1)^2.
\tag{38}
\]

Regard (38) as a quadratic in the rational number \(T\).  Its discriminant
is
\[
64D(3D-2).
\]
Write \(D=s^2\), where \(s=v\), and let \(c\) be the other normalized
coordinate of \(B\).  Then \(s,c\in\mathbb Q\),
\(s^2+c^2=1\), and \(s,c\ne0\).  Since the discriminant is a rational
square, there is a \(w\in\mathbb Q\) such that
\[
w^2=3s^2-2.
\]
Parametrize the rational unit circle by
\[
s=\frac{1-t^2}{1+t^2},\qquad
c=\frac{2t}{1+t^2}.
\]
The nonvanishing of \(c\) makes \(t\) a finite nonzero rational number.
Substitution, followed by \(y=w(1+t^2)\), gives

\[
y^2=t^4-10t^2+1.
\tag{39}
\]

It remains to record the rational points of this quartic.  For \(t\ne0\),
put
\[
X=\frac{y+1}{t^2},\qquad Y=t(X^2-1).
\]
Direct substitution gives
\[
Y^2=2(X-5)(X-1)(X+1).
\]
The change of variables
\[
x=\frac{X-1}{2},\qquad y_E=\frac Y4
\]
gives the elliptic curve

\[
E:\qquad y_E^2=x(x-2)(x+1)=x^3-x^2-2x.
\tag{40}
\]

For completeness, a standard \(2\)-isogeny descent determines
\(E(\mathbb Q)\).  For a curve
\[
y^2=x^3+ax^2+bx,
\]
the descent squareclasses are represented by squarefree divisors \(b_1\) of
\(b\); occurrence of \(b_1\) requires a primitive solution of
\[
N^2=b_1R^4+aR^2S^2+\frac b{b_1}S^4.
\]
The \(2\)-isogenous curve is
\[
y^2=x^3-2ax^2+(a^2-4b)x.
\]

For (40), the first descent image has all four possible squareclasses
\[
\{1,-2,2,-1\},
\]
represented by the point at infinity and
\((0,0),(2,0),(-1,0)\).  The isogenous curve is
\[
E':\qquad y^2=x^3+2x^2+9x.
\]
Its possible classes are \(\{\pm1,\pm3\}\).  The two negative classes make
the displayed quartic form negative definite.  For \(b_1=3\), that form is
\[
N^2=3R^4+2R^2S^2+3S^4.
\]
Modulo three, a primitive solution would force \(3\mid R\) or \(3\mid S\);
then reduction modulo nine gives \(N^2\equiv3\pmod9\), impossible.  Hence
the second descent image is \(\{1\}\).  The \(2\)-isogeny rank formula gives
\[
2^{\operatorname{rank}E(\mathbb Q)}
=\frac{4\cdot1}{4}=1.
\]

Finally, direct counting gives
\(\#E(\mathbb F_5)=\#E(\mathbb F_7)=4\); both primes are of good reduction.
Reduction at these two primes bounds the rational torsion by four, and the
four displayed two-torsion points already attain that bound.  Therefore
\[
E(\mathbb Q)=\{O,(0,0),(2,0),(-1,0)\}.
\]
In the \(X\)-coordinate these finite points have \(X=1,5,-1\).  But the
quartic map also gives
\[
(X^2-1)t^2=2(X-5).
\]
The values \(X=\pm1\) are impossible, and \(X=5\) forces \(t=0\).  Thus
(39) has no rational point with \(t\ne0\), contradicting the construction
above.  The residual edge-edge case is impossible, and with Sections 1--7
this excludes every center root supported on exactly two rational primes.
\(\square\)
