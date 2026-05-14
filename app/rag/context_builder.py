from rag.retriever import retrieve_context


def build_llm_context(user_query):

    retrieved_chunks = retrieve_context(
        user_query
    )

    context = []

    for chunk in retrieved_chunks:

        context.append({
            "type": chunk["type"],
            "content": chunk["content"]
        })

    return {
        "query": user_query,
        "retrieved_context": context
    }