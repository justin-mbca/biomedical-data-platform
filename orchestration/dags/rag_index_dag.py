"""
Airflow DAG: RAG Knowledge Index Build

Rebuilds vector index when source documents change.
"""

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta


def run_rag_index(**context):
    """Invoke RAG index build."""
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from pipelines.rag.build_index import index_documents
    index_documents(
        sources=[Path("docs/guidelines")],
        output_path=Path("data/rag_index"),
    )


with DAG(
    dag_id="rag_knowledge_index",
    default_args={
        "owner": "data-platform",
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
    },
    description="Build RAG vector index from guidelines",
    schedule_interval="@weekly",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["rag", "vector", "ai"],
) as dag:
    build_index = PythonOperator(
        task_id="build_vector_index",
        python_callable=run_rag_index,
    )
