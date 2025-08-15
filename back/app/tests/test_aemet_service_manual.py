from datetime import datetime
from app.services.aemet_service import AEMET_Client

# This is just temporal for manual testing
client = AEMET_Client(api_key="eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJqYXZnYXIwMjAxMDRAZ21haWwuY29tIiwianRpIjoiN2RjODYyZTAtM2IyNy00MDlkLThmZDYtMDgyYWMyYmQzY2Q4IiwiaXNzIjoiQUVNRVQiLCJpYXQiOjE3NTUxMTE5MDIsInVzZXJJZCI6IjdkYzg2MmUwLTNiMjctNDA5ZC04ZmQ2LTA4MmFjMmJkM2NkOCIsInJvbGUiOiIifQ.p4MYYeAiGSy_U8NYBNre4bNzo68mMYi2kyVka2GTaCU")

init_date = "2024-01-01T00:00:00UTC"
end_date  = "2024-01-02T23:59:59UTC"
station = "89064"

data = client.get_weather_data(init_date, end_date, station)

if data is None:
    print("No data available or an error occurred")
else:
    print("Data obtained successfully:")
    print(data)
