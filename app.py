from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from itsdangerous import URLSafeTimedSerializer
import logging
from config import config, Config
from models import db
from routes.auth import init_auth_routes
from routes.analyze import analyze_bp

def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config.get(config_name, config['development']))
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    CORS(app)
    db.init_app(app)
    JWTManager(app)
    mail = Mail(app)
    serializer = URLSafeTimedSerializer(app.config['JWT_SECRET_KEY'])
    with app.app_context():
        db.create_all()
    auth_bp = init_auth_routes(app, mail, serializer)
    app.register_blueprint(auth_bp)
    app.register_blueprint(analyze_bp)

    @app.route('/')
    def home():
        return (jsonify({'message': 'Crop Bot API with Auth, JWT, Email, Weather & Roboflow AI is running!', 'version': '2.0'}), 200)
    return app
app = create_app('production')
if __name__ == '__main__':
    app.run(debug=True)