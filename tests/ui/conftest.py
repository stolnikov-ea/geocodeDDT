import pytest
import logging
import allure
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

def pytest_exception_interact(node, call, report):
    if call.excinfo is not None:
        if "driver" in node.funcargs:
            driver = node.funcargs["driver"]
            try:
                screenshot_png = driver.get_screenshot_as_png()
                allure.attach(
                    body = screenshot_png,
                    name = "Скриншот в момент падения теста",
                    attachment_type = allure.attachment_type.PNG,
                )
                logger.info(f"Сделан скриншот для {node.nodeid}")
            except Exception as e:
                logger.warning(f"Не удалось сделать скриншот:: {e}")