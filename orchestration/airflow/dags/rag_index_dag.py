"""
Airflow DAG: RAG Knowledge Index Build

Rebuilds vector index weekly.
"""

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from pathlib import Path


def run_rag_index(**context):
    """Invoke RAG index build."""
    import sys
    root = Path(__file__).resolve().parents[3]
    sys.path.insert(0, str(root))
    from pipelines.rag.build_index import index_documents
    index_documents(sources=[root / "docs" / "guidelines"], output_path=root / "data" / "rag_index")


with DAG(
    dag_id="rag_knowledge_index",
    default_args={"owner": "data-platform", "retries": 1, "retry_delay": timedelta(minutes=5)},
    description="Build RAG vector index from guidelines",
    schedule_interval="@weekly",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["rag", "vector", "ai"],
) as dag:
    PythonOperator(task_id="build_vector_index", python_callable=run_rag_index)
