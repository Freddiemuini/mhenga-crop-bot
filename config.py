import os
from datetime import timedelta

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Base configuration"""
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        f"sqlite:///{os.path.join(BASE_DIR, 'users.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT Configuration
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "super-secret-key")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)

    # Mail Configuration (override via env vars in production)
    MAIL_SERVER = os.environ.get("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.environ.get("MAIL_PORT", 587))
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", "True") in ["True", "true", "1"]
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME", "freddymuini@gmail.com")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD", "vvkenhdxprvvqfwm")
    MAIL_DEFAULT_SENDER = (
        os.environ.get("MAIL_SENDER_NAME", "AgriBot"),
        os.environ.get("MAIL_SENDER_EMAIL", "freddymuini@gmail.com")
    )


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
}

# API Keys (set these as environment variables in Render)
AGROMONITORING_API_KEY = os.environ.get("AGROMONITORING_API_KEY", "4f84c6035c447f4c14faf4ac0f2f1a06")
ROBOFLOW_API_KEY = os.environ.get("ROBOFLOW_API_KEY", "ctkt12G5XN3jQUlLIiIk")
ROBOFLOW_MODEL_ID = os.environ.get("ROBOFLOW_MODEL_ID", "crop-disease-2rilx")
ROBOFLOW_MODEL_VERSION = os.environ.get("ROBOFLOW_MODEL_VERSION", "4")
