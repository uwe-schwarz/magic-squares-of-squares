# Center-offset relation scan

## Status and exact claim

This note records a deterministic bounded search. It is an empirical
falsification result, not a proof of global nonexistence or a novelty claim.

For a center root `e`, define

\[
S_e=\{d>0:e^2-d\text{ and }e^2+d\text{ are integer squares}\}.
\]

The completed scan exhausts every integer

\[
1\le e\le5\mathbin{\cdot}10^8
\]

and every element of `S_e`. It found:

- no three distinct offsets with a signed relation whose coefficient
  magnitudes are `{1,1,1}`;
- no three distinct offsets with a signed relation whose coefficient
  magnitudes are `{2,1,1}`;
- consequently, no full configuration `{a,b,a+b,|a-b|}`.

The first two statements are stronger than only checking the full
four-offset condition. For sorted positive values `x<y<z`, the scanner checks
all possible forms:

\[
x+y=z
\]

and

\[
2x+y=z,\qquad x+2y=z,\qquad x+z=2y.
\]

The output calls these `111` and `211` relation events. A relation can be
counted more than once through different ordered pair identities, so a
positive event count would not be a count of equivalence classes. A zero event
count is unambiguous: no such triple exists.

## Reproduction

```sh
cd magic-square-of-squares

clang++ -O3 -std=c++20 -Wall -Wextra -pedantic \
  center_relation_search.cpp -o /tmp/center_relation_search

/tmp/center_relation_search --self-test
python3 -m unittest -v test_center_relation_search.py
/tmp/center_relation_search 500000000 5000000
```

The two numeric arguments are the inclusive center-root limit and processing
block size. The exhaustive run reported:

```text
limit=500000000
block_size=5000000
primitive_triples=79577444
scaled_representations=1484878624
expected_scaled_representations=1484878624
centers_with_representations=386902588
expected_centers_with_representations=386902588
representation_count_failures=0
duplicate_offset_failures=0
offset_pair_tests=9752671373
relation_111_events=0
relation_211_events=0
full_candidates=0
eligible_primitive_centers=36533765
eligible_centers_with_at_least_4_offsets=23355653
eligible_four_rejected_by_original_constant_2=19567536
eligible_four_rejected_by_universal_sqrt3=19754486
eligible_four_rejected_by_sqrt3_plus_p5mod8_sqrt2=19888247
relation_examples=0
```

The filter counters are diagnostics only. The relation search itself includes
all centers, including even and nonprimitive ones, and does not rely on a
block-balance filter.

## Enumeration completeness

Every nonzero representation

\[
u^2+v^2=e^2
\]

comes from a scaled primitive Pythagorean triple. The scanner generates every
primitive triple with Euclid's coprimality and opposite-parity conditions,
then applies every scale whose hypotenuse lies in the current center block.
It records

\[
d=2uv,
\]

which gives

\[
(u-v)^2=e^2-d,
\qquad
(u+v)^2=e^2+d.
\]

As an independent global count, if

\[
e=\prod p^{k_p},
\]

then

\[
|S_e|=
\frac{\prod_{p\equiv1\pmod4}(2k_p+1)-1}{2}.
\]

The generated total and number of centers with nonempty `S_e` exactly match
the independently accumulated formula totals. Every individual center also
has the expected count, and no duplicate offset was generated.

Processing is blockwise only to bound memory. The primitive-triple list is
global, every legal scale interval is recomputed exactly for each block, and
records are sorted by `(e,d)` before analysis. The program is single-threaded;
there is no parallel merge or shard boundary.

## Crosschecks and positive tests

[test_center_relation_search.py](test_center_relation_search.py) independently
enumerates the lower square root `t` and tests whether

\[
2e^2-t^2
\]

is a square. Through `e=500`, its offset, pair, relation, full-configuration,
and filter counters match the C++ program exactly.

The C++ `--self-test` uses the synthetic set `{1,2,3,5}` to produce positive
`111`, `211`, and full four-offset detections, and `{10,23,41}` as a negative
control. This checks that the production zero is not caused by disabled or
inverted relation logic.

An AddressSanitizer and UndefinedBehaviorSanitizer build passed both the
self-test and the full scan through `e=10^6`.

## Integer-range audit

The executable rejects limits above `5*10^8`, the audited bound. At that
bound:

- Euclid parameters and center roots fit in 32-bit unsigned integers;
- Pythagorean legs are promoted before scaling;
- `u`, `v`, and every offset use 64-bit unsigned integers;
- `d<e^2<=2.5*10^17`;
- every tested linear combination is below `7.5*10^17`;
- factor blocks and all squared block-balance comparisons remain below
  `7.5*10^17`.

These are well below the 64-bit unsigned limit. The small-prime-factor table
is indexed only through the validated center bound.

## Interpretation

A hypothetical magic square in this range would supply four offsets
`{a,b,a+b,|a-b|}` and therefore several forbidden triples of the types tested.
The scan rules that out for `e<=5*10^8`. It says nothing definitive about
larger centers and is not a proof that either kind of triple is globally
impossible.
