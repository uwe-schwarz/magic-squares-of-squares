#!/usr/bin/env python3
"""Genus via the best plane model: eliminate the lowest-degree variable.

The pattern equations have degrees (8, 4, 3-4) in (t1, t2, t3).  The
original ledger (curve_genus.py) eliminated t3, producing components of
degree up to 92 whose Singular normalization exceeds 4 h.  But the genus
is a birational invariant: eliminating t2 (degree 4 in both equations)
gives another plane model of the SAME curve, typically irreducible of
degree around 23, which normalizes in seconds.

For every class and every distinct degree table of the t3-model, this
driver computes the t2-eliminated curve, factors it, and normalizes
every component of degree >= 3 in Singular (lines/conics are genus 0 by
degree).  Results are written incrementally to curve_genus2.json,
including the model degrees.  For the CFF classes the t2-model genera
must reproduce the committed t3-model values 78/105 -- the
model-independence cross-check.

Requires Singular on PATH.
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
from torus_curve import T1, T2, T3, pattern_equations  # noqa: E402
from curve_genus import singular_genus  # noqa: E402

LEDGER = HERE / "curve_genus2.json"


def m2_poly(terms):
    mons = []
    for c, i, j, k in terms:
        m = []
        if i:
            m.append(f"x^{i}")
        if j:
            m.append(f"y^{j}")
        if k:
            m.append(f"z^{k}")
        mons.append(f"({c})*{'*'.join(m)}" if m else f"({c})")
    return " + ".join(mons).replace("+ -", "- ")


def homogenize(f, varpair, target_vars):
    """(terms for the projectivized polynomial in x,y,z)."""

    p = sp.Poly(f, *varpair)
    d = p.total_degree()
    return [(int(c), i, j, d - i - j) for (i, j), c in p.terms()]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timeout", type=int, default=1800)
    args = parser.parse_args()

    table = [c for c in load_table_classes() if not c["excluded"]]
    deg = json.loads((HERE / "torus_curve_degrees.json").read_text())
    ledger: dict = {}
    if LEDGER.exists():
        ledger = json.loads(LEDGER.read_text())
    for c in table:
        if c["form"] in ledger and all(
            not t.get("partial") for t in ledger[c["form"]]["tables"].values()
        ) and ledger[c["form"]]["tables"]:
            continue
        print(f"building curves for {c['form']}", flush=True)
        tables = {tuple(v) for v in deg[c["form"]]["degrees"].values()}
        entry: dict = ledger.get(c["form"], {}).get("tables", {})
        done_tables = {
            tuple(int(x) for x in k.split("+"))
            for k in entry
            if not entry[k].get("partial")
        }
        for want in sorted(
            tables - done_tables, key=lambda t: (len(t), sum(t))
        ):
            done = False
            pat = None
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
                            if tuple(deg[c["form"]]["degrees"][key]) == want:
                                pat = (e1, e2, e3, swap)
                                done = True
                                break
            eq1, eq2 = pattern_equations(c["idx"], *pat)
            res2 = sp.resultant(sp.Poly(eq1, T2), sp.Poly(eq2, T2))
            facs = sp.factor_list(res2.as_expr())[1]
            info = []
            for f, mult in facs:
                d = int(sp.Poly(f, T1, T3).total_degree())
                mult = int(mult)
                if d <= 2:
                    info.append(
                        {"model_degree": d, "mult": mult, "genus": 0,
                         "note": "line/conic: genus 0 by degree"}
                    )
                    continue
                started = time.time()
                try:
                    g = singular_genus(
                        homogenize(f, (T1, T3), None), args.timeout
                    )
                except (subprocess.TimeoutExpired, RuntimeError) as exc:
                    info.append(
                        {"model_degree": d, "mult": mult,
                         "error": str(exc)[:150]}
                    )
                    print(f"{c['form']} t2-model deg {d}: FAILED {exc}",
                          flush=True)
                    continue
                info.append(
                    {"model_degree": d, "mult": mult, "genus": g,
                     "seconds": round(time.time() - started, 1)}
                )
                print(
                    f"{c['form']} t3-table {want} pattern {pat}: "
                    f"t2-model component degree {d} x{mult} -> genus {g} "
                    f"({info[-1].get('seconds')}s)",
                    flush=True,
                )
                # save after every component so interrupted runs resume
                # mid-class (mark the table partial until fully scanned)
                entry["+".join(str(x) for x in want)] = {
                    "pattern": list(pat),
                    "components": list(info),
                    "partial": True,
                }
                ledger[c["form"]] = {"role": c["role"], "tables": entry}
                LEDGER.write_text(json.dumps(ledger, indent=2) + "\n")
            entry["+".join(str(x) for x in want)] = {
                "pattern": list(pat),
                "components": info,
            }
            ledger[c["form"]] = {"role": c["role"], "tables": entry}
            LEDGER.write_text(json.dumps(ledger, indent=2) + "\n")
        print(f"recorded {c['form']}", flush=True)
    print(f"ledger written to {LEDGER}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
