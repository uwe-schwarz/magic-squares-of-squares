#!/usr/bin/env python3
"""Geometric genus of the coupled curves' genuine components (Singular).

For each class and each distinct degree table, one representative pattern
is normalized in Singular (normal.lib::genus) to obtain the geometric
genus of each irreducible factor of the eliminated plane curve,
projectivized.  Components of degree <= 2 (the degenerate lines and the
three-distinct-value conics) are recorded with their degree and genus 0
without invoking Singular (a line/conic over Q has genus 0), except that
conic factors are still passed through Singular when --all is set so the
claim "genus 0" is machine-checked too.

The genus ledger is written incrementally to curve_genus.json so long
batches can be resumed.

Faltings consequence (see coupled-curves.md): a component of geometric
genus >= 2 has only finitely many rational points, hence finitely many
(class, pattern) realizations can lie on it (each (t1, t2) admits at
most finitely many rational t3, the two quartics in t3 having a
zero-dimensional common zero locus unless sharing a factor -- a
degeneracy that would itself split the curve and is caught by the
factorization recorded here).

Requires Singular on PATH; tested with Singular 4.4.0.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from test_coupled_p2qr_scan import load_table_classes  # noqa: E402
from torus_curve import T1, T2, plane_curve  # noqa: E402

LEDGER = HERE / "curve_genus.json"


def homogenized_terms(f, target_degree: int):
    p = sp.Poly(f, T1, T2)
    d = p.total_degree()
    assert d == target_degree
    out = []
    for (i, j), c in p.terms():
        out.append((int(c), i, j, d - i - j))
    return out


def singular_genus(terms, timeout: int) -> int:
    mons = []
    for c, i, j, k in terms:
        m = []
        if i:
            m.append(f"x{i}")
        if j:
            m.append(f"y{j}")
        if k:
            m.append(f"z{k}")
        mons.append(f"({c})*{'*'.join(m) if m else '1'}")
    script = (
        'ring r = 0,(x,y,z),dp;\n'
        "poly f = " + " + ".join(mons).replace("+ -", "- ") + ";\n"
        'ideal i = f;\n'
        'LIB "normal.lib";\n'
        'genus(i);\n'
    )
    script_path = (
        Path("/tmp") / f"genus_{abs(hash(tuple(map(tuple, terms)))) % 10**10}.sin"
    )
    script_path.write_text(script)
    try:
        proc = subprocess.run(
            ["Singular", str(script_path)],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    finally:
        script_path.unlink(missing_ok=True)
    m = re.findall(r"^\s*(\d+)\s*$", proc.stdout, re.M)
    if not m:
        raise RuntimeError(
            f"no genus in output: {proc.stdout[-500:]} {proc.stderr[-300:]}"
        )
    return int(m[-1])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timeout", type=int, default=3600)
    parser.add_argument("--all", action="store_true",
                        help="also normalize degree <= 2 components")
    args = parser.parse_args()

    table = [c for c in load_table_classes() if not c["excluded"]]
    ledger: dict = {}
    if LEDGER.exists():
        ledger = json.loads(LEDGER.read_text())
    for c in table:
        if c["form"] in ledger:
            continue
        deg = json.loads((HERE / "torus_curve_degrees.json").read_text())
        tables = {
            tuple(v) for v in deg[c["form"]]["degrees"].values()
        }
        entry: dict = {}
        for want in sorted(tables, key=lambda t: (len(t), sum(t))):
            # find a pattern with this exact degree table
            done = False
            for swap in (False, True):
                if done:
                    break
                for e1 in (1, -1):
                    if done:
                        break
                    for e2 in (1, -1):
                        if done:
                            break
                        for e3 in (1, -1):
                            key = f"e=({e1},{e2},{e3}),swap={int(swap)}"
                            if (
                                tuple(
                                    deg[c["form"]]["degrees"][key]
                                )
                                == want
                            ):
                                F = plane_curve(
                                    c["idx"], e1, e2, e3, swap
                                )
                                done = True
                                break
                        if done:
                            break
                    if done:
                        break
            facs = sp.factor_list(F)[1]
            info = []
            for f, mult in facs:
                d = int(sp.Poly(f, T1, T2).total_degree())
                mult = int(mult)
                if d <= 2 and not args.all:
                    info.append(
                        {"degree": d, "mult": mult, "genus": 0,
                         "note": "line/conic: genus 0 by degree"}
                    )
                    continue
                started = time.time()
                g = singular_genus(
                    homogenized_terms(f, d), args.timeout
                )
                info.append(
                    {
                        "degree": d,
                        "mult": mult,
                        "genus": g,
                        "seconds": round(time.time() - started, 1),
                    }
                )
                print(
                    f"{c['form']} table {want}: component degree {d} "
                    f"x{mult} -> genus {g} "
                    f"({info[-1].get('seconds')}s)",
                    flush=True,
                )
            entry["+".join(str(x) for x in want)] = {
                "pattern": key,
                "components": info,
            }
        ledger[c["form"]] = {"role": c["role"], "tables": entry}
        LEDGER.write_text(json.dumps(ledger, indent=2) + "\n")
        print(f"recorded {c['form']}", flush=True)
    print(f"ledger written to {LEDGER}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
