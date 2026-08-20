# Contributing

This project welcomes mathematical review, corrections, counterexamples, and
reproducibility improvements.

## Mathematical reports

Please include:

1. the file, section, equation, or theorem affected;
2. the first step that does not follow;
3. an explicit counterexample, calculation, or reference when available;
4. whether the issue changes a theorem, only its proof, or only exposition.

A small failing test is ideal for errors in the finite classifiers or search
programs. A mathematical objection does not need code.

## Scope discipline

The unrestricted `3 x 3` problem is open. Do not describe a bounded search, a
necessary signature filter, or one prime-support exclusion as a solution of
the full problem. New claims should distinguish clearly among:

- a proved theorem;
- a machine-assisted finite classification;
- bounded computational evidence;
- a conjecture or heuristic;
- an unresolved proof gap.

## Development

Run the regression suite before proposing code changes:

```sh
make test
```

Source code, identifiers, comments, tests, and technical documentation should
remain in English. Keep generated build files out of commits, except for the
versioned report PDF.

