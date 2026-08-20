# Research report

Build the report from the repository root with:

```sh
make paper
```

The build uses Tectonic and writes temporary files to `paper/build/`. The
versioned PDF at `paper/prime-support-restrictions.pdf` is copied from that
build after validation.

The report is an overview and proof index. Detailed line-by-line derivations
and the exact finite classifiers remain in `research/prime-support/` so that
they can be reviewed and changed independently.

