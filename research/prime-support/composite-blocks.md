# Composite Gaussian block balance

## Status

This note records two strengthenings of the prime-power block bound in
[block-balance.md](block-balance.md).  Several rational prime-power blocks can
be grouped whenever their local Gaussian orientations separate into a row
sign and a column sign.  More generally, the exact common Gaussian divisor of
any three-offset relation gives a necessary monomial height inequality, with
no unit-index or separability hypothesis; using the same divisor across all
four offsets sharpens its normalized right side to one.  These are reusable
lemmas, not a global nonexistence proof.

## Setup

Let a hypothetical primitive magic square have center \(e^2\) and four
pairwise distinct positive offsets

\[
\mathcal D=\{a,b,a+b,|a-b|\}.
\]

Choose a three-element subset \(T=\{d_1,d_2,d_3\}\) and its relation

\[
c_1d_1+c_2d_2+c_3d_3=0,
\tag{1}
\]

whose coefficient magnitudes are either \(\{1,1,1\}\) or
\(\{2,1,1\}\).  Encode \(d_s\) by \(z_s\in\mathbb Z[i]\), with

\[
N(z_s)=e^2,\qquad d_s=|\operatorname{Im}(z_s^2)|.
\]

Let \(\mathcal B\) be a set of distinct prime-power blocks
\(p_r^{k_r}\mathrel\Vert e\) for which all three offsets in \(T\) are
\(p_r\)-adic units.  Fix \(p_r=\pi_r\bar\pi_r\).  The local valuation
spectrum then says that \(z_s\) contains either \(\pi_r^{2k_r}\) or
\(\bar\pi_r^{2k_r}\).  Record this choice by a bit \(b_{r,s}\).

The orientation matrix is *affinely separable* if

\[
b_{r,s}=u_r+v_s\pmod2
\tag{2}
\]

for some row bits \(u_r\) and column bits \(v_s\).  Equivalently, every
rectangular parity vanishes:

\[
b_{r,s}+b_{r,t}+b_{r',s}+b_{r',t}=0\pmod2.
\tag{3}
\]

In multiplicative \(\{\pm1\}\)-notation this says that the sign matrix is an
outer product of a row-sign vector and a column-sign vector.  Calling (2)
“rank one over \(\mathbb F_2\)” would be inaccurate: affine separability, not
ordinary matrix rank, is the required property.

Set

\[
A=\prod_{r\in\mathcal B}p_r^{k_r},
\qquad M=\frac eA.
\]

## Composite-block lemma

If the orientation matrix is affinely separable, then

\[
\boxed{A^2<3M^2.}
\tag{4}
\]

For a relation of coefficient type \(\{2,1,1\}\), the stronger bound is

\[
\boxed{A^2<2M^2.}
\tag{5}
\]

The integral forms are \(A^2\le3M^2-2\) and \(A^2\le2M^2-1\),
respectively.  If \(A>M\), the Gaussian relation below is forced to have
integer quotient of absolute value one.

### Proof

Replace \(\pi_r\) by \(\bar\pi_r\) according to the row bit \(u_r\), and
conjugate \(z_s\) according to the column bit \(v_s\).  Conjugation preserves
the absolute imaginary part.  Condition (2) now gives the common factor

\[
\Pi=\prod_{r\in\mathcal B}\pi_r^{2k_r}
\]

and representations

\[
z_s=\varepsilon_s\Pi w_s,\qquad N(w_s)=M^2.
\]

Put \(G_s=\varepsilon_s^2w_s^2\).  Absorb the sign of
\(\operatorname{Im}(\Pi^2G_s)\) into \(c_s\) in (1), and set

\[
H=c_1G_1+c_2G_2+c_3G_3.
\]

Then

\[
\operatorname{Im}(\Pi^2H)=0.
\tag{6}
\]

The same equal-vector and cube-root arguments as in the one-block proof show
that \(H\ne0\); pairwise distinctness of the offsets is used here.  Since
\(\Pi^2H\) is a nonzero rational integer and the Gaussian primes in \(\Pi\)
are coprime to their conjugates, equality of conjugate valuations gives

\[
\bar\Pi^2\mid H.
\]

In fact the quotient is rational:

\[
H=\bar\Pi^2n,\qquad n\in\mathbb Z\setminus\{0\},
\tag{7}
\]

because \(\Pi^2H=A^4n\) is real.  In coefficient type
\(\{1,1,1\}\), the integer \(n\) is odd.  Indeed, \(M\) is odd, so every
\(w_s\) has coordinates of opposite parity and hence
\(G_s\equiv1\pmod{2\mathbb Z[i]}\).  The three odd coefficients give
\(H\equiv1\pmod{2\mathbb Z[i]}\), while
\(\bar\Pi^2\equiv1\pmod{2\mathbb Z[i]}\) because every Gaussian prime above
an odd rational prime has fourth power congruent to one.  Therefore
\(n\equiv1\pmod2\), and

\[
A^2|n|=|H|<3M^2.
\]

This proves (4).  In coefficient type \(\{2,1,1\}\), parity gives
\(H\in2\mathbb Z[i]\); applying the same argument to \(H/2\) gives

\[
\frac H2=\bar\Pi^2n,\qquad A^2|n|<2M^2,
\]

and proves (5).  The integral and dominant-block statements follow exactly
as in the one-block case.

## Four-offset corollary

Suppose every offset in \(\mathcal D\) is a local unit at every block in
\(\mathcal B\), and suppose the orientation matrix with all four offset
columns is affinely separable.  Then

\[
\boxed{A<M.}
\tag{8}
\]

Indeed, the row and column conjugations in the lemma orient all four
encodings with the same factor \(\Pi\).  After changing the sign of each
residual square, write \(F_x\) so that
\(\operatorname{Im}(\Pi^2F_x)=x\) for
\(x\in\{a,b,c=a+b,d=|a-b|\}\), taking \(a>b\).  The two
coefficient-\(\{1,1,1\}\) relations give

\[
F_c-F_a-F_b=\bar\Pi^2n_1,
\qquad
F_d-F_a+F_b=\bar\Pi^2n_2
\]

with nonzero odd integers \(n_1,n_2\).  The two coefficient-
\(\{2,1,1\}\) relations are the half-sum and half-difference of these
Gaussian integers.  Both are nonzero by distinctness, so
\(n_1\ne\pm n_2\) and
\(\max(|n_1|,|n_2|)\ge3\).  The strict three-term estimate now gives

\[
3A^2\le A^2\max(|n_1|,|n_2|)<3M^2,
\]

which proves (8).  This uses affine separability across all four columns;
separability for only one selected triple is not enough.

## Arbitrary-triple common-factor lemma

The preceding argument has a useful form that does not require any block to
be a local unit.  Primitivity makes every center prime odd and split, so
write

\[
e=\prod_{r\in\mathcal P}p_r^{k_r},
\qquad p_r=\pi_r\bar\pi_r.
\]

For each retained column \(u\in T\), let \(j_{r,u}\) be its local index at
the block \(p_r^{k_r}\).  Independently replace each \(z_u\) by either \(z_u\)
or \(\bar z_u\).  This changes all indices in that column by the same sign;
write the resulting indices as \(j'_{r,u}\).  After multiplying each squared
encoding by a rational sign so that (1) becomes a relation between imaginary
parts, the corresponding Gaussian integers have the form

\[
Y_u=\omega_u\prod_{r\in\mathcal P}
 \pi_r^{\,2k_r+2j'_{r,u}}
 \bar\pi_r^{\,2k_r-2j'_{r,u}},
\qquad \omega_u\in\{\pm1\},
\qquad |Y_u|=e^2.                                \tag{9}
\]

Define the two coordinatewise minima

\[
a_r=\min_{u\in T}(2k_r+2j'_{r,u}),
\qquad
b_r=\min_{u\in T}(2k_r-2j'_{r,u}),              \tag{10}
\]

and put

\[
\begin{split}
D&=\prod_{r\in\mathcal P}p_r^{\min(a_r,b_r)},\\
\Pi&=
 \prod_{a_r>b_r}\pi_r^{\,a_r-b_r}
 \prod_{b_r>a_r}\bar\pi_r^{\,b_r-a_r},\\
F&=\prod_{r\in\mathcal P}\pi_r^{a_r}\bar\pi_r^{b_r}
  =D\Pi.
\end{split}                                      \tag{11}
\]

Then \(F\) is the exact common Gaussian monomial in the three \(Y_u\).  If
\(R_u=Y_u/F\) and

\[
H=\sum_{u\in T}c_uR_u,
\]

then (1) gives

\[
\operatorname{Im}(\Pi H)=0.                     \tag{12}
\]

For coefficient type \(\{1,1,1\}\) one consequently has

\[
H=\bar\Pi n,
\qquad n\in\mathbb Z\setminus\{0\}.
\]

For coefficient type \(\{2,1,1\}\), one has instead

\[
\frac H2=\bar\Pi n,
\qquad n\in\mathbb Z\setminus\{0\}.             \tag{13}
\]

In particular, every choice of the three individual column conjugations
satisfies the strict bounds

\[
\boxed{D\,N(\Pi)<3e^2}\quad(111),
\qquad
\boxed{D\,N(\Pi)<2e^2}\quad(211).                \tag{14}
\]

Equivalently, after division by \(e^2=\prod_r p_r^{2k_r}\),

\[
\boxed{
 \prod_{r\in\mathcal P}
 p_r^{\,\max(a_r,b_r)-2k_r}<3}
 \quad(111),
\qquad
\boxed{
 \prod_{r\in\mathcal P}
 p_r^{\,\max(a_r,b_r)-2k_r}<2}
 \quad(211).                                     \tag{15}
\]

The exponents in (15) may be negative.  For a fixed deleted column there are
only four distinct conjugation patterns: simultaneous conjugation of all
three retained columns exchanges every \(a_r\) with \(b_r\) and leaves (15)
unchanged.

### Proof

Equation (11) and unique factorization show that \(F\mid Y_u\) for all three
columns.  Since \(D\) is rational, the original imaginary-part relation is
exactly (12).  Thus \(\Pi H\) is a rational Gaussian integer.  Every prime
dividing the one-sided integer \(\Pi\) also divides this rational integer;
equality of conjugate valuations therefore shows that \(N(\Pi)\mid\Pi H\).
It follows that \(H=\bar\Pi n\) with \(n\in\mathbb Z\).

For a `211` relation, \(H/2\) is still a Gaussian integer.  Indeed, every
\(Y_u\) is congruent to \(1\) modulo \(2\mathbb Z[i]\), while the common
factor \(F\), having odd norm, is invertible modulo \(2\mathbb Z[i]\).
Consequently all three \(R_u\) have the same residue modulo
\(2\mathbb Z[i]\), and the two odd-coefficient terms cancel there.  Applying
the preceding rationality argument to \(H/2\) proves (13).

All three residual terms have the same modulus

\[
|R_u|=\frac{e^2}{|F|}
     =\frac{e^2}{D\sqrt{N(\Pi)}}.
\]

The standard equal-vector argument makes the relevant sum nonzero and the
triangle bound strict.  In type `111`, a zero sum would require a nonreal
cube root of unity in \(\mathbb Q(i)\).  In type `211`, equality or vanishing
would force the two unit-coefficient terms to encode the same absolute
offset, contrary to pairwise distinctness.  Hence

\[
|H|<\frac{3e^2}{D\sqrt{N(\Pi)}}
\quad(111),
\qquad
\left|\frac H2\right|
 <\frac{2e^2}{D\sqrt{N(\Pi)}}
\quad(211).
\]

Substitution of (13), or its `111` analogue, proves (14).  Finally,

\[
D\,N(\Pi)=\prod_{r\in\mathcal P}p_r^{\max(a_r,b_r)},
\]

which gives (15).

The composite-block bounds (4) and (5) are recovered as a special case.  A
selected aligned unit block contributes \(p_r^{2k_r}\) to the left side of
(15), while every unselected block contributes at least \(p_r^{-2k_r}\).
Thus that left side is at least \(A^2/M^2\).

## Arbitrary-four-offset corollary

Apply the same construction simultaneously to all four columns in
\(\mathcal D\): after independently conjugating their encodings, take the
minima (10) over all four columns and define \(D,\Pi,F\) by (11).  Then

\[
\boxed{D\,N(\Pi)<e^2}.                           \tag{16}
\]

Equivalently, every four-column conjugation pattern satisfies

\[
\boxed{
 \prod_{r\in\mathcal P}
 p_r^{\,\max(a_r,b_r)-2k_r}<1}.                 \tag{17}
\]

There are eight distinct patterns to check, because simultaneous conjugation
of all four columns leaves (17) unchanged.  No local-unit or affine-
separability assumption is needed.

### Proof

For \(x\in\{a,b,c=a+b,d=a-b\}\), with \(a>b\), choose the rational sign of
the conjugated square \(Y_x\) so that \(\operatorname{Im}(Y_x)=x\), and write
\(Y_x=FR_x=D\Pi R_x\).  Thus

\[
D\,\operatorname{Im}(\Pi R_x)=x.
\]

The two \(111\) relations give

\[
H_1=R_c-R_a-R_b=\bar\Pi n_1,
\qquad
H_2=R_d-R_a+R_b=\bar\Pi n_2,                    \tag{18}
\]

where the rationality argument above makes \(n_1,n_2\) nonzero integers.
They are odd: all four \(R_x\) have the same nonzero residue modulo
\(2\mathbb Z[i]\), so each \(H_i\) has that residue, whereas \(\bar\Pi\) is
invertible modulo \(2\mathbb Z[i]\).

The half-sum and half-difference are the two \(211\) relations

\[
\frac{H_1+H_2}{2}
 =\frac{R_c+R_d-2R_a}{2},
\qquad
\frac{H_1-H_2}{2}
 =\frac{R_c-R_d-2R_b}{2}.
\]

Both are Gaussian integers and both are nonzero.  Vanishing would force the
two unit-coefficient residual vectors to coincide, and hence two absolute
offsets to coincide.  Applying the \(211\) rationality argument shows that
both displayed quantities are nonzero integer multiples of \(\bar\Pi\).
Consequently \(n_1\ne\pm n_2\).  Since both are odd,
\(\max(|n_1|,|n_2|)\ge3\).

Finally, \(|R_x|=e^2/(D\sqrt{N(\Pi)})\), so the strict \(111\) triangle bound
in (18) gives

\[
3\sqrt{N(\Pi)}
\le \sqrt{N(\Pi)}\max(|n_1|,|n_2|)
<\frac{3e^2}{D\sqrt{N(\Pi)}}.                   \tag{19}
\]

This proves (16), and (17) follows from the last identity in the proof of
(15).  In the affinely separable all-unit setting, the left side of (17) is
at least \(A^2/M^2\), so the earlier conclusion \(A<M\) is recovered.

## How to use the lemma

For a fixed unit triple, group its center-prime blocks by their three-bit
orientation pattern modulo simultaneous sign reversal.  Each group is
automatically affinely separable, so its product \(A\) must satisfy (4) or
(5).  This can be substantially stronger than checking every prime-power
block separately.

The separation condition is a real limitation, not a notational artifact.
For example, the two-block center root \(e=5^2\cdot29=725\) has common
double-extreme offsets \(428904\) and \(456456\) whose two-block orientation
matrix has nonzero rectangular parity.  Its seven admissible offsets do not
form a magic-square configuration, but the example shows why unrelated local
orientations cannot simply be multiplied into one common Gaussian factor.
