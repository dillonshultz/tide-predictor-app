import streamlit as st
import requests
from datetime import datetime

st.set_page_config(
    page_title="Oregon Tide & Crabbing Predictor",
    page_icon="🦀",
    layout="wide"
)
st.markdown("""
    <style>
    .stApp {
        background-color: #0e4c92;
    }
    </style>
""", unsafe_allow_html=True)


st.subheader("Today's Tides")

st.sidebar.header("⚙️ Settings")

location = st.sidebar.selectbox(
    "Choose Location",
    ["Astoria", "Buoy 10"]
)

if location == "Astoria":
    station_id = "9439040"
else:
    station_id = "9439201"



selected_date = st.sidebar.date_input("Select Date")

st.title(~ Tides For Selected Location ~)

st.title("🦀 Oregon Tide & Crabbing Predictor")
st.caption("Live NOAA data to help you find the best crabbing conditions")
st.divider()

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
    st.success("Good crabbing near these high tides and wind:")
    for time in best_times:
        st.write("•", time)
else:
    st.warning("No good tides or winds found today.")


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

import requests

import matplotlib.pyplot as plt
import pandas as pd

tide_times = [t["t"] for t in data["predictions"]]
tide_heights = [float(t["v"]) for t in data["predictions"]]

df = pd.DataFrame({
    "Time": tide_times,
    "Height": tide_heights
})

df["Time"] = pd.to_datetime(df["Time"])

fig, ax = plt.subplots()
ax.plot(df["Time"], df["Height"])
ax.set_xlabel("Time")
ax.set_ylabel("Tide Height (ft)")
ax.set_title("Tide Heights for Today")

st.divider()
st.subheader("🌊 Tide Height Chart")

with st.container():
    st.pyplot(fig)



from datetime import datetime, timedelta


begin_date = selected_date.strftime("%Y%m%d")
end_date = (selected_date + timedelta(days=1)).strftime("%Y%m%d")
