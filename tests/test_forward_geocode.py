import pytest

from utils.data_loader import load_data

FORWARD_DATA = load_data("forward_geocode.csv")

ADDRESS_PARAMS = [row["address"] for row in FORWARD_DATA]
ADDRESS_IDS = ADDRESS_PARAMS
COORDS_PARAMS = [
    (
        row["address"],
        float(row["expected_lat"]),
        float(row["expected_lon"]),
    )
    for row in FORWARD_DATA
]



class TestForwardGeocode:

    @staticmethod
    def _get_first_result(client, address: str) -> dict:
        result = client.geocode(address)
        body = result["body"]
        assert isinstance(body, list), f'Ожидался список, получен {type(body)}'
        assert len(body) > 0, f'Адрес "{address}" не найден, список пуст'
        return body[0]

    @pytest.mark.parametrize(
        "address",
        ADDRESS_PARAMS,
        ids = ADDRESS_IDS,
    )
    def test_geocode_returns_200(self, client, address):
        result = client.geocode(address)
        assert result["status_code"] == 200

    @pytest.mark.parametrize(
        "address",
        ADDRESS_PARAMS,
        ids = ADDRESS_IDS,
    )
    def test_geocode_returns_coordinates(self, client, address):
        first_item = self._get_first_result(client, address)
        assert "lat" in first_item
        assert "lon" in first_item

    @pytest.mark.parametrize(
        "address, expected_lat, expected_lon",
        COORDS_PARAMS,
        ids = ADDRESS_IDS,
    )

    def test_geocode_coordinates_in_valid_range(self, client, address, expected_lat, expected_lon):
        first_item = self._get_first_result(client, address)
        lat = float(first_item["lat"])
        lon = float(first_item["lon"])
        assert -90 <= lat <= 90, f'Широта имеет невалидное значение: {lat}'
        assert -180 <= lon <= 180, f'Долгота имеет невалидное значение: {lon}'

    @pytest.mark.parametrize(
        "address, expected_lat, expected_lon",
        COORDS_PARAMS,
        ids = ADDRESS_IDS,
    )

    def test_geocode_coordinates_close_to_expected(self, client, address, expected_lat, expected_lon):
        first_item = self._get_first_result(client, address)
        lat = float(first_item["lat"])
        lon = float(first_item["lon"])

        tolerance = 0.01

        assert abs(lat - expected_lat) <= tolerance
        assert abs(lon - expected_lon) <= tolerance