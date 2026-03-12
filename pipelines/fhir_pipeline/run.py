"""FHIR pipeline entry point — delegates to fhir_ingestion."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from pipelines.fhir_ingestion.run import run, main

if __name__ == "__main__":
    main()
