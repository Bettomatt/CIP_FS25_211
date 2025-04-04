import requests
import csv
import json
import os

# Function to fetch train data from the SBB API
def fetch_train_data():
    # API URL (replace with the actual URL from SBB API)
    url = "https://api.sbb.ch/v1/connection"  # Example URL, replace with the actual API endpoint

    # Define parameters for the API request (you might need to adjust these based on the API documentation)
    params = {
        "from": "Zurich",  # Starting location
        "to": "Bern",      # Destination location
        "dateTime": "2025-04-05T08:00:00"  # Date and time (adjust as needed)
    }

    # Send the GET request
    response = requests.get(url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        print("Data fetched successfully")
        return response.json()  # Return the JSON data
    else:
        print(f"Error fetching data: {response.status_code}")
        return None

# Function to store data in a CSV file
def store_data_in_csv(data, filename="train_data.csv"):
    if not data:
        print("No data to store.")
        return

    # Check if 'connections' key exists in the data (adjust based on the actual API response structure)
    if 'connections' not in data:
        print("No connections data found.")
        return

    # Open a CSV file for writing
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        # Write headers (adjust keys based on your data structure)
        writer.writerow(["Departure", "Arrival", "Duration", "Train", "Platform"])

        # Write each connection's details
        for connection in data["connections"]:
            departure = connection.get("from", {}).get("departure", "N/A")
            arrival = connection.get("to", {}).get("arrival", "N/A")
            duration = connection.get("duration", "N/A")
            train = connection.get("train", {}).get("name", "N/A")
            platform = connection.get("from", {}).get("platform", "N/A")

            writer.writerow([departure, arrival, duration, train, platform])

    print(f"Data stored successfully in {filename}")

# Main function to execute the script
if __name__ == "__main__":
    # Fetch the train data
    train_data = fetch_train_data()

    # Store the fetched data in a CSV file
    store_data_in_csv(train_data)
