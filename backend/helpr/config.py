"""Configuration for the app. Loads database from Env vars."""
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://" + os.environ['DATABASE']
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY") if os.environ.get("SECRET_KEY") is not None else "development secret key"
