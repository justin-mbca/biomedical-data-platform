"""
Airflow DAG: Genomics Variant Processing

Processes VCFs on schedule or trigger. Configure:
- genomics_input_path
- genomics_output_path
"""

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta


def run_variant_pipeline(**context):
    """Invoke genomics variant pipeline."""
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from pipelines.genomics.variant_pipeline import run
    run(
        input_path=context["dag_run"].conf.get("input_path", "/data/variants.vcf.gz"),
        output_path=context["dag_run"].conf.get("output_path", "/data/genomics"),
    )


with DAG(
    dag_id="genomics_variant_pipeline",
    default_args={
        "owner": "data-platform",
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
    },
    description="VCF variant processing pipeline",
    schedule_interval=None,  # Triggered manually or by sensor
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["genomics", "variants", "vcf"],
) as dag:
    process = PythonOperator(
        task_id="process_variants",
        python_callable=run_variant_pipeline,
    )
