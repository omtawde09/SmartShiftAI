"""
Prediction Routes Blueprint
Registers all /predict_* API endpoints.
"""

from flask import Blueprint, request, jsonify
from backend.services.prediction_service import (
    predict_team_size,
    predict_duration,
    recommend_employees,
)

predict_bp = Blueprint("predict", __name__)


def bad_request(msg: str):
    return jsonify({"error": msg}), 400


# ------------------------------------------------------------------
# POST /predict_team_size
# ------------------------------------------------------------------
@predict_bp.route("/predict_team_size", methods=["POST"])
def api_predict_team_size():
    data = request.get_json(silent=True) or {}

    task_type = data.get("task_type", "")
    task_description = data.get("task_description", "")
    task_priority = data.get("task_priority", "Medium")
    task_complexity_score = data.get("task_complexity_score", 5)

    if not task_description:
        return bad_request("task_description is required")

    team_size = predict_team_size(
        task_type, task_description, task_priority, task_complexity_score
    )
    return jsonify({"team_size": team_size})


# ------------------------------------------------------------------
# POST /predict_duration
# ------------------------------------------------------------------
@predict_bp.route("/predict_duration", methods=["POST"])
def api_predict_duration():
    data = request.get_json(silent=True) or {}

    task_type = data.get("task_type", "")
    task_description = data.get("task_description", "")
    task_priority = data.get("task_priority", "Medium")
    task_complexity_score = data.get("task_complexity_score", 5)
    team_size = data.get("team_size", 3)

    if not task_description:
        return bad_request("task_description is required")

    duration = predict_duration(
        task_type, task_description, task_priority, task_complexity_score, team_size
    )
    return jsonify({"task_duration_days": duration})


# ------------------------------------------------------------------
# POST /recommend_employees
# ------------------------------------------------------------------
@predict_bp.route("/recommend_employees", methods=["POST"])
def api_recommend_employees():
    data = request.get_json(silent=True) or {}

    task_type = data.get("task_type", "")            # ← now required
    task_description = data.get("task_description", "")
    task_priority = data.get("task_priority", "Medium")
    task_complexity_score = data.get("task_complexity_score", 5)
    team_size = data.get("team_size", 3)

    if not task_description:
        return bad_request("task_description is required")

    employees = recommend_employees(
        task_type, task_description, task_priority, task_complexity_score, team_size
    )
    return jsonify({"recommended_employees": employees})


# ------------------------------------------------------------------
# POST /predict_task  — Full Pipeline
# ------------------------------------------------------------------
@predict_bp.route("/predict_task", methods=["POST"])
def api_predict_task():
    """
    Full AI pipeline:
    1. Predict team size
    2. Predict task duration
    3. Recommend top employees (task-aware, dynamic skill_match)
    Returns all three results in one response.
    """
    data = request.get_json(silent=True) or {}

    task_type = data.get("task_type", "")
    task_description = data.get("task_description", "")
    task_priority = data.get("task_priority", "Medium")
    task_complexity_score = data.get("task_complexity_score", 5)

    if not task_description:
        return bad_request("task_description is required")

    # Step 1: Team size
    team_size = predict_team_size(
        task_type, task_description, task_priority, task_complexity_score
    )

    # Step 2: Duration (uses predicted team_size)
    duration = predict_duration(
        task_type, task_description, task_priority, task_complexity_score, team_size
    )

    # Step 3: Recommend employees — now passes task_type for dynamic skill_match
    employees = recommend_employees(
        task_type, task_description, task_priority, task_complexity_score, team_size
    )

    return jsonify({
        "team_size": team_size,
        "task_duration_days": duration,
        "recommended_employees": employees,
    })


# ------------------------------------------------------------------
# GET /health
# ------------------------------------------------------------------
@predict_bp.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "SmartShift AI Backend"})
