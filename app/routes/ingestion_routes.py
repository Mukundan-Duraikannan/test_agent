from fastapi import APIRouter, UploadFile, File, HTTPException
from services import (clone_github_repository,extract_zip_file,scan_project)

router = APIRouter()

@router.post("/github")
def ingest_github(repo_url: str):
    if not repo_url.startswith("https://github.com/"):
        raise HTTPException(status_code=400,detail="Invalid GitHub URL")
    repo_data = clone_github_repository(repo_url)
    result = scan_project(repo_data["local_path"])
    return {**repo_data,**result}

@router.post("/upload-zip")
async def upload_zip(file: UploadFile = File(...)):
    if not file.filename.endswith(".zip"):
        raise HTTPException(status_code=400,detail="Only ZIP files allowed")

    project_data = await extract_zip_file(file)
    result = scan_project(project_data["local_path"])
    return {**project_data,**result}