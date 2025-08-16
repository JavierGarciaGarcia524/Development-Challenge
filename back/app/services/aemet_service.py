import requests
from datetime import datetime, timedelta
import time

class AEMET_Client:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://opendata.aemet.es/opendata/api/antartida"
        self.max_safe_days = 30     # Through integration testing, discovered that with more than 30 days, the API returns an error
        self.max_attempts = 5
        self.fields = ["fhora", "nombre", "temp", "pres", "vel"]

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
        
        # Segment the request
        current_date = parsed_init_date
        all_data = []
        
        while current_date <= parsed_end_date:
            segment_end = min(current_date + timedelta(days=self.max_safe_days - 1), parsed_end_date)   # Calculate the minimum of (current + safe, end)
            segment_init_str = current_date.strftime("%Y-%m-%dT%H:%M:%SUTC")    # Calc segment init
            segment_end_str = segment_end.strftime("%Y-%m-%dT%H:%M:%SUTC")      # Calc segment end
            
            segment_data = None
            for attempt in range(self.max_attempts):
                try:
                    headers = {'Accept': 'application/json', 'api_key': self.api_key}
                    url = (
                        f"{self.base_url}/datos/"
                        f"fechaini/{segment_init_str}/"
                        f"fechafin/{segment_end_str}/"
                        f"estacion/{station}"
                    )
                    
                    response = requests.get(url, headers=headers)   # Add API key to request
                    response.raise_for_status()                     # Check first call status
                    
                    if response.status_code == 200:
                        data_url = response.json().get('datos')     # Extract the 'datos' URL from the 
                        if data_url:
                            datos_response = requests.get(data_url)
                            datos_response.raise_for_status()       # Check second call status
                            segment_data = datos_response.json()
                            break

                except Exception as e:
                    print(f"Attempt {attempt + 1} failed: {str(e)}")
                    if attempt == self.max_attempts - 1:
                        return None
                    time.sleep(2 ** attempt)
                    
            if segment_data:        # I will also be adding reduction right here (though redundant)
                filtered_segment = [
                    {field: item[field] for field in self.fields if field in item}
                    for item in segment_data
                ]
                all_data.extend(filtered_segment)
            else:
                return None

            current_date = segment_end + timedelta(seconds=1)   # Go to next segment
        return all_data if all_data else None
