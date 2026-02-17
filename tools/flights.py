# tools/flights.py

def search_flights(
    origin: str,
    destination: str,
    date: str,
    budget: float
) -> list:
    """
    Search for available flights between two cities within a budget.
    Returns a list of flight options.
    """

    return [
        {
            "airline": "IndiGo",
            "departure": origin,
            "arrival": destination,
            "date": date,
            "price": 4500,
            "type": "cheap"
        },
        {
            "airline": "Vistara",
            "departure": origin,
            "arrival": destination,
            "date": date,
            "price": 7000,
            "type": "mid"
        },
        {
            "airline": "Air India",
            "departure": origin,
            "arrival": destination,
            "date": date,
            "price": 9500,
            "type": "expensive"
        }
    ]
