# app/utils/firebase.py

import pyrebase
import firebase_admin
from firebase_admin import credentials, firestore
import os

# Initialize Firebase Authentication
def initialize_firebase():
    firebase_config = {
        "apiKey": os.getenv('FIREBASE_API_KEY'),
        "authDomain": os.getenv('FIREBASE_AUTH_DOMAIN'),
        "projectId": os.getenv('FIREBASE_PROJECT_ID'),
        "storageBucket": os.getenv('FIREBASE_STORAGE_BUCKET'),
        "messagingSenderId": os.getenv('FIREBASE_MESSAGING_SENDER_ID'),
        "appId": os.getenv('FIREBASE_APP_ID'),
        "measurementId": os.getenv('FIREBASE_MEASUREMENT_ID')
    }
    firebase = pyrebase.initialize_app(firebase_config)
    return firebase.auth()

# Initialize Firestore for user data storage
def initialize_firestore():
    cred = credentials.Certificate('path/to/serviceAccountKey.json')
    firebase_admin.initialize_app(cred)
    return firestore.client()
