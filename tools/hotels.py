from langsmith import traceable

@traceable(name="search_flights")
def search_hotels(
    city: str,
    nights: int,
    budget: float,
    **kwargs
) -> list:
    """
    Search for hotels in a city within budget.
    """

    return [
        {
            "name": "Budget Inn",
            "city": city,
            "price_per_night": 1500,
            "rating": 3.5
        },
        {
            "name": "Comfort Stay",
            "city": city,
            "price_per_night": 2500,
            "rating": 4.2
        },
        {
            "name": "Luxury Suites",
            "city": city,
            "price_per_night": 4000,
            "rating": 4.8
        }
    ]
