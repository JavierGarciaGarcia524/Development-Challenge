import pytest
from app import create_app
from app.routes import aemet_client, weather_utils
from dotenv import load_dotenv
load_dotenv()

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    res = client.get("/api/")
    assert res.status_code == 200
    assert "Working" in res.get_data(as_text=True)

@pytest.mark.parametrize(
    "params",
    [
        ({'init_date': '2024-01-01', 'end_date': '2024-01-02'}),          # missing station
        ({'station': '89064', 'end_date': '2024-01-02'}),                 # missing init_date
        ({'station': '89064', 'init_date': '2024-01-01'}),                # missing end_date
        ({})                                                              # all missing
    ]
)
def test_weather_missing_required_params(client, params):
    # Case 1, test missing required query parameters
    res = client.get("/api/weather", query_string=params)
    assert res.status_code == 400
    assert "Missing basic parameters" in res.get_data(as_text=True)

def test_weather_valid(client, monkeypatch):
    # Case 2, test valid request with mocked AEMET data and processing
    # Mock AEMET_Client.get_weather_data
    class MockAemet:
        def get_weather_data(self, start, end, station):
            return [{"fhora": "2024-01-01T00:00:00", "temp": 10}]
    # Mock Weather_Utils.process_aemet_data
    class MockUtils:
        def process_aemet_data(self, raw_data, features, agg):
            import pandas as pd
            df = pd.DataFrame(raw_data).set_index('fhora')
            return df

    
    monkeypatch.setattr(aemet_client, "get_weather_data", MockAemet().get_weather_data)
    monkeypatch.setattr(weather_utils, "process_aemet_data", MockUtils().process_aemet_data)

    res = client.get("/api/weather", query_string={
        'station': '89064',
        'init_date': '2024-01-01',
        'end_date': '2024-03-31'
    })

    assert res.status_code == 200
    data = res.get_json()
    assert isinstance(data, list)
    assert data[0]["temp"] == 10
    
def test_real_process(client):
    # Case 3, test full API process with real request and data
    params = {
        "station": "89064",
        "init_date": "2024-01-01",
        "end_date": "2024-01-31",
        "desired_features[]": [],
        "aggregation_value": None
    }
    
    res = client.get('/api/weather', query_string=params)
    
    assert res.status_code == 200
    data = res.get_json()

    assert isinstance(data, list), "Should be JSON list"
    assert len(data) > 0, "There should be at least one record"
    assert "fhora" in data[0], "Records must contain 'fhora'"
    print(data[0])
    print(data[1])
    print(data[2])
    print(data[3])
    print(data[4])
    
    """
    NOTE: The JSON will contain the following attributes:
    - 'fhora': The timestamp of the observation
    + 'index': added automatically through conversion process
    - 'nombre': The name of the weather station
    - 'temp': The temperature reading
    - 'pres': The pressure reading
    - 'vel': The wind speed reading
    """
    
    # We can see equivalences are done correctly, still the problem of ignoring Madrid's 00:00 (Solved converting to equivalence)
    """
    fhora                      nombre                      temp pres   vel
    2024-01-01 01:00:00+01:00  JCI Estacion meteorologica  2.4  990.8  1.3 = {'fhora': 'Mon, 01 Jan 2024 00:00:00 GMT', 'nombre': 'JCI Estacion meteorologica', 'pres': 990.8, 'temp': 2.4, 'vel': 1.3}
    2024-01-01 01:10:00+01:00  JCI Estacion meteorologica  2.4  990.8  1.1 = {'fhora': 'Mon, 01 Jan 2024 00:10:00 GMT', 'nombre': 'JCI Estacion meteorologica', 'pres': 990.8, 'temp': 2.4, 'vel': 1.1}
    2024-01-01 01:20:00+01:00  JCI Estacion meteorologica  2.4  990.9  1.3 = {'fhora': 'Mon, 01 Jan 2024 00:20:00 GMT', 'nombre': 'JCI Estacion meteorologica', 'pres': 990.9, 'temp': 2.4, 'vel': 1.3}
    2024-01-01 01:30:00+01:00  JCI Estacion meteorologica  2.4  991.1  0.9 = {'fhora': 'Mon, 01 Jan 2024 00:30:00 GMT', 'nombre': 'JCI Estacion meteorologica', 'pres': 991.1, 'temp': 2.4, 'vel': 0.9}
    2024-01-01 01:40:00+01:00  JCI Estacion meteorologica  2.3  991.2  1.4 = {'fhora': 'Mon, 01 Jan 2024 00:40:00 GMT', 'nombre': 'JCI Estacion meteorologica', 'pres': 991.2, 'temp': 2.3, 'vel': 1.4}
    """