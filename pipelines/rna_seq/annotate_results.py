"""
Annotate DESeq2 results with gene symbols (from bioinformatics_pipeline).
Placeholder: merge with annotation file. Production: use biomaRt or Ensembl API.
"""

import pandas as pd
import sys


def run_annotate(results_csv: str, annotation_csv: str, out_csv: str) -> None:
    df = pd.read_csv(results_csv)
    try:
        ann = pd.read_csv(annotation_csv)
        if "gene_id" in ann.columns and "gene_id" in df.columns:
            df = df.merge(ann, on="gene_id", how="left")
        elif "gene_symbol" not in df.columns and "gene_symbol" in ann.columns:
            df["gene_symbol"] = ann["gene_symbol"].iloc[0] if len(ann) else ""
    except Exception:
        df["gene_symbol"] = df.get("gene_id", df.index if hasattr(df.index, "tolist") else "unknown")
    df.to_csv(out_csv, index=False)
    print(f"Annotated results saved to {out_csv}")


if __name__ == "__main__":
    if "snakemake" in globals():
        inp = snakemake.input  # noqa: F821
        results_csv = inp.results if hasattr(inp, "results") else inp[0]
        annotation_csv = inp.annotation if hasattr(inp, "annotation") else inp[1]
        out_csv = snakemake.output[0]  # noqa: F821
    else:
        if len(sys.argv) != 4:
            print("Usage: python annotate_results.py <results> <annotation> <out>")
            sys.exit(1)
        results_csv, annotation_csv, out_csv = sys.argv[1:4]
    run_annotate(results_csv, annotation_csv, out_csv)
