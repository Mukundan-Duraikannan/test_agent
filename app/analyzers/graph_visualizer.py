from pyvis.network import Network
from pathlib import Path
import uuid

GRAPH_DIR = Path("storage/graphs")
GRAPH_DIR.mkdir(parents=True, exist_ok=True)

def generate_interactive_graph(graph_data):

    net = Network(
        height="900px",
        width="100%",
        directed=True,
        notebook=False
    )

    for node in graph_data["nodes"]:

        node_id = str(node["id"])

        node_type = node.get("type", "unknown")

        net.add_node(
            node_id,
            label=node_id,
            title=node_type
        )

    for edge in graph_data["edges"]:

        net.add_edge(
            str(edge["from"]),
            str(edge["to"]),
            title=edge.get("relationship", "")
        )

    file_name = f"{uuid.uuid4()}.html"

    output_path = GRAPH_DIR / file_name

    net.save_graph(str(output_path))

    return file_name