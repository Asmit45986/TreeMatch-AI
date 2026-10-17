from pydantic import BaseModel
from typing import List, Dict, Optional

class StressMatrix(BaseModel):
    ph_status: str
    thermal_risk: str
    aqi_impact: str

class RoiScenarios(BaseModel):
    conservative_usd: float
    expected_usd: float
    optimistic_usd: float

class AfforestationResponse(BaseModel):
    predicted_soil_type: str
    recommended_tree: str
    survival_probability: float
    carbon_offset_tons_per_year: float
    financial_roi_estimate_usd: float
    maturation_years: int
    stress_matrix: StressMatrix
    roi_scenarios: RoiScenarios
    soil_advisory: str
    alternative_species: List[str]
    message: Optional[str] = "Success"