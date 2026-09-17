import pytest
import allure
import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from utils.data_loader import load_data

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
        url = "https://nominatim.openstreetmap.org/ui/search.html"
        with allure.step(f"1. Переходим на страницу: {url}"):
            driver.get(url)

        results_limit = 1
        with allure.step(f"2. Ограничиваем количество результатов до {results_limit}"):
            advanced_options = driver.find_element(By.ID, "searchAdvancedOptions")
            advanced_options.click()
            option_limit_box = driver.find_element(By.ID, "option_limit")
            option_limit_box.send_keys(results_limit)

        with allure.step(f"3. Ищем по адресу: {address}"):
            search_box = driver.find_element(By.ID, "q")
            search_box.send_keys(address)
            search_box.send_keys(Keys.RETURN)

        result_number = 1
        with allure.step(f"4. Открываем подробную информации о {result_number}-м результате поиска"):
            search_results_list = driver.find_element(By.ID, "searchresults")
            search_result_element = search_results_list.find_element(By.XPATH, f'.//div[@data-position="{result_number - 1}"]')
            search_result_element.click()
            details_button = search_result_element.find_element(By.CLASS_NAME, "btn-outline-secondary")
            details_button.click()

        with allure.step("5. Ищем широту и долготу в подробной информации"):
            details_table = driver.find_element(By.ID, "locationdetails")
            lat_lon_text = details_table.find_element(By.XPATH, ".//tr[contains(.,'Centre Point')]/td[2]").text
            lat, lon = lat_lon_text.split(",")

        tolerance = 0.01
        with allure.step("6. Проверяем корректности значений координат"):
            with allure.step(f"6.1. Проверяем совпадет ли значение широты с ожидаемым в пределах погрешности [{tolerance}]"):
                assert float(lat) == pytest.approx(expected_lat, abs = tolerance)
            with allure.step(f"6.2. Проверяем совпадет ли значение долготы с ожидаемым в пределах погрешности [{tolerance}]"):
                assert float(lon) == pytest.approx(expected_lon, abs = tolerance)
