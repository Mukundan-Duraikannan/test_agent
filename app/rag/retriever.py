import faiss
import pickle
import numpy as np

from sentence_transformers import (
    SentenceTransformer
)

MODEL_NAME = (
    "sentence-transformers/all-MiniLM-L6-v2"
)

model = SentenceTransformer(MODEL_NAME)


def retrieve_context(query, top_k=5):

    index = faiss.read_index(
        "storage/vector_store/faiss.index"
    )

    with open(
        "storage/vector_store/metadata.pkl",
        "rb"
    ) as f:

        metadata = pickle.load(f)

    query_embedding = model.encode(
        [query]
    ).astype("float32")

    distances, indices = index.search(
        query_embedding,
        top_k
    )

    results = []

    for idx in indices[0]:

        if idx < len(metadata):

            results.append(
                metadata[idx]
            )

    return results