# The multimagie.com lineage: primary-source record

Review date: 2026-08-22. Sources read in full: Christian Boyer's main page
`http://multimagie.com/English/SquaresOfSquares.htm`, his "Latest research"
page `SquaresOfSquaresSearch.htm`, and three downloadable preprints hosted
there: Buell (1999/2004), Woll (2017), and Pierrat–Thiriet–Zimmermann (2015).
This note records exactly what is known publicly, corrects two commonly
garbled citations, and states how each item relates to this repository's
scans and rigidity results.

## Buell 1999 (posted 2004): the hourglass search

Buell searched for a *magic hourglass*: entries a±b, a±c, a±d around center
a with the two horizontal lines and the three lines through the center all
equal. Writing a = A², every "primitive-type" offset has the form
b = 4mn(m²−n²) with A = m²+n², and the hourglass condition collapses to the
single signed relation b + c + d = 0 among three offsets, i.e. a {1,1,1}
relation. His pipeline: enumerate A with at least three representations,
filter the relation mod 2^16, then rank survivors by the highest power of 2
the congruence survives (best found: mod 2^46).

**Theorem 1.1 (Buell):** no magic hourglass with a < 25·10^24 arises this
way, from a complete scan of A ≤ 5·10^12.

**Scope caveat, confirmed from the parametrization itself:** requiring the
three offsets to come from representations of A captures only Gaussian
divisors t with t | A in Z[i]. General offsets d ∈ S_A use divisors t of A²
that do not divide A — equivalently, lines whose three entries share a
common factor. Zimmermann et al. state this gap explicitly. Example
(validated by hand during this review): for A = 65, the offset d = 3000
(65² ± 3000 = 35², 85²) comes from t = 39+52i with N(t) = 65², and no pair
(m,n) with m²+n² = 65 produces it. So Buell's theorem covers coprime-line
hourglasses only; his bound does not subsume this repository's all-offset
center scan, which reaches only e ≤ 5·10^8 but misses no offsets.

## Pech 2006

Extended Buell's method to A ≤ 10^13 (same coprime framework); best 2-adic
example mod 2^52.

## Morgenstern (2006–2014), per Boyer's chronology

- 2006: if a 3×3 magic square of distinct squares exists, every entry
  exceeds 10^14. This remains the strongest published entry-size bound and
  is consistent with (but far beyond) our scans.
- 2011–2012: constructed a full 3×3 magic square of squares modulo 2^90 —
  strictly stronger 2-adically than any hourglass example.
- 2014: enumerated all primitive arithmetic progressions of squares
  (step d = 4mn(m²−n²), m,n coprime, opposite parity, n < m < 2^24) up to
  common difference d = 6.0·10^23, checking hourglass-type relations; no
  solution. Also three further hourglass searches (June 2014), no solution.

## Pierrat–Thiriet–Zimmermann 2015: the fix and the modular facts

Three results that matter here.

**Lemma 1.** For a *primitive* 3×3 magic square of squares: the magic sum
is 3 mod 72 and every (square) entry is 1 mod 24. The same constraints hold
for the hourglass, Boyer's enigma 1, and all configurations 7.I–7.VIII
(from Boyer's 2004 search paper). Also the magic sum is not divisible by 7
or 11. In our centered language: 24 divides every offset d for primitive
solutions — a small-prime companion to our rigidity divisibility.

**Theorem 1.** A complete parametrization of *all* three-term APs of
squares x², A², y² including shared factors: for each square-free p ≡ 1
(mod 4) dividing A, decompose A/p = m² + p·n² (m even, n odd); then the
step is p²·4mn(m²−n²). The decomposition is unique. This is exactly the
gap in Buell's search, closed: imprimitive offsets are p²-scaled.

**Search.** With shared factors allowed they find genuine hourglasses
modulo 2^57 (e.g. center A = 1,289,865,125, with per-line factors
p = 5, t = 1, w = 1), three solutions mod 2^56 below A = 5·10^12, and a
7.VI configuration mod 2^59. Conclusion: the coprime and shared-factor
families behave differently 2-adically, and only the latter is the honest
setting.

## Roberts 2013 / Underwood 2014: offset divisibility

Working in precisely this repository's centered parametrization
(neighbors x±y, x±z, x±(y+z), x±(y−z) of x = e²), via mod-p analysis:

- mod 13: all nine cells squares forces (x, y, 0) or (x, 0, z) mod 13 —
  the same "torus collapses" phenomenon our rigidity theorems exploit;
- y·z is divisible by 2^6·3²·5²·7²·11·13·19·31 = 59,430,571,200;
- x·y·z is divisible by every prime < 40 except 23;
- x·y·z·(y+z)·(y−z) is divisible by
  2^13·3^5·5²·7²·11·13·17·19·23·29·31·37·41·43·47·53·61·67 ≈ 1.5·10^30
  — every prime below 70 except 59;
- they list 106 integers n ≤ 1608 such that at least one of
  x, y, z, y+z, y−z is divisible by n;
- Underwood sharpens: y and z are each divisible by 24, hence so are
  y±z, forcing 24^4 | y·z·(y+z)·(y−z) and refinements to 2^13·3^5.

## Woll 2017: the Gaussian hourglass

Woll proves: a magic hourglass of distinct squares exists iff (up to a
square-root rescaling in the converse) there are three distinct
non-real Gaussian integers of equal norm with z1⁴ + z2⁴ + z3⁴ real; the
hourglass entries are the real and imaginary parts of (1+i)z² and the
common norm squared. This is exactly this repository's S_e / offset
formulation of the {1,1,1} relation (three offsets of the same center with
a signed vanishing sum), derived independently. His "too difficult"
converse mirrors our S-unit normalization frustrations.

## Other recorded items (Boyer's pages)

- Rathbun 2017: the elliptic curve behind the 7-square example has rank 4.
- Labruna 2018 (thesis): magic squares of squares over finite fields;
  together with Morgenstern's mod-2^90 example this implies the solution
  variety has points everywhere locally — no single-modulus argument can
  ever prove impossibility outright.
- Woll 2018/2019 and Cain 2019: Gaussian-integer and ring-theoretic
  existence studies; the Math Intelligencer 2019 note.
- Proved dichotomy: a degenerate (non-distinct) square can have only 1 or
  3 distinct values among its entries, and a solution with 3 distinct
  values exists for any center of the form
  n²·5·13·17·(4k+1)-type products (the 3-distinct-value family).
- Buell is also credited on Boyer's main page with: any solution has
  center > 25·10^24 (in the coprime setting as discussed above).

## Synthesis for this repository

1. **Complementarity of scans.** Buell/Pech cover all centers to
   5·10^12/10^13 but only coprime-line offsets; the repo's center scan and
   our coupled scans cover all offsets but only e ≤ 5·10^8 exhaustively
   (plus the complete p²qr family through p,q,r ≤ 10^4 and the
   survivors-only family to 5.5·10^4, all offsets). Zimmermann's 2^57
   hourglass shows the shared-factor family is where 2-adic richness
   lives, i.e. the family our scanners target is the right one.

2. **Independent cross-validation of rigidity.** Our torus sweep found the
   rigid primes for surviving classes to be a subset of
   {7, 11, 13, 17, 19, 29, 31, 37, 43, 53, 67, 89, 103, 127}, with 23 and
   59 *not* rigid for any class. Roberts–Underwood independently found 23
   escaping the xyz-level analysis and 59 escaping everything — the escape
   primes match exactly. Where they force divisibility of the five-term
   product by every prime < 70 except 59, our per-class result forces
   divisibility of *all four offsets simultaneously* by the class's rigid
   product (up to 7·17·31·89·103·127 ≈ 4.29·10^9), including primes 89,
   103, 127 beyond their range. The two computations used different models
   (their direct residue analysis vs our norm-one torus reduction of the
   monomial system) and agree wherever they overlap.

3. **Stacked necessary divisibility.** Any primitive solution must have
   24 | every offset (Zimmermann + Underwood) and, per class, the rigid
   product | every offset (our rigidity.md). Future scans can prune on
   this: offsets must be divisible by 24 · (class rigid product).

4. **Strategic conclusion.** Morgenstern's mod-2^90 square plus
   finite-field existence results close the door on pure local
   contradictions: rigidity-style analysis can only ever produce necessary
   divisibility structure, never a bare impossibility. Any eventual proof
   must be global (height bounds, descent, or S-unit theory applied to the
   coupled system), and any search must exploit the stacked divisibility
   to have a chance beyond the 10^14 wall.

## File provenance

- Buell PDF: `multimagie.com/Buell.pdf` (4 pages, July 1, 2004 v2;
  text recovered by OCR from page images due to non-standard font
  encoding).
- Woll PDF: `multimagie.com/Woll.pdf` (June 2017).
- Zimmermann PDF: `members.loria.fr/PZimmermann/papers/squares.pdf`
  (March 13, 2015).
- Boyer pages fetched 2026-08-22; his chronology is the dating authority
  for items not read in the original.
