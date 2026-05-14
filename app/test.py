from llm.ollama_client import (generate_with_ollama)
from rag.context_builder import (build_llm_context)
query = "Generate hallucination tests"
context = build_llm_context(query)
response = generate_with_ollama(
    query,
    context
)

print(response)