import json
import os
import re
from typing import Dict, List

from google import genai


class SecurityAnalyzer:
    """Handles interaction with Gemini for server analysis[cite: 90, 91]."""

    def __init__(self):
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set.")

        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-flash-latest"

    def analyze(self, state: Dict) -> List[Dict]:
        prompt = self._build_prompt(state)
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
            )
            return self._parse_json(response.text)
        except Exception as e:
            print(f"AI Error: {e}")
            return []

    def _build_prompt(self, state: Dict) -> str:
        return f"""
        You are a Linux server security assistant. Detect issues and return ONLY JSON.
        Rules:
        - ssh_password_auth true -> secure_ssh
        - firewall_enabled false -> enable_firewall
        - outdated_packages not empty -> patch_system
        Format: [{{"issue": "...", "severity": "high", "action": "secure_ssh"}}]
        Server state: {json.dumps(state)}
        """

    def _parse_json(self, text: str) -> List[Dict]:
        """Cleans Markdown formatting before parsing."""
        cleaned = re.sub(r"```json|```", "", text).strip()
        return json.loads(cleaned)
