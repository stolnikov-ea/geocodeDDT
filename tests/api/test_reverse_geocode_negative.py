import pytest
import allure
from utils.data_loader import load_data

REVERSE_DATA_NEGATIVE = load_data("reverse_geocode_negative.csv")

ALL_PARAMS = [
    (
        row["lat"],
        row["lon"],
        row["expected_status"],
        row["expected_error"],
    )
    for row in REVERSE_DATA_NEGATIVE
]

IDS = [
    f'Широта: {row["lat"]} Долгота: {row["lon"]}'
    for row in REVERSE_DATA_NEGATIVE
]

@allure.feature("Геокодирование [API]")
@allure.story("Обратное геокодирование. Негативные")
@pytest.mark.api
@pytest.mark.reverse
@pytest.mark.negative
class TestReverseGeocodeNegativeApi:

    @allure.title("Проверка ответа на невалидный запрос")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize(
        "lat, lon, expected_status, expected_error",
        ALL_PARAMS,
        ids = IDS,
    )
    def test_reverse_geocode_negative(self, client, lat, lon, expected_status, expected_error):
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
