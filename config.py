
import os

class Config:
    API_TITLE = "Expenses API — Lab 3"
    API_VERSION = "1.0.0"
    OPENAPI_VERSION = "3.0.3"
    PROPAGATE_EXCEPTIONS = True
    JSON_SORT_KEYS = False

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "postgresql+psycopg2://postgres:postgres@localhost:5432/expenses")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # For flask-smorest error formatting
    # (leave SECRET_KEY optional for now)
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret")
