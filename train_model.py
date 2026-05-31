import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load dataset
df = pd.read_csv("data/diabetes.csv")

# Keep only relevant columns
df = df[["stab.glu", "glyhb", "chol"]]

# Remove missing values
df = df.dropna()

# Create risk labels
def create_risk(row):

    if row["stab.glu"] > 140 or row["chol"] > 240:
        return "High Risk"

    elif row["stab.glu"] > 100 or row["chol"] > 200:
        return "Medium Risk"

    else:
        return "Low Risk"

df["Risk"] = df.apply(create_risk, axis=1)

# Features
X = df[["stab.glu", "glyhb", "chol"]]

# Target
y = df["Risk"]

# Train model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X, y)

# Save model
joblib.dump(model, "health_model.pkl")

print("Model Trained Successfully")