import json
import logging
from pathlib import Path

from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.a2a.utils.agent_to_a2a import to_a2a

from travel_agent.models import WeatherForecast


# --------------------------------------------------
# Environment
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")

# --------------------------------------------------
# Logger
# --------------------------------------------------
logger = logging.getLogger(__name__)

# --------------------------------------------------
# Weather Tool
# --------------------------------------------------

def get_weather(location: str) -> str:
    """
    Get weather forecast for a location.

    Returns a JSON string containing the weather forecast
    or an unavailable response.
    """
    logger.info("Weather tool started for: %s", location)

    file_path = Path(__file__).parent / "data" / "weather.json"

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            weather_data = json.load(file)

        for weather in weather_data:

            if (
                weather["location"].strip().lower()
                == location.strip().lower()
            ):

                validated_weather = WeatherForecast(
                    **weather
                ).model_dump()

                return json.dumps(
                    {
                        "status": "success",
                        "data": validated_weather
                    },
                    indent=2
                )

        return json.dumps(
            {
                "status": "unavailable",
                "location": location,
                "message": (
                    f"No weather information found for {location}."
                )
            },
            indent=2
        )

    except Exception as e:

        logger.exception("Weather service failed")

        return json.dumps(
            {
                "status": "unavailable",
                "location": location,
                "message": (
                    "Weather information is temporarily unavailable."
                )
            },
            indent=2
        )


# --------------------------------------------------
# Weather Agent
# --------------------------------------------------

root_agent = Agent(
    model="gemini-3.5-flash-lite",
    name="weather_agent",
    description="Specialized agent for providing weather forecasts.",

    instruction="""
You are a Weather Specialist.

Your responsibility is ONLY to provide weather information.

When the user or another agent requests weather:

1. Use the get_weather tool.
2. Return the tool result accurately.
3. Do not invent weather information.
4. If weather is unavailable, clearly report that it is unavailable.
5. Do not create a travel itinerary.
6. Do not provide flights, hotels, or attractions.

Your response will be used by the Main Travel Planning Agent.
""",

    tools=[get_weather],
)


# --------------------------------------------------
# A2A Application
# --------------------------------------------------
# This exposes the Weather Agent as a remote A2A service.
# The Travel Agent connects to this service using its
# agent card at localhost:8001.

a2a_app = to_a2a(root_agent, port=8001)