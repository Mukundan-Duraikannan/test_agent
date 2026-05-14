from neo4j import GraphDatabase

URI = "neo4j://127.0.0.1:7687"
USERNAME = "neo4j"
PASSWORD = "MUKUNDAN@13"

driver = GraphDatabase.driver(
    URI,
    auth=(USERNAME, PASSWORD)
)

def export_to_neo4j(graph_data):

    with driver.session(database="architecture-graph") as session:

        for node in graph_data["nodes"]:

            session.run(
                """
                MERGE (n:Module {id: $id, type: $type})
                """,
                id=node["id"],
                type=node["type"]
            )

        for edge in graph_data["edges"]:

            session.run(
            """
            MATCH (a:Module {id: $source})
            MATCH (b:Module {id: $target})
            MERGE (a)-[:DEPENDS_ON]->(b)
            """,
            source=edge["from"],
            target=edge["to"]
        )