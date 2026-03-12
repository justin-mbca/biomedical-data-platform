"""
Airflow DAG: RNA-Seq Pipeline (Snakemake)

Runs Snakemake RNA-Seq workflow: QC → DESeq2 → volcano.
"""

from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

PROJECT_ROOT = "/opt/airflow"  # Adjust for your deployment

with DAG(
    dag_id="rna_seq_snakemake",
    default_args={
        "owner": "data-platform",
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
    },
    description="RNA-Seq Snakemake pipeline (QC, DESeq2, volcano)",
    schedule_interval=None,
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["rna_seq", "snakemake", "bioinformatics"],
) as dag:
    gen_data = BashOperator(
        task_id="generate_sample_data",
        bash_command=f"cd {PROJECT_ROOT} && python scripts/generate_rna_seq_sample.py",
    )
    run_snakemake = BashOperator(
        task_id="run_snakemake",
        bash_command=f"cd {PROJECT_ROOT}/workflows/snakemake && snakemake -j 2",
    )
    gen_data >> run_snakemake
