"""
RNA-Seq preprocess & QC (from bioinformatics_pipeline).
Snakemake-compatible: uses snakemake object when present.
"""

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import sys


def run_preprocess_qc(in_file: str, out_counts: str, out_plot: str) -> None:
    df = pd.read_csv(in_file, index_col=0)
    print("Count matrix shape:", df.shape)
    print("First 5 rows:")
    print(df.head())
    print("\nSummary statistics:")
    print(df.describe())
    print("\nMissing values per sample:")
    print(df.isnull().sum())
    library_sizes = df.sum(axis=0)
    print("\nLibrary sizes:")
    print(library_sizes)
    plt.figure(figsize=(6, 4))
    sns.barplot(x=library_sizes.index, y=library_sizes.values, palette="Blues_d")
    plt.ylabel("Total Counts")
    plt.title("Library Size per Sample")
    plt.tight_layout()
    plt.savefig(out_plot)
    cleaned = df.fillna(0).astype(int)
    cleaned.to_csv(out_counts)
    print(f"\nCleaned count matrix saved as {out_counts}")


if __name__ == "__main__":
    if "snakemake" in globals():
        in_file = snakemake.input[0]  # noqa: F821
        out_counts = snakemake.output[0]  # noqa: F821
        out_plot = snakemake.output[1]  # noqa: F821
    else:
        if len(sys.argv) != 4:
            print("Usage: python preprocess_qc.py <in_csv> <out_counts> <out_plot>")
            sys.exit(1)
        in_file, out_counts, out_plot = sys.argv[1:4]
    run_preprocess_qc(in_file, out_counts, out_plot)
