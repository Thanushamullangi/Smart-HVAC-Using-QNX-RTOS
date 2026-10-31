import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
from streamlit_autorefresh import st_autorefresh

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Smart HVAC Control Center",
    page_icon="🌿",
    layout="wide"
)

# ---------------- PREMIUM DASHBOARD STYLING ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0B1523, #142438);
    color: #F1F5F9;
}
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1450px;
}
h1, h2, h3 {
    color: #F1F5F9 !important;
    font-family: 'Segoe UI', sans-serif;
    font-weight: 700;
}
p, label, .stMarkdown {
    color: #CBD5E1;
}
[data-testid="stMetric"] {
    background: linear-gradient(145deg, #1C3045, #17283A);
    border: 1px solid #29445D;
    padding: 20px;
    border-radius: 16px;
    box-shadow: 0 5px 18px rgba(0,0,0,0.18);
}
[data-testid="stMetricValue"] {
    color: #42D4F5 !important;
    font-size: 30px;
    font-weight: 700;
}
[data-testid="stMetricLabel"] {
    color: #A8BDD0 !important;
}
div[data-testid="stAlert"] {
    border-radius: 12px;
}
div[data-testid="stPlotlyChart"] {
    background: #17283A;
    border: 1px solid #29445D;
    border-radius: 16px;
    padding: 12px;
}
hr {
    border-color: #29445D;
}
section[data-testid="stSidebar"] {
    background: #101D2D;
    border-right: 1px solid #29445D;
}
.stAlert {
    border-radius: 12px;
}
footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)

# The returned counter advances on each automatic rerun.
refresh_count = st_autorefresh(interval=2000, key="hvac_refresh")

# ---------------- LOAD DATASET ----------------
DATA_PATH = (
    Path(__file__).resolve().parent.parent
    / "Datasets"
    / "Occupancy_Estimation.csv"
)

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    df.columns = df.columns.str.strip()

    numeric_columns = [
        "S1_Temp", "S2_Temp", "S3_Temp", "S4_Temp",
        "S1_Light", "S2_Light", "S3_Light", "S4_Light",
        "S1_Sound", "S2_Sound", "S3_Sound", "S4_Sound",
        "S5_CO2", "S5_CO2_Slope", "S6_PIR", "S7_PIR",
        "Room_Occupancy_Count"
    ]

    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    required = [
        "S1_Temp", "S2_Temp", "S3_Temp", "S4_Temp",
        "S5_CO2", "Room_Occupancy_Count"
    ]
    return df.dropna(subset=required).reset_index(drop=True)

try:
    df = load_data()
except Exception as e:
    st.error(f"Could not load sensor dataset at {DATA_PATH}: {e}")
    st.stop()

if df.empty:
    st.error("No valid sensor readings found in the dataset.")
    st.stop()

# ---------------- AUTOMATIC RECORDED-DATA PLAYBACK ----------------
row_index = refresh_count % len(df)
row = df.iloc[row_index]

temperature_columns = ["S1_Temp", "S2_Temp", "S3_Temp", "S4_Temp"]
room_temperature = row[temperature_columns].mean()
co2 = row["S5_CO2"]
occupancy = int(row["Room_Occupancy_Count"])
pir1 = row["S6_PIR"]
pir2 = row["S7_PIR"]

# ---------------- HVAC DECISION ENGINE ----------------
# These are prototype recommendations, not physical AC commands.
if co2 > 1000:
    mode = "HIGH VENTILATION"
    decision = "Increase fresh-air ventilation."
    fan_speed = "HIGH"
elif occupancy == 0:
    mode = "ENERGY SAVING"
    decision = "Room is unoccupied. Reduce HVAC operation."
    fan_speed = "LOW"
elif room_temperature > 30:
    mode = "HIGH COOLING"
    decision = "High room temperature. Increase cooling."
    fan_speed = "HIGH"
elif room_temperature > 26:
    mode = "MODERATE COOLING"
    decision = "Room temperature is elevated. Increase cooling moderately."
    fan_speed = "MEDIUM"
else:
    mode = "NORMAL OPERATION"
    decision = "Room conditions are comfortable."
    fan_speed = "LOW"

if occupancy == 0:
    target_temperature = 28
elif room_temperature > 30:
    target_temperature = 22
elif room_temperature > 26:
    target_temperature = 24
else:
    target_temperature = 26

# ---------------- DASHBOARD ----------------
st.title("🌿 SMART HVAC CONTROL CENTER")
st.caption("Intelligent Room Monitoring | Automatic HVAC Decisions")
st.success("SYSTEM ONLINE — AUTOMATED RECORDED-DATA PLAYBACK")
st.info(
    f"Dataset record {row_index + 1} of {len(df)} "
    "| Refresh interval: 2 seconds"
)

st.subheader("📡 Automatic Sensor Monitoring")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Room Temperature", f"{room_temperature:.1f} °C")
c2.metric("CO₂ Concentration", f"{co2:.0f} ppm")
c3.metric("Occupancy", f"{occupancy} people")
c4.metric("Target AC Temperature", f"{target_temperature} °C")

st.subheader("🌡️ Room Temperature Sensors")
temp_cols = st.columns(4)
for i, col in enumerate(temperature_columns):
    temp_cols[i].metric(f"Sensor {i + 1}", f"{row[col]:.1f} °C")

st.subheader("👥 Occupancy Detection")
p1, p2, p3 = st.columns(3)
p1.metric("People Detected", occupancy)
p2.metric("PIR Sensor 1", str(pir1))
p3.metric("PIR Sensor 2", str(pir2))

st.divider()
st.subheader("🧠 Intelligent HVAC Decision")
if mode in ["HIGH VENTILATION", "HIGH COOLING"]:
    st.warning(f"⚠️ {mode}: {decision}")
elif mode == "ENERGY SAVING":
    st.success(f"🌱 {mode}: {decision}")
else:
    st.success(f"✅ {mode}: {decision}")

a, b, c = st.columns(3)
a.metric("HVAC Mode", mode)
b.metric("Recommended Fan Speed", fan_speed)
c.metric("Recommended AC Setpoint", f"{target_temperature} °C")

st.subheader("❄️ AC Performance Monitoring")
ac1, ac2, ac3 = st.columns(3)
ac1.metric("AC Inlet Temperature", "Not available")
ac2.metric("AC Outlet Temperature", "Not available")
ac3.metric("Humidity", "Not available")
st.caption("These measurements require additional physical sensors.")

# ---------------- HISTORY AND GRAPHS ----------------
if "history" not in st.session_state:
    st.session_state.history = []

timestamp = f"{row.get('Date', '')} {row.get('Time', '')}"
history_entry = {
    "Record": row_index + 1,
    "Temperature": room_temperature,
    "CO2": co2,
    "Occupancy": occupancy,
    "Timestamp": timestamp
}

if (
    not st.session_state.history
    or st.session_state.history[-1]["Record"] != row_index + 1
):
    st.session_state.history.append(history_entry)

st.session_state.history = st.session_state.history[-100:]
history_df = pd.DataFrame(st.session_state.history)

st.divider()
st.subheader("📊 Automatic Sensor Trends")

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=history_df["Record"],
    y=history_df["Temperature"],
    name="Room Temperature",
    mode="lines+markers"
))
fig.update_layout(
    title="Room Temperature Trend",
    xaxis_title="Dataset Record",
    yaxis_title="Temperature (°C)",
    height=350
)
st.plotly_chart(fig, use_container_width=True)

fig2 = go.Figure()
fig2.add_trace(go.Scatter(
    x=history_df["Record"],
    y=history_df["CO2"],
    name="CO2",
    mode="lines+markers"
))
fig2.update_layout(
    title="CO2 Concentration Trend",
    xaxis_title="Dataset Record",
    yaxis_title="CO2 (ppm)",
    height=350
)
st.plotly_chart(fig2, use_container_width=True)

st.caption(
    "Smart HVAC | QNX State-Level Hackathon | "
    "Recorded dataset-driven software demonstration"
)
