# calmpilot_ai_core/test_engine.py

from calmpilot_engine import get_suggestion

if __name__ == "__main__":
    print("--- Testing CalmPilot Engine ---")

    # Test 1: Meal suggestion for default user, quick meal needed
    print("\nTest 1: Lunch suggestion for 'user_default', quick meal needed.")
    context_meal = {"time_available": "quick", "mood": "light"}
    suggestion_meal = get_suggestion("user_default", "meal", context_meal)
    print(f"Suggestion: {suggestion_meal['suggestion']}")
    print(f"Rationale: {suggestion_meal['rationale']}")

    # Test 2: Task suggestion for 'user_b', low energy
    print("\nTest 2: Task suggestion for 'user_b', low energy.")
    context_task = {"energy_level": "low"}
    suggestion_task = get_suggestion("user_b", "task", context_task)
    print(f"Suggestion: {suggestion_task['suggestion']}")
    print(f"Rationale: {suggestion_task['rationale']}")

    # Test 3: Break suggestion for 'user_default', sunny weather
    print("\nTest 3: Break suggestion for 'user_default', sunny weather.")
    context_break = {"weather": "sunny"}
    suggestion_break = get_suggestion("user_default", "break", context_break)
    print(f"Suggestion: {suggestion_break['suggestion']}")
    print(f"Rationale: {suggestion_break['rationale']}")

    print("\n--- Testing Complete ---")