from __future__ import annotations

import argparse
import json
from pathlib import Path
import pandas as pd

from .attribution import classify_b1, classify_b2, classify_b3, classify_b4, classify_b5
from .io import row_to_evidence
from .scoring import macro_f1, abstention_rate, paired_bootstrap_b5_vs_best_previous
from .constants import BOOTSTRAP_SEED
CLASSIFIERS = {
    "B1": classify_b1,
    "B2": classify_b2,
    "B3": classify_b3,
    "B4": classify_b4,
    "B5": classify_b5,
}

def cmd_attribute(args):
    df = pd.read_csv(args.input, sep="\t")
    fn = CLASSIFIERS[args.layer]
    df["prediction"] = [fn(row_to_evidence(row)) for _, row in df.iterrows()]
    df.to_csv(args.output, sep="\t", index=False)

def cmd_score(args):
    df = pd.read_csv(args.input, sep="\t")
    y = df[args.truth_column].tolist()
    preds = {k: df[k].tolist() for k in args.layers}
    point = {
        k: {
            "macro_f1": macro_f1(y, preds[k]),
            "abstention": abstention_rate(preds[k]),
        }
        for k in args.layers
    }
    result = {"point": point}
    if all(k in preds for k in ["B1","B2","B3","B4","B5"]):
        result["paired_bootstrap"] = paired_bootstrap_b5_vs_best_previous(
            y,
            preds,
            n_boot=args.bootstrap,
            seed=args.seed,
        )
    Path(args.output).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

def main():
    p = argparse.ArgumentParser(prog="graph-valid")
    sub = p.add_subparsers(dest="command", required=True)

    a = sub.add_parser("attribute")
    a.add_argument("--input", required=True)
    a.add_argument("--output", required=True)
    a.add_argument("--layer", choices=sorted(CLASSIFIERS), required=True)
    a.set_defaults(func=cmd_attribute)

    s = sub.add_parser("score")
    s.add_argument("--input", required=True)
    s.add_argument("--truth-column", default="truth")
    s.add_argument("--layers", nargs="+", default=["B1","B2","B3","B4","B5"])
    s.add_argument("--bootstrap", type=int, default=10000)
    s.add_argument("--seed", type=int, default=BOOTSTRAP_SEED)
    s.add_argument("--output", required=True)
    s.set_defaults(func=cmd_score)

    args = p.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
