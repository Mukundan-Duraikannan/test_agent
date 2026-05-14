from git import Repo
from pathlib import Path
from fastapi import UploadFile
import uuid
import zipfile

from analyzers.api_analyzer import extract_endpoints
from analyzers.prompt_analyzer import extract_prompts
from analyzers.langgraph_analyzer import extract_langgraph_flows
from analyzers.dependency_analyzer import extract_dependencies
from analyzers.graph_builder import build_architecture_graph
from analyzers.graph_visualizer import generate_interactive_graph
from analyzers.export_neo import export_to_neo4j
from intelligence.architecture_intelligence import (analyze_architecture_intelligence)

REPO_DIR = Path("storage/repos")
UPLOAD_DIR = Path("storage/uploads")

REPO_DIR.mkdir(parents=True, exist_ok=True)
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

IGNORE_DIRS = {"__pycache__",".git","node_modules","venv",".idea",".vscode"}

def clone_github_repository(repo_url: str):
    project_id = str(uuid.uuid4())
    local_path = REPO_DIR / project_id
    Repo.clone_from(repo_url, local_path)
    return {
        "project_id": project_id,
        "local_path": str(local_path)
    }


async def extract_zip_file(file: UploadFile):
    project_id = str(uuid.uuid4())
    zip_path = UPLOAD_DIR / f"{project_id}.zip"
    with open(zip_path, "wb") as f:
        content = await file.read()
        f.write(content)
    extract_path = UPLOAD_DIR / project_id
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_path)
    return {
        "project_id": project_id,
        "local_path": str(extract_path)
    }

def scan_project(project_path: str):

    project_path = Path(project_path)
    files = []
    for file in project_path.rglob("*"):
        if any(part in IGNORE_DIRS for part in file.parts):
            continue
        if file.is_file():

            relative_path = str(
                file.relative_to(project_path)
            )

            files.append(relative_path)

    endpoints_data = extract_endpoints(project_path)

    prompts = extract_prompts(project_path)

    langgraph_data = extract_langgraph_flows(project_path)

    dependency_data = extract_dependencies(project_path)
    graph_data = {
    "nodes": [],
    "edges": []
}

    for node in dependency_data["graph_nodes"]:

        graph_data["nodes"].append({
            "id": node,
            "type": "module"
        })

    for edge in dependency_data["graph_edges"]:

        graph_data["edges"].append({
            "from": edge["from"],
            "to": edge["to"],
            "relationship": edge.get("relationship", "imports")
        })

    graph_file = generate_interactive_graph(graph_data)

    graph_url = f"http://127.0.0.1:8000/graphs/{graph_file}"
    architecture_graph = build_architecture_graph(
            endpoints=endpoints_data["endpoints"],
            prompts=prompts,
            dependencies=dependency_data,
            langgraph_data=langgraph_data
        )

    graph_html = generate_interactive_graph(
    architecture_graph
    )

    intelligence_data = analyze_architecture_intelligence(
    project_path=project_path,
    endpoints=endpoints_data["endpoints"],
    prompts=prompts
    )
    export_to_neo4j(graph_data)
    return {

        "files": files,
        "endpoints": endpoints_data["endpoints"],
        "external_api_calls":
            endpoints_data["external_api_calls"],
        "prompts": prompts,
        "graph_nodes":
            langgraph_data["graph_nodes"],

        "graph_edges":
            langgraph_data["graph_edges"],
        "dependencies": dependency_data,
        "architecture_graph": architecture_graph,
        "graph_visualization": graph_url,
        "architecture_intelligence":intelligence_data,
    }