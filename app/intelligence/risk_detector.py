def detect_risks(retrievals,prompts,auth_flows):

    risks = []
    if not auth_flows:
        risks.append({
            "risk": "missing_authentication",
            "severity": "high"
        })

    for prompt in prompts:

        text = str(prompt).lower()

        if "ignore previous instructions" in text:

            risks.append({
                "risk": "prompt_injection_vulnerable",
                "severity": "high"
            })

        if "do anything" in text:

            risks.append({
                "risk": "unsafe_prompt",
                "severity": "medium"
            })

    if not retrievals:

        risks.append({
            "risk": "hallucination_prone_flow",
            "severity": "high",
            "reason": "No retrieval pipeline detected"
        })

    return risks