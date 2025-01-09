# -*- coding: utf-8 -*-
"""
Compare Interpolation Method vs Original Data with Negatives Retained
Include Time-Series Plots for Both Datasets and Save Figures
@author: lb945465
"""

import pandas as pd
import matplotlib.pyplot as plt
import os

# Load the dataset
file_path = r'C:\Users\LB945465\OneDrive - University at Albany - SUNY\State University of New York\Extra\BrC study\raw files\phase_I_combined.csv'
data = pd.read_csv(file_path)

# Convert Date Time column to datetime
data["Date Time"] = pd.to_datetime(data["Date Time"])

# Extract Date Time and pre-processed BCc Post values for all wavelengths
wavelengths = ["UV", "Blue", "Green", "Red", "IR"]
time_series_data = data[["Date Time"] + [f"{wavelength} BCc Post" for wavelength in wavelengths]].copy()

# Create a dataset for interpolation method
interpolated_data = time_series_data.copy()

# Interpolation Method: Replace negatives with interpolated values
for wavelength in wavelengths:
    interpolated_data[f"{wavelength} BCc Post"] = interpolated_data[f"{wavelength} BCc Post"].apply(
        lambda x: None if x < 0 else x
    )
    interpolated_data[f"{wavelength} BCc Post"] = interpolated_data[f"{wavelength} BCc Post"].interpolate(method='linear')

# Define output path for figures
output_folder = r'C:\Users\LB945465\OneDrive - University at Albany - SUNY\State University of New York\Extra\BrC study\processed files'
os.makedirs(output_folder, exist_ok=True)

# Scatter Plot Comparison
plt.figure(figsize=(15, 8))
for wavelength in wavelengths:
    plt.scatter(time_series_data[f"{wavelength} BCc Post"], interpolated_data[f"{wavelength} BCc Post"], alpha=0.6, label=wavelength)

# Add labels, legend, and title
plt.xlabel("Original BCc Post (ng/m³, with Negatives)")
plt.ylabel("Interpolated BCc Post (ng/m³)")
plt.title("Comparison of Interpolation Method vs Original Data")
plt.legend(title="Wavelengths")
plt.grid(True)
plt.tight_layout()

# Save the scatter plot
scatter_plot_path = os.path.join(output_folder, "scatter_plot_interpolation_comparison.png")
plt.savefig(scatter_plot_path, dpi=300)
plt.show()

# Time-Series Plots: Original Data (Negatives Retained)
plt.figure(figsize=(15, 8), dpi=300)
for wavelength in wavelengths:
    plt.plot(time_series_data["Date Time"], time_series_data[f"{wavelength} BCc Post"], label=f"{wavelength} BCc Post (Original)")

# Add labels, legend, and title
plt.xlabel("Date Time")
plt.ylabel("BC concentration by wavelength (ng/m³)")
plt.title("Time Series: Original Data (Negatives Retained)")
plt.legend(title="Wavelengths")
plt.grid(True)
plt.tight_layout()

# Save the time-series plot for original data
time_series_original_path = os.path.join(output_folder, "time_series_original_data.png")
plt.savefig(time_series_original_path, dpi=300)
plt.show()

# Time-Series Plots: Interpolated Data
plt.figure(figsize=(15, 8), dpi=300)
for wavelength in wavelengths:
    plt.plot(interpolated_data["Date Time"], interpolated_data[f"{wavelength} BCc Post"], label=f"{wavelength} BCc Post (Interpolated)")

# Add labels, legend, and title
plt.xlabel("Date Time")
plt.ylabel("BC concentration by wavelength (ng/m³)")
plt.title("Time Series: Interpolated Data")
plt.legend(title="Wavelengths")
plt.grid(True)
plt.tight_layout()

# Save the time-series plot for interpolated data
time_series_interpolated_path = os.path.join(output_folder, "time_series_interpolated_data.png")
plt.savefig(time_series_interpolated_path, dpi=300)
plt.show()

# Save Results
output_path_interpolated = os.path.join(output_folder, "phase_I_interpolated.csv")
interpolated_data.to_csv(output_path_interpolated, index=False)

print(f"Interpolated data saved to {output_path_interpolated}")
print(f"Figures saved to {output_folder}")
