#!/usr/bin/env python3
"""Generate sample count matrix and gene annotation for RNA-Seq pipeline demo."""

import random
from pathlib import Path

import pandas as pd

# Run from project root: python scripts/generate_rna_seq_sample.py
BASE = Path(__file__).resolve().parents[1]
DATA = BASE / "workflows" / "snakemake" / "data"
DATA.mkdir(parents=True, exist_ok=True)

random.seed(42)
genes = [f"Gene_{i}" for i in range(500)]
samples = ["Sample_A1", "Sample_A2", "Sample_B1", "Sample_B2"]
counts = pd.DataFrame(
    {s: [random.randint(0, 1000) for _ in genes] for s in samples},
    index=genes,
)
counts.to_csv(DATA / "sample_counts.csv")
print(f"Wrote {DATA / 'sample_counts.csv'}")

ann = pd.DataFrame({"gene_id": genes, "gene_symbol": [g.replace("Gene_", "G") for g in genes]})
ann.to_csv(DATA / "gene_annotation.csv", index=False)
print(f"Wrote {DATA / 'gene_annotation.csv'}")
