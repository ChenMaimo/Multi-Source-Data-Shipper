import os

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
POLL_INTERVAL_SEC = int(os.getenv("POLL_INTERVAL_SEC", "60"))
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "5"))

CSV_FILE = os.getenv("CSV_FILE", "weather_data.csv")

CITIES = [c.strip() for c in os.getenv("CITIES", "Tel Aviv,Jerusalem").split(",")]