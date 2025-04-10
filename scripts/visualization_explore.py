import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind

# Setup folders
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_folder = os.path.join(project_dir, 'data', 'final_data')
output_folder = os.path.join(project_dir, 'outputs')
os.makedirs(output_folder, exist_ok=True)

# Load data
df = pd.read_csv(os.path.join(data_folder, 'data_no_nan.csv'))

sns.set_theme(style="whitegrid", font_scale=1.2)

# Scatterplot: Temperature vs Delay
plt.figure(figsize=(8, 6))
sns.scatterplot(x='temperature_2m', y='arrival_delay_min', data=df, alpha=0.5)
plt.title('Arrival Delay vs Temperature')
plt.xlabel('Temperature (°C)')
plt.ylabel('Arrival Delay (minutes)')
plt.tight_layout()
plt.savefig(os.path.join(output_folder, 'scatter_temperature_delay.png'))
plt.close()

# Scatterplot: Precipitation vs Delay
plt.figure(figsize=(8, 6))
sns.scatterplot(x='precipitation', y='arrival_delay_min', data=df, alpha=0.5)
plt.title('Arrival Delay vs Precipitation')
plt.xlabel('Precipitation (mm)')
plt.ylabel('Arrival Delay (minutes)')
plt.tight_layout()
plt.savefig(os.path.join(output_folder, 'scatter_precipitation_delay.png'))
plt.close()

# Scatterplot: Wind Speed vs Delay
plt.figure(figsize=(8, 6))
sns.scatterplot(x='wind_speed_10m', y='arrival_delay_min', data=df, alpha=0.5)
plt.title('Arrival Delay vs Wind Speed')
plt.xlabel('Wind Speed (km/h)')
plt.ylabel('Arrival Delay (minutes)')
plt.tight_layout()
plt.savefig(os.path.join(output_folder, 'scatter_wind_speed_delay.png'))
plt.close()

# Boxplot: Delay by Month
plt.figure(figsize=(12, 6))
month_order = ['January', 'February', 'March', 'April', 'May', 'June',
               'July', 'August', 'September', 'October', 'November', 'December']
sns.boxplot(x='month', y='arrival_delay_min', data=df, order=month_order, palette='pastel')
plt.title('Arrival Delay by Month')
plt.xlabel('Month')
plt.ylabel('Arrival Delay (minutes)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(output_folder, 'boxplot_delay_by_month.png'))
plt.close()

# Heatmap: Precipitation + Wind Speed vs Delay
pivot_table = df.pivot_table(
    index=pd.cut(df['precipitation'], bins=10),
    columns=pd.cut(df['wind_speed_10m'], bins=10),
    values='arrival_delay_min',
    aggfunc='mean'
)

plt.figure(figsize=(12, 8))
sns.heatmap(pivot_table, cmap='coolwarm', linewidths=0.5, cbar_kws={'label': 'Average Delay (minutes)'})
plt.title('Average Delay by Precipitation and Wind Speed')
plt.xlabel('Wind Speed (binned)')
plt.ylabel('Precipitation (binned)')
plt.tight_layout()
plt.savefig(os.path.join(output_folder, 'heatmap_precipitation_wind_speed.png'))
plt.close()

# Boxplot: Snow vs No Snow
snow_delays = df[df['snowfall'] > 0]['arrival_delay_min']
no_snow_delays = df[df['snowfall'] == 0]['arrival_delay_min']

plt.figure(figsize=(8, 6))
plt.boxplot([no_snow_delays, snow_delays], labels=['No Snow', 'Snow'])
plt.title('Arrival Delay: Snow vs No Snow')
plt.ylabel('Arrival Delay (minutes)')
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(output_folder, 'boxplot_snow_vs_no_snow.png'))
plt.close()

# T-Test: Snow vs No Snow
t_stat_snow, p_value_snow = ttest_ind(snow_delays, no_snow_delays, equal_var=False, nan_policy='omit')

# T-Test: Rain vs No Rain
rain_delays = df[df['precipitation'] > 0]['arrival_delay_min']
no_rain_delays = df[df['precipitation'] == 0]['arrival_delay_min']

t_stat_rain, p_value_rain = ttest_ind(rain_delays, no_rain_delays, equal_var=False, nan_policy='omit')

# Save t-test results
with open(os.path.join(output_folder, 'weather_ttest_results.txt'), 'w') as f:
    f.write("Snowfall Impact:\n")
    f.write(f"T-statistic: {t_stat_snow:.4f}\n")
    f.write(f"P-value: {p_value_snow:.4f}\n")
    if p_value_snow < 0.05:
        f.write("Conclusion: Snowfall has a significant effect on train delays.\n")
    else:
        f.write("Conclusion: No significant effect of snowfall on train delays.\n")

    f.write("\nRainfall Impact:\n")
    f.write(f"T-statistic: {t_stat_rain:.4f}\n")
    f.write(f"P-value: {p_value_rain:.4f}\n")
    if p_value_rain < 0.05:
        f.write("Conclusion: Rainfall has a significant effect on train delays.\n")
    else:
        f.write("Conclusion: No significant effect of rainfall on train delays.\n")

print("All plots and statistical test results saved to the 'outputs/' folder.")
