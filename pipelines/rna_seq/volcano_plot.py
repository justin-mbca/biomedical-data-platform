"""
Volcano plot from annotated DESeq2 results (from bioinformatics_pipeline).
Snakemake-compatible.
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import sys


def run_volcano_plot(in_file: str, out_file: str) -> None:
    df = pd.read_csv(in_file)
    df["-log10(pvalue)"] = -np.log10(df["pvalue"].replace(0, 1e-300))
    plt.figure(figsize=(8, 6))
    plt.scatter(df["log2FoldChange"], df["-log10(pvalue)"], c="grey", alpha=0.7, s=10)
    plt.xlabel("log2 Fold Change")
    plt.ylabel("-log10(p-value)")
    plt.title("Volcano Plot")
    plt.tight_layout()
    plt.savefig(out_file)
    print(f"Volcano plot saved to {out_file}")


if __name__ == "__main__":
    if "snakemake" in globals():
        in_file = snakemake.input[0]  # noqa: F821
        out_file = snakemake.output[0]  # noqa: F821
    else:
        if len(sys.argv) != 3:
            print("Usage: python volcano_plot.py <annotated_csv> <out_png>")
            sys.exit(1)
        in_file, out_file = sys.argv[1:3]
    run_volcano_plot(in_file, out_file)
