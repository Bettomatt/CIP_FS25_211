import time
import subprocess
import os
from datetime import datetime, timedelta

# Define the directory containing the scripts
directory = "/Users/lucasignorini/Documents/MSc_ids/Sem_2/CIP/00_Project/Git/Weather-and-Public-Transport/scripts"

# List of specific files to execute (in order)
files_to_execute = [
    "API-Call-XML_Livedata.py",
    "API-Call-XML_Site_Data_2.py",
    "Merge_JSON's.py"
]


# Function to execute files one by one
def execute_files(files):
    for file_name in files:
        file_path = os.path.join(directory, file_name)

        # Check if the file exists
        if os.path.isfile(file_path):
            print(f"Executing: {file_name}")
            subprocess.run(["python", file_path])  # Use "python3" if necessary
        else:
            print(f"File not found: {file_name}")


# Main loop that runs every `cycle_delay` seconds, synchronized with real-world time
while True:
    # Get the current time and the next time point (5 seconds after the start of the next minute)
    current_time = datetime.now()
    next_minute = current_time.replace(second=0, microsecond=0) + timedelta(minutes=1)

    # Calculate the time to wait until 5 seconds after the next full minute
    next_time_point = next_minute + timedelta(seconds=5)
    wait_time = (next_time_point - current_time).total_seconds()
    print(f"Waiting for {wait_time:.2f} seconds until 5 seconds after the next minute...")

    # Wait until 5 seconds after the next full minute
    time.sleep(wait_time)

    # Execute the files in the cycle
    print("Starting a new cycle of executions...")
    execute_files(files_to_execute)
