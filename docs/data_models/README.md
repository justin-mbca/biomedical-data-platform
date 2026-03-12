# Data Models

## OMOP CDM

The platform targets **OMOP CDM v5.4**. Key tables:

| Table | Source | Description |
|-------|--------|-------------|
| person | FHIR Patient | Demographics, gender, birth year |
| condition_occurrence | FHIR Condition | Diagnoses |
| measurement | FHIR Observation | Labs, vitals |
| observation | FHIR Observation | Other clinical observations |
| drug_exposure | FHIR MedicationRequest | Medications |

## FHIR R4 Mapping

| FHIR Resource | OMOP Table |
|---------------|------------|
| Patient | person |
| Condition | condition_occurrence |
| Observation | measurement, observation |
| MedicationRequest | drug_exposure |
| Encounter | visit_occurrence |

## Genomics Schema

Variants are stored with fields:

- chromosome, position, ref, alt
- gene, transcript
- impact (e.g., HIGH, MODERATE)
- clinical_significance
- population frequency (gnomAD, etc.)

## Vector Store Schema (RAG)

- **id**: Chunk identifier
- **embedding**: 384-dim vector (all-MiniLM-L6-v2)
- **payload**: source path, chunk text, metadata
