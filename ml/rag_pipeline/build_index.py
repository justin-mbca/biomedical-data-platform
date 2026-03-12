"""
RAG Pipeline — Build Vector Index

Entry point for ml/rag_pipeline. Delegates to pipelines.rag.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from pipelines.rag.build_index import index_documents, main

if __name__ == "__main__":
    main()
