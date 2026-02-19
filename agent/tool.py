from tools.flights import search_flights
from tools.hotels import search_hotels
from tools.cost import calculate_total_cost

TOOL_REGISTRY ={
    "search_flights": search_flights,
    "search_hotels": search_hotels,
    "calculate_total_cost": calculate_total_cost
}

def execute_tool(tool_name, args:dict):
    if tool_name not in TOOL_REGISTRY:
        raise ValueError(f"Unknown tool: {tool_name}")
    
    tool_fn=TOOL_REGISTRY[tool_name]
    return tool_fn(**args)