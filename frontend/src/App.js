import { useState, useEffect } from "react";
import axios from "axios";

const API = "http://127.0.0.1:8000";

const AQI_CONFIG = {
  1: { label: "Good", bg: "#e8f5e9", accent: "#2e7d32" },
  2: { label: "Fair", bg: "#f9fbe7", accent: "#558b2f" },
  3: { label: "Moderate", bg: "#fff8e1", accent: "#f57f17" },
  4: { label: "Poor", bg: "#fbe9e7", accent: "#bf360c" },
  5: { label: "Very Poor", bg: "#f3e5f5", accent: "#6a1b9a" },
};

const S = {
  app: { fontFamily: "'Inter', 'Segoe UI', sans-serif", background: "#f4f6fb", minHeight: "100vh", color: "#1a1a2e", padding: "36px 24px" },
  container: { maxWidth: 920, margin: "0 auto" },
  header: { marginBottom: 32, borderBottom: "1px solid #e0e4ef", paddingBottom: 20 },
  title: { fontSize: 26, fontWeight: 800, color: "#1a237e", margin: 0, letterSpacing: "-0.5px" },
  subtitle: { color: "#7986cb", marginTop: 6, fontSize: 13, fontWeight: 500 },
  aqiBanner: { borderRadius: 14, padding: "20px 28px", marginBottom: 24, display: "flex", justifyContent: "space-between", alignItems: "center", border: "1px solid #e0e4ef" },
  aqiLabel: { fontSize: 11, fontWeight: 700, textTransform: "uppercase", letterSpacing: 1.5, marginBottom: 6, opacity: 0.6 },
  aqiValue: { fontSize: 30, fontWeight: 800 },
  aqiRight: { fontSize: 13, fontWeight: 500, textAlign: "right", opacity: 0.75 },
  grid: { display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(140px, 1fr))", gap: 12, marginBottom: 24 },
  card: { background: "#ffffff", borderRadius: 12, padding: "16px 20px", border: "1px solid #e0e4ef", boxShadow: "0 1px 4px rgba(0,0,0,0.04)" },
  cardLabel: { fontSize: 10, color: "#7986cb", textTransform: "uppercase", letterSpacing: 1.2, marginBottom: 8, fontWeight: 600 },
  cardValue: { fontSize: 20, fontWeight: 700, color: "#1a237e" },
  section: { background: "#ffffff", borderRadius: 14, padding: 28, marginBottom: 20, border: "1px solid #e0e4ef", boxShadow: "0 1px 4px rgba(0,0,0,0.04)" },
  sectionTitle: { fontSize: 15, fontWeight: 700, color: "#1a237e", marginBottom: 20, marginTop: 0, letterSpacing: "-0.3px" },
  row: { display: "flex", gap: 12, alignItems: "center", marginBottom: 16, flexWrap: "wrap" },
  select: { padding: "10px 14px", borderRadius: 8, background: "#f4f6fb", border: "1px solid #c5cae9", color: "#1a1a2e", fontSize: 14, fontWeight: 500, outline: "none" },
  input: { padding: "10px 14px", borderRadius: 8, background: "#f4f6fb", border: "1px solid #c5cae9", color: "#1a1a2e", fontSize: 14, width: 70, fontWeight: 500 },
  btn: { padding: "10px 28px", background: "#1a237e", color: "white", border: "none", borderRadius: 8, cursor: "pointer", fontSize: 14, fontWeight: 700, letterSpacing: "0.3px" },
  resultSafe: { background: "#f1f8e9", border: "1px solid #aed581", borderRadius: 10, padding: 20 },
  resultUnsafe: { background: "#fff3e0", border: "1px solid #ffb74d", borderRadius: 10, padding: 20 },
  resultRow: { display: "flex", justifyContent: "space-between", padding: "10px 0", borderBottom: "1px solid #eeeeee", fontSize: 14 },
  resultLabel: { color: "#7986cb", fontWeight: 500 },
  resultValue: { fontWeight: 700, color: "#1a237e" },
  advice: { marginTop: 14, fontSize: 13, color: "#455a64", lineHeight: 1.6 },
  windowCard: { background: "#f8f9ff", borderRadius: 10, padding: "14px 20px", marginBottom: 10, display: "flex", justifyContent: "space-between", alignItems: "center", border: "1px solid #e8eaf6" },
  windowRank: { fontSize: 11, color: "#7986cb", fontWeight: 700, textTransform: "uppercase", letterSpacing: 1, marginBottom: 4 },
  windowTime: { fontWeight: 600, fontSize: 14, color: "#1a237e" },
  windowPM: { fontWeight: 800, color: "#2e7d32", fontSize: 18 },
  windowPMLabel: { fontSize: 11, color: "#7986cb", textAlign: "right" },
};

export default function App() {
  const [live, setLive] = useState(null);
  const [exposure, setExposure] = useState(null);
  const [forecast, setForecast] = useState(null);
  const [activity, setActivity] = useState("jogging");
  const [duration, setDuration] = useState(30);

  useEffect(() => {
    axios.get(`${API}/live`).then(r => setLive(r.data));
    axios.get(`${API}/forecast`).then(r => setForecast(r.data));
  }, []);

  const checkExposure = () => {
    axios.get(`${API}/exposure?activity=${activity}&duration=${duration}`).then(r => setExposure(r.data));
  };

  const aqi = live ? AQI_CONFIG[live.aqi] : null;

  return (
    <div style={S.app}>
      <div style={S.container}>
        <div style={S.header}>
          <h1 style={S.title}>🌬️ BreatheWise</h1>
          <p style={S.subtitle}>Real-time air quality intelligence · Delhi NCR</p>
        </div>

        {live && aqi && (
          <>
            <div style={{ ...S.aqiBanner, background: aqi.bg }}>
              <div>
                <div style={{ ...S.aqiLabel, color: aqi.accent }}>Current AQI — Delhi</div>
                <div style={{ ...S.aqiValue, color: aqi.accent }}>{live.aqi} — {aqi.label}</div>
              </div>
              <div style={{ ...S.aqiRight, color: aqi.accent }}>
                PM2.5: {live.pm25} µg/m³<br />
                {live.pm25 > 15 ? "⚠️ Above WHO safe limit" : "✅ Within WHO safe limit"}
              </div>
            </div>

            <div style={S.grid}>
              {[
                { label: "PM2.5", value: `${live.pm25} µg/m³` },
                { label: "PM10", value: `${live.pm10} µg/m³` },
                { label: "O₃ Ozone", value: `${live.o3} µg/m³` },
                { label: "NO₂", value: `${live.no2} µg/m³` },
                { label: "CO", value: `${live.co} µg/m³` },
              ].map(s => (
                <div key={s.label} style={S.card}>
                  <div style={S.cardLabel}>{s.label}</div>
                  <div style={S.cardValue}>{s.value}</div>
                </div>
              ))}
            </div>
          </>
        )}

        <div style={S.section}>
          <p style={S.sectionTitle}>Personal Exposure Calculator</p>
          <div style={S.row}>
            <select value={activity} onChange={e => setActivity(e.target.value)} style={S.select}>
              {["sleeping","sitting","walking_slow","walking_fast","jogging","cycling","intense_workout"].map(a => (
                <option key={a} value={a}>{a.replace(/_/g, " ")}</option>
              ))}
            </select>
            <input type="number" value={duration} onChange={e => setDuration(e.target.value)} style={S.input} />
            <span style={{ color: "#7986cb", fontSize: 13, fontWeight: 500 }}>minutes</span>
            <button onClick={checkExposure} style={S.btn}>Calculate</button>
          </div>

          {exposure && (
            <div style={exposure.is_safe ? S.resultSafe : S.resultUnsafe}>
              {[
                ["Activity", exposure.activity.replace(/_/g, " ")],
                ["PM2.5 Inhaled", `${exposure.pm25_exposure_ug} µg`],
                ["% of WHO Daily Limit", `${exposure.pct_of_who_daily_limit}%`],
                ["Status", exposure.is_safe ? "✅ Safe" : "❌ Unsafe"],
              ].map(([k, v]) => (
                <div key={k} style={S.resultRow}>
                  <span style={S.resultLabel}>{k}</span>
                  <span style={S.resultValue}>{v}</span>
                </div>
              ))}
              <div style={S.advice}>{exposure.advice}</div>
            </div>
          )}
        </div>

        {forecast && (
          <div style={S.section}>
            <p style={S.sectionTitle}>Cleanest Air Windows · Next 48hrs</p>
            {forecast.cleanest_windows.map((w, i) => (
              <div key={i} style={S.windowCard}>
                <div>
                  <div style={S.windowRank}>#{i + 1} Best Window</div>
                  <div style={S.windowTime}>{w.timestamp.replace("T", "  ")}</div>
                </div>
                <div>
                  <div style={S.windowPMLabel}>PM2.5</div>
                  <div style={S.windowPM}>{w.pm25} µg/m³</div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}