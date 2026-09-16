import logging
import pytest
import allure
import os
from datetime import datetime

from config.settings import USER_NAME, LOG_LEVEL, LOG_FORMAT
from src.geocoder_client import GeocoderClient

logging.basicConfig(
    level = getattr(logging, LOG_LEVEL),
    format = LOG_FORMAT,
)

logger = logging.getLogger(__name__)

def pytest_configure(config):

    allure_dir = config.getoption("--alluredir")
    env_file = os.path.join(allure_dir, "environment.properties")
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open (env_file, "a") as f:
        f.write(f"Дата_запуска: {now}\n")
        f.write(f"Пользователь: {USER_NAME}\n")
        f.write(f"Проект: geocodeDDT\n")

@pytest.fixture(scope = "session")
def client():
    logger.info("Открываю GeocoderClient")

    geocoder_client = GeocoderClient()
    yield geocoder_client
    geocoder_client.close()

    logger.info("GeocoderClient закрыт")