from pathlib import Path
import sys
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from graph_valid.io import row_to_evidence
from graph_valid.attribution import classify_b4, classify_b5

df = pd.read_csv(ROOT / "examples" / "example_evidence.tsv", sep="\t")
df["B4"] = [classify_b4(row_to_evidence(row)) for _, row in df.iterrows()]
df["B5"] = [classify_b5(row_to_evidence(row)) for _, row in df.iterrows()]
print(df[["case_id", "B4", "B5"]].to_string(index=False))
