import io
import os
import joblib
import numpy as np
import pandas as pd
import tensorflow as tf
from PIL import Image

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHECKPOINTS_DIR = os.path.join(BASE_DIR, "checkpoints")

# Load Models
SOIL_MODEL_PATH = os.path.join(CHECKPOINTS_DIR, "soil_classifier_7class.h5")
RECOMMENDER_PATH = os.path.join(CHECKPOINTS_DIR, "tree_recommender.pkl")
REGRESSOR_PATH = os.path.join(CHECKPOINTS_DIR, "survival_regressor.pkl")

print("⏳ Loading Trained Models into Memory...")
soil_model = tf.keras.models.load_model(SOIL_MODEL_PATH)
tree_recommender = joblib.load(RECOMMENDER_PATH)
survival_regressor = joblib.load(REGRESSOR_PATH)
print("✅ All Models Loaded Successfully!")

SOIL_CLASSES = [
    'Alluvial_Soil',
    'Arid_Soil',
    'Black_Soil',
    'Laterite_Soil',
    'Mountain_Soil',
    'Red_Soil',
    'Yellow_Soil'
]

def predict_soil_from_image(image_bytes: bytes) -> str:
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    image = image.resize((224, 224))
    img_array = np.array(image) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    
    predictions = soil_model.predict(img_array)
    predicted_idx = np.argmax(predictions[0])
    return SOIL_CLASSES[predicted_idx]

def run_afforestation_pipeline(soil_type: str, telemetry: dict) -> dict:
    # Full feature set aligned with trained Scikit-Learn models
    input_data = pd.DataFrame([{
        'Land_Type': telemetry.get('Land_Type', 'Agricultural'),
        'Soil_Type': soil_type,
        'pH': float(telemetry.get('pH', 6.5)),
        'Rainfall': float(telemetry.get('Rainfall', 800.0)),
        'Temperature': float(telemetry.get('Temperature', 25.0)),
        'Humidity': float(telemetry.get('Humidity', 60.0)),
        'Nitrogen': float(telemetry.get('Nitrogen', 40.0)),
        'Phosphorus': float(telemetry.get('Phosphorus', 30.0)),
        'Potassium': float(telemetry.get('Potassium', 20.0)),
        'Elevation': float(telemetry.get('Elevation', 200.0)),
        'Organic_Carbon': float(telemetry.get('Organic_Carbon', 0.5)),
        'Moisture': float(telemetry.get('Moisture', 45.0)),
        'Vegetation_Percentage': float(telemetry.get('Vegetation_Percentage', 30.0)),
        'Water_Nearby': float(telemetry.get('Water_Nearby', 1.0)), # 1.0 for Yes, 0.0 for No
        'AQI': float(telemetry.get('AQI', 80.0))
    }])

    recommended_tree = str(tree_recommender.predict(input_data)[0])
    survival_prob = float(survival_regressor.predict(input_data)[0])

    carbon_offset = round((survival_prob / 100.0) * 0.022 * 500, 2)
    financial_roi = round(carbon_offset * 15.0, 2)

    return {
        "predicted_soil_type": soil_type,
        "recommended_tree": recommended_tree,
        "survival_probability": round(survival_prob, 2),
        "carbon_offset_tons_per_year": carbon_offset,
        "financial_roi_estimate_usd": financial_roi,
        "message": "Afforestation analysis completed successfully!"
    }