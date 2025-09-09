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
from src.normalize.normelizer import UnifiedLog
from src.shipper.logzio_shipper import LogzioShipper

log = logging.getLogger("main")

def run_once(ship: bool = True) -> None:
    events = []

    owm = OpenWeatherMapFetcher()
    wapi = WeatherApiFetcher()
    csv_fetcher = CsvFetcher(config.CSV_FILE)

    log.info("Polling %d cities from OWM + WeatherAPI, and CSV=%s", len(config.CITIES), config.CSV_FILE)

    for city in config.CITIES:
        try:
            raw = owm.fetch_city(city)
            evt = UnifiedLog.from_openweathermap(raw)
            events.append(evt)
            log.info("OWM normalized", extra={"city": evt["city"], "temperature_celsius": evt["temperature_celsius"], "description": evt["description"]})
        except Exception as e:
            log.exception("OWM fetch failed city=%s: %s", city, e)

    for city in config.CITIES:
        try:
            raw = wapi.fetch_city(city)
            evt = UnifiedLog.from_weatherapi(raw)
            events.append(evt)
            log.info("WAPI normalized", extra={"city": evt["city"], "temperature_celsius": evt["temperature_celsius"], "description": evt["description"]})
        except Exception as e:
            log.exception("WAPI fetch failed city=%s: %s", city, e)

    try:
        rows = csv_fetcher.fetch()
        for row in rows:
            events.append(UnifiedLog.from_csv(row))
        log.info("CSV normalized rows=%d", len(rows))
    except Exception as e:
        log.exception("CSV fetch failed: %s", e)

    if ship and events:
        shipper = LogzioShipper()
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