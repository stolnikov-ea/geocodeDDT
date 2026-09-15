import pytest

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

class TestReverseGeocodeNegative:

    @pytest.mark.parametrize(
        "lat, lon, expected_status, expected_error",
        ALL_PARAMS,
        ids = IDS,
    )
    def test_reverse_geocode_negative(self, client, lat, lon, expected_status, expected_error):

        result = client.geocode_reverse(lat, lon)

        assert result["status_code"] == expected_status

        body = result["body"]
        actual_error = ""

        if isinstance(body, dict) and "error" in body:
            error_data = body["error"]

            if isinstance(error_data, dict) and "message" in error_data:
                actual_error = body["error"].get("message", "")
            elif isinstance(error_data, str):
                actual_error = error_data

        assert actual_error == expected_error