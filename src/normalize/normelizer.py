from typing import Dict, Any, Optional
from enum import Enum
from pydantic import field_validator, BaseModel

class Source(str, Enum):
    openweathermap ="openweathermap"
    weatherapi = "weatherapi"
    file = "file"

class UnifiedLog(BaseModel):
    city: Optional[str] = None
    temperature_cel: Optional[float] = None
    description: Optional[str] = None
    source_provider: Source

    def _into_float(value:Any) ->Optional[float]:
        if value is None or value == "":
            return None
        try:
            return float(value)
        except (TypeError, ValueError):
            return None
        
    def _first_or_none(seq:Any) ->Any:
        return seq[0] if isinstance(seq, list) and seq else None
    
    @field_validator("description", mode="before")
    @classmethod
    def _clean_desc(cls, v: Any) -> Any:
        if isinstance(v,str):
            v= v.strip()
            return v if v else None
        return v

    @field_validator("city", mode="before")
    @classmethod
    def _clean_city(cls, v:Any) -> Any:
        if isinstance(v,str):
            v = v.strip()
            return v if v else None
        return v


    @classmethod
    def from_openweathermap(cls, raw:Dict[str,Any])->"UnifiedLog":
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
    
    @classmethod
    def from_weatherapi(cls, raw:Dict[str,Any])->"UnifiedLog":
        loc = raw.get("location") or {}
        cur = raw.get("current") or {}
        cond = cur.get("condition") or {}
        return {
            "city": loc.get("name"),
            "temperature_celsius": cur.get("temp_c"),
            "description": cond.get("text"),
            "source_provider": "weatherapi",
        }

    @classmethod
    def from_csv(cls, row:Dict[str,Any]) ->"UnifiedLog":
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
    
    def to_dict(self)->Dict[str, Any]:
        return self.model_dump()

