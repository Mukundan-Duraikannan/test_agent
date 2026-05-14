import faiss
import numpy as np
import pickle
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

VECTOR_DB_DIR = (
    BASE_DIR / "storage/vector_store"
)
VECTOR_DB_DIR.mkdir(
    parents=True,
    exist_ok=True
)


def build_vector_store(embedded_chunks):

    dimension = len(
        embedded_chunks[0]["embedding"]
    )

    index = faiss.IndexFlatL2(dimension)

    vectors = np.array([
        chunk["embedding"]
        for chunk in embedded_chunks
    ]).astype("float32")

    index.add(vectors)

    faiss.write_index(
        index,
        str(VECTOR_DB_DIR / "faiss.index")
    )

    metadata = []

    for chunk in embedded_chunks:

        metadata.append({
            "content": chunk["content"],
            "type": chunk["type"],
            "metadata": chunk["metadata"]
        })

    with open(
        VECTOR_DB_DIR / "metadata.pkl",
        "wb"
    ) as f:

        pickle.dump(metadata, f)

    return {
        "vectors_stored": len(metadata),
        "index_path": str(
            VECTOR_DB_DIR / "faiss.index"
        )
    }