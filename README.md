# Biomedical Data Platform

A senior-level data engineering portfolio project demonstrating end-to-end capabilities in healthcare, genomics, and AI. This platform integrates FHIR healthcare data, OMOP clinical models, bioinformatics pipelines, and AI/RAG systems into a modern, scalable architecture.

[![CI](https://github.com/justin-mbca/biomedical-data-platform/actions/workflows/ci.yml/badge.svg)](https://github.com/justin-mbca/biomedical-data-platform/actions)

## Overview

The Biomedical Data Platform provides:

- **Healthcare data ingestion** — FHIR R4 → OMOP CDM via configurable pipelines
- **Genomics processing** — Variant calling, annotation, and clinical interpretation
- **AI/RAG knowledge system** — Vector-store powered clinical decision support
- **Feature store** — Feast for ML feature management
- **Data quality** — Great Expectations for validation
- **Orchestration** — Apache Airflow for pipeline scheduling

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        BIOMEDICAL DATA PLATFORM                               │
├─────────────────────────────────────────────────────────────────────────────┤
│  Sources          │  Ingestion       │  Storage        │  Consumption       │
│  FHIR / HL7        │  Kafka/PubSub   │  Delta Lake     │  dbt Models        │
│  VCF / BAM         │  Spark ETL      │  Parquet        │  Feature Store     │
│  Clinical DBs      │  Airflow DAGs   │  Vector DB      │  ML Pipelines      │
└─────────────────────────────────────────────────────────────────────────────┘
```

See [docs/architecture/README.md](docs/architecture/README.md) for detailed Mermaid diagrams.

## Technology Stack

| Layer | Technology |
|-------|------------|
| **Messaging** | Apache Kafka (or GCP Pub/Sub) |
| **Batch processing** | Apache Spark |
| **Storage** | Delta Lake, Parquet, PostgreSQL |
| **Orchestration** | Apache Airflow |
| **Transformation** | dbt |
| **Data quality** | Great Expectations |
| **Feature store** | Feast |
| **Vector DB** | Qdrant / Pinecone / pgvector |
| **Containerization** | Docker, Docker Compose |
| **CI/CD** | GitHub Actions |

## Repository Structure

```
biomedical-data-platform/
├── docs/                    # Documentation
│   ├── architecture/       # Diagrams, design decisions
│   ├── pipelines/           # Pipeline specifications
│   ├── data_models/        # FHIR, OMOP, genomics schemas
│   └── source_repos.md    # Origin of integrated code
├── pipelines/              # Pipeline implementations
│   ├── fhir_ingestion/     # FHIR → OMOP
│   ├── genomics/          # Variant processing
│   ├── rna_seq/           # RNA-Seq QC, DESeq2, volcano (bioinformatics_pipeline)
│   ├── rag/               # RAG knowledge pipeline
│   └── ml/                 # Feast feature store
├── workflows/snakemake/    # Snakemake RNA-Seq workflow
├── apps/analytics_dashboard/  # Streamlit oncology/RWD dashboard
├── orchestration/          # Airflow DAGs
├── dbt/                    # dbt transformations
├── scripts/                # Data generation, utilities
├── infrastructure/        # Docker, CI/CD
├── data_quality/           # Great Expectations
├── tests/
└── src/                    # FHIR/OMOP mapper, fetch, LLM
```

## Quick Start

### Prerequisites

- Docker & Docker Compose
- Python 3.10+
- Apache Spark 3.x (optional, for local dev)

### Local Setup

```bash
# Clone and enter
git clone https://github.com/justin-mbca/biomedical-data-platform.git
cd biomedical-data-platform

# Start core services (Kafka, PostgreSQL, Airflow)
cd infrastructure && docker-compose up -d

# Install Python dependencies
pip install -r requirements.txt

# Run example pipeline
python -m pipelines.fhir_ingestion.run --config config/fhir_demo.yaml
```

See [docs/setup.md](docs/setup.md) for detailed instructions.

## Example Pipelines

### 1. FHIR Ingestion Pipeline

Ingests FHIR R4 resources from REST APIs or HL7v2, maps to OMOP CDM, and loads into Delta Lake.

```bash
python -m pipelines.fhir_ingestion.run --source <fhir_endpoint>
```

### 2. Genomics Variant Processing

Processes VCF files: QC → annotation → clinical significance → Parquet/Delta.

```bash
python -m pipelines.genomics.variant_pipeline --input variants.vcf.gz
```

### 3. AI RAG Knowledge Pipeline

Indexes clinical guidelines and literature into a vector store for RAG-powered clinical decision support.

```bash
python -m pipelines.rag.build_index --sources docs/guidelines/
```

### 4. RNA-Seq Pipeline (Snakemake)

QC → DESeq2 → annotation → volcano plot (from bioinformatics_pipeline).

```bash
python scripts/generate_rna_seq_sample.py  # Create sample data
cd workflows/snakemake && snakemake -j 2
```

### 5. Analytics Dashboard

Streamlit dashboard for oncology/RWD analytics.

```bash
python scripts/generate_synthetic_oncology.py  # Optional: synthetic data
streamlit run apps/analytics_dashboard/app.py
```

## Use Cases

- **Precision medicine** — Integrate genomic variants with clinical EHR for risk stratification
- **Clinical trials** — OMOP-based cohort definitions and feasibility queries
- **Real-world evidence** — Synthetic and de-identified RWD analytics
- **AI-assisted diagnosis** — RAG over guidelines for decision support

## Documentation

- [Architecture Overview](docs/architecture/README.md)
- [Pipeline Specifications](docs/pipelines/README.md)
- [Data Models (FHIR, OMOP)](docs/data_models/README.md)
- [Setup Guide](docs/setup.md)
- [Contributing](CONTRIBUTING.md)

## Author

**Justin Zhang** — [GitHub](https://github.com/justin-mbca) · [LinkedIn](https://www.linkedin.com/in/justinzh)

Data Scientist, Computational Biologist, Software Developer  
Winnipeg, MB Canada

## License

MIT License — see [LICENSE](LICENSE).
