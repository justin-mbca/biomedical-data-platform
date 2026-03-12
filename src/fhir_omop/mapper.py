"""
FHIR R4 → OMOP CDM mapper.

Maps common FHIR resources to OMOP tables. Extensible for custom mappings.
"""

from typing import Any, Dict, Optional
from dataclasses import dataclass


@dataclass
class MappingConfig:
    """Configuration for FHIR→OMOP mapping."""
    omop_version: str = "5.4"
    source_system: str = "fhir"
    vocabulary_source: Optional[str] = None


def map_patient_to_person(fhir_patient: Dict[str, Any], config: MappingConfig) -> Dict[str, Any]:
    """Map FHIR Patient to OMOP person table."""
    name = (fhir_patient.get("name") or [{}])[0]
    given = " ".join(name.get("given", []))
    family = name.get("family", "")
    
    return {
        "person_id": fhir_patient.get("id", ""),
        "gender_concept_id": _gender_to_concept(fhir_patient.get("gender", "unknown")),
        "year_of_birth": _extract_year(fhir_patient.get("birthDate")),
        "race_concept_id": 0,
        "ethnicity_concept_id": 0,
        "location_id": None,
        "provider_id": None,
        "care_site_id": None,
        "person_source_value": fhir_patient.get("id", ""),
        "gender_source_value": fhir_patient.get("gender", ""),
        "race_source_value": None,
        "ethnicity_source_value": None,
    }


def map_condition_to_condition_occurrence(
    fhir_condition: Dict[str, Any], config: MappingConfig
) -> Dict[str, Any]:
    """Map FHIR Condition to OMOP condition_occurrence."""
    code = (fhir_condition.get("code", {}).get("coding") or [{}])[0]
    return {
        "condition_occurrence_id": fhir_condition.get("id", ""),
        "person_id": _extract_patient_ref(fhir_condition.get("subject", {})),
        "condition_concept_id": 0,  # Requires vocabulary lookup
        "condition_start_date": fhir_condition.get("onsetDateTime") or fhir_condition.get("onsetPeriod", {}).get("start"),
        "condition_end_date": fhir_condition.get("abatementDateTime"),
        "condition_type_concept_id": 32817,  # EHR
        "condition_source_value": code.get("code", ""),
        "condition_source_concept_id": 0,
    }


def map_observation_to_measurement(
    fhir_observation: Dict[str, Any], config: MappingConfig
) -> Dict[str, Any]:
    """Map FHIR Observation to OMOP measurement."""
    code = (fhir_observation.get("code", {}).get("coding") or [{}])[0]
    value = fhir_observation.get("valueQuantity") or fhir_observation.get("valueCodeableConcept")
    return {
        "measurement_id": fhir_observation.get("id", ""),
        "person_id": _extract_patient_ref(fhir_observation.get("subject", {})),
        "measurement_concept_id": 0,
        "measurement_date": fhir_observation.get("effectiveDateTime") or fhir_observation.get("effectivePeriod", {}).get("start"),
        "measurement_datetime": fhir_observation.get("effectiveDateTime"),
        "value_as_number": value.get("value") if isinstance(value, dict) else None,
        "value_as_concept_id": 0,
        "measurement_source_value": code.get("code", ""),
    }


def _gender_to_concept(gender: str) -> int:
    """Map FHIR gender to OMOP concept_id."""
    mapping = {"male": 8507, "female": 8532, "other": 8570, "unknown": 8551}
    return mapping.get(gender.lower(), 8551)


def _extract_year(date_str: Optional[str]) -> Optional[int]:
    """Extract year from FHIR date string."""
    if not date_str:
        return None
    try:
        return int(str(date_str)[:4])
    except (ValueError, TypeError):
        return None


def _extract_patient_ref(ref: Any) -> Optional[str]:
    """Extract patient ID from FHIR reference."""
    if isinstance(ref, dict):
        return ref.get("reference", "").split("/")[-1] if ref.get("reference") else None
    if isinstance(ref, str):
        return ref.split("/")[-1]
    return None
