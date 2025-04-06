import os
import json
from datetime import datetime

# Get the project directory
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Paths to folders
train_folder = os.path.join(project_dir, 'data', 'filtered-data')
weather_folder = os.path.join(project_dir, 'data', 'weather_data')
output_folder = os.path.join(project_dir, 'data', 'clean-dataset')

# Create clean-dataset folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Go through all train delay files
for train_file in os.listdir(train_folder):
    if not train_file.endswith('.json'):
        continue

    # Get the date from the train file name
    date_part = train_file.split('_')[0]  # Example: 2025-02-15
    print(f"Processing date: {date_part}")

    # Build file paths
    train_path = os.path.join(train_folder, train_file)
    weather_path = os.path.join(weather_folder, f"weather_data_{date_part}.json")

    # Check if matching weather file exists
    if not os.path.exists(weather_path):
        print(f"No weather data found for {date_part}, skipping...")
        continue

    # Load train data
    with open(train_path, "r", encoding="utf-8") as f:
        train_data = [json.loads(line) for line in f]

    # Load weather data
    with open(weather_path, "r", encoding="utf-8") as f:
        weather_data = json.load(f)

    # Prepare weather data into a simple lookup
    weather_lookup = {}
    for location, info in weather_data.items():
        if "hourly" in info and "time" in info["hourly"]:
            times = [datetime.fromisoformat(t) for t in info["hourly"]["time"]]
            for idx, t in enumerate(times):
                weather_lookup[(location, t.hour)] = {
                    "temperature_2m": info["hourly"].get("temperature_2m", [None])[idx],
                    "precipitation": info["hourly"].get("precipitation", [None])[idx],
                    "snowfall": info["hourly"].get("snowfall", [None])[idx],
                    "wind_speed_10m": info["hourly"].get("wind_speed_10m", [None])[idx],
                    "cloudcover": info["hourly"].get("cloudcover", [None])[idx],
                    "weathercode": info["hourly"].get("weathercode", [None])[idx],
                }

    # List to collect clean merged data
    clean_records = []

    # Go through all train records
    for record in train_data:
        try:
            # Skip records if arrival time or prognosis is missing
            if not record.get("ANKUNFTSZEIT") or not record.get("AN_PROGNOSE"):
                continue

            # Parse arrival times
            planned_arrival = datetime.strptime(record["ANKUNFTSZEIT"], "%d.%m.%Y %H:%M")
            real_arrival = datetime.strptime(record["AN_PROGNOSE"], "%d.%m.%Y %H:%M:%S")

            # Calculate delay in minutes
            delay_min = (real_arrival - planned_arrival).total_seconds() / 60

            # Find station and hour
            station = record["HALTESTELLEN_NAME"]
            hour = planned_arrival.hour

            # Get weather for that station and hour
            weather = weather_lookup.get((station, hour), None)

            if weather is None:
                continue  # If no weather found, skip

            # Build clean merged record
            clean_record = {
                "date": date_part,
                "station": station,
                "planned_arrival": planned_arrival.strftime("%Y-%m-%d %H:%M"),
                "real_arrival": real_arrival.strftime("%Y-%m-%d %H:%M"),
                "arrival_delay_min": delay_min,
                "cancelled": record.get("FAELLT_AUS_TF", False),
                "temperature_2m": weather["temperature_2m"],
                "precipitation": weather["precipitation"],
                "snowfall": weather["snowfall"],
                "wind_speed_10m": weather["wind_speed_10m"],
                "cloudcover": weather["cloudcover"],
                "weathercode": weather["weathercode"]
            }

            clean_records.append(clean_record)

        except Exception as e:
            print(f"Error in record: {e}")

    # Save clean data as JSON (one record per line)
    if clean_records:
        output_file = os.path.join(output_folder, f"clean_{date_part}.json")
        with open(output_file, "w", encoding="utf-8") as f:
            for record in clean_records:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
        print(f"Saved cleaned data to {output_file}")
    else:
        print(f"No valid records for {date_part}")
