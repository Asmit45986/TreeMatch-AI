import os
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, mean_squared_error

# Paths setup
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_PATH = os.path.join(BASE_DIR, "datasets", "corrected_afforestation_dataset.csv")
CHECKPOINTS_DIR = os.path.join(BASE_DIR, "checkpoints")

os.makedirs(CHECKPOINTS_DIR, exist_ok=True)

print("📖 Loading dataset...")
df = pd.read_csv(DATASET_PATH)

# Categorical and Numerical feature separation
categorical_features = ['Land_Type', 'Soil_Type']
numeric_features = [col for col in df.columns if col not in categorical_features + ['Image_ID', 'Best_Tree', 'Survival_Probability']]

# Preprocessor for Encoding categorical variables (Soil_Type, Land_Type)
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ],
    remainder='passthrough'
)

# -------------------------------------------------------------
# 1. Train Tree Recommender Model (Classifier)
# -------------------------------------------------------------
print("\n🌲 Training Tree Recommender Model...")
X_clf = df[categorical_features + numeric_features]
y_clf = df['Best_Tree']

X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(X_clf, y_clf, test_size=0.2, random_state=42)

clf_pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
])

clf_pipeline.fit(X_train_c, y_train_c)
y_pred_c = clf_pipeline.predict(X_test_c)
acc = accuracy_score(y_test_c, y_pred_c)
print(f"✅ Tree Recommender Accuracy: {acc * 100:.2f}%")

# Save Classifier Checkpoint
clf_path = os.path.join(CHECKPOINTS_DIR, "tree_recommender.pkl")
joblib.dump(clf_pipeline, clf_path)
print(f"💾 Saved Classifier model at: {clf_path}")

# -------------------------------------------------------------
# 2. Train Survival Rate Regressor Model (Regressor)
# -------------------------------------------------------------
print("\n📊 Training Survival Rate Regressor Model...")
X_reg = df[categorical_features + numeric_features]
y_reg = df['Survival_Probability']

X_train_r, X_test_r, y_train_r, y_test_r = train_test_split(X_reg, y_reg, test_size=0.2, random_state=42)

reg_pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
])

reg_pipeline.fit(X_train_r, y_train_r)
y_pred_r = reg_pipeline.predict(X_test_r)
mse = mean_squared_error(y_test_r, y_pred_r)
print(f"✅ Survival Regressor Mean Squared Error (MSE): {mse:.4f}")

# Save Regressor Checkpoint
reg_path = os.path.join(CHECKPOINTS_DIR, "survival_regressor.pkl")
joblib.dump(reg_pipeline, reg_path)
print(f"💾 Saved Regressor model at: {reg_path}")

print("\n🎉 ML Model Training Completed Successfully!")