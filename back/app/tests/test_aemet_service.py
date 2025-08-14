import pytest
from unittest.mock import patch, MagicMock
from app.services.aemet_service import AEMET_Client

# Dictionary of available stations
STATION_CODES = {
    "Meteo Station Gabriel de Castilla": "89065",
    "Meteo Station Juan Carlos I": "89064"
}

# I will be using mocks so far
@pytest.fixture     
def client():
    return AEMET_Client(api_key="FAKE_API_KEY")


def test_get_weather_data_success(client):
    # Case 1, two correct requests, with correct data
    mock_first_response = MagicMock(status_code=200)
    mock_first_response.json.return_value = {
        "datos": "https://fake-data-url.com/data.json"
    }

    mock_second_response = MagicMock(status_code=200)
    mock_second_response.json.return_value = {
        "temp": -2, "humidity": 70
    }

    with patch("app.services.aemet_service.requests.get", side_effect=[mock_first_response, mock_second_response]):
        result = client.get_weather_data(
            init_date="2025-08-01T00:00:00UTC",
            end_date="2025-08-02T00:00:00UTC",
            station=STATION_CODES["Meteo Station Gabriel de Castilla"]
        )

    assert result == {"temp": -2, "humidity": 70}


def test_no_data_key(client):
    # Case 2, first request returns invalid URL to the data
    mock_first_response = MagicMock(status_code=200)
    mock_first_response.json.return_value = {}

    with patch("app.services.aemet_service.requests.get", return_value=mock_first_response):
        result = client.get_weather_data(
            init_date="2025-08-01T00:00:00UTC",
            end_date="2025-08-02T00:00:00UTC",
            station=STATION_CODES["Meteo Station Juan Carlos I"]
        )

    assert result is None


def test_request_exception(client):
    # Case 3, connection error
    with patch("app.services.aemet_service.requests.get", side_effect=Exception("API error")):
        result = client.get_weather_data(
            init_date="2025-08-01T00:00:00UTC",
            end_date="2025-08-02T00:00:00UTC",
            station=STATION_CODES["Meteo Station Gabriel de Castilla"]
        )
    assert result is None


def test_invalid_date_range(client):
    # Case 4, invalid date range (e.g., end date is before start date)
    result = client.get_weather_data(
        init_date="2025-08-05T00:00:00UTC",
        end_date="2025-08-02T00:00:00UTC",  # Before start date
        station=STATION_CODES["Meteo Station Gabriel de Castilla"]
    )
    assert result is None


def test_invalid_station(client):
    # Case 5, invalid station code
    result = client.get_weather_data(
        init_date="2025-08-01T00:00:00UTC",
        end_date="2025-08-02T00:00:00UTC",
        station="INVALID"
    )
    assert result is None


def test_first_call_non_200(client):
    # Case 6, first call returns non-200 status
    mock_first_response = MagicMock(status_code=404)
    mock_first_response.raise_for_status.side_effect = Exception("Not Found")

    with patch("app.services.aemet_service.requests.get", return_value=mock_first_response):
        result = client.get_weather_data(
            init_date="2025-08-01T00:00:00UTC",
            end_date="2025-08-02T00:00:00UTC",
            station=STATION_CODES["Meteo Station Juan Carlos I"]
        )
    assert result is None

def test_second_call_non_200(client):
    # Case 6, second call returns non-200 status
    mock_first_response = MagicMock(status_code=200)
    mock_first_response.json.return_value = {"datos": "https://fake-data-url.com/data.json"}

    mock_second_response = MagicMock(status_code=500)
    mock_second_response.raise_for_status.side_effect = Exception("Server error")

    with patch("app.services.aemet_service.requests.get", side_effect=[mock_first_response, mock_second_response]):
        result = client.get_weather_data(
            init_date="2025-08-01T00:00:00UTC",
            end_date="2025-08-02T00:00:00UTC",
            station=STATION_CODES["Meteo Station Gabriel de Castilla"]
        )
    assert result is None

def test_invalid_date_format(client):
    # Case 7, invalid date format (remember it must follow this structure: YYYY-MM-DDTHH:MM:SSUTC)
    result = client.get_weather_data(
        init_date="2025/08/01",
        end_date="2025-08-02T00:00:00UTC",
        station=STATION_CODES["Meteo Station Juan Carlos I"]
    )
    assert result is None
