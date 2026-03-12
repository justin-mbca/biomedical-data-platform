# Real-World Data System Integrations

Reference for linking external biomedical and healthcare data systems to the platform. Use this when planning integrations, data-sharing agreements, or architecture design.

---

## Overview

| Category | Example Systems | Platform Mapping |
|----------|-----------------|------------------|
| Biotech / Pharma | Calico, Verily, Tempus, Flatiron | FHIR pipeline, Genomics pipeline |
| Public Datasets | TCGA, gnomAD, UK Biobank, All of Us | FHIR, VCF, BigQuery |
| EHR / Healthcare | Epic, Cerner, Athenahealth | FHIR pipeline |
| Genomics Platforms | Terra, DNAnexus, Illumina | Genomics pipeline, VCF |
| OMOP Ecosystems | OHDSI, Synpuf, ATLAS | dbt, data_models |
| Cloud | GCP, AWS HealthLake, Azure FHIR | Kafka, Terraform |

---

## 1. Biotech & Pharma Research

| System | Organization | Data Types | Integration Pattern |
|--------|--------------|------------|---------------------|
| **Calico** | Alphabet | Aging research, genomics, clinical trials | FHIR + VCF via data-sharing agreement; internal APIs |
| **Verily** | Alphabet | RWD, wearables, Study Watch, Baseline | FHIR, BigQuery exports, Study APIs |
| **Tempus** | Tempus Labs | Clinical + molecular oncology | FHIR, genomics APIs, structured exports |
| **Flatiron Health** | Roche | Oncology RWD, EHR-derived | OMOP CDM, FHIR; ETL to Delta/Parquet |
| **Foundation Medicine** | Roche | Genomic profiling (CGP, TMB) | VCF, structured reports, FMI API |
| **Guardant Health** | Guardant | Liquid biopsy, ctDNA | VCF, Guardant360/Lunar reports |
| **Grail** | Illumina | Early cancer detection (Galleri) | Structured assay outputs, APIs |

**Platform mapping:**
- FHIR data → `pipelines/fhir_ingestion`, `config/fhir_demo.yaml`
- VCF / genomics → `pipelines/genomics/variant_pipeline.py`
- OMOP bulk → `data_models/dbt`, Delta Lake

---

## 2. Public & Consortium Datasets

| System | Provider | Data Types | Access |
|--------|----------|------------|--------|
| **TCGA** | NCI | Cancer genomics (WGS, RNA-Seq) | GDC Data Portal, FTP, API |
| **gnomAD** | Broad Institute | Population allele frequencies | VCF, Parquet, REST API |
| **dbGaP** | NCBI | Genotype–phenotype, controlled | Application; VCF, BAM |
| **UK Biobank** | UK Biobank | 500k genotyping, phenotyping | Application; bulk/API |
| **All of Us** | NIH | EHR, genomics, surveys | Researcher Workbench; FHIR, BigQuery |
| **PCAWG** | ICGC | Pan-cancer WGS | GDC, VCF/BAM |
| **ClinVar** | NCBI | Pathogenicity annotations | FTP, API |
| **cBioPortal** | Memorial Sloan Kettering | Cancer genomics | REST API |
| **COSMIC** | Wellcome Sanger | Somatic mutations | API, downloads |
| **RefSeq** | NCBI | Gene/transcript reference | FTP, API |

**Platform mapping:**
- VCF/BAM → `pipelines/genomics/variant_pipeline.py`, Spark ETL
- FHIR (All of Us) → `pipelines/fhir_ingestion`
- BigQuery (All of Us) → Terraform GCP, dbt BigQuery adapter
- Reference data → `data/` or external catalog

---

## 3. Healthcare EHR Systems

| System | Vendor | Data Types | Integration |
|--------|--------|------------|-------------|
| **Epic** | Epic Systems | EHR, FHIR R4, HL7v2 | FHIR API, Care Everywhere, bulk exports |
| **Cerner** | Oracle Health | EHR, FHIR | FHIR API, CQL, Millennium exports |
| **Athenahealth** | Athenahealth | EHR, billing | FHIR API |
| **Allscripts** | Allscripts | EHR | FHIR, HL7 |
| **HAPI FHIR** | Open source | FHIR server | REST API (already supported) |
| **Synthea** | MITRE | Synthetic FHIR | FHIR bundles, REST; demo use |

**Platform mapping:**
- FHIR API → `config/fhir_demo.yaml` endpoint, `src/fhir_omop/fetch.py`
- HL7v2 → Kafka topic → Spark consumer (extend pipelines)
- Bulk exports → S3/GCS → Spark batch job

---

## 4. Genomics & Sequencing Platforms

| System | Provider | Data Types | Integration |
|--------|----------|------------|-------------|
| **Terra** | Broad / Verily | WES/WGS, workflows | WDL, BigQuery, GCS, Terra API |
| **DNAnexus** | DNAnexus | Pipelines, VCF/BAM | REST API, dx-toolkit |
| **Seven Bridges** | Seven Bridges | CGC, genomics | API, SBG CLI |
| **AnVIL** | NHGRI | Multi-omic, Terra-based | Terra, Docker, AnVIL API |
| **Illumina DRAGEN** | Illumina | Aligned BAM, VCF | File-based; pipeline output |
| **Basespace** | Illumina | Sequencing runs | Basespace API |

**Platform mapping:**
- VCF output → `pipelines/genomics/variant_pipeline.py --input <path>`
- BAM → Extend genomics pipeline (alignment → VCF → annotation)
- API pulls → Script in `scripts/` or Airflow DAG

---

## 5. OMOP & Standardized Data Ecosystems

| System | Provider | Data Types | Integration |
|--------|----------|------------|-------------|
| **OHDSI / ATLAS** | OHDSI | OMOP CDM, cohorts | Direct DB, ETL, WebAPI |
| **Synpuf** | CMS | Synthetic Medicare/OMOP | CSV/Parquet load |
| **AACT** | ClinicalTrials.gov | Trial metadata | REST API, bulk download |
| **Observational Health** | OHDSI | OMOP, Athena vocabularies | ETL tools, vocabulary load |

**Platform mapping:**
- OMOP tables → `data_models/dbt`, `dbt/models/sources.yml`
- Vocabulary → Load into `vocabulary` schema
- Cohort definitions → ATLAS JSON → SQL generation

---

## 6. Cloud Healthcare APIs

| Service | Provider | Role | Integration |
|---------|----------|------|-------------|
| **GCP Healthcare API** | Google | FHIR store, HL7v2, DICOM | Healthcare API FHIR, Pub/Sub triggers |
| **AWS HealthLake** | Amazon | FHIR store, analytics | HealthLake API, Glue ETL |
| **Azure FHIR** | Microsoft | FHIR service | Azure FHIR API, Event Grid |
| **Snowflake** | Snowflake | Data sharing, healthcare | OMOP in Snowflake, streams |

**Platform mapping:**
- `infrastructure/terraform/` → GCP BigQuery, GCS, Pub/Sub
- FHIR store → Replace `config` endpoint with Healthcare API URL
- Pub/Sub → Kafka equivalent; extend ingestion

---

## Integration Checklist

When adding a new data source:

- [ ] Identify data format (FHIR, VCF, HL7, Parquet, API)
- [ ] Check authentication (OAuth, API key, signed URL)
- [ ] Map to pipeline: `fhir_ingestion`, `genomics`, or new module
- [ ] Add config: `config/<source>_config.yaml`
- [ ] Create Airflow DAG if scheduled
- [ ] Document in this file

---

## Example: Calico-Style Integration

```
Calico / Partner Systems
    │
    ├── FHIR (clinical, trials) ────► pipelines/fhir_ingestion
    ├── VCF (genomics) ─────────────► pipelines/genomics/variant_pipeline
    └── Structured assays ──────────► Custom ETL → Delta Lake
                    │
                    ▼
            Kafka / Pub/Sub (optional)
                    │
                    ▼
            Spark ETL → Delta Lake / Parquet
                    │
                    ▼
            dbt (OMOP) → Analytics Warehouse
                    │
                    ▼
            Feast, ML pipelines, RAG
```

**Config changes:**
- `config/fhir_demo.yaml`: Set `source.endpoint` to partner FHIR URL
- `src/fhir_omop/fetch.py`: Add auth headers if required
- Genomics: Point `--input` to shared VCF path or object store

---

## References

- [FHIR R4](https://www.hl7.org/fhir/)
- [OMOP CDM](https://ohdsi.github.io/TheBookOfOhdsi/)
- [GDC API](https://docs.gdc.cancer.gov/API/PDF/API_UG.pdf)
- [All of Us Researcher Workbench](https://www.researchallofus.org/)
- [GCP Healthcare API](https://cloud.google.com/healthcare-api/docs)
