INTENT_TEST_PROMPT = """
You are an AI chatbot testing expert.

Architecture Context:
{context}

Generate intent validation tests.

Focus on:
- business logic
- task completion
- response relevance

Return JSON.
"""


HALLUCINATION_TEST_PROMPT = """
You are an AI hallucination detection expert.

Architecture Context:
{context}

Generate hallucination testcases.

Focus on:
- fabricated APIs
- unsupported claims
- fake employee data
- fake summaries

Return JSON.
"""