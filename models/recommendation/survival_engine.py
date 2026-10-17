class TreeSurvivalPredictor:
    def __init__(self, csv_path: str = "datasets/tree_species_10000.csv"):
        self.csv_path = csv_path

    def predict_survival(self, species_name: str, telemetry: dict) -> dict:
        ph = float(telemetry.get('pH', 6.5))
        temp = float(telemetry.get('Temperature', 25.0))
        aqi = float(telemetry.get('AQI', 80.0))
        moisture = float(telemetry.get('Moisture', 45.0))
        rainfall = float(telemetry.get('Rainfall', 800.0))

        survival = 98.0

        if ph < 6.0:
            survival -= (6.0 - ph) * 12.0
        elif ph > 7.5:
            survival -= (ph - 7.5) * 12.0

        if temp > 30.0:
            survival -= (temp - 30.0) * 1.8
        elif temp < 15.0:
            survival -= (15.0 - temp) * 2.0

        if aqi > 50.0:
            survival -= (aqi - 50.0) * 0.12

        if moisture < 40.0:
            survival -= (40.0 - moisture) * 0.5
        if rainfall < 600.0:
            survival -= (600.0 - rainfall) * 0.03

        final_survival_pct = round(max(25.0, min(99.0, survival)), 1)

        return {
            "species_name": species_name,
            "survival_percentage": final_survival_pct
        }