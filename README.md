# Weather-and-Public-Transport
Weather and Public Transport

Script folder:

### **Fetch and Save SBB Train Data**

**Description**:  
This script fetches real-time train data from the SBB API, but due to the API's daily data limit and historical data availability, it only fetches one day's worth of data at a time. The API has not been updated for a month, so the **historical data was fetched via `historic_train_data.py`**. The fetched data is saved in the `data` folder as a JSON file.

### **What it does**:
* **Fetches** real-time train data from the SBB API (limited to one day's worth of data per request).
* **Saves** the fetched data as a JSON file in the `data` folder.
* **Historical data** is fetched via the `historic_train_data.py` script due to API limitations and lack of recent updates.


### **How to run**:
Run the script to fetch real-time data from the SBB API and save it in the `data` folder. Since the API only allows fetching one day of data at a time, historical data is fetched separately through `historic_train_data.py`.


### **historic train data.py**

This script fetches historical train data in CSV format from the OpenTransportData Swiss website and saves it to the data/historic-data folder.

#### What it does:

* Scrapes CSV file links from https://data.opentransportdata.swiss/dataset/istdaten.
* 
* Downloads the CSV files to the data/historic-data folder.
* 
* Skips files that already exist.

### **Filter historic train data.py**

This script processes large CSV files of historic train data, filters them by the 30 most popular stops, and saves the filtered data as JSON files in the `data/filtered-data` folder. **CSV files are too large to be stored on GitHub, so only the filtered data is stored.**

### **What it does**:
* Filters CSV files from `data/historic-data` for the top 30 most popular stops.
* *aves the filtered data as JSON files to `data/filtered-data`.
* Skips files that are already processed.

### **How to run**:
Run the script, and it will process and filter the CSV files from `data/historic-data` and store the filtered JSON data in the `data/filtered-data` folder.

### fetch_weather.py
Fetches **hourly historical weather data** for 30 Swiss cities from the **Open-Meteo API**.

### **What it does**:
* Loops through the **last 60 days**.
* For each day and station, collects **temperature**, **precipitation**, **snowfall**, **wind speed**, **cloud cover**, and **weather code**.
* Saves one JSON file **per day** in `data/weather_data/`.
* Skips already existing files to avoid duplicates.

### **How to run**:
Run the script with `python scripts/fetch_weather.py` from the project root to fetch and save historical weather data into `data/weather_data/`.

### **merge_train_weather.py**

This script **merges filtered train delay data** with **weather data** for each day, based on station and hour, and saves the merged clean dataset in the `data/clean-dataset/` folder.

### **What it does**:
* Loops through each day’s filtered train data from `data/filtered-data/`.
* Loads matching weather data from `data/weather_data/`.
* Matches records by **station name** and **hour**.
* Calculates **arrival delays in minutes**.
* Saves the merged data as a **JSON file (one record per line)** in `data/clean-dataset/`.
* Skips train records if arrival times are missing or weather data is not available.

### **How to run**:
Run the script with: