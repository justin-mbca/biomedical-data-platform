# Setup Guide

## Prerequisites

- **Docker** 20.10+ and Docker Compose
- **Python** 3.10 or 3.11
- **Apache Spark** 3.5+ (optional, for local Spark jobs)

## Quick Start

### 1. Clone and Install

```bash
git clone https://github.com/justin-mbca/biomedical-data-platform.git
cd biomedical-data-platform
pip install -r requirements.txt
```

### 2. Run with Docker Compose

```bash
cd infrastructure
docker-compose up -d
# or: cd infrastructure/docker && docker-compose up -d
```

This starts:

- **Kafka** (port 9092)
- **PostgreSQL** (port 5432) — Airflow metadata
- **Airflow** webserver (port 8080) — login: admin/admin

### 3. Generate Sample Data & Run Pipelines

```bash
# Generate sample data
python scripts/generate_rna_seq_sample.py
python scripts/generate_synthetic_oncology.py

# FHIR ingestion (use sample bundle - no server needed)
python -m pipelines.fhir_ingestion.run --source config/sample_fhir_bundle.json

# Genomics (requires a VCF file)
python -m pipelines.genomics.variant_pipeline --input path/to/variants.vcf.gz --output data/genomics

# RAG index build
python -m pipelines.rag.build_index --sources docs/guidelines/ --output data/rag_index

# Analytics dashboard
streamlit run apps/analytics_dashboard/app.py
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `FHIR_ENDPOINT` | FHIR R4 base URL |
| `OMOP_OUTPUT_PATH` | Output path for OMOP data |
| `KAFKA_BOOTSTRAP_SERVERS` | Kafka brokers (default: localhost:9092) |
| `POSTGRES_*` | PostgreSQL connection (Airflow) |

## Airflow DAGs

DAGs are in `orchestration/airflow/dags/` (or `orchestration/dags/`). After starting docker-compose:

1. Open http://localhost:8080
2. Unpause `fhir_ingestion`, `genomics_variant_pipeline`, `rag_knowledge_index`, or `rna_seq_snakemake`
3. Trigger runs manually or wait for schedule

## dbt

```bash
cd data_models/dbt
# or: cd dbt
dbt deps
dbt run
dbt test
```

Configure `~/.dbt/profiles.yml` to point to your OMOP database or DuckDB/Spark adapter.

## Great Expectations

```bash
python data_quality/run_validation.py --data data/omop/person.parquet --suite person_suite
```

Suites: `person_suite`, `schema_drift_suite`, `null_rate_suite`, `data_freshness_suite`

## Troubleshooting

- **Kafka connection refused**: Ensure Zookeeper is up first; wait 30s after `docker-compose up`
- **Airflow DB init**: On first run, Airflow may need `airflow db init` and `airflow users create` — the image handles this
- **PyArrow/Spark**: Use `pip install pyarrow` for Parquet; Spark is optional for smaller datasets
