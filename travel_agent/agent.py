import sys
from pathlib import Path

from google.adk.agents import Agent
from google.adk.tools.mcp_tool.mcp_toolset import (
    McpToolset,
    StdioConnectionParams,
    StdioServerParameters,
)
#from google.adk.agents.remote_a2a_agent import RemoteA2aAgent
from google.adk.tools.agent_tool import AgentTool

from .flight_agent.agent import root_agent as flight_agent
from .hotel_agent.agent import root_agent as hotel_agent
from .attractions_agent.agent import root_agent as attractions_agent

# --------------------------------------------------
# Project Root
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]


# --------------------------------------------------
# Weather MCP Toolset
# --------------------------------------------------
# The Weather MCP Server runs as a separate process.
# ADK communicates with it through stdio.

weather_mcp_toolset = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command=sys.executable,
            args=[
                "-m",
                "mcp_servers.weather_mcp_server",
            ],
            cwd=str(PROJECT_ROOT),
        ),
        timeout=10,
    ),
)

# --------------------------------------------------
# Remote Weather Agent
# --------------------------------------------------
# The Weather Agent runs as a separate A2A service.
# Start it independently on port 8001.

# weather_agent = RemoteA2aAgent(
#     name="weather_agent",
#     description=(
#         "Provides weather forecasts for a destination. "
#         "Use this agent to retrieve weather information "
#         "for a travel location and date range."
#     ),
#     agent_card=(
#         "http://localhost:8001/"
#         ".well-known/agent-card.json"
#     ),
#     mode="task",
# )

# --------------------------------------------------
# Main Travel Planning Agent
# --------------------------------------------------
TRAVEL_AGENT_INSTRUCTION = """
You are travel_agent, the main travel-planning orchestrator and
the only agent responsible for the final user response.

Your job is to collect information from specialized sources and
produce one consolidated answer.

Available sources:

1. Flight Agent
2. Hotel Agent
3. Attractions Agent
4. Weather MCP tool

Execution rules:

- Determine which sources are needed from the user's request.
- Call only the required sources.
- Call each source at most once per user request.
- Never retry a source after it returns a result or fails.
- Treat a successful result as final for the current request.
- If information is missing, mark it as unavailable.
- Never invent missing flights, hotels, attractions, prices, or weather.
- Do not transfer control to another agent.
- Do not return intermediate tool results.
- Do not restart the workflow.

Examples:

- For a weather-only question, call only the Weather MCP tool.
- For a complete trip-planning request, call the flight, hotel,
  attractions, and weather sources as required.
- If the user does not ask for weather, do not call the Weather MCP tool.

After the required sources have returned or failed:

1. Review the collected results.
2. Create one final consolidated response.
3. Stop using tools.

The final response should contain the relevant sections:

- Trip Summary
- Flight Information
- Hotel Information
- Weather Summary, if requested
- Day-by-Day Itinerary, if itinerary planning was requested
- Estimated Cost, only when enough prices are available
- Important Notes

For a weather-only request, answer directly with the weather result.
Do not call flight, hotel, or attractions agents.
"""

root_agent = Agent(
    model="gemini-3.5-flash-lite",
    name="travel_agent",
    description="A travel planning orchestrator.",
    instruction=TRAVEL_AGENT_INSTRUCTION,
    tools=[
        AgentTool(agent=flight_agent),
        AgentTool(agent=hotel_agent),
        AgentTool(agent=attractions_agent),
        weather_mcp_toolset,
    ],
)

