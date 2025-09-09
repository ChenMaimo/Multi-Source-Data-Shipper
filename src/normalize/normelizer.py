from typing import Dict, Any, Optional

class UnifiedLog:
    @staticmethod
    def from_openweathermap(raw:Dict[str,Any])->Dict[str,Any]:
        city = raw.get("name")
        temp = (raw.get("main") or {}).get("temp")
        desc = None
        weather = raw.get("weather")
        if isinstance(weather, list) and weather:
            desc = (weather[0] or {}).get("description")
        return {
            "city": city,
            "temperature_celsius": temp,
            "description": desc,
            "source_provider": "openweathermap",
        }
    
    @staticmethod
    def from_weatherapi(raw:Dict[str,Any])->Dict[str,Any]:
        loc = raw.get("location") or {}
        cur = raw.get("current") or {}
        cond = cur.get("condition") or {}
        return {
            "city": loc.get("name"),
            "temperature_celsius": cur.get("temp_c"),
            "description": cond.get("text"),
            "source_provider": "weatherapi",
        }

    @staticmethod
    def from_csv(row:Dict[str,Any]) ->Dict[str,Any]:
        city =  row.get("city")
        temp_val: Optional[float] = None
        t = row.get("temperature")
        if t is not None and t != "":
            try:
                temp_val = float(t)
            except ValueError:
                temp_val = None
        return {
            "city": city,
            "temperature_celsius": temp_val,
            "description": row.get("description"),
            "source_provider": "file",
        }

