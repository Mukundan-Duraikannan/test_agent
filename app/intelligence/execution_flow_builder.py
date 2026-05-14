def build_execution_flows(endpoints,retrievals,memories,tools):

    flows = []

    for endpoint in endpoints:

        flow = {
            "endpoint": endpoint["route"],
            "steps": []
        }

        flow["steps"].append("user_request")

        if retrievals:
            flow["steps"].append("retrieval")

        if memories:
            flow["steps"].append("memory")

        if tools:
            flow["steps"].append("tool_execution")
       
        flow["steps"].append("llm_response")

        flows.append(flow)

    return flows