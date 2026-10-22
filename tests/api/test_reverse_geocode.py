import pytest
import allure
from utils.data_loader import load_data_xml

DATA = load_data_xml("reverse_geocode.xml")

POSITIVE_PARAMS = [
    (
        row["lat"],
        row["lon"],
        row["expected_address"],
    )
    for row in DATA["positive"]
]

POSITIVE_LAT_LON = [
    (
        row["lat"],
        row["lon"],
    )
    for row in DATA["positive"]
]

POSITIVE_IDS = [
    f'Широта: {row["lat"]} Долгота: {row["lon"]}'
    for row in DATA["positive"]
]

NEGATIVE_PARAMS = [
    (
        row["lat"],
        row["lon"],
        row["expected_status"],
        row["expected_error"],
    )
    for row in DATA["negative"]
]

NEGATIVE_IDS = [
    f'Широта: {row["lat"]} Долгота: {row["lon"]}'
    for row in DATA["negative"]
]

@allure.feature("Геокодирование [API]")
@allure.story("Обратное геокодирование")
@pytest.mark.api
@pytest.mark.reverse
class TestReverseGeocodeApi:

    @allure.title("Проверка успешного ответа [200]")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.positive
    @pytest.mark.parametrize(
        "lat, lon",
        POSITIVE_LAT_LON,
        ids = POSITIVE_IDS,
    )
    def test_returns_200(self, client, lat: float, lon: float):
        with allure.step(f"1. Отправляем запрос с широтой [{lat}] и долготой [{lon}]"):
            result = client.geocode_reverse(lat, lon)

        with allure.step("2. Проверяем, равен ли код ответа [200]"):
            assert result["status_code"] == 200

    @allure.title("Проверка наличия адреса в ответе")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.positive
    @pytest.mark.parametrize(
        "lat, lon",
        POSITIVE_LAT_LON,
        ids = POSITIVE_IDS,
    )
    def test_returns_display_name(self, client, lat: float, lon: float):
        with allure.step(f"1. Отправляем запрос с широтой [{lat}] и долготой [{lon}]"):
            result = client.geocode_reverse(lat, lon)
        with allure.step("2. Проверяем наличие адреса в ответе"):
            assert "display_name" in result["body"]

    @allure.title("Проверка корректности адреса в ответе")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.positive
    @pytest.mark.parametrize(
        "lat, lon, expected_address",
        POSITIVE_PARAMS,
        ids = POSITIVE_IDS,
    )
    def test_returns_correct_display_name(self, client, lat: float, lon: float, expected_address: str):
        with allure.step(f"1. Отправляем запрос с широтой [{lat}] и долготой [{lon}]"):
            result = client.geocode_reverse(lat, lon)

        with allure.step(f"2. Проверяем, соответствует ли адрес в ответе ожидаемому: {expected_address}"):
            assert expected_address.lower() in result["body"]["display_name"].lower()

    @allure.title("Проверка ответа на невалидный запрос")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.negative
    @pytest.mark.parametrize(
        "lat, lon, expected_status, expected_error",
        NEGATIVE_PARAMS,
        ids = NEGATIVE_IDS,
    )
    def test_negative(self, client, lat, lon, expected_status, expected_error):
        with allure.step(f"1. Отправляем запрос с широтой [{lat}] и долготой [{lon}]"):
            result = client.geocode_reverse(lat, lon)

        with allure.step(f"2. Проверяем, что код ответа равен {expected_status}"):
            assert result["status_code"] == expected_status

        with allure.step(f"3. Проверяем, что сообщение об ошибке: {expected_error}"):
            body = result["body"]
            actual_error = ""

            if isinstance(body, dict) and "error" in body:
                error_data = body["error"]

                if isinstance(error_data, dict) and "message" in error_data:
                    actual_error = body["error"].get("message", "")
                elif isinstance(error_data, str):
                    actual_error = error_data

            assert actual_error.lower() == expected_error.lower()
