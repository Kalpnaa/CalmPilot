# CalmPilot/main.py

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import sys
import os

# Add the parent directory of calmpilot_ai_core to the Python path
# This allows FastAPI app to import modules from calmpilot_ai_core
# Assumes main.py is in the directory *above* calmpilot_ai_core
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'calmpilot_ai_core')))

# Now, import your AI engine and the simulated preferences
try:
    # We import SIMULATED_USER_PREFERENCES directly to allow main.py to modify it
    from calmpilot_engine import get_suggestion, SIMULATED_USER_PREFERENCES
except ImportError as e:
    print(f"Error importing calmpilot_engine: {e}")
    print("Please ensure 'calmpilot_ai_core' folder is in the same directory as main.py and contains calmpilot_engine.py")
    sys.exit(1) # Exit if the core AI engine can't be imported

app = FastAPI(
    title="CalmPilot Backend API",
    description="API for fetching personalized suggestions from the CalmPilot AI.",
    version="0.1.0",
)

# --- CORS Middleware ---
# This is CRUCIAL for allowing your frontend (running on a different port/address)
# to communicate with your backend.
origins = [
    "http://localhost",
    "http://localhost:3000", # Common for React/Vue/Angular dev servers
    "http://127.0.0.1:3000",  # Also common
    "http://127.0.0.1:5500", # Your frontend's current origin if using Live Server (e.g., VS Code)
    # Add any other frontend URLs when you deploy!
    # If you were using ngrok, its HTTPS URL would go here too (e.g., "https://abcdef123456.ngrok-free.app")
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Allows all HTTP methods (GET, POST, OPTIONS etc.)
    allow_headers=["*"], # Allows all headers
)

# --- Pydantic Models for Request Body Validation ---
# These define the expected structure of the JSON input from the frontend.
class Context(BaseModel):
    time_available: str | None = None  # e.g., "Under 15 minutes (Very Quick)", "15-30 minutes (Medium Quick)"
    mood: str | None = None           # e.g., "light", "heavy"
    energy_level: str | None = None   # e.g., "low", "medium", "high"
    weather: str | None = None        # e.g., "sunny", "cloudy", "rainy"
    feeling: str | None = None        # e.g., "Stressed", "Tired", "Restless"
    # Add any other context parameters you use in get_suggestion based on your form/logic

class SuggestionRequest(BaseModel):
    user_id: str
    decision_type: str # e.g., "meal", "task", "break"
    context: Context   # Use the Context model defined above

# --- Pydantic Model for Custom Preferences Form Submission Data ---
# IMPORTANT: Adjust these field names (`user_id`, `meal_pref_type`, etc.)
# to exactly match the `name` attributes of your form fields in preferences_form.html.
# For checkbox questions (like meal_pref_cuisine), they will come as a list.
class CustomFormPreferenceData(BaseModel):
    user_id: str
    meal_pref_type: str | None = None
    meal_pref_cuisine: list[str] | None = None # For multi-select/checkboxes
    meal_pref_time_available: str | None = None
    task_pref_effort: str | None = None
    task_pref_type: list[str] | None = None # For multi-select/checkboxes
    task_pref_quick_wins: str | None = None
    break_pref_recharge: str | None = None
    break_pref_location: str | None = None
    # Add any other fields from your preferences_form.html here

# --- API Endpoints ---

# Handles CORS preflight (OPTIONS) requests for the /get_suggestion endpoint
@app.options("/get_suggestion")
async def options_get_suggestion():
    return {}

# Main endpoint to get a personalized suggestion
@app.post("/get_suggestion")
async def get_suggestion_endpoint(request: SuggestionRequest):
    """
    Receives a request for a suggestion and returns a personalized recommendation
    from the CalmPilot AI engine.
    """
    try:
        suggestion_data = get_suggestion(
            user_id=request.user_id,
            decision_type=request.decision_type,
            context=request.context.model_dump(exclude_unset=True) # Convert Pydantic model to dict, excluding unset fields
        )
        return suggestion_data
    except Exception as e:
        print(f"Error generating suggestion: {e}", file=sys.stderr) # Log to stderr
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred while generating the suggestion.")

# Endpoint to receive user preferences from the custom HTML form
@app.post("/receive_preferences_from_form") # Renamed for clarity, was /receive_google_form_submission
async def receive_preferences_from_form(data: CustomFormPreferenceData):
    """
    Receives user preferences from the custom HTML form and updates the
    simulated user preferences in the AI engine.
    """
    try:
        # Update the global SIMULATED_USER_PREFERENCES dictionary
        SIMULATED_USER_PREFERENCES[data.user_id] = data.model_dump(exclude_unset=True)
        print(f"Received preferences for user: {data.user_id}")
        print(f"Updated SIMULATED_USER_PREFERENCES: {SIMULATED_USER_PREFERENCES.get(data.user_id)}")
        return {"message": "Preferences received and updated successfully!", "user_id": data.user_id}
    except Exception as e:
        print(f"Error receiving form submission: {e}", file=sys.stderr)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to process form submission.")

# Endpoint to get all available user IDs for the frontend dropdown
@app.get("/get_all_user_ids", response_model=list[str])
async def get_all_user_ids():
    """
    Returns a list of all user IDs currently in the simulated preferences.
    This is used by the frontend to populate the user selection dropdown.
    """
    return list(SIMULATED_USER_PREFERENCES.keys())

# Root endpoint for a basic server check
@app.get("/")
async def root():
    return {"message": "CalmPilot Backend is running!"}

# Uvicorn entry point for running the FastAPI application
if __name__ == "__main__":
    # Ensure this script is run from the CalmPilot/ directory (where main.py is)
    # so that calmpilot_ai_core can be found.
    uvicorn.run(app, host="0.0.0.0", port=8000)