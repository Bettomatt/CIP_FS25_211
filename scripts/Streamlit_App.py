import json
import streamlit as st
import folium
from streamlit_folium import st_folium
import subprocess
import os
import re


# Define the directory containing the scripts
directory = os.path.dirname(os.path.abspath(__file__))

# List of specific files to execute (in order)
files_to_execute = [
    "API-Call-XML_Livedata.py",
    "API-Call-XML_Site_Data_2.py",
    "Merge_JSON's.py"
]

# Streamlit page config
st.set_page_config(layout="wide")

# Function to execute files one by one with error handling
def execute_files(files):
    for file_name in files:
        file_path = os.path.join(directory, file_name)

        if os.path.isfile(file_path):
            try:
                result = subprocess.run(["python", file_path], capture_output=True, text=True)

                if result.returncode == 0:
                    print(f"✅ {file_name} executed successfully")
                else:
                    print(f"❌ Error executing {file_name}: {result.stderr}")

            except Exception as e:
                print(f"⚠️ Exception while executing {file_name}: {e}")
        else:
            print(f"⚠️ File not found: {file_name}")


# Load JSON Data
def load_data():
    try:
        with open("merged_data.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        st.error("🚨 merged_data.json not found!")
        return {}

# Title
st.title("Live Traffic Data Visualization")

# Layout with columns
col1, col2 = st.columns([1, 3])

#show-data function: executes files and visualises the data on the map
def show_data():
    execute_files(files_to_execute)  # Execute the API files

    # Load the latest data after the API execution
    data = load_data()
    first_stations = dict(list(data.items()))  # Get first 50 stations
    #ZH_stations = [x for x in first_stations if re.match(r"^ZH.*", x)]
    # Create a map 46.79850620748795, 8.23179447609246
    m = folium.Map(location=[46.7985, 8.2317], zoom_start=8)

    # Add markers dynamically based on new data
    for station in first_stations:
        print(station)
        if station.startswith("ZH"):
            try:
                lat = first_stations[station].get("latitude")
                lon = first_stations[station].get("longitude")
                timestamp = first_stations[station].get("timestamp")
                #print(type(lat),type(lon))
                if type(lat) and type(lon) == str:
                    lat = float(lat)
                    lon = float(lon)
                else:
                    continue



                cars_h = first_stations[station]["measurements"][0]["VehiclesPerHour"]
                car_avg_speed = first_stations[station]["measurements"][1]["AverageSpeed"]

                popup_info = f"""
                <b>Timestamp:</b> {timestamp}<br>
                <b>Cars per Hour:</b> {cars_h}<br>
                <b>Average Speed:</b> {car_avg_speed} km/h
                """

                folium.Marker([lat, lon], popup=folium.Popup(popup_info, max_width=250), icon=folium.Icon(color="blue")).add_to(m)

            except (IndexError, KeyError):
                continue  # Skip stations with missing measurement data

    # Display the map in the second column
    with col2:
        st_folium(m, width=1000, height=600)

# Text and refresh-button on the webpage
with col1:
    st.header("About this App")
    st.write(
        "This app displays live traffic data on an interactive map. "
        "The data is updated when you refresh the page."
    )
    if st.button("Refresh Data (Manual)"):
        show_data()
        # pass
    st.write("Click the button to refresh data.")

#initial call of function show data
show_data()
