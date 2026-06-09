import json
from datetime import datetime

SENSOR_MAP = {
    12234787: "pm25",
    12234786: "pm10",
    12234785: "o3",
    12234784: "no2",
    12234782: "co",
    12234788: "humidity",
    12234790: "temperature",
    14340715: "wind_speed",
    14340714: "wind_direction"
}

def parse_openweather(raw: dict) -> dict:
    item = raw["list"][0]
    return {
        "source": "openweathermap",
        "timestamp": datetime.utcfromtimestamp(item["dt"]).isoformat(),
        "aqi": item["main"]["aqi"],
        "pm25": item["components"]["pm2_5"],
        "pm10": item["components"]["pm10"],
        "o3": item["components"]["o3"],
        "no2": item["components"]["no2"],
        "co": item["components"]["co"],
        "so2": item["components"]["so2"],
    }

def parse_openaq_station(raw: dict, station_name: str) -> dict:
    result = {"source": "openaq", "station": station_name}
    for reading in raw.get("results", []):
        sensor_id = reading["sensorsId"]
        if sensor_id in SENSOR_MAP:
            field = SENSOR_MAP[sensor_id]
            result[field] = reading["value"]
            result["timestamp"] = reading["datetime"]["local"]
    return result

def parse_all(filepath: str):
    with open(filepath) as f:
        raw = json.load(f)

    parsed = {
        "collected_at": raw["collected_at"],
        "openweather": parse_openweather(raw["openweather_live"]),
        "stations": {}
    }

    for station_name, station_raw in raw["openaq_stations"].items():
        parsed["stations"][station_name] = parse_openaq_station(
            station_raw, station_name
        )

    return parsed

if __name__ == "__main__":
    result = parse_all("../data/raw_sample.json")
    print(json.dumps(result, indent=2))
