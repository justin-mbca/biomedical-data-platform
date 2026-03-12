#!/usr/bin/env python3
"""
FHIR Ingestion Pipeline — Entry Point

Ingests FHIR R4 resources, maps to OMOP CDM, and writes to Delta Lake/Parquet.
Usage:
    python -m pipelines.fhir_ingestion.run --config config/fhir_demo.yaml
    python -m pipelines.fhir_ingestion.run --source http://localhost:8080/fhir
"""

import argparse
import json
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.fhir_omop.mapper import (
    MappingConfig,
    map_patient_to_person,
    map_condition_to_condition_occurrence,
    map_observation_to_measurement,
)


def load_fhir_bundle(path_or_url: str) -> dict:
    """Load FHIR bundle from file or fetch from URL."""
    if path_or_url.startswith("http"):
        import urllib.request
        with urllib.request.urlopen(path_or_url) as resp:
            return json.load(resp)
    with open(path_or_url) as f:
        data = json.load(f)
    # If single resource, wrap in bundle
    if "resourceType" in data and data.get("resourceType") != "Bundle":
        return {"resourceType": "Bundle", "entry": [{"resource": data}]}
    return data


def run(config_path: str | None = None, source: str | None = None) -> None:
    """Run FHIR ingestion pipeline."""
    if config_path:
        import yaml
        with open(config_path) as f:
            cfg = yaml.safe_load(f)
    else:
        cfg = {
            "source": {"type": "fhir", "endpoint": source or "http://localhost:8080/fhir"},
            "mapping": {"omop_version": "5.4", "source_system": "fhir_demo"},
            "output": {"format": "parquet", "path": "./data/omop"},
        }

    mapping_config = MappingConfig(
        omop_version=cfg.get("mapping", {}).get("omop_version", "5.4"),
        source_system=cfg.get("mapping", {}).get("source_system", "fhir"),
    )

    endpoint = cfg.get("source", {}).get("endpoint") or source
    if not endpoint:
        print("No FHIR source configured. Use --config or --source.")
        sys.exit(1)

    print(f"Ingesting from: {endpoint}")
    bundle = load_fhir_bundle(endpoint)

    person_rows = []
    condition_rows = []
    measurement_rows = []

    for entry in bundle.get("entry", []):
        resource = entry.get("resource", {})
        res_type = resource.get("resourceType", "")

        if res_type == "Patient":
            person_rows.append(map_patient_to_person(resource, mapping_config))
        elif res_type == "Condition":
            condition_rows.append(map_condition_to_condition_occurrence(resource, mapping_config))
        elif res_type == "Observation":
            measurement_rows.append(map_observation_to_measurement(resource, mapping_config))

    out_path = Path(cfg.get("output", {}).get("path", "./data/omop"))
    out_path.mkdir(parents=True, exist_ok=True)

    for name, rows in [("person", person_rows), ("condition_occurrence", condition_rows), ("measurement", measurement_rows)]:
        if rows:
            out_file = out_path / f"{name}.parquet"
            try:
                import pyarrow as pa
                import pyarrow.parquet as pq
                table = pa.Table.from_pylist(rows)
                pq.write_table(table, out_file)
                print(f"Wrote {len(rows)} rows to {out_file}")
            except ImportError:
                # Fallback: write JSON
                with open(out_path / f"{name}.json", "w") as f:
                    json.dump(rows, f, indent=2)
                print(f"Wrote {len(rows)} rows to {out_path}/{name}.json (pyarrow not available)")

    print("FHIR ingestion complete.")


def main() -> None:
    parser = argparse.ArgumentParser(description="FHIR → OMOP Ingestion Pipeline")
    parser.add_argument("--config", "-c", help="Path to YAML config")
    parser.add_argument("--source", "-s", help="FHIR endpoint URL")
    args = parser.parse_args()
    run(config_path=args.config, source=args.source)


if __name__ == "__main__":
    main()
