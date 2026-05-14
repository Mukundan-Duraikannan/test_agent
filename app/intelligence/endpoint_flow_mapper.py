import ast
from pathlib import Path


RETRIEVAL_PATTERNS = [
    "similarity_search",
    "as_retriever",
    "retrieve",
    "get_relevant_documents"
]

MEMORY_PATTERNS = [
    "chat_history",
    "memory",
    "conversation",
    "messages",
    "history",
    "conversationbuffermemory",
    "redischatmessagehistory",
    "save_context",
    "load_memory_variables"
]

LLM_PATTERNS = [
    "chatopenai",
    "chatgroq",
    "ollama",
    "llm",
    "invoke"
]

TOOL_PATTERNS = [
    "bind_tools",
    "toolnode",
    "tool"
]


def detect_function_features(function_node):

    features = {
        "retrieval": False,
        "memory": False,
        "llm": False,
        "tools": False
    }

    for node in ast.walk(function_node):

        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Attribute):

                method = node.func.attr.lower()
                if method in [
                    p.lower()
                    for p in RETRIEVAL_PATTERNS
                ]:
                    features["retrieval"] = True
                if method in [
                    p.lower()
                    for p in TOOL_PATTERNS
                ]:
                    features["tools"] = True
                if method in [
                    p.lower()
                    for p in LLM_PATTERNS
                ]:
                    features["llm"] = True
                if any(
                    pattern in method
                    for pattern in MEMORY_PATTERNS
                ):
                    features["memory"] = True
            elif isinstance(node.func, ast.Name):

                func_name = node.func.id.lower()

                if func_name in [
                    p.lower()
                    for p in LLM_PATTERNS
                ]:
                    features["llm"] = True

                if func_name in [
                    p.lower()
                    for p in TOOL_PATTERNS
                ]:
                    features["tools"] = True

        elif isinstance(node, ast.Name):

            variable = node.id.lower()

            if any(pattern in variable for pattern in MEMORY_PATTERNS):
                features["memory"] = True

        elif isinstance(node, ast.Attribute):

            attr = node.attr.lower()

            if any(
                pattern in attr
                for pattern in MEMORY_PATTERNS
            ):
                features["memory"] = True

    return features


def map_endpoint_flows(project_path, endpoints):

    endpoint_flows = []

    endpoint_function_map = {}
    for endpoint in endpoints:

        endpoint_function_map[
            endpoint["function"]
        ] = endpoint

    for file in Path(project_path).rglob("*.py"):

        try:

            source = file.read_text(
                encoding="utf-8"
            )

            tree = ast.parse(source)

            for node in ast.walk(tree):

                if isinstance(node, ast.FunctionDef):

                    function_name = node.name

                    if function_name in endpoint_function_map:

                        endpoint_data = (
                            endpoint_function_map[
                                function_name
                            ]
                        )

                        features = (
                            detect_function_features(node)
                        )

                        endpoint_flows.append({

                            "endpoint":
                                endpoint_data["route"],

                            "method":
                                endpoint_data["method"],

                            "function":
                                function_name,
                            "file":
                                str(file),

                            "features":
                                features
                        })

        except Exception:
            continue

    return endpoint_flows