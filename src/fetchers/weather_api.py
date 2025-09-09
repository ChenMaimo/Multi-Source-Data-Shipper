import os
import requests
from typing import Dict, Any

class WeatherApiFetcher:
    def __init__(self) ->None:
        self.api_key = os.getenv("WEATHER_API_KEY")
        if not self.api_key:
            raise RuntimeError("Missing Weather Api Key")
        base = os.getenv("WEATHER_API_URL", "http://api.weatherapi.com/v1").strip().rstrip("/")
        self.base_url = f"{base}/current.json"
        self.session = requests.Session()

    def fetch_city(self, city_name:str)->Dict[str,Any]:
        params = {
            "key": self.api_key,
            "q": city_name
        }
        resp = self.session.get(self.base_url,params=params, timeout=8)
        resp.raise_for_status()
        return resp.json()