AUTH_PATTERNS = [
    "Depends",
    "JWT",
    "OAuth2PasswordBearer",
    "authenticate",
    "verify_token"
]

from pathlib import Path

def analyze_auth_flows(project_path):

    auth_flows = []

    for file in Path(project_path).rglob("*.py"):

        try:
            source = file.read_text(encoding="utf-8")

            for pattern in AUTH_PATTERNS:

                if pattern.lower() in source.lower():

                    auth_flows.append({
                        "file": str(file),
                        "auth_type": pattern
                    })

        except:
            continue

    return auth_flows