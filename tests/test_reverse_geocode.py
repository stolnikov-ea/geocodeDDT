import pytest
import allure
from utils.data_loader import load_data

REVERSE_DATA = load_data("reverse_geocode.csv")

SENT_PARAMS = [
    (
        row["lat"],
        row["lon"],
    )
    for row in REVERSE_DATA
]

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

@allure.feature("Геокодирование")
@allure.story("Обратное геокодирование")
@pytest.mark.reverse
@pytest.mark.positive
class TestReverseGeocode:

    @allure.title("Проверка успешного ответа [200]")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("api")
    @pytest.mark.parametrize(
        "lat, lon",
        SENT_PARAMS,
        ids = IDS,
    )
    def test_reverse_geocode_returns_200(self, client, lat: float, lon: float):
        with allure.step(f"1. Отправляем запрос с широтой [{lat}] и долготой [{lon}]"):
            result = client.geocode_reverse(lat, lon)

        with allure.step("2. Проверяем, равен ли код ответа [200]"):
            assert result["status_code"] == 200

    @allure.title("Проверка наличия адреса в ответе")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("api")
    @pytest.mark.parametrize(
        "lat, lon",
        SENT_PARAMS,
        ids=IDS,
    )
    def test_reverse_geocode_returns_display_name(self, client, lat: float, lon: float):
        with allure.step(f"1. Отправляем запрос с широтой [{lat}] и долготой [{lon}]"):
            result = client.geocode_reverse(lat, lon)
        with allure.step("2. Проверяем наличие адреса в ответе"):
            assert "display_name" in result["body"]

    @allure.title("Проверка корректности адреса в ответе")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("api")
    @pytest.mark.parametrize(
        "lat, lon, expected_address",
        ALL_PARAMS,
        ids = IDS,
    )
    def test_reverse_geocode_returns_correct_display_name(self, client, lat: float, lon: float, expected_address: str):
        with allure.step(f"1. Отправляем запрос с широтой [{lat}] и долготой [{lon}]"):
            result = client.geocode_reverse(lat, lon)

        with allure.step(f"2. Проверяем, соответствует ли адрес в ответе ожидаемому: {expected_address}"):
            assert expected_address.lower() in result["body"]["display_name"].lower()