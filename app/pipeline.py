from models.recommendation.tree_engine import TreeEngine
from models.recommendation.survival_engine import TreeSurvivalPredictor
from models.recommendation.carbon_engine import CarbonCreditEstimator

# Instantitate recommendation engines from models/recommendation
tree_engine_instance = TreeEngine("datasets/tree_species_10000.csv")
survival_predictor = TreeSurvivalPredictor()
carbon_estimator = CarbonCreditEstimator()

def predict_soil_from_image(image_bytes: bytes) -> str:
    # Retain your CNN Model inference logic here
    return "Black_Soil"

def run_afforestation_pipeline(predicted_soil: str, telemetry_data: dict) -> dict:
    # 1. Dynamic Tree Recommendation from 10,000 Dataset
    recommended_tree = tree_engine_instance.recommend_best_tree(predicted_soil, telemetry_data)
    species_name = recommended_tree["species_name"]

    # 2. Survival & Carbon Calculations
    env_profile = {
        'weather': {
            'temperature': telemetry_data.get('Temperature', 25.0),
            'humidity': telemetry_data.get('Humidity', 60.0)
        },
        'air_quality': {
            'aqi_index': telemetry_data.get('AQI', 80.0) / 50.0
        }
    }

    survival_info = survival_predictor.predict_survival(species_name, env_profile)
    survival_pct = survival_info.get("survival_percentage", 90.0)

    carbon_info = carbon_estimator.estimate_carbon_credits(
        tree_name=species_name,
        tree_count=1000,
        survival_percentage=survival_pct,
        project_years=10
    )

    return {
        "predicted_soil": predicted_soil,
        "recommended_species": species_name,
        "survival_probability": f"{survival_pct}%",
        "carbon_offset": str(carbon_info.get("total_co2_absorbed_tons", 10.0)),
        "estimated_roi_usd": f"${round(carbon_info.get('carbon_credits', 0.0) * 20.0, 2)} USD",
        "details": {
            "survival_details": survival_info,
            "carbon_details": carbon_info
        }
    }