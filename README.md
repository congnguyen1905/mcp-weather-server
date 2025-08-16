# MCP Weather Server for n8n

A simple Model Context Protocol (MCP) server that provides weather information via OpenWeather API, designed to work with n8n's MCP client.

## Features

- 🌤️ Get current weather for any city
- 📡 Server-Sent Events (SSE) for real-time communication
- 🔌 MCP protocol compatible
- 🚀 FastAPI-based REST API
- 🧪 Built-in testing tools

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure OpenWeather API Key

The server already has an API key configured, but you can set your own:

```bash
export OPENWEATHER_API_KEY="your_api_key_here"
```

### 3. Run the Server

```bash
python mcp_weather_server.py
```

The server will start on port 8000 by default. You can change this by setting the `PORT` environment variable.

## API Endpoints

- `GET /` - Server status
- `GET /tools` - List available MCP tools
- `GET /server-info` - Server information
- `GET /sse?client_id=<id>` - SSE connection for MCP client
- `POST /call` - Call a tool
- `GET /test` - Test endpoint

## Testing

### Test the Server

```bash
python test_mcp_client.py
```

This will test all the endpoints and verify the MCP connection is working.

### Manual Testing

1. **Check server status:**
   ```bash
   curl http://localhost:8000/
   ```

2. **List tools:**
   ```bash
   curl http://localhost:8000/tools
   ```

3. **Test SSE connection:**
   ```bash
   curl "http://localhost:8000/sse?client_id=test"
   ```

4. **Call a tool:**
   ```bash
   curl -X POST http://localhost:8000/call \
     -H "Content-Type: application/json" \
     -d '{"client_id":"test","tool":"get_current_weather","args":{"location":"London"}}'
   ```

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
   - **Tools**: The node should automatically discover available tools

### 3. Use the Weather Tool

The MCP client will provide access to the `get_current_weather` tool with:
- **Input**: `location` (string) - City name
- **Output**: Weather information including temperature, humidity, wind speed, etc.

## MCP Protocol Details

The server implements the Model Context Protocol with:

- **Tool Discovery**: Tools are exposed via `/tools` endpoint
- **SSE Communication**: Real-time updates via Server-Sent Events
- **Tool Execution**: Tools are called via `/call` endpoint
- **Error Handling**: Comprehensive error responses with debugging information

## Troubleshooting

### Common Issues

1. **Connection Refused**: Make sure the server is running on the correct port
2. **CORS Errors**: The server includes CORS headers, but check your n8n configuration
3. **Tool Not Found**: Verify the tool name matches exactly: `get_current_weather`
4. **Client Not Connected**: Ensure the SSE connection is established before calling tools

### Debug Mode

The server includes extensive logging. Check the console output for:
- `[SSE]` - Server-Sent Events connection logs
- `[CALL]` - Tool execution logs

### Testing Connection

Use the test script to verify each component:

```bash
python test_mcp_client.py
```

This will test:
- Server connectivity
- Tool discovery
- SSE connection
- Tool execution

## Development

### Adding New Tools

To add new tools, modify the `TOOLS` list in `mcp_weather_server.py`:

```python
TOOLS = [
    {
        "name": "your_tool_name",
        "description": "Tool description",
        "inputSchema": {
            "type": "object",
            "properties": {
                "param_name": {
                    "type": "string",
                    "description": "Parameter description"
                }
            },
            "required": ["param_name"]
        }
    }
]
```

Then implement the tool logic in the `call_tool` function.

## License

This project is open source and available under the MIT License. 