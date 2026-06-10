# BreatheWise

**AQI Forecasting & Personal Exposure Engine for Delhi NCR**

Most air quality apps tell you the AQI. None tell you what it means for 
*your* body, *your* activity, *right now*. BreatheWise does.

---

## What Makes This Different

Standard AQI apps: "PM2.5 is 36 µg/m³"

BreatheWise: "A 30-minute jog right now puts 3.8 µg of PM2.5 into your 
lungs — 35% of your entire WHO daily safe limit. Best window to run today 
is tomorrow 12:00 — PM2.5 drops to 26.46."

---

## ML Benchmark

Trained and evaluated two time-series models on 96 hours of real CPCB 
Delhi PM2.5 data:

| Model   | RMSE  | MAPE   | Notes                        |
|---------|-------|--------|------------------------------|
| Prophet | 12.63 | 24.69% | Baseline additive seasonality |
| LSTM    | 6.10  | 12.39% | 2-layer, 64 hidden units      |

LSTM outperforms Prophet by **51% on RMSE** and **50% on MAPE** on 
held-out test data.

---

## Architecture
OpenWeatherMap Air Pollution API   ←   live readings + 48hr forecast
OpenAQ v3 (CPCB stations)         ←   ground truth — RK Puram, Punjabi 
Bagh, IGI Airport
│
▼
Ingestion Pipeline (collector.py)
│
├──▶  Parser (parser.py)           extract pm25, pm10, o3, no2, co, 
temp
├──▶  Exposure Engine (exposure.py) activity × breathing rate × WHO 
threshold
├──▶  Forecast Parser (forecast.py) 48hr hourly PM2.5 windows
└──▶  LSTM Model (lstm_model.py)    PyTorch · 2-layer · seq_len=24
│
▼
FastAPI Backend (main.py)
│
▼
React Frontend Dashboard
---

## API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/live` | Live PM2.5, PM10, O3, NO2, CO for Delhi |
| GET | `/exposure?activity=jogging&duration=30` | Personal PM2.5 dose vs 
WHO limit |
| GET | `/forecast` | 48hr forecast + top 3 cleanest windows |
| GET | `/best-window?activity=jogging&duration=30` | Optimal activity 
window today |
| GET | `/activities` | Supported activity types with MET values |

---

## Personal Exposure Model

Exposure is calculated using activity-based breathing physiology:
breathing_rate = BASE_RATE × MET_value
air_inhaled (m³) = breathing_rate × duration
PM2.5_dose (µg) = PM2.5_concentration × air_inhaled
exposure_pct = dose / WHO_24hr_reference_dose × 100
MET values range from 0.8 (sleeping) to 10.0 (intense workout). WHO 24hr 
PM2.5 safe limit: 15 µg/m³.

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Data Sources | OpenWeatherMap API, OpenAQ v3 (CPCB) |
| ML | PyTorch (LSTM), Prophet, Scikit-learn |
| Backend | Python 3.11, FastAPI, Uvicorn |
| Frontend | React, Axios |
| Deployment | Docker, docker-compose |

---

## Local Setup

**Prerequisites:** Docker, or Python 3.11 + Node 18

**With Docker:**
```bash
git clone https://github.com/connectjigyasasrivastava/BreatheWise
cd BreatheWise
cp .env.example .env
# Add OPENWEATHER_API_KEY and OPENAQ_API_KEY to .env
docker-compose up
```

**Without Docker:**
```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend (separate terminal)
cd frontend
npm install
npm start
```

---

## Data Sources

| Source | Coverage | Update Frequency |
|--------|----------|-----------------|
| OpenWeatherMap | Delhi coordinates | Hourly |
| OpenAQ — RK Puram (CPCB) | South Delhi | 15 min |
| OpenAQ — Punjabi Bagh (CPCB) | West Delhi | 15 min |
| OpenAQ — IGI Airport (CPCB) | Southwest Delhi | 15 min |

---

## Project Status

- [x] Multi-source ingestion pipeline
- [x] PM2.5 personal exposure calculator
- [x] 48hr forecast with cleanest window detection
- [x] Prophet vs LSTM benchmark
- [x] FastAPI — 5 production endpoints
- [x] React dashboard
- [x] Docker deployment
- [ ] PostgreSQL time-series storage
- [ ] Historical trend analysis
- [ ] Multi-city support

---

## Why This Exists

Delhi's annual mean PM2.5 is 7–10x the WHO safe limit. 20 million 
residents make daily decisions — when to exercise, whether to send 
children to school, which route to commute — without any tool that 
translates raw pollution numbers into personal health impact.

BreatheWise is that translation layer.

---

Built by [Jigyasa 
Srivastava](https://www.linkedin.com/in/jigyasa-srivastava-9b6125377/)
