# CalmPilot AI Assistant

## 🚀 Project Overview

CalmPilot is an intelligent AI assistant designed to enhance personal well-being and productivity. It offers personalized suggestions for daily decisions like meals, tasks, and breaks, tailored to individual user preferences and current context. Additionally, it features a versatile "Ask Me Anything" (AMA) capability, allowing users to get quick, personalized answers to a wide range of general questions.

This project demonstrates the integration of a FastAPI backend with a Google Gemini (or similar LLM) API, serving a simple HTML/CSS/JavaScript frontend.

## ✨ Features

* **Personalized Suggestions:** Get AI-driven recommendations for:
    * **Meals:** Based on dietary preferences, cuisine, and time available.
    * **Tasks:** Tailored to effort levels, quick wins, and user energy.
    * **Breaks:** Designed for optimal recharge considering mood and location.
* **Contextual Awareness:** Suggestions are dynamically adjusted based on current mood, energy level, weather, and available time, prioritizing immediate needs over general preferences where conflicts arise.
* **"Ask Me Anything" (AMA):** Ask general day-to-day questions and receive concise, personalized answers from the AI.
* **User Profiles:** Simulate distinct user profiles with stored preferences for a tailored experience.
* **Simple Frontend:** An intuitive web interface built with HTML, CSS, and vanilla JavaScript for easy interaction.
* **Robust Backend:** Powered by FastAPI for efficient API handling and LLM integration.

## 🛠️ Technologies Used

* **Backend:**
    * Python 3.x
    * FastAPI: Web framework for building APIs.
    * `google-generativeai`: Python client library for the Google Gemini API.
    * `uvicorn`: ASGI server to run the FastAPI application.
    * `pydantic`: For data validation and settings management.
* **Frontend:**
    * HTML5
    * CSS3
    * JavaScript (Vanilla JS)
* **AI Model:**
    * Google Gemini 1.5 Flash (via API)

## 📂 Project Structure

.
├── main.py                          # FastAPI application, API endpoints, LLM integration
├── calmpilot_ai_core/
│   ├── init.py                  # Makes it a Python package
│   ├── calmpilot_engine.py          # Stores simulated user preferences (in-memory)
│   └── decision_data.py             # Defines the list of available meal, task, and break options
├── main2.html                       # Frontend HTML file with interactive elements
├── README.md                        # This file
└── requirements.txt                 # Python dependencies


## ⚙️ Setup and Installation

Follow these steps to get CalmPilot up and running on your local machine.

### 1. Clone the Repository

```bash
git clone <your-repository-url> # Replace with your actual repository URL
cd CalmPilot-AI-Assistant     # Or whatever your project folder is named
2. Create a Virtual Environment (Recommended)
Bash

python -m venv venv
# On Windows
.\venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
3. Install Dependencies
Bash

pip install -r requirements.txt
If requirements.txt is missing, you can create it or install manually:

Bash

pip install fastapi uvicorn google-generativeai pydantic python-dotenv # If using dotenv for API key
4. Obtain Google Gemini API Key
Go to Google AI Studio.
Log in with your Google account.
Create a new API key or copy an existing one.
5. Configure API Key
Open main.py and locate the line:

Python

genai.configure(api_key="YOUR_GEMINI_API_KEY") # <<< IMPORTANT: REPLACE WITH YOUR ACTUAL GEMINI API KEY
Replace "YOUR_GEMINI_API_KEY" with the API key you obtained from Google AI Studio.

Alternatively (and recommended for security):
You can use environment variables.

Install python-dotenv: pip install python-dotenv
Create a file named .env in the root of your project directory (.) with the following content:
GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
In main.py, modify the API key configuration like this:
    import os
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
```
(Remember to add `.env` to your `.gitignore` file to prevent committing your API key.)
6. Run the Backend
Navigate to your project's root directory in the terminal where your virtual environment is active, and run:

Bash

uvicorn main:app --reload --host 0.0.0.0 --port 8000
This will start the FastAPI server, typically accessible at http://127.0.0.1:8000. The --reload flag ensures the server restarts automatically on code changes.

7. Run the Frontend
Open main2.html in your web browser.

Recommended: Use a Live Server extension (e.g., for VS Code) for easy development, as it handles running a local server and refreshing. If using Live Server, its default address is often http://127.0.0.1:5500 or http://localhost:5500. Ensure this origin is allowed in main.py's CORS configuration.

🚀 How to Use
Set Up Preferences (Simulated): The calmpilot_engine.py currently holds SIMULATED_USER_PREFERENCES. You can edit this file directly to pre-define user profiles (user_a, user_b, etc.) with their meal, task, and break preferences.
Select User Profile: On the main2.html page, select a user from the "Select Your Profile" dropdown.
Get a Personalized Suggestion:
Choose a "decision type" (Meal, Task, Break).
Fill in optional "Current Context" fields (Time Available, Mood, Energy Level, etc.).
Click "Get My CalmPilot Suggestion".
The AI will provide a tailored suggestion and a rationale.
Ask Me Anything:
Type any general question into the "Your Question" textarea.
Click "Ask CalmPilot AI".
The AI will provide a direct answer, potentially personalized based on the selected user's preferences.
💡 Future Enhancements
Persistent User Data: Implement a simple database (e.g., SQLite) or JSON file storage for user preferences and suggestions history, so data persists across server restarts.
User Onboarding/Preference Form: Create a dedicated HTML form for users to input and save their preferences, rather than editing calmpilot_engine.py directly.
Suggestion History: Display a log of past suggestions and AI answers for each user.
Feedback Mechanism: Add "Like/Dislike" buttons for suggestions to gather user feedback and potentially refine the AI's future responses.
Enhanced Context: Allow more dynamic and rich input for current context (e.g., free-form text input for specific situations).
Improved UI/UX: Refine the styling, add animations, and improve responsiveness for a smoother user experience.
Error Handling on Frontend: Display more user-friendly error messages if the backend or LLM call fails.
More Diverse Options: Expand decision_data.py with a wider variety of suggestions.
Deployment: Deploy the FastAPI backend and HTML frontend to a cloud platform (e.g., Render, Heroku, Vercel, Netlify for frontend, etc.).
🤝 Contributing
Feel free to fork this repository, open issues, and submit pull requests. Any contributions are welcome!

