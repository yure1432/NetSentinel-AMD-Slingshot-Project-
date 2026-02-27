import json
import logging
import os
import subprocess
from typing import Dict, List

from actions import ActionExecutor
from ai_module import SecurityAnalyzer
from collector import SystemCollector

# config + logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("NetSentinel")

# main scanner logic


class JavaScanner:

    def __init__(self, subnet: str, jar_path: str = "scanner.jar"):
        self.subnet = subnet
        self.jar_path = jar_path

    def scan(self) -> List[Dict]:
        """Runs the Java JAR and parses the JSON output."""
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


# main function


class MainFunction:

    def __init__(self, scanner: JavaScanner):
        self.scanner = scanner
        self.collector = SystemCollector()
        self.analyzer = SecurityAnalyzer()
        self.executor = ActionExecutor()

    def run(self):
        hosts = self.scanner.scan()
        if not hosts:
            logger.warning("No hosts found. Exiting.")
            return

        for host in hosts:
            ip = host["ip"]
            logger.info(f"Processing {ip}...")

            state = self.collector.collect(ip)
            if not state:
                continue

            recommendations = self.analyzer.analyze(state)

            for rec in recommendations:
                action = rec.get("action")
                if action and action != "none":
                    self.executor.apply(ip, action)


# execution

if __name__ == "__main__":
    if "GEMINI_API_KEY" not in os.environ:
        logger.error("GEMINI_API_KEY environment variable is missing!")
        exit(1)

    TARGET_SUBNET = "192.168.1.0/24"

    scanner_instance = JavaScanner(TARGET_SUBNET)
    master = MainFunction(scanner_instance)

    logger.info("=== NetSentinel Master Pipeline Started ===")
    master.run()
