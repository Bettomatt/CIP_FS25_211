from scipy.stats import linregress
from preprocessing import get_data_no_nan
import matplotlib.pyplot as plt

# get data
alldata = get_data_no_nan()

print(max(alldata["arrival_delay_min"]))

# Filter out negative delay values before extracting y
alldata = alldata[alldata["arrival_delay_min"] >= 0]

"""
all column names:

Index(['date', 'station', 'planned_arrival', 'real_arrival',
       'arrival_delay_min', 'cancelled', 'temperature_2m', 'precipitation',
       'snowfall', 'wind_speed_10m', 'cloudcover', 'weathercode',
       'precipitation_category', 'snowfall_category', 'weekday', 'month',
       'month_num', 'orig_weather_description', 'simp_weather_description'],
      dtype='object')
"""


########################################################
#%%%% Relationship between train delay and precipitation
########################################################

precipitation = alldata["precipitation"]
y = alldata["arrival_delay_min"]

# Perform regression
slope, intercept, r_value, p_value, std_err = linregress(precipitation, y)

# Print results
print("precipitation and delay regression results:")
print(f"Regression Coefficient (Slope): {slope:.4f}")
print(f"Intercept: {intercept:.4f}")
print(f"R² Score: {r_value**2:.4f}")
print(f"P-Value: {p_value:.4f} (Significance)")
print(f"Standard Error: {std_err:.4f}\n")

# Plot
plt.scatter(precipitation, y, label="Datapoint per Train", alpha=0.5)
plt.plot(precipitation, slope * precipitation + intercept, color="red", label=f"Regression Line (y = {slope:.2f}x + {intercept:.2f})")
plt.xlabel("Precipitation (mm)")
plt.ylabel("Train Delay (min)")
plt.title("Linear Regression using SciPy")
plt.legend()
plt.xlim(min(precipitation) - 0, max(precipitation) + 1)  # Extend x-axis by 1 unit on each side
plt.ylim(min(y) - 0, max(y) + 5)  # Extend y-axis by 10 units on each side
plt.show()


"""
•	Rain has a statistically significant but practically negligible effect on train delays.
•	Other factors (e.g., train congestion, infrastructure, accidents) likely have a much stronger influence.
"""


########################################################
#%%%% Relationship between train delay and snowfall
########################################################


snowfall = alldata["snowfall"]

# Perform regression
slope, intercept, r_value, p_value, std_err = linregress(snowfall, y)

# Print results
print("snowfall regression results:")
print(f"Regression Coefficient (Slope): {slope:.4f}")
print(f"Intercept: {intercept:.4f}")
print(f"R² Score: {r_value**2:.4f}")
print(f"P-Value: {p_value:.4f} (Significance)")
print(f"Standard Error: {std_err:.4f}\n")

# Plot
plt.scatter(snowfall, y, label="Datapoint per Train", alpha=0.5)
plt.plot(snowfall, slope * snowfall + intercept, color="red", label=f"Regression Line (y = {slope:.2f}x + {intercept:.2f})")
plt.xlabel("snowfall (cm)")
plt.ylabel("Train Delay (min)")
plt.title("Relationship between train delay and snowfall")
plt.legend()
plt.show()


########################################################
#%%%% Relationship between train delay and temperature
########################################################


temperature = alldata["temperature_2m"]

# Perform regression
slope, intercept, r_value, p_value, std_err = linregress(temperature, y)

# Print results
print("temperature regression results:")
print(f"Regression Coefficient (Slope): {slope:.4f}")
print(f"Intercept: {intercept:.4f}")
print(f"R² Score: {r_value**2:.4f}")
print(f"P-Value: {p_value:.4f} (Significance)")
print(f"Standard Error: {std_err:.4f}\n")

# Plot
plt.scatter(temperature, y, label="Datapoint per Train", alpha=0.5)
plt.plot(temperature, slope * temperature + intercept, color="red", label=f"Regression Line (y = {slope:.2f}x + {intercept:.2f})")
plt.xlabel("Temperature C")
plt.ylabel("Train Delay (min)")
plt.title("Relationship between train delay and temperature")
plt.legend()
plt.show()


########################################################
#%%%% Relationship between train delay and wind
########################################################


wind_speed = alldata["wind_speed_10m"]

# Perform regression
slope, intercept, r_value, p_value, std_err = linregress(wind_speed, y)

# Print results
print("temperature regression results:")
print(f"Regression Coefficient (Slope): {slope:.4f}")
print(f"Intercept: {intercept:.4f}")
print(f"R² Score: {r_value**2:.4f}")
print(f"P-Value: {p_value:.4f} (Significance)")
print(f"Standard Error: {std_err:.4f}\n")

# Plot
plt.scatter(wind_speed, y, label="Datapoint per Train", alpha=0.5)
plt.plot(wind_speed, slope * wind_speed + intercept, color="red", label=f"Regression Line (y = {slope:.2f}x + {intercept:.2f})")
plt.xlabel("wind_speed km/h")
plt.ylabel("Train Delay (min)")
plt.title("Relationship between train delay and wind speed")
plt.legend()
plt.show()