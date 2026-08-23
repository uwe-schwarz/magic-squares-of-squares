# The coupled curves: slope coordinates and the rational-point problem

## Status

This note records the 2026-08-23 reduction of the sixteen surviving
`p^2 q r` classes to explicit algebraic curves, the verified
correspondence between rational points and (potential) magic squares, the
committed degree table of the curves, and the first argument-height
search.  Nothing here is a proof of nonexistence and no counterexample is
claimed; the global problem remains open.

## 1. The correspondence

Fix a class with local-index matrix `j` and a fixed-`e0` sign/edge
pattern.  Parametrize each generator quotient `rho = pi/conj(pi)` by the
slope of `pi` itself:

```
rho(t) = (1 + i t)/(1 - i t),   t = Im(pi)/Re(pi).
```

Every rational slope is realized by a Gaussian integer and conversely;
`t -> rho(t)` is exact in `Q(i)`.  The normalized column
`x_c = rho^(2 j_p) sigma^(2 j_q) tau^(2 j_r)` is then a `Q(i)` point at
rational slopes, and the two pattern equations are two polynomials in
`(t1, t2, t3)` after clearing the never-rationally-vanishing factors
`(1 + t^2)`.  Eliminating `t3` (resultant of two quartics) gives a plane
curve `F(t1, t2)`.

Two facts make this correspondence interesting.

**(a) Primality is never needed for the construction.**  For *any*
Gaussian integers `(pi, beta, gamma)` with `N(pi)^2 N(beta) N(gamma) =
e^2`, the monomial `z_c` gives `d_c = |Im(z_c^2)|` in `S_e`
(`e^2 +- d_c = (Re z_c +- Im z_c)^2`), and the pattern equations depend
only on the slopes.  Scaling `pi -> k*pi` changes nothing in the pattern
and freely grows the entries.  Hence a slope triple with all four offsets
nonzero that solves some pattern yields, for every scaling, a genuine
`3 x 3` magic square of (distinct, positive) squares -- a counterexample
to the open problem, *provided* the nine entries check out in
`verify_candidate`.  Conversely:

**(b) Prime-support solutions live on the curves.**  Every solution with
prime `p, q, r = 1 mod 4` is classified by the committed switching-class
machinery into one of the 134 classes, and the sixteen survivors carry
the monomial model above; its slopes are rational.  Therefore:

> If all sixteen classes' curves have only degenerate rational points
> (points whose four `Im(x_c)` all vanish or repeat so that `verify_candidate`
> fails on distinctness), then no magic square of squares with
> prime-support center root `p^2 q r` exists, of any size.

This is the "couple then project globally" attack of the independent
audit, now with exact objects.  Note the honest asymmetry: for
composite-norm centers the sixteen monomial models cover only part of the
configuration space, so the converse implication is one-sided there.

The projection `F` vanishing is *necessary* for a rational solution (the
`t3` fiber may be algebraic only); the correspondence tests pin the
solution-direction, and any candidate from a search is re-verified in
full Gaussian arithmetic before anything is claimed.

## 2. The degree table

`torus_curve.py` builds every pattern's resultant and factors it over
`Q` (ledger: [torus_curve_degrees.json](torus_curve_degrees.json)).  The
outcome is uniform in structure across all sixteen classes: the curve
splits into **small components -- lines and conics -- plus one genuine
coupled component**:

| class (role) | component degrees over the 16 patterns |
| --- | --- |
| `I0:0000/0011/0101` (CFF) | (21) or (23) |
| `I0:0000/0101/0110` (CFF) | (21) or (23) |
| `I2:0000/*001/01*1` (ECE) | (1, 91) or (92) |
| `I2:0000/*001/010*` (ECE) | (1, 87) or (88) |
| `I2:0000/*011/01*1` (ECE) | (1, 91) or (92) |
| `I2:0000/*011/011*` (ECE) | (1, 87) or (88) |
| `I2:0000/0011/01*0` (EFE) | (81) or (92) |
| `I2:0000/0011/010*` (EFE) | (81) or (92) |
| `I2:0000/0011/0101` (EFF) | (23) |
| `I2:0000/01*0/01*1` (EEE) | (1, 1, 1, 80) or (92) |
| `I2:0000/010*/011*` (EEE) | (1, 1, 1, 2, 2, 64) or (92) |
| `I2:0000/0101/*001` (EFC) | (81) or (92) |
| `I2:0000/0101/*011` (EFC) | (81) or (92) |
| `I2:0000/0101/00*1` (EFE) | (92) |
| `I2:0000/0101/01*0` (EFE) | (92) |
| `I2:0000/0101/0110` (EFF) | (23) |

The small components are not noise: they carry the degenerate families.
The line `t1 = 0` is the real-generator locus, and the genus-0 conics of
`I2:0000/010*/011*` carry the **three-distinct-value family** -- the
classical degenerate squares of the multimagie lineage (a non-distinct
square has 1 or 3 distinct values; the 3-value family is parametrizable,
and here it literally sits on rational curves inside the coupled
variety).  The genuine components have degrees 21-92; a smooth plane
curve of degree `d >= 4` already has genus `>= 3`, so if the genuine
components are irreducible of geometric genus `>= 2`, Faltings gives
*finitely many* rational points per (class, pattern) -- the next target
of this attack (singularity analysis pending; see Section 4).

## 3. The argument-height search

[slope_search.py](slope_search.py) enumerates rational slope triples
`b/a`, `0 <= b <= a <= bound`, over all 16 classes and all 16 patterns,
in exact `Fraction` arithmetic, and classifies hits:

- fully degenerate (all four `Im = 0`): the trivial all-equal square;
- exactly one zero offset: the three-distinct-value family (counted,
  sampled, not candidates);
- all four offsets nonzero: a **candidate**, immediately re-embedded and
  run through `verify_candidate`; a pass would be a counterexample.

Verified outcome at `bound = 12` (46 slopes, 103,823 triples, 16
classes): **zero candidates**; 1,128 three-value hits; 25 fully
degenerate class-triples.  At `bound = 20` (129 slopes, 2,146,689
triples, ~1.6 h): **zero candidates**, 3,096 three-value hits (ledger
[slope_search_20.json](slope_search_20.json)).  The committed exhaustive
scans bound the *norms* of the generators (`p, q, r <= 2*10^4`); this
search bounds the *arguments* -- a genuinely new axis, and by the
scaling remark in Section 1 an empty candidate set at height `H` cannot
be contradicted by any entry-size bound (a hit would scale to
arbitrarily large entries).

## 4. Finiteness (Faltings)

The computational pillars of a finiteness theorem per class, all
machine-verified:

**(i) Exceptional components are unrealizable or empty.**  The only
pattern-curve components that are not genuine coupled curves are lines
`t1 = 0` (the ECE classes and `I2:0000/01*0/01*1`), the lines
`t1 = +-1` (both EEE classes), and the two vertical conics
`t1^2 +- 2 t1 - 1` (`I2:0000/010*/011*` only).  A generator slope of
`0` or `+-1` forces its norm to be a square or twice a square -- never
an odd prime `= 1 mod 4` -- so prime-support points avoid every line;
the conics have no rational point at all (their `t1`-values are
`1 +- sqrt(2)`).

**(ii) Genuine components have high genus.**  The normalization genus of
each projectivized `Q`-irreducible genuine component, computed by
Singular (`normal.lib`, driver [curve_genus.py](curve_genus.py), ledger
[curve_genus.json](curve_genus.json)): the CFF components (degree 21 and
23) have genus **78** and **105**.  (The remaining classes' components,
degree 64-92, are being normalized in a running batch; the ledger is
written incrementally and this section is updated as they land.)
Geometrically reducible components would also give finiteness (rational
points of a `Q`-irreducible but geometrically split curve lie in
conjugate-intersections), so genus `>= 2` is a sufficient, not necessary,
record.

**(iii) The `t3`-fiber is finite at every realizable point.**  The two
`t3`-quartics vanish identically only at `(t1, t2)` in
`{(0, 0), (0, +-1)}`, and only for eight mixed-sign patterns of the two
EFC classes (full 16 x 16 sweep, 2026-08-23) -- points on the excluded
real-generator line with excluded `t2`-slope.  Everywhere else the fiber
has at most 16 points.

**Theorem (finiteness, status: verified for the two CFF classes).**
For each class whose genuine components all have normalization genus
`>= 2`: only finitely many rational slope triples solve its patterns
outside the excluded lines (Faltings on each component, plus (iii));
each slope triple corresponds to at most finitely many prime-support
generator triples (the primitive representative is unique up to units);
hence the class has at most **finitely many** prime-support `p^2 q r`
realizations, of any size.  Stated honestly: this is finiteness, not
emptiness -- exhibiting or excluding the finitely many points per curve
(Chabauty / Mordell-Weil sieve) is the next step, and the
argument-height searches (Section 3) found none through bound 20 for the
full sweep direction.

## 4b. The six-point grid: rational points of the CFF curves

[rational_point_search.py](rational_point_search.py) enumerates `t1`
with `0 <= b <= a <= bound` and finds every rational `t2` on each
genuine component with denominator up to `2*10^5`: the specialized
univariate is solved numerically to 40 digits, candidates are
recognized by continued fractions, and every recognition is verified
exactly by substitution (ledger
[rational_points.json](rational_points.json)).

Verified outcome (the four classes with small genuine components -- both
CFF and both EFF -- all 32 distinct pattern curves, `t1`-height `<= 30`):
every genuine component carries **exactly the six rational points**
`{0, 1} x {-1, 0, 1}` -- the same grid for every curve, with no further
rational point of `t2`-denominator `<= 2*10^5` -- and every grid point
has unrealizable `t1` (a square or twice a square norm, never an odd
`1 mod 4` prime).  In particular **no realizable rational point exists
on any CFF/EFF pattern curve with `t1`-height `<= 30` and
`t2`-denominator `<= 2*10^5`**, so no prime-support realization of these
four classes has `t1`-height `<= 30`.  The remaining twelve classes'
curves (genuine degrees 64-92) are being swept at `t1`-height `<= 12`.

Conjecture (emptiness target): the six grid points are the *complete*
rational point sets of the genuine components (all classes).  Combined
with the finiteness theorem this would make every class empty of
prime-support realizations: every prime-support solution projects to a
rational point of some pattern curve, and all such points are
unrealizable.  Proving the conjecture -- Chabauty on a quotient of the
genus-78/105 curves, a covering argument, or a Mordell-Weil sieve
against the known grid -- is the next step of this attack.

## 5. Next steps

1. **Genus of the genuine components.**  Singularity analysis of the
   degree 21-92 factors (and of the degree-21/23 CFF and EFF curves,
   the smallest); geometric genus `>= 2` plus Faltings gives finiteness
   of rational points per class-pattern.  Note the clean classes'
   components (81-92) are the big ones; the rigid classes own the small
   genuine curves.
2. **Structure of the three-value locus.**  The conic components deserve
   exact parametrization -- they are the classical family seen from the
   coupled side, and their intersection with the genuine components
   constrains where degenerate points can lie.
3. **Deeper argument-height searches** (and eventually `t3`-fiber-aware
   curve-point search instead of box search).

## Reproduce

```sh
python3 -m unittest -v test_torus_curve.py   # correspondence + degree pins
python3 slope_search.py --bound 12           # ~4 minutes
python3 torus_curve.py --json /tmp/deg.json  # full degree table (~1 h)
```
