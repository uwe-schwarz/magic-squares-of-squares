# Exactly three blocks: the balanced/extreme regime

## Status

This note proves four exact reductions:

- a center supported on exactly three prime-power blocks cannot have all four
  offsets locally extreme at all three blocks;
- for a squarefree center root supported on exactly three primes, incidence,
  orientation frustration, nonzero-ness, and pairwise distinctness leave 28
  physical switching classes;
- exact arithmetic arguments exclude all 28 of those classes;
- the same classification and all of its arithmetic exclusions remain valid
  for arbitrary exponents provided every local index is either balanced or
  extreme.

Thus no center root \(p^kq^\ell r^m\) supported on exactly three primes is
admissible when all its local indices lie in
\(\{0,\mathord\pm k\}\), \(\{0,\mathord\pm\ell\}\), and
\(\{0,\mathord\pm m\}\), respectively.  In particular, this includes the
squarefree case.  It does not exclude a higher-exponent block with a genuine
intermediate local index, and it is not a proof of global nonexistence.

The finite classification is reproduced by
[`three_block_squarefree.py`](three_block_squarefree.py) and
[`three_block_signatures.py`](three_block_signatures.py), using exact
rational and binary arithmetic.  The final exclusions in Sections 14--16
and their block transfer in Section 17 are proof-only arithmetic descents,
not bounded searches.

After interchanging the two corner coordinates if necessary, write

\[
 D_0=a,\quad D_1=b,\quad D_2=c=a+b,\quad D_3=d=a-b,
 \qquad a>b>0.                                      \tag{1}
\]

Columns 0 and 1 are corners; columns 2 and 3 are edges.  Deleting an edge
leaves a coefficient-111 relation, while deleting a corner leaves a
coefficient-211 relation.

## 1. Three all-unit blocks are impossible

Let

\[
 e=PQR=p^kq^\ell r^m
\]

have exactly three prime-power blocks.  Choose one Gaussian prime above each
rational prime and put

\[
 U=\frac{\pi^{4k}}{P^2},\qquad
 V=\frac{\rho^{4\ell}}{Q^2},\qquad
 W=\frac{\sigma^{4m}}{R^2}.                         \tag{2}
\]

Assume all four offsets are local units at all three blocks.  Each block is
then extreme, so an offset chooses each factor in (2) or its conjugate.
Overall signs and conjugation do not change the absolute imaginary part.
The orientation is a vector in \(\mathbb F_2^3\) modulo simultaneous
complementation.

There are four such classes.  Repeating one repeats the absolute offset, so
distinctness forces all four.  Row and column switches put them in the
Hadamard form

\[
 \begin{pmatrix}
 0&0&0&0\\
 0&0&1&1\\
 0&1&0&1
 \end{pmatrix}.                                     \tag{3}
\]

No factor in (2) is real or purely imaginary: otherwise its two valuations
above the underlying rational prime would agree, although they are \(4k,0\),
or the analogous pair.  Thus

\[
 x=\tan\arg U,\qquad y=\tan\arg V,\qquad z=\tan\arg W
\]

are nonzero rationals.  After removing the common nonzero cosine factor, the
four signed projections are

\[
\begin{aligned}
 S_0&=x+y+z-xyz, & S_1&=x+y-z+xyz,\\
 S_2&=x-y+z+xyz, & S_3&=x-y-z-xyz.                  \tag{4}
\end{aligned}
\]

Their absolute values must equal the four values in (1).

Assign the \(S_i\) bijectively to the roles \((a,b,c,d)\), and independently
choose their four absolute-value signs.  The \(4!2^4=384\) possibilities are
exhaustive.  The equations

\[
 c-a-b=0,\qquad d-a+b=0                              \tag{5}
\]

are linear in \((x,y,z,w)\), where \(w=xyz\).  Exact row reduction gives 48
rank-two equation spaces, each with multiplicity eight.  Signed
permutations of \(x,y,z\), with the product sign on \(w\), give two orbits
of size 24.  Representatives are

\[
\begin{array}{ll}
 \mathrm A:&x-z-2w=0,\qquad y-2z+w=0,\\
 \mathrm B:&2x-z-w=0,\qquad 2y-5z-w=0.               \tag{6}
\end{array}
\]

Put \(t=xy\), so \(w=zt\).  Orbit A yields

\[
 x=z(1+2t),\quad y=z(2-t),\quad
 v^2=t(1+2t)(2-t),\quad v=z(1+2t)(2-t).
\]

With \(X=-2t-1,Y=2v\), this is

\[
 E:\quad Y^2=X(X+1)(X+5).                            \tag{7}
\]

Orbit B yields

\[
 x=\frac{z(1+t)}2,\quad y=\frac{z(5+t)}2,\quad
 v^2=t(t+1)(t+5),\quad v=\frac{z(t+1)(t+5)}2,
\]

the same curve with \(X=t,Y=v\).

A full 2-descent on (7) has Kummer candidates

\[
 b_1\in\{\mathord\pm1,\mathord\pm5\},\qquad
 b_2\in\{\mathord\pm1,\mathord\pm2\}.
\]

The real components leave eight pairs.  Four are the rational two-torsion
classes.  A primitive point in any other class would give

\[
 b_2U_2^2-b_1U_1^2=T_0^2,\qquad
 b_1b_2U_3^2-b_1U_1^2=5T_0^2.
\]

The classes \((1,2),(5,2)\) make all four variables even by reduction modulo
8; the classes \((-1,-2),(-5,-2)\) make them all divisible by 5.  Counts
\(\#E(\mathbb F_3)=\#E(\mathbb F_7)=4\) at good primes exclude further
torsion.  Hence

\[
 E(\mathbb Q)=\{O,(0,0),(-1,0),(-5,0)\}.             \tag{8}
\]

For orbit B the affine \(t\)-values are \(0,-1,-5\); for orbit A they are
\(0,-\tfrac12,2\).  The first contradicts \(t=xy\ne0\), and every other
value makes a factor in the defining equation for \(t\) vanish while
\(t\ne0\).  The point at infinity is not affine.  This proves:

\[
 \boxed{\text{Three prime-power blocks cannot all be unit at all four
 offsets.}}                                         \tag{9}
\]

The proof did not use squarefree exponents.

## 2. Every three-offset relation must be frustrated

[`hourglass-sunit.md`](hourglass-sunit.md) sharpens its coherent-orientation
theorem to both coefficient types:

\[
 \boxed{\text{Every 111 and every 211 relation of three distinct positive
 admissible offsets is orientation-incoherent.}}     \tag{10}
\]

For 111, the exact coherent quotient becomes a signed zero sum of the four
unit vectors

\[
 \alpha\beta,\quad\alpha\gamma,\quad\beta\gamma,\quad1.
\]

Four unit vectors with zero sum pair antipodally.  Every pairing would make
at least two disjoint one-sided Gaussian support blocks trivial, forcing one
primitive denominator to equal one.

For 211, the quotient first makes the pair-support factor opposite the
doubled term trivial.  The remaining sign classes reduce either to a
forbidden slope of magnitude one or to a strictly positive rational square
\(T\) on

\[
 Z^2=T(T+1)(T+9).
\]

A 2-isogeny descent gives rank zero and the complete \(T\)-coordinate set
\(\{0,-1,-9,3,-3\}\), with no strictly positive rational square.  The
detailed sign normalization and descent are kept in
`hourglass-sunit.md`; only the conclusion (10) is used below.

## 3. Exact squarefree distinctness

Now let \(e=pqr\).  For column \(c\), write its local-index vector as

\[
 j_c=(j_{p,c},j_{q,c},j_{r,c})\in\{-1,0,1\}^3.       \tag{11}
\]

A zero coordinate is the unique balanced exception in that prime row; a
nonzero coordinate records an extreme orientation.  Up to sign, the
normalized squared direction is

\[
 \prod_s\left(\frac{\pi_s}{\bar\pi_s}\right)^{2j_{s,c}}.
\]

Thus \(j_c=0\) gives offset zero, while \(j_c=\pm j_d\) gives equal absolute
offsets.

Conversely, two unit complex numbers with the same absolute imaginary part
differ by sign and possibly conjugation.  Unique factorization at the three
disjoint Gaussian supports then gives \(j_c=\pm j_d\).  Therefore
nonzero-ness and pairwise distinctness are exactly

\[
 j_c\ne0,\qquad j_c\ne\pm j_d\quad(c\ne d).          \tag{12}
\]

This projective exponent-vector test is stronger than merely rejecting a
column balanced at all three primes.

## 4. Complete physical binary classification

Write `F` for a prime row without a balanced column, and put a star in the
balanced column otherwise.  A bit records each nonzero coordinate in (11).
The classifier applies:

1. the four incoherence requirements (10);
2. the exact projective condition (12);
3. row switches, column switches, prime permutations, the corner swap, and
   the edge swap.

Corners are never exchanged with edges.  The mask symmetry is exactly

\[
 S_3\ \text{on rows}\ \times S_2\ \text{on corners}\
 \times S_2\ \text{on edges}.                        \tag{13}
\]

There are 16 mask orbits.  Exhausting at most \(2^{12}\) bit assignments in
each gives:

| Canonical mask | Raw survivors | Switching classes |
| --- | ---: | ---: |
| `F,F,F` | 384 | 1 |
| `F,F,C` | 768 | 4 |
| `F,F,E` | 768 | 4 |
| `F,C,C`, same corner | 384 | 2 |
| `F,C0,C1` | 384 | 2 |
| `F,C,E` | 384 | 6 |
| `F,E,E`, same edge | 384 | 2 |
| `F,E0,E1` | 384 | 2 |
| `C,C,C`, same corner | 0 | 0 |
| `C,C,C`, two at one corner | 64 | 1 |
| `C,C,E`, same corner | 64 | 1 |
| `C0,C1,E` | 64 | 1 |
| `C,E,E`, same edge | 64 | 1 |
| `C,E0,E1` | 64 | 1 |
| `E,E,E`, same edge | 0 | 0 |
| `E,E,E`, two at one edge | 64 | 1 |

Raw survivors are labeled bit assignments after all four incoherence tests
and (12), before switching and mask automorphisms.  Repeated letters without
numeric suffix mean the same exception column.  The script prints every
canonical bit matrix.

The table has 29 switching classes.  Its single `F,F,F` class is the
Hadamard class excluded by (9).  Hence the exact binary squarefree residue is

\[
 \boxed{28\text{ physical switching classes, all with at least one balanced
 exception.}}                                       \tag{14}
\]

This proves neither existence nor nonexistence.  It identifies exactly where
incidence, frustration, and projective distinctness stop; a further
three-block argument must use block-size arithmetic or couple the four
Gaussian identities more strongly.

## 5. One `112` class is arithmetically impossible

Consider the physical mask `(0,0,1)`: the `p`- and `q`-rows are balanced at
the first corner, while the `r`-row is balanced at the second corner.  The
classifier leaves exactly one switching class,

```text
*000/*011/0*01.
```

Choose Gaussian primes above `p,q,r` and, after the row switches represented
in this normal form, put

\[
 x=\frac{\pi^4}{p^2}=e^{i\alpha},\qquad
 y=\frac{\rho^4}{q^2}=e^{i\beta},\qquad
 z=\frac{\sigma^4}{r^2}=e^{i\gamma}.               \tag{15}
\]

Independent column switches only multiply the following directions by
signs, which do not affect their absolute imaginary parts.  The four column
directions are

\[
 z,\qquad xy,\qquad x\bar y z,\qquad x\bar y\bar z.\tag{16}
\]

The first two columns are the corners and the last two are the edges.  Put

\[
 A=|\sin\gamma|,\qquad B=|\sin(\alpha+\beta)|,
 \qquad \Delta=\alpha-\beta.
\]

The two edge projections are

\[
 \sin(\Delta+\gamma)=u+v,\qquad
 \sin(\Delta-\gamma)=u-v,                           \tag{17}
\]

where

\[
 u=\sin\Delta\cos\gamma,\qquad
 v=\cos\Delta\sin\gamma.
\]

For arbitrary real `u,v`,

\[
 \{|u+v|,|u-v|\}
 =\{|u|+|v|,\,\bigl||u|-|v|\bigr|\}.
\]

The magic-square edge magnitudes are likewise
\(\{A+B,|A-B|\}\).  The unordered pair that generates a sum and an
absolute difference is uniquely recovered, so

\[
 \{|u|,|v|\}=\{A,B\}.                               \tag{18}
\]

If \(|v|=A\), then \(|\cos\Delta|=1\).  This makes `u=0` and the
two edge magnitudes in (17) equal, contradicting distinctness.  Hence
\(|u|=A\).  Neither coordinate of a nontrivial one-sided Gaussian block
vanishes, so \(\cos\gamma\ne0\), and therefore

\[
 \boxed{|\tan\gamma|=|\sin(\alpha-\beta)|}.          \tag{19}
\]

Write the two rational unit directions in reduced Gaussian form as

\[
 z=\frac{R+iS}{r^2},\qquad
 x\bar y=\frac{C+iN}{p^2q^2}.                       \tag{20}
\]

The coordinates `R,S` are coprime: a common rational prime would divide the
norm \(r^4\), but the one-sided Gaussian factor \(\sigma^4\) is not
divisible by both primes above `r`.  Moreover, `N` is divisible by neither
`p` nor `q`.  Explicitly,

\[
 2iN=\pi^4\bar\rho^4-\bar\pi^4\rho^4.
\]

Modulo \(\pi\), the first term vanishes and the second does not; modulo
\(\bar\rho\), the first term vanishes and the second again does not.  Thus
both fractions in

\[
 \frac{|S|}{|R|}=\frac{|N|}{p^2q^2}
\]

are reduced.  Equation (19) consequently forces

\[
 |R|=p^2q^2,\qquad (pq)^4+S^2=r^4.                 \tag{21}
\]

It remains to recall the rational points on the resulting quartic.  With

\[
 t=\frac{pq}{r},\qquad v_0=\frac{S}{r^2},
\]

equation (21) gives

\[
 v_0^2=1-t^4,\qquad 0<t<1.                         \tag{22}
\]

For `t` nonzero, the substitution

\[
 X=\frac{2(1+v_0)}{t^2},\qquad
 Y=\frac{4(1+v_0)}{t^3}
\]

maps (22) to

\[
 E:\qquad Y^2=X^3+4X.                              \tag{23}
\]

For completeness, the standard 2-isogeny at `(0,0)` gives

\[
 E':\qquad y^2=x^3-16x.
\]

The descent image for `E` is \(\{1,2\}\): the only candidate
squareclasses are \(\mathord\pm1,\mathord\pm2\), negative classes are
excluded by \(X(X^2+4)\ge0\), and both positive classes occur.  For `E'`,
the classes \(1,-1\) occur, while the two remaining covers would be

\[
 M_0^2=2M_1^4-8M_2^4
 \quad\text{or}\quad
 M_0^2=-2M_1^4+8M_2^4.
\]

If `M1` is odd, either right side is a nonsquare modulo 16; if `M1` is even,
primitivity makes `M2` odd and the right side is 8 modulo 16.  Hence the
second descent image is \(\{1,-1\}\), and the 2-isogeny rank formula gives
`rank E(Q)=0`.

Direct counting gives \(\#E(\mathbb F_3)=4\) and
\(\#E(\mathbb F_5)=8\).  The four visible points therefore exhaust the
rational torsion:

\[
 E(\mathbb Q)=\{O,(0,0),(2,4),(2,-4)\}.             \tag{24}
\]

A point produced by (22) has `X>0`, so (24) forces `X=2`; the inverse
relation \(t=2X/Y\) then gives only `t=1` or `t=-1`.  Neither lies in the
required range \(0<t<1\) (and `t=1` forces the forbidden boundary `S=0`).
This excludes the unique `(0,0,1)` class and sharpens the squarefree
residue to

\[
 \boxed{27\text{ physical switching classes}.}      \tag{25}
\]

## 6. Two companion `112` classes have the same obstruction

The same quartic excludes two further physical classes.  First consider the
mask `(2,2,3)`, whose unique canonical form is

```text
00*0/00*1/010*.
```

With `x,y,z` as in (15), put

\[
 \Sigma=\alpha+\beta,\qquad \Delta=\alpha-\beta.
\]

The two corner directions and two edge directions are, respectively,

\[
 xyz,\quad xy\bar z;\qquad z,\quad x\bar y.         \tag{26}
\]

Writing

\[
 u=\sin\Sigma\cos\gamma,\qquad
 v=\cos\Sigma\sin\gamma,
\]

the corner projections are `u+v` and `u-v`.  Their sum and absolute
difference are the edge magnitudes.  Therefore

\[
 \{|\sin\gamma|,|\sin\Delta|\}
 =\{2|u|,2|v|\}.                                    \tag{27}
\]

If \(|\sin\gamma|=2|v|\), then
\(|\cos\Sigma|=1/2\).  Both sine and cosine of `Sigma` are rational because
`xy` is a rational point on the unit circle, whereas
\(\sin^2\Sigma=3/4\) has no rational square root.  Hence the other matching
in (27) is forced, and it gives

\[
 |\tan\gamma|=2|\sin\Sigma|.                        \tag{28}
\]

For the second mask `(0,0,2)`, the unique canonical form is

```text
*000/*010/00*1.
```

Its corner and edge directions are

\[
 z,\quad xyz;\qquad x\bar y,\quad xy\bar z,         \tag{29}
\]

with arguments

\[
 \gamma,\quad\Sigma+\gamma;\qquad
 \Delta,\quad\Sigma-\gamma.
\]

Choose signs `a,b` which make the two corner projections positive and signs
for the edge projections.  First suppose the displayed third column is the
sum edge and the fourth is the difference edge.  The latter relation has
the form

\[
 d\sin(\Sigma-\gamma)
 =a\sin\gamma-b\sin(\Sigma+\gamma),
 \qquad a,b,d\in\{1,-1\}.                           \tag{30}
\]

Put \(s=b/a\) and \(t=d/a\).  Expanding (30) gives

\[
 (t+s)\sin\Sigma\cos\gamma
 +(s-t)\cos\Sigma\sin\gamma-\sin\gamma=0.         \tag{31}
\]

If `t=-s`, this gives \(\cos\Sigma=s/2\), the same rational-phase
impossibility as above.  If `t=s`, it gives (28), including its factor `2`.

The edge-swapped assignment gives no extra branch.  If the displayed fourth
column is the sum edge, its signed relation instead expands to

\[
 (t-s)\sin\Sigma\cos\gamma
 -(t+s)\cos\Sigma\sin\gamma-\sin\gamma=0.          \tag{32}
\]

Now `t=s` gives \(\cos\Sigma=\mathord\pm1/2\), while `t=-s` gives
\(\tan\gamma=\mathord\pm2\sin\Sigma\).  Thus both physical edge-role
assignments reduce to (28).

Write

\[
 z=\frac{R+iS}{r^2},\qquad
 xy=\frac{C+iL}{p^2q^2}.
\]

Exactly as after (20), the fractions \(S/R\) and
\(2L/(p^2q^2)\) are reduced; `p,q` are odd and neither divides `L`.
Equation (28) therefore gives

\[
 |R|=p^2q^2,\qquad |S|=2|L|,\qquad
 (pq)^4+(2L)^2=r^4.                                 \tag{33}
\]

But (33) is the quartic (21), whose rational points were completely
excluded in (22)--(24).  The two companion classes are impossible.  Together
with Section 5 this sharpens the squarefree residue to

\[
 \boxed{25\text{ physical switching classes}.}      \tag{34}
\]

## 7. One `123` class is elementary

The mask `(0,1,2)` also has one canonical form,

```text
*000/1*01/00*1.
```

Its first two columns are the corners.  Their directions and the direction
of the third column are

\[
 \bar y z=e^{iA},\qquad xz=e^{iB},\qquad
 xy=e^{i(B-A)}.                                     \tag{35}
\]

The third column is one of the two edges.  Whether it is the sum edge or the
absolute-difference edge, its required magnitude gives signs
\(s,t\in\{1,-1\}\) such that

\[
 \sin(B-A)=s\sin A+t\sin B.                         \tag{36}
\]

All three sines are nonzero by offset positivity.  Put

\[
 u=\tan\frac A2,\qquad v=\tan\frac B2.
\]

The nonzero corner projections make `u,v` finite and nonzero.  Clearing the
two half-angle denominators in (36) gives

\[
 (v-u)(1+uv)-su(1+v^2)-tv(1+u^2)=0.                \tag{37}
\]

For the four choices of `(s,t)`, the left side factors, up to order, as

\[
 2v(1+uv),\qquad 2uv(v-u),\qquad
 2(v-u),\qquad -2u(1+uv).                           \tag{38}
\]

Every zero in (38) is degenerate: `u=0` or `v=0` makes a corner projection
zero, while `v=u` or `1+uv=0` makes
\(\sin(B-A)=0\).  This contradiction covers both possible edge roles of the
third column.  Hence the `(0,1,2)` class is impossible, and the current
squarefree residue is

\[
 \boxed{24\text{ physical switching classes}.}      \tag{39}
\]

## 8. The last repeated-edge `112` class

Consider the mask `(0,2,2)` and its unique form

```text
*000/00*1/10*1.
```

Put \(U=\beta+\gamma\) and \(V=\beta-\gamma\).  The corner and edge
directions are

\[
 y\bar z,\quad xyz;\qquad x,\quad x\bar y\bar z,
\]

with arguments

\[
 V,\quad\alpha+U;\qquad\alpha,\quad\alpha-U.        \tag{40}
\]

Choose signs for the two corner projections and the two edge projections.
If the displayed third column is the sum edge, the two signed relations may
be written

\[
 c\sin\alpha=a\sin V+b\sin(\alpha+U),
\qquad
 d\sin(\alpha-U)=a\sin V-b\sin(\alpha+U).          \tag{41}
\]

Eliminating \(a\sin V\), and writing \(s=c/b,t_0=d/b\), gives

\[
 \tan\alpha=
 \begin{cases}
 \displaystyle\frac{\sin U}{s-3\cos U},&t_0=1,\\[2mm]
 \displaystyle\frac{3\sin U}{s-\cos U},&t_0=-1.
 \end{cases}                                       \tag{42}
\]

If the two edge roles are swapped, the analogous equations with
\(\sin\alpha\) and \(\sin(\alpha-U)\) exchanged give the same four
possibilities.  Thus, with \(t=\tan(U/2)\), signs absorbed, every case lies
in

\[
 \tan\alpha\in
 \left\{\mathord\pm3t,\mathord\pm\frac3t,
 \mathord\pm\frac{t}{1-2t^2},
 \mathord\pm\frac{t}{2-t^2}\right\}.              \tag{43}
\]

The denominators in (42)--(43) do not vanish: that would require either a
vanishing coordinate of a one-sided Gaussian block or a rational square
root of `2`.

Write the one-sided square roots of the two phases as

\[
 \pi^2=A+iB,\qquad \rho^2\sigma^2=R+iS.            \tag{44}
\]

Unique factorization and parity give

\[
 \gcd(A,B)=\gcd(R,S)=1,\quad A,R\text{ odd},\quad
 4\mid B,S,
\]

and

\[
 A^2+B^2=p^2,\qquad R^2+S^2=(qr)^2,\qquad
 \tan\alpha=\frac{2AB}{A^2-B^2},\qquad t=\frac SR.\tag{45}
\]

Both displayed tangent fractions are reduced.  For the first two branches
in (43), cancelling at most a factor `3` shows that one of

\[
 R^2+9S^2,\qquad 9R^2+S^2
\]

is also a square.  Together with (45), this contradicts the simultaneous
square obstruction \(R^2+S^2=W_1^2\),
\(R^2+9S^2=W_2^2\) proved in the coherent-`211` descent of
[`hourglass-sunit.md`](hourglass-sunit.md), with `R,S` interchanged when
needed.

For the third branch of (43), the coordinate pair

\[
 (RS,R^2-2S^2)
\]

is coprime.  Equality of the reduced tangent fractions and (45) give

\[
 p^4=R^4-3R^2S^2+4S^4.                             \tag{46}
\]

For the fourth branch, the coordinate gcd of

\[
 (RS,2R^2-S^2)
\]

is exactly `2`: there is no common odd prime, while `R` is odd and
\(4\mid S\).  Put \(S=2S_0\).  After the exact factor-two reduction, taking
the same norm gives

\[
 p^4=R^4-3R^2S_0^2+4S_0^4.                        \tag{47}
\]

Both (46) and (47) contradict the quartic lemma in Section 6 of
[`two-block-exponent-one.md`](two-block-exponent-one.md), since all relevant
coordinates are nonzero.  Therefore the `(0,2,2)` class is impossible.

## 9. The last distinct-edge `123` class

The mask `(0,2,3)` has the unique form

```text
*000/00*1/101*.
```

The four phase arguments are

\[
 A=\beta-\gamma,\qquad B=\alpha+\beta+\gamma,
 \qquad C=\alpha-\gamma,\qquad D=\alpha-\beta,     \tag{48}
\]

where `A,B` are the corners and `C,D` are the edges.  In particular,
\(A=C-D\).  Adding the two signed edge relations, in either assignment of
the sum and difference roles, gives signs \(g,d\in\{1,-1\}\) such that

\[
 2\sin(C-D)=g\sin C+d\sin D.                       \tag{49}
\]

Put \(u=\tan(C/2)\) and \(v=\tan(D/2)\).  Clearing denominators in (49)
gives, for the four choices of `(g,d)`, the factors

\[
 (3u-v)(1+uv),\quad (u-v)(uv+3),\quad
 (u-v)(3uv+1),\quad (u-3v)(1+uv).                  \tag{50}
\]

The quantities `u,v` are finite and nonzero.  The factors `u-v` and
`1+uv` would make the corner projection \(\sin(C-D)\) zero.  Hence (50)
leaves only

\[
 v=3u,\qquad u=3v,\qquad uv=-3,\qquad uv=-\frac13. \tag{51}
\]

Now `u` and `v` are the reduced coordinate slopes of the primitive Gaussian
integers \(\pi^2\bar\sigma^2\) and
\(\pi^2\bar\rho^2\), whose hypotenuses are `pr` and `pq`.  Write
\(u=S/R\), so \(R^2+S^2=(pr)^2\).  In each case of (51), reducing the
corresponding slope `v` cancels at most a factor `3`.  Its square norm then
makes one of

\[
 R^2+9S^2,\qquad 9R^2+S^2
\]

a square.  The same simultaneous-square obstruction used in Section 8 gives
a contradiction.  Thus `(0,2,3)` is impossible as well.

All six binary classes without an `F` row have now been excluded.  Every
squarefree three-prime survivor must have at least one prime block extreme
at all four offsets, and the residue is

\[
 \boxed{22\text{ physical switching classes}.}      \tag{52}
\]

## 10. Four `FF` classes are impossible

It remains useful to exploit the extra rigidity of two all-extreme rows.
Put

\[
 U=\alpha+\beta,\qquad \Delta=\alpha-\beta.
\]

Consider first the corner-exception and edge-exception forms

```text
0000/0001/*010
0000/0001/01*0.
```

Their corner and edge arguments are, respectively,

\[
 (U,U+\gamma;\ U-\gamma,\Delta+\gamma)
\]

and

\[
 (U+\gamma,U-\gamma;\ U,\Delta+\gamma).            \tag{53}
\]

In the first form, the displayed third column is a signed sum or difference
of the two corners, so for some \(s,t\in\{1,-1\}\),

\[
 \sin(U-\gamma)=s\sin U+t\sin(U+\gamma).           \tag{54}
\]

If `t=-1`, expansion gives \(\cos\gamma=s/2\); if `t=1`, it gives
\(\tan U=-2s\sin\gamma\).  In the second form the corresponding equation
is

\[
 \sin U=s\sin(U+\gamma)+t\sin(U-\gamma),           \tag{55}
\]

which gives the same two alternatives.  The free signs in (54)--(55) cover
both assignments of the two physical edge roles.

The value \(\cos\gamma=\mathord\pm1/2\) is impossible because both
coordinates of the rational unit direction `z` are rational.  For the other
alternative, write

\[
 \pi^2\rho^2=A+iB,\qquad \sigma^2=C+iD.
\]

These are primitive one-sided Gaussian integers, with

\[
 A^2+B^2=(pq)^2,\qquad C^2+D^2=r^2,\qquad
 \tan U=\frac{2AB}{A^2-B^2},\qquad
 2\sin\gamma=\frac{4CD}{r^2}.                      \tag{56}
\]

The two fractions in (56) are reduced.  Hence (54) or (55) forces

\[
 r^4+(4CD)^2=(pq)^4,                                \tag{57}
\]

contradicting the quartic obstruction (21)--(24).

The second corner-exception form

```text
0000/0100/*001
```

has corner arguments \(U,\Delta+\gamma\) and edge arguments
\(U+\gamma,U-\gamma\).  Put

\[
 u=\sin U\cos\gamma,\qquad v=\cos U\sin\gamma.
\]

The two edge magnitudes are \(|u+v|,|u-v|\).  Inverting their sum and
absolute difference against the corner magnitudes gives

\[
 \{|u|,|v|\}
 =\{|\sin U|,|\sin(\Delta+\gamma)|\}.              \tag{58}
\]

The matching \(|u|=|\sin U|\) would force
\(|\cos\gamma|=1\), contradicting the nonzero imaginary coordinate of the
one-sided `r`-block.  The other matching gives

\[
 |\tan U|=|\sin\gamma|.
\]

Using the same reduced coordinates as in (56) now yields

\[
 r^4+(2CD)^2=(pq)^4,                                \tag{59}
\]

again impossible by (21)--(24).  The unordered argument in (58) already
covers both edge-role assignments.

Finally, the edge-exception form

```text
0000/0100/00*1
```

has corner arguments \(U+\gamma,\Delta+\gamma\) and edge arguments
\(U,U-\gamma\).  The coefficient-`211` relation involving the first corner
and both edges has, after sign normalization, the form

\[
 2\sin(U+\gamma)=s\sin U+t\sin(U-\gamma).          \tag{60}
\]

With \(w=\tan(\gamma/2)\), expansion over all four sign choices gives

\[
 \tan U\in
 \left\{\mathord\pm3w,\mathord\pm\frac3w,
 \mathord\pm\frac{w}{1-2w^2},
 \mathord\pm\frac{w}{2-w^2}\right\}.              \tag{61}
\]

Write \(\sigma^2=R+iS\), so

\[
 \gcd(R,S)=1,\quad R\text{ odd},\quad4\mid S,\quad
 R^2+S^2=r^2,\quad w=\frac SR.                     \tag{62}
\]

The first two branches of (61), after cancelling at most a factor `3`,
contradict the simultaneous-square obstruction used in Sections 8--9.  For
the third branch, the reduced coordinate pair is
\((RS,R^2-2S^2)\), and taking norms gives

\[
 (pq)^4=R^4-3R^2S^2+4S^4.                          \tag{63}
\]

For the fourth branch, \((RS,2R^2-S^2)\) has coordinate gcd exactly `2`.
Writing \(S=2S_0\) after reduction gives

\[
 (pq)^4=R^4-3R^2S_0^2+4S_0^4.                     \tag{64}
\]

Equations (63)--(64) contradict the quartic lemma used in Section 8.  This
exhausts all signs and both edge roles in (60).

Of the 22 classes remaining after Section 9, eight had two `F` rows and
fourteen had one.  We have excluded four of the former.  Thus every survivor
still has an all-extreme prime row, and the current exact squarefree residue
is

\[
 \boxed{18\text{ physical switching classes}:\ 4\text{ with two `F` rows
 and }14\text{ with one}.}                          \tag{65}
\]

## 11. Four repeated-exception one-`F` classes are impossible

The same short phase arguments eliminate every class in which the other two
prime rows are balanced at the same corner or at the same edge.

For

```text
0000/*001/*010
```

the corner directions are `x,xyz` and the edge directions are
\(xy\bar z,x\bar y z\).  Put \(W=\beta-\gamma\).  The edge arguments are
\(\alpha+W,\alpha-W\).  Inverting their sum and absolute difference against
the two corner magnitudes gives

\[
 \{|\sin\alpha\cos W|,|\cos\alpha\sin W|\}
 =\{|\sin\alpha|,|\sin(\alpha+\beta+\gamma)|\}.
                                                               \tag{66}
\]

The first matching would force \(|\cos W|=1\), impossible for a nontrivial
one-sided composite block.  The second gives

\[
 |\tan\alpha|=|\sin W|.                             \tag{67}
\]

Write

\[
 \pi^2=A+iB,\qquad \rho^2\bar\sigma^2=C+iD.
\]

Both Gaussian integers are primitive, their coordinates are nonzero, and

\[
 A^2+B^2=p^2,\qquad C^2+D^2=(qr)^2.
\]

The reduced fractions in (67) therefore give

\[
 p^4=(qr)^4+(2CD)^2,                                \tag{68}
\]

contradicting (21)--(24).

For

```text
0000/*001/*011
```

put instead \(W=\beta+\gamma\).  The known edge has argument
\(\alpha-W\), while the corners have arguments \(\alpha,\alpha+W\).
Thus

\[
 \sin(\alpha-W)=s\sin\alpha+t\sin(\alpha+W).
\]

As in (54), expansion gives either \(\cos W=\mathord\pm1/2\), impossible
for a rational unit direction, or
\(|\tan\alpha|=2|\sin W|\).  With
\(\rho^2\sigma^2=C+iD\), reduced coordinates give

\[
 p^4=(qr)^4+(4CD)^2,                                \tag{69}
\]

again impossible.

The edge analogue

```text
0000/01*0/01*1
```

has corner arguments \(\alpha+W,\alpha-W\), with
\(W=\beta+\gamma\), and a known edge argument \(\alpha\).  Its signed
relation

\[
 \sin\alpha=s\sin(\alpha+W)+t\sin(\alpha-W)
\]

has the same two branches and the same contradiction (69).  Free signs and
the unordered magnitude inversions cover both physical edge roles in all
three cases.

The final form

```text
0000/00*1/01*0
```

has a known corner argument \(\alpha-W\) and edge arguments
\(\alpha,\alpha+W\), where \(W=-\beta+\gamma\).  Sum/difference inversion
gives

\[
 2\sin(\alpha-W)=s\sin\alpha+t\sin(\alpha+W).       \tag{70}
\]

With \(w=\tan(W/2)\), the four sign choices yield the familiar exhaustive
set

\[
 \tan\alpha\in
 \left\{\mathord\pm3w,\mathord\pm\frac3w,
 \mathord\pm\frac{w}{1-2w^2},
 \mathord\pm\frac{w}{2-w^2}\right\}.              \tag{71}
\]

Write \(\bar\rho^2\sigma^2=C+iD\).  Then

\[
 C^2+D^2=(qr)^2,\qquad \gcd(C,D)=1,\qquad
 C\text{ odd},\quad4\mid D,\qquad w=\frac DC.
\]

The two factor-`3` branches contradict the simultaneous-square obstruction.
The next branch gives

\[
 p^4=C^4-3C^2D^2+4D^4,
\]

and the last branch has coordinate gcd exactly `2`; after writing
\(D=2D_0\), it gives

\[
 p^4=C^4-3C^2D_0^2+4D_0^4.                        \tag{72}
\]

Both contradict the quartic lemma used in Sections 8 and 10.  Thus all four
repeated-exception one-`F` classes are impossible.

The exact squarefree residue is now

\[
 \boxed{14\text{ physical switching classes}:\ 4\text{ with two `F` rows
 and }10\text{ with one}.}                          \tag{73}
\]

## 12. Rigidity of the four remaining two-`F` classes

The four surviving two-`F` classes admit a sharper arithmetic normal form.
Relabel their two all-extreme primes so that \(p\ge q\), normalize the
`p`-row to `0000`, and choose Gaussian primes with

\[
 P=\pi^4,\qquad Q=\rho^4,\qquad R=\sigma^4,
 \qquad |P|=p^2,\quad |Q|=q^2,\quad |R|=r^2.       \tag{74}
\]

The following table records a same-oriented `r`-triple in each canonical
form.  The retained column set includes the balanced entry and two entries
with the same extreme `r`-orientation.

| Canonical form | Retained columns | Omitted role | Type |
| --- | --- | --- | --- |
| `0000/0011/*001` | `0,1,2` | edge `3` | `111` |
| `0000/0101/*001` | `0,1,2` | edge `3` | `111` |
| `0000/0011/01*0` | `0,2,3` | corner `1` | `211` |
| `0000/0101/00*1` | `0,1,2` | edge `3` | `111` |

Align the common `p`-orientation in the indicated triple and form its
Gaussian sum `H` as in [`block-balance.md`](block-balance.md).  Every
residual term is divisible by \(\sigma^2\): the balanced term contains
\(r^2=\sigma^2\bar\sigma^2\), while the two extreme terms contain
\(R=\sigma^4\).  In type `211`, the same divisibility remains true for
`H/2`, because \(\sigma\) is odd.  Hence

\[
 H=\bar P n\quad(111),
 \qquad \frac H2=\bar P n\quad(211),
 \qquad n\in\mathbb Z\setminus\{0\}.               \tag{75}
\]

Since \(\gcd(\sigma,\bar P)=1\), divisibility of the left side by
\(\sigma^2\) gives \(\sigma^2\mid n\).  The quotient `n` is rational, so
conjugation also gives \(\bar\sigma^2\mid n\), and therefore
\(r^2\mid n\).  Write \(n=r^2m\).  The strict height estimates are

\[
 |m|p^2<3q^2\quad(111),
 \qquad |m|p^2<2q^2\quad(211).                     \tag{76}
\]

In type `111`, `n` and hence `m` are odd; since \(p\ge q\), the first
inequality forces \(|m|<3\) and therefore \(m=\mathord\pm1\).  In type
`211`, the second inequality gives \(|m|<2\), which has the same conclusion
without a parity assumption.  Thus every remaining two-`F` class satisfies

\[
 \boxed{n=\mathord\pm r^2.}                        \tag{77}
\]

There is a common exact identity for the three `111` forms.  After absorbing
all coefficient and quotient signs into
\(\varepsilon_j\in\{\mathord\pm1\}\), it is

\[
 \varepsilon_0Qr^2+R(\varepsilon_1Q+\varepsilon_2\bar Q)
   =\varepsilon_3r^2\bar P.                        \tag{78}
\]

Rearranging and cancelling one factor \(\sigma^2\) gives

\[
 \bar\sigma^2(\varepsilon_3\bar P-\varepsilon_0Q)
   =\sigma^2(\varepsilon_1Q+\varepsilon_2\bar Q). \tag{79}
\]

The two Gaussian primes above `r` are coprime, so
\(\bar\sigma^2\mid(\varepsilon_1Q+\varepsilon_2\bar Q)\).  This last
bracket is either twice the real coordinate of `Q` or twice `i` times its
imaginary coordinate, up to sign.  Because `r` is odd and the bracket is
axis-parallel, rational conjugation shows that \(r^2\) divides the
corresponding nonzero coordinate of `Q`.  A one-sided fourth power has both
coordinates nonzero and each has absolute value strictly below \(q^2\).
Consequently the three `111` classes obey

\[
 \boxed{r<q\le p.}                                 \tag{80}
\]

More explicitly, if that coordinate is \(r^2k\), then

\[
 \varepsilon_3\bar P-\varepsilon_0Q=2kuR,
 \qquad k\in\mathbb Z\setminus\{0\},
 \quad u\in\{\mathord\pm1,\mathord\pm i\}.       \tag{81}
\]

Equation (81) is a residual signed fourth-power equation, not yet a
contradiction.

The sole `211` form instead has the exact identity

\[
 \varepsilon_2\bar Qr^2
  +R(\varepsilon_3\bar Q+2\varepsilon_0Q)
  =2\varepsilon_4r^2\bar P,                        \tag{82}
\]

and hence

\[
 \bar\sigma^2\mid(\varepsilon_3\bar Q+2\varepsilon_0Q).       \tag{83}
\]

Unlike the bracket in (79), this one is not axis-parallel.  Thus (83) alone
does not imply divisibility of a Cartesian coordinate by \(r^2\), and the
ordering (80) is asserted only for the three `111` forms.  In particular,
the edge-exception form ending in `00*1` belongs to the `111` family; only
the form ending in `01*0` supplies the `211` identity (82).  These are only
necessary equations for four of the fourteen classes counted in (73), so
they do not reduce that count.

## 13. The ten remaining one-`F` classes are impossible

The last ten classes with only one all-extreme row are excluded by four
elementary Gaussian divisor comparisons.  We first isolate the common
arithmetic lemma.  Let `s` be an odd split prime, choose
\(N(\tau)=s\), and write

\[
 S=\tau^2=X+iY,
 \qquad X^2+Y^2=s^2,
 \qquad \gcd(X,Y)=1,
 \quad X\text{ odd},\quad4\mid Y.                 \tag{84}
\]

Both `X` and `Y` are nonzero because a one-sided Gaussian prime power cannot
be associated to its conjugate.  Let \(N(\beta)=t\) for a different odd
split prime.  We use the following shorthand.

| Symbol | Gaussian divisibility | Consequence |
| --- | --- | --- |
| `A2(t,s)` | \(\beta^2\mid\bar S\mathbin\pm S\) | \(t^2<s\) |
| `A4(t,s)` | \(\beta^2\mid\bar S^2\mathbin\pm S^2\) | \(t<s\) |
| `S2(t,s)` | \(\beta^2\mid2\bar S\mathbin\pm S\), or its conjugate | \(t<s\) |
| `S4(t,s)` | \(\beta^2\mid2\bar S^2\mathbin\pm S^2\), or its conjugate | \(t<s^2\) |

For `A2`, the divisible expression is either `2X` or `-2iY`.  Conjugating
the divisibility and using \(\gcd(\beta,\bar\beta)=1\) shows that the
rational integer \(t^2\) divides the corresponding coordinate.  Since `t`
is odd and both coordinates have absolute value strictly below `s`, this
gives \(t^2<s\).  Applying the same argument to the nonzero coordinates of
\(S^2\), whose modulus is \(s^2\), proves `A4`.

For the skew expressions,

\[
 N(2\bar S+S)=9X^2+Y^2,
 \qquad N(2\bar S-S)=X^2+9Y^2.                    \tag{85}
\]

Both norms are `1` modulo `8`.  If `S2(t,s)` held with \(t\ge s\), then
the positive integer obtained by dividing the relevant norm in (85) by
\(t^2\) would be congruent to `1` modulo `8` and strictly smaller than `9`.
It would therefore equal `1`.  This would make both
\(X^2+Y^2\) and one of \(9X^2+Y^2,X^2+9Y^2\) squares, contradicting the
simultaneous-square lemma proved in the coherent-`211` descent of
[`hourglass-sunit.md`](hourglass-sunit.md).  Hence `S2(t,s)` implies
\(t<s\).  Applying this argument to \(S^2\), whose odd coordinate remains
odd and whose even coordinate is divisible by `4`, gives

\[
 \boxed{
 \begin{aligned}
  \mathrm{A2}(t,s)&\Longrightarrow t^2<s,&
  \mathrm{A4}(t,s)&\Longrightarrow t<s,\\
  \mathrm{S2}(t,s)&\Longrightarrow t<s,&
  \mathrm{S4}(t,s)&\Longrightarrow t<s^2.
 \end{aligned}}                                    \tag{86}
\]

Now normalize the unique `F` row to `0000` and denote its prime by `p`.
In either of the other rows, retain the balanced column and the two columns
having the same extreme bit; equivalently, delete that row's minority-bit
column.  The resulting triple has type `111` when an edge is deleted and
type `211` when a corner is deleted.

Aligning the common `p`-orientation gives
\(H=\bar Pn\) in type `111` and \(H/2=\bar Pn\) in type `211`, as in
Section 12.  If the selected row is the `q`-row, all three residual terms
are divisible by the same one of \(\rho^2,\bar\rho^2\).  Dividing by `2` in type
`211` does not change this valuation because `q` is odd.  Since `n` is
rational and `p` and `q` are distinct, conjugation gives

\[
 q^2\mid n_q.
 \qquad\text{Likewise,}\qquad r^2\mid n_r.         \tag{87}
\]

Substituting (87) back into the two exact relations and cancelling the
common Gaussian square leaves one of four small factors in the other prime
block.  Up to signs and conjugation, they are

\[
 \begin{array}{c|c}
 \mathrm{A2}(q,r)&\bar\rho^2\mid\bar\sigma^2\mathbin\pm\sigma^2\\
 \mathrm{A4}(q,r)&\bar\rho^2\mid\bar\sigma^4\mathbin\pm\sigma^4\\
 \mathrm{S2}(q,r)&\bar\rho^2\mid2\bar\sigma^2\mathbin\pm\sigma^2\\
 \mathrm{S4}(q,r)&\bar\rho^2\mid2\bar\sigma^4\mathbin\pm\sigma^4
 \end{array}                                       \tag{88}
\]

The same formulas with `q,r` interchanged describe the second deletion.
For example, a `111` triple containing one balanced and one extreme
`r`-factor leaves
\(r^2\mathbin\pm R=\sigma^2(\bar\sigma^2\mathbin\pm\sigma^2)\),
which is `A2(q,r)` after the
coprime factor \(\sigma^2\) is removed.  In a `211` triple the doubled
corner instead produces the skew factors in the last two rows of (88).
This also shows explicitly why passing through `H/2` loses no Gaussian
prime factor.

The two forced deletions in every remaining one-`F` form are as follows.
Digits in the triple columns are the retained column indices.

| Canonical form | `q`-triple | First comparison | `r`-triple | Second comparison |
| --- | --- | --- | --- | --- |
| `0000/*001/0*10` | `012` | `A2(q,r)` | `013` | `A2(r,q)` |
| `0000/*001/0*11` | `012` | `A2(q,r)` | `123` | `A4(r,q)` |
| `0000/*001/01*0` | `012` | `A2(q,r)` | `023` | `S2(r,q)` |
| `0000/*001/01*1` | `012` | `A2(q,r)` | `123` | `S4(r,q)` |
| `0000/*010/00*1` | `013` | `A4(q,r)` | `012` | `A2(r,q)` |
| `0000/*010/01*0` | `013` | `A4(q,r)` | `023` | `S2(r,q)` |
| `0000/*011/00*1` | `023` | `A2(q,r)` | `012` | `A2(r,q)` |
| `0000/*011/01*1` | `023` | `A2(q,r)` | `123` | `S4(r,q)` |
| `0000/00*1/010*` | `012` | `A4(q,r)` | `023` | `S2(r,q)` |
| `0000/01*0/011*` | `023` | `S2(q,r)` | `123` | `S2(r,q)` |

In every row except the fourth and eighth, (86) simultaneously gives
\(q<r\) and \(r<q\), sometimes with one inequality strengthened to a
square.  In the fourth and eighth rows it gives
\(q^2<r<q^2\).  Thus

\[
 \boxed{\text{No squarefree one-`F` class is arithmetically admissible.}}
                                                               \tag{89}
\]

Together with Sections 5--11, this excludes twenty-four of the twenty-eight
classes in (14).  The exact squarefree residue is therefore

\[
 \boxed{4\text{ physical switching classes, precisely the two-`F` forms
 of Section 12}.}                                  \tag{90}
\]

## 14. The two corner-exception `FF` classes are impossible

The two all-extreme rows can be aligned in a second way.  Coupling the two
exact quotients closes both corner-exception forms left by Section 12.
Continue to write

\[
 P=A+iB,\qquad Q=X+iY,\qquad R=U+iV,\qquad w=\frac R{r^2}.
                                                               \tag{91}
\]

All six coordinates are nonzero, `P,Q,R` are primitive Gaussian integers,
and \(U^2+V^2=r^4\).

### 14.1 The form `0000/0011/*001`

Let \(a_j\in\{1,-1\}\) be the four projection signs.  Aligning first the
`p`-row on columns `0,1,2`, and then the `q`-row on columns `0,1,3`, gives

\[
\begin{aligned}
 a_2\bar Q R-a_0Qr^2-a_1QR&=\mu r^2\bar P,\\
 a_3\bar P R+a_0Pr^2-a_1PR&=m r^2\bar Q .
\end{aligned}                                                   \tag{92}
\]

The first quotient has \(\mu=\mathord\pm1\) by (77).  Negating all signs
if necessary, take \(\mu=1\).  Reduction of the first line modulo `8` leaves
only

\[
 (a_0,a_1,a_2)=(1,-1,1),\quad(-1,1,1),\quad(-1,-1,-1).          \tag{93}
\]

The second aligned triple gives \(m\in\mathbb Z\setminus\{0\}\).  Its
height bound, together with the first one, is

\[
 p^2<3q^2,\qquad |m|q^2<3p^2,
\]

so \(|m|<9\).  The standard fourth-power residues modulo `16` in (92) give
\(p\equiv q\pmod8\) and

\[
 m=a_3+a_0-a_1.
\]

Thus the exhaustive list is

| \(a_0\) | \(a_1\) | \(a_2\) | \(a_3\) | \(m\) |
| ---: | ---: | ---: | ---: | ---: |
| \(1\) | \(-1\) | \(1\) | \(1\) | \(3\) |
| \(1\) | \(-1\) | \(1\) | \(-1\) | \(1\) |
| \(-1\) | \(1\) | \(1\) | \(1\) | \(-1\) |
| \(-1\) | \(1\) | \(1\) | \(-1\) | \(-3\) |
| \(-1\) | \(-1\) | \(-1\) | \(1\) | \(1\) |
| \(-1\) | \(-1\) | \(-1\) | \(-1\) | \(-1\) |

The third and sixth rows are impossible immediately.  In each, the same
nonzero difference \(P-\bar Q\) is a real multiple of both \(w\) and
\(\bar w\), with an extra common factor `i`.  More explicitly, the two
comparisons are, up to simultaneous signs,

\[
 P-\bar Q=2iY\bar w=-2iBw.
\]

They would make \(w/\bar w=R/\bar R\) real.  This is impossible because
both \(U\) and \(V\) are nonzero.

For the first row, (92) and its conjugate become

\[
 P+\bar Q=2\frac X{r^2}\bar R,
 \qquad P-3\bar Q=-2\frac A{r^2}R.                \tag{94}
\]

Taking norms, the second resulting quadratic plus three times the first is
\(4(B^2+3Y^2)=0\), again impossible.  For the fourth row one obtains

\[
 P-\bar Q=2i\frac Y{r^2}\bar R,
 \qquad P-3\bar Q=-2\frac A{r^2}R.                \tag{95}
\]

The two norms and the fact that the product of the left sides is purely
imaginary give

\[
 X(A-X)=0,\qquad B(B+3Y)=0.
\]

Hence \(A=X\) and \(B=-3Y\).  Both
\(X^2+Y^2=q^4\) and \(X^2+9Y^2=p^4\) would then be squares, contrary to the
simultaneous-square lemma used in Sections 8, 9, and 13.

It remains to exclude the two rows with \(m=1\).  The second and fifth rows
of the table respectively give

\[
\begin{array}{c|c|c}
 &\text{first alignment}&\text{second alignment}\\ \hline
 \mathrm{A1}&\bar P+Q=2kR&P-\bar Q=-2i\ell R\\
 \mathrm{A2}&\bar P-Q=2i\ell R&P+\bar Q=2kR,
\end{array}                                                     \tag{96}
\]

where \((k,\ell)=(X/r^2,B/r^2)\) in `A1` and
\((k,\ell)=(A/r^2,Y/r^2)\) in `A2`.  The axis divisibility in the two
alignments shows that these are nonzero integers.  Adding and subtracting
the conjugated identities in (96) gives, respectively,

\[
\begin{array}{c|c|c}
 \mathrm{A1}&P=k\bar R-i\ell R&\bar Q=k\bar R+i\ell R\\
 \mathrm{A2}&P=kR-i\ell\bar R&\bar Q=kR+i\ell\bar R.
\end{array}                                                     \tag{97}
\]

Any common divisor of \(k\) and \(\ell\) would divide both coordinates of
the primitive Gaussian integer `P`; hence \(\gcd(k,\ell)=1\).  Comparing
the coordinate used in the definition of \(k\) or \(\ell\) in (97) gives,
up to sign,

\[
 \frac\ell k=-\frac V{r^2+U}.
\]

The fraction on the right is the reduced half-angle ratio of the primitive
Pythagorean triple \(U^2+V^2=r^4\).  Its reduced numerator and denominator
therefore have square sum \(r^2\).  Since \(\ell/k\) is reduced,

\[
 k^2+\ell^2=r^2.                                  \tag{98}
\]

The parallelogram identity applied to either row of (97) now gives

\[
 p^4+q^4=2r^4(k^2+\ell^2)=2r^6.                  \tag{99}
\]

Consequently

\[
 \left(\frac{p^4-q^4}{2}\right)^2+(pq)^4=(r^3)^4,              \tag{100}
\]

contradicting the Fermat descent lemma \(X^2+Y^4=Z^4\) in Section 2 of
[`two-block-exponent-one.md`](two-block-exponent-one.md).  Thus
`0000/0011/*001` is impossible, and the exact residue drops from four to
three physical classes.

### 14.2 The form `0000/0101/*001`

Normalize the projection sign in column `0` to \(e_0=-1\).  Aligning the
`p`-row on columns `0,1,2` gives a `111` identity, while aligning the
`q`-row on columns `0,2,3` gives a `211` identity:

\[
\begin{aligned}
 e_2QR+Qr^2-e_1\bar Q R&=\mu r^2\bar P,\\
 Pr^2+\frac R2(e_2P-e_3\bar P)&=h r^2\bar Q.
\end{aligned}                                                   \tag{101}
\]

The two height estimates give \(p^2<3q^2\) and
\(|h|q^2<2p^2\), hence \(|h|<6\).  Reduction of the first line modulo `8`
allows only

\[
 (e_1,e_2;\mu)=(-1,-1;1),(1,-1;-1),(1,1;1).
\]

In the second line, \(e_2=e_3\) gives \(h\equiv1\pmod8\),
\((e_2,e_3)=(-1,1)\) gives \(h\equiv0\pmod8\), and
\((e_2,e_3)=(1,-1)\) gives \(h\equiv2\pmod8\).  The middle case would have
\(h=0\); the bound fixes the other two quotients as \(h=1,2\).  Thus there
are exactly four rows:

| \(e_1\) | \(e_2\) | \(e_3\) | \(\mu\) | \(h\) |
| ---: | ---: | ---: | ---: | ---: |
| \(-1\) | \(-1\) | \(-1\) | \(1\) | \(1\) |
| \(1\) | \(-1\) | \(-1\) | \(-1\) | \(1\) |
| \(1\) | \(1\) | \(1\) | \(1\) | \(1\) |
| \(1\) | \(1\) | \(-1\) | \(1\) | \(2\) |

In the first and third rows, conjugating the first identity and comparing it
with the second again writes the same nonzero \(P-\bar Q\) as a real
multiple of \(i\bar R\) and of \(iR\).  Thus \(R/\bar R\) would be real,
which is impossible.

For the second row, put \(x=X/r^2\) and \(b=B/r^2\).  Equations (101) are

\[
 \bar P+Q=2xR,\qquad P-\bar Q=ibR.                \tag{102}
\]

After conjugating the first equation, the product
\((P+\bar Q)(P-\bar Q)\) is purely imaginary, so

\[
 A^2-B^2=X^2-Y^2.                                 \tag{103}
\]

On the other hand, the parallelogram identity and (102) give

\[
 4X^2+B^2=|P+\bar Q|^2+|P-\bar Q|^2
          =2p^4+2q^4.
\]

Substitution of (103) reduces this to \(3B^2=0\), a contradiction.

For the last row, equations (101), after conjugating the first, are

\[
 P-\bar Q=-2i\frac Y{r^2}\bar R,
 \qquad P-2\bar Q=-\frac A{r^2}R.                 \tag{104}
\]

Set \(u=A-X\) and \(v=B+Y\).  The two norms and the vanishing real part of
the product in (104) become

\[
 u^2+v^2=4Y^2,\qquad (v+Y)^2=4uX,\qquad
 u(u-X)=v(v+Y).
\]

Eliminating \(uX\) gives

\[
 3v^2+2vY-5Y^2=(v-Y)(3v+5Y)=0.
\]

If \(v=Y\), the first norm says \(u^2=3Y^2\); if
\(v=-5Y/3\), it says \(u^2=11Y^2/9\).  Both are impossible for nonzero
rational \(u,Y\).  This excludes the fourth row and hence the entire form
`0000/0101/*001`.

The exact squarefree residue is now

\[
 \boxed{2\text{ physical switching classes, the edge-exception forms }
  \texttt{0000/0011/01*0}\text{ and }\texttt{0000/0101/00*1}.} \tag{105}
\]

## 15. The sole `211` `FF` class is impossible

Consider `0000/0011/01*0` and again normalize the column-`0` projection
sign to \(e_0=-1\).  The `p`-aligned `211` identity on columns `0,2,3`
is

\[
 e_2\bar Qr^2+e_3\bar QR+2QR=2\mu r^2\bar P.       \tag{106}
\]

Modulo `8`, (106) forces \(e_3=-e_2\) and \(\mu=1\).  Put
\(s=e_2\).  The identity is therefore

\[
 2r^2\bar P=2QR+s\bar Q(r^2-R).                   \tag{107}
\]

Its reduction modulo `16` also forces \(r\equiv1\pmod8\): if the
fourth-power residue above `r` is the nontrivial one, the last bracket in
(107) contributes a nonzero imaginary residue `8`, while all other terms
agree.

Align the `q`-row by conjugating columns `2,3`.  The same-oriented
`r`-triple is now the `211` triple on columns `1,2,3`, and its exact
quotient identity is

\[
 -e_2\bar Pr^2+e_3\bar P\bar R-2e_1P\bar R
     =2h r^2\bar Q.                               \tag{108}
\]

The two strict height bounds are

\[
 p^2<2q^2,\qquad |h|q^2<2p^2,
\]

so \(|h|<4\).  Since \(r\equiv1\pmod8\), division of (108) by `2`
and reduction modulo `8` gives

\[
 h\equiv-(e_1+s)\pmod8.
\]

The quotient is nonzero.  Hence \(e_1=s\) and \(h=-2s\).  Substitution
in (108) removes the sign altogether:

\[
 \bar P(r^2+\bar R)+2P\bar R=4r^2\bar Q.          \tag{109}
\]

Put \(w=R/r^2\), \(t=\bar w\), and \(z=Q/\bar Q\).  Thus
\(|t|=|z|=1\).  Equation (107), its conjugate, and (109) become

\[
 2P-sQ=t(2\bar Q-sQ),\qquad
 \bar P(1+t)+2Pt=4\bar Q.                         \tag{110}
\]

Eliminate `P` from (110) and divide by \(\bar Q\).  For the two values of
`s` this gives

\[
\begin{aligned}
 s=1:\quad
 z&=\frac{4t^3+t^2-8t-1}{2(t^3-t^2-t-1)},\\
 s=-1:\quad
 z&=-\frac{4t^3-t^2-8t+1}{2(t^3-t^2+t+1)}.
\end{aligned}                                                    \tag{111}
\]

Neither denominator vanishes on the unit circle.  Indeed, either vanishing
condition can be written

\[
 t^2(t-1)=\mathord\pm(t+1).
\]

Taking absolute values gives \(|t-1|=|t+1|\), hence
\(\operatorname{Re}t=0\) and \(t=\mathord\pm i\).  Direct substitution
excludes both values.

Finally use \(\bar t=1/t\) in \(z\bar z=1\).  Subtracting `1` from the
norm of the two expressions in (111) and factoring gives, respectively,

\[
 \frac{33t(t-1)^2(t+1)^2}
 {4(t^3-t^2-t-1)(t^3+t^2+t-1)}=0,                 \tag{112}
\]

and

\[
 -\frac{33t(t-1)^2(t+1)^2}
 {4(t^3-t^2+t+1)(t^3+t^2-t+1)}=0.                 \tag{113}
\]

The denominators are nonzero, and \(t\ne0\), so both cases force
\(t=\mathord\pm1\).  This would make the primitive one-sided fourth power
`R` axis-parallel, which is impossible.  Thus `0000/0011/01*0` is
excluded.

The exact squarefree residue is now the single edge-exception `111` form

\[
 \boxed{\texttt{0000/0101/00*1}.}                 \tag{114}
\]

## 16. The final `FF` class is impossible

It remains to exclude `0000/0101/00*1`.  With \(e_0=-1\), aligning the
`p`-row on columns `0,1,2` and the `q`-row on columns `0,2,3` gives

\[
\begin{aligned}
 e_2Qr^2+QR-e_1\bar QR&=\mu r^2\bar P,\\
 e_2Pr^2-e_3\bar PR+2PR&=2h r^2\bar Q.
\end{aligned}                                                   \tag{115}
\]

Here \(h\in\mathbb Z\setminus\{0\}\).  The strict height estimates are
\(p^2<3q^2\) and \(|h|q^2<2p^2\), so \(|h|<6\).  The same modulo-`8`
calculation as in Section 14.2 leaves exactly

| \(e_1\) | \(e_2\) | \(e_3\) | \(\mu\) | \(h\) |
| ---: | ---: | ---: | ---: | ---: |
| \(-1\) | \(-1\) | \(-1\) | \(1\) | \(1\) |
| \(1\) | \(-1\) | \(-1\) | \(-1\) | \(1\) |
| \(1\) | \(1\) | \(1\) | \(1\) | \(1\) |
| \(1\) | \(1\) | \(-1\) | \(1\) | \(2\) |

Indeed, the first line of (115) allows only
\((e_1,e_2;\mu)=(-1,-1;1),(1,-1;-1),(1,1;1)\).  In the second,
\(e_2=e_3\) gives \(h=1\), the pair \((-1,1)\) would give \(h=0\), and
the pair \((1,-1)\) gives \(h=2\).  Reduction modulo `16` also gives
\(p\equiv q\pmod8\) and \(r\equiv1\pmod8\).

Put \(w=R/r^2\).  The four rows of the table are, in order,

\[
\begin{array}{c|c|c}
 &\text{first alignment}&\text{second alignment}\\ \hline
 \mathrm{R}&\bar P+Q=2Xw&P+2\bar Q=(\bar P+2P)w\\
 \mathrm{M1}&\bar P-Q=-2iYw&P+2\bar Q=(\bar P+2P)w\\
 \mathrm{I}&\bar P-Q=2iYw&P-2\bar Q=(\bar P-2P)w\\
 \mathrm{M2}&\bar P-Q=2iYw&4\bar Q-P=(\bar P+2P)w.
\end{array}                                                     \tag{116}
\]

The two mixed rows are impossible by a short unit-circle calculation.  Put
\(t=\bar w\) and \(z=Q/\bar Q\).  Conjugate the first identity in each
mixed row, use it to eliminate `P` from the second, and divide by
\(\bar Q\).  The two results are

\[
\begin{aligned}
 \mathrm{M1}:\quad
 z&=\frac{t^3-5t^2+2t+1}{t^3-2t^2-t+1},\\
 \mathrm{M2}:\quad
 z&=\frac{t^3-t^2+2t-1}{t^3+2t^2-t-1}.
\end{aligned}                                                   \tag{117}
\]

The denominators do not vanish for \(|t|=1\).  For `M1`, combining a
vanishing denominator with its reciprocal conjugate would force \(t=1\),
which is not a root.  For `M2`, a vanishing denominator would give
\(|t+2|=|t+1|\), hence \(\operatorname{Re}t=-3/2\), contradicting
\(|t|=1\).
Using \(\bar t=1/t\) and \(|z|=1\), the two norm differences factor as

\[
\begin{aligned}
 \mathrm{M1}:\quad |z|^2-1
 &=-\frac{12t^2(t-1)^2}
 {(t^3-2t^2-t+1)(t^3-t^2-2t+1)},\\
 \mathrm{M2}:\quad |z|^2-1
 &=-\frac{6t(t-1)^2(t^2+t+1)}
 {(t^3+2t^2-t-1)(t^3+t^2-2t-1)}.
\end{aligned}                                                   \tag{118}
\]

The first line forces \(t=1\), which would make `R` real.  The second
forces the same alternative or \(t^2+t+1=0\); the latter has no root in
\(\mathbb Q(i)\), whereas \(t=\bar R/r^2\in\mathbb Q(i)\).  Thus only
the real row `R` and imaginary row `I` of (116) remain.

Write

\[
 \sigma^2=C+iD,\qquad C^2+D^2=r^2,\qquad
 R=(C+iD)^2.                                      \tag{119}
\]

Here \(\gcd(C,D)=1\), \(C\) is odd, \(4\mid D\), and both coordinates are
nonzero.  In the real row, conjugating the first identity in (116) gives
\(P=2X\bar w-\bar Q\), hence

\[
 A=\frac{X(C^2-3D^2)}{r^2},\qquad
 B=Y-\frac{4CDX}{r^2}.
\]

Substitution in the second identity reduces both its coordinates to the
single equation

\[
 Cr^2Y=DX(5D^2-3C^2).                            \tag{120}
\]

The numerator and denominator of
\(Y/X=D(5D^2-3C^2)/(Cr^2)\) have gcd
\(g_R=\gcd(C,5)\).  Indeed, the gcd at `C` is exactly \(g_R\), while
modulo `r` the bracket is \(8D^2\ne0\).  Primitivity of `Q` therefore
fixes, up to a simultaneous sign,

\[
 (A,B,X,Y)=\frac1{g_R}
 \bigl(C(C^2-3D^2),\ D(5D^2-7C^2),\ Cr^2,\
       D(5D^2-3C^2)\bigr).                        \tag{121}
\]

In particular,

\[
 \pi^4+\bar\rho^4=P+\bar Q
   =\mathord\pm\frac{2C}{g_R}\bar\sigma^4
   =(\pi^2+i\bar\rho^2)(\pi^2-i\bar\rho^2).     \tag{122}
\]

The rational coefficient is an `r`-unit.  The two factors on the right are
coprime at \(\bar\sigma\): a common divisor would divide both
\(2\pi^2\) and \(2\bar\rho^2\).  Hence one factor contains all of
\(\bar\sigma^4\), and

\[
 r^4\le N(\pi^2\mathord\pm i\bar\rho^2)
       \le(p+q)^2\le4p^2.                         \tag{123}
\]

For the imaginary row, the first identity gives

\[
 A=X-\frac{4CDY}{r^2},\qquad
 B=-\frac{Y(3C^2-D^2)}{r^2},
\]

and the second reduces to

\[
 Dr^2X=CY(5C^2-3D^2).                             \tag{124}
\]

Now the reduced gcd is \(g_I=\gcd(D,5)\); modulo `r` the relevant bracket
is \(8C^2\ne0\).  Thus

\[
 (A,B,X,Y)=\frac1{g_I}
 \bigl(C(5C^2-7D^2),\ D(D^2-3C^2),\
       C(5C^2-3D^2),\ Dr^2\bigr),                 \tag{125}
\]

up to a simultaneous sign, and

\[
 \pi^4-\bar\rho^4=P-\bar Q
  =\mathord\pm\frac{2Di}{g_I}\bar\sigma^4
  =(\pi-\bar\rho)(\pi+\bar\rho)(\pi^2+\bar\rho^2).
                                                               \tag{126}
\]

The three factors are pairwise coprime at \(\bar\sigma\): if
\(\bar\sigma\) divided a linear factor and the quadratic factor, substituting
\(\pi\equiv\mathord\pm\bar\rho\pmod{\bar\sigma}\) in the latter would give
\(2\bar\rho^2\equiv0\pmod{\bar\sigma}\), which is impossible.  Thus one
factor contains all of \(\bar\sigma^4\); here too the displayed rational
coefficient is an `r`-unit.  If it is a linear factor, then

\[
 r^4\le N(\pi\mathord\pm\bar\rho)
       \le(\sqrt p+\sqrt q)^2\le4p.               \tag{127}
\]

If it is the quadratic factor, (123) holds instead.

It remains only to compare these factor bounds with the exact coordinate
height.  Let \(F_R,F_I\) be the numerators of \(g_R^2p^4\) and
\(g_I^2p^4\) in (121) and (125).  Direct expansion gives

\[
\begin{aligned}
 25r^6-F_R
 &=8C^2(3C^4+4C^2D^2+17D^4)>0,\\
 25r^6-F_I
 &=8D^2(17C^4+4C^2D^2+3D^4)>0.
\end{aligned}                                                   \tag{128}
\]

Thus in either row

\[
 p^4<25r^6,\qquad p^2<5r^3.                       \tag{129}
\]

The linear case of (127) would give \(r^8\le16p^2<80r^3\), hence
\(r^5<80\), impossible for the odd prime `r`.  In every remaining case,
(123) and (129) give
\(r^4<20r^3\), hence \(r<20\).  Since already \(r\equiv1\pmod8\), one
must have \(r=17\).  The primitive representation in (119) is then

\[
 |C|=15,\qquad |D|=8.                             \tag{130}
\]

For the real row, \(g_R=5\) and (121) gives

\[
 p^4=4{,}041{,}865,\qquad
 44^4<p^4<45^4.
\]

For the imaginary row, \(g_I=1\) and (125) gives

\[
 p^4=127{,}016{,}569,\qquad
 106^4<p^4<107^4.
\]

Neither value is a fourth power.  This final contradiction empties the
squarefree residue:

\[
 \boxed{\text{No squarefree three-prime class is arithmetically
 admissible.}}                                      \tag{131}
\]

## 17. Block transfer for arbitrary balanced/extreme exponents

The squarefree notation in Sections 3--16 hides a useful invariance.  Let

\[
 e=p^kq^\ell r^m,
 \qquad \mathsf P=p^k,\quad \mathsf Q=q^\ell,\quad
 \mathsf R=r^m,
\]

where the rational primes are distinct.  Choose Gaussian primes above them
and put

\[
 \Pi=\pi^k,\qquad \varrho=\rho^\ell,\qquad \Sigma=\sigma^m.
\]

For a block \(s^a\), let \(j_{s,c}\in[-a,a]\) be the local index of offset
column `c` in the notation of [`block-balance.md`](block-balance.md).  Assume
in this section that every local index is balanced or extreme.  Thus, for
some \(b_{s,c}\in\{0,\mathord\pm1\}\),

\[
 j_c=(k b_{p,c},\ell b_{q,c},m b_{r,c}).           \tag{132}
\]

The following elementary block facts are all that the squarefree arithmetic
uses.

- A one-sided Gaussian prime power such as \(\Pi\), and any product of such
  powers on disjoint rational-prime supports, is primitive.  It cannot be
  real or purely imaginary.  Otherwise a rational prime would occur at both
  conjugate Gaussian supports, contradicting unique factorization.
- If \(\Theta=\tau^a\) and \(T=s^a=N(\Theta)\), then
  \(\Theta^2=X+iY\) has coprime nonzero coordinates, with `X` odd and
  \(4\mid Y\) after the usual harmless choice of orientation.  Moreover,

  \[
   \Theta^4\equiv
   \begin{cases}
    1,&T\equiv1\pmod8,\\
    9+8i,&T\equiv5\pmod8
   \end{cases}
   \pmod{16\mathbb Z[i]}.                          \tag{133}
  \]

  This follows by writing \(\Theta=u+iv\), where `u,v` have opposite
  parity.  Every center prime is \(1\pmod4\), so these are the only two
  block-norm residues modulo `8`.
- If \(\Theta^d\mid n\) for a rational integer `n`, conjugation also gives
  \(\bar\Theta^d\mid n\).  Since the two factors are coprime,
  \(T^d\mid n\).  The same support argument shows that all coordinate
  fractions used below remain reduced after replacing a Gaussian prime by
  its one-sided power.

The normalized squared direction of column `c` is still, up to sign,

\[
 \prod_{s\in\{p,q,r\}}
 \left(\frac{\pi_s}{\bar\pi_s}\right)^{2j_{s,c}}.
\]

Unique factorization says that two absolute directions agree exactly when
their weighted vectors in (132) are equal up to a global sign.  Since the
weight matrix \(\operatorname{diag}(k,\ell,m)\) is invertible over the
rationals, this is equivalent to

\[
 b_c=\mathord\pm b_d.
\]

Thus the nonzero/distinctness test (12), the incoherence test (10), and the
entire binary classification of Section 4 are unchanged.  Exponent labels
may split an orbit if one insists on fixing a distinguished row before
quotienting, but they create no new bit matrix: after relabeling the three
actual blocks, every labeled class lies over one of the same 28 physical
classes.

Here is the section-by-section arithmetic audit.  In every row, make the
uniform substitution

\[
 (p,q,r;\pi,\rho,\sigma)
 \longmapsto
 (\mathsf P,\mathsf Q,\mathsf R;\Pi,\varrho,\Sigma).
\]

| Sections | What has to be checked | Why the proof is block-generic |
| --- | --- | --- |
| 5--7 | Rational phases and reduced coordinates | Replace \(\pi^4/p^2\) by \(\Pi^4/\mathsf P^2\), and similarly in the other rows.  Disjoint one-sided products are primitive; reduction modulo the underlying Gaussian prime shows that their cross-coordinate is coprime to the full block denominator.  The terminal equation is \((\mathsf P\mathsf Q)^4+S^2=\mathsf R^4\), so the same rational quartic applies. |
| 8--11 | Half-angle slopes, factors `2` and `3`, and quartic norms | The primitive block squares \(\Pi^2\), \(\varrho^2\Sigma^2\), and their conjugate variants have exactly the parity and coprimality used there.  Cancelling at most `3`, or exactly the displayed factor `2`, is unchanged.  The simultaneous-square and quartic lemmas are statements about arbitrary nonzero integers. |
| 12 | Integral quotient rigidity | A balanced residual factor is \(\mathsf R^2=\Sigma^2\bar\Sigma^2\), while an extreme one is \(\Sigma^4\).  Hence \(\Sigma^2\mid n\), rationality gives \(\mathsf R^2\mid n\), and the same height bounds force \(n=\mathord\pm\mathsf R^2\) after ordering \(\mathsf P\ge\mathsf Q\). |
| 13 | The four divisor comparisons | Use the block comparison lemma below.  The two forced row deletions therefore give the same contradictory strict inequalities between \(\mathsf Q\) and \(\mathsf R\). |
| 14--15 | Coupled quotients, congruences, and unit-circle elimination | The displayed Gaussian identities are homogeneous in the three balanced factors and fourth powers.  Equation (133), the block height bounds, primitivity, and the rational unit-circle arguments reproduce every sign row and every contradiction verbatim.  In (98)--(100), for example, one obtains \(k_0^2+\ell_0^2=\mathsf R^2\) and \(\mathsf P^4+\mathsf Q^4=2\mathsf R^6\), followed by the same Fermat descent. |
| 16 | UFD factor placement and the final height | The only apparent use of a prime rather than a block is the last small-value step; it is checked separately below. |

For completeness, the generalized comparison lemma used in the Section-13
row is immediate.  Let \(T=t^a\), \(S=s^b\),
\(\mathrm B=\beta^a\), \(\Theta=\tau^b\), and
\(Z=\Theta^2=X+iY\), with the two rational-prime supports distinct.  The
same proofs as for (86) give

\[
\begin{aligned}
 \mathrm B^2\mid\bar Z\mathbin\pm Z
   &\Longrightarrow T^2<S,&
 \mathrm B^2\mid\bar Z^2\mathbin\pm Z^2
   &\Longrightarrow T<S,\\
 \mathrm B^2\mid2\bar Z\mathbin\pm Z
   &\Longrightarrow T<S,&
 \mathrm B^2\mid2\bar Z^2\mathbin\pm Z^2
   &\Longrightarrow T<S^2.
\end{aligned}                                                     \tag{134}
\]

For the axis-parallel expressions, conjugation makes \(T^2\) divide the
corresponding nonzero coordinate.  For a skew expression its norm is
\(9X^2+Y^2\) or \(X^2+9Y^2\).  If the asserted strict inequality failed,
division by \(T^2\) would leave a positive integer smaller than `9` and
congruent to `1` modulo `8`; it would be `1`, contradicting the same
simultaneous-square lemma.  Applying this to \(Z^2\) proves the two
fourth-power versions.

It remains to audit the endpoint of Section 16.  Interpret its `P,Q,R` as
\(\Pi^4,\varrho^4,\Sigma^4\) and write
\(\Sigma^2=C+iD\).  The coordinate gcd calculations are unchanged.  In
particular, neither `C` nor `D` is divisible by the underlying prime `r`,
and modulo `r` the two relevant brackets are \(8D^2\) and \(8C^2\).
Thus the rational coefficients in the analogues of (122) and (126) are
`r`-units.  Pairwise coprimality at \(\bar\sigma\) places all of
\(\bar\Sigma^4=\bar\sigma^{4m}\) in one factor of

\[
 \Pi^4+\bar\varrho^4
  =(\Pi^2+i\bar\varrho^2)(\Pi^2-i\bar\varrho^2)
\]

or

\[
 \Pi^4-\bar\varrho^4
  =(\Pi-\bar\varrho)(\Pi+\bar\varrho)
    (\Pi^2+\bar\varrho^2).
\]

Consequently the exact transferred bounds are

\[
 \mathsf P^4<25\mathsf R^6,\qquad
 \mathsf R^4\le4\mathsf P^2
 \quad\text{or, for a linear factor,}\quad
 \mathsf R^4\le4\mathsf P.                       \tag{135}
\]

The linear alternative gives \(\mathsf R^5<80\), impossible because
\(\mathsf R\ge5\).  The quadratic alternative gives
\(\mathsf R<20\).  The sign audit still gives
\(\mathsf R\equiv1\pmod8\).  Since
\(\mathsf R=r^m\), \(r\equiv1\pmod4\), and a power with \(m\ge2\) is at
least \(5^2=25\), the only possibility is
\(\mathsf R=r=17\).  Hence the representation (130) and the two numerical
values following it are literally unchanged, except that their left side
is now \(\mathsf P^4\).  Each lies strictly between consecutive fourth
powers, although \(\mathsf P\) is an integer.  This is the same final
contradiction.

We have therefore proved the block form of the squarefree result.  If the
center root of a hypothetical primitive square is
\(e=p^kq^\ell r^m\), supported on exactly three distinct rational primes,
and every local index at each of the four offsets is either zero or extreme,
then

\[
 \boxed{\text{no such square is admissible.}}       \tag{136}
\]

For \(e=p^2qr\), the `q`- and `r`-indices automatically satisfy this
hypothesis.  At least three `p`-indices are extreme.  The theorem excludes
both an all-extreme `p`-row and a balanced exceptional `p`-row.  Therefore
any still-hypothetical center of this shape would have to satisfy

\[
 \boxed{\text{the unique nonextreme \(p\)-index is }j_p=\mathord\pm1.}
                                                               \tag{137}
\]

This corollary also states the exact remaining scope: genuine intermediate
indices, not higher exponents by themselves, are what the present
three-block argument does not cover.

## 18. Reproduction

```sh
python3 three_block_signatures.py
python3 three_block_squarefree.py
python3 -m unittest -v \
  test_three_block_signatures.py test_three_block_squarefree.py
```

The tests check the coarse incidence-only classification, the
`384 -> 48 -> 2` all-unit reduction, every physical mask count, and explicit
collision, Hadamard, and zero-column examples for (12).  They also pin the
twenty-four canonical forms excluded in Sections 5--11 and 13.  Sections
14--16 are exact proof-only Gaussian, unit-circle, and height descents, and
Section 17 is their proof-only block transfer.  The tests do not purport to
mechanize those arguments.
