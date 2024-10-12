# app/__init__.py

from flask import Flask
from app.utils.firebase import initialize_firebase, initialize_firestore
from dotenv import load_dotenv
import os

def create_app():
    # Load environment variables from .env
    load_dotenv()

    app = Flask(__name__)

    # Set Flask configuration (SECRET_KEY is loaded from .env)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    # Initialize Firebase Authentication and Firestore
    app.firebase_auth = initialize_firebase()
    app.firestore_db = initialize_firestore()

    return app
