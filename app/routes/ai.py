# /app/routes/ai.py
from flask import Blueprint, request, jsonify, current_app
from flask_login import login_required, current_user
import openai
import os

ai_blueprint = Blueprint('ai', __name__)

# Initialize OpenAI API with the key from environment variables
openai.api_key = os.getenv('OPENAI_API_KEY')

# Route to handle chatbot interactions
@ai_blueprint.route('/chatbot', methods=['POST'])
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
    
    # Create a summary of the user's food logs and potential risks
    food_summary = ""
    for log in food_logs:
        log_data = log.to_dict()
        food_summary += f"{log_data['food_name']} (Harmful Ingredients: {log_data['harmful_count']}), "

    # Create personalized prompt for OpenAI
    prompt = f"""
    You are a health assistant helping a user improve their diet. The user has logged these foods:
    {food_summary}
    
    The user's profile:
    - Age: {profile['age']}
    - Weight: {profile['weight']} kg
    - Height: {profile['height']} cm
    - Allergies: {profile.get('allergies', 'None')}
    - Health Conditions: {profile.get('health_conditions', 'None')}
    
    User's input: "{user_message}"

    Based on this information, give the user personalized dietary advice. If their food intake includes harmful ingredients, suggest healthier alternatives. Also, ask them relevant questions about their lifestyle, such as water intake, exercise, and sunlight exposure. Identify any risks based on their diet and suggest improvements.
    """

    # Call OpenAI's GPT API
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # You can choose other models like "gpt-3.5-turbo"
            prompt=prompt,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.7,
        )
        chatbot_reply = response.choices[0].text.strip()
    except Exception as e:
        chatbot_reply = "Sorry, I encountered an error processing your request."

    return jsonify({"response": chatbot_reply})
