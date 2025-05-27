import os
import sys

# Add these lines for debugging purposes
print(f"DEBUG: Current Working Directory: {os.getcwd()}")
print(f"DEBUG: sys.path: {sys.path}")
print(f"DEBUG: Attempting to import 'decision_data' from: {os.path.dirname(__file__)}")
print(f"DEBUG: Does 'decision_data.py' exist in this directory? {os.path.exists(os.path.join(os.path.dirname(__file__), 'decision_data.py'))}")
# End of debug lines

from .decision_data import MEAL_OPTIONS, TASK_OPTIONS, BREAK_OPTIONS
from .decision_data import MEAL_OPTIONS, TASK_OPTIONS, BREAK_OPTIONS

# --- SIMULATED USER PREFERENCES (Now can be updated dynamically) ---
# This dictionary will store the preferences submitted by the form.
# It's initialized with some default users for testing.
SIMULATED_USER_PREFERENCES = {
    "user_a": {
        "user_id": "user_a",
        "meal_pref_type": "Vegetarian",
        "meal_pref_cuisine": ["Indian (North)", "Healthy / Salad focused"],
        "meal_pref_time_available": "Under 15 minutes (Very Quick)",
        "task_pref_effort": "Low Effort (e.g., replying to a short email)",
        "task_pref_type": ["Digital (emails, files, online research)", "Planning (to-do lists, scheduling)"],
        "task_pref_quick_wins": "Very Quick Wins (under 5 mins)",
        "break_pref_recharge": "Passive (e.g., listening to music, mindful breathing)",
        "break_pref_location": "Indoors (at my desk)"
    },
    "user_b": {
        "user_id": "user_b",
        "meal_pref_type": "Non-vegetarian",
        "meal_pref_cuisine": ["Chinese / Oriental", "Western / Continental"],
        "meal_pref_time_available": "15-30 minutes (Medium Quick)",
        "task_pref_effort": "Medium Effort (e.g., organizing a small folder)",
        "task_pref_type": ["Physical (tidying, quick errands)", "Communication (quick calls, messages)"],
        "task_pref_quick_wins": "Any quick task will do",
        "break_pref_recharge": "Active (e.g., stretching, short walk)",
        "break_pref_location": "Outdoors (e.g., balcony, outside building)"
    },
}

# The get_suggestion function from previous iterations is no longer needed here
# because the LLM in main.py will now handle the suggestion logic.
# If you had any other utility functions specific to calmpilot_engine that are
# still relevant outside of the main suggestion logic, they would remain here.