from intelligence.retrieval_detector import detect_retrieval_flows
from intelligence.memory_detector import detect_memory_usage
from intelligence.tool_call_detector import detect_tool_calls
from intelligence.auth_flow_analyzer import analyze_auth_flows
from intelligence.execution_flow_builder import build_execution_flows
from intelligence.risk_detector import detect_risks

def analyze_architecture_intelligence(project_path,endpoints,prompts):

    retrievals = detect_retrieval_flows(project_path)

    memories = detect_memory_usage(project_path)

    tools = detect_tool_calls(project_path)

    auth_flows = analyze_auth_flows(project_path)

    execution_flows = build_execution_flows(
        endpoints,
        retrievals,
        memories,
        tools
    )

    risks = detect_risks(
        retrievals,
        prompts,
        auth_flows
    )

    return {
        "retrieval_flows": retrievals,
        "memory_usage": memories,
        "tool_calls": tools,
        "auth_flows": auth_flows,
        "execution_flows": execution_flows,
        "risks": risks
    }