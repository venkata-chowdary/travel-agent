SEARCH_FLIGHTS_SCHEMA ={
    "name": "search_flights",
    "description": "Search for available flights between two cities within a budget",
    "parameters":{
        "type":"object",
        "properties": {
            "origin": {"type": "string"},
            "destination": {"type": "string"},
            "date": {"type": "string"},
            "budget": {"type": "number"}
        },
    "required": ["origin", "destination", "date", "budget"]
    }
}