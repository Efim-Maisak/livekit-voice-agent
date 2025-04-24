# Экспортируем все инструменты для удобного импорта
from .weather import lookup_weather
from .get_tasks import get_tasks
from .search_web import search_web


__all__ = [
    "lookup_weather",
    "get_tasks",
    "search_web"
    # Добавьте другие названия функций
]