from app.modules.harmful_ingredients import call_ingredients
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from datetime import datetime, timedelta

food_blueprint = Blueprint('food', __name__)
#0 means no harmful ingredients, 1 is 1-3, 2 is 3 or more
status = 0

# Route to log food consumption and view past logs
@food_blueprint.route('/log_food', methods=['GET', 'POST'])
@login_required
def log_food():
    if request.method == 'POST':
        # Collect form data
        food_name = request.form.get('food')
        time = request.form.get('time')
        date = request.form.get('date')  # The date selected by the user

        #dictionary to store harmful ingredients
        harmful_ingredients = call_ingredients(food_name)
        if len(harmful_ingredients == 0):
            status = 0
        elif len(harmful_ingredients) <= 3:
            status = 1
        else:    
            status = 2

        # Save the food log in Firestore, grouped by date
        current_app.firestore_db.collection('food_logs').add({
            'user_id': current_user.id,
            'food_name': food_name,
            'harmful_ingredients': harmful_ingredients,
            'ingredients' : call_ingredients(food_name)
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
