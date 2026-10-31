import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Resolve paths relative to this script so it works from any working directory.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "Datasets" / "Occupancy_Estimation.csv"
OUTPUT_PATH = Path(__file__).resolve().parent / "occupancy_graph.png"

# Load the recorded occupancy dataset.
df = pd.read_csv(DATA_PATH)
df.columns = df.columns.str.strip()

print("FIRST FIVE RECORDS:")
print(df.head())

print("\nDATASET SHAPE:")
print(df.shape)

print("\nCOLUMN NAMES:")
print(df.columns.tolist())

print("\nPEOPLE COUNT DISTRIBUTION:")
print(df["Room_Occupancy_Count"].value_counts().sort_index())

print("\nMISSING VALUES:")
print(df.isnull().sum())

# Visualise people-count distribution.
occupancy_counts = df["Room_Occupancy_Count"].value_counts().sort_index()

plt.figure(figsize=(8, 5))
plt.bar(occupancy_counts.index.astype(str), occupancy_counts.values)
plt.title("Room Occupancy Distribution")
plt.xlabel("Number of People in Room")
plt.ylabel("Number of Records")
plt.tight_layout()
plt.savefig(OUTPUT_PATH, dpi=150)
plt.close()

# Temperature and CO2 analysis.
temperature_columns = ["S1_Temp", "S2_Temp", "S3_Temp", "S4_Temp"]
df["Average_Temperature"] = df[temperature_columns].mean(axis=1)

print("\n========== TEMPERATURE ANALYSIS ==========")
print(df["Average_Temperature"].describe())
print("\nOverall Average Temperature:")
print(round(df["Average_Temperature"].mean(), 2), "°C")

print("\n========== CO2 ANALYSIS ==========")
print(df["S5_CO2"].describe())
print("\nOverall Average CO2:")
print(round(df["S5_CO2"].mean(), 2), "ppm")

print(f"\nOccupancy graph saved to: {OUTPUT_PATH}")
print("PROGRAM FINISHED SUCCESSFULLY")
