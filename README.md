# BreatheWise

> Real-time air quality intelligence that tells you not just how bad the 
air is — but what to do about it.

## The Problem
AQI data exists everywhere. No tool answers the actual human question:
"Should I go for a run at 6am or 7pm? Which route to office has lowest 
pollution exposure today?"

BreatheWise solves that.

## What It Does
- Personal Exposure Calculator:  given your activity, duration, and 
route, calculates your estimated PM2.5 exposure vs WHO safe limits
- Activity Recommender: finds the safest window for outdoor activity 
in the next 48 hours
- Route Comparator: compares two commute routes by pollution 
exposure, not just time
- Weekly Health Report: tracks your cumulative pollution exposure 
over time

## Architecture
OpenWeatherMap API (live AQI + 48hr forecast) + OpenAQ API (historical 
ground station data)
->
Python Ingestion Pipeline
->
Exposure Calculation Engine (PM2.5 → µg/m³ personal dose)
->
FastAPI Backend → React Frontend


## Tech Stack
- Backend: Python, FastAPI, PostgreSQL
- Data Sources: OpenWeatherMap Air Pollution API, OpenAQ v3
- Frontend: React, Mapbox
- Deployment: Docker

## Live Demo
[Link coming soon — Delhi NCR, India dataset]

## Setup
```bash
git clone https://github.com/connectjigyasasrivastava/BreatheWise
cd BreatheWise
cp .env.example .env
# Add your OpenWeatherMap API key
pip install -r requirements.txt
uvicorn backend.main:app --reload
```

## Current Status
- [x] Repository setup
- [x] Data source verification (OpenWeatherMap + OpenAQ)
- [ ] Ingestion pipeline
- [ ] Exposure calculation engine
- [ ] Activity recommender
- [ ] Route comparator
- [ ] Frontend dashboard
- [ ] Deployment

## Why This Matters
Delhi NCR ranks among India's top 5 most polluted cities.
600M+ Indians have access to AQI data but zero tools to act on it.
Breathewise bridges that gap.

---
Built by Jigyasa Srivastava | 
https://www.linkedin.com/in/jigyasa-srivastava-9b6125377/ | [Portfolio] 
coming soon
