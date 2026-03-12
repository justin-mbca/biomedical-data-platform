#!/usr/bin/env python3
"""
Genomics Variant Processing Pipeline

Processes VCF files: QC → annotation → clinical significance → Parquet/Delta.
Usage:
    python -m pipelines.genomics.variant_pipeline --input variants.vcf.gz
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Iterator

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))


def parse_vcf_simple(path: str) -> Iterator[dict]:
    """Simple VCF parser for demonstration. Production: use cyvcf2 or pysam."""
    import gzip
    open_fn = gzip.open if path.endswith(".gz") else open
    mode = "rt" if path.endswith(".gz") else "r"
    
    with open_fn(path, mode) as f:
        header = []
        for line in f:
            if line.startswith("##"):
                continue
            if line.startswith("#"):
                header = line[1:].strip().split("\t")
                continue
            parts = line.strip().split("\t")
            if len(parts) < 8:
                continue
            rec = dict(zip(header[: len(parts)], parts))
            rec["CHROM"] = rec.get("CHROM", "")
            rec["POS"] = int(rec.get("POS", 0))
            rec["REF"] = rec.get("REF", "")
            rec["ALT"] = rec.get("ALT", "")
            rec["QUAL"] = rec.get("QUAL", ".")
            rec["INFO"] = rec.get("INFO", "")
            yield rec


def annotate_variant(rec: dict) -> dict:
    """Placeholder: add annotation fields. Integrate VEP, ANNOVAR, or similar."""
    return {
        "chromosome": rec.get("CHROM", ""),
        "position": rec.get("POS", 0),
        "ref": rec.get("REF", ""),
        "alt": rec.get("ALT", ""),
        "gene": _extract_gene(rec.get("INFO", "")),
        "impact": "unknown",
        "clinical_significance": "uncertain",
        "source_vcf": rec,
    }


def _extract_gene(info: str) -> str:
    """Extract gene from INFO field if present."""
    for part in info.split(";"):
        if part.startswith("GENE="):
            return part.split("=", 1)[1]
    return ""


def run(input_path: str, output_path: str, limit: int | None = None) -> None:
    """Run variant processing pipeline."""
    out_dir = Path(output_path)
    out_dir.mkdir(parents=True, exist_ok=True)
    
    annotated = []
    for i, rec in enumerate(parse_vcf_simple(input_path)):
        if limit and i >= limit:
            break
        annotated.append(annotate_variant(rec))
    
    out_file = out_dir / "variants.parquet"
    try:
        import pyarrow as pa
        import pyarrow.parquet as pq
        # Flatten for Parquet
        rows = [{k: v for k, v in r.items() if k != "source_vcf"} for r in annotated]
        table = pa.Table.from_pylist(rows)
        pq.write_table(table, out_file)
        print(f"Wrote {len(rows)} variants to {out_file}")
    except ImportError:
        with open(out_dir / "variants.json", "w") as f:
            json.dump(
                [{k: v for k, v in r.items() if k != "source_vcf"} for r in annotated],
                f,
                indent=2,
            )
        print(f"Wrote {len(annotated)} variants to {out_dir}/variants.json")
    
    print("Variant pipeline complete.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Genomics Variant Processing Pipeline")
    parser.add_argument("--input", "-i", required=True, help="Input VCF path")
    parser.add_argument("--output", "-o", default="./data/genomics", help="Output directory")
    parser.add_argument("--limit", "-n", type=int, help="Max variants to process")
    args = parser.parse_args()
    run(args.input, args.output, args.limit)


if __name__ == "__main__":
    main()
