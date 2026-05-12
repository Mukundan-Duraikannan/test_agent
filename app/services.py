from git import Repo
from pathlib import Path
from fastapi import UploadFile
import uuid
import zipfile

REPO_DIR = Path("storage/repos")
UPLOAD_DIR = Path("storage/uploads")

REPO_DIR.mkdir(parents=True, exist_ok=True)
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

IGNORE_DIRS = {"__pycache__",".git","node_modules","venv",".idea",".vscode"}

def clone_github_repository(repo_url: str):
    project_id = str(uuid.uuid4())
    local_path = REPO_DIR / project_id
    Repo.clone_from(repo_url, local_path)
    return {"project_id": project_id,"local_path": str(local_path)}


async def extract_zip_file(file: UploadFile):
    project_id = str(uuid.uuid4())
    zip_path = UPLOAD_DIR / f"{project_id}.zip"
    with open(zip_path, "wb") as f:
        content = await file.read()
        f.write(content)
    extract_path = UPLOAD_DIR / project_id

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_path)
    return {"project_id": project_id,"local_path": str(extract_path)}


def scan_project(project_path: str):
    project_path = Path(project_path)
    files = []
    for file in project_path.rglob("*"):
        if any(part in IGNORE_DIRS for part in file.parts):
            continue
        if file.is_file():
            relative_path = str(file.relative_to(project_path))
            files.append(relative_path)
    return {"files": files}
