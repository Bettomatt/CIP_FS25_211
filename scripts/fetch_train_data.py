import requests
import os
import json
from datetime import datetime

# API endpoint
url = "https://data.sbb.ch/api/explore/v2.1/catalog/datasets/ist-daten-sbb/records?limit=100"

# Fetch data
response = requests.get(url)

if response.status_code == 200:
    data = response.json()

    # Format current timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"sbb_data_{timestamp}.json"

    # Get relative path to /data
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_folder = os.path.join(project_root, "data")

    os.makedirs(data_folder, exist_ok=True)
    file_path = os.path.join(data_folder, filename)

    # Save JSON data
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✅ Data saved to {file_path}")
else:
    print(f"❌ Failed to fetch data: {response.status_code}")