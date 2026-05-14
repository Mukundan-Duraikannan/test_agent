from pathlib import Path
import json

BASE_DIR = Path(__file__).resolve().parent.parent

CHUNK_STORAGE_DIR = (
    BASE_DIR / "storage/chunks"
)

CHUNK_STORAGE_DIR.mkdir(
    parents=True,
    exist_ok=True
)


def save_chunks_to_json(
    chunks,
    filename="chunks.json"
):

    output_path = (
        CHUNK_STORAGE_DIR / filename
    )

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            chunks,
            f,
            indent=2,
            ensure_ascii=False
        )

    return str(output_path)


def build_code_chunks(
    project_path,
    endpoints,
    prompts,
    architecture_intelligence
):

    chunks = []

    for endpoint in endpoints:

        chunks.append({

            "type": "endpoint",

            "tags": [
                "api",
                "chatbot",
                "route"
            ],

            "file": endpoint.get("file"),

            "content": f"""
            Endpoint Route: {endpoint.get("route")}

            HTTP Method:
            {endpoint.get("method")}

            Function:
            {endpoint.get("function")}

            Framework:
            {endpoint.get("framework")}
            """,

            "metadata": endpoint
        })

    for prompt in prompts:

        chunks.append({

            "type": "prompt",

            "tags": [
                "llm",
                "prompt",
                "generation"
            ],

            "file": prompt.get("file"),

            "content": f"""
            Prompt Type:
            {prompt.get("type")}

            Prompt:
            {prompt.get("prompt")}
            """,

            "metadata": prompt
        })

    for retrieval in architecture_intelligence.get(
        "retrieval_flows",
        []
    ):

        chunks.append({

            "type": "retrieval_flow",

            "tags": [
                "rag",
                "retrieval",
                "llm"
            ],

            "file": retrieval.get("file"),

            "content": f"""
            Retrieval pipeline detected.

            Method:
            {retrieval.get("method")}

            Type:
            {retrieval.get("type")}
            """,

            "metadata": retrieval
        })

    for memory in architecture_intelligence.get(
        "memory_usage",
        []
    ):

        chunks.append({

            "type": "memory_flow",

            "tags": [
                "memory",
                "chat_history",
                "state"
            ],

            "file": memory.get("file"),

            "content": f"""
            Memory usage detected.

            Memory Type:
            {memory.get("memory_type")}
            """,

            "metadata": memory
        })

    for auth in architecture_intelligence.get(
        "auth_flows",
        []
    ):

        chunks.append({

            "type": "auth_flow",

            "tags": [
                "authentication",
                "jwt",
                "security"
            ],

            "file": auth.get("file"),

            "content": f"""
            Authentication flow detected.

            Auth Type:
            {auth.get("auth_type")}
            """,

            "metadata": auth
        })

    for flow in architecture_intelligence.get(
        "execution_flows",
        []
    ):

        chunks.append({

            "type": "execution_flow",

            "tags": [
                "workflow",
                "execution",
                "agent"
            ],

            "content": f"""
            Endpoint:
            {flow.get("endpoint")}

            Execution Steps:
            {' -> '.join(flow.get('steps', []))}
            """,

            "metadata": flow
        })

    return chunks