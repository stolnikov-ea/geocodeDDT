import pytest
import allure
from utils.data_loader import load_data
from src.ui_pages import GeocoderUI

REVERSE_DATA = load_data("reverse_geocode.csv")

ALL_PARAMS = [
    (
        row["lat"],
        row["lon"],
        row["expected_address"],
    )
    for row in REVERSE_DATA
]

IDS = [
    f'Широта: {row["lat"]} Долгота: {row["lon"]}'
    for row in REVERSE_DATA
]

@pytest.mark.ui
@allure.feature("Геокодирование [UI]")
@allure.story("Обратное геокодирование")
@pytest.mark.ui
@pytest.mark.reverse
@pytest.mark.positive
class TestReverseGeocodeUi:

    @allure.title("Проверка корректности координат при прямом геокодировании")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize(
        "lat, lon, expected_address",
        ALL_PARAMS,
        ids=IDS,
    )
    def test_reverse_geocode_search_max_zoom(self, driver, lat: float, lon: float, expected_address: str):
        ui = GeocoderUI(driver)

        with allure.step(f"1. Выполняем поиск по координатам. Широта: [{lat}], Долгота: [{lon}]"):
            ui.reverse_search(lat, lon)

        with allure.step(f"2. Открываем детали по первому результату поиска"):
            ui.open_details_for_first_result()

        with allure.step(f"3. Проверяем, соответствует ли адрес в ответе ожидаемому: {expected_address}"):
            actual_address = ui.get_address_name()
            assert expected_address.lower() in actual_address.lower()