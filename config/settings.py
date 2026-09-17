"""
Конфигурация проекта geocodeDDT

Все изменяемые параметры вынесены сюда
"""

import os

# API
API_BASE_URL = "https://nominatim.openstreetmap.org"                    # базовый URL
API_TIMEOUT = 10                                                        # время ожидания ответа, сек.
API_RETRY_COUNT = 3                                                     # количество попыток при неудачном запросе
API_RETRY_DELAY = 5                                                     # таймаут
API_MIN_INTERVAL = 1.0                                                  # минимальные интервал между запросами, сек. (минимум 1 секундла для Nominatim)

#Пользовательские данные
USER_EMAIL = os.getenv("USER_EMAIL", "unknown@mail.ru")                 # почта указывается по требованиям Nominatim
USER_NAME = os.getenv("USER_NAME", "Unknown User")                      # имя пользователя указывается для отображения в отчете Allure

# Логирование
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")                              # уровень логирования
LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"        # формат вывода логов