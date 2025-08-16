# MCP Weather Server for n8n

A simple Model Context Protocol (MCP) server that provides weather information via OpenWeather API, designed to work with n8n's MCP client. This server uses the `fastmcp` library for easy MCP implementation.

## Features

- 🌤️ Get current weather for any city
- 📅 Get 5-day weather forecast
- 📡 Server-Sent Events (SSE) for real-time communication
- 🔌 MCP protocol compatible
- 🚀 Simple and lightweight implementation

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure OpenWeather API Key

You must set your OpenWeather API key as an environment variable:

```bash
export OPENWEATHER_API_KEY="your_api_key_here"
```

**Note**: The API key is required and the server will not start without it.

### 3. Run the Server

```bash
python mcp_openweather_server.py
```

The server will start on port 8000 using SSE (Server-Sent Events) transport.

## Available Tools

The server provides two MCP tools:

### 1. `get_current_weather`

Get current weather conditions for a city.

**Parameters:**
- `city` (string, required): The name of the city (e.g., "London")
- `units` (string, optional): Temperature units - "metric" (Celsius), "imperial" (Fahrenheit), or "standard" (Kelvin). Defaults to "metric".

**Returns:**
- City name
- Temperature
- Feels like temperature
- Weather condition description
- Humidity percentage
- Wind speed
- Data source

### 2. `get_weather_forecast`

Get 5-day weather forecast for a city.

**Parameters:**
- `city` (string, required): The name of the city (e.g., "London")
- `units` (string, optional): Temperature units - "metric" (Celsius), "imperial" (Fahrenheit), or "standard" (Kelvin). Defaults to "metric".

**Returns:**
- City name
- Forecast data for the next 24 hours (3-hour intervals)
- Data source

## n8n Integration

### 1. Install n8n MCP Client

In your n8n instance, install the MCP client node:

```bash
npm install n8n-nodes-mcp-client
```

### 2. Configure MCP Client Node

1. Add the MCP Client node to your workflow
2. Configure the connection:
   - **Server URL**: `http://localhost:8000`
   - **Client ID**: `n8n` (or any unique identifier)
   - **Transport**: SSE (Server-Sent Events)

### 3. Use the Weather Tools

The MCP client will automatically discover both available tools:
- `get_current_weather` - for current weather conditions
- `get_weather_forecast` - for weather forecasts

## Technical Details

### Architecture

- **Framework**: Uses `fastmcp` library for MCP implementation
- **Transport**: Server-Sent Events (SSE) over HTTP
- **Port**: 8000 (configurable in code)
- **API**: OpenWeatherMap API v2.5

### Error Handling

The server includes error handling for:
- Missing API key
- Failed API requests
- Invalid responses

### Dependencies

- `fastmcp`: MCP server implementation
- `requests`: HTTP client for API calls
- `os`: Environment variable handling

## Troubleshooting

### Common Issues

1. **Missing API Key**: Ensure `OPENWEATHER_API_KEY` environment variable is set
2. **Port Already in Use**: Change the port in the code if 8000 is occupied
3. **API Rate Limits**: OpenWeather API has rate limits for free tier accounts

### Testing

You can test the server by running it and checking the console output. The server will show connection logs and any errors that occur.

## Development

### Adding New Tools

To add new tools, use the `@mcp.tool` decorator:

```python
@mcp.tool
def your_tool_name(param1: str, param2: int = 0) -> dict:
    """
    Tool description.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Tool result
    """
    # Tool implementation
    return {"result": "success"}
```

### Modifying Server Configuration

To change the server configuration, modify the `mcp.run()` call at the bottom of the file:

```python
mcp.run(transport="sse", port=8000)
```

## License

This project is open source and available under the MIT License. 