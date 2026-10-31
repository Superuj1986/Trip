"""Small OpenWeather MCP server used by :mod:`trip.mcp_client`."""

import os

import httpx
from mcp.server.fastmcp import FastMCP


OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
OPENWEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5"
REQUEST_TIMEOUT = 15.0

mcp = FastMCP("TripMate Weather")


async def _get_weather(endpoint: str, city: str) -> dict:
    if not OPENWEATHER_API_KEY:
        raise RuntimeError("OPENWEATHER_API_KEY is not configured.")
    if not city.strip():
        raise ValueError("A city is required.")

    params = {
        "q": city.strip(),
        "appid": OPENWEATHER_API_KEY,
        "units": "metric",
    }
    async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as session:
        response = await session.get(
            f"{OPENWEATHER_BASE_URL}/{endpoint}", params=params
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_current_weather(city: str) -> dict:
    """Get current weather conditions for a city."""
    return await _get_weather("weather", city)


@mcp.tool()
async def get_forecast(city: str) -> dict:
    """Get the five-day forecast for a city."""
    return await _get_weather("forecast", city)


if __name__ == "__main__":
    mcp.run(transport="stdio")
