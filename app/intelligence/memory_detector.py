import ast
from pathlib import Path

MEMORY_PATTERNS = [
    "ConversationBufferMemory",
    "RedisChatMessageHistory",
    "chat_history",
    "memory"
]

def detect_memory_usage(project_path):

    memories = []

    for file in Path(project_path).rglob("*.py"):

        try:
            source = file.read_text(encoding="utf-8")

            for pattern in MEMORY_PATTERNS:

                if pattern.lower() in source.lower():

                    memories.append({
                        "file": str(file),
                        "memory_type": pattern
                    })

        except:
            continue

    return memories