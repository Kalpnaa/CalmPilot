# calmpilot_ai_core/calmpilot_engine.py

import pandas as pd
import random
from decision_data import MEAL_OPTIONS, TASK_OPTIONS, BREAK_OPTIONS

# --- Simulated User Preferences (For Prototype from Google Form) ---
# These represent the data you'd expect from the Google Form for different users.
SIMULATED_USER_PREFERENCES = {
    "user_default": {
        "meal_pref_type": "Indian",
        "meal_pref_time": "quick",
        "task_pref_effort": "low",
        "task_pref_time": "quick",
        "break_pref_activity": "passive"
    },
    "user_b": { # Example for another simulated user profile
        "meal_pref_type": "Western",
        "meal_pref_time": "medium",
        "task_pref_effort": "medium",
        "task_pref_time": "medium",
        "break_pref_activity": "active"
    }
}

# --- Core Suggestion Logic ---
def get_suggestion(user_id: str, decision_type: str, context: dict) -> dict:
    """
    Generates a single, personalized suggestion based on user preferences and context.
    """
    user_prefs = SIMULATED_USER_PREFERENCES.get(user_id, SIMULATED_USER_PREFERENCES["user_default"])

    options = []
    if decision_type == "meal":
        options = MEAL_OPTIONS
    elif decision_type == "task":
        options = TASK_OPTIONS
    elif decision_type == "break":
        options = BREAK_OPTIONS
    else:
        return {"suggestion": "No specific options for this decision type.", "rationale": ""}

    filtered_options = []
    for option in options:
        score = 0

        # Apply preferences and context-based scoring
        if decision_type == "meal":
            if option.get("type") == user_prefs.get("meal_pref_type"): score += 2
            if option.get("time") == user_prefs.get("meal_pref_time"): score += 1
            if context.get("mood") == option.get("mood"): score += 1
        elif decision_type == "task":
            if option.get("effort") == user_prefs.get("task_pref_effort"): score += 2
            if option.get("time") == user_prefs.get("task_pref_time"): score += 1
            if context.get("energy_level") == "low" and option.get("effort") == "low": score += 1
        elif decision_type == "break":
            if option.get("activity") == user_prefs.get("break_pref_activity"): score += 2
            if context.get("weather") == "sunny" and option.get("type") == "outdoor": score += 1

        option["score"] = score
        filtered_options.append(option)

    # Select the best option (or a random one if scores are tied/no strong matches)
    best_option = None
    if filtered_options:
        filtered_options.sort(key=lambda x: x["score"], reverse=True)
        max_score = filtered_options[0]["score"]
        top_scorers = [opt for opt in filtered_options if opt["score"] == max_score]
        best_option = random.choice(top_scorers)

    if best_option:
        rationale = f"Based on your preferences and current context, '{best_option['name']}' seems like a great fit."
        if decision_type == "meal" and user_prefs.get("meal_pref_type") == best_option.get("type"):
             rationale += f" You often prefer {best_option.get('type')} options."
        if context.get("time_available") == "quick" and best_option.get("time") == "quick":
            rationale += " It's also a quick option."

        return {
            "suggestion": best_option["name"],
            "details": best_option, # Good for debugging, can be removed for final output
            "rationale": rationale
        }
    else:
        return {
            "suggestion": "I'm a bit stumped right now. Maybe try again with different context?",
            "rationale": "No suitable options found based on your preferences."
        }