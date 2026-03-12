#!/usr/bin/env python3
"""Generate synthetic oncology patient data for dashboard demo."""

import random
from pathlib import Path

import pandas as pd

OUT = Path(__file__).resolve().parents[1] / "data" / "synthetic_oncology_patients.csv"
OUT.parent.mkdir(parents=True, exist_ok=True)

random.seed(42)
n = 100
df = pd.DataFrame({
    "patient_id": [f"P{i:05d}" for i in range(n)],
    "age": [random.randint(35, 85) for _ in range(n)],
    "gender": random.choices(["M", "F"], k=n),
    "cancer_type": random.choices(["Breast", "Lung", "Colorectal", "Prostate", "Melanoma"], k=n),
    "stage": random.choices(["I", "II", "III", "IV"], k=n),
    "biomarker_status": random.choices(["Positive", "Negative", "Unknown"], k=n),
    "treatment": random.choices(["Chemotherapy", "Immunotherapy", "Targeted", "Surgery", "Radiation"], k=n),
    "survival_months": [random.randint(6, 60) for _ in range(n)],
})
df.to_csv(OUT, index=False)
print(f"Generated {len(df)} synthetic patients → {OUT}")
