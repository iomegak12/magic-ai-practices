"""Local tools — weather, time, and location."""

from datetime import datetime
from random import randint
from typing import Annotated
from zoneinfo import ZoneInfo

from agent_framework import tool
from pydantic import Field


@tool(approval_mode="never_require")
def get_weather(
    location: Annotated[str, Field(description="The location to get the weather for.")],
) -> str:
    """Get the weather for a given location."""
    conditions = ["sunny", "cloudy", "rainy", "stormy"]
    return (
        f"The weather in {location} is {conditions[randint(0, 3)]} "
        f"with a high of {randint(25, 40)}°C."
    )


@tool(approval_mode="never_require")
def get_current_time(
    timezone_name: Annotated[
        str,
        Field(
            description="The IANA timezone name, e.g. 'Asia/Kolkata', 'America/New_York', 'Europe/London'."
        ),
    ],
) -> str:
    """Get the current time in a given timezone."""
    try:
        tz = ZoneInfo(timezone_name)
        now = datetime.now(tz)
        return f"The current time in {timezone_name} is {now.strftime('%Y-%m-%d %H:%M:%S %Z')}."
    except KeyError:
        return f"Unknown timezone: '{timezone_name}'. Please use IANA format (e.g. 'Asia/Kolkata')."


@tool(approval_mode="never_require")
def get_location_info(
    city: Annotated[str, Field(description="The city name to get information about.")],
) -> str:
    """Get basic information about a city."""
    city_data = {
        "mumbai": {
            "country": "India",
            "population": "20.7 million",
            "timezone": "Asia/Kolkata",
            "coordinates": "19.0760°N, 72.8777°E",
            "known_for": "Financial capital of India, Bollywood, Gateway of India",
        },
        "new york": {
            "country": "USA",
            "population": "8.3 million",
            "timezone": "America/New_York",
            "coordinates": "40.7128°N, 74.0060°W",
            "known_for": "Statue of Liberty, Wall Street, Times Square",
        },
        "london": {
            "country": "UK",
            "population": "8.9 million",
            "timezone": "Europe/London",
            "coordinates": "51.5074°N, 0.1278°W",
            "known_for": "Big Ben, Buckingham Palace, Tower Bridge",
        },
        "tokyo": {
            "country": "Japan",
            "population": "13.9 million",
            "timezone": "Asia/Tokyo",
            "coordinates": "35.6762°N, 139.6503°E",
            "known_for": "Technology hub, Shibuya Crossing, Mount Fuji views",
        },
        "paris": {
            "country": "France",
            "population": "2.2 million",
            "timezone": "Europe/Paris",
            "coordinates": "48.8566°N, 2.3522°E",
            "known_for": "Eiffel Tower, Louvre Museum, Notre-Dame",
        },
        "hyderabad": {
            "country": "India",
            "population": "10.5 million",
            "timezone": "Asia/Kolkata",
            "coordinates": "17.3850°N, 78.4867°E",
            "known_for": "IT hub, Charminar, Biryani",
        },
        "seattle": {
            "country": "USA",
            "population": "749,256",
            "timezone": "America/Los_Angeles",
            "coordinates": "47.6062°N, 122.3321°W",
            "known_for": "Space Needle, Microsoft, Amazon HQ",
        },
        "amsterdam": {
            "country": "Netherlands",
            "population": "921,402",
            "timezone": "Europe/Amsterdam",
            "coordinates": "52.3676°N, 4.9041°E",
            "known_for": "Canals, Van Gogh Museum, Anne Frank House",
        },
    }
    info = city_data.get(city.lower())
    if info:
        return (
            f"{city.title()} ({info['country']}): Population {info['population']}, "
            f"Timezone {info['timezone']}, Coordinates {info['coordinates']}. "
            f"Known for: {info['known_for']}."
        )
    return (
        f"Basic info for {city.title()}: A city worth exploring! "
        f"(Detailed data not available in the local database.)"
    )
