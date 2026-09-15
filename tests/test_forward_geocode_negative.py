import pytest

from utils.data_loader import load_data

FORWARD_DATA_NEGATIVE = load_data("forward_geocode_negative.csv")

NEGATIVE_PARAMS = [
    (
        row["address"],
        row["expected_status"],
        row["expected_error"],
    )
    for row in FORWARD_DATA_NEGATIVE
]
NEGATIVE_IDS = [row["address"] for row in FORWARD_DATA_NEGATIVE]

class TestForwardGeocodeNegative:

    @pytest.mark.parametrize(
        "address, expected_status, expected_error",
        NEGATIVE_PARAMS,
        ids=NEGATIVE_IDS,
    )
    def test_forward_geocode_negative(self, client, address, expected_status, expected_error):

        result = client.geocode(address)

        assert result["status_code"] == expected_status

        body = result["body"]

        if isinstance(body, dict) and "error" in body:
            actual_error = body["error"].get("message", "")
        else:
            actual_error = ""

        assert actual_error == expected_error
