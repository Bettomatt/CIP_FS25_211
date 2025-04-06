import requests
import json
import os
from datetime import datetime

# Set the API URL for fetching data
api_url = "https://data.sbb.ch/api/explore/v2.1/catalog/datasets/ist-daten-sbb/records"

# Set how many records to get at once (max 100 records per request)
records_per_request = 100
offset = 0  # Start from the beginning
all_records = []  # To store all the data

# Try to connect and get the first response from the API
first_response = requests.get(api_url, params={"limit": records_per_request, "offset": offset})
print("First response status code:", first_response.status_code)
print("Sample data:", first_response.json())

# Check if the first response is good
if first_response.status_code == 200:
    # Keep fetching records until we get no more data
    while True:
        # Set the parameters for the request (limit and offset)
        params = {
            "limit": records_per_request,
            "offset": offset
        }

        # Get data from the API
        response = requests.get(api_url, params=params)

        # If the request is successful, process the data
        if response.status_code == 200:
            data = response.json()
            records = data.get("records") or data.get("results", [])
            print(f"Got {len(records)} records at offset {offset}")

            # If no records are returned, stop fetching
            if not records:
                print("No more records.")
                break

            # Add the new records to the list
            all_records.extend(records)

            # Move to the next set of records
            offset += records_per_request
        else:
            print(f"Error at offset {offset}. Error code: {response.status_code}")
            break
else:
    print("Could not connect to the API.")

# If we have records, save them to a file
if all_records:
    # Create a filename with the current date and time
    now = datetime.now()
    filename = f"sbb_data_{now.strftime('%Y%m%d_%H%M%S')}.json"

    # Get the project folder and create the 'data' folder if it doesn't exist
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_folder = os.path.join(project_root, "data")
    os.makedirs(data_folder, exist_ok=True)

    # Save the records to a JSON file
    file_path = os.path.join(data_folder, filename)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump({"records": all_records}, f, ensure_ascii=False, indent=2)

    print(f"Data saved to: {file_path}")
else:
    print("No data to save.")

