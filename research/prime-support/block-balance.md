# Refined prime-power block balance

## Status

This note records a necessary condition for a hypothetical primitive
`3 x 3` magic square of nine pairwise distinct positive integer squares.  The
argument has been checked algebraically and by bounded exact enumeration, but
it has not been peer reviewed and no novelty claim is made here.

The result refines the initial bound

\[
p^k \le 2\frac{e}{p^k}
\]

to a strict bound with constant \(\sqrt 3\).  It also proves that a block
from a prime congruent to \(5\) modulo \(8\) is strictly smaller than its
complement.

## Theorem

Let a `3 x 3` magic square consist of nine pairwise distinct positive integer
squares.  Divide out the common gcd of their square roots, so that the roots
are globally primitive.  If the center is \(e^2\), and

\[
p^k\mathrel\Vert e,\qquad M=\frac{e}{p^k},
\]

then \(p\equiv1\pmod4\) and

\[
\boxed{p^{2k}<3M^2.}
\]

If \(p\equiv5\pmod8\), then in fact

\[
\boxed{p^k<M}
\]

holds.

More precisely, the \(\sqrt2\) bound holds unless exactly one of the four
offsets is a \(p\)-adic nonunit and that exceptional offset is one of the two
edge-pair offsets \(a+b\) or \(|a-b|\).  That exceptional case can occur only
when \(p\equiv1\pmod8\).

There is also a rigidity statement beyond the height bound.  If
\(p^k\ge M\), exactly one offset is a \(p\)-adic nonunit; it is necessarily
one of the two edge-pair offsets, and \(p\equiv1\pmod8\).  If its local index
is \(j\), then

\[
k\ge3,\qquad
\left\lfloor\frac{k}{2}\right\rfloor+1\le |j|\le k-1,\qquad
p^{2(k-|j|)}<\sqrt2\,M.
\]

In particular, neither a prime block, a squared-prime block, nor a balanced
exceptional representation can be dominant.

There is one further exclusion when the center has exactly three
prime-power blocks.  If

\[
e=PQR,\qquad P=p^k>QR,\qquad Q=q^\ell,\qquad R=r^m,
\]

then the two complementary blocks \(Q,R\) cannot both be extremal at all four
offsets.  Thus every surviving dominant three-block configuration has a
nonextremal local index in at least one complementary block.

Here \(p^k=M\) cannot occur, since \(p\nmid M\) while \(p^k>1\).  Thus every
use of the exact dominant identity below is justified whenever
\(p^k\ge M\).

## 1. Four offsets and their Gaussian encoding

Every `3 x 3` magic square with center \(e^2\) can be written as

\[
\begin{pmatrix}
e^2+x & e^2-x-y & e^2+y\\
e^2-x+y & e^2 & e^2+x-y\\
e^2-y & e^2+x+y & e^2-x
\end{pmatrix}.
\]

With \(a=|x|\) and \(b=|y|\), the four positive offsets of opposite pairs are

\[
\mathcal D=\{a,b,a+b,|a-b|\}.
\]

They are pairwise distinct because all nine entries are pairwise distinct.
For every \(d\in\mathcal D\), there are positive integers \(r,t\) with

\[
r^2=e^2+d,\qquad t^2=e^2-d.
\]

The roots \(r,t\) have the same parity.  Thus

\[
u=\frac{r+t}{2},\qquad v=\frac{r-t}{2}
\]

are integers and, for \(z=u+iv\in\mathbb Z[i]\),

\[
N(z)=u^2+v^2=e^2,\qquad d=2uv=|\operatorname{Im}(z^2)|.
\]

The sign of the imaginary part is immaterial because the offset is positive.

## 2. Prime divisors of a primitive center

If \(p\equiv3\pmod4\) divides \(e\), then

\[
u^2+v^2\equiv0\pmod p
\]

forces \(p\mid u,v\).  Hence \(p\mid r,t\) for every opposite pair, so \(p\)
divides all nine roots, contradicting primitivity.

If \(2\mid e\), then \(u^2+v^2=e^2\equiv0\pmod4\) forces both \(u,v\) even.
The same contradiction follows.  Therefore \(e\) is odd and every prime
divisor of \(e\) is congruent to \(1\) modulo \(4\).

## 3. Exact local valuation spectrum

Fix \(p^k\mathrel\Vert e\), choose \(p=\pi\bar\pi\) in \(\mathbb Z[i]\), and
write \(e=p^kM\).  Every \(z\) of norm \(e^2\) has the form

\[
z=\varepsilon\pi^{k+j}\bar\pi^{k-j}w,
\qquad -k\le j\le k,
\]

where \(\varepsilon\in\{\pm1,\pm i\}\), \(p\nmid N(w)\), and \(N(w)=M^2\).
For \(d=|\operatorname{Im}(z^2)|\),

\[
v_p(d)=
\begin{cases}
2(k-|j|),&j\ne0,\\
\ge2k,&j=0.
\end{cases}
\tag{1}
\]

For example, if \(j>0\),

\[
z=\varepsilon p^{k-j}\pi^{2j}w.
\]

After removing \(p^{2(k-j)}\) from \(\operatorname{Im}(z^2)\), the remaining
imaginary part is a \(p\)-adic unit.  Indeed,

\[
\operatorname{Im}(\pi^{4j}w^2)
=\frac{\pi^{4j}w^2-\bar\pi^{4j}\bar w^2}{2i}.
\]

Here \(2i\) is invertible modulo \(\pi\).  If the displayed integer were
divisible by \(p\), reduction of its numerator modulo \(\pi\) would give
\(-\bar\pi^{4j}\bar w^2\equiv0\pmod\pi\), impossible because
\(p\nmid N(w)\).  The case \(j<0\) follows by conjugation, and \(j=0\) is
immediate.  In particular,

\[
v_p(d)=0\quad\Longleftrightarrow\quad |j|=k.
\tag{2}
\]

## 4. At least three offsets are local units

For an odd prime \(p\), the minimum among

\[
v_p(a),\ v_p(b),\ v_p(a+b),\ v_p(a-b)
\]

occurs at least three times.  If \(v_p(a)\ne v_p(b)\), both \(a+b\) and
\(a-b\) have the smaller valuation.  If the valuations are equal, \(a+b\)
and \(a-b\) cannot both have a larger valuation, since \(2\) is invertible.

This common minimum is zero.  Otherwise (1) makes every offset divisible by
\(p^2\).  Since \(p^2\mid e^2\), all nine square entries would be divisible by
\(p^2\), so all roots would be divisible by \(p\).  Thus at least three
offsets are \(p\)-adic units, and their Gaussian exponents are extremal by
(2).

### Line-support corollary

The same statement has a useful geometric interpretation.  A center prime
\(p\) divides the square roots in at most one opposite pair.  If an offset
\(d\) is a \(p\)-unit, then

\[
r^2\equiv d\not\equiv0\pmod p,
\qquad
t^2\equiv-d\not\equiv0\pmod p,
\]

so neither paired root is divisible by \(p\).  If \(d\) is the unique
nonunit, its valuation is at least two, and both \(e^2+d\) and \(e^2-d\)
have roots divisible by \(p\).  Thus \(p\) divides either only the center
root, or exactly the center and the two roots on one complete line through
it.  A corner-offset exception \(a\) or \(b\) selects a diagonal; an
edge-offset exception \(a+b\) or \(|a-b|\) selects the central row or column.

## 5. Small additive relations

Every three-element subset of \(\mathcal D\) has a relation

\[
c_1d_1+c_2d_2+c_3d_3=0
\tag{3}
\]

of one of these two coefficient types:

| omitted offset | coefficient magnitudes |
| --- | --- |
| \(a+b\) or \(|a-b|\) | \(\{1,1,1\}\) |
| \(a\) or \(b\) | \(\{2,1,1\}\) |

Examples are \((a+b)-a-b=0\) and, for \(a>b\),
\((a+b)+(a-b)-2a=0\).

Choose a relation among three \(p\)-unit offsets.  Conjugate each associated
Gaussian integer independently when needed, so that

\[
z_s=\varepsilon_s\pi^{2k}w_s,\qquad N(w_s)=M^2.
\]

Set

\[
G_s=\varepsilon_s^2w_s^2,\qquad |G_s|=M^2,
\]

and let \(\eta_s\) be the sign of
\(\operatorname{Im}(\pi^{4k}G_s)\).  Absorb \(\eta_s\) into the coefficient
of (3).  With the resulting signed coefficients, still denoted \(c_s\),

\[
H=c_1G_1+c_2G_2+c_3G_3\in\mathbb Z[i]
\]

satisfies

\[
\operatorname{Im}(\pi^{4k}H)=0.
\tag{4}
\]

This explicit sign step is required; writing only the absolute imaginary
parts hides it.

## 6. Nonvanishing

The Gaussian integer \(H\) is nonzero.

For coefficient type \(\{1,1,1\}\), a zero sum would consist of three
nonzero complex vectors of the same length.  Their signed ratios would be
primitive cube roots of unity.  Such roots do not lie in \(\mathbb Q(i)\),
whereas all ratios of the \(G_s\) do.

For coefficient type \(\{2,1,1\}\), equality would force equality in the
triangle inequality.  The two shorter vectors would be equal and point
opposite the doubled vector.  Hence \(G_i=\pm G_j\) for some \(i\ne j\), which
would give equal absolute imaginary parts after multiplication by
\(\pi^{4k}\).  That contradicts distinctness of the offsets.

This is exactly where pairwise distinctness is essential.  Without it, the
primitive repeated-entry square

\[
\begin{pmatrix}
49&1&25\\1&25&49\\25&49&1
\end{pmatrix}
\]

has center root \(e=5\) and violates even the original constant-2 bound.

## 7. Height conclusion

Equation (4) and \(H\ne0\) imply

\[
\pi^{4k}H\in\mathbb Z\setminus\{0\}.
\]

A rational integer has equal \(\pi\)- and \(\bar\pi\)-valuations.  Therefore

\[
\bar\pi^{4k}\mid H.
\tag{5}
\]

For coefficient type \(\{1,1,1\}\),

\[
|H|\le3M^2.
\]

Equality would make all three signed summands co-directed, again forcing
two offsets to coincide.  Hence \(|H|<3M^2\).  Since a nonzero multiple of
\(\bar\pi^{4k}\) has modulus at least \(p^{2k}\), (5) gives

\[
p^{2k}<3M^2.
\tag{6}
\]

For coefficient type \(\{2,1,1\}\), use parity before estimating.  Because
\(M\) is odd, a Gaussian integer \(w=A+iB\) of norm \(M^2\) has coordinates
of opposite parity.  Thus

\[
w^2\equiv1\pmod{2\mathbb Z[i]},
\qquad G_s=\varepsilon_s^2w_s^2\equiv1\pmod{2\mathbb Z[i]}.
\]

The coefficient pattern makes \(H\in2\mathbb Z[i]\).  Put \(K=H/2\).  Then
\(K\ne0\), \(\operatorname{Im}(\pi^{4k}K)=0\), and
\(\bar\pi^{4k}\mid K\).  Moreover,

\[
|K|\le2M^2,
\]

again strictly by distinctness.  Therefore

\[
p^{2k}<2M^2.
\tag{7}
\]

Equations (6) and (7) prove the universal \(\sqrt3\) bound.

There is a little more arithmetic in the same conclusion.  Write

\[
H=\bar\pi^{4k}n
\]

in coefficient type \(\{1,1,1\}\).  Equation (4) shows that the quotient
\(n\) is not merely Gaussian but belongs to \(\mathbb Z\setminus\{0\}\).
Moreover, \(n\) is odd: modulo \(2\mathbb Z[i]\), all three \(G_s\) and
\(\bar\pi^{4k}\) are congruent to \(1\), while signs are immaterial.  In
coefficient type \(\{2,1,1\}\), write instead

\[
\frac H2=\bar\pi^{4k}n,
\qquad n\in\mathbb Z\setminus\{0\}.
\]

Consequently the integral versions of (6) and (7) are

\[
p^{2k}\le 3M^2-2
\quad\text{and}\quad
p^{2k}\le 2M^2-1,
\tag{8}
\]

respectively.  If the prime-power block is dominant, \(p^k>M\), the quotient
is forced to have absolute value one.  Thus the chosen relation satisfies the
exact identity

\[
H=\pm\bar\pi^{4k}
\quad\text{or}\quad
H=\pm2\bar\pi^{4k},
\tag{9}
\]

according to its coefficient type.  This rigidity does not by itself exclude
a dominant block, but it is stronger than the height inequality alone.

## 8. A dominant block has a unique exceptional offset

There is one consequence that uses all four offsets at once and is therefore
not visible in a single three-term relation.

**Proposition.**  If all four offsets are \(p\)-adic units, then

\[
p^k<M.
\tag{10}
\]

In particular, if \(p^k\ge M\), exactly three offsets are \(p\)-adic units and
the fourth is a \(p\)-adic nonunit.

To prove this, suppose first that all four offsets are units.  Write

\[
c=a+b,\qquad d=|a-b|,
\]

and interchange \(a,b\) if necessary so that \(d=a-b\).  Orient the four
extreme Gaussian encodings simultaneously: after the independent
conjugations used in Section 5, replace each \(G_x\) by \(F_x=\pm G_x\) so
that

\[
\operatorname{Im}(\pi^{4k}F_x)=x
\qquad(x\in\{a,b,c,d\}).
\tag{11}
\]

The two coefficient-\(\{1,1,1\}\) relations give

\[
H_1=F_c-F_a-F_b=\bar\pi^{4k}n_1,
\qquad
H_2=F_d-F_a+F_b=\bar\pi^{4k}n_2,
\tag{12}
\]

where \(n_1,n_2\) are nonzero odd integers.  The two remaining
three-offset relations have coefficient type \(\{2,1,1\}\), and their halved
Gaussian sums are

\[
K_3=\frac{F_c+F_d-2F_a}{2}
    =\frac{H_1+H_2}{2},
\qquad
K_4=\frac{F_c-F_d-2F_b}{2}
    =\frac{H_1-H_2}{2}.
\tag{13}
\]

Both \(K_3\) and \(K_4\) are nonzero by the distinct-offset nonvanishing
argument in Section 6.  Hence \(n_1\ne n_2\) and \(n_1\ne-n_2\), so the two
odd integers have different absolute values and

\[
\max(|n_1|,|n_2|)\ge3.
\]

Applying the strict coefficient-\(\{1,1,1\}\) estimate to the larger quotient
gives

\[
3p^{2k}\le p^{2k}\max(|n_1|,|n_2|)<3M^2,
\]

which proves (10).  Section 4 supplies at least three unit offsets, so the
last assertion follows.

This proposition is genuinely a four-offset statement.  An abstract exact
identity involving only one unit triple does not enforce the existence of
the omitted fourth opposite pair.

## 9. Divisibility forced by the exceptional offset

The unique-exception case has an additional two-sided divisibility that is
not part of the height argument.  This does not yet exclude the case, but it
gives a smaller exact identity on which a further descent would have to act.

Let the exceptional offset have local index \(j\), with \(|j|<k\), and put

\[
h=k-|j|\ge1.
\]

Conjugate its Gaussian encoding if necessary and change its sign so that its
oriented square is

\[
Y_0=p^{2h}\pi^{4|j|}G_0,\qquad N(G_0)=M^4,
\tag{14}
\]

and its imaginary part is the positive exceptional offset.  Continue to
write \(F_x\) for the positively oriented residual squares of the three unit
offsets.  Assuming \(a>b\), define \(U,V\) by the following table.

| exceptional offset | \(U\), whose projected imaginary part is exceptional | orthogonal partner \(V\) |
| --- | --- | --- |
| \(c=a+b\) | \(F_a+F_b\) | \(F_a-F_b\) |
| \(d=a-b\) | \(F_a-F_b\) | \(F_a+F_b\) |
| \(a\) | \((F_c+F_d)/2\) | \((F_c-F_d)/2\) |
| \(b\) | \((F_c-F_d)/2\) | \((F_c+F_d)/2\) |

The halves in the last two rows are Gaussian integers because every
\(F_x\equiv1\pmod{2\mathbb Z[i]}\).  In every row,

\[
R=Y_0-\pi^{4k}U\in\mathbb Z,
\tag{15}
\]

because its imaginary part is zero.  The two summands in (15) have respective
\(\pi\)-valuations

\[
2h+4|j|
\quad\text{and at least}\quad
4k,
\]

and the first is smaller.  Hence \(R\ne0\) and

\[
v_\pi(R)=2h+4|j|.
\tag{16}
\]

Since \(R\) is rational, it has the same \(\bar\pi\)-valuation.  Looking at
(15) at \(\bar\pi\), where \(Y_0\) has valuation \(2h\), therefore gives

\[
\bar\pi^{2h}\mid U.
\tag{17}
\]

In fact this valuation is exact.  The valuation of \(R\) is
\(2h+4|j|>2h\), so the two terms on the right of (15) must cancel at
valuation \(2h\).  Hence

\[
v_{\bar\pi}(U)=2h.
\]

The partner \(V\) is a \(\bar\pi\)-unit.  For example, if \(c\) is
exceptional, the exact unit relation says

\[
F_a-F_b=F_d-n\bar\pi^{4k}
\]

for an integer \(n\), so \(V\equiv F_d\not\equiv0\pmod{\bar\pi}\).
The other three rows follow from the other three relations in exactly the
same way.

The two residual squares used to form \(U,V\) have equal norm.  Consequently

\[
\operatorname{Re}(U\bar V)=0,
\]

so \(U/V\in i\mathbb Q\).  Write \(U/V=i r/s\) with coprime rational
integers \(r,s\).  Because \(V\) is a \(\bar\pi\)-unit, (17) says that
\(p^{2h}\mid r\).  A rational integer has the same \(\pi\)- and
\(\bar\pi\)-valuation, and therefore

\[
\boxed{p^{2h}\mid U\quad\text{in }\mathbb Z[i].}
\tag{18}
\]

There is a substantially stronger size consequence than the triangle bound
on \(U\).  Absorb the sign between its two residual squares into one square
root.  For an exceptional edge write

\[
U=x^2+y^2,
\]

and for an exceptional corner write

\[
2U=x^2+y^2,
\]

where \(N(x)=N(y)=M^2\).  Since \(p\) is odd, (18) makes
\(\pi^{2h}\) divide one of \(x+iy,x-iy\); the two factors are coprime at
\(\pi\) because \(x,y\) are local units.  Equal norms give the identities

\[
\overline{x+iy}=-iM^2\frac{x+iy}{xy},
\qquad
\overline{x-iy}= iM^2\frac{x-iy}{xy}.
\]

The multipliers are local units at \(p\).  Thus whichever linear factor is
divisible by \(\pi^{2h}\) is also divisible by \(\bar\pi^{2h}\), and hence by
the rational integer \(p^{2h}\).  Its modulus is strictly less than \(2M\):
equality in the triangle inequality would make \(x=\pm iy\), forcing
\(x^2+y^2=0\), whereas the exceptional offset is positive.  Moreover,
\(x\) and \(y\) are odd Gaussian integers, so \(x\pm iy\) is divisible by
\(1+i\).  This factor is coprime to \(p\).  Therefore

\[
\boxed{\sqrt2\,p^{2h}<2M,\quad\text{or equivalently}\quad
p^{2h}<\sqrt2\,M.}
\tag{19}
\]

In particular, a dominant block cannot have a balanced exceptional
representation.  If \(|j|=0\), then \(h=k\), while
\(p^k>M\) and (19) would give \(M^2<p^{2k}<2M\), impossible here
(the balance bound already forces \(M>1\), and \(M\) is odd).  Hence every
dominant exceptional index is genuinely intermediate.  Moreover, since
every center prime is at least \(5\), (19) and \(p^{h+|j|}>M\) imply
\[
|j|\ge h.
\]

Thus a dominant block necessarily has

\[
\boxed{
k\ge2,\qquad
\left\lceil\frac{k}{2}\right\rceil\le |j|\le k-1.
}
\tag{20}
\]

The midpoint allowed by (20) is also impossible.  Suppose
\(|j|=h\), so \(k=2h\) and \(p^{2h}=p^k\).  Denote this dominant block by
\(q=p^k\).  In the linear-factor argument above, let \(L=x\pm iy\) be the
factor divisible by \(q\).  It is also divisible by \(1+i\), while
\[
|L|<2M<2q.
\]
Consequently \(N(L/q)\) is a positive even integer less than \(4\), and
\[
L=\varepsilon q(1+i)
\tag{21}
\]
for a Gaussian unit \(\varepsilon\).

Replace \(y\) by \(-y\) if necessary so that \(L=x+iy\); this does not
change \(y^2\).  The equal-norm identity displayed above now gives
\[
xy=-iM^2\frac{L}{\bar L}=\pm M^2.
\]
After absorbing an inessential sign, \(y=\bar x\).  It follows that the
orthogonal partner \(V\) in the table is axis-aligned.  More explicitly, if
\(x=a+ib\), then (21) gives \(q=|a\pm b|\), while
\(M^2=a^2+b^2\).  Hence
\[
2|ab|=q^2-M^2
\quad\text{and}\quad
|x^2-y^2|=4|ab|=2(q^2-M^2).
\]
Put
\[
C=q^2-M^2>0,\qquad T=\bar\pi^{4k},\qquad |T|=q^2.
\]
For an exceptional edge, \(|V|=2C\); for an exceptional corner,
\(|V|=C\).  The exact unit-triple quotient has absolute value one because
\(q>M\), so the remaining residual square has the form \(V\pm T\) and
modulus \(M^2\).

In the edge case, projecting
\[
N(V\pm T)=M^4
\]
onto the axis of \(V\) says that the corresponding integer coordinate of
\(T\) has absolute value
\[
\frac{5q^2-3M^2}{4}.
\]
This is not an integer: \(q^2\equiv M^2\equiv1\pmod8\), so its numerator is
congruent to \(2\pmod8\).  In the corner case, the same norm calculation
says that the axis coordinate of \(T\) has absolute value \(q^2=|T|\).
It would make \(T\) real or purely imaginary.  That is impossible for
\(\bar\pi^{4k}\): otherwise \(\pi/\bar\pi\) would be a root of unity, making
the two Gaussian primes above the odd split prime \(p\) associates.

Thus \(|j|>h=k-|j|\).  Combining this with the preceding bounds gives the
sharper necessary condition

\[
\boxed{
k\ge3,\qquad
\left\lfloor\frac{k}{2}\right\rfloor+1\le |j|\le k-1.
}
\tag{22}
\]

Finally put \(U=p^{2h}U_0\).  Dividing (15) by
\(p^{2h}\pi^{4|j|}\) and using (16) yields the exact descended identity

\[
\boxed{
G_0-\pi^{4h}U_0=n_0\bar\pi^{4|j|},
\qquad n_0\in\mathbb Z\setminus\{0\}.
}
\tag{23}
\]

Thus the original exponent \(k=h+|j|\) splits into a rational divisibility
of \(U\) and a new pure Gaussian divisor of exponent \(|j|\).

There is an exact small-factor normal form for the same reduction.  In the
linear-factor argument leading to (19), both factors satisfy

\[
v_\pi(x\mathbin\pm iy)=v_{\bar\pi}(x\mathbin\pm iy),
\]

by the two displayed conjugation identities.  Their product is \(U\) in the
edge case and \(2U\) in the corner case.  Since
\(v_{\bar\pi}(U)=2h\), the factor selected there has valuation exactly
\(2h\) at both primes above \(p\), and the other factor is a \(p\)-unit.
After changing the sign of \(y\), write the selected factor as

\[
L=x+iy=p^{2h}W,
\qquad p\nmid N(W),
\qquad 1+i\mid W.
\tag{24}
\]

Put \(n=N(W)\).  Then \(n\) is a positive even integer, and the strict
triangle estimate together with dominance and (22) gives

\[
0<n<\frac{4M^2}{p^{4h}}<4p^{2(|j|-h)}.
\tag{25}
\]

The equal-norm conjugation identity gives
\(iy/W=\overline{x/W}\).  Hence there is a \(t\in\mathbb Q\) such that,
with \(P=p^{4h}\) and \(m=M^2\),

\[
x=W\left(\frac{p^{2h}}2+it\right),
\qquad
y=W\left(-t-i\frac{p^{2h}}2\right),
\qquad
m=n\left(\frac P4+t^2\right).
\tag{26}
\]

In particular,

\[
x^2-y^2=\frac{W^2}{n}(nP-2m).
\tag{27}
\]

Up to an overall sign, the partner \(V\) is the right side of (27) for an
edge exception and half that value for a corner exception.  The exact
unit-triple identity therefore becomes, with \(T=\bar\pi^{4k}\),

\[
\left|\frac{W^2}{n}(nP-2m)\mathbin\pm T\right|=m
\quad\text{(edge)},
\]

or

\[
\left|\frac{W^2}{2n}(nP-2m)\mathbin\pm T\right|=m
\quad\text{(corner)}.
\tag{28}
\]

The corner equation has a stronger form even without dominance.  Retain the
integer quotient \(\nu\ne0\) in the coefficient-\(\{2,1,1\}\) identity, so
that its last term is \(\nu T\), and put

\[
E=nP-2m,\qquad C=\operatorname{Re}(W^2\bar T)\in\mathbb Z.
\]

Squaring and multiplying by \(n\) gives

\[
n\left(m^2-\nu^2p^{4k}-\frac{E^2}{4}\right)=\pm\nu EC.
\tag{29}
\]

Here \(p\nmid C\).  Indeed,

\[
2C=W^2\bar T+\bar W^2T,
\]

and reduction modulo \(\pi\) kills the first term but not the second:
\(\bar W\) is a \(\pi\)-unit by (24), and
\(T=\bar\pi^{4k}\) is also a \(\pi\)-unit.  On the other hand,
\(E\) is a \(p\)-unit, and direct expansion of the left side of (29) is

\[
np^{4h}
\left(
nm-\frac{n^2}{4}p^{4h}-\nu^2p^{4(k-h)}
\right).
\]

It follows first that \(v_p(\nu)\ge4h\).  With this information, the
parenthesized factor is congruent to \(nm\not\equiv0\pmod p\).  Hence every
corner exception satisfies the exact quotient valuation

\[
\boxed{v_p(\nu)=4h.}
\]

For a dominant block, Section 7 gives \(|\nu|=1\), which contradicts this
valuation.  Therefore

\[
\boxed{\text{a dominant prime-power block cannot have a corner exception}.}
\tag{30}
\]

The surviving edge case also has an exact quotient restriction.  Retain its
integer coefficient-\(\{1,1,1\}\) quotient \(\nu\).  Squaring gives

\[
n\bigl(m^2-\nu^2p^{4k}-E^2\bigr)=\pm2\nu EC.
\]

Modulo \(p\), the left side is \(-3nm^2\), a unit.  Hence \(p\nmid\nu\),
and

\[
C\equiv\pm\frac{3}{4\nu}\,nm\pmod p.
\]

On the other hand, reduction of
\(2C=W^2\bar T+\bar W^2T\) modulo \(\pi\) gives
\(2C\equiv\bar W^2T\).  The right side is a square in the residue field:
\(T=\bar\pi^{4k}\) is a fourth power.  Since an edge exception forces
\(p\equiv1\pmod8\), the numbers \(2,-1\), and \(m=M^2\) are also quadratic
residues.  Therefore

\[
\boxed{p\nmid\nu,\qquad
\left(\frac np\right)=\left(\frac{3\nu}{p}\right).}
\tag{31}
\]

For a dominant block \(\nu=\pm1\), and the second formula reduces to
\(\left(\frac np\right)=\left(\frac3p\right)\).

### Content of the selected linear factor

The norm `n` in the edge case has a more precise squareclass.  Retain the
two equal-norm residual roots `x,y` used in (24), and put

\[
 x\bar y=A+iB,\qquad \delta=\gcd(A,B)>0,\qquad
 a=\frac A\delta,\quad b=\frac B\delta,
 \quad c=\frac{M^2}{\delta}.
\]

Then \(A^2+B^2=M^4\), so \((a,b,c)\) is a primitive Pythagorean
triple.  The axis-degenerate case would make the two corner residual squares
equal up to sign and repeat an absolute offset, so `a,b` are nonzero.

Depending on the absorbed square signs and on which linear factor was
selected in (24), that factor is associated to one of
\(x\mathbin\pm y,x\mathbin\pm iy\).  Directly,

\[
 N(x\mathbin\pm y)=2\delta(c\mathbin\pm a),\qquad
 N(x\mathbin\pm iy)=2\delta(c\mathbin\pm b).        \tag{32}
\]

For a primitive Pythagorean triple, `c` plus or minus its even leg is a
square, while `c` plus or minus its odd leg is twice a square.  Hence every
nonzero selected factor has norm \(2\delta s^2\) or
\(4\delta s^2\) for an integer `s`.

Equation (24) is the exact division \(L=p^{2h}W\), with
\(p\nmid N(W)\).  Also \(p\nmid2\delta\), because `p` is odd and
\(N(x\bar y)=M^4\) is a `p`-unit.  Taking norms therefore forces
\(p^{2h}\mid s\).  Therefore, for some nonzero integer `z`,

\[
 \boxed{n=N(W)=2\delta z^2\quad\text{or}\quad4\delta z^2.}       \tag{33}
\]

The squareclass of \(\delta\) is read directly from the two corner indices.
For \(q^\ell\mathrel\Vert M\), let \(j_a,j_b\) be their local indices after
the orientations used above.  The two valuations of \(x\bar y\) at the
Gaussian primes above `q` are

\[
 2\ell+j_a-j_b,\qquad 2\ell-j_a+j_b.
\]

A rational power of `q` divides both Cartesian coordinates exactly when it
divides \(x\bar y\) at both Gaussian primes.  Consequently

\[
 \boxed{v_q(\delta)=2\ell-|j_a-j_b|.}               \tag{34}
\]

If the two corners are both `q`-extreme, the right side is even.  It is odd
exactly when a corner is the unique `q`-exception and its index gap
\(\ell-|j_q|\) is odd.  Thus, modulo rational squares, \(\delta\) is the
product of precisely those complement primes having such a corner exception.

For a dominant edge exception, \(p\equiv1\pmod8\), so `2` and `-1` are
quadratic residues modulo `p`.  Combining (31), \(|\nu|=1\), and (33) gives
the additional necessary condition

\[
 \boxed{\left(\frac{\delta}{p}\right)
       =\left(\frac3p\right).}                     \tag{35}
\]

The same parity analysis gives the additional dichotomy

\[
4\mid n
\quad\text{or}\quad
n\equiv2\pmod8.
\tag{36}
\]

To see this, if \(v_2(n)=1\), then \(L=x+iy\) has exactly one factor
\(1+i\).  The odd Gaussian integers \(x,y\) consequently have the same
parity orientation, so \(x^2-y^2\in8\mathbb Z[i]\).  Taking norms in (27)
gives \(8\mid E\); writing \(n=2r\) then gives \(r\equiv1\pmod4\).
The other possibility is \(v_2(n)\ge2\).

Thus every remaining dominant exception is an edge and has a Gaussian
direction \(W^2/n\)
whose even norm is bounded solely in terms of the index gap
\(|j|-h\).  This is a genuine reduction, but not yet a closed descent: no
argument above proves that \(U_0\) retains the equal-norm square structure of
the original three encodings, and the edge equation in (28) has not been
shown impossible for all admissible \(n\).

## 10. The modulo-8 refinement

If all four offsets are \(p\)-units, choose a triple of coefficient type
\(\{2,1,1\}\) and apply (7).  If exactly three are units and the exception is
\(a\) or \(b\), the unique unit triple again has type \(\{2,1,1\}\).

It remains to understand an exceptional edge offset.  Every \(p\)-unit offset
is a nonzero quadratic residue modulo \(p\), since
\(e^2+d=r^2\) gives \(d\equiv r^2\pmod p\).  If \(p\mid a+b\), then
\(b\equiv-a\pmod p\), and the other edge offset is congruent to
\(\pm2a\).  If \(p\mid|a-b|\), then \(b\equiv a\pmod p\), and
\(a+b\equiv2a\pmod p\).  In either case \(2\) is a quadratic residue modulo
\(p\), using also that \(-1\) is a residue because \(p\equiv1\pmod4\).
Consequently \(p\equiv1\pmod8\).

Thus a prime \(p\equiv5\pmod8\) always falls under (7).  More strongly, if
\(p^k\ge M\), Proposition (10) would force a unique exceptional offset.
It cannot be an edge by the preceding quadratic-residue argument and cannot
be a corner by (30).  Therefore \(p^k<M\), proving the stronger assertion in
the theorem.

## 11. A dominant three-block center needs a nonextremal complement

Suppose now that the center has exactly three prime-power blocks,

\[
 e=PQR,\qquad P=p^k>QR,\qquad Q=q^\ell,\qquad R=r^m,              \tag{37}
\]

for distinct odd split primes \(p,q,r\).  Assume for contradiction that the
\(q\)- and \(r\)-indices are extremal at all four offsets.  The preceding
sections show that the unique \(p\)-exception is an edge.  The other three
offsets therefore give a coefficient-\(111\) identity, and dominance makes
its quotient exact as in (9).

Choose Gaussian primes with

\[
 N(\rho)=q,\qquad N(\sigma)=r,\qquad N(\pi)=p,
\]

and put \(x=\rho^\ell\), \(y=\sigma^m\), and
\(z=\bar\pi^k\).  Thus

\[
 N(x)=Q,\qquad N(y)=R,\qquad N(z)=P.
\]

Across the retained three offsets, neither complementary orientation row can
be constant.  Otherwise the two columns in the majority orientation of the
other row would have the same residual fourth power up to sign, and hence the
same absolute projected offset, contrary to distinctness.  Each row therefore
has a unique minority column.

First suppose that the two minority columns coincide.  Up to conjugation,
the three residual fourth powers are
\(\mathcal A,\mathcal A,\bar{\mathcal A}\), where
\(\mathcal A=(xy)^4=U+iV\).  Normalize the sign of the exact identity so that
its right side is \(z^4\).  Every odd Gaussian fourth power is \(1\) modulo
\(8\), so the three effective signs have sum \(1\): exactly two are positive
and one is negative.  If a repeated term is negative, the two copies cancel
and \(z^4=\bar{\mathcal A}\), forcing \(P=QR\).  If the conjugate term is
negative, then

\[
 z^4=2\mathcal A-\bar{\mathcal A}=U+3iV.
\]

The one-sided Gaussian support makes both \(U,V\) nonzero.  Taking norms
would make both

\[
 U^2+V^2=(QR)^4,
 \qquad
 U^2+9V^2=P^4
\]

integer squares.  This contradicts the simultaneous-square obstruction
proved in Section 4 of [hourglass-sunit.md](hourglass-sunit.md).

It remains to treat distinct minority columns.  Relabel the three retained
offsets so that their residual roots are

\[
 a=xy,\qquad c=\bar x y,\qquad b=x\bar y.
\]

After absorbing the projection signs, the exact dominant identity is

\[
 z^4=\eta_0a^4+\eta_qc^4+\eta_rb^4,
 \qquad \eta_0,\eta_q,\eta_r\in\{1,-1\},          \tag{38}
\]

with exactly one negative sign.  Put

\[
 \mathcal C=(1+\sqrt[4]{3})^2,
 \qquad L=1+\sqrt3.
\]

Reduce (38) modulo \(x^4=\rho^{4\ell}\).  If
\(\eta_q=1\), then \(x^4\mid z^4-c^4\).  The four linear factors
\(z-uc\), \(u\in\{1,-1,i,-i\}\), are pairwise coprime at \(\rho\), so one
contains all of \(x^4\).  Since the universal height bound gives
\(P<\sqrt3\,QR\),

\[
 Q^4\le N(z-uc)
 \le (\sqrt P+\sqrt{QR})^2
 <\mathcal C QR.
\]

If \(\eta_q=-1\), use instead

\[
 z^4+c^4=(z^2+ic^2)(z^2-ic^2).
\]

The two factors are again coprime at \(\rho\), so one contains \(x^4\), and

\[
 Q^4\le N(z^2\mathbin\pm ic^2)
 \le(P+QR)^2<L^2Q^2R^2.
\]

Consequently

\[
 \eta_q=1\Longrightarrow Q^3<\mathcal C R,
 \qquad
 \eta_q=-1\Longrightarrow Q<LR.                 \tag{39}
\]

The symmetric reduction modulo \(y^4\) gives

\[
 \eta_r=1\Longrightarrow R^3<\mathcal C Q,
 \qquad
 \eta_r=-1\Longrightarrow R<LQ.                 \tag{40}
\]

There are now only three possible locations for the unique negative sign.
If \(\eta_0=-1\), both strong bounds apply, and multiplication gives
\(QR<\mathcal C<6\), impossible because \(Q,R\ge5\).  If
\(\eta_q=-1\), then (39), (40) give

\[
 R^2<\mathcal C L<15,
\]

again impossible for \(R\ge5\).  The case \(\eta_r=-1\) is symmetric.
Thus two all-extreme complementary blocks cannot occur in a dominant
three-block center.  The numerical inequalities used here are rigorous, for
\(\sqrt[4]3<4/3\) and \(\sqrt3<7/4\) give
\(\mathcal C<49/9<6\) and
\(\mathcal C L<539/36<15\).

## Reproducible checks

Run:

```sh
python3 -m unittest -v test_search.py
python3 search.py --center 65
python3 search.py --limit 1000000
```

The program enumerates all Gaussian norm representations of each candidate
center root and then tests the complete four-offset condition.  It is a
bounded falsification tool, not a proof of global nonexistence.
