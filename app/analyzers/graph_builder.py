import networkx as nx

def build_architecture_graph(endpoints,prompts,dependencies,langgraph_data):

    graph = nx.DiGraph()
    for ep in endpoints:
        route = ep["route"]
        graph.add_node(route,type="endpoint")
        graph.add_node(
            ep["function"],
            type="function"
        )

        graph.add_edge(
            route,
            ep["function"],
            relationship="calls"
        )
    for prompt in prompts:

        prompt_name = (
            prompt.get("variable")
            or prompt.get("type")
        )

        graph.add_node(
            prompt_name,
            type="prompt"
        )
    for edge in dependencies["graph_edges"]:

        graph.add_edge(
            edge["from"],
            edge["to"],
            relationship=edge["relationship"]
        )
    for node in langgraph_data["graph_nodes"]:
        graph.add_node(
            node,
            type="langgraph_node"
        )

    for edge in langgraph_data["graph_edges"]:

        graph.add_edge(
            edge["from"],
            edge["to"],
            relationship=edge["type"]
        )

    return {
        "nodes": [
            {
                "id": n,
                "type": graph.nodes[n].get("type")
            }
            for n in graph.nodes
        ],

        "edges": [
            {
                "from": u,
                "to": v,
                "relationship": d.get("relationship")
            }
            for u, v, d in graph.edges(data=True)
        ]
    }