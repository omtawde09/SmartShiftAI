"""
SmartShift AI — Flask Application Entry Point
"""

import sys
import os

# Add project root to path so `backend.*` imports work
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask
from flask_cors import CORS
from backend.routes.predict import predict_bp


def create_app():
    app = Flask(__name__)
    CORS(app)  # Allow all origins for local dev / demo

    # Register prediction blueprint (all routes at root level)
    app.register_blueprint(predict_bp)

    return app


if __name__ == "__main__":
    app = create_app()
    print("=" * 55)
    print("  SmartShift AI Backend")
    print("  Running on: http://localhost:8080")
    print("=" * 55)
    app.run(host="0.0.0.0", port=8080, debug=True)
