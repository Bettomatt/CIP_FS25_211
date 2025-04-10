import matplotlib.pyplot as plt
import pandas as pd
import os

# First, execute the data processing step in the script "preprocessing".
# Use dataframe < data_no_nan >

# Define the directory where the CSV files are stored
path = "data/final_data"
# Construct the full file paths
data_no_nan2_path = os.path.join(path, "data_no_nan2.csv")
data_no_nan_path = os.path.join(path, "data_no_nan.csv")

# Load the CSV files into DataFrames
data_no_nan2 = pd.read_csv(data_no_nan2_path)
data_no_nan = pd.read_csv(data_no_nan_path)

# Research Questions:
# %%% 1.  How Do Different Weather Conditions Influence Train Delays?

# %%% 1. Scatterplot

# Create subplots for temperature, precipitation, and wind speed vs. arrival delay.
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# Temperature vs. Arrival Delay
axes[0].scatter(data_no_nan['temperature_2m'], data_no_nan['arrival_delay_min'], alpha=0.5)
axes[0].set_title("Temperature vs. Train Delays")
axes[0].set_xlabel("Temperature (°C)")
axes[0].set_ylabel("Arrival Delay (min)")

# Precipitation vs. Arrival Delay
axes[1].scatter(data_no_nan['precipitation'], data_no_nan['arrival_delay_min'], alpha=0.5)
axes[1].set_title("Precipitation vs. Train Delays")
axes[1].set_xlabel("Precipitation (mm)")
axes[1].set_ylabel("")

# Wind Speed vs. Arrival Delay
axes[2].scatter(data_no_nan['wind_speed_10m'], data_no_nan['arrival_delay_min'], alpha=0.5)
axes[2].set_title("Wind Speed vs. Train Delays")
axes[2].set_xlabel("Wind Speed (m/s)")
axes[2].set_ylabel("")

plt.tight_layout()
plt.show()

# %%% 1. Heat Map
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# Temperature vs. Arrival Delay heat map
h_temp = axes[0].hist2d(data_no_nan['temperature_2m'],
                          data_no_nan['arrival_delay_min'],
                          bins=50, cmap='viridis')
axes[0].set_title("Temperature vs. Train Delays")
axes[0].set_xlabel("Temperature (°C)")
axes[0].set_ylabel("Arrival Delay (min)")
plt.colorbar(h_temp[3], ax=axes[0])

# Precipitation vs. Arrival Delay heat map
h_precip = axes[1].hist2d(data_no_nan['precipitation'],
                            data_no_nan['arrival_delay_min'],
                            bins=50, cmap='viridis')
axes[1].set_title("Precipitation vs. Train Delays")
axes[1].set_xlabel("Precipitation (mm)")
axes[1].set_ylabel("Arrival Delay (min)")
plt.colorbar(h_precip[3], ax=axes[1])

# Wind Speed vs. Arrival Delay heat map
h_wind = axes[2].hist2d(data_no_nan['wind_speed_10m'],
                          data_no_nan['arrival_delay_min'],
                          bins=50, cmap='viridis')
axes[2].set_title("Wind Speed vs. Train Delays")
axes[2].set_xlabel("Wind Speed (m/s)")
axes[2].set_ylabel("Arrival Delay (min)")
plt.colorbar(h_wind[3], ax=axes[2])

plt.tight_layout()
plt.show()



# %%% 2. Is There a Seasonal Variation in Train Punctuality Related to Weather Conditions?

# Sort the data by month number so that the boxplot displays months in calendar order.
data_clean_iqr_sorted = data_no_nan.sort_values('month_num')

plt.figure(figsize=(12,6))
data_clean_iqr_sorted.boxplot(column='arrival_delay_min', by='month', grid=False)
plt.title("Arrival Delay by Month (Seasonal Variation)")
plt.xlabel("Month")
plt.ylabel("Arrival Delay (min)")
plt.suptitle("")  # Remove the automatic subtitle
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


#%%% 3. How Does Extreme Weather Impact Train Disruptions?

# Boxplot of Delays under Extreme Weather Conditions:
# Compares distributions of arrival delays for “extreme” versus “normal” weather days.

