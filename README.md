# SmartShift AI — Workforce Optimization System

> AI-powered workforce planning: predict team size, task duration, and get employee recommendations in one click.

---

## Project Structure

```
SmartShiftAI/
├── frontend/
│   ├── index.html                  ← Login / role selection page
│   ├── dashboard-admin.html        ← Admin dashboard (with AI Prediction panel)
│   └── dashboard-worker.html       ← Worker dashboard
│
├── ml_models/
│   ├── team_size_model.pkl
│   ├── task_duration_model.pkl
│   └── employee_recommendation_model.pkl
│
├── datasets/                       ← Training datasets (CSV files)
│
├── training/                       ← Model training scripts
│   ├── train_team_size.py
│   ├── train_duration.py
│   └── train_employee_recommendation.py
│
├── backend/
│   ├── app.py                      ← Flask entry point (port 8080)
│   ├── routes/
│   │   └── predict.py              ← API endpoints
│   ├── services/
│   │   └── prediction_service.py   ← Model loading + prediction logic
│   └── utils/
│       └── employees.py            ← Mock employee pool
│
└── requirements.txt
```

---

## Quickstart

### 1. Install Python dependencies

```powershell
pip install -r requirements.txt
```

### 2. Start the Flask backend

```powershell
cd backend
python app.py
```

Expected output:
```
=======================================================
  SmartShift AI Backend
  Running on: http://localhost:8080
=======================================================
[SmartShift AI] Loading ML models...
  ✔ team_size_model loaded
  ✔ task_duration_model loaded
  ✔ employee_recommendation_model loaded
```

### 3. Open the frontend

Open `frontend/index.html` in your browser (double-click or drag into Chrome/Edge).

### 4. Demo flow

1. Select **Admin** on the role selection page
2. Enter any email + any access code (e.g. `ADM-2024-001`)
3. Click **Sign In as Admin →**
4. On the dashboard, scroll down to the **🤖 AI Task Prediction** panel
5. Fill in task details and click **🚀 Run AI Prediction**
6. Results appear: **Recommended Team Size**, **Estimated Duration**, **Recommended Employees**

---

## API Reference

Base URL: `http://localhost:8080`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/predict_team_size` | Predict team size only |
| POST | `/predict_duration` | Predict task duration only |
| POST | `/recommend_employees` | Recommend employees only |
| POST | `/predict_task` | **Full pipeline** (all 3 models) |

### POST /predict_task — Request Body

```json
{
  "task_type": "Backend Development",
  "task_description": "Build a REST API for payment processing",
  "task_priority": "High",
  "task_complexity_score": 7
}
```

### POST /predict_task — Response

```json
{
  "team_size": 4,
  "task_duration_days": 2,
  "recommended_employees": [
    {
      "name": "Neha Sharma",
      "id": "EMP-009",
      "primary_skill": "Machine Learning",
      "experience_years": 4,
      "performance_score": 4.7,
      "match_probability": 89.5
    }
  ]
}
```

---

## Machine Learning Models

| Model | Algorithm | Target |
|-------|-----------|--------|
| `team_size_model.pkl` | Random Forest Regressor | `team_size` |
| `task_duration_model.pkl` | Random Forest Regressor | `task_duration_days` |
| `employee_recommendation_model.pkl` | Random Forest Classifier | `high_contributor` (0/1) |

All models use sklearn pipelines with TF-IDF for text, OneHotEncoder for categories, and StandardScaler for numerics.
