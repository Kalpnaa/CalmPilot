from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any # Import Any for context type hint

# Import the Google Generative AI library
import google.generativeai as genai

import sys
import os
import json # Import json for parsing LLM response

# Add the parent directory of calmpilot_ai_core to the Python path
# This helps ensure Python can find modules within 'calmpilot_ai_core'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'calmpilot_ai_core')))

try:
    # Import from your custom modules
    from calmpilot_ai_core.calmpilot_engine import SIMULATED_USER_PREFERENCES
    from calmpilot_ai_core.decision_data import MEAL_OPTIONS, TASK_OPTIONS, BREAK_OPTIONS
except ImportError as e:
    print(f"Error importing modules from calmpilot_ai_core: {e}", file=sys.stderr)
    print("Please ensure 'calmpilot_ai_core' folder is in the same directory as main.py,", file=sys.stderr)
    print("and contains calmpilot_engine.py (with SIMULATED_USER_PREFERENCES) and decision_data.py.", file=sys.stderr)
    sys.exit(1) # Exit if core AI engine or data can't be imported


# --- Initialize FastAPI App ---
app = FastAPI(
    title="CalmPilot Backend API",
    description="API for fetching personalized suggestions from the CalmPilot AI.",
    version="0.1.0",
)

# --- CORS Middleware ---
# This allows your frontend (e.g., running on Live Server) to make requests to this backend.
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5500", # Your frontend's current origin if using Live Server
    # Add any other frontend URLs when you deploy!
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Allow all standard HTTP methods
    allow_headers=["*"], # Allow all headers
)

# --- Pydantic Models for Request Body Validation ---
# These define the expected structure of incoming JSON data.

class Context(BaseModel):
    # Optional fields for user's current situation/mood
    time_available: Optional[str] = None
    mood: Optional[str] = None
    energy_level: Optional[str] = None
    weather: Optional[str] = None
    feeling: Optional[str] = None

class SuggestionRequest(BaseModel):
    user_id: str
    decision_type: str # e.g., "meal", "task", "break"
    context: Context # Use the Context model defined above

# NEW: Model for a general text query
class GeneralQueryRequest(BaseModel):
    user_id: str # Keep user_id for potential personalization based on preferences
    query_text: str # The actual question from the user

class CustomFormPreferenceData(BaseModel):
    # Fields matching your preference form inputs
    user_id: str
    meal_pref_type: Optional[str] = None
    meal_pref_cuisine: Optional[List[str]] = None
    meal_pref_time_available: Optional[str] = None
    task_pref_effort: Optional[str] = None
    task_pref_type: Optional[List[str]] = None
    task_pref_quick_wins: Optional[str] = None
    break_pref_recharge: Optional[str] = None
    break_pref_location: Optional[str] = None

# --- LLM Integration Configuration ---
genai.configure(api_key="AIzaSyDrKYV03rpLoBfII1R60QQ7eS1W2khdRWQ") 

# Initialize the Gemini model to be used for generating suggestions
MODEL_NAME = 'models/gemini-1.5-flash-latest'
model = genai.GenerativeModel(MODEL_NAME)

# --- API Endpoints ---

@app.get("/")
async def root():
    """
    Basic endpoint to confirm the backend is running.
    """
    return {"message": "CalmPilot Backend is running!"}

# Handles CORS preflight (OPTIONS) requests for the /get_suggestion endpoint
# This is often needed for POST requests from different origins.
@app.options("/get_suggestion")
async def options_get_suggestion():
    return {}

@app.post("/get_suggestion")
async def get_llm_suggestion(request_data: SuggestionRequest):
    """
    Generates a personalized suggestion (meal, task, or break) using an LLM
    based on user preferences and current context.
    """
    user_id = request_data.user_id
    decision_type = request_data.decision_type
    context = request_data.context.model_dump(exclude_unset=True) # Convert Pydantic Context model to a dict

    # Retrieve user preferences from the in-memory store
    user_prefs = SIMULATED_USER_PREFERENCES.get(user_id)
    if not user_prefs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User preferences not found. Please submit your preferences first."
        )

    # Select the relevant options list (Meal, Task, or Break) for the LLM to consider
    options_list = []
    if decision_type == "meal":
        options_list = MEAL_OPTIONS
    elif decision_type == "task":
        options_list = TASK_OPTIONS
    elif decision_type == "break":
        options_list = BREAK_OPTIONS
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid decision type. Must be 'meal', 'task', or 'break'."
        )

    # --- Construct the Prompt for the LLM ---
    # Prepare user preferences for the prompt (convert lists to strings for readability)
    printable_user_prefs = {}
    for key, value in user_prefs.items():
        if isinstance(value, list):
            printable_user_prefs[key] = ", ".join(value)
        else:
            printable_user_prefs[key] = value

    # Format options list for the prompt (show name and details)
    # Updated to show more relevant attributes for LLM
    formatted_options = "\n".join([
        f"- {opt.get('name', 'Unnamed Option')} (Time: {opt.get('total_time_minutes', opt.get('estimated_duration_minutes', opt.get('duration_minutes', 'N/A')))} mins, "
        f"Effort: {opt.get('effort_level', 'N/A')}, "
        f"Mood Benefit: {', '.join(opt.get('mood_benefit', []))}, "
        f"Location: {opt.get('location', 'N/A')})"
        for opt in options_list
    ])


    # The core prompt that guides the LLM's behavior and desired output format
   # ... [previous code remains unchanged] ...

    # The core prompt that guides the LLM's behavior and desired output format
    prompt_template = f"""
You are CalmPilot, a highly intelligent AI assistant focused on enhancing personal well-being through personalized suggestions. Your goal is to provide ONE optimal **{decision_type}** suggestion based on both the **User Preferences** and the **Current Context** — but when there's a conflict, CONTEXT always wins.

---

🔍 **Prioritization Rules**:
1. ✅ Always prioritize the **Current Context** over user preferences — especially:
   - Time constraints
   - Mood
   - Energy level
   - Weather compatibility

2. ⏱️ Respect time limits strictly. Only suggest options where:
   - 'total_time_minutes' (meals)
   - 'estimated_duration_minutes' (tasks)
   - 'duration_minutes' (breaks)
   are **less than or equal to** `time_available`. If no valid options, suggest the closest match *with a warning*.

3. 🍽️ For meals:
   - Match 'cuisine' and 'dietary_tags' with preferences.
   - Stay within the available time.

4. ✅ For tasks:
   - Match 'effort_level' to 'energy_level'.
   - Prioritize 'quick_win' if the user is feeling low or unmotivated.

5. 🧘 For breaks:
   - Match 'activity_level' and 'mood_benefit' with current mood.
   - Consider 'location' and adjust if weather is bad.

---

👤 **User ID**: {user_id}

📋 **Preferences**:
{printable_user_prefs}

📍 **Current Context**:
{context}

---

📚 **Available {decision_type.capitalize()} Options**:
(Choose exactly ONE. Do NOT invent new ones.)
{formatted_options}

---

📤 **Respond in JSON only**:
```json
{{
  "suggestion_name": "Option Name",
  "rationale": "Reason why this option fits CURRENT CONTEXT best",
  "decision_type": "{decision_type}"
}}
"""

    print("\n--- Sending Prompt to LLM ---")
    print(prompt_template)
    print("----------------------------\n")

    try:
        # Call the Gemini API to get the content
        response = model.generate_content(prompt_template)
        llm_response_text = response.text
        print(f"--- LLM Raw Response --- \n{llm_response_text}\n-----------------------\n")

        # --- IMPORTANT: Extract JSON from potential Markdown code block ---
        parsed_llm_response = llm_response_text.strip() # Remove any leading/trailing whitespace
        if parsed_llm_response.startswith("```json"):
            # Find the start and end of the JSON block within the markdown
            start_index = parsed_llm_response.find('{')
            end_index = parsed_llm_response.rfind('}') + 1 # +1 to include the closing brace
            
            if start_index != -1 and end_index != -1 and start_index < end_index:
                parsed_llm_response = parsed_llm_response[start_index:end_index].strip()
            else:
                # Fallback if markdown format is unexpected but ````json` is present
                parsed_llm_response = parsed_llm_response[len("```json"):].strip()
                if parsed_llm_response.endswith("```"):
                    parsed_llm_response = parsed_llm_response[:-len("```")].strip()
        elif parsed_llm_response.startswith("```"): # General markdown block
            start_index = parsed_llm_response.find('{')
            end_index = parsed_llm_response.rfind('}') + 1
            if start_index != -1 and end_index != -1 and start_index < end_index:
                parsed_llm_response = parsed_llm_response[start_index:end_index].strip()
            else:
                parsed_llm_response = parsed_llm_response[len("```"):].strip()
                if parsed_llm_response.endswith("```"):
                    parsed_llm_response = parsed_llm_response[:-len("```")].strip()

        # Now, attempt to parse the cleaned string as JSON
        llm_suggestion_data = json.loads(parsed_llm_response)

        # Basic validation of the LLM's response format
        if "suggestion_name" not in llm_suggestion_data or "rationale" not in llm_suggestion_data:
            raise ValueError("LLM response missing required fields (suggestion_name or rationale).")

        # Return the LLM's suggestion structured for the frontend
        return {
            "suggestion": llm_suggestion_data.get("suggestion_name", "No suggestion"),
            "rationale": llm_suggestion_data.get("rationale", "No rationale provided."),
            "details": llm_suggestion_data # Include all LLM's parsed data here for frontend use/debugging
        }

    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {e}. Raw LLM response was:\n'{llm_response_text}'", file=sys.stderr)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to parse LLM response (Invalid JSON): {e}"
        )
    except Exception as e:
        print(f"Error calling LLM or processing response: {e}", file=sys.stderr)
        # Fallback or general error message if LLM fails or other issues occur
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get LLM suggestion due to an internal error: {e}"
        )

# NEW ENDPOINT: For general day-to-day questions
@app.post("/ask_ai")
async def ask_general_question(request_data: GeneralQueryRequest):
    """
    Handles general day-to-day questions using the LLM, optionally
    considering user preferences for personalization.
    """
    user_id = request_data.user_id
    user_query = request_data.query_text

    # Retrieve user preferences for personalization (optional, but good for context)
    user_prefs = SIMULATED_USER_PREFERENCES.get(user_id, {})
    
    printable_user_prefs = {}
    for key, value in user_prefs.items():
        if isinstance(value, list):
            printable_user_prefs[key] = ", ".join(value)
        else:
            printable_user_prefs[key] = value

    # Construct the prompt for the general question
    # We include user preferences here to allow the LLM to personalize answers
    prompt_for_general_question = f"""
    You are CalmPilot, a helpful AI assistant. Answer the following question concisely and directly.
    If applicable, try to personalize your answer based on the user's preferences, but do not force it.
    If the question is about personal styling, assume a general sense of fashion and practicality.

    User's Question: {user_query}

    User ID: {user_id}
    User Preferences (for context, may be empty):
    {printable_user_prefs}

    Provide your answer in plain text.
    """

    print("\n--- Sending General Query to LLM ---")
    print(prompt_for_general_question)
    print("------------------------------------\n")

    try:
        response = model.generate_content(prompt_for_general_question)
        ai_response_text = response.text
        print(f"--- LLM Raw General Response --- \n{ai_response_text}\n----------------------------------\n")
        
        return {"answer": ai_response_text}

    except Exception as e:
        print(f"Error calling LLM for general question: {e}", file=sys.stderr)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get AI answer due to an internal error: {e}"
        )


@app.post("/receive_preferences_from_form")
async def receive_preferences_from_form(data: CustomFormPreferenceData):
    """
    Receives user preferences from the HTML form and stores them in memory.
    """
    try:
        # Update the global SIMULATED_USER_PREFERENCES dictionary
        # .model_dump(exclude_unset=True) ensures only provided fields are stored
        SIMULATED_USER_PREFERENCES[data.user_id] = data.model_dump(exclude_unset=True)
        print(f"Received preferences for user: {data.user_id}")
        print(f"Updated SIMULATED_USER_PREFERENCES for {data.user_id}: {SIMULATED_USER_PREFERENCES.get(data.user_id)}")
        return {"message": "Preferences received and updated successfully!", "user_id": data.user_id}
    except Exception as e:
        print(f"Error receiving form submission: {e}", file=sys.stderr)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process form submission. Please try again."
        )

@app.get("/get_all_user_ids", response_model=List[str])
async def get_all_user_ids():
    """
    Returns a list of all user IDs currently in the simulated preferences.
    This is used by the frontend to populate the user selection dropdown.
    """
    return list(SIMULATED_USER_PREFERENCES.keys())


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)