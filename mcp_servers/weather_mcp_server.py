from mcp.server.fastmcp import FastMCP
from travel_agent.weather_agent.agent import get_weather as existing_get_weather

mcp = FastMCP("weather-mcp-server")

@mcp.tool()
def get_weather(location: str) -> str:
    """
    Get weather information for a location.
    """
    return existing_get_weather(location)


if __name__ == "__main__":
    mcp.run()