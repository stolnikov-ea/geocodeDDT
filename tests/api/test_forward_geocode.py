import pytest
import allure
from utils.data_loader import load_data_xml

DATA = load_data_xml("forward_geocode.xml")

POSITIVE_PARAMS = [
    (
        row["address"],
        row["expected_lat"],
        row["expected_lon"],
    )
    for row in DATA["positive"]
]

POSITIVE_ADDRESSES = [row["address"] for row in DATA["positive"]]

POSITIVE_IDS = POSITIVE_ADDRESSES

NEGATIVE_PARAMS = [
    (
        row["address"],
        row["expected_status"],
        row["expected_error"],
    )
    for row in DATA["negative"]
]

NEGATIVE_IDS = [row["address"] if row["address"] else "(empty)" for row in DATA["negative"]]

@allure.feature("Геокодирование [API]")
@allure.story("Прямое геокодирование")
@pytest.mark.api
@pytest.mark.forward
class TestForwardGeocodeApi:

    @staticmethod
    def _get_first_result(client, address: str) -> dict:
        result = client.geocode(address)
        body = result["body"]

        assert isinstance(body, list), f'Ожидался список, получен {type(body)}'
        assert len(body) > 0, f'Адрес "{address}" не найден, список пуст'

        return body[0]

    @allure.title("Проверка успешного ответа [200]")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.positive
    @pytest.mark.parametrize(
        "address",
        POSITIVE_ADDRESSES,
        ids = POSITIVE_IDS,
    )
    def test_returns_200(self, client, address: str):
        with allure.step(f"1. Отправляем запрос с адресом: {address}"):
            result = client.geocode(address)

        with allure.step("2. Проверяем, равен ли код ответа [200]"):
            assert result["status_code"] == 200

    @allure.title("Проверка наличия координат в ответе")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.positive
    @pytest.mark.parametrize(
        "address",
        POSITIVE_ADDRESSES,
        ids = POSITIVE_IDS,
    )
    def test_returns_coordinates(self, client, address: str):
        with allure.step(f"1. Отправляем запрос с адресом: {address}. Получаем первый объект из ответа"):
            first_item = self._get_first_result(client, address)

        with allure.step("2. Проверяем наличие координат в ответе"):
            with allure.step("2.1. Проверяем наличие широты в ответе"):
                assert "lat" in first_item
            with allure.step("2.2. Проверяем наличие долготы в ответе"):
                assert "lon" in first_item

    @allure.title("Проверка валидности значений координат")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.positive
    @pytest.mark.parametrize(
        "address, expected_lat, expected_lon",
        POSITIVE_PARAMS,
        ids = POSITIVE_IDS,
    )
    def test_coordinates_in_valid_range(self, client, address: str, expected_lat:float, expected_lon: float):
        with allure.step(f"1. Отправляем запрос с адресом: {address}. Получаем первый объект из ответа"):
            first_item = self._get_first_result(client, address)

        with allure.step("2. Достаем из ответа координаты"):
            lat = float(first_item["lat"])
            lon = float(first_item["lon"])

        with allure.step("3. Проверяем валидность значений координат"):
            with allure.step("3.1. Проверяем находится ли значение широты в пределах [-90; 90]"):
                assert -90 <= lat <= 90, f'Широта имеет невалидное значение: {lat}'
            with allure.step("3.2. Проверяем находится ли значение долготы в пределах [-180; 180]"):
                assert -180 <= lon <= 180, f'Долгота имеет невалидное значение: {lon}'

    @allure.title("Проверка соответствия значений координат ожидаемым")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.positive
    @pytest.mark.parametrize(
        "address, expected_lat, expected_lon",
        POSITIVE_PARAMS,
        ids = POSITIVE_IDS,
    )
    def test_coordinates_close_to_expected(self, client, address: str, expected_lat:float, expected_lon: float):
        with allure.step(f"1. Отправляем запрос с адресом: {address}. Получаем первый объект из ответа"):
            first_item = self._get_first_result(client, address)
        with allure.step("2. Достаем из ответа координаты"):
            lat = float(first_item["lat"])
            lon = float(first_item["lon"])

        tolerance = 0.01
        with allure.step("3. Проверяем корректность значений координат"):
            with allure.step(f"3.1. Проверяем совпадет ли значение широты с ожидаемым в пределах погрешности [{tolerance}]"):
                assert lat == pytest.approx(expected_lat, abs = tolerance)
            with allure.step(f"3.2. Проверяем совпадет ли значение долготы с ожидаемым в пределах погрешности [{tolerance}]"):
                assert lon == pytest.approx(expected_lon, abs = tolerance)

    @allure.title("Проверка ответа на невалидный запрос")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.negative
    @pytest.mark.parametrize(
        "address, expected_status, expected_error",
        NEGATIVE_PARAMS,
        ids = NEGATIVE_IDS,
    )
    def test_negative(self, client, address, expected_status, expected_error):
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