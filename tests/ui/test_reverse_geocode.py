import pytest
import allure
import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from utils.data_loader import load_data

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
        url = "https://nominatim.openstreetmap.org/ui/reverse.html"
        with allure.step(f"1. Переходим на страницу: {url}"):
            driver.get(url)

        with allure.step(f"2. Вводим в поля широту [{lat}] и долготу [{lon}]"):
            lat_box = driver.find_element(By.ID, "reverse-lat")
            lat_box.send_keys(lat)
            lon_box = driver.find_element(By.ID, "reverse-lon")
            lon_box.send_keys(lon)

        with allure.step("3. Нажимаем кнопку Search"):
            search_section = driver.find_element(By.CLASS_NAME, "search-section")
            search_button = search_section.find_element(By.CLASS_NAME, "btn-primary")
            search_button.click()

        result_number = 1
        with allure.step(f"4. Открываем подробную информации о {result_number}-м результате поиска"):
            search_results_list = driver.find_element(By.ID, "searchresults")
            search_result_element = search_results_list.find_element(By.XPATH, f'.//div[@data-position="{result_number - 1}"]')
            search_result_element.click()
            details_button = search_result_element.find_element(By.CLASS_NAME, "btn-outline-secondary")
            details_button.click()

        with allure.step("5. Ищем адрес в подробной информации"):
            address_table = driver.find_element(By.ID, "address")
            name_text = address_table.find_element(By.XPATH, ".//tbody/tr[1]/td[1]").text

        with allure.step("6. Проверяем, соответствует ли адрес в ответе ожидаемому: {expected_address}"):
            assert expected_address.lower() in name_text.lower()