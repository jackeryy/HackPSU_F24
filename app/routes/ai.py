# /app/routes/ai.py
from flask import Blueprint, request, jsonify, current_app
from flask_login import login_required, current_user
import openai
import os

ai_blueprint = Blueprint('ai', __name__)

# Initialize OpenAI API with the key from environment variables
openai.api_key = os.getenv('OPENAI_API_KEY')

# Route to handle chatbot interactions
@ai_blueprint.route('/chatbot', methods=['GET','POST'])
@login_required
def chatbot():

    data = request.get_json()
    user_message = data.get('message')

    # Fetch user profile data
    user_doc = current_app.firestore_db.collection('users').document(current_user.id).get()
    profile = user_doc.to_dict()

    # Fetch user food logs
    food_logs = current_app.firestore_db.collection('food_logs') \
        .where('user_id', '==', current_user.id).stream()
    
    food_summary = ""
    harmful_ingredients_count = 0

    for log in food_logs:
        log_data = log.to_dict()
        food_name = log_data['food_name']
        harmful_info = log_data.get('harmful_info', [])  # Harmful ingredients insights
        ingredients = log_data.get('ingredients', 'No ingredients listed')

        # Summarize all ingredients and harmful ingredient risks
        food_summary += f"\n- {food_name}: Ingredients = {ingredients}"

        # List harmful ingredients and their risks
        for ingredient_info in harmful_info:
            food_summary += f"\n  * {ingredient_info['ingredient']} - {ingredient_info['risk']}"
            harmful_ingredients_count += 1

    # Create personalized prompt for OpenAI
    prompt = f"""
    You are a nutrition assistant analyzing a user's diet and providing personalized feedback. The user has logged the following food items and ingredients:

    {food_summary}
    
    The user's profile is as follows:
    - Age: {profile['age']}
    - Weight: {profile['weight']} kg
    - Height: {profile['height']} cm
    - Allergies: {profile.get('allergies', 'None')}
    - Health Conditions: {profile.get('health_conditions', 'None')}
    
    Based on the food logs, analyze the user's diet. Provide personalized dietary advice, suggest healthier food alternatives, and recommend foods they may be missing (such as potassium, fiber, or protein). Identify any health risks based on harmful ingredients (e.g., sugar, sodium, trans fats) and suggest what the user should avoid. If possible, highlight foods that they should consider eating more of.

    User's input: "{user_message}"

    Your feedback should be detailed and insightful, offering the user practical solutions to improve their diet and avoid harmful ingredients.
    You will refer to scholarly research papers (such as pubmed) to base your feedback to the user.
    """

    # Call OpenAI's GPT API
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use newer model name
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=50,
            temperature=0.7,
        )
        chatbot_reply = response['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"Error in OpenAI API call: {e}")
        chatbot_reply = "Sorry, I encountered an error processing your request."


    return jsonify({"response": chatbot_reply})
