import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# First, execute the data processing step in the script visualizations_part1.
# Use dataframe < data_no_nan >

# Research Questions:
# %%% 1.  How Do Different Weather Conditions Influence Train Delays?

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

