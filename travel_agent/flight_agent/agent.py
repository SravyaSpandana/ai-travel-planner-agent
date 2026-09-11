import json
from pathlib import Path

from google.adk.agents import Agent

from travel_agent.models import Flight


# --------------------------------------------------
# Flight Search Tool
# --------------------------------------------------

def search_flights(origin: str, destination: str) -> str:
    """
    Search available flights between two cities.

    Returns validated flight information as a JSON string.
    """

    file_path = Path(__file__).parent / "data" / "flights.json"

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            flights = json.load(file)

        results = [
            flight
            for flight in flights
            if flight["origin"].strip().lower() == origin.strip().lower()
            and flight["destination"].strip().lower()
            == destination.strip().lower()
        ]

        if not results:
            return json.dumps(
                {
                    "status": "unavailable",
                    "origin": origin,
                    "destination": destination,
                    "message": (
                        f"No flights found from "
                        f"{origin} to {destination}."
                    )
                },
                indent=2
            )

        validated_results = [
            Flight(**flight).model_dump()
            for flight in results
        ]

        return json.dumps(
            {
                "status": "success",
                "origin": origin,
                "destination": destination,
                "flights": validated_results
            },
            indent=2
        )

    except Exception as e:
        print(f"Flight search failed: {e}")

        return json.dumps(
            {
                "status": "unavailable",
                "origin": origin,
                "destination": destination,
                "message": "Flight information is temporarily unavailable."
            },
            indent=2
        )


# --------------------------------------------------
# Flight Agent
# --------------------------------------------------

root_agent = Agent(
    model="gemini-3.5-flash-lite",
    name="flight_agent",
    description="Specialized agent for searching flights.",

    instruction="""
You are a Flight Search Specialist.

Your responsibility is ONLY to provide flight information.

When flight information is requested:
1. Use the search_flights tool.
2. Present the available flight options clearly.
3. Include airline, departure time, arrival time, price,
   and other available details.
4. Do not invent flight details, prices, schedules,
   or availability.
5. If no flights are found, clearly report that information
   is unavailable.
6. Do not create the overall travel itinerary.
7. Do not provide hotels, weather, or attractions.

Your response will be used by the Main Travel Planning Agent.
""",

    tools=[search_flights],
)