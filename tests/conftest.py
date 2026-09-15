import logging
import pytest
import allure
from datetime import datetime

from config.settings import USER_NAME, LOG_LEVEL, LOG_FORMAT
from src.geocoder_client import GeocoderClient

logging.basicConfig(
    level = getattr(logging, LOG_LEVEL),
    format = LOG_FORMAT,
)

logger = logging.getLogger(__name__)

def pytest_configure(config):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if hasattr(config, "allure_properties"):
        config.allure_properties.append(("Дата запуска", now))
        config.allure_properties.append(("Пользователь", USER_NAME))
        config.allure_properties.append(("Проект", "geocodeDDT"))

@pytest.fixture(scope = "session")
def client():
    logger.info("Открываю GeocoderClient")

    geocoder_client = GeocoderClient()
    yield geocoder_client
    geocoder_client.close()

    logger.info("GeocoderClient закрыт")