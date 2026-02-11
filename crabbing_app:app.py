import streamlit as st
import requests
from datetime import datetime

st.title("🦀 Tide Predictor")

location = st.selectbox(
    "Choose a location:",
    ["Astoria", "Buoy 10 Area"]
)

if location == "Astoria":
    station_id = "9439040"
else:
    station_id = "9439201"

st.subheader("Today's Tides")

# Get today's date in the format NOAA requires (YYYYMMDD)
today = datetime.now().strftime("%Y%m%d")

url = f"https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?product=predictions&application=web_services&begin_date={today}&end_date={today}&datum=MLLW&station={station_id}&time_zone=lst_ldt&units=english&interval=hilo&format=json"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()

    if "predictions" in data:
        for tide in data["predictions"]:
            if tide["type"] == "H":
                tide_type = "High"
            else:
                tide_type = "Low"

            st.write(tide["t"], "-", tide_type, "tide")
    else:
        st.error("NOAA did not return tide predictions.")
        st.write(data)
else:
    st.error("Could not connect to NOAA tide data.")
    st.write("Status code:", response.status_code)

begin_date=20260210

st.subheader("🦀 Best Crabbing Times")

best_times = []

for tide in data["predictions"]:
    if tide["type"] == "H":
        best_times.append(tide["t"])

if best_times:
    st.success("Good crabbing near these high tides:")
    for time in best_times:
        st.write("•", time)
else:
    st.warning("No strong tides found today.")

import requests

if location == "Astoria":
    lat = 46.1879
    lon = -123.8313
else:
    lat = 46.2490
    lon = -123.7680

weather_api_key = "d6dd14da21a89d5e15c1d1a701534ed0"

weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={weather_api_key}&units=imperial"

weather_response = requests.get(weather_url)
weather_data = weather_response.json()

weather_response = requests.get(weather_url)
weather_data = weather_response.json()

if weather_response.status_code == 200 and "wind" in weather_data:
    wind_speed = weather_data["wind"]["speed"]
    st.subheader("🌬 Current Wind Speed")
    st.write(f"{wind_speed} mph")
else:
    wind_speed = None
    st.info("Wind data not available yet (API key may still be activating).")

st.subheader("🦀 Best Crabbing Times")

best_times = []

for tide in data["predictions"]:
    if tide["type"] == "H":
        if wind_speed is not None and wind_speed < 12:
            best_times.append(tide["t"])

if best_times:
    st.success("Good crabbing near these high tides with calm wind:")
    for time in best_times:
        st.write("•", time)
else:
    st.warning("Wind may be too strong or no good tides today.")
