from tools.flights import search_flights

TOOL_REGISTRY ={
    "search_flights": search_flights
}

def execute_tool(tool_name, args:dict):
    if tool_name not in TOOL_REGISTRY:
        raise ValueError(f"Unknown tool: {tool_name}")
    
    tool_fn=TOOL_REGISTRY[tool_name]
    return tool_fn(**args)