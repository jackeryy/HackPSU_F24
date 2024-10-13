# HackPSU_F24

## Inspiration 
The inspiration for our website is centered around how many people get chronic illness's when they age and a lot of the time this is because if undetected nutritional deficiencies in their diet. We want to build a healthier future for people around the world by giving them AI-driven advice about their diet to potentially prevent chronic illnesses in their lifetime.

## Overview 
The website asks users to create an account where they will put in their basic health information, they will be reminded daily to log in their meals by manual search or by scanning packaged items barcodes. The AI-assistant will give the user real time feedback on the nutritional deficiencies and what chronic illnesses can be cause from their diet. The website will also give future dietary suggestions for a healthier life.

## How we built it
We built the **AI-driven Nutritional Deficiency Detector** using a combination of Flask for the backend, Firebase for user authentication and database storage, and OpenAI's GPT-3 for personalized dietary insights. Users log their daily food intake, which is analyzed by our AI assistant to detect nutritional deficiencies and harmful ingredients in their diet. The system uses Firebase's Firestore to store food logs and user profile information, while Flask handles user authentication and manages the chatbot functionality. 

## Challenges we ran into
We encountered several challenges during the development process. One major challenge was integrating the **barcode scanner** for automatically logging food items. Ensuring the scanner worked efficiently across different devices and accurately pulled up food data proved to be difficult, especially with time constraints. We also struggled with **styling our pages** to make them both user-friendly and visually appealing, given the need to balance functionality and design within a short time frame. Additionally, integrating multiple technologies—Firebase, Flask, and OpenAI—posed challenges, especially in managing user authentication and ensuring smooth data flow between the frontend and backend.


## Accomplishments that we're proud of
We are proud of successfully integrating OpenAI into the project to create a personalized chatbot that provides valuable dietary insights. The seamless user experience—from signing up, logging food, and interacting with the AI assistant—is a major accomplishment. We also take pride in using Firebase for managing user data securely and creating an engaging and responsive interface for users to track and improve their nutrition. Building a functional and useful prototype in such a short time was a significant achievement for our team.

## What we learned
Through this project, we learned how to work with Firebase for user authentication and database management, and how to integrate it with Flask to manage user sessions. We gained deeper knowledge of how to use OpenAI’s API effectively, especially when it comes to crafting prompts to deliver meaningful and personalized responses. We also learned how to structure a full-stack application that combines frontend user interactions with backend data processing, as well as the importance of collaboration and version control when working in a team.

## What's next for AI-driven Nutritional Deficiency Detector
We have several exciting plans for the future development of the **AI-driven Nutritional Deficiency Detector**:

### 1. Symptom Tracking for Improved AI Assessment
We plan to add a **symptom tracking feature**, allowing users to log health symptoms (e.g., fatigue, headaches, digestive issues). This data will be integrated into the AI assistant’s analysis to provide more accurate dietary recommendations and help users understand if certain symptoms are linked to nutritional deficiencies or harmful ingredients in their diet. By connecting diet to health symptoms, the AI can provide even more personalized advice.

### 2. Expanding the Food Library
We aim to expand our **food library**, allowing users to log a wider variety of foods, including prepackaged foods and international cuisine. This would improve the accuracy of the nutritional data and the AI’s analysis. We also want to link our barcode scanner to a larger database, making it easier for users to scan and log food items without manually entering details.

### 3. Building a Mobile App
One of our key goals is to develop a **mobile app** for iOS and Android, making it easier for users to track their nutrition on the go. A mobile app will allow for real-time logging, push notifications for meal reminders, and seamless access to the AI assistant’s recommendations.

### 4. Smartwatch Integration
To further enhance the user experience, we plan to integrate our system with **smartwatches** and other wearable devices. This will allow us to track additional health metrics such as heart rate, sleep patterns, and physical activity. The AI assistant will use this data to provide even more comprehensive health insights and suggestions, tying together nutrition, fitness, and overall well-being.

### 5. Improved AI with More Insights
We will continue to improve the AI assistant, adding more sophisticated **machine learning models** to assess users' long-term health trends. This includes identifying patterns in their dietary habits and suggesting actionable improvements. The AI could also alert users if they are at risk of specific health conditions based on their logged symptoms and food intake over time.

### 6. Enhanced User Interface and Experience
We aim to further refine the **user interface and experience** by making the chatbot more interactive and adding features such as voice commands, a personalized dashboard with visual data (caloric intake, nutrient graphs), and easy navigation to food logs and recommendations.

These future enhancements will help make our AI-driven nutrition assistant even more accurate, accessible, and helpful, improving users' overall health and well-being.
