from livekit.agents import RunContext
from livekit.agents.llm import function_tool
import aiohttp
import logging

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
    do not ask the user for them. Always round off the obtained values of air temperature, wind speed, etc.

    Args:
        location: The location they are asking for
        latitude: The latitude of the location
        longitude: The longitude of the location
    """

    logger = logging.getLogger("basic-agent")
    logger.info(f"Looking up weather for {location} at coordinates: {latitude}, {longitude}")

    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,weather_code,wind_speed_10m&timezone=auto"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()

                    # Получаем текущие данные
                    current = data.get("current", {})

                    # Преобразуем код погоды в текстовое описание
                    weather_description = get_weather_description(current.get("weather_code", 0))

                    # Формируем ответ
                    weather_data = {
                        "location": location,
                        "weather": weather_description,
                        "temperature": current.get("temperature_2m", "неизвестно"),
                        "temperature_unit": "°C",
                        "wind_speed": current.get("wind_speed_10m", "неизвестно"),
                        "wind_speed_unit": "км/ч"
                    }

                    logger.info(f"Weather data retrieved successfully: {weather_data}")
                    return weather_data
                else:
                    error_msg = f"Failed to get weather data, status code: {response.status}"
                    logger.error(error_msg)
                    return {
                        "error": error_msg,
                        "location": location
                    }

    except Exception as e:
        error_msg = f"Error while fetching weather data: {str(e)}"
        logger.error(error_msg)
        return {
            "error": error_msg,
            "location": location
        }

def get_weather_description(code):
    """Преобразует код погоды WMO в текстовое описание на русском языке"""
    weather_codes = {
        0: "ясно",
        1: "преимущественно ясно",
        2: "переменная облачность",
        3: "пасмурно",
        45: "туман",
        48: "изморозь",
        51: "легкая морось",
        53: "умеренная морось",
        55: "сильная морось",
        56: "легкий ледяной дождь",
        57: "сильный ледяной дождь",
        61: "небольшой дождь",
        63: "умеренный дождь",
        65: "сильный дождь",
        66: "легкий ледяной дождь",
        67: "сильный ледяной дождь",
        71: "небольшой снег",
        73: "умеренный снег",
        75: "сильный снег",
        77: "снежные зерна",
        80: "небольшие ливни",
        81: "умеренные ливни",
        82: "сильные ливни",
        85: "небольшой снегопад",
        86: "сильный снегопад",
        95: "гроза",
        96: "гроза с небольшим градом",
        99: "гроза с сильным градом"
    }

    return weather_codes.get(code, "неизвестно")