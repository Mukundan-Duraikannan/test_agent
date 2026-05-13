import ast
from pathlib import Path

PROMPT_VARIABLES = [
    "prompt",
    "system",
    "assistant",
    "template",
    "instruction"
]

DB_PROMPT_PATTERNS = [
    "find_one",
    "query",
    "execute",
    "get_prompt",
    "fetch_prompt",
    "load_prompt"
]

PROMPT_FILE_KEYWORDS = [
    "prompt",
    "template",
    "llm",
    "agent"
]


def extract_prompts(project_path):

    prompts = []
    for file in Path(project_path).rglob("*.py"):

        try:
            source = file.read_text(encoding="utf-8")
            tree = ast.parse(source)

            for node in ast.walk(tree):
                if isinstance(node, ast.Assign):

                    for target in node.targets:

                        if isinstance(target, ast.Name):

                            variable_name = target.id.lower()

                            if any(
                                k in variable_name
                                for k in PROMPT_VARIABLES
                            ):

                                if isinstance(node.value, ast.Constant):

                                    prompts.append({
                                        "file": str(file),
                                        "type": "static_prompt",
                                        "variable": variable_name,
                                        "prompt": node.value.value
                                    })
                                elif isinstance(node.value, ast.JoinedStr):

                                    full_prompt = ""

                                    for value in node.value.values:

                                        if isinstance(value, ast.Constant):
                                            full_prompt += str(value.value)

                                    prompts.append({
                                        "file": str(file),
                                        "type": "fstring_prompt",
                                        "variable": variable_name,
                                        "prompt": full_prompt
                                    })

                elif isinstance(node, ast.Call):

                    if isinstance(node.func, ast.Attribute):

                        method = node.func.attr
                        if method == "from_template":

                            if node.args:

                                arg = node.args[0]

                                if isinstance(arg, ast.Constant):

                                    prompts.append({
                                        "file": str(file),
                                        "type": "chat_prompt_template",
                                        "prompt": arg.value
                                    })
                        elif method in DB_PROMPT_PATTERNS:

                            prompts.append({
                                "file": str(file),
                                "type": "database_prompt_source",
                                "source_method": method
                            })

        except:
            continue

    for ext in ["*.yaml", "*.yml", "*.json"]:

        for file in Path(project_path).rglob(ext):

            try:

                filename = file.name.lower()

                if any(k in filename for k in PROMPT_FILE_KEYWORDS):

                    prompts.append({
                        "file": str(file),
                        "type": "config_file_prompt",
                        "format": file.suffix
                    })

            except:
                continue

    return prompts