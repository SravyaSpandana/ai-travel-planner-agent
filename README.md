# AI Travel Planner Agent

An agentic AI travel planning application built using **Google Agent Development Kit (ADK)**, the **A2A protocol**, and the **Model Context Protocol (MCP)**.

The application uses multiple specialized agents to help users plan a trip by retrieving flight information, hotel details, attractions, and weather information.

## Features

- Multi-agent travel planning
- Flight search using local JSON data
- Hotel search using local JSON data
- Attractions search using local JSON data
- Weather information through a remote A2A agent
- Weather functionality exposed through a local MCP server
- Communication between agents using the A2A protocol
- Tool integration using the Model Context Protocol
- Agent orchestration using Google ADK
- Structured responses using Pydantic models
- Graceful error handling for missing or unavailable data
- Modular agent-based architecture

## Technology Stack

- Python
- Google Agent Development Kit
- A2A Protocol
- Model Context Protocol
- FastMCP
- Pydantic
- Uvicorn
- JSON
- Python Virtual Environment

## Agent Architecture

The application consists of the following agents:

### 1. Travel Planner Agent

The main/root agent responsible for coordinating the travel planning workflow.

It delegates tasks to the specialized agents and combines their responses into a complete travel plan.

### 2. Flight Agent

Retrieves flight information from a local JSON data source based on the requested travel details.

### 3. Hotel Agent

Retrieves hotel information from a local JSON data source based on the destination and other travel requirements.

### 4. Attractions Agent

Retrieves attractions and sightseeing information from a local JSON data source.

### 5. Weather Agent

The Weather Agent was initially exposed as a remote agent using the **A2A protocol**.

The project now also includes a local **Weather MCP Server**, which exposes weather functionality as an MCP tool that can be consumed by the Travel Planner Agent through an MCP toolset.

## MCP Integration

The project integrates the **Model Context Protocol (MCP)** to expose weather functionality as a reusable tool.

The Weather MCP Server is implemented using **FastMCP** and provides a weather tool such as:

```python
get_weather(location: str)
```

The Travel Planner Agent connects to the local MCP server using the ADK `McpToolset`.

The MCP server communicates with the Travel Planner Agent through **stdio communication**.

### MCP Communication Flow

```text
Travel Planner Agent
        |
        v
McpToolset
        |
        | stdio communication
        v
Weather MCP Server
        |
        v
Weather Service
        |
        v
Local Weather Data
```

The MCP server is launched as a Python module:

```bash
python -m mcp_servers.weather_mcp_server
```

The ADK application starts and communicates with the MCP server when the weather tool is required.

## Project Structure

```text
AITravelPlanner/
│
├── travel_agent/
│   ├── __init__.py
│   ├── agent.py
│   ├── models.py
│   │
│   ├── attractions_agent/
│   │   ├── __init__.py
│   │   ├── agent.py
│   │   ├── data/
│   │   └── __pycache__/
│   │
│   ├── flight_agent/
│   │   ├── __init__.py
│   │   └── agent.py
│   │
│   ├── hotel_agent/
│   │   ├── __init__.py
│   │   └── agent.py
│   │
│   └── weather_agent/
│       ├── __init__.py
│       └── agent.py
│
├── mcp_servers/
│   ├── __init__.py
│   ├── weather_mcp_server.py
│   └── test_weather_mcp.py
│
├── test_a2a.py
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

> The `.venv/`, `__pycache__/`, and `.adk/` directories are local environment or generated files and should not be committed to GitHub.

## Prerequisites

Before running the application, make sure the following are installed:

- Python 3.10 or later
- Git
- Google ADK
- Visual Studio Code or another code editor
- Access to the required Google/Gemini API configuration

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/SravyaSpandana/ai-travel-planner-agent.git
```

Move into the project directory:

```bash
cd ai-travel-planner-agent
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

For Windows:

```powershell
.venv\Scripts\activate
```

For macOS/Linux:

```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

If the A2A dependency is not already included in `requirements.txt`, install it using:

```bash
pip install "google-adk[a2a]"
```

The MCP dependency is included in the project requirements. If required, it can be installed using:

```bash
pip install mcp
```

## Configuration

The application requires the appropriate Google/Gemini API configuration.

Create a `.env` file in the project root based on `.env.example`.

Example:

```env
GOOGLE_API_KEY=your_api_key_here
```

Do not commit the `.env` file or any API keys to GitHub.

The `.env` file should be excluded through `.gitignore`.

## Running the Application

The Weather Agent was previously run as a separate remote A2A service. The current implementation also supports weather functionality through the local MCP server.

### 1. Activate the virtual environment

For Windows:

```powershell
.venv\Scripts\activate
```

### 2. Start the Weather A2A Agent

If you want to run and test the A2A-based Weather Agent, run the following command from the project root:

```bash
uvicorn travel_agent.weather_agent.agent:a2a_app --host localhost --port 8001
```

The Weather Agent will be available on:

```text
http://localhost:8001
```

Keep this terminal running.

### 3. Start the Travel Planner Agent

Open a second terminal and activate the virtual environment:

```powershell
.venv\Scripts\activate
```

Start the Travel Planner Agent using the configured Google ADK development command or entry point.

The Travel Planner Agent can communicate with the Weather Agent through A2A or use the local Weather MCP Server through the configured MCP toolset, depending on the current implementation.

## Running the MCP Server

The Weather MCP Server is normally started automatically by the Travel Planner Agent through `McpToolset`.

To start the MCP server independently, run the following command from the project root.

For Windows:

```powershell
.venv\Scripts\python.exe -m mcp_servers.weather_mcp_server
```

For macOS/Linux:

```bash
.venv/bin/python -m mcp_servers.weather_mcp_server
```

The MCP server uses stdio communication, so it may appear to wait without displaying a normal web page or HTTP response.

Stop the server using:

```text
Ctrl + C
```

## Testing A2A Communication

The project includes `test_a2a.py` for testing the A2A communication.

Make sure the Weather Agent is running before executing the test.

Run:

```bash
python test_a2a.py
```

## Testing MCP Integration

The project includes `mcp_servers/test_weather_mcp.py` for testing the Weather MCP functionality.

Run:

```bash
python -m mcp_servers.test_weather_mcp
```

You can also verify that the MCP server module can be imported successfully:

```powershell
.venv\Scripts\python.exe -c "import mcp_servers.weather_mcp_server; print('MCP module loaded successfully')"
```

## Example Workflow

A typical travel planning request follows this flow:

```text
User
  |
  v
Travel Planner Agent
  |
  ├──> Flight Agent
  |
  ├──> Hotel Agent
  |
  ├──> Attractions Agent
  |
  └──> Weather MCP Toolset
             |
             v
       Weather MCP Server
             |
             v
        Weather Service
```

The Travel Planner Agent collects the responses from the specialized agents and generates a consolidated travel plan.

## Example Request

A user may ask:

```text
Plan a trip to Singapore for 5 days.
Include flight options, hotels, attractions, and weather information.
```

The Travel Planner Agent processes the request and retrieves information from the relevant specialized agents and weather MCP tool.

## Error Handling

The agents include graceful handling for scenarios such as:

- Destination not found
- No matching flight data
- No matching hotel data
- No attractions available
- Weather information unavailable
- Invalid or incomplete input
- Missing local data files
- Service communication failures
- A2A service communication errors
- MCP server communication errors

The agents return structured responses indicating whether the request was successful or unavailable.

## Data Sources

The current version uses local JSON data for demonstration purposes.

The data files are maintained within the relevant agent directory, including the attractions agent's data directory.

The Weather MCP Server currently reuses the existing weather service and local weather data.

These local data sources can later be replaced with real-time external APIs or additional MCP-based tools.

## Current Implementation

The current version includes:

- Google ADK-based agent orchestration
- Separate specialized travel agents
- Local JSON-based data retrieval
- Pydantic-based response validation
- Remote Weather Agent
- A2A-based communication with the Weather Agent
- Local Weather MCP Server
- Weather functionality exposed as an MCP tool
- MCP tool integration using `McpToolset`
- stdio-based MCP communication
- Complete travel itinerary generation
- A2A communication testing using `test_a2a.py`
- MCP testing using `test_weather_mcp.py`

## Future Enhancements

Planned improvements include:

- Add more MCP servers for external travel tools
- Add real-time flight APIs
- Add real-time hotel availability APIs
- Add live weather APIs
- Add news and travel advisory information
- Add currency exchange information
- Add persistent user preferences
- Add itinerary export functionality
- Add database support
- Add authentication and authorization
- Add automated testing
- Add deployment using cloud services
- Improve observability and logging

## Development Notes

Check the current Git status:

```bash
git status
```

To commit future changes:

```bash
git add .
git commit -m "Describe your changes"
git push
```

## License

This project is intended for learning, experimentation, and demonstration of agentic AI concepts using Google ADK, the A2A protocol, and MCP.