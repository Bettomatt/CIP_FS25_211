import requests  # To send requests to the weather API
import os  # To handle file operations
import json  # To save data in JSON format
from datetime import datetime, timedelta  # To work with dates

# List of locations for which we want weather data
locations = [
    "Zürich HB", "Bern", "Basel SBB", "Genève", "Lausanne", "Luzern", "Winterthur",
    "St. Gallen", "Lugano", "Biel/Bienne", "Thun", "Schaffhausen", "Chur",
    "Olten", "Neuchâtel", "Fribourg", "Sion", "Aarau", "Uster", "Yverdon-les-Bains",
    "Wil SG", "Kreuzlingen", "Zug", "Wädenswil", "Solothurn", "Baden", "Lenzburg",
    "Brugg AG", "Bellinzona", "Montreux"
]

# URL of the weather API
api_url = "https://archive-api.open-meteo.com/v1/archive"

# Get the absolute path for the project and create the folder to save weather data
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
weather_data_folder = os.path.join(project_dir, 'data', 'weather_data')
os.makedirs(weather_data_folder, exist_ok=True)

# Parameters for the weather API
params = {
    "hourly": "temperature_2m,precipitation,snowfall,wind_speed_10m,cloudcover,weathercode",  # What data we need
    "temperature_unit": "celsius",  # Temperature in Celsius
    "windspeed_unit": "kmh",  # Wind speed in km/h
    "precipitation_unit": "mm",  # Precipitation in mm
    "snowfall_unit": "cm",  # Snowfall in cm
    "timezone": "Europe/Zurich"  # Timezone for Switzerland
}

# Function to fetch weather data for a location on a specific date
def fetch_weather(location, date):
    print(f"Fetching weather data for {location} on {date}...")

    # Coordinates for each location (latitude, longitude)
    location_coords = {
        "Zürich HB": (47.378177, 8.540192),
        "Bern": (46.94809, 7.44744),
        "Basel SBB": (47.547354, 7.591716),
        "Genève": (46.2044, 6.1432),
        "Lausanne": (46.5197, 6.6323),
        "Luzern": (47.0502, 8.3093),
        "Winterthur": (47.498, 8.724),
        "St. Gallen": (47.4245, 9.3747),
        "Lugano": (46.005, 8.951),
        "Biel/Bienne": (47.1365, 7.2468),
        "Thun": (46.759, 7.629),
        "Schaffhausen": (47.697, 8.635),
        "Chur": (46.8504, 9.532),
        "Olten": (47.351, 7.904),
        "Neuchâtel": (46.989, 6.931),
        "Fribourg": (46.8024, 7.1515),
        "Sion": (46.2333, 7.3667),
        "Aarau": (47.3913, 8.0455),
        "Uster": (47.3505, 8.7199),
        "Yverdon-les-Bains": (46.7807, 6.6415),
        "Wil SG": (47.4693, 9.0423),
        "Kreuzlingen": (47.6502, 9.1824),
        "Zug": (47.166, 8.515),
        "Wädenswil": (47.231, 8.654),
        "Solothurn": (47.2077, 7.5323),
        "Baden": (47.472, 8.306),
        "Lenzburg": (47.3896, 8.178),
        "Brugg AG": (47.4767, 8.2033),
        "Bellinzona": (46.1911, 9.0294),
        "Montreux": (46.4333, 6.9167)
    }

    # Check if the location has coordinates
    if location not in location_coords:
        print(f"Coordinates for {location} are not available.")
        return None

    # Get latitude and longitude for the location
    lat, lon = location_coords[location]

    # Update parameters with the location's coordinates and date
    params.update({"latitude": lat, "longitude": lon, "start_date": date, "end_date": date})

    # Make the request to the weather API
    response = requests.get(api_url, params=params)

    # If the request is successful, return the data
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Failed to fetch data for {location} on {date}: {response.status_code}")
        return None

# Function to save weather data for the last 2 months
def save_weather_data():
    end_date = datetime.today()  # Today's date
    start_date = end_date - timedelta(days=60)  # Two months ago

    # Loop through each day from 2 months ago to today
    current_date = start_date
    while current_date <= end_date:
        date_str = current_date.strftime('%Y-%m-%d')  # Format the date as YYYY-MM-DD

        # Check if a file for this day already exists
        file_path = os.path.join(weather_data_folder, f"weather_data_{date_str}.json")

        if os.path.exists(file_path):  # If the file exists, skip this day
            print(f"Weather data for {date_str} already exists, skipping...")
        else:
            all_weather_data = {}
            # Fetch weather data for each location
            for location in locations:
                weather_data = fetch_weather(location, date_str)

                # If data is fetched, save it to the dictionary
                if weather_data:
                    all_weather_data[location] = weather_data

            # Save the weather data to a file if we got data
            if all_weather_data:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(all_weather_data, f, ensure_ascii=False, indent=2)
                print(f"Weather data for {date_str} saved to {file_path}")
            else:
                print(f"No weather data found for {date_str}")

        # Move to the next day
        current_date += timedelta(days=1)

# Run the function to save the weather data
save_weather_data()
