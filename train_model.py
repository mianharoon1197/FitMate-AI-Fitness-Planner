import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib

# Load dataset
df = pd.read_csv("fitness_plan_dataset.csv")

# Encode categorical columns
label_encoders = {}
categorical_columns = [
    "Gender", "Activity_Level", "Activity_Type", "Work_Type",
    "Diet", "Allergies", "Health_Condition", "Fitness_Goal"
]

for col in categorical_columns:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

# Features and targets
X = df.drop(columns=["Calories_Intake", "Protein_Intake", "Recommended_Exercises", "Recommended_Sleep", "Exercise_Duration"])
y = df[["Calories_Intake", "Protein_Intake", "Exercise_Duration"]]

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save model and encoders
joblib.dump(model, "fitness_model.pkl")
joblib.dump(label_encoders, "label_encoders.pkl")

print("✅ Model and encoders saved successfully!")
