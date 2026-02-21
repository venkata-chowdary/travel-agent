from langsmith import traceable

@traceable(name="calculate_total_cost")

def calculate_total_cost(
    flight_price: float,
    hotel_price_per_night: float,
    nights: int,
    **kwargs
) -> float:
    """
    Calculate total trip cost.
    """

    return flight_price + (hotel_price_per_night * nights)
