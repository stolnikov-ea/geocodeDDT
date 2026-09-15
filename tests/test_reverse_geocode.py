import pytest

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

class TestReverseGeocode:

    @pytest.mark.parametrize(
        "lat, lon",
        SENT_PARAMS,
        ids = IDS,
    )
    def test_reverse_geocode_returns_200(self, client, lat, lon):
        result = client.geocode_reverse(lat, lon)
        assert result["status_code"] == 200

    @pytest.mark.parametrize(
        "lat, lon",
        SENT_PARAMS,
        ids=IDS,
    )
    def test_reverse_geocode_returns_display_name(self, client, lat, lon):
        result = client.geocode_reverse(lat, lon)
        assert "display_name" in result["body"]

    @pytest.mark.parametrize(
        "lat, lon, expected_address",
        ALL_PARAMS,
        ids = IDS,
    )
    def test_reverse_geocode_returns_correct_display_name(self, client, lat, lon, expected_address):
        result = client.geocode_reverse(lat, lon)
        assert result["body"]["display_name"] == expected_address