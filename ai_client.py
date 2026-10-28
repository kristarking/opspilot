import json
import os
from google import genai
from google.genai import types

MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.8-flash")

def ask_json(system_prompt, user_content):
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
