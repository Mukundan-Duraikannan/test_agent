import ast
from pathlib import Path

TOOL_PATTERNS = [
    "bind_tools",
    "ToolNode",
    "tool",
    "tools"
]

def detect_tool_calls(project_path):

    tools = []

    for file in Path(project_path).rglob("*.py"):

        try:
            source = file.read_text(encoding="utf-8")
            tree = ast.parse(source)

            for node in ast.walk(tree):

                if isinstance(node, ast.Call):

                    if isinstance(node.func, ast.Attribute):

                        if node.func.attr in TOOL_PATTERNS:

                            tools.append({
                                "file": str(file),
                                "tool_usage": node.func.attr
                            })

        except:
            continue

    return tools