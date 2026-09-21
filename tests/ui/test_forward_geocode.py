import pytest
import allure
from utils.data_loader import load_data
from src.ui_pages import GeocoderUI

FORWARD_DATA = load_data("forward_geocode.csv")

ALL_PARAMS = [
    (
        row["address"],
        row["expected_lat"],
        row["expected_lon"],
    )
    for row in FORWARD_DATA
]

IDS = [row["address"] for row in FORWARD_DATA]

@pytest.mark.ui
@allure.feature("Геокодирование [UI]")
@allure.story("Прямое геокодирование")
@pytest.mark.ui
@pytest.mark.forward
@pytest.mark.positive
class TestForwardGeocodeUi:
    @allure.title("Проверка корректности координат при прямом геокодировании")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize(
        "address, expected_lat, expected_lon",
        ALL_PARAMS,
        ids = IDS,
    )
    def test_forward_geocode_simple_search(self, driver, address: str, expected_lat: float, expected_lon: float):
        ui = GeocoderUI(driver)

        with allure.step(f"1. Выполняем поиск по адресу: {address}"):
            ui.forward_search(address)

        with allure.step(f"2. Открываем детали по первому результату поиска"):
            ui.open_details_for_first_result()

        with allure.step("3. Проверяем корректности значений координат"):
            lat, lon = ui.get_coordinates()
            tolerance = 0.01
            with allure.step(f"3.1. Проверяем совпадет ли значение широты с ожидаемым в пределах погрешности [{tolerance}]"):
                assert lat == pytest.approx(expected_lat, abs = tolerance)
            with allure.step(f"3.2. Проверяем совпадет ли значение долготы с ожидаемым в пределах погрешности [{tolerance}]"):
                assert lon == pytest.approx(expected_lon, abs = tolerance)
