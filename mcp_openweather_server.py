from fastmcp import FastMCP
import requests
import os

# Initialize the MCP server
mcp = FastMCP(name="OpenWeatherMCPServer")

# Get the OpenWeatherMap API key from environment variable
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
if not OPENWEATHER_API_KEY:
    raise ValueError("OPENWEATHER_API_KEY environment variable not set")


# Define a tool to get current weather
@mcp.tool
def get_current_weather(city: str, units: str = "metric") -> dict:
    """
    Get current weather for a specified city.

    Args:
        city: The name of the city (e.g., "London")
        units: Temperature units ("metric" for Celsius, "imperial" for Fahrenheit, "standard" for Kelvin)

    Returns:
        A dictionary containing weather information
    """
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": OPENWEATHER_API_KEY,
        "units": units
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()

        return {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "condition": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
            "source": "OpenWeatherMap API"
        }
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to fetch weather data: {str(e)}"}


# Define a tool to get weather forecast (extension)
@mcp.tool
def get_weather_forecast(city: str, units: str = "metric") -> dict:
    """
    Get 5-day weather forecast for a specified city.

    Args:
        city: The name of the city (e.g., "London")
        units: Temperature units ("metric" for Celsius, "imperial" for Fahrenheit, "standard" for Kelvin)

    Returns:
        A dictionary containing forecast data
    """
    base_url = "http://api.openweathermap.org/data/2.5/forecast"
    params = {
        "q": city,
        "appid": OPENWEATHER_API_KEY,
        "units": units,
        "cnt": 40  # Up to 5 days (8 calls/day)
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()

        forecast = []
        for item in data["list"][:8]:  # First 24 hours (3-hour intervals)
            forecast.append({
                "time": item["dt_txt"],
                "temperature": item["main"]["temp"],
                "condition": item["weather"][0]["description"]
            })

        return {
            "city": data["city"]["name"],
            "forecast": forecast,
            "source": "OpenWeatherMap API"
        }
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to fetch forecast data: {str(e)}"}


# Run the server with HTTP transport
if __name__ == "__main__":
    mcp.run(transport="sse", port=8000)  # Use Server-Sent Events (SSE) for HTTP