import ast
from pathlib import Path
import networkx as nx


def is_internal_module(project_path, module_name):

    module_path = (
        Path(project_path)
        / f"{module_name.replace('.', '/')}.py"
    )

    return module_path.exists()


def extract_dependencies(project_path):

    graph = nx.DiGraph()

    for file in Path(project_path).rglob("*.py"):

        try:
            source = file.read_text(encoding="utf-8")
            tree = ast.parse(source)

            current_module = str(file)

            graph.add_node(current_module)

            for node in ast.walk(tree):

                if isinstance(node, ast.Import):

                    for alias in node.names:

                        relationship = (
                            "internal"
                            if is_internal_module(project_path, alias.name)
                            else "external"
                        )

                        graph.add_edge(
                            current_module,
                            alias.name,
                            relationship=relationship
                        )

                elif isinstance(node, ast.ImportFrom):

                    if node.module:

                        relationship = (
                            "internal"
                            if is_internal_module(project_path, node.module)
                            else "external"
                        )

                        graph.add_edge(
                            current_module,
                            node.module,
                            relationship=relationship
                        )

        except:
            continue

    return {
        "graph_nodes": list(graph.nodes),
        "graph_edges": [
            {
                "from": u,
                "to": v,
                "relationship": d.get("relationship")
            }
            for u, v, d in graph.edges(data=True)
        ]
    }