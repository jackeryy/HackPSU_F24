import firebase_admin
from firebase_admin import credentials, firestore
import pyrebase
import os

# Initialize Firebase Admin SDK for Firestore
def initialize_firebase():
    # Path to your Firebase Admin SDK service account key JSON file
    cred = credentials.Certificate('instance/serviceAccountKey.json')  # Replace with the path to your service account key file
    firebase_admin.initialize_app(cred)  # Initialize Firebase Admin SDK
    return firestore.client()  # Return Firestore client for database operations

# Initialize Pyrebase for Authentication (Firebase client-side SDK)
def initialize_pyrebase():
    # Configuration for Firebase project
    firebase_config = {
        "apiKey": os.getenv('FIREBASE_API_KEY'),               # Your Firebase project's API key
        "authDomain": os.getenv('FIREBASE_AUTH_DOMAIN'),       # Firebase Auth domain
        "projectId": os.getenv('FIREBASE_PROJECT_ID'),         # Firebase project ID
        "storageBucket": os.getenv('FIREBASE_STORAGE_BUCKET'), # Firebase Storage bucket
        "messagingSenderId": os.getenv('FIREBASE_MESSAGING_SENDER_ID'), # Messaging sender ID
        "appId": os.getenv('FIREBASE_APP_ID'),                 # Firebase App ID
        "databaseURL": ""
    }
    
    # Initialize Pyrebase app for Firebase client SDK functionality
    firebase = pyrebase.initialize_app(firebase_config)
    
    # Return the authentication service to handle email/password sign-in
    return firebase.auth()
