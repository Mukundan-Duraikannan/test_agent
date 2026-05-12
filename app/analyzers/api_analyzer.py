import ast
from pathlib import Path

HTTP_METHODS = ["get", "post", "put", "delete"]
def extract_endpoints(project_path):
    endpoints = []
    for file in Path(project_path).rglob("*.py"):
        try:
            source = file.read_text(encoding="utf-8")
            tree = ast.parse(source)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    for decorator in node.decorator_list:
                        if isinstance(decorator, ast.Call):
                            if isinstance(decorator.func, ast.Attribute):
                                method = decorator.func.attr
                                if method in HTTP_METHODS:
                                    route = decorator.args[0].value
                                    endpoints.append({"file": str(file),"function": node.name,"method": method.upper(),"route": route})
        except Exception:
            continue
    return endpoints