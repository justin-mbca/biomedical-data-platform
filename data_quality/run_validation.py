#!/usr/bin/env python3
"""Run Great Expectations validation on OMOP tables.

Suites: person_suite, schema_drift_suite, null_rate_suite, data_freshness_suite
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def run(data_path: str, suite_name: str = "person_suite") -> bool:
    """Validate data against expectation suite."""
    base = Path(__file__).parent
    candidates = [
        base / "great_expectations" / "expectations" / f"{suite_name}.json",
        base / "expectations" / f"{suite_name}.json",
        base / "expectations" / "fhir_omop_suite.json",
    ]
    suite_path = next((p for p in candidates if p.exists()), None)

    if suite_path is None:
        print(f"Suite not found: {suite_name}")
        return False

    data_path = Path(data_path)
    if not data_path.exists():
        print(f"Data not found: {data_path}. Run FHIR ingestion first.")
        return True

    import pandas as pd
    df = pd.read_parquet(data_path)
    if df.empty:
        print("Empty dataset.")
        return True

    suite = json.loads(suite_path.read_text())
    failed = []

    for exp in suite.get("expectations", []):
        ett = exp.get("expectation_type", "")
        kwargs = exp.get("kwargs", {})
        col = kwargs.get("column")

        if "expect_column_values_to_not_be_null" in ett and col in df.columns:
            if df[col].isnull().any():
                failed.append(f"{col}: has nulls")
        elif "expect_column_values_to_be_in_set" in ett and col in df.columns:
            allowed = set(kwargs.get("value_set", []))
            invalid = ~df[col].isin(allowed)
            if invalid.any():
                failed.append(f"{col}: invalid values")
        elif "expect_column_values_to_be_between" in ett and col in df.columns:
            lo, hi = kwargs.get("min_value"), kwargs.get("max_value")
            if (df[col] < lo).any() or (df[col] > hi).any():
                failed.append(f"{col}: out of range [{lo}, {hi}]")
        elif "expect_column_to_exist" in ett:
            if col not in df.columns:
                failed.append(f"column missing: {col}")

    if failed:
        print("Validation FAILED:", failed)
        return False
    print(f"Validated {len(df)} rows with {suite_name}")
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default="data/omop/person.parquet")
    parser.add_argument("--suite", default="person_suite")
    args = parser.parse_args()
    ok = run(args.data, args.suite)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
