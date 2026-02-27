import json
import os
import re
from typing import Dict, List

from google import genai


class SecurityAnalyzer:

    def __init__(self):
        self.api_key = os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable is missing!")
        self.client = genai.Client(api_key=self.api_key)
        self.model = "gemini-flash-latest"

    def analyze(self, state: Dict) -> List[Dict]:
        prompt = f"""
        Analyze the following server state and return a JSON list of security actions.
        PRIORITY HIERARCHY:
        1. CRITICAL: empty_password_accounts, world_writable_configs (Action: fix_config_perms)
        2. HIGH: ssh_root_login (Action: disable_root_ssh), ssh_password_auth (Action: secure_ssh)
        3. MEDIUM: insecure_services_active (Action: remove_insecure_services), firewall_enabled (Action: enable_firewall)
        4. LOW: outdated_packages (Action: patch_system), firewall_logging (Action: enable_fw_logging)
        Available Actions: secure_ssh, disable_root_ssh, enable_firewall, enable_fw_logging, patch_system, remove_insecure_services, fix_config_perms.
        Server State: {json.dumps(state)}
        Return ONLY a valid JSON list. Format: [{{"issue": "...", "severity": "...", "action": "..."}}]
        """
        try:
            response = self.client.models.generate_content(
                model=self.model, contents=prompt
            )
            return self._parse_json(response.text or "")
        except Exception:
            return []

    def _parse_json(self, text: str) -> List[Dict]:
        cleaned = re.sub(r"```json|```", "", text).strip()
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            return []
