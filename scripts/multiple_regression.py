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
