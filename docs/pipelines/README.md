# Pipeline Specifications

## FHIR Ingestion Pipeline

**Purpose**: Ingest FHIR R4 resources, map to OMOP CDM, write to Delta Lake/Parquet.

**Inputs**: FHIR REST API, HL7v2 messages (via Kafka), or FHIR bundle files.

**Outputs**: OMOP person, condition_occurrence, measurement, observation, etc.

**Flow**:
1. Fetch or consume FHIR resources
2. Map using `src.fhir_omop.mapper`
3. Validate with Great Expectations
4. Write to Delta/Parquet
5. Trigger dbt models

## Genomics Variant Pipeline

**Purpose**: Process VCF files — QC, annotation, clinical significance.

**Inputs**: VCF (.vcf, .vcf.gz), optionally BAM for re-calling.

**Outputs**: Parquet/Delta with annotated variants.

**Flow**:
1. Parse VCF
2. Apply QC filters
3. Annotate (VEP, ANNOVAR, or custom)
4. Classify clinical significance
5. Write to Parquet/Delta

## RAG Knowledge Pipeline

**Purpose**: Index clinical guidelines and literature for RAG-powered decision support.

**Inputs**: Markdown, PDF, or text documents.

**Outputs**: Vector index (Qdrant, pgvector, or Pinecone).

**Flow**:
1. Extract text from documents
2. Chunk with overlap
3. Generate embeddings (sentence-transformers or API)
4. Upsert to vector store
