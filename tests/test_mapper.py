"""Tests for FHIR → OMOP mapper."""

import pytest
from src.fhir_omop.mapper import (
    MappingConfig,
    map_patient_to_person,
    _gender_to_concept,
    _extract_year,
)


def test_gender_to_concept():
    assert _gender_to_concept("male") == 8507
    assert _gender_to_concept("female") == 8532
    assert _gender_to_concept("unknown") == 8551


def test_extract_year():
    assert _extract_year("1990-05-15") == 1990
    assert _extract_year(None) is None


def test_map_patient_to_person():
    config = MappingConfig()
    fhir = {
        "id": "patient-123",
        "gender": "female",
        "birthDate": "1985-03-20",
        "name": [{"given": ["Jane"], "family": "Doe"}],
    }
    person = map_patient_to_person(fhir, config)
    assert person["person_id"] == "patient-123"
    assert person["gender_concept_id"] == 8532
    assert person["year_of_birth"] == 1985
