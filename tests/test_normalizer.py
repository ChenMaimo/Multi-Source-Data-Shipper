import pytest
from normalize.normelizer import UnifiedLog

def _as_dict(evt):
    if isinstance(evt, dict):
        return evt
    return evt.to_dict()

def _has_unified_keys(evt):
    evt = _as_dict(evt)
    assert set(evt.keys()) == {
        "city",
        "temperature_celsius",
        "description",
        "source_provider",
    }

def test_from_owm_basic():
    raw = {"name": "Tel Aviv", "main": {"temp": 28.3}, "weather": [{"description": "clear sky"}]}
    evt = UnifiedLog.from_openweathermap(raw)
    _has_unified_keys(evt)
    evt = _as_dict(evt)
    assert evt["city"] == "Tel Aviv"
    assert evt["temperature_celsius"] == 28.3
    assert evt["description"] == "clear sky"
    assert evt["source_provider"] == "openweathermap"

def test_from_wapi_basic():
    raw = {"location": {"name": "Jerusalem"}, "current": {"temp_c": 22.0, "condition": {"text": "Partly cloudy"}}}
    evt = UnifiedLog.from_weatherapi(raw)
    _has_unified_keys(evt)
    evt = _as_dict(evt)
    assert evt["city"] == "Jerusalem"
    assert evt["temperature_celsius"] == 22.0
    assert evt["description"] == "Partly cloudy"
    assert evt["source_provider"] == "weatherapi"

def test_from_csv_basic():
    row = {"city": "Berlin", "temperature": "18.5", "description": "Scattered clouds"}
    evt = UnifiedLog.from_csv(row)
    _has_unified_keys(evt)
    evt = _as_dict(evt)
    assert evt["city"] == "Berlin"
    assert evt["temperature_celsius"] == 18.5
    assert evt["description"] == "Scattered clouds"
    assert evt["source_provider"] == "file"

def test_from_owm_missing_weather_array():
    raw = {"name": "Tel Aviv", "main": {"temp": 28.3}, "weather": []}
    evt = UnifiedLog.from_openweathermap(raw)
    _has_unified_keys(evt)
    evt = _as_dict(evt)
    assert evt["description"] is None
