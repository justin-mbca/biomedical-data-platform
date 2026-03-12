"""
Airflow DAG: FHIR Ingestion Pipeline

Schedules daily FHIR → OMOP ingestion. Configure variables in Airflow:
- fhir_source_endpoint
- omop_output_path
"""

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta


def run_fhir_ingestion(**context):
    """Invoke FHIR ingestion pipeline."""
    import subprocess
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from pipelines.fhir_ingestion.run import run
    run(config_path="config/fhir_demo.yaml")


default_args = {
    "owner": "data-platform",
    "depends_on_past": False,
    "email_on_failure": True,
    "email_on_retry": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="fhir_ingestion",
    default_args=default_args,
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
        bash_command="echo 'Run Great Expectations suite here'",
    )
    ingest >> validate
