from datetime import datetime

class WeatherUtils:
    @staticmethod
    def format_aemet_date(dt: datetime) -> str:
        return dt.strftime("%Y-%m-%dT%H:%M:%SUTC")
