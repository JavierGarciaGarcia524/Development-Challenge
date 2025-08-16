import pytest
import os
import pandas as pd
from dotenv import load_dotenv
from app.services.aemet_service import AEMET_Client
from app.services.weather_utils import Weather_Utils
from tabulate import tabulate

# Dictionary of available stations
STATION_CODES = {
    "Meteo Station Gabriel de Castilla": "89065",
    "Meteo Station Juan Carlos I": "89064"
}

load_dotenv()
api_key = os.getenv("AEMET_API_KEY")

# Since the AEMET service is working, we will use it for the tests from now on, also using mock data since AEMET api only lets 5 querys per minute
@pytest.fixture     
def aemet_client():
    return AEMET_Client(api_key=api_key)

@pytest.fixture
def weather_utils():
    return Weather_Utils()

@pytest.fixture
def mock_weather_data():
    """ Fixture with mock data for testing """
    return [
        {
            "fhora": "2024-01-01T00:00:00UTC",
            "nombre": "Station1",
            "temp": 22.5,
            "pres": 1012,
            "vel": 10,
            "humedad": 60       # Added humidity, just to be eliminated in the process
        },
        {
            "fhora": "2024-01-01T01:00:00UTC",
            "nombre": "Station1",
            "temp": 22.3,
            "pres": 1013,
            "vel": 12,
            "humedad": 58       # Added humidity, just to be eliminated in the process
        }
    ]
    
def test_process_with_empty_data(weather_utils):
    # Case 1, test with no data
    result = weather_utils.process_aemet_data([], [], None)
    assert result is None
    
def test_process_with_missing_fhora(weather_utils):
    # Case 2, data without 'fhora'
    bad_data = [{"nombre": "Station1", "temp": 22.5}]
    result = weather_utils.process_aemet_data(bad_data, [], None)
    assert result is None

def test_process_basic_columns(mock_weather_data, weather_utils):
    # Case 3, test with basic columns without aggregation nor selection
    result = weather_utils.process_aemet_data(mock_weather_data, [], None)
    
    assert isinstance(result, pd.DataFrame)
    assert set(result.columns) == {'fhora','nombre', 'temp', 'pres', 'vel'}

def test_process_with_feature_selection(mock_weather_data, weather_utils):
    # Case 4, test with specific feature selection
    result = weather_utils.process_aemet_data(mock_weather_data, ['temp'], None)
    
    assert 'temp' in result.columns
    assert 'pres' not in result.columns
    assert 'vel' not in result.columns

def test_daily_aggregation(weather_utils):
    # Case 5, test daily aggregation
    daily_mock = [
        {"fhora": "2024-01-01T00:00:00UTC", "nombre": "Station1", "temp": 22, "pres": 1010, "vel": 12},
        {"fhora": "2024-01-01T01:00:00UTC", "nombre": "Station1", "temp": 24, "pres": 1012, "vel": 14},
        {"fhora": "2024-01-02T00:00:00UTC", "nombre": "Station1", "temp": 20, "pres": 1008, "vel": 10}
    ]
    
    result = weather_utils.process_aemet_data(daily_mock, [], 'daily')
    print(result.head(5))
    assert len(result) == 2  # Only 2 days
    
    avrg_1st_january = result.iloc[0, 2]    # First instance, third value (1st january, temp) should contain the average (22-24) = 23
    assert avrg_1st_january == 23

def test_monthly_aggregation(weather_utils):
    # Case 6, test monthly aggregation
    monthly_mock = [
        {"fhora": "2024-01-01T00:00:00UTC", "nombre": "Station1", "temp": 22, "pres": 1010, "vel": 12},
        {"fhora": "2024-01-15T00:00:00UTC", "nombre": "Station1", "temp": 24, "pres": 1012, "vel": 14},
        {"fhora": "2024-02-01T00:00:00UTC", "nombre": "Station1", "temp": 20, "pres": 1008, "vel": 10}
    ]
    
    result = weather_utils.process_aemet_data(monthly_mock, [], 'monthly')
    print(result.head(5))
    assert len(result) == 2  # Only 2 months
    target = pd.Timestamp("2024-01-01 00:00:00", tz="Europe/Madrid")

    avrg_january = result.iloc[0, 2]    # First instance, third value (january, temp) should contain the average (22-24) = 23
    assert avrg_january == 23


def test_timezone_conversion(weather_utils):
    # Case 7, test timezone conversion
    tz_mock = [
        {"fhora": "2024-01-01T00:00:00UTC", "nombre": "Station1", "temp": 22.5}
    ]
    
    # Process without specific aggregation
    result = weather_utils.process_aemet_data(tz_mock, ["temp"], None)

    # Check if timezone is adapted properly
    fhora0 = pd.to_datetime(result.iloc[0]['fhora'])
    assert fhora0.tzinfo is not None, "fhora should have timezone info"
    print("fhora[0]:", fhora0)


def test_process_aemet_data_complete(aemet_client, weather_utils):
    # Case 8, try the complete process, query and process the data
    # Mock example
    init_date = "2024-01-01T00:00:00UTC"    # For this example I will pass hours in UTC, since Madrid - UTC conversion takes place in the request (Despite if not done, an hour is miscounted for each mean)
    end_date  = "2024-03-31T23:59:59UTC"
    station = "89064"

    # Obtain data
    raw_data = aemet_client.get_weather_data(init_date, end_date, station)
    assert raw_data is not None, "No data obtained"
    # Process
    df = weather_utils.process_aemet_data(raw_data, [], 'daily')

    # Show head for debugging
    print(df.head(5))
    assert df is not None,                  "Result should not be none"
    assert isinstance(df, pd.DataFrame),    "Result should be a dataframe"
    assert df['fhora'].dtype == object or pd.api.types.is_datetime64_any_dtype(df['fhora']), \
        f"'fhora' column should be datetime, got {df['fhora'].dtype}"
    for col in ['temp', 'pres', 'vel']:
        assert pd.api.types.is_numeric_dtype(df[col]), f"Column {col} should be numeric"
    assert df['temp'].min() > -50 and df['temp'].max() < 60,    "Temperature values are unrealistic"
    assert df['pres'].min() > 800 and df['pres'].max() < 1100,  "Pressure values are unrealistic"
    assert df['vel'].min() >= 0,                                "Wind speed cannot be negative"

    """
    NOTE: The dataframe will contain the following columns:
    - 'fhora': The timestamp of the observation
    - 'nombre': The name of the weather station
    - 'temp': The temperature reading
    - 'pres': The pressure reading
    - 'vel': The wind speed reading
    """
