#!/usr/bin/env python3
"""Run Great Expectations validation on OMOP tables."""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def run(data_path: str, suite_name: str = "fhir_omop_suite") -> bool:
    """Validate data using Great Expectations."""
    try:
        import great_expectations as gx
    except ImportError:
        print("Great Expectations not installed. Run: pip install great-expectations")
        return False

    context = gx.get_context()
    suite_path = Path(__file__).parent / "expectations" / f"{suite_name}.json"
    if not suite_path.exists():
        print(f"Suite not found: {suite_path}")
        return False

    # For demo: validate a Parquet/Delta table
    validator = context.sources.add_pandas("omop").read_parquet(data_path)
    result = context.run_checkpoint(
        checkpoint_name="omop_checkpoint",
        validations=[{"batch_request": {"datasource_name": "omop", "data_asset_name": "person"}}],
    )
    print(result)
    return result["success"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default="data/omop/person.parquet")
    parser.add_argument("--suite", default="fhir_omop_suite")
    args = parser.parse_args()
    ok = run(args.data, args.suite)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
