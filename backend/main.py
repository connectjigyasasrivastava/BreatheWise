import os
import json
import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from exposure import calculate_exposure, best_activity_window, ACTIVITY_MET
from forecast import parse_forecast, best_windows

app = FastAPI(title="BreatheWise API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

OPENWEATHER_KEY = os.getenv("OPENWEATHER_API_KEY")
DELHI_LAT = 28.61
DELHI_LON = 77.20

def get_live_aqi():
    url = f"https://api.openweathermap.org/data/2.5/air_pollution?lat={DELHI_LAT}&lon={DELHI_LON}&appid={OPENWEATHER_KEY}"
    return requests.get(url).json()

def get_forecast():
    url = f"https://api.openweathermap.org/data/2.5/air_pollution/forecast?lat={DELHI_LAT}&lon={DELHI_LON}&appid={OPENWEATHER_KEY}"
    return requests.get(url).json()

@app.get("/")
def root():
    return {"message": "BreatheWise API running"}

@app.get("/live")
def live_aqi():
    raw = get_live_aqi()
    item = raw["list"][0]
    return {
        "aqi": item["main"]["aqi"],
        "pm25": item["components"]["pm2_5"],
        "pm10": item["components"]["pm10"],
        "o3": item["components"]["o3"],
        "no2": item["components"]["no2"],
        "co": item["components"]["co"],
    }

@app.get("/exposure")
def exposure(activity: str = "jogging", duration: int = 30):
    raw = get_live_aqi()
    pm25 = raw["list"][0]["components"]["pm2_5"]
    return calculate_exposure(pm25, activity, duration)

@app.get("/best-window")
def best_window(activity: str = "jogging", duration: int = 30):
    raw = get_forecast()
    entries = parse_forecast(raw)
    return best_activity_window(entries, activity, duration)

@app.get("/forecast")
def forecast_48hr():
    raw = get_forecast()
    entries = parse_forecast(raw)
    top3 = best_windows(entries, top_n=3)
    return {"total_hours": len(entries), "cleanest_windows": top3}

@app.get("/activities")
def activities():
    return {"available_activities": list(ACTIVITY_MET.keys())}
