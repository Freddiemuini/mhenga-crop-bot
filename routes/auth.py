from flask import Blueprint, request, jsonify, url_for
from models import db, User
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature

auth_bp = Blueprint('auth', __name__)


def init_auth_routes(app, mail, serializer):
    """Initialize authentication routes with app and mail context"""
    
    @auth_bp.route('/signup', methods=['POST'])
    def signup():
        data = request.get_json()
        name = data.get("name")
        email = data.get("email")
        password = data.get("password")

        if not name or not email or not password:
            return jsonify({"error": "All fields (name, email, password) are required"}), 400

        if User.query.filter_by(email=email.lower()).first():
            return jsonify({"error": "User already exists"}), 400

        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")

        new_user = User(
            name=name,
            email=email.lower(),
            password=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()

        try:
            msg = Message(
                subject="Welcome to AgriBot 🌱",
                recipients=[email],
                body=f"Hello {name},\n\n"
                     f"Welcome to AgriBot! 🎉\n\n"
                     "You can now log in and start identifying crop diseases, "
                     "getting prevention tips, and weather insights.\n\n"
                     "Happy Farming!\n\n- AgriBot Team"
            )
            mail.send(msg)
        except Exception as e:
            print("Email sending failed:", str(e))
            return jsonify({"message": "Signup successful, but email sending failed."}), 201

        return jsonify({"message": "Signup successful, welcome email sent!"}), 201

    @auth_bp.route('/login', methods=['POST'])
    def login():
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400

        user = User.query.filter_by(email=email.lower()).first()
        if not user or not check_password_hash(user.password, password):
            return jsonify({"error": "Invalid email or password"}), 401

        access_token = create_access_token(identity=user.email)
        return jsonify({
            "message": "Login successful",
            "access_token": access_token,
            "user": {"name": user.name, "email": user.email}
        }), 200

    @auth_bp.route('/reset-password-request', methods=['POST'])
    def reset_password_request():
        data = request.get_json()
        email = data.get("email")

        if not email:
            return jsonify({"error": "Email is required"}), 400

        user = User.query.filter_by(email=email.lower()).first()
        if not user:
            return jsonify({"error": "No account found with this email"}), 404

        token = serializer.dumps(email.lower(), salt="password-reset-salt")
        reset_link = url_for('auth.reset_password_confirm', token=token, _external=True)

        try:
            msg = Message(
                subject="AgriBot Password Reset 🔑",
                recipients=[email],
                body=f"Hello {user.name},\n\n"
                     f"We received a request to reset your password.\n\n"
                     f"Click the link below to reset it:\n{reset_link}\n\n"
                     f"This link is valid for 30 minutes.\n\n"
                     f"If you didn't request this, you can ignore this email."
            )
            mail.send(msg)
        except Exception as e:
            print("Password reset email failed:", str(e))
            return jsonify({"error": "Failed to send reset email"}), 500

        return jsonify({"message": "Password reset link sent to your email."}), 200

    @auth_bp.route('/reset-password-confirm/<token>', methods=['POST'])
    def reset_password_confirm(token):
        try:
            email = serializer.loads(token, salt="password-reset-salt", max_age=1800)
        except SignatureExpired:
            return jsonify({"error": "The reset link has expired"}), 400
        except BadSignature:
            return jsonify({"error": "Invalid reset link"}), 400

        data = request.get_json()
        new_password = data.get("new_password")

        if not new_password:
            return jsonify({"error": "New password is required"}), 400

        user = User.query.filter_by(email=email.lower()).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        user.password = generate_password_hash(new_password, method="pbkdf2:sha256")
        db.session.commit()

        return jsonify({"message": "Password has been reset successfully"}), 200

    return auth_bp
