"""
Airflow DAG: Genomics Variant Processing

Processes VCFs on trigger.
"""

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta


def run_variant_pipeline(**context):
    """Invoke genomics variant pipeline."""
    import sys
    from pathlib import Path
    root = Path(__file__).resolve().parents[3]
    sys.path.insert(0, str(root))
    from pipelines.genomics.variant_pipeline import run
    conf = context.get("dag_run", {}).conf or {}
    run(
        input_path=conf.get("input_path", "/data/variants.vcf.gz"),
        output_path=conf.get("output_path", "/data/genomics"),
    )


with DAG(
    dag_id="genomics_variant_pipeline",
    default_args={"owner": "data-platform", "retries": 1, "retry_delay": timedelta(minutes=5)},
    description="VCF variant processing pipeline",
    schedule_interval=None,
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["genomics", "variants", "vcf"],
) as dag:
    PythonOperator(task_id="process_variants", python_callable=run_variant_pipeline)
