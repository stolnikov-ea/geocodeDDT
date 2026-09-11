"""
Конфигурация проекта geocodeDDT

Все изменяемые параметры вынесены сюда
"""

import os

# API
API_BASE_URL = "https://nominatim.openstreetmap.org"
API_TIMEOUT = 10                # время ожидания ответа, сек.
API_RETRY_COUNT = 3             # количество попыток при неудачном запросе
API_RETRY_DELAY = 5             # таймаут
API_MIN_INTERVAL = 1.0          # минимальные интервал между запросами, сек.

# Логирование

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"