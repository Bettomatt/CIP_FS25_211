
import pandas as pd
import numpy as np
import scipy.linalg
from preprocessing import get_data_no_nan2

# Load and clean data
alldata = get_data_no_nan2()

# Feature selection (weather-related features)
X = alldata[["precipitation", "snowfall", "temperature_2m", "wind_speed_10m"]].copy()

# Convert all columns in X to numeric (to avoid object types)
X = X.apply(pd.to_numeric, errors='coerce')

# Generate interaction terms
X["precip_snow"] = X["precipitation"] * X["snowfall"]
X["precip_temp"] = X["precipitation"] * X["temperature_2m"]
X["precip_wind"] = X["precipitation"] * X["wind_speed_10m"]
X["snow_temp"] = X["snowfall"] * X["temperature_2m"]
X["snow_wind"] = X["snowfall"] * X["wind_speed_10m"]
X["temp_wind"] = X["temperature_2m"] * X["wind_speed_10m"]

# Print data types of the columns to verify they are numeric
print(X.dtypes)

# Target variable
y = alldata["arrival_delay_min"]

# Remove negative delays
valid_indices = y >= 0
X = X[valid_indices]
y = y[valid_indices]

# Add a bias term (intercept) to X
X.insert(0, "Intercept", 1)

# Solve linear regression using least squares
beta, residuals, rank, singular_values = scipy.linalg.lstsq(X, y)

# Predictions
y_pred = X @ beta  # Matrix multiplication

# Calculate R²
SS_total = np.sum((y - np.mean(y))**2)
SS_residual = np.sum((y - y_pred)**2)
r2 = 1 - (SS_residual / SS_total)

# Print results
print("Regression Coefficients:")
print(pd.DataFrame({"Feature": X.columns, "Coefficient": beta}))

print(f"\nR² Score: {r2:.4f}")

"""
Effect of Weather on Train Delays:
Weather variables (precipitation, snowfall, temperature, wind speed) were tested as predictors of train arrival delays.
Most individual weather effects were small and had minimal impact on delays.

Interaction Effects:
Interactions between precipitation, snowfall, temperature, and wind speed were included to check for combined effects.
Some interactions (e.g., snow × temp, snow × wind) showed small effects, but none were substantial.

Model Fit (R² Score = 0.0004):
The model explains only 0.04% of the variation in train delays.
This means weather conditions alone do not significantly influence delays.

Key Takeaways:
The impact of weather on train delays is negligible.
Other factors (e.g., operational issues, infrastructure, congestion) likely play a much larger role.
"""



"""
Regression Coefficients:
           Feature  Coefficient
0        Intercept     1.450841
1    precipitation     0.160493
2         snowfall    -0.071101
3   temperature_2m    -0.002831
4   wind_speed_10m    -0.015505
5      precip_snow    -0.099169
6      precip_temp    -0.013805
7      precip_wind    -0.002369
8        snow_temp     0.073333
9        snow_wind     0.015182
10       temp_wind     0.002343

"""

"""
What has been done?
Multiple Linear Regression with Interaction Terms:

A regression model was built to analyze the effect of precipitation, snowfall, temperature, and wind speed on train arrival delays.
Interaction terms (e.g., precipitation × wind speed, snowfall × temperature) were included to examine 
whether weather factors together have a combined effect on delays.

Regression Results:
Individual weather variables had small coefficients, indicating a weak relationship with train delays.
Interaction terms showed no substantial impact—some had small positive or negative coefficients, 
but none were significant enough to explain delays.

Model Performance (R² Score = 0.0004):
The model explained only 0.04% of the variation in train delays, 
meaning that weather and its interactions do not meaningfully predict delays.

What does this outcome mean?
No strong combined effect was found between weather variables on train delays.
Train delays are likely influenced by other factors (e.g., operational disruptions, track conditions, 
scheduling issues) rather than weather conditions alone.
"""