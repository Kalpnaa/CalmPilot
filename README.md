# CalmPilot AI Assistant

## 🚀 Project Overview

**CalmPilot** is an AI-powered assistant that enhances personal well-being and productivity. It offers personalized suggestions for meals, tasks, and breaks, based on user preferences and real-time context. It also includes an “Ask Me Anything” (AMA) feature for quick, intelligent responses to general questions.

This project integrates a **FastAPI** backend with a **Google Gemini API**, serving a clean HTML/CSS/JavaScript frontend.

---

## ✨ Features

- **Personalized Suggestions**  
  - Meals (based on diet, cuisine, and time)
  - Tasks (based on energy, effort, and duration)
  - Breaks (based on mood and location)
- **Context-Aware Recommendations**
- **Ask Me Anything (AMA)**: Get smart, concise answers
- **Simulated User Profiles**
- **Minimal Frontend UI**
- **Robust FastAPI Backend**

---

## 🛠️ Technologies Used

**Backend:**
- Python 3.9
- FastAPI
- `google-generativeai`
- `uvicorn`
- `pydantic`
- `python-dotenv` (optional for API key handling)

**Frontend:**
- HTML5
- CSS3
- JavaScript (Vanilla JS)

**AI Model:**
- Google Gemini 1.5 Flash (via API)

---

## 📂 Project Structure

.
├── main.py
├── calmpilot_ai_core/
│ ├── init.py
│ ├── calmpilot_engine.py 
│ └── decision_data.py # Suggestion options
├── main2.html # Frontend HTML file
├── requirements.txt # Dependencies
└── README.md # 

---

## ⚙️ Setup and Installation

### 1. Clone the Repository

git clone <your-repository-url>
cd CalmPilot-AI-Assistant
### 2. Create a Virtual Environment (Recommended)
bash
Copy
Edit
python -m venv venv
# Activate:
# Windows:
.\venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
### 3. Install Dependencies
pip install -r requirements.txt
If requirements.txt is missing:
pip install fastapi uvicorn google-generativeai pydantic python-dotenv
### 4. Get Your Google Gemini API Key
Visit Google AI Studio

Generate and copy your API key

### 5. Configure the API Key
Option A: Hardcode (not recommended for production)
In main.py:
genai.configure(api_key="YOUR_GEMINI_API_KEY")
Option B: Use .env File (recommended)
Install dotenv:
pip install python-dotenv
Create a .env file:
env
GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
Update main.py:
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
Make sure .env is listed in .gitignore.

### 6. Run the Backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
FastAPI will start at http://127.0.0.1:8000.

### 7. Run the Frontend
Open main2.html in a browser.

For better experience, use a Live Server extension (e.g., in VS Code).

***🚀 How to Use***
Select a User Profile from the dropdown.

Choose a Suggestion Type (Meal, Task, Break).

Optionally Fill Context Fields (Mood, Energy, Time).

Click "Get My CalmPilot Suggestion" to receive AI advice.

Use the "Ask Me Anything" section for general queries.

User preferences are stored in calmpilot_engine.py (editable).

***💡 Future Enhancements***
Persistent user data (SQLite or JSON)

Onboarding UI for user preferences

Suggestion & answer history

Feedback buttons (Like/Dislike)

Advanced context input

Better UI/UX with animations

Frontend error handling

More diverse suggestions

Full deployment (Render, Netlify, etc.)

***🤝 Contributing***
Contributions are welcome!
Feel free to fork this repo, open issues, or submit pull requests.
