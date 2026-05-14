from sentence_transformers import SentenceTransformer

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)


def generate_embeddings(chunks):

    texts = [
        chunk["content"]
        for chunk in chunks
    ]

    embeddings = model.encode(
        texts,
        show_progress_bar=True
    )

    embedded_chunks = []

    for chunk, embedding in zip(chunks, embeddings):

        embedded_chunks.append({
            "content": chunk["content"],
            "type": chunk.get("type"),
            "metadata": chunk.get("metadata", {}),
            "embedding": embedding
        })

    return embedded_chunks