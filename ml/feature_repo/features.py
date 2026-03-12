"""
Feast Feature Definitions — Biomedical Data Platform

Example feature views for clinical and genomic features.
"""

from datetime import timedelta
from feast import Entity, FeatureView, Field
from feast.types import Float32, Int64, String
from feast.infra.offline_stores.file import FileOfflineStore
from feast.infra.online_stores.sqlite import SqliteOnlineStore


# Entities
patient = Entity(name="patient_id", join_keys=["patient_id"])

# Example: Person-level features (demographics, risk score)
person_features = FeatureView(
    name="person_features",
    entities=[patient],
    ttl=timedelta(days=365),
    schema=[
        Field(name="year_of_birth", dtype=Int64),
        Field(name="gender_concept_id", dtype=Int64),
        Field(name="risk_score", dtype=Float32),
    ],
    source=FileOfflineStore(path="data/feast/person.parquet"),
    online=True,
)

# Example: Genomic features (variant count per gene)
variant_features = FeatureView(
    name="variant_features",
    entities=[patient],
    ttl=timedelta(days=365),
    schema=[
        Field(name="gene", dtype=String),
        Field(name="pathogenic_count", dtype=Int64),
        Field(name="vus_count", dtype=Int64),
    ],
    source=FileOfflineStore(path="data/feast/variants.parquet"),
    online=True,
)
