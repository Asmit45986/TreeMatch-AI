import os
import sys
import pandas as pd
import numpy as np

print("🚀 Script execution started...")

# Absolute path resolution to prevent silent path errors
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASETS_DIR = os.path.join(BASE_DIR, "datasets")

# Search for any CSV file inside datasets folder or its subfolders
input_csv = None
for root, dirs, files in os.walk(DATASETS_DIR):
    for file in files:
        if file.endswith(".csv") and "corrected" not in file:
            input_csv = os.path.join(root, file)
            break

if not input_csv:
    print(f"❌ Error: Could not find any original CSV file inside: {DATASETS_DIR}")
    sys.exit(1)

print(f"📖 Found target CSV dataset: {input_csv}")
df = pd.read_csv(input_csv)

VALID_SOILS = [
    'Alluvial_Soil',
    'Arid_Soil',
    'Black_Soil',
    'Laterite_Soil',
    'Mountain_Soil',
    'Red_Soil',
    'Yellow_Soil'
]

def map_soil_type(row):
    pH = float(row['pH']) if 'pH' in row and pd.notnull(row['pH']) else 7.0
    rainfall = float(row['Rainfall']) if 'Rainfall' in row and pd.notnull(row['Rainfall']) else 800.0
    
    if 'Soil_Type' in row and pd.notnull(row['Soil_Type']):
        old_soil = str(row['Soil_Type']).strip()
        if old_soil == 'Alluvial': return 'Alluvial_Soil'
        if old_soil == 'Sandy' and rainfall < 500: return 'Arid_Soil'
        if old_soil == 'Clayey' and pH > 7.5: return 'Black_Soil'
        if old_soil == 'Rocky': return 'Mountain_Soil'
        if pH < 6.0: return 'Laterite_Soil' if rainfall > 800 else 'Red_Soil'
        if old_soil == 'Loamy': return 'Yellow_Soil' if pH < 6.8 else 'Alluvial_Soil'

    return np.random.choice(VALID_SOILS)

# Transform Soil_Type column
df['Soil_Type'] = df.apply(map_soil_type, axis=1)

# Save corrected dataset
output_csv = os.path.join(DATASETS_DIR, "corrected_afforestation_dataset.csv")
df.to_csv(output_csv, index=False)

print(f"✅ SUCCESS! Corrected dataset generated at:\n   {output_csv}")