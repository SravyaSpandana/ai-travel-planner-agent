import asyncio
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


PROJECT_ROOT = Path(__file__).resolve().parents[1]


async def main() -> None:
    server_parameters = StdioServerParameters(
        command=sys.executable,
        args=[
            "-m",
            "mcp_servers.weather_mcp_server",
        ],
        cwd=str(PROJECT_ROOT),
    )

    async with stdio_client(server_parameters) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            tools_result = await session.list_tools()

            print("\nAvailable MCP tools:")
            for tool in tools_result.tools:
                print(f"- {tool.name}")

            result = await session.call_tool(
                "get_weather",
                arguments={"location": "Paris"},
            )

            print("\nWeather tool response:")
            print(result)


if __name__ == "__main__":
    asyncio.run(main())