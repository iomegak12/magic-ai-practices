"""Tool definitions for the TechWeatherAssistant agent."""

from random import randint
from typing import Annotated

from agent_framework import tool
from pydantic import Field


@tool(approval_mode="never_require")
def get_weather(
    location: Annotated[str, Field(description="The location to get the weather for.")],
) -> str:
    """Get the weather for a given location."""
    conditions = ["sunny", "cloudy", "rainy", "stormy"]
    return f"The weather in {location} is {conditions[randint(0, 3)]} with a high of {randint(30, 38)}°C."


@tool(approval_mode="never_require")
def unstable_data_service(
    query: Annotated[str, Field(description="The data query to execute.")],
) -> str:
    """A simulated data service that always fails — used to demonstrate exception handling."""
    raise Exception(
        "Data service request timed out after 30s — connection to upstream service refused"
    )
