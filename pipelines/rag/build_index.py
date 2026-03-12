#!/usr/bin/env python3
"""
RAG Knowledge Pipeline — Build Vector Index

Indexes clinical guidelines and literature into a vector store for RAG.
Usage:
    python -m pipelines.rag.build_index --sources docs/guidelines/
"""

import argparse
import hashlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))


def chunk_text(text: str, chunk_size: int = 512, overlap: int = 64) -> list[str]:
    """Split text into overlapping chunks."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        if chunk.strip():
            chunks.append(chunk.strip())
        start = end - overlap
    return chunks


def get_embedding(text: str) -> list[float]:
    """Get embedding for text. Uses sentence-transformers if available."""
    try:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer("all-MiniLM-L6-v2")
        return model.encode(text).tolist()
    except ImportError:
        # Fallback: deterministic pseudo-embedding for demo
        h = hashlib.sha256(text.encode()).hexdigest()
        return [int(h[i : i + 2], 16) / 255.0 for i in range(0, 32, 2)]


def index_documents(sources: list[Path], output_path: Path) -> None:
    """Index documents and write to vector store."""
    all_points = []
    
    for src in sources:
        if not src.exists():
            print(f"Skipping missing: {src}")
            continue
        if src.is_file():
            files = [src]
        else:
            files = list(src.rglob("*.md")) + list(src.rglob("*.txt"))
        
        for f in files:
            text = f.read_text(encoding="utf-8", errors="ignore")
            for i, chunk in enumerate(chunk_text(text)):
                emb = get_embedding(chunk)
                all_points.append({
                    "id": hashlib.sha256(f"{f}:{i}".encode()).hexdigest()[:16],
                    "source": str(f),
                    "chunk": chunk,
                    "embedding": emb,
                })
    
    out_path = Path(output_path)
    out_path.mkdir(parents=True, exist_ok=True)
    
    try:
        from qdrant_client import QdrantClient
        from qdrant_client.models import Distance, VectorParams, PointStruct
        client = QdrantClient(path=str(out_path / "qdrant_data"))
        client.create_collection(
            collection_name="clinical_guidelines",
            vectors_config=VectorParams(size=len(all_points[0]["embedding"]), distance=Distance.COSINE),
        )
        client.upsert(
            collection_name="clinical_guidelines",
            points=[
                PointStruct(id=p["id"], vector=p["embedding"], payload={"source": p["source"], "chunk": p["chunk"]})
                for p in all_points
            ],
        )
        print(f"Indexed {len(all_points)} chunks to Qdrant at {out_path / 'qdrant_data'}")
    except ImportError:
        import json
        with open(out_path / "index.json", "w") as f:
            json.dump([{k: v for k, v in p.items()} for p in all_points], f, indent=2)
        print(f"Indexed {len(all_points)} chunks to {out_path / 'index.json'} (Qdrant not available)")
    
    print("RAG index build complete.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build RAG Vector Index")
    parser.add_argument("--sources", "-s", nargs="+", default=["docs/guidelines/"], help="Source dirs/files")
    parser.add_argument("--output", "-o", default="./data/rag_index", help="Output path")
    args = parser.parse_args()
    sources = [Path(s) for s in args.sources]
    index_documents(sources, Path(args.output))


if __name__ == "__main__":
    main()
