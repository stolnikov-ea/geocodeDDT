import logging
import pytest

from config.settings import LOG_LEVEL, LOG_FORMAT

from src.geocoder_client import GeocoderClient

logger = logging.getLogger(__name__)

logging.basicConfig(
    level = getattr(logging, LOG_LEVEL),
    format = LOG_FORMAT,
)

@pytest.fixture(scope = "session")
def client():
    logger.info("Открываю GeocoderClient")

    geocoder_client = GeocoderClient()
    yield geocoder_client
    geocoder_client.close()

    logger.info("GeocoderClient закрыт")
