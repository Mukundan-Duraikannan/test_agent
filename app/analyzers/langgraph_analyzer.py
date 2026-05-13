import ast
from pathlib import Path

def extract_langgraph_flows(project_path, project_context=None):
    graph_nodes = []
    graph_edges = []
    context = project_context or {}

    for file in Path(project_path).rglob("*.py"):
        try:
            source = file.read_text(encoding="utf-8")
            tree = ast.parse(source)
            local_vars = {}

            for node in ast.walk(tree):
                if isinstance(node, ast.Assign):
                    if isinstance(node.targets[0], ast.Name) and isinstance(node.value, ast.Constant):
                        local_vars[node.targets[0].id] = node.value.value

                if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                    method = node.func.attr
                    if method == "add_node":
                        if len(node.args) >= 1:
                            node_name = resolve_node_name(node.args[0], {**context, **local_vars})
                            if node_name:
                                graph_nodes.append(node_name)
                    elif method == "add_edge":
                        if len(node.args) >= 2:
                            start = resolve_node_name(node.args[0], {**context, **local_vars})
                            end = resolve_node_name(node.args[1], {**context, **local_vars})
                            if start and end:
                                graph_edges.append({
                                    "from": start,
                                    "to": end,
                                    "type": "direct"
                                })
                    elif method == "add_conditional_edges":
                        if len(node.args) >= 3:
                            source_node = resolve_node_name(node.args[0], {**context, **local_vars})
                            mapping = node.args[2]
                            
                            if isinstance(mapping, ast.Dict):
                                for k, v in zip(mapping.keys, mapping.values):
                                    target = resolve_node_name(v, {**context, **local_vars})
                                    cond = resolve_node_name(k, {**context, **local_vars})
                                    if source_node and target:
                                        graph_edges.append({
                                            "from": source_node,
                                            "to": target,
                                            "type": "conditional",
                                            "condition": cond
                                        })

        except Exception:
            continue

    return {
        "graph_nodes": list(set(graph_nodes)),
        "graph_edges": graph_edges
    }

def resolve_node_name(node, variables):
    """Helper to catch Constants, Names (Variables), and Attributes."""
    if isinstance(node, ast.Constant):
        return str(node.value)
    if isinstance(node, ast.Name):
        return str(variables.get(node.id, node.id))
    if isinstance(node, ast.Attribute):
        return node.attr
    return None