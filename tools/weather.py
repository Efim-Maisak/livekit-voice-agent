from livekit.agents import RunContext
from livekit.agents.llm import function_tool

@function_tool
async def lookup_weather(
    self,
    context: RunContext,
    location: str,
    latitude: str,
    longitude: str,
):
    """Called when the user asks for weather related information.
    Ensure the user's location (city or region) is provided.
    When given a location, please estimate the latitude and longitude of the location and
    do not ask the user for them.

    Args:
        location: The location they are asking for
        latitude: The latitude of the location
        longitude: The longitude of the location
    """

    import logging
    logger = logging.getLogger("basic-agent")
    logger.info(f"Looking up weather for {location}")

    return {
        "weather": "sunny",
        "temperature": 70,
        "location": location,
    }