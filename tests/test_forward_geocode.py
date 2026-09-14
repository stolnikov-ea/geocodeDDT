import pytest

from utils.data_loader import load_data

FORWARD_DATA = load_data("forward_geocode.csv")

class TestForwardGeocode:

    @pytest.mark.parametrize(
        "address",
        [row["address"] for row in FORWARD_DATA],
        ids=[row["address"] for row in FORWARD_DATA],
    )
    def test_geocode_returns_200(self, client, address):
        result = client.geocode(address)
        assert result["status_code"] == 200

    @pytest.mark.parametrize(
        "address",
        [row["address"] for row in FORWARD_DATA],
        ids=[row["address"] for row in FORWARD_DATA],
    )
    def test_geocode_returns_coordinates(self, client, address):
        result = client.geocode(address)
        body = result["body"]
        assert "lat" in body
        assert "lon" in body

    @pytest.mark.parametrize(
        "address, expected_lat, expected_lon",
        [
            (row["address"], row["expected_lat"], row["expected_lon"])
            for row in FORWARD_DATA
        ],
        ids=[row["address"] for row in FORWARD_DATA],
    )

    def test_geocode_coordinates_in_valid_range(self, client, address, expected_lat, expected_lon):
        result = client.geocode(address)
        body = result["body"]
        lat = float(body["lat"])
        lon = float(body["lon"])
        assert -90 <= lat <= 90, f'Широта имеет невалидное значение: {lat}'
        assert -180 <= lon <= 180, f'Долгота имеет невалидное значение: {lon}'

    @pytest.mark.parametrize(
        "address, expected_lat, expected_lon",
        [
            (row["address"], row["expected_lat"], row["expected_lon"])
            for row in FORWARD_DATA
        ],
        ids=[row["address"] for row in FORWARD_DATA],
    )

    def test_geocode_coordinates_close_to_expected(self, client, address, expected_lat, expected_lon):
        result = client.geocode(address)
        body = result["body"]
        lat = float(body["lat"])
        lon = float(body["lon"])

        tolerance = 0.01

        assert abs(lat - expected_lat) <= tolerance
        assert abs(lon - expected_lon) <= tolerance