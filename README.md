# CIP_FS25_211: Weather-and-Public-Transport
This project analyzes the impact of weather conditions on the efficiency of public transportation between different cities in Switzerland, with a particular focus on delays in train services.

## Student Contributions

All team members contributed to all stages of the project (data collection, transformation and analysis).
However, specific areas of focus were:

**Tobias Schöpfer:** Focused on data cleansing, creating weather-related categories and performing exploratory data analysis using various visualizations (boxplots, heatmaps).

**Mattia Bettoja:** Primarily responsible for data collection, including accessing APIs (SBB, Open-Meteo) and downloading historical datasets for trains and weather. Also contributed to structuring and preparing the data for merging and analysis.

**Luca Signorini:** Developed an alternative real-time data acquisition branch and performed Linear/ multiple regressions to analyze the impact of weather on train delays


## Scripts folder:
This folder contains all scripts for fetching, processing, merging and visualizing data

### **fetch_train_data.py**
This script fetches train data from the SBB API, but due to the API's daily data limit and historical data availability, it only fetches one day's worth of data at a time. The API has not been updated for a month. The fetched data is saved in the `data` folder as a JSON file.

### **historic_train_data.py**
This script fetches historical train data in CSV format from the OpenTransportData Swiss website and saves it to the data/historic-data folder.

### **historic_data_filter_json_convert.py**
_Run historic_train_data.py first to download the CSV files._ 
This script processes large CSV files of historic train data, filters them by the 30 most popular stops and saves the filtered data as JSON files in the `data/filtered-data` folder. **CSV files are too large to be stored on GitHub, so only the filtered data is stored.**

### **fetch_weather.py**
Fetches hourly historical weather data for 30 Swiss cities from the Open-Meteo API.
Saves one JSON file per day in data/weather_data/.

### **merge_train_weather.py**
_Requires running historic_data_filter_json_convert.py and fetch_weather.py first._
Merges filtered train delay data with corresponding weather data by station and hour.
Saves the cleaned, merged datasets as JSON files in data/clean-dataset/.

### **linear-regression.py**
_Requires running preprocessing first._
Runs simple linear regressions between weather factors and train delays, based on preprocessed data.

### **multiple_regression.py**
_Requires running preprocessing first._
Performs multiple linear regression to predict train delays based on weather factors.

### **preprocessing.py**
_Requires running merge_train_weather.py first to generate the merged input data._
Cleans and prepares the merged train and weather data for analysis by removing outliers, handling missing values and creating new time- and weather-based features.

### **visualization_explore.py**
_Requires running preprocessing first._
Creates visualizations (scatterplots, boxplots, heatmaps) to explore relationships between weather conditions and train delays

### **visualizations_part1.py**
_Requires running preprocessing first._
Generates various exploratory plots (boxplots, heatmaps, scatterplots) to analyze the relationship between weather conditions and train delays

### **visualizations_part2.py**
_Requires running preprocessing first._
Generates plots to answer key research questions

### **visualizations_part3.ipynb**
_Requires running preprocessing first._
Creates additional visualizations to further explore the relationship between weather conditions and train delays.


## Data Folder
Contains all datasets used in the project, including raw, processed and final data

### **historic-data**
Raw historical train data (CSV files) downloaded from opentransportdata.swiss. Due to their large size, these files are stored only locally and are not included in the GitHub repository.

### **filtered-data**
Filtered train data (JSON format) focusing on the 30 most popular stations

### **weather_data**
Historical weather data (JSON files) collected from the Open-Meteo API.

### **clean-dataset**
Merged train and weather datasets, cleaned and ready for analysis (JSON files).

### **final_data**
Final processed datasets used for regression and visualization (CSV files).
