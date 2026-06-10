import json
from datetime import datetime

def parse_forecast(raw: dict) -> list:
    """
    Extract hourly PM2.5 and AQI from OpenWeatherMap
    48hr forecast response.
    """
    entries = []
    for item in raw["list"]:
        entries.append({
            "timestamp": 
datetime.utcfromtimestamp(item["dt"]).isoformat(),
            "aqi": item["main"]["aqi"],
            "pm25": item["components"]["pm2_5"],
            "pm10": item["components"]["pm10"],
            "o3": item["components"]["o3"],
            "no2": item["components"]["no2"],
            "co": item["components"]["co"],
        })
    return entries

def best_windows(forecast_entries: list, top_n: int = 3) -> list:
    """
    Return top N hours with lowest PM2.5 in the forecast.
    """
    sorted_entries = sorted(forecast_entries, key=lambda x: x["pm25"])
    return sorted_entries[:top_n]

if __name__ == "__main__":
    with open("../data/raw_sample.json") as f:
        raw = json.load(f)

    forecast = parse_forecast(raw["openweather_forecast"])

    print(f"Total forecast hours: {len(forecast)}")
    print("\n=== Full 48hr Forecast (first 5 hours) ===")
    print(json.dumps(forecast[:5], indent=2))

    print("\n=== Top 3 Cleanest Air Windows ===")
    best = best_windows(forecast)
    print(json.dumps(best, indent=2))
