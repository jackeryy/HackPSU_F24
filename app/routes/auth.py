# /app/routes/auth.py

from flask import Blueprint, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_login import login_user, logout_user, login_required
from app import User, create_app

app = create_app()

auth_blueprint = Blueprint('auth', __name__)

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

# Registration route
@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        password = form.password.data

        try:
            # Register user with Firebase Authentication
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
@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        try:
            # Authenticate user with Firebase
            user = app.firebase_auth.sign_in_with_email_and_password(email, password)
            user_id = user['localId']

            # Retrieve user profile from Firestore
            user_doc = app.firestore_db.collection('users').document(user_id).get()
            if user_doc.exists:
                user_data = user_doc.to_dict()
                login_user(User(user_id, user_data['first_name'], user_data['last_name'], user_data['email']))
                return redirect(url_for('home'))
        except Exception as e:
            flash(f'Login failed: {e}', 'danger')

    return render_template('login.html', form=form)

# Logout route
@auth_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
