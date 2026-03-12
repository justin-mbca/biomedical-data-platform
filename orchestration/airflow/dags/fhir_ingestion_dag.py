"""
Airflow DAG: FHIR Ingestion Pipeline

Schedules daily FHIR → OMOP ingestion.
"""

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta


def run_fhir_ingestion(**context):
    """Invoke FHIR ingestion pipeline."""
    import sys
    from pathlib import Path
    root = Path(__file__).resolve().parents[3]
    sys.path.insert(0, str(root))
    from pipelines.fhir_ingestion.run import run
    run(config_path=str(root / "config" / "fhir_demo.yaml"))


with DAG(
    dag_id="fhir_ingestion",
    default_args={
        "owner": "data-platform",
        "retries": 2,
        "retry_delay": timedelta(minutes=5),
    },
    description="FHIR R4 → OMOP CDM ingestion pipeline",
    schedule_interval="@daily",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["fhir", "omop", "healthcare"],
) as dag:
    ingest = PythonOperator(
        task_id="ingest_fhir_to_omop",
        python_callable=run_fhir_ingestion,
    )
    validate = BashOperator(
        task_id="validate_omop",
        bash_command="python data_quality/run_validation.py --data data/omop/person.parquet || true",
    )
    ingest >> validate
