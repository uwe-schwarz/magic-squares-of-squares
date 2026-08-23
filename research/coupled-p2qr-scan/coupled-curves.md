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
degenerate class-triples.  The committed exhaustive scans bound the
*norms* of the generators (`p, q, r <= 2*10^4`); this search bounds the
*arguments* -- a genuinely new axis, and by the scaling remark in Section
1 an empty candidate set at height `H` cannot be contradicted by any
entry-size bound (a hit would scale to arbitrarily large entries).

## 4. Next steps

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
