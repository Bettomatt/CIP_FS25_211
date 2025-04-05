import requests
import os
import json
from datetime import datetime

# Resource ID from opentransportdata.swiss (istdaten)
resource_id = "7282348a-ae58-4d59-af77-c6bfae1c7669"

# Base URL for the CKAN DataStore search API
base_url = "https://data.opentransportdata.swiss/api/action/datastore_search"

limit = 1000  # Number of records per request (adjust as allowed by the API)
offset = 0
all_records = []

# If an API key is required, add it here:
# API_KEY = "YOUR_API_KEY"
# headers = {"Authorization": API_KEY}
# If not required, use an empty dictionary:
headers = {}

print("Starting to fetch all data...")

while True:
    params = {
        "resource_id": resource_id,
        "limit": limit,
        "offset": offset
    }

    response = requests.get(base_url, params=params, headers=headers)
    if response.status_code != 200:
        print(f"❌ Error at offset {offset}: {response.status_code}")
        print(response.text)
        break

    # The API response should have a "result" object with a "records" list
    result = response.json().get("result", {})
    records = result.get("records", [])
    if not records:
        # No more records available
        break

    all_records.extend(records)
    print(f"✅ Fetched {len(records)} records at offset {offset}")
    offset += limit

print(f"Total records fetched: {len(all_records)}")

# Create a timestamped filename for saving the data as JSON
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"istdaten_all_{timestamp}.json"

# Determine the relative path to the /data folder in your project.
# This assumes your project root is one level above this script.
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_folder = os.path.join(project_root, "data")
os.makedirs(data_folder, exist_ok=True)
file_path = os.path.join(data_folder, filename)

# Save all fetched data to a JSON file
with open(file_path, "w", encoding="utf-8") as f:
    json.dump(all_records, f, ensure_ascii=False, indent=2)

print(f"✅ Data saved to {file_path}")
