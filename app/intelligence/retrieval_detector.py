import ast
from pathlib import Path

RETRIEVAL_PATTERNS = [
    "similarity_search",
    "as_retriever",
    "invoke",
    "retrieve",
    "get_relevant_documents"
]

def detect_retrieval_flows(project_path):

    retrievals = []

    for file in Path(project_path).rglob("*.py"):

        try:
            source = file.read_text(encoding="utf-8")
            tree = ast.parse(source)

            for node in ast.walk(tree):

                if isinstance(node, ast.Call):

                    if isinstance(node.func, ast.Attribute):

                        method = node.func.attr

                        if method in RETRIEVAL_PATTERNS:

                            retrievals.append({
                                "file": str(file),
                                "method": method,
                                "type": "retrieval_pipeline"
                            })

        except:
            continue

    return retrievals