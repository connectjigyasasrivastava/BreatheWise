import json
import pandas as pd
import numpy as np
import torch
from prophet import Prophet
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error

from forecast import parse_forecast
from lstm_model import LSTMModel, create_sequences, train, evaluate as lstm_evaluate

def run_prophet(entries: list):
    records = [{"ds": pd.to_datetime(e["timestamp"]), "y": e["pm25"]} for e in entries]
    df = pd.DataFrame(records).sort_values("ds").reset_index(drop=True)

    split = int(len(df) * 0.8)
    train_df = df[:split]
    test_df = df[split:]

    model = Prophet(
        changepoint_prior_scale=0.05,
        seasonality_mode="additive",
        daily_seasonality=True,
        weekly_seasonality=False,
        yearly_seasonality=False
    )
    model.fit(train_df)

    future = model.make_future_dataframe(periods=len(test_df), freq="h")
    forecast = model.predict(future)

    predicted = forecast["yhat"].tail(len(test_df)).values
    actual = test_df["y"].values

    rmse = mean_squared_error(actual, predicted) ** 0.5
    mape = mean_absolute_percentage_error(actual, predicted) * 100

    return {"model": "Prophet", "rmse": round(rmse, 2), "mape": round(mape, 2)}

def run_lstm(entries: list):
    pm25 = np.array([e["pm25"] for e in entries]).reshape(-1, 1)
    scaler = MinMaxScaler()
    scaled = scaler.fit_transform(pm25)

    seq_len = 24
    X, y = create_sequences(scaled, seq_len)

    split = int(len(X) * 0.8)
    X_train = torch.FloatTensor(X[:split])
    y_train = torch.FloatTensor(y[:split])
    X_test = torch.FloatTensor(X[split:])
    y_test = torch.FloatTensor(y[split:])

    model = LSTMModel(input_size=1, hidden_size=64, num_layers=2)
    model = train(model, X_train, y_train, epochs=100)
    metrics = lstm_evaluate(model, X_test, y_test, scaler)
    metrics["model"] = "LSTM"
    return metrics

if __name__ == "__main__":
    with open("../data/raw_sample.json") as f:
        raw = json.load(f)

    entries = parse_forecast(raw["openweather_forecast"])
    print(f"Benchmarking on {len(entries)} hourly Delhi PM2.5 data points\n")

    prophet_results = run_prophet(entries)
    print(f"Prophet done — RMSE: {prophet_results['rmse']}, MAPE: {prophet_results['mape']}%")

    lstm_results = run_lstm(entries)
    print(f"LSTM done — RMSE: {lstm_results['rmse']}, MAPE: {lstm_results['mape']}%")

    print("\n=== Benchmark Results ===")
    results = [prophet_results, lstm_results]
    for r in results:
        print(f"{r['model']:10} | RMSE: {r['rmse']:6.2f} | MAPE: {r['mape']:6.2f}%")

    winner = min(results, key=lambda x: x["rmse"])
    print(f"\nWinner: {winner['model']} with RMSE {winner['rmse']}")
