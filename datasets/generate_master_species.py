import pandas as pd
import numpy as np
import os

os.makedirs("datasets", exist_ok=True)

tree_species_names = [
    "Neem", "Teak", "Acacia (Babool)", "Shisham", "Bamboo", "Khejri", "Amaltas", "Banyan", "Peepal", 
    "Eucalyptus", "Oak", "Pine", "Cedar", "Mahogany", "Cashew", "Gulmohar", "Jacaranda", "Arjun Tree", 
    "Kadamba", "Karanj", "Sal", "Sandalwood", "Deodar", "Silver Oak", "Haritaki", "Bahera", "Amla"
]

soil_types_list = [
    "Alluvial_Soil", "Black_Soil", "Red_Soil", "Arid_Soil", 
    "Laterite_Soil", "Mountain_Soil", "Yellow_Soil"
]

dataset = []

# Loop up to 10,000 species
for i in range(1, 10001):
    base_name = np.random.choice(tree_species_names)
    species_name = f"{base_name} Var_{i}"
    
    assigned_soils = np.random.choice(soil_types_list, size=2, replace=False)
    
    dataset.append({
        "species_id": f"TREE_{i:05d}",
        "species_name": species_name,
        "soil_types": ",".join(assigned_soils),
        "min_ph": round(float(np.random.uniform(5.0, 6.5)), 1),
        "max_ph": round(float(np.random.uniform(7.0, 8.5)), 1),
        "min_temp_c": int(np.random.randint(10, 22)),
        "max_temp_c": int(np.random.randint(35, 48)),
        "min_rainfall_mm": int(np.random.randint(300, 800)),
        "max_rainfall_mm": int(np.random.randint(1200, 3000)),
        "aqi_max_tolerance": int(np.random.randint(3, 6)),
        "co2_absorption_kg_yr": round(float(np.random.uniform(12.0, 32.0)), 1),
        "maturation_years": int(np.random.randint(5, 15))
    })

df = pd.DataFrame(dataset)
df.to_csv("datasets/tree_species_10000.csv", index=False)
print("✅ Master Dataset with 10,000 Species saved successfully at: datasets/tree_species_10000.csv")