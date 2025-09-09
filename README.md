# Multi-Source Data Shipper

A small integration service that fetches weather data from external APIs (like OpenWeatherMap, WeatherAPI), normalizes the schema, and ships structured logs to Logz.io via HTTP.

---

## 📌 Features
- Fetches data from multiple weather APIs
- Normalizes different schemas into a unified event format
- Sends structured logs to Logz.io
- Configurable with `.env` file
- Includes unit tests with **pytest**

---

## 🛠️ Installation

Clone the repository:

git clone https://github.com/ChenMaimo/Multi-Source-Data-Shipper


## 🛠️ Local Setup

python -m venv venv
source venv/bin/activate   # On macOS/Linux
venv\Scripts\activate      # On Windows


## ⚙️ Configuration
-LOGZIO_TOKEN=your-logzio-token
-OPENWEATHER_API_KEY=your-openweather-key
-WEATHERAPI_KEY=your-weatherapi-key
-LOGIZ_LISENTER_HOST =https://listener-eu.logz.io:8071
-WEATHER_API_URL= http://api.weatherapi.com/v1
-OPEN_WEATHER_API_URL=https://api.openweathermap.org/data/2.5/weather
-CITIES=Tel Aviv,Jerusalem
-POLL_INTERVAL_SEC=60
-CSV_FILE= path to file
-LOG_LEVEL=INFO


## Run locally
python -m src.main

## Run Tests 
use the following command :
pytest -q