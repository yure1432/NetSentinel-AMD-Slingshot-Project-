import json
import logging
import subprocess
from typing import Dict, List, Optional

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("NetSentinel")


class SlingshotScanner:

    def __init__(self, subnet: str, jar_path: str = "scanner.jar"):
        self.subnet = subnet
        self.jar_path = jar_path

    def scan(self) -> List[Dict]:
        logger.info(f"Starting network scan on {self.subnet}...")
        try:
            result = subprocess.run(
                ["java", "-jar", self.jar_path, self.subnet],
                capture_output=True,
                text=True,
                check=True,
            )
            data = json.loads(result.stdout)
            return data.get("hosts", [])
        except subprocess.CalledProcessError as e:
            logger.error(f"Java Scanner failed: {e.stderr}")
            return []
        except json.JSONDecodeError:
            logger.error("Failed to parse Scanner JSON output.")
            return []


class ReinforcementEngine:

    def __init__(self, scanner: SlingshotScanner):
        from actions import ActionExecutor
        from ai_module import SecurityAnalyzer
        from collector import SystemCollector

        self.scanner = scanner
        self.collector = SystemCollector()
        self.analyzer = SecurityAnalyzer()
        self.executor = ActionExecutor()

    def run(self):
        """Executes the full pipeline[cite: 86]."""
        hosts = self.scanner.scan()
        if not hosts:
            logger.warning("No hosts found. Exiting.")
            return

        for host in hosts:
            ip = host["ip"]
            logger.info(f"Processing {ip}...")

            # State Collection [cite: 89]
            state = self.collector.collect(ip)
            if not state:
                continue

            # AI Analysis [cite: 90]
            recommendations = self.analyzer.analyze(state)

            # Execution [cite: 87, 88]
            for rec in recommendations:
                action = rec.get("action")
                if action and action != "none":
                    self.executor.apply(ip, action)


if __name__ == "__main__":
    SUBNET = "192.168.0.0/24"
    engine = ReinforcementEngine(SlingshotScanner(SUBNET))
    engine.run()
