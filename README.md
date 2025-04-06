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
* **Filters** CSV files from `data/historic-data` for the top 30 most popular stops.
* **Saves** the filtered data as JSON files to `data/filtered-data`.
* **Skips** files that are already processed.

### **How to run**:
Run the script, and it will process and filter the CSV files from `data/historic-data` and store the filtered JSON data in the `data/filtered-data` folder.
