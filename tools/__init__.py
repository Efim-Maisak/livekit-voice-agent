# Экспортируем все инструменты для удобного импорта
from tools.weather import lookup_weather
# например: from tools.calendar import check_schedule, add_event



__all__ = [
    "lookup_weather",
    # Добавьте другие названия функций
]