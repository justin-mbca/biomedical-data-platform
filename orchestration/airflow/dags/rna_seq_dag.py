"""
Airflow DAG: RNA-Seq Snakemake Pipeline
"""
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

PROJECT_ROOT = "/opt/airflow"

with DAG(
    dag_id="rna_seq_snakemake",
    default_args={"owner": "data-platform", "retries": 1, "retry_delay": timedelta(minutes=5)},
    description="RNA-Seq Snakemake: QC → DESeq2 → volcano",
    schedule_interval=None,
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["rna_seq", "snakemake", "bioinformatics"],
) as dag:
    gen = BashOperator(
        task_id="generate_sample_data",
        bash_command=f"cd {PROJECT_ROOT} && python scripts/generate_rna_seq_sample.py",
    )
    run = BashOperator(
        task_id="run_snakemake",
        bash_command=f"cd {PROJECT_ROOT}/workflows/snakemake && snakemake -j 2",
    )
    gen >> run
