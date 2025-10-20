from dotenv import load_dotenv
load_dotenv()

import os
import time
import logging
from src.logging_conf import setup_logging
from src import config

from src.fetchers.open_weather_api import OpenWeatherMapFetcher
from src.fetchers.weather_api import WeatherApiFetcher
from src.fetchers.csv_fetcher import CsvFetcher
from src.normalize.normelizer import (UnifiedLog, OwmNormalizer, WeatherApiNormalizer, CsvNormalizer)
from src.shipper.logzio_shipper import LogzioShipper

log = logging.getLogger("main")

def build_dependencies():
    own = OpenWeatherMapFetcher()
    wapi = WeatherApiFetcher()
    csv_fetcher = CsvFetcher(config.CSV_FILE)

    owm_norm = OwmNormalizer()
    wapi_norm = WeatherApiNormalizer()
    csv_norm = CsvNormalizer()

    shipper = LogzioShipper()
    return (own, owm_norm), (wapi, wapi_norm), (csv_fetcher, csv_norm), shipper

def run_once(ship: bool = True) -> None:
    events = []

    (owm, owm_norm), (wapi, wapi_norm), (csv_fetcher, csv_norm), shipper = build_dependencies()


    log.info("Polling %d cities from OWM + WeatherAPI, and CSV=%s", len(config.CITIES), config.CSV_FILE)

    for city in config.CITIES:
        try:
            raw = owm.fetch_city(city)
            evt = UnifiedLog.from_openweathermap(raw)
            eve_to_ship = evt.model_dump()
            events.append(eve_to_ship)
            log.info("OWM normalized city=%s temp=%s desc=%s", evt.city, evt.temperature_celsius, evt.description)
        except Exception as e:
            log.exception("OWM fetch failed city=%s: %s", city, e)

    for city in config.CITIES:
        try:
            raw = wapi.fetch_city(city)
            evt = UnifiedLog.from_weatherapi(raw)
            eve_to_ship = evt.model_dump()
            events.append(eve_to_ship)
            log.info("OWM normalized city=%s temp=%s desc=%s",
                     evt.city, evt.temperature_celsius, evt.description)
        except Exception as e:
            log.exception("WAPI fetch failed city=%s: %s", city, e)

    try:
        count = 0
        for row in csv_fetcher.fetch():
            evt: UnifiedLog = csv_norm.normalize(row)
            events.append(evt.model_dump())
            count += 1
        log.info("CSV normalized rows=%d", count)
    except Exception as e:
        log.exception("CSV fetch failed: %s", e)

    if ship and events:
        log.info("Shipping %d events to Logz.io", len(events))
        shipper.ship(events)
        log.info("Sent %d events to Logz.io", len(events))
    else:
        log.info("Dry run only: %d events", len(events))
        for e in events:
            print(e)


def run_forever() -> None:
    setup_logging()
    poll = config.POLL_INTERVAL_SEC
    ship = os.getenv("DRY_RUN", "0") != "1"
    log.info("Starting poller interval=%ss ship=%s", poll, ship)
    try:
        while True:
            try:
                run_once(ship=ship)
            except Exception as e:
                log.exception("Cycle failed: %s", e)
            time.sleep(poll)
    except KeyboardInterrupt:
        log.info("Shutting down gracefully (Ctrl+C)")

if __name__ == "__main__":
    run_forever()