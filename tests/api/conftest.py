import logging
import pytest

from src.geocoder_client import GeocoderClient

logger = logging.getLogger(__name__)

@pytest.fixture(scope = "session")
def client():
    logger.info("Открываю GeocoderClient")
    geocoder_client = GeocoderClient()
    yield geocoder_client
    geocoder_client.close()
    logger.info("GeocoderClient закрыт")