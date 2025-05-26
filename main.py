# CalmPilot/main.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import sys
import os

# Add the parent directory of calmpilot_ai_core to the Python path
# This allows FastAPI app to import modules from calmpilot_ai_core
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'calmpilot_ai_core')))

# Now, import your AI engine
try:
    from calmpilot_engine import get_suggestion
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
    # Add any other frontend URLs when you deploy!
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"], # Allows all headers
)

# --- Pydantic Models for Request Body Validation ---
# These define the expected structure of the JSON input from the frontend.
class Context(BaseModel):
    time_available: str | None = None  # e.g., "quick", "medium"
    mood: str | None = None           # e.g., "light", "heavy", "stressed"
    energy_level: str | None = None   # e.g., "low", "medium", "high"
    weather: str | None = None        # e.g., "sunny", "cloudy"
    feeling: str | None = None        # e.g., "Stressed", "Tired", "Restless"
    # Add any other context parameters you use in get_suggestion based on your form/logic

class SuggestionRequest(BaseModel):
    user_id: str
    decision_type: str # e.g., "meal", "task", "break"
    context: Context   # Use the Context model defined above

# --- API Endpoint ---
@app.post("/get_suggestion")
async def get_suggestion_endpoint(request: SuggestionRequest):
    """
    Receives a request for a suggestion and returns a personalized recommendation
    from the CalmPilot AI engine.
    """
    try:
        # Call your AI's get_suggestion function
        suggestion_data = get_suggestion(
            user_id=request.user_id,
            decision_type=request.decision_type,
            context=request.context.model_dump(exclude_unset=True) # Convert Pydantic model to dict
        )
        return suggestion_data
    except Exception as e:
        # Log the full error for debugging, but return a generic message to the client
        print(f"Error generating suggestion: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while generating the suggestion.")

# --- Root Endpoint (Optional, just for testing if server is running) ---
@app.get("/")
async def root():
    return {"message": "CalmPilot Backend is running!"}

# You don't typically run uvicorn like this directly in main.py for deployment,
# but for local testing, it's convenient.
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)