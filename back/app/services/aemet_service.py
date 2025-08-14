import requests
from datetime import datetime

class AEMET_Client:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://opendata.aemet.es/opendata/api/antartida"

    def get_weather_data(self, init_date, end_date, station):
        # Obtain all data from aemet. Reminder that dates must follow the format: YYYY-MM-DDTHH:MM:SSUTC. Will add this at the weather_utils.py file
        # Date validation, just done to double check
        try:
            parsed_init_date = datetime.strptime(init_date, "%Y-%m-%dT%H:%M:%SUTC")
            parsed_end_date = datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%SUTC")
            if parsed_end_date < parsed_init_date:
                print("Dates range error")
                return None
        except ValueError as e:
            print(f"Date format error: {str(e)}")
            return None
        # Request structure building
        headers = {'api_key': self.api_key}
        url = (
            f"{self.base_url}/datos/"
            f"fechaini/{init_date}/"
            f"fechafin/{end_date}/"
            f"estacion/{station}"
        )
        try:
            # Initial petition to access the real data URL
            response = requests.get(url, headers=headers)   # Add API key to request
            response.raise_for_status()                     # Check first call status
            if response.status_code == 200:
                data_url = response.json().get('datos')     # Extract the 'datos' URL from the response (In AEMET, 'datos' does not contain the data itself, but the URL to them)
                if data_url != None:
                    # Second call for real data
                    datos_response = requests.get(data_url)
                    datos_response.raise_for_status()       # Check second call status
                    return datos_response.json()
            return None
        except Exception as e:
            print(f"Error in AEMET API: {str(e)}")
            return None
