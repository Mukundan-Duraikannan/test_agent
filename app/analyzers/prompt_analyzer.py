from pathlib import Path
import re


PROMPT_KEYWORDS=["prompt","system","assistant","chat","ChatPromptTemplate"]
def extract_prompts(project_path):
    prompts=[]
    for file in Path(project_path).rglob("*.py"):
        try:
            content=file.read_text(encoding='utf-8')
            for keyword in PROMPT_KEYWORDS:
                if keyword in content:
                    prompts.append({"file":str(file),"keyword":keyword})
        except:
            continue
    return prompts
        
