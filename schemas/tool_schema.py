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

SEARCH_HOTELS_SCHEMA ={
    "name": "search_hotels",
    "description": "Search for hotels in a city. Hotels are always available regardless of dates.",
    "parameters":{
        "type": "object",
        "properties":{
            "city": {"type": "string"},
            "nights": {"type": "number"},
            "budget": {"type": "number"},
            "check_in": {"type": "string"},
            "check_out": {"type": "string"},
        },
        "required": ["city", "budget", "nights"]
    },
}


CALCULATE_TOTAL_COST_SCHEMA = {
    "name": "calculate_total_cost",
    "description": "Calculate total trip cost using flight and hotel prices",
    "parameters": {
        "type": "object",
        "properties": {
            "flight_price": {"type": "number"},
            "hotel_price_per_night": {"type": "number"},
            "nights": {"type": "number"}
        },
        "required": ["flight_price", "hotel_price_per_night", "nights"]
    }
}
