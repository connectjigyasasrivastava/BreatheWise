import requests
import os
import json
from datetime import datetime

OPENAQ_KEY = os.getenv("OPENAQ_API_KEY")
OPENWEATHER_KEY = os.getenv("OPENWEATHER_API_KEY")

DELHI_STATIONS = {
    "rk_puram": 17,
    "punjabi_bagh": 50,
    "igi_airport": 15
}

DELHI_LAT = 28.61
DELHI_LON = 77.20

def fetch_openaq_latest(location_id: int):
    url = f"https://api.openaq.org/v3/locations/{location_id}/latest"
    headers = {"X-API-Key": OPENAQ_KEY}
    r = requests.get(url, headers=headers)
    return r.json()

def fetch_openweather_aqi():
    url = f"https://api.openweathermap.org/data/2.5/air_pollution?lat={DELHI_LAT}&lon={DELHI_LON}&appid={OPENWEATHER_KEY}"
    r = requests.get(url)
    return r.json()

def fetch_openweather_forecast():
    url = f"https://api.openweathermap.org/data/2.5/air_pollution/forecast?lat={DELHI_LAT}&lon={DELHI_LON}&appid={OPENWEATHER_KEY}"
    r = requests.get(url)
    return r.json()

def collect_all():
    timestamp = datetime.utcnow().isoformat()
    data = {
        "collected_at": timestamp,
        "openweather_live": fetch_openweather_aqi(),
        "openweather_forecast": fetch_openweather_forecast(),
        "openaq_stations": {}
    }
    for name, station_id in DELHI_STATIONS.items():
        data["openaq_stations"][name] = fetch_openaq_latest(station_id)
    return data

if __name__ == "__main__":
    result = collect_all()
    with open("../data/raw_sample.json", "w") as f:
        json.dump(result, f, indent=2)
    print(f"Data collected at {result['collected_at']}")
    print(f"Saved to data/raw_sample.json")
