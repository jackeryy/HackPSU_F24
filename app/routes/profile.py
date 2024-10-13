from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app  # Import current_app from flask
from flask_login import login_required, current_user
from app import User

profile_blueprint = Blueprint('profile', __name__)

# Route to view and edit user profile
@profile_blueprint.route('/profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        # Collect form data
        height = request.form.get('height')
        weight = request.form.get('weight')
        age = request.form.get('age')
        allergies = request.form.get('allergies')
        health_conditions = request.form.get('health_conditions')

        # Update user profile in Firestore
        current_app.firestore_db.collection('users').document(current_user.id).update({
            'height': height,
            'weight': weight,
            'age': age,
            'allergies': allergies,
            'health_conditions': health_conditions
        })

        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile.edit_profile'))

    # GET request: Fetch the user's profile data
    user_doc = current_app.firestore_db.collection('users').document(current_user.id).get()
    user_data = user_doc.to_dict()

    # Render the profile template with user data
    return render_template('profile.html', user=user_data)
