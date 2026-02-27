import json
import subprocess

from actions import ACTION_MAP
from ai_module import analyze_server
from collector import collect_state
from policy import filter_actions
from scorer import calculate_score

SUBNET = "192.168.0.0/24"


def run_java_scanner():
    result = subprocess.run(
        ["java", "-jar", "scanner.jar", SUBNET], capture_output=True, text=True
    )
    return json.loads(result.stdout)


def reinforce():
    print("Running network scan...")
    scan_data = run_java_scanner()
    servers = [h["ip"] for h in scan_data["hosts"]]

    print("Collecting server states...")
    states = {}
    for ip in servers:
        states[ip] = collect_state(ip)

    print("Analyzing with AI...")
    ai_results = {}
    for ip, state in states.items():
        ai_results[ip] = analyze_server(state)

    print("Applying reinforcement...")
    for stage in ["secure_ssh", "enable_firewall", "patch_system"]:
        print(f"\n=== STAGE: {stage} ===")
        for ip in servers:
            actions = ai_results[ip]
            allowed = filter_actions(actions)

            if stage in allowed:
                ACTION_MAP[stage](ip)

    score = calculate_score(states)
    print(f"\nFinal security score: {score}")


if __name__ == "__main__":
    reinforce()
