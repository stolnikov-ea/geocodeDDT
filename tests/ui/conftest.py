import pytest
import logging
from selenium import webdriver

logger = logging.getLogger(__name__)

@pytest.fixture(scope="function")
def driver():
    browser = webdriver.Chrome()
    logger.info("Открываю экземпляр Google Chrome")
    browser.implicitly_wait(5)
    yield browser
    browser.quit()
    logger.info("Закрываю экземпляр Google Chrome")