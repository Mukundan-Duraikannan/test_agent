from pathlib import Path
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

CHUNK_STORAGE_DIR = (
    BASE_DIR / "storage/chunks"
)
CHUNK_STORAGE_DIR.mkdir(
    parents=True,
    exist_ok=True
)
CHUNK_SIZE = 1500

def save_chunks_to_json(
    chunks,
    filename="chunks.json"
):

    output_path = (
        CHUNK_STORAGE_DIR / filename
    )

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            chunks,
            f,
            indent=2,
            ensure_ascii=False
        )

    return str(output_path)

def chunk_text(text, chunk_size=CHUNK_SIZE):

    chunks = []

    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i + chunk_size])
    return chunks

def build_code_chunks(project_path,endpoints,prompts,architecture_intelligence):
    chunks = []

    project_path = Path(project_path)
    for file in project_path.rglob("*.py"):

        try:

            source = file.read_text(
                encoding="utf-8"
            )

            file_chunks = chunk_text(source)

            for chunk in file_chunks:

                chunks.append({
                    "type": "code",
                    "file": str(file),
                    "content": chunk
                })

        except:
            continue

    for endpoint in endpoints:

        chunks.append({
            "type": "endpoint",
            "content": str(endpoint),
            "metadata": endpoint
        })
    for prompt in prompts:

        chunks.append({
            "type": "prompt",
            "content": str(prompt),
            "metadata": prompt
        })
    chunks.append({
        "type": "architecture_intelligence",
        "content": str(architecture_intelligence)
    })
    return chunks