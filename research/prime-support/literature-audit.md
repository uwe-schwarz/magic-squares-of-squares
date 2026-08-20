# Literature and claim audit

## Current status

The classical problem asks for a `3 x 3` magic square of nine pairwise
distinct positive integer squares.  The following sources describe the
problem as open or develop necessary reformulations rather than a solution:

- Andrew Bremner, [On squares of squares](https://matwbn.icm.edu.pl/ksiazki/aa/aa88/aa8837.pdf), Acta Arithmetica 88 (1999), gives the elliptic-curve reformulation: three points in \(2E(\mathbb Q)\) whose x-coordinates are in arithmetic progression.
- Andrew Bremner, [On squares of squares II](https://www.impan.pl/shop/publication/transaction/download/product/82367), Acta Arithmetica 99 (2001), studies the associated intersections of quadrics and high-genus curves.
- Paul Pierrat, François Thiriet, and Paul Zimmermann, [Magic Squares of Squares](https://members.loria.fr/PZimmermann/papers/squares.pdf) (2015), proves the `1 mod 24` entry condition and gives a complete parametrization of three-square arithmetic progressions around a fixed square center.  It also explains why earlier hourglass searches with pairwise-coprimality assumptions do not cover the general case.
- Christian Woll, [A Partial Residue Categorization of the Magic Square of Squares](https://arxiv.org/abs/1809.03067) (2018), studies center-prime residue classes.
- Onno Cain, [Gaussian Integers, Rings, Finite Fields, and the Magic Square of Squares](https://arxiv.org/abs/1908.03236) (2019), gives Gaussian and finite-ring reformulations.
- Christian Wolird, [A New Transformation of the Magic Square of Squares](https://arxiv.org/abs/2310.12164) (2023), relates arithmetic triples of Gaussian squares.
- Nick Rome and Shuntaro Yamagishi, [On the existence of magic squares of powers](https://arxiv.org/abs/2406.09364) (published 2025), proves existence for square magic squares of every order at least four; it does not settle order three.
- Peter Müller, [On Euler's magic matrices of sizes 3 and 8](https://doi.org/10.4064/aa250422-2-8), Acta Arithmetica 222.1 (2026), again describes the unrestricted order-three problem as open.  Its nonexistence theorem assumes the additional Euler condition \(MM^T=\gamma I\), so it does not settle the present problem.

This is not a systematic MathSciNet or zbMATH priority search.  The absence of
the refined block inequality from this small source set does not establish
novelty.

## The three-offset subproblem

The apparently weaker question behind the `111` counter in
[center-relation-scan.md](center-relation-scan.md) has itself been asked
explicitly.  A 2017 [MathOverflow question](https://mathoverflow.net/questions/269278/sums-of-areas-of-unit-pythagorean-triangles)
asks whether the sum of the areas of two rational right triangles with unit
hypotenuse can be the area of a third.  With the standard rational parameter,
this is exactly the existence of nontrivial rational solutions of

\[
\frac{2x(x^2-1)}{(x^2+1)^2}
+\frac{2y(y^2-1)}{(y^2+1)^2}
=\frac{2z(z^2-1)}{(z^2+1)^2},
\]

and hence exactly a coefficient-`{1,1,1}` relation among three normalized
center offsets.  The page records no answer; comments report negative
searches in parameter height, but those comments are neither a proof nor a
reproducible publication.  The older [MathPages discussion](https://www.mathpages.com/home/kmath417.htm)
also treats the full square as open and develops the same centered
arithmetic-progression formulation.

A second MathPages note, [Discordance Impedes Square
Magic](https://www.mathpages.com/home/kmath511/kmath511.htm), isolates the
coefficient-`{2,1,1}` subproblem: three rational right triangles with a common
hypotenuse whose areas lie in arithmetic progression.  It reports no genuine
example, exhibits relaxed examples when the common hypotenuse need not be a
square, and excludes some parameter families through concordant forms, but it
does not give a general proof.  Thus the local `211` scan is bounded evidence
for a previously identified open subproblem, not a new formulation or a
solution of it.

The local scan through center root \(e=5\cdot10^8\) is therefore best viewed as an
independent bounded search in a different height: it exhausts the common
integer denominator \(e\), not the individual rational parameters.  Its zero
`111` count must not be presented as progress on the global existence
question without that distinction.

An independent project by `mystimath` [reports a revalidated B6 search](https://github.com/mystimath/magic-square-of-squares-3x3/blob/main/docs/40-b4-b6-publication-revalidation-2026-07-21.md)
with no full `9/9` candidate through its root-box bound `R = 1,000,000`.
That is useful corroborating computational evidence, but this repository has
not reproduced the run.  Its root-box height is not interchangeable with
either the center-root bound \(e\) or the primitive-hypotenuse bound \(H\)
used by the local scanners.

## Audit of the 2025/2026 nonexistence claim

Oscar Hill's [On Arithmetic Progressions and a Proof of the Nonexistence of
Magic Squares of Squares](https://arxiv.org/abs/2510.08286) claims to settle the problem.
The current arXiv revision is v3 from 7 April 2026.  Its conclusion does not
follow from the displayed argument.

The fatal step is immediately after equations (29) and (30).  Equation (29)
is one scalar equality for the linked numerical parameters of a hypothetical
square.  The paper then observes that its left side contains only even powers
of \(\alpha_{1d}\), compares coefficients with the right side, and concludes
that \(\beta_{1d}^2-\beta_{1n}^2=0\).

Coefficient comparison is valid for a polynomial identity, not for equality
at one parameter value.  From \(P(x_0)=Q(x_0)\), one cannot conclude that the
odd coefficients of \(Q\) vanish merely because \(P\) has no odd powers.  The
other quantities \(N_i\) and \(\beta_i\) are themselves linked to the
\(\alpha\)-data, so they also cannot be held fixed while varying
\(\alpha_{1d}\).  No identity on an infinite or Zariski-dense parameter set is
proved.  A valid completion would need a new Diophantine argument showing that
equation (29) has no admissible solution with \(\beta_1\ne1\).

Therefore this preprint is a claimed solution, not an established proof of
nonexistence.  Finding this gap does not prove that a magic square exists; it
leaves the original problem open.

The same invalid coefficient comparison is present in versions 1, 2, and 3.
The current [OpenAlex record](https://api.openalex.org/works/https://doi.org/10.48550/arxiv.2510.08286)
lists only an unaccepted, unpublished preprint.  No correction, referee
discussion, or journal version was found in the bounded search.

## Two other 2026 preprints

Valentyn Voronsbekher's [On magic hourglasses of squares having no centre of
prime-power or semiprime type](https://doi.org/10.5281/zenodo.21910218)
(Zenodo, 13 August 2026) is directly relevant.  It proves the stronger
statement that even a seven-cell magic hourglass cannot have center root
\(e=p^\alpha\) or \(e=pq\).  Every full magic square contains such an
hourglass.

The prime-power proof uses Gaussian representations and distinct
\(p\)-adic valuations.  The semiprime proof reduces its remaining cases to

\[
A^4-3A^2B^2+B^4=w^2
\]

and the rank-zero elliptic curve \(Y^2=X(X+1)(X+5)\); the curve data agree
with [LMFDB 80.a2](https://www.lmfdb.org/EllipticCurve/Q/80/a/2).  A spot
audit found the argument coherent, but the work is unrefereed.  The author
also discloses that the elliptic-curve portion was AI-generated and then
checked in Magma and PARI/GP.  The squarefree-semiprime result in this
directory therefore has a stronger known antecedent, although its elementary
four-offset proof is different and specific to full magic squares.

Hiroki Fukui's [Nonexistence of 3x3 Magic Squares of Squares,
v2.0](https://doi.org/10.5281/zenodo.20265497) is not a valid solution.  Its
bitstring setup treats \(e^2\) as a product of distinct primes, which cannot
represent a nontrivial integer square and loses higher Gaussian exponents.
It also states \(r_2(2p_1p_2)=36\), whereas the sum-of-two-squares formula
gives \(4(1+1)(1+1)=16\).  These are structural, not cosmetic, errors.

## Geometric work in progress

Ben D. Singer, mentored by Asher Auel, reports Hodge numbers, an explicit
Picard basis, the Néron-Severi group, and the algebraic Brauer group of the
magic-square surface in the [YMC 2025 abstract
book](https://ymc.osu.edu/sites/default/files/2025-07/Young%20Mathematicians%20Conference%202025%20Abstract%20Book.pdf#page=7).
The proposed next step is a Brauer-Manin obstruction on the relevant open
surface.  No associated paper or arXiv preprint was located.

## Overlap with the block-balance argument

No equivalent of the quantitative bound in
[block-balance.md](block-balance.md) was found in the checked papers and
preprints.  This is a bounded negative search, not evidence of priority or
novelty.  Its ingredients overlap substantially with prior work:

- restrictions \(p\mid e\Rightarrow p\equiv1\pmod4\);
- allocation of split primes in \(\mathbb Z[i]\);
- minimum-valuation arguments for admissible differences; and
- the pure prime-power exclusion, now also in Voronsbekher's preprint.

What is different in the local note is the quantitative restriction on each
prime-power block in a center with arbitrary additional prime factors, plus
the \(\sqrt3\), \(\sqrt2\), exact-quotient, and compatible composite-block
refinements.  No originality claim should be made without a systematic
MathSciNet/zbMATH search and expert review.

The same bounded search found no source stating the arbitrary-exponent
two-block exclusion
\[
 e=p^kq^\ell.
\]
Voronsbekher's stated two-prime result is the squarefree case \(e=pq\);
the proof in [two-block-exponent-one.md](two-block-exponent-one.md) allows
both exponents to be arbitrary.  This distinction is mathematically
substantive, but a negative phrase/title search is not a priority search and
does not justify a novelty claim.
