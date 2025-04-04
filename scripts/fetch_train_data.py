import requests
import os
import json
from datetime import datetime

# API endpoint
base_url = "https://data.sbb.ch/api/explore/v2.1/catalog/datasets/ist-daten-sbb/records"

limit = 100
offset = 0
all_records = []

# First request to see what the API returns
params = {"limit": limit, "offset": offset}
response = requests.get(base_url, params=params)
print("Initial response status:", response.status_code)
print("Initial response JSON:", response.json())

# Check if the API returns data
if response.status_code == 200:
    while True:
        params = {"limit": limit, "offset": offset}
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            # Try both keys if needed:
            records = data.get("records") or data.get("results", [])
            print(f"Offset {offset}: {len(records)} records returned.")

            if not records:
                break  # no more records
            all_records.extend(records)
            offset += limit
        else:
            print(f"❌ Failed at offset {offset}: {response.status_code}")
            break
else:
    print(f"❌ Initial fetch failed: {response.status_code}")

print(f"Total records fetched: {len(all_records)}")

# Save if records were fetched
if all_records:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"sbb_all_data_{timestamp}.json"
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_folder = os.path.join(project_root, "data")
    os.makedirs(data_folder, exist_ok=True)
    file_path = os.path.join(data_folder, filename)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump({"records": all_records}, f, ensure_ascii=False, indent=2)

    print(f"✅ All data saved to {file_path}")
else:
    print("❌ No data fetched.")
