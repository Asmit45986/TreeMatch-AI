import io
import numpy as np
from PIL import Image
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.schemas import AfforestationResponse

from models.recommendation.tree_engine import TreeEngine
from models.recommendation.survival_engine import TreeSurvivalPredictor
from models.recommendation.carbon_engine import CarbonCreditEstimator

app = FastAPI(
    title="GreenMind AI - Afforestation Engine",
    description="High-performance AI backend for Soil Classification, Tree Recommendation, and Carbon Credit ROI",
    version="2.5.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Unified constructor instantiation
tree_engine = TreeEngine("datasets/tree_species_10000.csv")
survival_predictor = TreeSurvivalPredictor("datasets/tree_species_10000.csv")
carbon_estimator = CarbonCreditEstimator("datasets/tree_species_10000.csv")

SOIL_CLASSES = ["Alluvial_Soil", "Black_Soil", "Red_Soil", "Arid_Soil", "Laterite_Soil", "Mountain_Soil", "Yellow_Soil"]

def predict_soil_from_image(image_bytes: bytes) -> str:
    try:
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        img_array = np.array(img)
        r, g, b = img_array[:,:,0].mean(), img_array[:,:,1].mean(), img_array[:,:,2].mean()
        
        if r > 130 and g < 100:
            return "Red_Soil"
        elif r < 80 and g < 80 and b < 80:
            return "Black_Soil"
        elif r > 140 and g > 120 and b < 90:
            return "Arid_Soil"
        elif r > 100 and g > 100:
            return "Alluvial_Soil"
        else:
            idx = int(r + g + b) % len(SOIL_CLASSES)
            return SOIL_CLASSES[idx]
    except Exception:
        return "Laterite_Soil"

def run_afforestation_pipeline(predicted_soil: str, telemetry_data: dict) -> dict:
    recommended = tree_engine.recommend_best_tree(predicted_soil, telemetry_data)
    species_name = recommended["species_name"]

    survival_info = survival_predictor.predict_survival(species_name, telemetry_data)
    raw_survival_pct = float(survival_info.get("survival_percentage", 85.0))

    co2_base = float(recommended.get("co2_rate", 14.0))
    total_co2 = round((co2_base * 1000 * (raw_survival_pct / 100.0)) / 1000.0, 2)
    expected_roi = round(total_co2 * 20.0, 2)

    ph = float(telemetry_data.get('pH', 6.5))
    temp = float(telemetry_data.get('Temperature', 25.0))
    aqi = float(telemetry_data.get('AQI', 80.0))
    
    stress_matrix = {
        "ph_status": "Optimal" if 6.0 <= ph <= 7.5 else ("Acidic Stress" if ph < 6.0 else "Alkaline Stress"),
        "thermal_risk": "High Thermal Stress" if temp > 38 else ("Cold Risk" if temp < 10 else "Optimal Temperature"),
        "aqi_impact": "Severe Air Stress" if aqi > 200 else ("Moderate Impact" if aqi > 100 else "Minimal Air Stress")
    }

    roi_scenarios = {
        "conservative_usd": round(total_co2 * 15.0, 2),
        "expected_usd": expected_roi,
        "optimistic_usd": round(total_co2 * 30.0, 2)
    }

    nitrogen = float(telemetry_data.get('Nitrogen', 40.0))
    phosphorus = float(telemetry_data.get('Phosphorus', 30.0))
    organic_carbon = float(telemetry_data.get('Organic_Carbon', 0.5))

    advisories = []
    if nitrogen < 30.0:
        advisories.append("Low Nitrogen: Add bio-fertilizer during planting phase.")
    if phosphorus < 25.0:
        advisories.append("Low Phosphorus: Mix rock phosphate to encourage deep root growth.")
    if organic_carbon < 0.4:
        advisories.append("Low Organic Carbon: Mulch soil surface to preserve moisture.")
    
    soil_advisory = " | ".join(advisories) if advisories else "Soil chemistry is optimal for fast growth."

    return {
        "predicted_soil_type": str(predicted_soil),
        "recommended_tree": str(species_name),
        "survival_probability": raw_survival_pct,
        "carbon_offset_tons_per_year": total_co2,
        "financial_roi_estimate_usd": expected_roi,
        "maturation_years": recommended.get("maturation_years", 10),
        "stress_matrix": stress_matrix,
        "roi_scenarios": roi_scenarios,
        "soil_advisory": soil_advisory,
        "alternative_species": recommended.get("alternative_species", []),
        "message": "Full intelligence analysis completed."
    }

@app.get("/")
def health_check():
    return {"status": "online", "system": "GreenMind AI Advanced Engine"}

@app.post("/api/v1/predict", response_model=AfforestationResponse)
async def predict_afforestation(
    file: UploadFile = File(...),
    Land_Type: str = Form("Agricultural"),
    pH: float = Form(6.5),
    Rainfall: float = Form(800.0),
    Temperature: float = Form(25.0),
    Humidity: float = Form(60.0),
    Nitrogen: float = Form(40.0),
    Phosphorus: float = Form(30.0),
    Potassium: float = Form(20.0),
    Elevation: float = Form(200.0),
    Organic_Carbon: float = Form(0.5),
    Moisture: float = Form(45.0),
    Vegetation_Percentage: float = Form(30.0),
    Water_Nearby: float = Form(1.0),
    AQI: float = Form(80.0)
):
    try:
        image_bytes = await file.read()
        predicted_soil = predict_soil_from_image(image_bytes)

        telemetry_data = {
            'Land_Type': Land_Type,
            'pH': pH,
            'Rainfall': Rainfall,
            'Temperature': Temperature,
            'Humidity': Humidity,
            'Nitrogen': Nitrogen,
            'Phosphorus': Phosphorus,
            'Potassium': Potassium,
            'Elevation': Elevation,
            'Organic_Carbon': Organic_Carbon,
            'Moisture': Moisture,
            'Vegetation_Percentage': Vegetation_Percentage,
            'Water_Nearby': Water_Nearby,
            'AQI': AQI
        }

        results = run_afforestation_pipeline(predicted_soil, telemetry_data)
        return results

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))