import requests
import os

OPENAQ_KEY = os.getenv("OPENAQ_API_KEY")
OPENWEATHER_KEY = os.getenv("OPENWEATHER_API_KEY")

DELHI_STATIONS = [17, 50, 15]
DELHI_LAT = 28.61
DELHI_LON = 77.20

def fetch_openaq_latest(location_id: int):
    url = f"https://api.openaq.org/v3/locations/{location_id}/latest"
    headers = {"X-API-Key": OPENAQ_KEY}
    response = requests.get(url, headers=headers)
    return response.json()

def fetch_openweather_aqi():
    url = f"https://api.openweathermap.org/data/2.5/air_pollution?lat={DELHI_LAT}&lon={DELHI_LON}&appid={OPENWEATHER_KEY}"
    response = requests.get(url)
    return response.json()

if __name__ == "__main__":
    print("=== OpenWeatherMap Live AQI ===")
    owm = fetch_openweather_aqi()
    print(owm)

    print("\n=== OpenAQ RK Puram Station ===")
    oaq = fetch_openaq_latest(17)
    print(oaq)
