from livekit.agents import RunContext
from livekit.agents.llm import function_tool
import aiohttp
import os
import logging


@function_tool
async def search_web(
    self,
    context: RunContext,
    question: str,
):
    """Called when the user asks to find any information in the internet.
    This tool will retrieve information about the user's specific question from the google search.

    Args:
        question: The specific question what user is asking for search in the web
    """
    import logging
    logger = logging.getLogger("basic-agent")
    logger.info(f"Search web: {question}")

    # Get API key and URL from environment variables
    api_key = os.environ.get("N8N_AGENT_API_KEY")
    api_url = os.environ.get("N8N_AGENT_URL")

    if not api_key:
        logger.error("N8N_AGENT_API_KEY environment variable not set")
        return {
            "status": "error",
            "message": "Не удалось выполнить поиск в интернете. Ошибка авторизации API."
        }

    if not api_url:
        logger.error("N8N_AGENT_URL environment variable not set")
        return {
            "status": "error",
            "message": "Не указан URL API для выполнения запроса."
        }

    # Make API request
    try:
        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": api_key,
                "Content-Type": "application/json"
            }
            params = {
                "request": question
            }

            logger.info(f"Making GET request to {api_url} with params {params}")
            async with session.get(api_url, headers=headers, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    logger.info(f"Successfully retrieved search results")
                    return data
                else:
                    error_text = await response.text()
                    logger.error(f"Failed to retrieve data. Status: {response.status}, Response: {error_text}")
                    return {
                        "status": "error",
                        "message": f"Не удалось получить ответ. Код ошибки: {response.status}"
                    }
    except Exception as e:
        logger.error(f"Exception when retrieving search data: {str(e)}")
        return {
            "status": "error",
            "message": "Произошла ошибка при получении результатов поиска в интернете."
        }