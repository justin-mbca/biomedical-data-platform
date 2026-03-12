"""FHIR ingestion pipeline — maps FHIR R4 to OMOP CDM."""
from pipelines.fhir_ingestion.run import run

__all__ = ["run"]
