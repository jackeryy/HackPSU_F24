# /app/__init__.py

from flask import Flask
from app.utils.firebase import initialize_firebase, initialize_firestore
from flask_login import LoginManager

def create_app():
    app = Flask(__name__)

    # Load configuration and initialize Firebase
    app.config['SECRET_KEY'] = 'your-secret-key'  # You can load from a config file or .env

    # Initialize Firebase
    app.firebase_auth = initialize_firebase()
    app.firestore_db = initialize_firestore()

    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    # Import and register blueprints here
    from app.routes.auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app
