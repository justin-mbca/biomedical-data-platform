# Biomedical Data Platform — Architecture

## High-Level Architecture

```mermaid
flowchart TB
    subgraph Sources["Data Sources"]
        FHIR[FHIR R4 API]
        HL7[HL7 v2]
        VCF[VCF / BAM]
        PDF[Clinical PDFs]
    end

    subgraph Ingestion["Ingestion Layer"]
        Kafka[Apache Kafka / PubSub]
        Spark[Apache Spark]
    end

    subgraph Storage["Storage Layer"]
        Delta[Delta Lake]
        Parquet[Parquet]
        PG[(PostgreSQL)]
        Vector[(Vector DB)]
    end

    subgraph Orchestration["Orchestration"]
        Airflow[Airflow]
    end

    subgraph Transformation["Transformation"]
        dbt[dbt]
        GX[Great Expectations]
    end

    subgraph Consumption["Consumption"]
        Feast[Feast Feature Store]
        ML[ML Pipelines]
        RAG[RAG System]
    end

    FHIR --> Kafka
    HL7 --> Kafka
    VCF --> Spark
    PDF --> Spark
    Kafka --> Spark
    Spark --> Delta
    Spark --> Parquet
    Airflow --> Spark
    Airflow --> dbt
    dbt --> Delta
    GX --> Delta
    Delta --> Feast
    Delta --> ML
    Parquet --> Vector
    Vector --> RAG
```

## Data Flow

```mermaid
flowchart LR
    subgraph Ingest["1. Ingest"]
        A[FHIR] --> B[Kafka]
        C[VCF] --> D[Spark]
        B --> D
    end

    subgraph Store["2. Store"]
        D --> E[Delta Lake]
        D --> F[Parquet]
    end

    subgraph Transform["3. Transform"]
        E --> G[dbt]
        G --> H[OMOP CDM]
    end

    subgraph Quality["4. Validate"]
        H --> I[Great Expectations]
    end

    subgraph Consume["5. Consume"]
        H --> J[Feature Store]
        F --> K[Vector Index]
        J --> L[ML]
        K --> M[RAG]
    end
```

## Component Architecture

```mermaid
flowchart TB
    subgraph Pipelines["Pipeline Modules"]
        FHIR_PIPE[FHIR Ingestion]
        GEN_PIPE[Genomics Pipeline]
        RAG_PIPE[RAG Knowledge Pipeline]
    end

    subgraph Shared["Shared Libraries"]
        FHIR_MAP[FHIR→OMOP Mapper]
        VARIANT_ANN[Variant Annotator]
        EMBED[Embedding Service]
    end

    subgraph Infra["Infrastructure"]
        DOCKER[Docker]
        K8S[Kubernetes]
        GH[GitHub Actions]
    end

    FHIR_PIPE --> FHIR_MAP
    GEN_PIPE --> VARIANT_ANN
    RAG_PIPE --> EMBED
    Pipelines --> DOCKER
    DOCKER --> K8S
    GH --> DOCKER
```

## FHIR → OMOP Pipeline

```mermaid
sequenceDiagram
    participant FHIR as FHIR Server
    participant Kafka as Kafka
    participant Spark as Spark Job
    participant Delta as Delta Lake
    participant dbt as dbt

    FHIR->>Kafka: Push Patient, Condition, Observation
    Kafka->>Spark: Consume messages
    Spark->>Spark: Map to OMOP
    Spark->>Delta: Write person, condition_occurrence, measurement
    dbt->>Delta: Transform, deduplicate
    dbt->>Delta: Create analytics tables
```

## Technology Choices

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Messaging | Kafka | Decoupling, replay, scale; Pub/Sub for GCP |
| Batch | Spark | Unified engine for FHIR, VCF, large-scale ETL |
| Storage | Delta Lake | ACID, time travel, schema evolution |
| Orchestration | Airflow | DAG-first, rich ecosystem, healthcare adoption |
| Transformation | dbt | SQL-based, versioned, testable |
| Data quality | Great Expectations | Declarative expectations, profiling |
| Feature store | Feast | Online/offline, point-in-time correctness |
