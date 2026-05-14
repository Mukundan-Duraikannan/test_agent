import re

def clean_mermaid_id(text):

    text = str(text)

    text = text.replace("\\", "_")
    text = text.replace("/", "_")
    text = text.replace("{", "")
    text = text.replace("}", "")
    text = text.replace("-", "_")
    text = text.replace(".", "_")
    text = text.replace(":", "_")
    text = text.replace(" ", "_")

    text = re.sub(r'[^a-zA-Z0-9_]', '', text)

    return text


def generate_mermaid(graph_data):

    lines = ["graph TD"]

    for edge in graph_data["edges"]:

        source = clean_mermaid_id(edge["from"])
        target = clean_mermaid_id(edge["to"])

        source_label = str(edge["from"])
        target_label = str(edge["to"])

        lines.append(
            f'{source}["{source_label}"] --> {target}["{target_label}"]'
        )

    return "\n".join(lines)