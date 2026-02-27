import json
import os

from google import genai

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

MODEL = "gemini-flash-latest"


def analyze_server(state):
    prompt = f"""
You are a Linux server security assistant.

Detect issues and return ONLY JSON.

Rules:
- ssh_password_auth true → secure_ssh
- firewall_enabled false → enable_firewall
- outdated_packages not empty → patch_system

Format:
[
  {{
    "issue": "...",
    "severity": "high|medium|low",
    "action": "secure_ssh|enable_firewall|patch_system|none"
  }}
]

Server state:
{json.dumps(state)}
"""

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt,
        )

        text = response.text.strip()

        return json.loads(text)

    except Exception as e:
        print("Gemini error:", e)
        return []
