import json
import datetime
from pathlib import Path

JSON_PATH = Path(__file__).parent.parent / "data" / "applied_jobs.json"

def load_data():
    if not JSON_PATH.exists():
        return {"jobs_applied": [], "applications_today": 0, "last_run_date": ""}
    with open(JSON_PATH, "r") as file:
        return json.load(file)

def save_data(data):
    with open(JSON_PATH, "w") as file:
        json.dump(data, file, indent=4)

def reset_daily_limit(data):
    today = datetime.date.today().isoformat()
    if data["last_run_date"] != today:
        data["applications_today"] = 0
        data["last_run_date"] = today
    return data