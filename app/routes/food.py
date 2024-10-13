# /app/routes/food.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from datetime import datetime, timedelta

food_blueprint = Blueprint('food', __name__)

# Route to log food consumption and view past logs
@food_blueprint.route('/log_food', methods=['GET', 'POST'])
@login_required
def log_food():
    if request.method == 'POST':
        # Collect form data
        food_name = request.form.get('food')
        calories = request.form.get('calories')
        time = request.form.get('time')
        date = request.form.get('date')  # The date selected by the user

        # Save the food log in Firestore, grouped by date
        current_app.firestore_db.collection('food_logs').add({
            'user_id': current_user.id,
            'food_name': food_name,
            'calories': calories,
            'time': time,
            'date': date
        })

        flash('Food log added successfully!', 'success')
        return redirect(url_for('food.log_food'))

    # Retrieve the last 7 days of logs to display
    today = datetime.now()
    dates = [(today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]  # Last 7 days

    # Fetch logs for the last 7 days
    food_logs_by_day = {}
    for date in dates:
        food_logs_by_day[date] = current_app.firestore_db.collection('food_logs')\
            .where('user_id', '==', current_user.id)\
            .where('date', '==', date).stream()
        food_logs_by_day[date] = [log.to_dict() for log in food_logs_by_day[date]]

    return render_template('log_food.html', food_logs_by_day=food_logs_by_day, dates=dates)
