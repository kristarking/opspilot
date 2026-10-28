import datetime
import hashlib
import json
import os
from google import genai
from google.genai import types

MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.8-flash")
DAILY_LIMIT = int(os.environ.get("DAILY_CALL_LIMIT", "15"))
QUOTA_FILE = "quota.json"
CACHE_DIR = "cache"

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

def cache_path(system_prompt, user_content):
    text = MODEL + system_prompt + user_content
    key = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return os.path.join(CACHE_DIR, key + ".json")

def ask_json(system_prompt, user_content):
    path = cache_path(system_prompt, user_content)
    use_cache = os.environ.get("OPSPILOT_NO_CACHE") != "1"
    if use_cache and os.path.exists(path):
        with open(path) as f:
            return json.load(f)
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
    result = json.loads(response.text)
    os.makedirs(CACHE_DIR, exist_ok=True)
    with open(path, "w") as f:
        json.dump(result, f)
    return result
