import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score


# --------------------------------------------------
# LOAD DATASET
# --------------------------------------------------

data_path = "../dataset/dataset_task_duration_model.csv"

df = pd.read_csv(data_path)

print("Dataset shape:", df.shape)
print(df.head())


# --------------------------------------------------
# FEATURE ENGINEERING
# --------------------------------------------------

# workload per employee
df["complexity_per_person"] = (
    df["task_complexity_score"] / df["team_size"]
)


# --------------------------------------------------
# FEATURES / TARGET
# --------------------------------------------------

X = df[
    [
        "task_type",
        "task_description",
        "task_priority",
        "task_complexity_score",
        "team_size",
        "complexity_per_person"
    ]
]

y = df["task_duration_days"]


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

categorical_features = ["task_type", "task_priority"]

numeric_features = [
    "task_complexity_score",
    "team_size",
    "complexity_per_person"
]

text_feature = "task_description"


preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),

        ("num", StandardScaler(), numeric_features),

        ("text", TfidfVectorizer(max_features=200), text_feature),
    ]
)


# --------------------------------------------------
# MODEL PIPELINE
# --------------------------------------------------

model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),

        ("regressor", RandomForestRegressor(
            n_estimators=300,
            max_depth=14,
            random_state=42
        ))
    ]
)


# --------------------------------------------------
# TRAIN MODEL
# --------------------------------------------------

print("\nTraining Task Duration model...")

model.fit(X_train, y_train)

print("Training complete")


# --------------------------------------------------
# EVALUATION
# --------------------------------------------------

predictions = model.predict(X_test)

mae = mean_absolute_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

print("\nModel Evaluation")
print("---------------------")
print("MAE:", mae)
print("R2 Score:", r2)


# --------------------------------------------------
# SAVE MODEL
# --------------------------------------------------

model_path = "../models/task_duration_model.pkl"

joblib.dump(model, model_path)

print("\nTask Duration model saved successfully at:", model_path)


# --------------------------------------------------
# EXAMPLE PREDICTION
# --------------------------------------------------

sample_task = pd.DataFrame({

    "task_type": ["Backend Development"],

    "task_description": [
        "Design scalable microservice architecture for payment processing with secure APIs and logging systems"
    ],

    "task_priority": ["High"],

    "task_complexity_score": [8],

    "team_size": [4],

    "complexity_per_person": [8/4]
})

prediction = model.predict(sample_task)

print("\nExample Prediction")
print("---------------------")

print("Predicted task duration:", round(prediction[0]), "days")