import logging
from pathlib import Path
from datetime import datetime

from config.settings import USER_NAME, LOG_LEVEL, LOG_FORMAT
from src.geocoder_client import GeocoderClient

logging.basicConfig(
    level = getattr(logging, LOG_LEVEL),
    format = LOG_FORMAT,
)

def pytest_configure(config):
    allure_dir_raw = config.getoption("--alluredir")
    if allure_dir_raw:
        allure_path = Path(allure_dir_raw).resolve()
        allure_path.mkdir(parents=True, exist_ok=True)
        env_file = allure_path / "environment.properties"
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open (env_file, "w", encoding="utf-8") as f:
            f.write(f"Дата_запуска: {now}\n")
            f.write(f"Пользователь: {USER_NAME}\n")
            f.write(f"Проект: geocodeDDT\n")