# WHO PM2.5 safe limits (µg/m³)
WHO_LIMITS = {
    "pm25_annual": 5.0,
    "pm25_24hr": 15.0,
    "pm10_24hr": 45.0,
    "o3_8hr": 100.0
}

# MET (Metabolic Equivalent) — breathing rate multiplier per activity
ACTIVITY_MET = {
    "sleeping": 0.8,
    "sitting": 1.0,
    "walking_slow": 2.5,
    "walking_fast": 4.0,
    "jogging": 7.0,
    "cycling": 8.0,
    "intense_workout": 10.0
}

# Breathing volume per MET per hour (litres)
BASE_BREATHING_RATE = 0.5  # litres/min at rest

def calculate_exposure(
    pm25: float,
    activity: str,
    duration_minutes: int
) -> dict:
    """
    Calculate personal PM2.5 exposure in µg based on
    activity type, duration, and current PM2.5 concentration.
    """
    met = ACTIVITY_MET.get(activity, 1.0)
    breathing_rate_lpm = BASE_BREATHING_RATE * met
    total_air_inhaled_litres = breathing_rate_lpm * duration_minutes
    total_air_inhaled_m3 = total_air_inhaled_litres / 1000

    exposure_ug = pm25 * total_air_inhaled_m3

    who_24hr_dose = WHO_LIMITS["pm25_24hr"] * (
        BASE_BREATHING_RATE * 1440 / 1000
    )
    exposure_pct_of_daily_limit = (exposure_ug / who_24hr_dose) * 100

    safe = exposure_pct_of_daily_limit < 25

    if pm25 <= 15:
        advice = "Air is clean. Safe for all activities."
    elif pm25 <= 35:
        advice = "Moderate pollution. Avoid intense outdoor workouts."
    elif pm25 <= 55:
        advice = "Unhealthy for sensitive groups. Limit outdoor exposure."
    elif pm25 <= 75:
        advice = "Unhealthy. Wear N95 mask outdoors."
    else:
        advice = "Hazardous. Stay indoors. Avoid all outdoor activity."

    return {
        "activity": activity,
        "duration_minutes": duration_minutes,
        "pm25_concentration": pm25,
        "air_inhaled_m3": round(total_air_inhaled_m3, 4),
        "pm25_exposure_ug": round(exposure_ug, 3),
        "pct_of_who_daily_limit": round(exposure_pct_of_daily_limit, 1),
        "is_safe": safe,
        "advice": advice
    }

def best_activity_window(forecast_list: list, activity: str, 
duration_minutes: int) -> dict:
    """
    Given a list of hourly forecast dicts with pm25 values,
    return the hour with lowest exposure.
    """
    best = None
    for entry in forecast_list:
        pm25 = entry.get("pm25")
        if pm25 is None:
            continue
        result = calculate_exposure(pm25, activity, duration_minutes)
        result["timestamp"] = entry.get("timestamp")
        if best is None or result["pm25_exposure_ug"] < best["pm25_exposure_ug"]:
            best = result
    return best

if __name__ == "__main__":
    # Test with RK Puram live reading
    test = calculate_exposure(
        pm25=31.0,
        activity="jogging",
        duration_minutes=30
    )
    import json
    print(json.dumps(test, indent=2))
