# Import the modules we need
import requests
import json
import os
from datetime import datetime

# This is the link where we ask for train data from SBB (Swiss Railways)
api_url = "https://data.sbb.ch/api/explore/v2.1/catalog/datasets/ist-daten-sbb/records"

# How many data entries we want to get per request
records_per_request = 100
offset = 0  # Start at the beginning of the data
all_records = []  # A list to store everything we get

# Let's try to get the first batch of data
first_response = requests.get(api_url, params={"limit": records_per_request, "offset": offset})

# Print the status (200 means OK), and show some sample data
print("First response status code:", first_response.status_code)
print("Sample data from the API:", first_response.json())

# If the first request was successful, continue getting more data
if first_response.status_code == 200:

    while True:
        # Set the parameters for each request (how many + where to start)
        params = {
            "limit": records_per_request,
            "offset": offset
        }

        # Send the request
        response = requests.get(api_url, params=params)

        # Check if it worked
        if response.status_code == 200:
            # Get the actual data
            data = response.json()

            # Try to get the records (sometimes it's under different keys)
            records = data.get("records") or data.get("results", [])

            print(f"Got {len(records)} records at offset {offset}")

            # If no more records are returned, stop the loop
            if not records:
                print("No more records to fetch.")
                break

            # Add these records to our full list
            all_records.extend(records)

            # Move the offset forward to get the next batch next time
            offset += records_per_request

        else:
            # If we get an error (like 400), we stop and print a message
            print(f"❌ Stopped at offset {offset}. Error code: {response.status_code}")
            break

else:
    print("❌ Could not connect to the API on the first try.")

# Show how many records we got in total
print("✅ Total records collected:", len(all_records))

# If we actually got data, let's save it
if all_records:
    # Make a filename with today's date and time
    now = datetime.now()
    filename = f"sbb_data_{now.strftime('%Y%m%d_%H%M%S')}.json"

    # Make a 'data' folder in the same place as your script
    data_folder = os.path.join(os.getcwd(), "data")
    os.makedirs(data_folder, exist_ok=True)  # Make sure the folder exists

    # Full path to where we'll save the file
    file_path = os.path.join(data_folder, filename)

    # Write the data into a JSON file
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump({"records": all_records}, f, ensure_ascii=False, indent=2)

    print(f"✅ Data saved to: {file_path}")
else:
    print("❌ No data was fetched, so nothing was saved.")
