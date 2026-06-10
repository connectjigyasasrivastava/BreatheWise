import json
import pandas as pd
from prophet import Prophet
from datetime import datetime

def prepare_training_data(forecast_entries: list) -> pd.DataFrame:
    """
    Convert forecast entries to Prophet format (ds, y).
    """
    records = []
    for entry in forecast_entries:
        records.append({
            "ds": pd.to_datetime(entry["timestamp"]),
            "y": entry["pm25"]
        })
    df = pd.DataFrame(records)
    df = df.sort_values("ds").reset_index(drop=True)
    return df

def train_and_forecast(df: pd.DataFrame, hours_ahead: int = 24) -> pd.DataFrame:
    """
    Train Prophet model and forecast next N hours.
    """
    model = Prophet(
        changepoint_prior_scale=0.05,
        seasonality_mode="additive",
        daily_seasonality=True,
        weekly_seasonality=False,
        yearly_seasonality=False
    )
    model.fit(df)

    future = model.make_future_dataframe(periods=hours_ahead, freq="h")
    forecast = model.predict(future)

    return forecast[["ds", "yhat", "yhat_lower", 
"yhat_upper"]].tail(hours_ahead)

def evaluate(df: pd.DataFrame, forecast: pd.DataFrame) -> dict:
    """
    Basic MAPE evaluation on training data.
    """
    merged = df.merge(forecast, on="ds", how="inner")
    if merged.empty:
        return {"mape": None, "rmse": None}

    merged["error"] = abs(merged["y"] - merged["yhat"]) / merged["y"]
    mape = merged["error"].mean() * 100

    merged["sq_error"] = (merged["y"] - merged["yhat"]) ** 2
    rmse = merged["sq_error"].mean() ** 0.5

    return {
        "mape": round(mape, 2),
        "rmse": round(rmse, 2),
        "samples": len(merged)
    }

if __name__ == "__main__":
    with open("../data/raw_sample.json") as f:
        raw = json.load(f)

    from forecast import parse_forecast
    entries = parse_forecast(raw["openweather_forecast"])

    df = prepare_training_data(entries)
    print(f"Training on {len(df)} hourly data points")

    forecast = train_and_forecast(df, hours_ahead=24)
    print("\n=== 24hr Prophet Forecast (first 5) ===")
    print(forecast.head().to_string())

    metrics = evaluate(df, forecast)
    print(f"\n=== Model Metrics ===")
    print(f"MAPE: {metrics['mape']}%")
    print(f"RMSE: {metrics['rmse']}")
