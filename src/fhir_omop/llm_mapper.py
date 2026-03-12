"""
LLM-powered FHIR→OMOP mapping (from fhir_omop_agent).
Uses Ollama/Llama or OpenAI for mapping when available.
Falls back to rule-based mapper if LLM unavailable.
"""

import json
from typing import Any, Optional

from src.fhir_omop.mapper import MappingConfig, map_patient_to_person


def fhir_to_omop_sql_llm(fhir_json: dict, table: str, model: str = "llama2") -> Optional[str]:
    """
    Map FHIR resource to OMOP SQL using LLM (Ollama).
    Returns SQL INSERT string or None if LLM unavailable.
    """
    try:
        from ollama import Client
        client = Client()
        prompt = f"""You are a biomedical data engineer.
Map the following FHIR resource to an OMOP {table} INSERT statement.
Use OMOP CDM v5.4 fields. If a field is missing, use NULL.

FHIR resource:
{json.dumps(fhir_json, indent=2)}
"""
        response = client.generate(model=model, prompt=prompt)
        return response.get("response", "")
    except ImportError:
        return None
    except Exception:
        return None


def map_with_llm_or_rules(
    fhir_resource: dict,
    table: str,
    config: MappingConfig,
    use_llm: bool = True,
) -> dict | str:
    """
    Map FHIR to OMOP: try LLM first, fall back to rule-based.
    Returns dict for programmatic use, or SQL string if LLM succeeded and table requested.
    """
    if use_llm and table == "person":
        sql = fhir_to_omop_sql_llm(fhir_resource, table)
        if sql:
            return sql
    # Rule-based fallback
    if fhir_resource.get("resourceType") == "Patient":
        return map_patient_to_person(fhir_resource, config)
    # Other tables: use mapper functions if implemented
    from src.fhir_omop.mapper import (
        map_condition_to_condition_occurrence,
        map_observation_to_measurement,
    )
    rt = fhir_resource.get("resourceType", "")
    if rt == "Condition":
        return map_condition_to_condition_occurrence(fhir_resource, config)
    if rt == "Observation":
        return map_observation_to_measurement(fhir_resource, config)
    return {}
