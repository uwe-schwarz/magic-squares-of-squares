# The weighted `p^2 q r` signature residue

## Status

Let a primitive centered magic square of squares have center root

\[
 e=p^2qr,
\]

where `p,q,r` are distinct rational primes.  The block-generalization in
[`three-block-squarefree.md`](three-block-squarefree.md) excludes every
three-block configuration whose local indices are all balanced or extreme.
Consequently a survivor in this exponent pattern must have one genuinely
intermediate `p`-index.  This note first classifies the signatures that
remain after that reduction.  It then applies the exact corner-quotient and
edge-content bounds from [`block-balance.md`](block-balance.md)
simultaneously to all exceptional rows.

The orientation classifier gives `134` physical classes.  The universal
exceptional-row filter excludes `58`; exact aligned quotients raise the
total to `85`; safe two-row composite blocks raise it to `95`; the general
common-factor height raises it to `104`; coupling every admissible column
conjugation in the divisor comparisons raises it to `110`; factoring the
even-level axis expressions raises it to `113`; a congruence refinement of
the skew expressions raises it to `116`; discrete prime floors raise it to
`117`; a complementary-axis descent raises it to `118`:

\[
 \boxed{134=118+16,\qquad
 16\text{ necessary weighted switching classes remain}.}
\]

The number `16` is exact relative to the inequalities proved here.  No
remaining class is asserted to be arithmetically realizable.

## 1. Exact weighted local data

Every center prime is congruent to `1` modulo `4`.  At least three of the
four offsets are local units at each prime.  The exponent-one rows therefore
have indices in `{-1,0,1}`: they are either extreme at all four columns, or
have one balanced column and three extreme columns.

For the squared-prime row, the all-balanced/extreme alternative is already
excluded.  Its unique nonunit column must therefore have index `+1` or `-1`;
the other three columns have extreme index `+2` or `-2`.  Mark the
intermediate column by `I`.

The block-balance theorem supplies a separate size restriction.  A block of
exponent one or two cannot be at least as large as its coprime complement;
equality is impossible here.  Every survivor counted below must therefore
satisfy

\[
 p^2<qr,\qquad q<p^2r,\qquad r<p^2q.               \tag{1}
\]

For each column `c`, let

\[
 j_c=(j_{p,c},j_{q,c},j_{r,c}),
 \qquad |j_{p,c}|\in\{1,2\},
 \qquad j_{q,c},j_{r,c}\in\{-1,0,1\}.
\]

The magnitude `1` in the first coordinate occurs at the unique `I` column;
every zero is the unique balanced incidence in its row.  Unique
factorization at the three disjoint Gaussian supports gives the exact
nonzero/distinctness condition

\[
 j_c\ne0,
 \qquad j_c\ne\mathord\pm j_d\quad(c\ne d).       \tag{2}
\]

Every three-column `111` or `211` relation must also have a frustrated
orientation cycle.  The classifier applies that condition to each of the
four column deletions.

## 2. Exact physical quotient

The squared-prime row is distinguished, while the `q` and `r` rows may be
interchanged.  Columns `0,1` are corners and columns `2,3` are edges.  The
physical symmetry group used here is therefore

\[
 S_2\text{ on the exponent-one rows}
 \ \times\ S_2\text{ on corners}
 \ \times\ S_2\text{ on edges},                  \tag{3}
\]

together with independent row and column orientation switches.  Corners are
never exchanged with edges, and the intermediate marker moves with its
physical column.

Write `F` when an exponent-one row has no balanced column, and write `C0`,
`C1`, `E2`, or `E3` for its balanced corner or edge.  Up to (3), the marker
is either the first corner `I0` or the first edge `I2`.  Exhaustion gives the
following complete breakdown.  “Raw” counts labeled bit assignments for the
displayed canonical incidence pattern after (2) and the four frustration
tests, before switching and pattern automorphisms.

| Intermediate column | Unordered `q,r` pattern | Raw | Classes |
| --- | --- | ---: | ---: |
| `I0` | `F,F` | 1536 | 7 |
| `I0` | `F,C0` | 768 | 6 |
| `I0` | `F,C1` | 1152 | 9 |
| `I0` | `F,E2` | 1152 | 18 |
| `I0` | `C0,C0` | 384 | 2 |
| `I0` | `C0,C1` | 384 | 3 |
| `I0` | `C0,E2` | 384 | 6 |
| `I0` | `C1,C1` | 384 | 2 |
| `I0` | `C1,E2` | 448 | 7 |
| `I0` | `E2,E2` | 384 | 3 |
| `I0` | `E2,E3` | 448 | 4 |
| `I2` | `F,F` | 1536 | 7 |
| `I2` | `F,C0` | 1152 | 18 |
| `I2` | `F,E2` | 768 | 6 |
| `I2` | `F,E3` | 1152 | 9 |
| `I2` | `C0,C0` | 384 | 3 |
| `I2` | `C0,C1` | 448 | 4 |
| `I2` | `C0,E2` | 384 | 6 |
| `I2` | `C0,E3` | 448 | 7 |
| `I2` | `E2,E2` | 384 | 2 |
| `I2` | `E2,E3` | 384 | 3 |
| `I2` | `E3,E3` | 384 | 2 |
| **Total** |  | **14848** | **134** |

All 22 marker/incidence orbits have at least one necessary signature.  The
large residue is expected: the exceptional `p` incidence is nonzero, so it
cannot collide projectively with any of the three magnitude-`2` incidences,
and its marked position reduces the available physical automorphisms.

## 3. Universal exceptional-row inequalities

Write `C` for a corner exception, `E` for an edge exception, and `F` for an
all-extreme row.  Thus, for example, `CFE` means that the `p`-row has its
intermediate index at a corner, the `q`-row is all-extreme, and the `r`-row
has a balanced edge.  The exponent-one rows may always be interchanged.

### Corner exceptions

Let `s` be the base prime of a corner-exceptional block, let its block
exponent be `k_s`, and let `M_s` be its coprime complement.  The index gap is
one in every case here.  The exact corner quotient from
[`block-balance.md`](block-balance.md) therefore satisfies

\[
 v_s(\nu_s)=4,
 \qquad
 |\nu_s|s^{2k_s}<2M_s^2.                         \tag{4}
\]

The second inequality is the strict `211` height bound for the halved
Gaussian relation.  Since `s^4` divides `nu_s`, (4) gives

\[
 \boxed{
 p^4<\sqrt2\,qr,\qquad
 q^3<\sqrt2\,p^2r,\qquad
 r^3<\sqrt2\,p^2q
 }
 \tag{5}
\]

whenever the corresponding row is corner-exceptional.

### Edge exceptions

Suppose row `s` is edge-exceptional.  Its two corner indices are extreme.
Align their signs and, for every row `t`, put

\[
 j'_{t,c}=\operatorname{sgn}(j_{s,c})j_{t,c}
 \quad(c=0,1),
 \qquad
 d_t=2k_t-|j'_{t,0}-j'_{t,1}|,                  \tag{6}
\]

where `(k_p,k_q,k_r)=(2,1,1)`.  It is essential in (6) to use the actual
intermediate magnitude `|j_(p,I)|=1`, not merely its sign.

For the two equal-norm residual corner roots, let `delta` be the gcd of the
Cartesian coordinates of their Gaussian product.  The exact content formula
is

\[
 v_t(\delta)=d_t\quad(t\ne s).
\]

There are no other rational prime factors because the center has exactly the
three displayed blocks.  Hence

\[
 \delta=\prod_{t\ne s}t^{d_t}.                  \tag{7}
\]

The selected linear factor has the form `L=s^2 W`, and its norm satisfies

\[
 N(W)=2\delta z^2\quad\hbox{or}\quad4\delta z^2
 \qquad(z\in\mathbb Z\setminus\{0\}).
\]

Since `|L|<2M_s`, this gives the strict comparison

\[
 \boxed{s^4\delta<2M_s^2.}                      \tag{8}
\]

Every edge-exceptional base also satisfies

\[
 s\equiv1\pmod8,\qquad
 s\nmid\nu_s,\qquad
 \left(\frac{\delta}{s}\right)
 =\left(\frac{3\nu_s}{s}\right).               \tag{9}
\]

The congruences in (9) are retained as necessary filters; the class count
below uses only (1), (5), and (8).

## 4. The exact monomial filter

Put

\[
 \ell=(\log_2p,\log_2q,\log_2r).
\]

Each strict comparison has the form `A dot ell < c`.  With
`d=(d_p,d_q,d_r)`, all vectors used by the filter are as follows.

| Bound | `A` | `c` |
| --- | --- | ---: |
| `D_p: p^2<qr` | `(2,-1,-1)` | `0` |
| `D_q: q<p^2r` | `(-2,1,-1)` | `0` |
| `D_r: r<p^2q` | `(-2,-1,1)` | `0` |
| `C_p` | `(4,-1,-1)` | `1/2` |
| `C_q` | `(-2,3,-1)` | `1/2` |
| `C_r` | `(-2,-1,3)` | `1/2` |
| `E_p(d)` | `(4,d_q-2,d_r-2)` | `1` |
| `E_q(d)` | `(d_p-4,4,d_r-2)` | `1` |
| `E_r(d)` | `(d_p-4,d_q-2,4)` | `1` |

Here is the exhaustive arithmetic comparison.  In the certificate column,
`sum => (v;c)` means that the indicated nonnegative sum of bounds gives
`v dot ell < c`.  Because every center prime is at least `5`, a
row is contradictory as soon as

\[
 5^{v_p+v_q+v_r}\ge2^c.                          \tag{10}
\]

An em dash means that these inequalities alone do not exclude that group.
The edge-content triples are ordered as `(d_p,d_q,d_r)`.

| Role | Edge contents | Classes | Certificate | Result |
| --- | --- | ---: | --- | --- |
| `CCC` | none | 7 | `C_p+C_q+C_r => ((0,1,1);3/2)` | excluded |
| `CCE` | `E_r(1,1,2)` | 9 | `2C_p+C_q+E_r => ((3,0,1);5/2)` | excluded |
| `CCE` | `E_r(3,1,2)` | 4 | `C_p+C_q+E_r => ((1,1,2);2)` | excluded |
| `CEE` | `E_q(1,2,2), E_r(1,2,2)` | 2 | `2C_p+E_q+E_r => ((2,2,2);3)` | excluded |
| `CEE` | `E_q(3,2,0), E_r(1,0,2)` | 4 | `C_p+E_q+E_r => ((0,1,1);5/2)` | excluded |
| `CEE` | `E_q(3,2,2), E_r(3,2,2)` | 1 | `C_p+E_q+E_r => ((2,3,3);5/2)` | excluded |
| `CFC` | none | 15 | — | remains |
| `CFE` | `E_r(1,0,2)` | 5 | — | remains |
| `CFE` | `E_r(1,2,2)` | 5 | `2D_q+2C_p+E_r => ((1,0,0);2)` | excluded |
| `CFE` | `E_r(3,0,2)` | 5 | — | remains |
| `CFE` | `E_r(3,2,2)` | 3 | `D_q+C_p+E_r => ((1,0,2);3/2)` | excluded |
| `CFF` | none | 7 | — | remains |
| `ECC` | `E_p(4,1,1)` | 7 | `E_p+C_q+C_r => ((0,1,1);2)` | excluded |
| `ECE` | `E_p(4,1,0), E_r(0,1,2)` | 9 | — | remains |
| `ECE` | `E_p(4,1,2), E_r(4,1,2)` | 4 | `E_p+C_q+E_r => ((2,1,3);5/2)` | excluded |
| `EEE` | `E_p(4,0,0), E_q(0,2,2), E_r(0,2,2)` | 3 | — | remains |
| `EEE` | `E_p(4,0,2), E_q(0,2,0), E_r(4,0,2)` | 1 | `E_p+E_q+E_r => ((0,0,2);3)` | excluded |
| `EEE` | `E_p(4,2,0), E_q(4,2,0), E_r(0,0,2)` | 3 | `E_p+E_q+E_r => ((0,2,0);3)` | excluded |
| `EFC` | `E_p(4,0,1)` | 10 | — | remains |
| `EFC` | `E_p(4,2,1)` | 8 | `D_q+E_p+C_r => ((0,0,1);3/2)` | excluded |
| `EFE` | `E_p(4,0,0), E_r(0,2,2)` | 5 | — | remains |
| `EFE` | `E_p(4,0,2), E_r(4,0,2)` | 5 | — | remains |
| `EFE` | `E_p(4,2,0), E_r(0,0,2)` | 5 | — | remains |
| `EFF` | `E_p(4,0,0)` | 3 | — | remains |
| `EFF` | `E_p(4,2,0)` | 4 | — | remains |

The excluded rows total

\[
 7+13+7+8+7+4+4+8=58,
\]

leaving the exact role breakdown

\[
\begin{array}{c|rrrrrrrr}
\text{role}&CFC&CFE&CFF&ECE&EEE&EFC&EFE&EFF\\ \hline
\text{remaining}&15&10&7&9&3&10&15&7.
\end{array}                                      \tag{11}
\]

For completeness, the filter does not stop after finding the displayed
small certificates.  If the available bounds are `A_i ell < c_i`, every
possible monomial certificate belongs to the rational polyhedral cone

\[
 \lambda_i\ge0,
 \qquad
 \sum_i\lambda_iA_i\ge0.                         \tag{12}
\]

After writing

\[
 \ell=(\log_2 5)(1,1,1)+y,
 \qquad y\ge0,
\]

Farkas' lemma says that this
cone contains every infeasibility certificate.  It is pointed, so its
extreme rays suffice.  With only three output coordinates, an extreme ray
has at most four positive multipliers.  The implementation enumerates every
such support and its independent active output coordinates, computes the
nullspaces over exact rational numbers, and checks (10) after clearing
denominators to an integer comparison.  Thus `76` is not a cutoff artifact:
it is the exact residue of (1), (5), and (8).

## 5. Safe aligned-quotient comparisons

The universal bounds do not use the orientation of a full retained triple.
There is a second exact filter whenever three roles can be assigned as
follows.

- An **aligned row** is extreme with one orientation on all three retained
  columns.
- A **divisor row** contains its exceptional column and has the same extreme
  orientation on the other two retained columns.
- The third row is the **remaining row**.

Let `o` be the omitted column.  The relation is `111` when `o` is an edge
and `211` when `o` is a corner.  Write `K_o=3` and `K_o=2`, respectively.
If the aligned block is represented by the one-sided Gaussian integer
\(\mathcal A\), its exact quotient is

\[
 H=\bar{\mathcal A}^{4}n\quad(111),\qquad
 \frac H2=\bar{\mathcal A}^{4}n\quad(211),
 \qquad n\in\mathbb Z\setminus\{0\}.             \tag{13}
\]

For a balanced exponent-one divisor row with Gaussian prime `beta`, the
three squared local factors contain a common `beta^2`; rationality of `n`
therefore gives `b^2 | n`.  The intermediate `p`-row has more content.  In
every applicable class its three squared local factors, after orientation,
are

\[
 \pi^6\bar\pi^2,\qquad \pi^8,\qquad\pi^8.
\]

Thus `\pi^6\mid n`, and rationality gives

\[
 \boxed{p^6\mid n.}                              \tag{14}
\]

The `211` halving loses no factor: `2` is a unit at every Gaussian prime
above an odd center prime.  Applying the strict height estimate to (13) and
the forced rational content gives the following exact quotient bounds.  In
the table `a,b,c` denote the aligned, divisor, and remaining base rows.

| Aligned row | Divisor row | Quotient height |
| --- | --- | --- |
| `p` | `b in {q,r}` | `p^4 < K_o c^2` |
| `a in {q,r}` | `p` | `p^2 a^2 < K_o c^2` |
| `a in {q,r}` | other exponent-one row | `a^2 < K_o p^4` |

The last row does not occur among the `134` frustrated signatures.  Indeed,
the normalized `p` orientations are constant; together with an aligned row
and the equal divisor pair, that retained relation would be coherent.

There is also a divisor comparison.  Cancel the common factor of the
divisor row in (13), then reduce modulo its conjugate.  If `beta` is the
Gaussian prime above its underlying base prime `b`, the surviving two-term
factor has one of the forms

\[
 \begin{array}{c|c}
 A_d&\bar\beta^2\mid\bar\gamma^d\mathbin\pm\gamma^d\\
 S_d&\bar\beta^2\mid2\bar\gamma^d\mathbin\pm\gamma^d
 \end{array}                                      \tag{15}
\]

up to conjugation and signs.  The family is `A` when the two retained
coefficients have magnitudes `1,1`, and `S` when they have magnitudes `2,1`.
This distinction is physical: for a corner omission the doubled retained
corner can be the divisor exception, leaving an `A` rather than an `S`
factor.  The level is `d=2` when the remaining exception lies in the pair
and `d=4` when two opposite exponent-one extremes remain.  The same
coordinate and simultaneous-square arguments as in Section 13 of
[`three-block-squarefree.md`](three-block-squarefree.md) give

\[
 \boxed{
 A_d(b,c)\Longrightarrow b^2<c^{d/2},\qquad
 S_d(b,c)\Longrightarrow b<c^{d/2}.}             \tag{16}
\]

If the remaining row were `p`, equal intermediate/extreme orientations
would give level `2`, while opposite orientations would give level `6`;
the corresponding bounds would be `A_2(b,p): b^2<p`,
`S_2(b,p): b<p`, `A_6(b,p): b^2<p^3`, and
`S_6(b,p): b<p^3`.  Exhaustion shows that none of these cases occurs, for
the coherence reason above.  This is a useful check that the intermediate
column has not accidentally been treated as a balanced incidence.

There are exactly `86` safe comparisons in `70` of the `134` classes.  Add
their quotient heights and (16) to the bounds of Section 4.  Since the
`111` constant is `3`, the exact certificate evaluator records a right side
as `2^a 3^b`; no floating logarithm or replacement of `3` by `4` is used.
The exhaustive cone calculation excludes `27` classes not excluded in
Section 4.  In the table below, `Q_(a,b)^o` denotes the quotient-height row
aligned at `a`, with divisor `b` and omitted column `o`.  Repeated
certificate terms carry the displayed coefficient.

| Newly excluded canonical form(s) | Certificate | Aggregate contradiction |
| --- | --- | --- |
| `I0:0000/0001/0010` | `Q_(r,p)^2+Q_(q,p)^3` | `p^4<9` |
| `I0:0000/0001/0100` | `Q_(r,p)^1+Q_(q,p)^3` | `p^4<6` |
| `I0:0000/0001/*010`, `I0:0000/0001/*011`, `I0:0000/0001/0*10` | `C_r+Q_(q,p)^3` | `qr<3 sqrt(2)` |
| `I0:0000/0100/*001`, `I0:0000/0100/0*01` | `C_r+Q_(q,p)^1` | `qr<2 sqrt(2)` |
| `I0:0000/0001/0*11` | `A_4(r,q)+Q_(q,p)^3` | `p^2<3` |
| `I0:0000/0001/01*0`, `I0:0000/0001/01*1` | `E_r(1,0,2)+2Q_(q,p)^3` | `pq^2<18` |
| `I0:0000/0010/01*0` | `E_r(1,0,2)+2Q_(q,p)^2` | `pq^2<18` |
| `I0:0000/0100/00*1` | `E_r(3,0,2)+Q_(q,p)^1` | `pr^2<4` |
| `I2:0000/0001/0100` | `Q_(r,p)^1+Q_(q,p)^3` | `p^4<6` |
| `I2:0000/0100/0111` | `Q_(r,p)^0+Q_(q,p)^1` | `p^4<4` |
| `I2:0000/0100/*001`, `I2:0000/0111/*001`, `I2:0000/0111/*011` | `C_r+Q_(q,p)` | `qr<2 sqrt(2)` |
| `I2:0000/0100/*010`, `I2:0000/0100/001*` | `Q_(q,p)^1+A_4(r,q)` | `p^2<2` |
| `I2:0000/0001/01*0`, `I2:0000/0001/010*` | `E_r(0,0,2)+2Q_(q,p)^3` | `q^2<18` |
| `I2:0000/0100/00*1` | `E_r(4,0,2)+Q_(q,p)^1` | `p^2r^2<4` |
| `I2:0000/0100/01*1`, `I2:0000/0100/011*` | `E_r(0,2,2)+2Q_(q,p)^1` | `q^4<8` |
| `I2:0000/*010/01*0` | `2E_r(0,1,2)+A_4(q,r)+3Q_(p,q)^2` | `p^4<108` |
| `I2:0000/*010/010*`, `I2:0000/*010/011*` | `E_r(0,1,2)+2A_2(q,r)+Q_(p,q)^2` | `q^3<6` |

In the three-form row with `Q_(q,p)` the omitted column is `1` for the
first form and `0` for the other two.  Every aggregate contradicts
`p,q,r>=5`.  Thus the exact residue after this stage is

\[
 \boxed{134-85=49.}                              \tag{17}
\]

## 6. Two-row composite-block bounds

A further safe use of the exact orientations groups two prime-power blocks.
Fix an omitted column `o` and two rows `s,t`.  Suppose each row is
all-extreme, or has its exception precisely at `o`, and suppose the XOR of
their two orientation bits is constant on the retained triple.  This is
exactly affine separability of the two-row orientation matrix.  The
composite-block lemma in [`composite-blocks.md`](composite-blocks.md) applies
with

\[
 \mathsf A=s^{k_s}t^{k_t},\qquad
 \mathsf M=u^{k_u},\qquad (k_p,k_q,k_r)=(2,1,1),
\]

where `u` is the remaining row.  It gives the safe monomial bound

\[
 \boxed{\mathsf A^2<K_o\mathsf M^2.}             \tag{18}
\]

The arbitrary orientations in the third row stay inside the residual
Gaussian factors; they do not need to be coherent and do not weaken the
composite-block proof.  Exhaustion finds `18` such groupings.  Adding (18)
to the exact cone excludes ten more classes:

| Newly excluded canonical form | Certificate | Aggregate contradiction |
| --- | --- | --- |
| `I0:0000/0001/0011` | `C_p+G2_12` | `qr<3 sqrt(2)` |
| `I0:0000/0001/0101` | `C_p+G1_12` | `qr<2 sqrt(2)` |
| `I0:0000/0100/0101` | `C_p+G3_12` | `qr<3 sqrt(2)` |
| `I0:0000/0101/0*01` | `C_p+G1_12` | `qr<2 sqrt(2)` |
| `I0:0000/0111/0*01` | `2C_r+G0_01` | `r^4<4` |
| `I0:0000/0111/00*1` | `E_r(3,0,2)+G0_01` | `p^3r^2<4` |
| `I2:0000/0001/0101` | `E_p(4,2,0)+G1_12` | `q^2<4` |
| `I2:0000/0011/0100` | `E_p(4,2,0)+G0_12` | `q^2<4` |
| `I2:0000/0010/010*` | `E_r(0,0,2)+G2_01` | `r^2<6` |
| `I2:0000/0110/*001` | `E_p(4,0,1)+G0_12` | `r<4` |

Here `Go_st` denotes (18) for omitted column `o` and row pair `s,t`, with
rows numbered `p=0,q=1,r=2`.  The final exact role breakdown is

\[
\begin{array}{c|rrrrrrrr}
\text{role}&CFC&CFE&CFF&ECE&EEE&EFC&EFE&EFF\\ \hline
\text{remaining}&7&5&2&6&3&5&8&3.
\end{array}                                      \tag{19}
\]

Consequently

\[
 \boxed{134=95+39}                               \tag{20}
\]

is the exact residue through the two-row composite stage.

## 7. The general common-factor height

The preceding aligned and composite bounds are special cases of a direct
common-factor calculation that does not require an extreme row.  Fix one
deletion, order its retained columns as `c0<c1<c2`, and independently
conjugate their Gaussian encodings.  Modulo simultaneous conjugation there
are exactly four choices

\[
 (\epsilon_0,\epsilon_1,\epsilon_2)
   =(1,\mathord\pm1,\mathord\pm1).               \tag{21}
\]

Put `j'_(s,c)=epsilon_c j_(s,c)`.  For a row of exponent `k_s`, the two
local exponents in the squared encoding are

\[
 2k_s+2j'_{s,c},\qquad 2k_s-2j'_{s,c}.
\]

Their common minima over the retained triple are

\[
 a_s=\min_c(2k_s+2j'_{s,c}),\qquad
 b_s=\min_c(2k_s-2j'_{s,c}).                    \tag{22}
\]

Let

\[
 D=\prod_s s^{\min(a_s,b_s)}
\]

be the rational part of the common Gaussian divisor, and let `Pi` be its
remaining one-sided part.  Then

\[
 N(\Pi)=\prod_s s^{|a_s-b_s|}.
\]

After cancelling the common divisor, the offset relation has
\(\operatorname{Im}(\Pi H)=0\).  The same cube-root and equality arguments
as before give \(H\ne0\); rationality forces \(\bar\Pi\mid H\).  In type
`211`, all three residual terms are congruent modulo `2`, so \(H/2\) is
integral and the identical
argument applies after halving.  Comparing the forced divisor with the
strict height gives

\[
 D N(\Pi)<K_o e^2.
\]

Equivalently, the exact monomial inequality for this sign pattern is

\[
 \boxed{
  \prod_{s\in\{p,q,r\}}
   s^{\max(a_s,b_s)-2k_s}<K_o,
  \qquad (k_p,k_q,k_r)=(2,1,1).}                 \tag{23}
\]

Every choice in (21) is legitimate: conjugating one column preserves its
absolute offset and only changes the absorbed projection sign.  Thus the
third-row frustration does not obstruct (23).  Enumerating four patterns
for each of four deletions in all `134` forms gives `2144` audited
common-factor events.  Together with the divisor comparisons (16) and the
universal bounds, their exact cones exclude `104` classes.  This is `19`
more than the aligned-quotient stage; the ten composite exclusions in
Section 6 occur among those nineteen.  The other nine are:

| Newly excluded after Section 6 | Certificate | Aggregate contradiction |
| --- | --- | --- |
| `I0:0000/0101/*001` | `3C_p+C_r+2H1_(++-)` | `p^2<16` |
| `I0:0000/0101/0*10` | `3C_p+C_r+2H0_(+-+)` | `p^2<16` |
| `I0:0000/0101/0*11` | `Q_(p,r)^0+H2_(+--)` | `p^2<6` |
| `I0:0000/0011/01*1` | `Q_(p,r)^0+H1_(+--)` | `p^2<4` |
| `I0:0000/0101/00*1` | `4C_p+E_r(3,0,2)+3H1_(++-)` | `p^3<64` |
| `I0:0000/0110/00*0` | `2C_p+Q_(r,p)^2+2H1_(+-+)` | `p^2<24` |
| `I0:0000/0110/00*1` | `4C_p+E_r(3,0,2)+3H0_(++-)` | `p^3<64` |
| `I2:0000/0110/*010` | `Q_(p,r)^2+H1_(+-+)` | `p^2<6` |
| `I2:0000/0101/001*` | `Q_(p,r)^2+H0_(+-+)` | `p^2<6` |

Here `Ho_(epsilon0 epsilon1 epsilon2)` denotes (23).  The exact final role
breakdown is

\[
\begin{array}{c|rrrrrrrr}
\text{role}&CFC&CFE&CFF&ECE&EEE&EFC&EFE&EFF\\ \hline
\text{remaining}&4&1&2&6&3&4&7&3.
\end{array}                                      \tag{24}
\]

Therefore the complete proved filter in this note leaves

\[
 \boxed{134=104+30.}                             \tag{25}
\]

## 8. All coupled divisor comparisons

Section 5 normalized the already displayed columns and found `86` safe
comparisons.  The normalization is not unique: for each retained triple one
may apply any of the four coupled column conjugations (21) before choosing
the aligned and divisor rows.  This preserves the absolute offsets and the
coefficient magnitudes, so every resulting quotient identity is valid.

The exhaustive rule is most cleanly stated using the transformed local
indices.  A row `a` may be aligned when all three retained values are the
same extreme `+k_a` or `-k_a`.  A different row `b` may be the divisor row
when its exception is retained and its other two values are equal extremes.
At an exponent-one divisor the common one-sided exponent is `2`.  At the
intermediate `p` divisor it is

\[
 6\quad\hbox{if the intermediate and pair orientations agree},\qquad
 2\quad\hbox{if they disagree}.                  \tag{26}
\]

Rationality of the exact quotient adds the conjugate factor, and reduction
at the opposite Gaussian square again leaves a two-term factor in the third
row.  Computing its exponent after removing the exact gcd gives all levels
without treating `I` as balanced:

| Remaining row and retained pair | Level |
| --- | ---: |
| exponent one, exception plus extreme | `2` |
| exponent one, opposite extremes | `4` |
| `p`, `I` plus equally oriented extreme | `2` |
| `p`, `I` plus oppositely oriented extreme | `6` |
| `p`, opposite extremes | `8` |

Thus (15)--(16) apply with `d\in\{2,4,6,8\}`.  In particular, an
opposite-extreme `p` pair is `A_8` or `S_8`, not level `4`; its axis bound
is `b^2<p^4`.  For the skew family the coefficient magnitudes are `2,1`
according to the actual doubled corner.  The simultaneous-square proof of
`S_d` remains valid at levels `6` and `8`: write `\gamma^d` as the square of
the primitive odd-norm Gaussian integer `\gamma^{d/2}`.  Its coordinates
have the same odd/divisible-by-four parity used in (16).  An equal-monomial
skew pair would be an immediate coprime-support contradiction; none occurs
in the classified forms.

The local-exponent enumerator finds exactly `300` distinct safe events in
`114` of the `134` classes.  It adds both the rational-content quotient
height and the divisor comparison for every event.  Coupling these bounds
with the exact common-factor and universal cones excludes six more classes:

| Newly excluded canonical form | Certificate | Aggregate contradiction |
| --- | --- | --- |
| `I0:0000/0101/0*00` | `A_2(r,p)+2A_2(p,r)` | `p^3<1` |
| `I0:0000/0011/01*0` | `E_r(1,0,2)+H0_(+--)+4A_2(p,r)` | `p<4` |
| `I2:0000/0110/*000` | `S_2(p,r)+A_2(r,p)` | `r<1` |
| `I2:0000/0101/000*` | `S_2(r,p)+S_2(p,r)` | `1<1` |
| `I2:0000/0101/010*` | `S_2(r,p)+S_2(p,r)` | `1<1` |
| `I2:0000/*001/011*` | `H0_(+++)+A_2(q,p)` | `p<2` |

The strict zero-vector certificates in the fourth and fifth rows are valid:
adding two strict reciprocal inequalities gives the impossible `0<0` in
logarithmic form.  The final role breakdown is

\[
\begin{array}{c|rrrrrrr}
\text{role}&CFC&CFF&ECE&EEE&EFC&EFE&EFF\\ \hline
\text{remaining}&3&2&5&3&3&5&3.
\end{array}                                      \tag{27}
\]

The exact weighted residue is therefore

\[
 \boxed{134=110+24.}                             \tag{28}
\]

## 9. Factoring the axis expressions

The coordinate estimate in (16) leaves substantial arithmetic unused.
Suppose an axis event has even level `d` and write

\[
 Z=\gamma^{d/2}=X+iY,
 \qquad X^2+Y^2=c^{d/2}.
\]

The Gaussian divisibility in (15), together with its conjugate, says that
the rational integer `b^2` divides a nonzero Cartesian coordinate of

\[
 \gamma^d=Z^2=(X^2-Y^2)+2iXY.
\]

The Gaussian integer `Z` is primitive at the distinct divisor prime `b`.
Thus `b` cannot divide both `X` and `Y`, nor both `X-Y` and `X+Y`; the
latter gcd divides `2`, and `b` is odd.  Consequently the whole factor
`b^2` divides one of

\[
 X,\qquad Y,\qquad X-Y,\qquad X+Y.
\]

All four quantities have absolute value strictly below
`sqrt(2) |Z|`.  This sharpens every even-level axis comparison to

\[
 \boxed{
 A_d(b,c)\Longrightarrow
 b^2<\sqrt2\,c^{d/4}.}                           \tag{29}
\]

The exact enumerator uses the equivalent integral inequality
`b^8<4c^d`.  Among the `300` generalized events, exactly `200` axis events
occur in `109` classes.  Adding (29) excludes precisely three of the
`24` survivors from Section 8:

| Newly excluded canonical form | Axis certificate | Aggregate contradiction |
| --- | --- | --- |
| `I0:0000/0011/*001` | `2A_4(p,r)+A_8(r,p)` | `p^8<64` |
| `I0:0000/0101/*011` | `2A_4(p,r)+A_8(r,p)` | `p^8<64` |
| `I0:0000/0011/0*01` | `2A_4(p,r)+A_6(r,p)` | `p^10<64` |

Every center prime is at least `5`, so each displayed inequality is
impossible.  The remaining role breakdown is

\[
\begin{array}{c|rrrrrr}
\text{role}&CFF&ECE&EEE&EFC&EFE&EFF\\ \hline
\text{remaining}&2&5&3&3&5&3.
\end{array}                                      \tag{30}
\]

Hence the exact weighted residue through all bounds proved here is

\[
 \boxed{134=113+21.}                             \tag{31}
\]

For level `6` one may factor the original coordinate still further.  If
`gamma=x+iy`, its real coordinate has factors
`(x-y)(x+y)(x^2-4xy+y^2)(x^2+4xy+y^2)`, while its imaginary coordinate has
factors `2xy(x^2-3y^2)(3x^2-y^2)`.  A center divisor prime cannot meet two
of these factors: the only possible odd common prime is `3`, whereas every
center prime is `1 modulo 4`.  This gives the valid refinement
`A_6(b,c) => b^2<3c`, but it excludes no additional class in the exact cone.

## 10. A congruence gap for the skew expressions

There is a different sharpening for every skew event.  Put

\[
 W=\gamma^d=X+iY,
 \qquad X^2+Y^2=c^d.
\]

Because `d` is even, primitivity and odd norm give `X` odd and `4 | Y`,
after conjugation if necessary.  For

\[
 K=2\bar W\mathbin\pm W
\]

the norm is either `9X^2+Y^2` or `X^2+9Y^2`.  The divisibility in (15)
therefore makes

\[
 t=\frac{N(K)}{b^2}
\]

a positive integer.  Both `N(K)` and `b^2` are `1 modulo 8`, so
`t=1 modulo 8`.  Modulo `3` there are only two possibilities.  If the
coordinate outside the coefficient `9` is not divisible by `3`, then
`t=1 modulo 3`.  If it is divisible by `3`, primitivity and the fact that
`-1` is not a square modulo `3` give `v_3(t)=2` exactly.

No square value of `t` is possible: it would make `N(K)` a square, while
`X^2+Y^2=c^d` is already a square, contradicting the simultaneous-square
lemma used in (16).  Moreover,

\[
 t=N\left(\frac K{\bar\beta^2}\right),
\]

so `t` is itself a Gaussian norm.  Every rational prime congruent to `3`
modulo `4` therefore has even valuation in `t`.

There is one more useful sieve.  Write
`gamma^(d/2)=U+iV` and put

\[
 F=U^4-U^2V^2+V^4.
\]

The two skew norms are congruent modulo `5` to `F` and `4F`.  For a
primitive pair `(U,V)`, `F` is `1` or `3` modulo `5`; the value `3` forces
`U^2+V^2=0 modulo 5`, hence `c=5`.  It follows that `5` divides neither
`t` nor `b`, while `t=2` or `3 modulo 5` forces `c=5`.

Combining the modulo `8` and modulo `3` conditions, nonsquareness, and the
Gaussian-norm condition leaves exactly

\[
 73,97,145,153,193
\]

as candidates below `241`.  The value `145` is excluded modulo `5`; the
other four force `c=5`.  Up to units and conjugation take `gamma=2+i`.
For `d=2,4,6,8`, the eight skew norms factor as

\[
\begin{gathered}
97,\quad3^2\mathbin\cdot17,\quad
3^2\mathbin\cdot113,\quad5233,\\
17^2\mathbin\cdot433,\quad3^2\mathbin\cdot3457,\quad
3^2\mathbin\cdot281\mathbin\cdot1033,\quad
89\mathbin\cdot14537.
\end{gathered}
\]

The only square of an admissible split divisor prime in this list is
`17^2`, whose quotient is `433`; none yields one of the four candidates.
Thus `t>=241` at every level.

The level records more information.  If a split prime `lambda` occurs to
odd valuation in `t`, reduction at one of the Gaussian primes above
`lambda` shows that one of `+2,-2` is a `d`-th power modulo `lambda`.
For `d=6`, the preceding sieves together with this sixth-power condition
leave only `369` in the interval from `241` through `432`.  At the inert
prime `11`, however, the norm-one group has order `12`, so its sixth power
is `+1` or `-1`.  The corresponding skew norm is therefore a nonzero
quadratic residue, whereas `369=6 modulo 11` is not.  Hence `t>=433` at
level `6`; the value `433` does occur in the displayed `c=5`, `d=6` list.

For `d=4`, the fourth-power sieve leaves only `601` and `801` below `1201`.
At the inert prime `7`, a norm-one element has order dividing `8`; its
fourth power is `+1` or `-1`, so again the skew norm, and hence `t`, is a
quadratic residue.  Both `601` and `801` are nonresidues modulo `7`, giving
`t>=1201`.

For `d=8`, after the eighth-power split-prime sieve the remaining candidates
below `4201` are

\[
 601,801,1249,1609,1801,2089,2281,2529,3049,3529.
\]

Use the inert primes `7,31,47`.  If `z=gamma/bar gamma`, then `z` lies in
their norm-one groups, of orders `8,32,48`.  Thus `z^8` has order at most
`1,4,6`, respectively, and the two normalized skew norms are quadratic
residues: modulo `31` their possible values are `1,9,5`, and modulo `47`
they are `1,9,3,7` (modulo `7` they are `1,9`).  Consequently `t` must
be a quadratic residue modulo all three primes.  Each number in the list
fails at least one of these three tests; the first surviving candidate is
`4201`.

Since both coordinates of `W` are nonzero, `N(K)<9c^d`.  The resulting
level-specific bounds are

\[
 \boxed{
 \begin{aligned}
 S_2(b,c)&\Longrightarrow241b^2<9c^2,\\
 S_4(b,c)&\Longrightarrow1201b^2<9c^4,\\
 S_6(b,c)&\Longrightarrow433b^2<9c^6,\\
 S_8(b,c)&\Longrightarrow4201b^2<9c^8.
 \end{aligned}}                                  \tag{32}
\]

Exactly `100` of the `300` generalized events are skew events; they occur
in `76` classes.  Adding (32) to the exact cone excludes three more classes:

| Newly excluded canonical form | Certificate | Aggregate contradiction |
| --- | --- | --- |
| `I2:0000/0100/0101` | `Q_(q,p)^1+G3_12+S_4(p,q)` | `1<54/1201` |
| `I2:0000/0110/*011` | `A_8(r,p)+4S_2(p,r)` | `1<2^2 3^8/241^4` |
| `I2:0000/0101/011*` | `A_8(r,p)+4S_2(p,r)` | `1<2^2 3^8/241^4` |

Here the `A_8` terms use the sharp axis bound (29).  The final role
breakdown is

\[
\begin{array}{c|rrrrrr}
\text{role}&CFF&ECE&EEE&EFC&EFE&EFF\\ \hline
\text{remaining}&2&5&3&2&4&2.
\end{array}                                      \tag{33}
\]

Thus the exact weighted residue is

\[
 \boxed{134=116+18.}                             \tag{34}
\]

## 11. Discrete prime floors

The continuous logarithmic cone can also use two elementary congruence
floors.  Section 3 already records that every edge-exceptional base is
`1 modulo 8`, hence at least `17`.  A skew comparison supplies another
floor even when its divisor row is all-extreme or corner-exceptional.
Reducing (15) modulo the Gaussian prime above `b` gives

\[
 \left(\frac\gamma{\bar\gamma}\right)^d
   =\mathord\pm2\pmod b.                         \tag{35}
\]

Since `d` is even and `b=1 modulo 4`, this forces `(2/b)=1`, hence
`b=1 modulo 8` and `b>=17`.  At levels `4` and `8`, one of `+2,-2` must be
a fourth power.  The only primes congruent to `1 modulo 8` below `73` are
`17,41`, and direct enumeration of their fourth powers contains neither
sign.  Thus an `S_4` or `S_8` divisor base is at least `73`; this is sharp
at `73` for the unsigned condition.

Applying these coordinate floors to the exact cone excludes one further
class:

| Newly excluded canonical form | Certificate | Aggregate contradiction |
| --- | --- | --- |
| `I2:0000/*001/01*0` | `5E_p(4,1,0)+3E_r(0,1,2)+A_8(q,p)` | `r^2<2^10` |

The `A_8` term again means the fourfold-scaled sharp bound (29).  In this
class the `r` row is an `S_8` divisor, so `r>=73`, whereas the certificate
gives `r^2<1024`.  The final role breakdown is

\[
\begin{array}{c|rrrrrr}
\text{role}&CFF&ECE&EEE&EFC&EFE&EFF\\ \hline
\text{remaining}&2&4&3&2&4&2.
\end{array}                                      \tag{36}
\]

Accounting also for distinctness of `p,q,r` against the exact allowed prime
sets and all six size orderings does not exclude another class.  The final
residue in this note is

\[
 \boxed{134=117+17.}                             \tag{37}
\]

## 12. Complementary level-eight axes

One of the `17` classes left by the separate inequalities has canonical form

```text
I2:0000/01*0/011*
```

All three exceptional columns are edges.  Its two coupled comparisons are
`A_8(r,p)` after omitting column `2` and `A_8(q,p)` after omitting column
`3`.  For either physical assignment of the sum and difference edges, the
corner coefficients in one relation have equal effective signs and those in
the other have opposite signs.  Thus one divisor sees the real coordinate
of the same Gaussian power and the other sees its imaginary coordinate;
swapping the physical edges merely exchanges `q` and `r`.

Call the imaginary-coordinate divisor `s` and the real-coordinate divisor
`t`.  Write

\[
 \pi^4=A+iB,\qquad
 A^2+B^2=p^4,\qquad \gcd(A,B)=1,                 \tag{38}
\]

where `A` is odd and `4 | B`.  Since `s,t` are odd, the two axis
divisibilities give

\[
 s^2\mid AB,\qquad
 t^2\mid(A-B)(A+B).                              \tag{39}
\]

The factors in each product are coprime at the relevant divisor prime.
Consequently `s^2` divides `A` or `B`, and hence `s<p`.  On the other hand,
the dominant-block and exceptional-`p` bounds for this class are

\[
 p^2<st,\qquad p^4<2s^2t^2.                     \tag{40}
\]

The first inequality forces `t>p`.  Since `t^2 | A-B` or `t^2 | A+B`,
while \(0<|A\mathbin\pm B|<\sqrt2p^2\) and `t^2>p^2`, the quotient must be
`1`.  Squaring therefore gives

\[
 s^2\mid t^4-p^4=(t-p)(t+p)(t^2+p^2).
\]

The three factors are pairwise coprime at `s`: their pairwise gcds divide
`2p` or `2p^2`, and `s` is odd and distinct from `p,t`.  Moreover,
`t^2<sqrt(2)p^2`, and (40) gives

\[
 s^2>\frac{p^2}{2\sqrt2}>
 (1+2^{1/4})p>t+p,
\]

where the middle inequality uses `p>=17`.  Hence `s^2 | t^2+p^2`.  Put

\[
 k=\frac{t^2+p^2}{s^2}
   <2\frac{t^2}{p^2}
       \left(\frac{t^2}{p^2}+1\right)
   <4+2\sqrt2<7.                                \tag{41}
\]

Every exceptional base here is `1 modulo 8`, so
`p^2=s^2=t^2=1 modulo 16` and therefore `k=2 modulo 16`.  The positive
integer in (41) must be `k=2`.  But then
`s^2=(t^2+p^2)/2>p^2`, contradicting `s<p`.  This excludes precisely the
displayed `EEE` class.  The role breakdown becomes

\[
\begin{array}{c|rrrrrr}
\text{role}&CFF&ECE&EEE&EFC&EFE&EFF\\ \hline
\text{remaining}&2&4&2&2&4&2.
\end{array}                                      \tag{42}
\]

Thus the final residue proved in this note is

\[
 \boxed{134=118+16.}                             \tag{43}
\]

## 13. Reproduction and boundary

Run

```sh
python3 three_block_p2qr_signatures.py
python3 p2qr_monomial_filter.py
python3 -m unittest -v test_three_block_p2qr_signatures.py
python3 -m unittest -v test_p2qr_monomial_filter.py
```

The signature implementation enumerates the weighted vectors directly.  Its
test has a second implementation which explicitly enumerates all 64
effective row and column switches instead of using the classifier's
spanning-forest normal form.  It pins every row of the first table and the
total `134`.

The monomial filter restores the actual local-index magnitudes, computes all
edge contents, enumerates the `86` safe quotient comparisons, `18`
composite groupings, and `2144` general common-factor patterns, and
`300` coupled divisor comparisons.  It enumerates each Farkas cone over
exact rational numbers.  Its tests pin the `58/76`, `85/49`, `95/39`,
`104/30`, `110/24`, `113/21`, `116/18`, `117/17`, and `118/16` stages,
every role
count, the intermediate `\pi^6` content, levels `6` and `8`, the corner/edge
coefficient distinction, the factorized axis and sharpened skew bounds,
the discrete prime floors, and the exact newly excluded form sets.

The remaining `16` classes satisfy only necessary local, orientation, and
monomial comparison conditions.  This note does not couple all four exact
Gaussian quotient identities, impose the quadratic-character part of (9),
or prove that any remaining class yields integer offsets or a magic square.
