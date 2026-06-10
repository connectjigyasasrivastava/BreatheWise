import json
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error

# ── Model Definition ──────────────────────────────────────────────────────────
class LSTMModel(nn.Module):
    def __init__(self, input_size=1, hidden_size=64, num_layers=2, output_size=1):
        super(LSTMModel, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size)
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size)
        out, _ = self.lstm(x, (h0, c0))
        return self.fc(out[:, -1, :])

# ── Data Preparation ──────────────────────────────────────────────────────────
def create_sequences(data: np.ndarray, seq_len: int):
    X, y = [], []
    for i in range(len(data) - seq_len):
        X.append(data[i:i+seq_len])
        y.append(data[i+seq_len])
    return np.array(X), np.array(y)

def prepare_data(entries: list, seq_len: int = 24):
    pm25_values = np.array([e["pm25"] for e in entries]).reshape(-1, 1)

    scaler = MinMaxScaler()
    scaled = scaler.fit_transform(pm25_values)

    X, y = create_sequences(scaled, seq_len)

    split = int(len(X) * 0.8)
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]

    X_train = torch.FloatTensor(X_train)
    X_test = torch.FloatTensor(X_test)
    y_train = torch.FloatTensor(y_train)
    y_test = torch.FloatTensor(y_test)

    return X_train, X_test, y_train, y_test, scaler

# ── Training ──────────────────────────────────────────────────────────────────
def train(model, X_train, y_train, epochs=100, lr=0.001):
    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)

    for epoch in range(epochs):
        model.train()
        output = model(X_train)
        loss = criterion(output, y_train)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if (epoch + 1) % 20 == 0:
            print(f"Epoch {epoch+1}/{epochs} — Loss: {loss.item():.6f}")

    return model

# ── Evaluatio────────────────────────────────────────────────────────────────
def evaluate(model, X_test, y_test, scaler):
    model.eval()
    with torch.no_grad():
        predictions = model(X_test).numpy()

    predictions = scaler.inverse_transform(predictions)
    actuals = scaler.inverse_transform(y_test.numpy())

    rmse = mean_squared_error(actuals, predictions) ** 0.5
    mape = mean_absolute_percentage_error(actuals, predictions) * 100

    return {
        "rmse": round(rmse, 2),
        "mape": round(mape, 2),
        "samples": len(actuals)
    }

# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    with open("../data/raw_sample.json") as f:
        raw = json.load(f)

    from forecast import parse_forecast
    entries = parse_forecast(raw["openweather_forecast"])

    print(f"Total data points: {len(entries)}")

    X_train, X_test, y_train, y_test, scaler = prepare_data(entries, seq_len=24)
    print(f"Train: {len(X_train)} sequences | Test: {len(X_test)} sequences")

    model = LSTMModel(input_size=1, hidden_size=64, num_layers=2)
    print("\nTraining LSTM...")
    model = train(model, X_train, y_train, epochs=100)

    metrics = evaluate(model, X_test, y_test, scaler)
    print(f"\n=== LSTM Metrics ===")
    print(f"RMSE: {metrics['rmse']}")
    print(f"MAPE: {metrics['mape']}%")
    print(f"Test samples: {metrics['samples']}")
