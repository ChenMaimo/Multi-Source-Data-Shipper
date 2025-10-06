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
        weather = cls._first_or_none(raw.get("weather"))
        desc = (weather or {}).get("description")
        temp_val = (raw.get("main") or {}).get("temp")
        temp_c = cls._coerce_float(temp_val)
       
        return cls(
            city=raw.get("name"),
            temperature_celsius=temp_c,
            description=desc,
            source_provider=Source.openweathermap,
        )
    
    @classmethod
    def from_weatherapi(cls, raw:Dict[str,Any])->"UnifiedLog":
        loc = raw.get("location") or {}
        cur = raw.get("current") or {}
        cond = cur.get("condition") or {}
        return cls(
            city=loc.get("name"),
            temperature_celsius=cls._coerce_float(cur.get("temp_c")),
            description=cond.get("text"),
            source_provider=Source.weatherapi,
        )

    @classmethod
    def from_csv(cls, row:Dict[str,Any]) ->"UnifiedLog":
        return cls(
            city=row.get("city"),
            temperature_celsius=cls._coerce_float(row.get("temperature")),
            description=row.get("description"),
            source_provider=Source.file,
        )
    
    def to_dict(self)->Dict[str, Any]:
        return self.model_dump()

