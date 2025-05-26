# calmpilot_ai_core/decision_data.py

MEAL_OPTIONS = [
    {"id": "meal_1", "name": "Indian Thali", "type": "Indian", "time": "medium", "mood": "heavy"},
    {"id": "meal_2", "name": "Quick Sandwich", "type": "Western", "time": "quick", "mood": "light"},
    {"id": "meal_3", "name": "South Indian Dosa", "type": "Indian", "time": "medium", "mood": "medium"},
    {"id": "meal_4", "name": "Salad Bowl", "type": "Healthy", "time": "quick", "mood": "light"},
    {"id": "meal_5", "name": "Pizza Slice", "type": "Western", "time": "quick", "mood": "heavy"},
]

TASK_OPTIONS = [
    {"id": "task_1", "name": "Clear Inbox (5 mins)", "type": "digital", "time": "quick", "effort": "low"},
    {"id": "task_2", "name": "Organize Downloads (10 mins)", "type": "digital", "time": "medium", "effort": "medium"},
    {"id": "task_3", "name": "Quick Desk Tidy (5 mins)", "type": "physical", "time": "quick", "effort": "low"},
    {"id": "task_4", "name": "Reply to that one email (3 mins)", "type": "digital", "time": "very_quick", "effort": "low"},
    {"id": "task_5", "name": "Plan next 3 tasks (10 mins)", "type": "planning", "time": "medium", "effort": "medium"},
]

BREAK_OPTIONS = [
    {"id": "break_1", "name": "Listen to a Calm Song (5 mins)", "type": "audio", "activity": "passive"},
    {"id": "break_2", "name": "Quick Stretch (5 mins)", "type": "physical", "activity": "active"},
    {"id": "break_3", "name": "Step Outside (10 mins)", "type": "outdoor", "activity": "active"},
    {"id": "break_4", "name": "Mindful Breathing (3 mins)", "type": "mental", "activity": "passive"},
    {"id": "break_5", "name": "Read one page of a book (5 mins)", "type": "reading", "activity": "passive"},
]