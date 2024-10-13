from flask import Flask
from dotenv import load_dotenv
import os
from app.utils.firebase import initialize_firebase, initialize_pyrebase
from flask_login import LoginManager, UserMixin

class User(UserMixin):
    def __init__(self, user_id, first_name, last_name, email):
        self.id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    # Initialize Firestore (Firebase Admin SDK handles both Firestore and Authentication globally)
    app.firestore_db = initialize_firebase()  # Use Firebase Admin SDK for Firestore

    # Initialize Pyrebase Auth (for email/password authentication)
    app.firebase_auth = initialize_pyrebase()  # Use Pyrebase for client-side login

    # Flask-Login setup
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        # Fetch user from Firestore by ID
        user_doc = app.firestore_db.collection('users').document(user_id).get()
        if user_doc.exists:
            user_data = user_doc.to_dict()
            return User(user_id, user_data['first_name'], user_data['last_name'], user_data['email'])
        return None

    # Register blueprints
    from app.routes.auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app