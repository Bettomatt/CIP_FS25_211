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
precipitation     float64
snowfall          float64
temperature_2m    float64
wind_speed_10m    float64
dtype: object
Regression Coefficients:
          Feature  Coefficient
0       Intercept     1.367037
1   precipitation     0.033858
2        snowfall     0.058494
3  temperature_2m     0.010327
4  wind_speed_10m     0.000534
R² Score: 0.0002
"""

"""
A multiple linear regression was performed in which weather conditions were used to predict train arrival delays. 
A bias term (intercept, expected train arrival delay) was inserted, and precipitation, snowfall, temperature, and 
wind speed were included as explanatory variables. It was found that an intercept of approximately 1.3670 was estimated, 
with coefficients for precipitation, snowfall, temperature, and wind speed of about 0.0339, 0.0585, 0.0103, and 0.0005, 
respectively. It was observed that increases in each weather variable were associated with only minimal increases in 
the arrival delay. The overall model fit was determined to be extremely poor, as indicated by an R² score of 0.0002, 
which suggests that only 0.02% of the variance in arrival delay was explained by the weather features. It was concluded 
that the influence of the selected weather conditions on train delays is negligible, and it was suggested that other 
factors might be required to better explain the variability in train delays.
"""