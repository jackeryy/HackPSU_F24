# app/routes/auth.py

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from app import create_app, User

app = create_app()

auth_blueprint = Blueprint('auth', __name__)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User model for Flask-Login
class User(UserMixin):
    def __init__(self, user_id, username, email):
        self.id = user_id
        self.username = username
        self.email = email

# Load user function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    user_doc = app.firestore_db.collection('users').document(user_id).get()
    if user_doc.exists:
        user_data = user_doc.to_dict()
        return User(user_id, user_data['username'], user_data['email'])
    return None

# Registration form
class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=30)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=30)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

# Login form
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

# Home route (requires login)
@app.route('/')
@login_required
def home():
    return render_template('home.html', name=current_user.username)

# Registration route
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        password = form.password.data

        try:
            # Create the user with Firebase Authentication
            user = app.firebase_auth.create_user_with_email_and_password(email, password)
            user_id = user['localId']

            # Store user profile in Firestore
            app.firestore_db.collection('users').document(user_id).set({
                'first_name': first_name,
                'last_name': last_name,
                'email': email
            })

            flash('Registration successful. You can now log in.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            flash(f'Registration failed: {e}', 'danger')

    return render_template('register.html', form=form)

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        try:
            # Authenticate user with Firebase
            user = app.firebase_auth.sign_in_with_email_and_password(email, password)
            user_id = user['localId']

            # Retrieve user info from Firestore
            user_doc = app.firestore_db.collection('users').document(user_id).get()
            if user_doc.exists:
                user_data = user_doc.to_dict()
                login_user(User(user_id, user_data['username'], user_data['email']))
                return redirect(url_for('home'))
        except Exception as e:
            flash(f'Login failed: {e}', 'danger')

    return render_template('login.html', form=form)

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))
