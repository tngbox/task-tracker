import requests
import json

API_BASE = "http://localhost:8000"

tasks = [
    {"title": "Design homepage layout", "description": "Create mockups", "priority": "High", "status": "ToDo", "assignee": "Alice"},
    {"title": "Build API endpoints", "description": "CRUD routes", "priority": "Medium", "status": "InProgress", "assignee": "Bob"},
    {"title": "Write documentation", "priority": "Low", "status": "Done", "assignee": "Charlie"},
    {"title": "Set up database", "priority": "Medium", "status": "ToDo"},
    {"title": "Fix critical bug", "priority": "High", "status": "InProgress"},
]

for task in tasks:
    try:
        response = requests.post(f"{API_BASE}/tasks", json=task)
        if response.status_code == 201:
            print(f"✓ Created: {task['title']}")
        else:
            print(f"✗ Failed: {task['title']} - Status {response.status_code}")
    except Exception as e:
        print(f"✗ Error creating {task['title']}: {e}")

print("\nDone! Refresh your browser to see the tasks.")
