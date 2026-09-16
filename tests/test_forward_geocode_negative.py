import pytest
import allure
from utils.data_loader import load_data

FORWARD_DATA_NEGATIVE = load_data("forward_geocode_negative.csv")

ALL_PARAMS = [
    (
        row["address"],
        row["expected_status"],
        row["expected_error"],
    )
    for row in FORWARD_DATA_NEGATIVE
]

IDS = [row["address"] for row in FORWARD_DATA_NEGATIVE]

@allure.feature("Геокодирование")
@allure.story("Прямое геокодирование. Негативные")
@pytest.mark.forward
@pytest.mark.negative
class TestForwardGeocodeNegative:

    @allure.title("Проверка ответа на невалидный запрос")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("api")
    @pytest.mark.parametrize(
        "address, expected_status, expected_error",
        ALL_PARAMS,
        ids=IDS,
    )
    def test_forward_geocode_negative(self, client, address, expected_status, expected_error):
        with allure.step(f"1. Отправляем запрос с адресом: {address}"):
            result = client.geocode(address)

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
