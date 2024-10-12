from flask import Flask, render_template, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
#API we will use to get food facts
EDAMAM_APP_ID = 'e19d64b6'
EDAMAM_APP_KEY = '2d17a8adc75926ed22284fd2ad2a1009'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yoursecretkey'  # Change this for production

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# In-memory user store (in real scenarios, use a database)
users = {}

# User model
class User(UserMixin):
    def __init__(self, id, username, email, password):
        self.id = id
        self.username = username
        self.email = email
        self.password = password

    def get_id(self):
        return self.id

# LoginManager: Load user function
@login_manager.user_loader
def load_user(user_id):
    return users.get(int(user_id))

# Registration form
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
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
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        hashed_password = generate_password_hash(form.password.data)
        
        # Create a new user and add to the in-memory user store
        user_id = len(users) + 1
        user = User(user_id, username, email, hashed_password)
        users[user_id] = user

        flash('Registration successful. You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        
        # Find user by email
        user = next((u for u in users.values() if u.email == email), None)
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Login failed. Please check your email and password.', 'danger')
    
    return render_template('login.html', form=form)

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

# Route for logging food and fetching nutrition information
@app.route('/log-food', methods=['GET', 'POST'])
def log_food():
    if request.method == 'POST':
        food_item = request.form.get('food_item')
        if food_item:
            # Call Edamam API to get nutrition data
            api_url = f"https://api.edamam.com/api/food-database/v2/parser?ingr={food_item}&app_id={EDAMAM_APP_ID}&app_key={EDAMAM_APP_KEY}"
            response = requests.get(api_url)
            data = response.json()

            # Check if we have a valid response with nutrition data
            if 'parsed' in data and data['parsed']:
                nutrition_info = data['parsed'][0]['food']['nutrients']
                return render_template('log_food.html', food_item=food_item, nutrition_info=nutrition_info)
            else:
                flash('No nutrition data found for this item. Please try another one.', 'danger')
        else:
            flash('Please enter a valid food item.', 'warning')

    return render_template('log_food.html')


if __name__ == '__main__':
    app.run(debug=True)
