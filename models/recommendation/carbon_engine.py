class CarbonCreditEstimator:
    def __init__(self, csv_path: str = "datasets/tree_species_10000.csv"):
        self.csv_path = csv_path

    def estimate_carbon_credits(self, tree_name: str, tree_count: int = 1000, survival_percentage: float = 85.0, project_years: int = 10) -> dict:
        effective_trees = tree_count * (survival_percentage / 100.0)
        co2_tons = round((effective_trees * 22.0 * project_years) / 1000.0, 2)
        credits = round(co2_tons, 2)

        return {
            "tree_name": tree_name,
            "total_co2_absorbed_tons": co2_tons,
            "carbon_credits": credits
        }