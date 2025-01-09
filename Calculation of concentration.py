import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
from scipy.stats import linregress

# Load the dataset
file_path = r'C:\Users\LB945465\OneDrive - University at Albany - SUNY\State University of New York\Extra\BrC study\raw files\phase_I_combined.csv'
phase_I_data = pd.read_csv(file_path)

# Convert Date Time column to datetime
phase_I_data["Date Time"] = pd.to_datetime(phase_I_data["Date Time"])

# Constants
filter_area = 1.54  # cm² (standard filter area for MicroAeth)
time_step = 60  # seconds (minute-level data)
MAC = {
    "UV": 1.0,      # m²/g (example for 370 nm; adjust based on literature)
    "Blue": 1.5,    # m²/g (example for 470 nm)
    "Green": 2.0,   # m²/g (example for 520 nm)
    "Red": 2.5,     # m²/g (example for 590 nm)
    "IR": 10.0      # m²/g (example for 880 nm)
}

# Extract relevant columns
columns_to_keep = [
    "Date Time", "GPS Lat", "GPS Long", "Datum ID", "Flow Total",
    "UV BCc Post", "Blue BCc Post", "Green BCc Post", "Red BCc Post", "IR BCc Post"
]
for wavelength in ["UV", "Blue", "Green", "Red", "IR"]:
    columns_to_keep.extend([f"{wavelength} ATN1", f"{wavelength} ATN2"])
data = phase_I_data[columns_to_keep].copy()

# Calculate the change in ATN for each wavelength
for wavelength in ["UV", "Blue", "Green", "Red", "IR"]:
    data[f"{wavelength}_dATN"] = data[f"{wavelength} ATN2"] - data[f"{wavelength} ATN1"]

# Calculate absorption coefficients (b_abs)
for wavelength in ["UV", "Blue", "Green", "Red", "IR"]:
    data[f"{wavelength}_b_abs"] = data[f"{wavelength}_dATN"] / (filter_area * time_step)

# Calculate BC concentrations (BCc)
for wavelength in ["UV", "Blue", "Green", "Red", "IR"]:
    data[f"{wavelength}_BCc_Calculated"] = data[f"{wavelength}_b_abs"] / MAC[wavelength]

# Save the processed data for comparison
output_path = r'C:\Users\LB945465\OneDrive - University at Albany - SUNY\State University of New York\Extra\BrC study\processed files\phase_I_comparison.csv'
data.to_csv(output_path, index=False)
print(f"Comparison data saved to {output_path}")

# Generate scatter plots and save to a single PDF
pdf_path = r'C:\Users\LB945465\OneDrive - University at Albany - SUNY\State University of New York\Extra\BrC study\processed files\phase_I_comparison_scatter_plots.pdf'
with PdfPages(pdf_path) as pdf:
    for wavelength in ["UV", "Blue", "Green", "Red", "IR"]:
        # Extract calculated and pre-processed BCc values
        x = data[f"{wavelength}_BCc_Calculated"]
        y = data[f"{wavelength} BCc Post"]
        
        # Perform linear regression
        slope, intercept, r_value, _, _ = linregress(x, y)
        line_eq = f"y = {slope:.2f}x + {intercept:.2f}"
        r_squared = f"$R^2$ = {r_value**2:.2f}"
        
        # Scatter plot with regression line
        plt.figure(figsize=(10, 6))
        plt.scatter(x, y, alpha=0.6, label="Data points")
        plt.plot(x, slope * x + intercept, color="red", label=f"Fit: {line_eq}\n{r_squared}")
        plt.xlabel(f"{wavelength} BCc Calculated (ng/m³)")
        plt.ylabel(f"{wavelength} BCc Post (ng/m³)")
        plt.title(f"{wavelength} BCc Comparison (Calculated vs Post-Processed)")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        pdf.savefig()
        plt.close()

print(f"Scatter plots saved to {pdf_path}")
