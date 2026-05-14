import ollama

MODEL_NAME = "mistral"
MODEL_NAME = "mistral"

def generate_with_ollama(user_query,context):
    prompt = f"""
You are an AI chatbot testing expert.
Architecture Context:
{context}

User Request:
{user_query}

Generate detailed AI chatbot test cases.

Return JSON.
"""
    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ]
    ) 
    return response["message"]["content"]
   