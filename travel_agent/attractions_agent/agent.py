import json
from pathlib import Path

from google.adk.agents import Agent

from travel_agent.models import Attraction


# --------------------------------------------------
# Attractions Search Tool
# --------------------------------------------------

def search_attractions(location: str) -> str:
    """
    Search attractions for a given location.

    Returns validated attraction information as a JSON string.
    """

    file_path = Path(__file__).parent / "data" / "attractions.json"

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            attractions = json.load(file)

        results = [
            attraction
            for attraction in attractions
            if attraction["location"].strip().lower()
            == location.strip().lower()
        ]

        if not results:
            return json.dumps(
                {
                    "status": "unavailable",
                    "location": location,
                    "message": f"No attractions found in {location}."
                },
                indent=2
            )

        validated_results = [
            Attraction(**attraction).model_dump()
            for attraction in results
        ]

        return json.dumps(
            {
                "status": "success",
                "location": location,
                "attractions": validated_results
            },
            indent=2
        )

    except Exception as e:
        print(f"Attractions search failed: {e}")

        return json.dumps(
            {
                "status": "unavailable",
                "location": location,
                "message": (
                    "Attractions information is temporarily unavailable."
                )
            },
            indent=2
        )


# --------------------------------------------------
# Attractions Agent
# --------------------------------------------------

root_agent = Agent(
    model="gemini-3.5-flash-lite",
    name="attractions_agent",
    description="Specialized agent for finding tourist attractions.",

    instruction="""
You are an Attractions Search Specialist.

Your responsibility is ONLY to provide attraction and
activity information.

When attractions are requested:
1. Use the search_attractions tool.
2. Present the available attractions clearly.
3. Include attraction names, descriptions, locations,
   and other available details.
4. Do not invent attraction information.
5. If no attractions are found, clearly report that
   information is unavailable.
6. Do not create the overall travel itinerary.
7. Do not provide flights, hotels, or weather.

Your response will be used by the Main Travel Planning Agent.
""",

    tools=[search_attractions],
)