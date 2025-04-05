import requests
import json
import os
from datetime import datetime

# API endpoint URL for the SBB Ist-Daten dataset
api_url = "https://data.sbb.ch/api/explore/v2.1/catalog/datasets/ist-daten-sbb/records"

# Set how many records you want per request (the API limit is 100)
records_per_request = 100
offset = 0  # Start at the beginning
all_records = []  # This list will store all fetched records

# First, try to connect and see what the API returns (for debugging)
first_response = requests.get(api_url, params={"limit": records_per_request, "offset": offset})
print("First response status code:", first_response.status_code)
print("Sample data from the API:", first_response.json())

# Check if we could connect successfully
if first_response.status_code == 200:
    # Loop to get all records in batches of 100
    while True:
        # Set the request parameters (limit and offset)
        params = {
            "limit": records_per_request,
            "offset": offset
        }
        # Send the GET request
        response = requests.get(api_url, params=params)

        # If the request is successful, process the data
        if response.status_code == 200:
            data = response.json()
            # Sometimes the data may be under "records" or "results"
            records = data.get("records") or data.get("results", [])
            print(f"Got {len(records)} records at offset {offset}")

            # If no records are returned, we stop fetching more data
            if not records:
                print("No more records to fetch.")
                break

            # Add these records to our list
            all_records.extend(records)
            # Increase the offset to get the next batch
            offset += records_per_request
        else:
            print(f"Stopped at offset {offset}. Error code: {response.status_code}")
            break
else:
    print("Could not connect to the API on the first try.")

print("Total records collected:", len(all_records))

# Save the data if we got any records
if all_records:
    # Create a filename with the current date and time
    now = datetime.now()
    filename = f"sbb_data_{now.strftime('%Y%m%d_%H%M%S')}.json"

    # Get the project root and then the 'data' folder (assumes your project structure is set up)
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_folder = os.path.join(project_root, "data")
    os.makedirs(data_folder, exist_ok=True)
    file_path = os.path.join(data_folder, filename)

    # Save the complete data to the JSON file
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump({"records": all_records}, f, ensure_ascii=False, indent=2)

    print(f"Data saved to: {file_path}")
else:
    print("No data was fetched, so nothing was saved.")
