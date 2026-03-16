import os
from datetime import timedelta

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'users.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    JWT_SECRET_KEY = "super-secret-key"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "freddymuini@gmail.com"
    MAIL_PASSWORD = "vvkenhdxprvvqfwm"
    MAIL_DEFAULT_SENDER = ("AgriBot", "freddymuini@gmail.com")


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
}

AGROMONITORING_API_KEY = "4f84c6035c447f4c14faf4ac0f2f1a06"
ROBOFLOW_API_KEY = "ctkt12G5XN3jQUlLIiIk"
ROBOFLOW_MODEL_ID = "crop-disease-2rilx"
ROBOFLOW_MODEL_VERSION = "4"
