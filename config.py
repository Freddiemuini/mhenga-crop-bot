import os
from datetime import timedelta
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', f"sqlite:///{os.path.join(BASE_DIR, 'users.db')}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'super-secret-key')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True').lower() in ['true', '1', 'yes']
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', 'freddymuini@gmail.com')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', 'vvkenhdxprvvqfwm')
    MAIL_DEFAULT_SENDER = (os.getenv('MAIL_SENDER_NAME', 'AgriBot'), os.getenv('MAIL_SENDER_EMAIL', 'freddymuini@gmail.com'))

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
config = {'development': DevelopmentConfig, 'production': ProductionConfig, 'default': DevelopmentConfig}
AGROMONITORING_API_KEY = '4f84c6035c447f4c14faf4ac0f2f1a06'
ROBOFLOW_API_KEY = 'ctkt12G5XN3jQUlLIiIk'
ROBOFLOW_MODEL_ID = 'crop-disease-2rilx'
ROBOFLOW_MODEL_VERSION = '4'