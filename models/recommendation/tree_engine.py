import os
import pandas as pd
import numpy as np

class TreeEngine:
    def __init__(self, csv_path: str = "datasets/tree_species_10000.csv"):
        self.csv_path = csv_path
        self.df = self._load_dataset()

    def _load_dataset(self) -> pd.DataFrame:
        if os.path.exists(self.csv_path):
            return pd.read_csv(self.csv_path)
        else:
            soils = ["Alluvial_Soil", "Black_Soil", "Red_Soil", "Arid_Soil", "Laterite_Soil", "Mountain_Soil", "Yellow_Soil"]
            data = []
            for i in range(1, 10001):
                data.append({
                    "species_id": f"TREE_{i:05d}",
                    "species_name": f"Species_Var_{i}",
                    "soil_types": ",".join(np.random.choice(soils, size=2, replace=False)),
                    "min_ph": round(float(np.random.uniform(4.5, 6.0)), 1),
                    "max_ph": round(float(np.random.uniform(7.0, 8.5)), 1),
                    "min_temp_c": int(np.random.randint(10, 20)),
                    "max_temp_c": int(np.random.randint(30, 45)),
                    "min_rainfall_mm": int(np.random.randint(300, 800)),
                    "max_rainfall_mm": int(np.random.randint(1200, 2500)),
                    "aqi_max_tolerance": int(np.random.randint(2, 5)),
                    "co2_absorption_kg_yr": round(float(np.random.uniform(12.0, 32.0)), 1),
                    "maturation_years": int(np.random.randint(5, 15))
                })
            return pd.DataFrame(data)

    def recommend_best_tree(self, soil_type: str, telemetry: dict) -> dict:
        ph = float(telemetry.get('pH', 6.5))
        rainfall = float(telemetry.get('Rainfall', 800.0))
        temp = float(telemetry.get('Temperature', 25.0))
        
        matching_df = self.df[self.df['soil_types'].str.contains(soil_type, case=False, na=False)].copy()
        if matching_df.empty:
            matching_df = self.df.copy()

        ph_penalty = np.maximum(0, matching_df['min_ph'] - ph) + np.maximum(0, ph - matching_df['max_ph'])
        temp_penalty = np.maximum(0, matching_df['min_temp_c'] - temp) + np.maximum(0, temp - matching_df['max_temp_c'])
        rain_penalty = np.maximum(0, matching_df['min_rainfall_mm'] - rainfall) + np.maximum(0, rainfall - matching_df['max_rainfall_mm'])

        matching_df['suitability_score'] = (ph_penalty * 10.0) + (temp_penalty * 2.0) + (rain_penalty / 50.0)

        sorted_df = matching_df.sort_values(by='suitability_score', ascending=True)
        best_match = sorted_df.iloc[0]

        alt_matches = []
        if len(sorted_df) > 2:
            alt_matches = [
                str(sorted_df.iloc[1]['species_name']),
                str(sorted_df.iloc[2]['species_name'])
            ]

        return {
            "species_name": str(best_match['species_name']),
            "co2_rate": float(best_match['co2_absorption_kg_yr']),
            "maturation_years": int(best_match['maturation_years']),
            "alternative_species": alt_matches
        }