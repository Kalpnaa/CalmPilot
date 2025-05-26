# calmpilot_ai_core/calmpilot_engine.py

import random
# Make sure decision_data.py is in the same directory as this file
from decision_data import MEAL_OPTIONS, TASK_OPTIONS, BREAK_OPTIONS

# --- SIMULATED USER PREFERENCES (Matching Google Form Structure) ---
# IMPORTANT: These keys and values should EXACTLY match what you defined in your Google Form
# and what you expect to get if you were to read the Google Sheet directly.
SIMULATED_USER_PREFERENCES = {
    "user_a": {
        "user_id": "user_a",
        "meal_pref_type": "Vegetarian",
        "meal_pref_cuisine": ["Indian (North)", "Healthy / Salad focused"], # Checkbox values as a list
        "meal_pref_time_available": "Under 15 minutes (Very Quick)",
        "task_pref_effort": "Low Effort (e.g., replying to a short email)",
        "task_pref_type": ["Digital (emails, files, online research)", "Planning (to-do lists, scheduling)"], # Checkbox values as a list
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
    # Add more user profiles (e.g., "user_c", "user_d") here by manually filling your Google Form
    # with different answers and then copying the resulting structure from the Google Sheet.
}

# --- Core Suggestion Logic ---
def get_suggestion(user_id: str, decision_type: str, context: dict) -> dict:
    """
    Generates a single, personalized suggestion based on user preferences and context.

    Args:
        user_id (str): The ID of the user (e.g., "user_a", "user_b").
        decision_type (str): The type of decision requested ("meal", "task", "break").
        context (dict): Dictionary with current situational context (e.g., {"time_available": "quick", "mood": "light"}).

    Returns:
        dict: A dictionary containing "suggestion" (str), "details" (dict, for debugging), and "rationale" (str).
    """
    user_prefs = SIMULATED_USER_PREFERENCES.get(user_id, SIMULATED_USER_PREFERENCES["user_a"]) # Default to user_a if ID not found

    options = []
    if decision_type == "meal":
        options = MEAL_OPTIONS
    elif decision_type == "task":
        options = TASK_OPTIONS
    elif decision_type == "break":
        options = BREAK_OPTIONS
    else:
        return {"suggestion": "No specific options for this decision type.", "rationale": "Invalid decision type.", "details": {}}

    filtered_options = []
    for option in options:
        score = 0

        # --- Scoring Logic based on Google Form Preferences and Context ---
        if decision_type == "meal":
            # Match meal type preference
            if user_prefs.get("meal_pref_type") == option.get("type"):
                score += 3
            # Match cuisine preference (handle list for checkboxes)
            if isinstance(user_prefs.get("meal_pref_cuisine"), list) and option.get("type") in user_prefs.get("meal_pref_cuisine"):
                score += 2
            # Match time availability preference
            if user_prefs.get("meal_pref_time_available") == option.get("time"):
                score += 2
            # Match current mood context
            if context.get("mood") == option.get("mood"):
                score += 1

        elif decision_type == "task":
            # Match task effort preference
            if user_prefs.get("task_pref_effort") == option.get("effort"):
                score += 3
            # Match task type preference (handle list for checkboxes)
            if isinstance(user_prefs.get("task_pref_type"), list) and option.get("type") in user_prefs.get("task_pref_type"):
                score += 2
            # Match quick wins preference
            if user_prefs.get("task_pref_quick_wins") == option.get("time"): # Assuming option.time maps to quick win categories
                score += 2
            # Context: low energy often implies low effort
            if context.get("energy_level") == "low" and option.get("effort") == "low":
                score += 1


        elif decision_type == "break":
            # Match break recharge preference
            if user_prefs.get("break_pref_recharge") == option.get("activity"):
                score += 3
            # Match break location preference (assuming option.type can map to location like "outdoor", "indoor")
            if user_prefs.get("break_pref_location") == option.get("type"):
                score += 2
            # Context: if feeling stressed, passive breaks score higher
            if context.get("feeling") == "Stressed" and option.get("activity") == "passive":
                score += 1


        option["score"] = score
        filtered_options.append(option)

    # Select the best option (or a random one if scores are tied/no strong matches)
    best_option = None
    if filtered_options:
        # Sort by score, highest first
        filtered_options.sort(key=lambda x: x["score"], reverse=True)
        # Get the highest score
        max_score = filtered_options[0]["score"]
        # Find all options that have the maximum score
        top_scorers = [opt for opt in filtered_options if opt["score"] == max_score]
        # Randomly choose one from the top scorers to add some variety
        best_option = random.choice(top_scorers)

    if best_option:
        # Construct the rationale based on what matched
        rationale = f"Based on your preferences and current context, '{best_option['name']}' seems like a great fit."
        
        if decision_type == "meal":
            if user_prefs.get("meal_pref_type") == best_option.get("type"):
                rationale += f" You often prefer {best_option.get('type')} options."
            if user_prefs.get("meal_pref_time_available") == best_option.get("time"):
                rationale += f" It's a '{best_option.get('time')}' option, matching your time availability."
        elif decision_type == "task":
            if user_prefs.get("task_pref_effort") == best_option.get("effort"):
                rationale += f" It's a '{best_option.get('effort')}' effort task, which aligns with your preference."
            if user_prefs.get("task_pref_quick_wins") == best_option.get("time"):
                rationale += f" This is a '{best_option.get('time')}' task, fitting your quick win goal."
        elif decision_type == "break":
            if user_prefs.get("break_pref_recharge") == best_option.get("activity"):
                rationale += f" This is a '{best_option.get('activity')}' activity, which you often prefer for breaks."
            if user_prefs.get("break_pref_location") == best_option.get("type"):
                rationale += f" It's a '{best_option.get('type')}' break, matching your preferred location."

        return {
            "suggestion": best_option["name"],
            "details": best_option, # Keep for debugging/understanding, can be removed in final
            "rationale": rationale
        }
    else:
        return {
            "suggestion": "I'm a bit stumped right now. Maybe try again with different context?",
            "rationale": "No suitable options found based on your preferences.",
            "details": {}
        }