
#%%%####################################################################################################
# First visualizations to explore the data
########################################################################################################
# %%% Heat Map: Arrival Delay vs Temperature
print(data_no_nan['temperature_2m'].describe())

plt.figure(figsize=(10, 6))
hb = plt.hist2d(data_no_nan['temperature_2m'], data_no_nan['arrival_delay_min'], bins=50, cmap='viridis')
plt.colorbar(hb[3], label='Number of Observations')
plt.title("Heatmap of Arrival Delay vs Temperature")
plt.xlabel("Temperature (°C)")
plt.ylabel("Arrival Delay (min)")
plt.tight_layout()
plt.show()

# %%% Heat Map: Arrival Delay vs Precipitation
print(data_no_nan['precipitation'].describe())

# to find missing days
data_no_nan.boxplot(column='precipitation', by='date', grid=False)
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 6))
hb = plt.hist2d(data_no_nan['precipitation'], data_no_nan['arrival_delay_min'], bins=50, cmap='viridis')
plt.colorbar(hb[3], label='Number of Observations')
plt.title("Heatmap of Arrival Delay vs Precipitation")
plt.xlabel("Precipitation (mm)")
plt.ylabel("Arrival Delay (min)")
plt.tight_layout()
plt.show()

# %%% Boxplot: Arrival Delay vs Precipitation
plt.figure(figsize=(10, 6))
data_no_nan.boxplot(
    column='arrival_delay_min',
    by='precipitation_category',
    grid=False
)

plt.title("Arrival Delay by Snowfall Category")
plt.suptitle("")  # Remove the default subtitle
plt.xlabel("Snowfall Range")
plt.ylabel("Arrival Delay (min)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# %%% Heat Map: Arrival Delay vs Wind Speed (km/h)
print(data_no_nan['wind_speed_10m'].describe())

plt.figure(figsize=(10, 6))
hb = plt.hist2d(data_no_nan['wind_speed_10m'], data_no_nan['arrival_delay_min'], bins=50, cmap='viridis')
plt.colorbar(hb[3], label='Number of Observations')
plt.title("Heatmap of Arrival Delay vs Wind Speed")
plt.xlabel("Wind Speed (km/h)")
plt.ylabel("Arrival Delay (min)")
plt.tight_layout()
plt.show()

# %%% Heat Map: Arrival Delay vs Snowfall (cm)
print(data_no_nan['snowfall'].describe())

plt.figure(figsize=(10, 6))
hb = plt.hist2d(data_no_nan['snowfall'], data_no_nan['arrival_delay_min'], bins=50, cmap='viridis')
plt.colorbar(hb[3], label='Number of Observations')
plt.title("Heatmap of Arrival Delay vs Snowfall")
plt.xlabel("Snowfall (cm)")
plt.ylabel("Arrival Delay (min)")
plt.tight_layout()
plt.show()

# %%% Boxplot: Arrival Delay vs Snowfall (cm)
plt.figure(figsize=(10, 6))
data_no_nan.boxplot(
    column='arrival_delay_min',
    by='snowfall_category',
    grid=False
)

plt.title("Arrival Delay by Snowfall Category")
plt.suptitle("")  # Remove the default subtitle
plt.xlabel("Snowfall Range")
plt.ylabel("Arrival Delay (min)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# %%% Box plot of Arrival Delays by day of the week
plt.figure(figsize=(10,6))
# Creates a box plot for arrival delays grouped by weekday
data_no_nan.boxplot(column='arrival_delay_min', by='weekday', grid=False)
plt.title("Arrival Delay by Day of the Week")
plt.suptitle("")  # Remove default subtitle
plt.xlabel("Day of the Week")
plt.ylabel("Arrival Delay (min)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# %%% Box plot of Arrival Delays by Cancellation Status
print(data_no_nan['cancelled'].describe())
# It is possible that no connections were cancelled (then all FALSE)

plt.figure(figsize=(10,6))
# Creates a box plot for arrival delays grouped by weekday
data_no_nan.boxplot(column='arrival_delay_min', by='cancelled', grid=False)
plt.title("Arrival Delay by Cancellation Status")
plt.suptitle("")  # Remove default subtitle
plt.xlabel("Cancellation Status")
plt.ylabel("Arrival Delay (min)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# %%% Box plot of Arrival Delays by Weather Code
"""
Weather condition is a numeric code. Follow WMO weather interpretation codes. See table below for details.
WMO Weather interpretation codes (WW)
Code	    Description
0	        Clear sky
1,  2,  3	Mainly clear, partly cloudy, and overcast
45, 48	    Fog and depositing rime fog
51, 53, 55	Drizzle: Light, moderate, and dense intensity
56, 57	    Freezing Drizzle: Light and dense intensity
61, 63, 65	Rain: Slight, moderate and heavy intensity
66, 67	    Freezing Rain: Light and heavy intensity
71, 73, 75	Snow fall: Slight, moderate, and heavy intensity
77	        Snow grains
80, 81, 82	Rain showers: Slight, moderate, and violent
85, 86	    Snow showers slight and heavy
95 *	    Thunderstorm: Slight or moderate
96, 99 *	Thunderstorm with slight and heavy hail
"""

plt.figure(figsize=(10,6))
# Creates a box plot for arrival delays grouped by weekday
data_no_nan.boxplot(column='arrival_delay_min', by='simp_weather_description', grid=False)
plt.title("Arrival Delay by Weather Category")
plt.suptitle("")  # Remove default subtitle
plt.xlabel("Weather Category (simplified)")
plt.ylabel("Arrival Delay (min)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# %%% Box plot of Arrival Delays by Station
plt.figure(figsize=(10,6)) # Change of size is not working in .py
# Creates a box plot for arrival delays grouped by weekday
data_no_nan.boxplot(column='arrival_delay_min', by='station', grid=False)
plt.title("Arrival Delay by Stations")
plt.suptitle("")  # Remove default subtitle
plt.xlabel("Station")
plt.ylabel("Arrival Delay (min)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

