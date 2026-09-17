import selenium
import pytest
import allure


@pytest.mark.ui
@allure.feature("Геокодирование")
@allure.story("Прямое геокодирование")
@pytest.mark.ui
@pytest.mark.forward
@pytest.mark.positive
class TestForwardGeocodeUi:

    pass