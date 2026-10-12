"""Rebuild web/scores.json from data/transactions.csv (columns: actual, risk_score).

Run from the repo root after re-exporting transactions.csv from the notebook:
    python web/build_scores.py
"""
import csv, json, os

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
fraud, legit = [], []
with open(os.path.join(root, "data", "transactions.csv")) as fh:
    for row in csv.DictReader(fh):
        score = round(float(row["risk_score"]), 6)
        (fraud if row["actual"] == "1" else legit).append(score)

out = os.path.join(root, "web", "scores.json")
with open(out, "w") as fh:
    json.dump({"fraud": sorted(fraud), "legit": sorted(legit)}, fh, separators=(",", ":"))
print(f"Wrote {out}: {len(fraud)} fraud, {len(legit)} legitimate")
