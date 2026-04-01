import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report


# --------------------------------------------------
# LOAD DATASET
# --------------------------------------------------

data_path = "../dataset/dataset_employee_recommendation_model.csv"

df = pd.read_csv(data_path)

print("Dataset shape:", df.shape)
print(df.head())


# --------------------------------------------------
# FEATURES / TARGET
# --------------------------------------------------

X = df[
    [
        "task_description",
        "task_priority",
        "task_complexity_score",
        "employee_primary_skill",
        "skill_level",
        "experience_years",
        "is_intern",
        "skill_match",
        "employee_performance_score",
        "employee_availability_score"
    ]
]

y = df["high_contributor"]


# --------------------------------------------------
# TRAIN TEST SPLIT
# --------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("Training samples:", len(X_train))
print("Testing samples:", len(X_test))


# --------------------------------------------------
# FEATURE PIPELINE
# --------------------------------------------------

categorical_features = [
    "task_priority",
    "employee_primary_skill"
]

numeric_features = [
    "task_complexity_score",
    "skill_level",
    "experience_years",
    "is_intern",
    "skill_match",
    "employee_performance_score",
    "employee_availability_score"
]

text_feature = "task_description"


preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),

        ("num", StandardScaler(), numeric_features),

        ("text", TfidfVectorizer(max_features=300), text_feature),
    ]
)


# --------------------------------------------------
# MODEL PIPELINE
# --------------------------------------------------

model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),

        ("classifier", RandomForestClassifier(
            n_estimators=300,
            max_depth=14,
            random_state=42
        ))
    ]
)


# --------------------------------------------------
# TRAIN MODEL
# --------------------------------------------------

print("\nTraining Employee Recommendation model...")

model.fit(X_train, y_train)

print("Training complete")


# --------------------------------------------------
# EVALUATION
# --------------------------------------------------

predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print("\nModel Evaluation")
print("---------------------")
print("Accuracy:", accuracy)

print("\nClassification Report")
print(classification_report(y_test, predictions))


# --------------------------------------------------
# SAVE MODEL
# --------------------------------------------------

model_path = "../models/employee_recommendation_model.pkl"

joblib.dump(model, model_path)

print("\nEmployee Recommendation model saved successfully at:", model_path)


# --------------------------------------------------
# EXAMPLE PREDICTION
# --------------------------------------------------

sample_employee = pd.DataFrame({

    "task_description": [
        "Develop scalable backend API service for payment processing"
    ],

    "task_priority": ["High"],

    "task_complexity_score": [7],

    "employee_primary_skill": ["Backend Development"],

    "skill_level": [4],

    "experience_years": [5],

    "is_intern": [0],

    "skill_match": [1],

    "employee_performance_score": [4.2],

    "employee_availability_score": [0.8]
})

prediction = model.predict(sample_employee)

print("\nExample Prediction")
print("---------------------")

if prediction[0] == 1:
    print("Employee is a GOOD candidate for this task")
else:
    print("Employee is NOT ideal for this task")