# Biomedical Data Platform — Complete Setup Steps

Single reference for setting up the entire project. For troubleshooting, see [setup.md](setup.md).

---

## Prerequisites

| Tool | Version | Required |
|------|---------|----------|
| **Python** | 3.10 or 3.11 | Yes |
| **Docker** | 20.10+ | For full stack |
| **Docker Compose** | — | For Kafka, Airflow |
| **Git** | — | Yes |
| **R** | — | For RNA-Seq pipeline |
| **Snakemake** | — | For RNA-Seq pipeline |
| **Apache Spark** | 3.5+ | Optional |

---

## Step 1: Clone the Repository

```bash
git clone https://github.com/justin-mbca/biomedical-data-platform.git
cd biomedical-data-platform
```

---

## Step 2: Create Virtual Environment (Recommended)

```bash
python -m venv .venv

# Activate (Linux/macOS)
source .venv/bin/activate

# Activate (Windows)
.venv\Scripts\activate
```

---

## Step 3: Install Python Dependencies

```bash
pip install -r requirements.txt
```

---

## Step 4: Generate Sample Data

```bash
# RNA-Seq pipeline data (count matrix + gene annotation)
python scripts/generate_rna_seq_sample.py

# Synthetic oncology data (for dashboard)
python scripts/generate_synthetic_oncology.py
```

---

## Step 5: Run Infrastructure (Optional)

From project root:

```bash
cd infrastructure
docker-compose up -d
```

Or, using the docker subfolder:

```bash
cd infrastructure/docker
docker-compose up -d
```

This starts:

- **Zookeeper** (port 2181)
- **Kafka** (port 9092)
- **PostgreSQL** (port 5432) — Airflow metadata
- **Airflow** webserver (port 8080) — login: `admin` / `admin`

**Wait 30–60 seconds** for all services to start.

---

## Step 6: Run FHIR Ingestion

```bash
# Using bundled sample data (no server needed)
python -m pipelines.fhir_ingestion.run --source config/sample_fhir_bundle.json
```

Or with a live FHIR endpoint:

```bash
python -m pipelines.fhir_ingestion.run --source "https://hapi.fhir.org/baseR4/Patient?_count=10"
```

Or with config file:

```bash
python -m pipelines.fhir_ingestion.run --config config/fhir_demo.yaml
```

---

## Step 7: Validate Data Quality

```bash
python data_quality/run_validation.py --data data/omop/person.parquet --suite person_suite
```

Available suites: `person_suite`, `schema_drift_suite`, `null_rate_suite`, `data_freshness_suite`

---

## Step 8: Run dbt Transformations (Optional)

Configure `~/.dbt/profiles.yml` to point to your OMOP database, or use the project's DuckDB profile:

```bash
cd data_models/dbt
dbt deps
dbt run
dbt test
```

(Alternatively, run from `dbt/` if that's your project root.)

---

## Step 9: Run RNA-Seq Pipeline (Optional)

Requires R and Snakemake installed.

```bash
cd workflows/snakemake
snakemake -j 2
```

---

## Step 10: Build RAG Index (Optional)

```bash
python -m pipelines.rag.build_index --sources docs/guidelines/ --output data/rag_index
```

---

## Step 11: Launch Analytics Dashboard

```bash
streamlit run apps/analytics_dashboard/app.py
```

Opens in your browser (typically http://localhost:8501).

---

## Step 12: Verify Setup (Optional)

```bash
# Run unit tests
pytest tests/ -v

# Lint check
ruff check src pipelines
black --check src pipelines
```

---

## Airflow DAGs (when using Docker)

DAGs are in `orchestration/airflow/dags/` (or `orchestration/dags/` for legacy paths).

1. Open http://localhost:8080
2. Login: admin / admin
3. Unpause DAGs: `fhir_ingestion`, `genomics_variant_pipeline`, `rag_knowledge_index`, `rna_seq_snakemake`
4. Trigger runs manually or wait for schedule

---

## Environment Variables

| Variable | Description |
|----------|-------------|
| `FHIR_ENDPOINT` | FHIR R4 base URL |
| `OMOP_OUTPUT_PATH` | Output path for OMOP data |
| `KAFKA_BOOTSTRAP_SERVERS` | Kafka brokers (default: localhost:9092) |
| `POSTGRES_*` | PostgreSQL connection (for Airflow) |

---

## Minimal Run (No Docker)

To run without Docker (FHIR + dashboard only):

```bash
git clone https://github.com/justin-mbca/biomedical-data-platform.git
cd biomedical-data-platform
pip install -r requirements.txt

python scripts/generate_synthetic_oncology.py
python -m pipelines.fhir_ingestion.run --source config/sample_fhir_bundle.json
streamlit run apps/analytics_dashboard/app.py
```

---

## Quick Reference: Full Example Workflow

1. Ingest FHIR → `python -m pipelines.fhir_ingestion.run --source config/sample_fhir_bundle.json`
2. Validate → `python data_quality/run_validation.py --data data/omop/person.parquet --suite person_suite`
3. Transform → `cd data_models/dbt && dbt run`
4. Explore → Open `notebooks/02_analytics_example.ipynb`
5. Dashboard → `streamlit run apps/analytics_dashboard/app.py`

---

## Troubleshooting

- **Kafka connection refused**: Wait 30s after `docker-compose up`; Zookeeper must start first.
- **Airflow DB init**: The image usually handles this; if not, run `airflow db init` and `airflow users create` inside the container.
- **PyArrow/Spark**: Install pyarrow for Parquet: `pip install pyarrow`. Spark is optional for smaller datasets.
- **dbt source not found**: Ensure OMOP data exists in `data/omop/` or configure `profiles.yml` for your warehouse.

See [setup.md](setup.md) for more troubleshooting.
