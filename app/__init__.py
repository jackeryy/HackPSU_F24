# /app/__init__.py

from flask import Flask
from dotenv import load_dotenv
import os
from app.utils.firebase import initialize_firebase, initialize_firestore
from flask_login import LoginManager, UserMixin

# Define a simple User model for Flask-Login
class User(UserMixin):
    def __init__(self, user_id, first_name, last_name, email):
        self.id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

# Factory function to create and configure the Flask app
def create_app():
    # Load environment variables from the .env file
    load_dotenv()

    # Initialize the Flask app
    app = Flask(__name__)

    # Set Flask configuration using SECRET_KEY from .env
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    # Initialize Firebase services (authentication and Firestore)
    app.firebase_auth = initialize_firebase()
    app.firestore_db = initialize_firestore()

    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # Redirect to login page if not logged in

    # Define the user loader function for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        # Fetch user data from Firestore
        user_doc = app.firestore_db.collection('users').document(user_id).get()
        if user_doc.exists:
            user_data = user_doc.to_dict()
            return User(user_id, user_data['first_name'], user_data['last_name'], user_data['email'])
        return None

    # Import and register the auth blueprint for authentication routes
    from app.routes.auth import auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app
