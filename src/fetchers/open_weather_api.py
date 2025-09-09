import requests
import os
from typing import Dict, Any

class OpenWeatherMapFetcher:
    def __init__(self)->None:
        self.api_key = os.getenv("OPEN_WEATHER_API")
        if not self.api_key:
            raise RuntimeError("Missing Open Weather Api Key")
        self.base_url = os.getenv("OPEN_WEATHER_API_URL","https://api.openweathermap.org/data/2.5/weather")
        self.session = requests.Session()

    def fetch_city(self,city_name:str)->Dict[str,Any]:
        params = {
            "q":city_name,
            "appid": self.api_key,
            "units":"metric"
        }
        resp = self.session.get(self.base_url, params=params, timeout=8)
        resp.raise_for_status()
        return resp.json()