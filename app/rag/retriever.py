import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
model = SentenceTransformer(MODEL_NAME)

def retrieve_context(query, top_k=5, allowed_types=None):
    index = faiss.read_index("storage/vector_store/faiss.index")
    with open("storage/vector_store/metadata.pkl", "rb") as f:
        metadata = pickle.load(f)
    query_embedding = model.encode([query]).astype("float32")
    distances, indices = index.search(query_embedding, top_k)
    results = []

    for idx in indices[0]:

        if idx < len(metadata):

            item = metadata[idx]

            if allowed_types and item.get("type") not in allowed_types:
                continue

            results.append(item)
    seen = set()
    unique_results = []
    for item in results:
        key = f"{item.get('file')}::{item.get('type')}::{item.get('content','')[:50]}"

        if key in seen:
            continue

        seen.add(key)
        unique_results.append(item)

    return unique_results