"""
Prediction Service
Loads all three trained ML models at startup and exposes prediction functions.
"""

import os
import joblib
import pandas as pd

from backend.utils.employees import EMPLOYEES

# ------------------------------------------------------------------
# Resolve paths relative to this file
# ------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, "..", "ml_models")

# ------------------------------------------------------------------
# Load models once at import time
# ------------------------------------------------------------------
print("[SmartShift AI] Loading ML models...")

team_size_model = joblib.load(os.path.join(MODELS_DIR, "team_size_model.pkl"))
print("  OK: team_size_model loaded")

task_duration_model = joblib.load(os.path.join(MODELS_DIR, "task_duration_model.pkl"))
print("  OK: task_duration_model loaded")

employee_rec_model = joblib.load(os.path.join(MODELS_DIR, "employee_recommendation_model.pkl"))
print("  OK: employee_recommendation_model loaded")

print("[SmartShift AI] All models ready.\n")


# ------------------------------------------------------------------
# Skill -> Task type mapping
# Determines which employee skills are RELEVANT for each task type.
# skill_match = 1  means the employee's skill matches the task.
# skill_match = 0  means they don't.
# ------------------------------------------------------------------
TASK_SKILL_MAP = {
    "Backend Development":   {"Backend Development", "DevOps", "Quality Assurance"},
    "Frontend Development":  {"Frontend Development", "Quality Assurance"},
    "Machine Learning":      {"Machine Learning", "Data Science"},
    "Data Science":          {"Data Science", "Machine Learning"},
    "DevOps":                {"DevOps", "Backend Development", "Quality Assurance"},
    "Customer Service":      {"Customer Service", "Human Resources"},
    "Operations Management": {"Operations Management", "Project Management"},
    "Security Management":   {"Security Management"},
    "Human Resources":       {"Human Resources", "Customer Service"},
    "Finance":               {"Finance"},
    "Quality Assurance":     {"Quality Assurance", "Backend Development", "Frontend Development"},
    "Project Management":    {"Project Management", "Operations Management"},
}


def _compute_skill_match(employee_primary_skill: str, task_type: str) -> int:
    """Return 1 if the employee's primary skill is relevant for task_type, else 0."""
    relevant = TASK_SKILL_MAP.get(task_type, set())
    return 1 if employee_primary_skill in relevant else 0


# ------------------------------------------------------------------
# Prediction functions
# ------------------------------------------------------------------

def predict_team_size(task_type: str, task_description: str,
                      task_priority: str, task_complexity_score: float) -> int:
    df = pd.DataFrame([{
        "task_type": task_type,
        "task_description": task_description,
        "task_priority": task_priority,
        "task_complexity_score": float(task_complexity_score),
    }])
    result = team_size_model.predict(df)
    return max(1, round(float(result[0])))


def predict_duration(task_type: str, task_description: str,
                     task_priority: str, task_complexity_score: float,
                     team_size: int) -> int:
    complexity_per_person = float(task_complexity_score) / max(1, team_size)
    df = pd.DataFrame([{
        "task_type": task_type,
        "task_description": task_description,
        "task_priority": task_priority,
        "task_complexity_score": float(task_complexity_score),
        "team_size": team_size,
        "complexity_per_person": complexity_per_person,
    }])
    result = task_duration_model.predict(df)
    return max(1, round(float(result[0])))


def recommend_employees(task_type: str, task_description: str,
                        task_priority: str, task_complexity_score: float,
                        team_size: int) -> list:
    """
    Rank all employees for the given task and return the top `team_size`.

    Strategy (two fixes applied):
    1. skill_match is computed DYNAMICALLY per employee from TASK_SKILL_MAP,
       not read from a static field.
    2. TIERED SORT: employees whose skill matches the task_type always rank
       ABOVE non-matching employees, regardless of raw model probability.
       Within each tier we sort by model probability descending.
       This guarantees task-relevant employees are always shown first.
    """
    rows = []
    skill_matches = []

    for emp in EMPLOYEES:
        sm = _compute_skill_match(emp["employee_primary_skill"], task_type)
        skill_matches.append(sm)
        rows.append({
            "task_description": task_description,
            "task_priority": task_priority,
            "task_complexity_score": float(task_complexity_score),
            "employee_primary_skill": emp["employee_primary_skill"],
            "skill_level": emp["skill_level"],
            "experience_years": emp["experience_years"],
            "is_intern": emp["is_intern"],
            "skill_match": sm,                          # dynamic
            "employee_performance_score": emp["employee_performance_score"],
            "employee_availability_score": emp["employee_availability_score"],
        })

    df = pd.DataFrame(rows)
    # predict_proba gives continuous ranking within each skill tier
    probas = employee_rec_model.predict_proba(df)[:, 1]

    scored = []
    for i, emp in enumerate(EMPLOYEES):
        scored.append({
            "name": emp["name"],
            "id": emp["id"],
            "primary_skill": emp["employee_primary_skill"],
            "skill_level": emp["skill_level"],
            "experience_years": emp["experience_years"],
            "performance_score": emp["employee_performance_score"],
            "availability_score": emp["employee_availability_score"],
            "skill_match": skill_matches[i],
            "match_probability": round(float(probas[i]) * 100, 1),
        })

    # TIERED SORT: skill-matched employees always come first.
    # Within each tier, best model probability wins.
    matched   = sorted([e for e in scored if e["skill_match"] == 1],
                        key=lambda x: x["match_probability"], reverse=True)
    unmatched = sorted([e for e in scored if e["skill_match"] == 0],
                        key=lambda x: x["match_probability"], reverse=True)

    ordered = matched + unmatched
    return ordered[:team_size]
