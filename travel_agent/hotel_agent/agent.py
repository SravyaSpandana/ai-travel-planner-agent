import json
from pathlib import Path

from google.adk.agents import Agent

from travel_agent.models import Hotel


# --------------------------------------------------
# Hotel Search Tool
# --------------------------------------------------

def search_hotels(city: str) -> str:
    """
    Search available hotels in a city.

    Returns validated hotel information as a JSON string.
    """

    file_path = Path(__file__).parent / "data" / "hotels.json"

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            hotels = json.load(file)

        results = [
            hotel
            for hotel in hotels
            if hotel["city"].strip().lower() == city.strip().lower()
        ]

        if not results:
            return json.dumps(
                {
                    "status": "unavailable",
                    "city": city,
                    "message": f"No hotels found in {city}."
                },
                indent=2
            )

        validated_results = [
            Hotel(**hotel).model_dump()
            for hotel in results
        ]

        return json.dumps(
            {
                "status": "success",
                "city": city,
                "hotels": validated_results
            },
            indent=2
        )

    except Exception as e:
        print(f"Hotel search failed: {e}")

        return json.dumps(
            {
                "status": "unavailable",
                "city": city,
                "message": "Hotel information is temporarily unavailable."
            },
            indent=2
        )


# --------------------------------------------------
# Hotel Agent
# --------------------------------------------------

root_agent = Agent(
    model="gemini-3.5-flash-lite",
    name="hotel_agent",
    description="Specialized agent for searching hotels.",

    instruction="""
You are a Hotel Search Specialist.

Your responsibility is ONLY to provide hotel information.

When hotel information is requested:
1. Use the search_hotels tool.
2. Present the available hotel options clearly.
3. Include the hotel name, rating, and price per night
   when those fields are available.
4. Do not invent hotel names, ratings, prices, or availability.
5. If no hotels are found, clearly report that information
   is unavailable.
6. Do not create the overall travel itinerary.
7. Do not provide flights, weather, or attractions.

Your response will be used by the Main Travel Planning Agent.
""",

    tools=[search_hotels],
)