# analyzers/api_analyzer.py

import ast
from pathlib import Path

from analyzers.utils import resolve_node_value

HTTP_METHODS = ["get", "post", "put", "delete", "patch"]

def build_project_context(project_path):

    context = {}

    for file in Path(project_path).rglob("*.py"):

        try:
            source = file.read_text(encoding="utf-8")
            tree = ast.parse(source)

            for node in ast.walk(tree):

                if isinstance(node, ast.Assign):

                    if len(node.targets) > 0:

                        target = node.targets[0]

                        if isinstance(target, ast.Name):

                            value = resolve_node_value(
                                node.value,
                                context,
                                context
                            )

                            if value:
                                context[target.id] = value

        except:
            continue

    return context


def extract_endpoints(project_path):

    endpoints = []
    external_api_calls = []

    project_context = build_project_context(project_path)

    for file in Path(project_path).rglob("*.py"):

        try:
            source = file.read_text(encoding="utf-8")
            tree = ast.parse(source)

            variables = {}
            router_prefixes = {}
            for node in ast.walk(tree):
                if isinstance(node, ast.Assign):

                    if len(node.targets) > 0:

                        target = node.targets[0]
                        if isinstance(target, ast.Name):

                            value = resolve_node_value(
                                node.value,
                                variables,
                                project_context
                            )

                            variables[target.id] = value
                        if (
                            isinstance(node.value, ast.Call)
                            and getattr(node.value.func, "id", "") == "APIRouter"
                        ):

                            router_name = target.id

                            prefix = ""

                            for kw in node.value.keywords:

                                if kw.arg == "prefix":

                                    prefix = resolve_node_value(
                                        kw.value,
                                        variables,
                                        project_context
                                    )

                            router_prefixes[router_name] = prefix

            for node in ast.walk(tree):

                if isinstance(node, ast.FunctionDef):

                    for decorator in node.decorator_list:

                        if isinstance(decorator, ast.Call):

                            if isinstance(decorator.func, ast.Attribute):

                                method = decorator.func.attr

                                router_name = ""

                                if isinstance(decorator.func.value, ast.Name):
                                    router_name = decorator.func.value.id

                                prefix = router_prefixes.get(router_name, "")
                                if method in HTTP_METHODS:

                                    route = ""

                                    if decorator.args:

                                        route = resolve_node_value(
                                            decorator.args[0],
                                            variables,
                                            project_context
                                        ) or ""

                                    full_route = (
                                        prefix + route
                                    ).replace("//", "/")

                                    endpoints.append({
                                        "file": str(file),
                                        "framework": "fastapi",
                                        "function": node.name,
                                        "method": method.upper(),
                                        "route": full_route
                                    })
                                elif method == "route":

                                    route = ""
                                    methods = ["GET"]

                                    if decorator.args:

                                        route = resolve_node_value(
                                            decorator.args[0],
                                            variables,
                                            project_context
                                        ) or ""

                                    for kw in decorator.keywords:

                                        if kw.arg == "methods":

                                            if isinstance(kw.value, ast.List):

                                                methods = []

                                                for elt in kw.value.elts:

                                                    if isinstance(elt, ast.Constant):
                                                        methods.append(elt.value)

                                    full_route = (
                                        prefix + route
                                    ).replace("//", "/")

                                    endpoints.append({
                                        "file": str(file),
                                        "framework": "flask",
                                        "function": node.name,
                                        "method": methods,
                                        "route": full_route
                                    })
                elif isinstance(node, ast.Call):

                    if isinstance(node.func, ast.Attribute):

                        if (
                            isinstance(node.func.value, ast.Name)
                            and node.func.value.id in ["requests", "httpx"]
                        ):

                            external_api_calls.append({
                                "file": str(file),
                                "library": node.func.value.id,
                                "method": node.func.attr.upper()
                            })

        except Exception:
            continue

    return {
        "endpoints": endpoints,
        "external_api_calls": external_api_calls
    }