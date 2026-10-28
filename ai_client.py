import datetime
import json
import os
from google import genai
from google.genai import types

MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.8-flash")
DAILY_LIMIT = int(os.environ.get("DAILY_CALL_LIMIT", "20"))
QUOTA_FILE = "quota.json"

def check_quota():
    today = datetime.date.today().isoformat()
    data = {"date": today, "calls": 0}
    if os.path.exists(QUOTA_FILE):
        with open(QUOTA_FILE) as f:
            saved = json.load(f)
        if saved.get("date") == today:
            data = saved
    if data["calls"] >= DAILY_LIMIT:
        raise RuntimeError("Daily call limit reached. Stopping on purpose.")
    data["calls"] += 1
    with open(QUOTA_FILE, "w") as f:
        json.dump(data, f)
    return data["calls"]

def ask_json(system_prompt, user_content):
    check_quota()
    client = genai.Client()
    response = client.models.generate_content(
        model=MODEL,
        contents=user_content,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            response_mime_type="application/json",
            temperature=0.2,
        ),
    )
    return json.loads(response.text)
